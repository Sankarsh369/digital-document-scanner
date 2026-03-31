# Digital Document Scanner

Transform messy, shadowed, or skewed photos of documents into clean, high-contrast "scanned" versions using computer vision.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

The **Digital Document Scanner** is a Python-based computer vision application that converts smartphone photos of documents into crisp, professional-looking scans. It automatically detects paper boundaries, corrects perspective distortion, and applies thresholding to produce high-contrast black-and-white outputs suitable for printing, archiving, or sharing.

### The Problem

Taking photos of handwritten notes, printed documents, or receipts often results in:
- **Shadows and uneven lighting** that make text hard to read
- **Skewed angles and perspective distortion** from non-perpendicular camera positioning
- **Low contrast** that reduces legibility when printed or viewed on different screens
- **Distracting backgrounds** that make the document less professional-looking

This project solves these issues by applying fundamental computer vision techniques learned in the course.

## ✨ Features

- **Automatic Document Detection**: Uses edge detection and contour analysis to locate paper boundaries
- **Perspective Correction**: Applies homography transforms to produce a flat, bird's-eye view
- **Adaptive Thresholding**: Handles uneven lighting conditions for consistent results
- **Multiple Thresholding Methods**: Choose between adaptive, Otsu's, or simple thresholding
- **Debug Mode**: Visualize intermediate processing steps for learning and troubleshooting
- **Manual Override**: Process entire images when automatic detection isn't needed

## 🎓 Course Concepts Applied

This project demonstrates practical application of the following computer vision concepts:

1. **Grayscale Conversion** - Simplifies image processing by reducing color information
2. **Gaussian Blur** - Removes noise before edge detection to improve accuracy
3. **Canny Edge Detection** - Identifies strong gradients that represent paper edges
4. **Contour Detection** - Locates closed regions and identifies the document boundary
5. **Morphological Operations** - Uses dilation to close gaps in detected edges
6. **Perspective Transform (Homography)** - Corrects skew and produces flat document views
7. **Adaptive Thresholding** - Creates crisp black-and-white output while handling lighting variations

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/digital-document-scanner.git
   cd digital-document-scanner
   ```

2. **Install dependencies**
   ```bash
   pip install opencv-python numpy
   ```

   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python document_scanner.py --help
   ```

## 📖 Usage

### Basic Usage

Convert a document photo to a scanned version:

```bash
python document_scanner.py input_photo.jpg output_scan.jpg
```

### Advanced Options

**Choose a thresholding method:**
```bash
# Adaptive thresholding (default, best for varying lighting)
python document_scanner.py photo.jpg scan.jpg --method adaptive

# Otsu's method (good for uniform lighting)
python document_scanner.py photo.jpg scan.jpg --method otsu

# Simple threshold (fastest, less adaptive)
python document_scanner.py photo.jpg scan.jpg --method simple
```

**Enable debug mode to see processing steps:**
```bash
python document_scanner.py photo.jpg scan.jpg --debug
```

**Process entire image without automatic detection:**
```bash
python document_scanner.py photo.jpg scan.jpg --force-full
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `input` | Path to input image file | Required |
| `output` | Path for output scanned image | Required |
| `--method` | Thresholding method: `adaptive`, `otsu`, or `simple` | `adaptive` |
| `--debug` | Show intermediate processing windows | `False` |
| `--force-full` | Skip document detection, process entire image | `False` |

## 🔍 How It Works

### Processing Pipeline

1. **Image Loading & Resizing**
   - Load the input image
   - Resize to 800px max dimension for faster processing

2. **Document Detection**
   - Convert to grayscale
   - Apply Gaussian blur (5×5 kernel) to reduce noise
   - Detect edges using Canny algorithm (thresholds: 75, 200)
   - Dilate edges to close small gaps
   - Find contours and identify the largest quadrilateral

3. **Perspective Correction**
   - Order corner points (top-left, top-right, bottom-right, bottom-left)
   - Calculate destination rectangle dimensions
   - Apply perspective transform to get flat view

4. **Scan Effect**
   - Convert to grayscale
   - Apply chosen thresholding method for high-contrast output
   - Save the final scanned image

### Thresholding Methods Explained

**Adaptive Thresholding** (Recommended)
- Calculates threshold locally for small regions
- Handles varying lighting conditions
- Best for documents with shadows or uneven illumination
- Parameters: 11×11 block size, constant C=10

**Otsu's Method**
- Automatically determines optimal global threshold
- Works well for images with bimodal histograms
- Good for uniformly lit documents
- Faster than adaptive thresholding

**Simple Thresholding**
- Uses fixed threshold value (128)
- Fastest method
- Best for high-quality, evenly-lit images


## 💡 Example Use Cases

1. **Student Notes**: Digitize handwritten class notes for easy sharing and backup
2. **Receipts**: Create clean scans of receipts for expense tracking or tax purposes
3. **Contracts**: Convert signed paper contracts to professional digital versions
4. **Whiteboards**: Capture and clean up whiteboard content from meetings
5. **Book Pages**: Create readable scans of textbook pages or articles

## 🐛 Troubleshooting

**Problem: Document not detected automatically**
- Solution: Use `--force-full` flag to process the entire image
- Ensure the document has clear edges against the background
- Try adjusting lighting conditions for better contrast

**Problem: Output is too dark or too light**
- Solution: Try different thresholding methods (`--method otsu` or `--method simple`)
- Ensure input image has reasonable lighting

**Problem: Perspective correction is incorrect**
- Solution: Make sure the document is the largest quadrilateral in the image
- Remove other papers or objects from the background
- Use `--debug` to visualize detected contours

**Problem: ImportError for cv2**
- Solution: Reinstall OpenCV: `pip install --upgrade opencv-python`

## 🔬 Technical Details

### Algorithm Parameters

- **Canny Edge Detection**: Low threshold = 75, High threshold = 200
- **Gaussian Blur**: Kernel size = 5×5, Sigma = 0 (auto-calculated)
- **Contour Approximation**: Epsilon = 2% of perimeter
- **Adaptive Threshold**: Block size = 11, Constant C = 10
- **Morphological Dilation**: 3×3 rectangular kernel, 2 iterations

### Performance Considerations

- Images are resized to 800px max dimension for processing speed
- Contour search limited to top 5 largest contours
- Coordinate scaling preserves original image quality in output

## 🤝 Contributing

Contributions are welcome! Here are ways you can help:

1. Report bugs or suggest features via GitHub Issues
2. Submit pull requests with improvements
3. Add example images demonstrating edge cases
4. Improve documentation

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/digital-document-scanner.git
cd digital-document-scanner
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Course: [Computer Vision Course Name]
- OpenCV Documentation: https://docs.opencv.org/
- Inspired by real-world document scanning needs in academic and professional settings

## 📞 Contact

- **Author**: [S Sankarsha]
- **Email**: [Sankarshsreekulam@gmail.com]
- **GitHub**: [@Sankarsh369](https://github.com/Sankarsh369)
- **Project Link**: https://github.com/Sankarsh369/digital-document-scanner

---

**Made with ❤️ for better document digitization**
