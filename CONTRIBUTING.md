# Contributing to Digital Document Scanner

First off, thank you for considering contributing to Digital Document Scanner! It's people like you that make this tool better for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide sample images** (if the issue is image-specific)
* **Describe the behavior you observed** and what you expected
* **Include your environment**: OS, Python version, OpenCV version

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

* **Use a clear and descriptive title**
* **Provide a detailed description** of the proposed feature
* **Explain why this enhancement would be useful** to most users
* **List any alternative solutions** you've considered

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include comments for complex algorithms
* Update the README.md if you change functionality
* Add test cases for new features

## Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/Sankarsh369/digital-document-scanner.git
cd digital-document-scanner

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scanner
python document_scanner.py examples/input/sample.jpg test_output.jpg --debug
```

## Code Style

* Follow PEP 8 guidelines
* Use descriptive variable names
* Add docstrings to all functions
* Comment complex algorithms
* Keep functions focused and modular

## Testing

Before submitting a pull request:

1. Test your changes with various image types
2. Verify both automatic detection and manual modes work
3. Run with `--debug` flag to check intermediate results
4. Test on different operating systems if possible

## Community

* Be respectful and welcoming
* Help others learn
* Give constructive feedback
* Assume good intentions

Thank you for contributing! 🎉
