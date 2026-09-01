"""Digital Document Scanner - live web demo.

Wraps document_scanner.py (the original CLI tool) in a small Flask app:
upload a photo of a document, get back a clean scanned version, viewed
inline and downloadable.
"""
import base64
import io
import logging
import os
import sys
import uuid

import cv2
import numpy as np
from flask import Flask, render_template, request, send_file, abort

# document_scanner.py lives one directory up (repo root).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from document_scanner import detect_document_contour, four_point_transform, apply_scan_effect  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}
MAX_CONTENT_LENGTH = 12 * 1024 * 1024  # 12 MB

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Scanned results are cached in memory only, keyed by a random id, so the
# result page can offer a "download" link without writing files to disk
# (which wouldn't persist across gunicorn workers/restarts anyway).
_results = {}
MAX_CACHED_RESULTS = 50


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_png_base64(image):
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Failed to encode image")
    return base64.b64encode(buffer).decode("ascii"), buffer.tobytes()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    file = request.files.get("image")
    if not file or file.filename == "":
        return render_template("index.html", message="Please choose an image to scan.")

    if not allowed_file(file.filename):
        return render_template("index.html", message="Unsupported file type. Use JPG, PNG, WEBP, or BMP.")

    method = request.form.get("method", "adaptive")
    if method not in ("adaptive", "otsu", "simple"):
        method = "adaptive"

    file_bytes = file.read()
    if not file_bytes:
        return render_template("index.html", message="That file looks empty.")

    npbuf = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(npbuf, cv2.IMREAD_COLOR)
    if image is None:
        return render_template("index.html", message="Couldn't read that as an image.")

    try:
        doc_cnt = detect_document_contour(image)
        if doc_cnt is not None:
            warped = four_point_transform(image, doc_cnt)
            detected = True
        else:
            warped = image
            detected = False

        scanned = apply_scan_effect(warped, method=method)
    except Exception:
        logger.exception("Scan pipeline failed")
        return render_template("index.html", message="Something went wrong processing that image. Try a different photo.")

    original_b64, _ = encode_png_base64(image)
    scanned_b64, scanned_bytes = encode_png_base64(scanned)

    result_id = uuid.uuid4().hex
    if len(_results) >= MAX_CACHED_RESULTS:
        _results.pop(next(iter(_results)))
    _results[result_id] = scanned_bytes

    return render_template(
        "index.html",
        original_b64=original_b64,
        scanned_b64=scanned_b64,
        detected=detected,
        method=method,
        result_id=result_id,
    )


@app.route("/download/<result_id>")
def download(result_id):
    data = _results.get(result_id)
    if data is None:
        abort(404)
    return send_file(
        io.BytesIO(data),
        mimetype="image/png",
        as_attachment=True,
        download_name="scanned-document.png",
    )


@app.route("/health")
def health():
    return {"status": "ok"}


@app.errorhandler(413)
def too_large(_error):
    return render_template("index.html", message="That image is too large (12 MB max)."), 413


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", code=500, message="Something went wrong."), 500


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug_mode)
