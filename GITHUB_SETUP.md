# GitHub Repository Setup Guide

This guide will help you set up your Digital Document Scanner project on GitHub.

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com and log in
2. Click the "+" icon in the top-right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `digital-document-scanner`
   - **Description**: "Transform document photos into clean scans using computer vision"
   - **Visibility**: Public (recommended for academic projects)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Initialize Your Local Repository

Open terminal/command prompt in your project folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make your first commit
git commit -m "Initial commit: Digital Document Scanner with full documentation"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/digital-document-scanner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR-USERNAME`** with your actual GitHub username!

## Step 3: Verify Your Repository

1. Go to your repository on GitHub
2. You should see all files:
   - `document_scanner.py` (main code)
   - `README.md` (comprehensive documentation)
   - `requirements.txt` (dependencies)
   - `LICENSE` (MIT license)
   - `.gitignore` (ignore unnecessary files)
   - `CONTRIBUTING.md` (contribution guidelines)

## Step 4: Add Topics/Tags

1. On your repository page, click the gear icon next to "About"
2. Add topics: `computer-vision`, `opencv`, `python`, `document-scanner`, `image-processing`, `edge-detection`
3. Click "Save changes"

## Step 5: Create Example Directories (Optional but Recommended)

```bash
# Create directories for examples
mkdir -p examples/input examples/output

# Add sample images to examples/input/
# Process them and save to examples/output/

# Commit the examples
git add examples/
git commit -m "Add example input and output images"
git push
```

## Step 6: Enable GitHub Pages for Documentation (Optional)

1. Go to repository Settings
2. Scroll to "GitHub Pages" section
3. Select source: main branch, /root folder
4. Your README will be visible at: `https://YOUR-USERNAME.github.io/digital-document-scanner/`

## Best Practices for Academic Projects

### Regular Commits
Show your development process with meaningful commits:
```bash
git commit -m "Implement edge detection pipeline"
git commit -m "Add adaptive thresholding support"
git commit -m "Fix corner ordering bug"
git commit -m "Add debug visualization mode"
```

### Meaningful Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix perspective transform for landscape images" not "Fix bug"
- Reference issues: "Fix #3: Handle images without clear edges"

### Branch for Features (Advanced)
```bash
# Create a feature branch
git checkout -b add-batch-processing

# Make changes and commit
git add .
git commit -m "Add batch processing capability"

# Push branch
git push -u origin add-batch-processing

# Create pull request on GitHub
# Merge when ready
```

## Demonstrating Development History

For academic evaluation, your commit history should show:
- Progressive development (not one massive commit)
- Bug fixes and improvements
- Documentation updates
- Testing iterations

Example timeline:
```
Initial commit: Project structure and basic detection
Add Canny edge detection implementation
Implement perspective transform
Add adaptive thresholding
Fix contour detection edge cases
Add command-line interface
Write comprehensive README
Create project report
Add examples and test cases
Final documentation polish
```

## Troubleshooting

**Problem**: `git push` asks for username/password repeatedly
- **Solution**: Set up SSH keys or use Personal Access Token
- Guide: https://docs.github.com/en/authentication

**Problem**: Files too large to push
- **Solution**: Add large files to `.gitignore` or use Git LFS
- For this project, example images should be <5MB each

**Problem**: Merge conflicts
- **Solution**: Pull latest changes before pushing
```bash
git pull origin main
# Resolve conflicts if any
git add .
git commit -m "Resolve merge conflicts"
git push
```

## For Submission

When submitting to VITyarthi:
1. **Repository URL**: Provide direct link: `https://github.com/YOUR-USERNAME/digital-document-scanner`
2. **README**: Already in repository (shows on main page)
3. **Project Report**: Upload the DOCX file separately

Your repository demonstrates:
- ✅ Clean, well-organized code
- ✅ Comprehensive documentation
- ✅ Professional presentation
- ✅ Real development process (if you commit regularly)
- ✅ Open-source best practices

Good luck with your project! 🚀
