"""
Digital Document Scanner
========================
Transforms messy, shadowed, or skewed photos of documents into
clean, high-contrast "scanned" versions using OpenCV.

Course Concepts Applied:
  - Grayscale Conversion
  - Gaussian Blur
  - Canny Edge Detection
  - Contour Detection
  - Perspective Transform (Homography)
  - Adaptive Thresholding
"""

import cv2
import numpy as np
import argparse
import os
import sys


# ─────────────────────────────────────────────
# 1. UTILITY HELPERS
# ─────────────────────────────────────────────

def order_points(pts):
    """
    Order four corner points as: [top-left, top-right, bottom-right, bottom-left].
    Required for a consistent perspective transform.
    """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left  → smallest sum
    rect[2] = pts[np.argmax(s)]   # bot-right → largest  sum
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right → smallest diff
    rect[3] = pts[np.argmax(diff)]  # bot-left  → largest  diff
    return rect


def four_point_transform(image, pts):
    """
    Apply a perspective (bird's-eye) transform to the detected paper region.
    Returns a top-down, de-skewed crop of the document.
    """
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Compute the width of the new image
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    # Compute the height of the new image
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # Destination points for the "flat" view
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))
    return warped


# ─────────────────────────────────────────────
# 2. DOCUMENT DETECTION
# ─────────────────────────────────────────────

def detect_document_contour(image, debug=False):
    """
    Detect the largest quadrilateral in the image (assumed to be the paper).

    Pipeline:
      1. Convert to grayscale
      2. Gaussian Blur  → removes noise before edge detection
      3. Canny Edge Detection → finds strong gradients (paper edges)
      4. Dilate edges  → closes small gaps in the outline
      5. Find contours → locate closed regions
      6. Pick the largest 4-sided contour → the paper

    Returns the four corner points (numpy array, shape 4×2) or None.
    """
    orig_h, orig_w = image.shape[:2]

    # ── Step 1: Resize for faster processing (keep aspect ratio) ──
    scale = 800.0 / max(orig_h, orig_w)
    resized = cv2.resize(image, (int(orig_w * scale), int(orig_h * scale)))

    # ── Step 2: Grayscale Conversion ──────────────────────────────
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # ── Step 3: Gaussian Blur ──────────────────────────────────────
    # kernel (5,5) smooths noise; sigma=0 = auto-calculated
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # ── Step 4: Canny Edge Detection ──────────────────────────────
    # Thresholds (75, 200): lower catches weak edges, upper keeps strong ones
    edges = cv2.Canny(blurred, 75, 200)

    if debug:
        cv2.imshow("DEBUG: Grayscale", gray)
        cv2.imshow("DEBUG: Blurred",   blurred)
        cv2.imshow("DEBUG: Canny Edges", edges)
        cv2.waitKey(0)

    # ── Step 5: Dilate to close edge gaps ─────────────────────────
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # ── Step 6: Find & filter contours ────────────────────────────
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area descending; examine top-5 candidates
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    doc_cnt = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        # approxPolyDP simplifies the contour; epsilon = 2% of perimeter
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:          # quadrilateral found
            doc_cnt = approx
            break

    if doc_cnt is None:
        return None

    # Scale corner coordinates back to original image size
    doc_cnt = (doc_cnt / scale).astype("float32")
    return doc_cnt.reshape(4, 2)


# ─────────────────────────────────────────────
# 3. SCAN EFFECT (Thresholding)
# ─────────────────────────────────────────────

def apply_scan_effect(image, method="adaptive"):
    """
    Convert a de-skewed image into a crisp black-and-white "scan".

    method = 'adaptive'  : handles uneven lighting (recommended)
    method = 'otsu'      : global threshold – fast, good for uniform lighting
    method = 'simple'    : fixed threshold at 128
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if method == "adaptive":
        # blockSize=11 – neighbourhood size; C=10 – constant subtracted from mean
        scanned = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11, C=10
        )
    elif method == "otsu":
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, scanned = cv2.threshold(
            blurred, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:  # simple / fallback
        _, scanned = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    return scanned


# ─────────────────────────────────────────────
# 4. MAIN SCAN PIPELINE
# ─────────────────────────────────────────────

def scan_document(input_path, output_path, method="adaptive",
                  debug=False, force_full=False):
    """
    Full document-scanning pipeline.

    Args:
        input_path  : Path to the source photo.
        output_path : Where to save the scanned output.
        method      : Thresholding method ('adaptive', 'otsu', 'simple').
        debug       : Show intermediate windows if True.
        force_full  : Skip contour detection; process the whole image.

    Returns:
        True on success, False on failure.
    """
    # ── Load image ────────────────────────────────────────────────
    image = cv2.imread(input_path)
    if image is None:
        print(f"[ERROR] Cannot read image: {input_path}")
        return False

    print(f"[INFO] Loaded '{input_path}'  ({image.shape[1]}×{image.shape[0]} px)")

    if force_full:
        print("[INFO] Skipping contour detection – processing full image.")
        warped = image
    else:
        # ── Detect paper contour ──────────────────────────────────
        print("[INFO] Detecting document edges …")
        doc_cnt = detect_document_contour(image, debug=debug)

        if doc_cnt is None:
            print("[WARN] No quadrilateral found. Processing full image instead.")
            warped = image
        else:
            print("[INFO] Document detected. Applying perspective transform …")
            warped = four_point_transform(image, doc_cnt)

            if debug:
                # Draw the detected contour on a copy for visual inspection
                vis = image.copy()
                cv2.drawContours(vis, [doc_cnt.astype(int)], -1, (0, 255, 0), 3)
                cv2.imshow("DEBUG: Detected Contour", vis)
                cv2.waitKey(0)

    # ── Apply scan effect ─────────────────────────────────────────
    print(f"[INFO] Applying '{method}' thresholding …")
    scanned = apply_scan_effect(warped, method=method)

    # ── Save output ───────────────────────────────────────────────
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, scanned)
    print(f"[INFO] Scanned image saved → '{output_path}'")

    if debug:
        cv2.imshow("Final Scanned Output", scanned)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return True


# ─────────────────────────────────────────────
# 5. CLI ENTRY POINT
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Digital Document Scanner – turn a photo into a crisp scan."
    )
    parser.add_argument("input",  help="Path to the input image (JPG/PNG/etc.)")
    parser.add_argument("output", help="Path for the scanned output image")
    parser.add_argument(
        "--method", choices=["adaptive", "otsu", "simple"],
        default="adaptive",
        help="Thresholding method (default: adaptive)"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Show intermediate debug windows"
    )
    parser.add_argument(
        "--force-full", action="store_true",
        help="Skip document detection; process the entire image"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    success = scan_document(
        args.input,
        args.output,
        method=args.method,
        debug=args.debug,
        force_full=args.force_full
    )
    sys.exit(0 if success else 1)