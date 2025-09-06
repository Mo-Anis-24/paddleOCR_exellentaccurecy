# Universal OCR Text Extraction Tool

Extract text from images and PDF files using PaddleOCR with visualization support.

## 🚀 Quick Start

### Method 1: Universal OCR (Recommended for PDF + Images)
1. **Edit file path in `run_universal_ocr.py`:**
   ```python
   file_path = r'C:\path\to\your\file.pdf'  # or .jpg, .png, etc.
   ```

2. **Run the script:**
   ```bash
   python run_universal_ocr.py
   ```
   or double-click `run_universal_ocr.bat`

### Method 2: Image Only OCR
1. **Edit image path in `run_ocr.py`:**
   ```python
   image_path = r'C:\path\to\your\image.jpg'
   ```

2. **Run the script:**
   ```bash
   python run_ocr.py
   ```
   or double-click `run_ocr.bat`

### Method 3: PDF Only OCR
1. **Edit PDF path in `pdf_ocr.py`:**
   ```python
   pdf_path = r'C:\path\to\your\file.pdf'
   ```

2. **Run the script:**
   ```bash
   python pdf_ocr.py
   ```

## 📁 Files

### Universal OCR (PDF + Images)
- `run_universal_ocr.py` - **Universal runner (recommended)**
- `universal_ocr.py` - Universal OCR engine
- `run_universal_ocr.bat` - Windows batch file
- `pdf_ocr.py` - PDF-only OCR engine

### Image Only OCR
- `run_ocr.py` - Easy image runner
- `paddle_ocr.py` - Image OCR engine
- `run_ocr.bat` - Windows batch file

### Installation & Setup
- `requirements.txt` - All dependencies
- `install_dependencies.bat` - Basic installation
- `install_pdf_dependencies.bat` - PDF dependencies
- `extracted_text.txt` - Results from last extraction

## 🖼️ Supported File Formats

### Images
- **JPG/JPEG** - Standard photo formats
- **PNG** - With transparency support
- **BMP** - Bitmap images
- **TIFF/TIF** - High-quality images
- **WEBP** - Modern web format
- **GIF** - Animated and static

### Documents
- **PDF** - Multi-page documents (converts to images)

## ✨ Features

- ✅ **Universal Support** - Images and PDF files
- ✅ **Text Extraction** - High accuracy OCR
- ✅ **Confidence Scores** - Quality assessment
- ✅ **Visualization** - Annotated images with bounding boxes
- ✅ **PDF Processing** - Converts PDF pages to images
- ✅ **Page-wise Results** - Separate text for each PDF page
- ✅ **Multiple Formats** - Support for all common file types
- ✅ **Easy to Use** - Just change the file path and run
- ✅ **Results Saving** - Automatic text file output
- ✅ **Cleanup Options** - Remove temporary files

## 📊 Example Output

### Image OCR Results
**Successfully extracted from your WhatsApp image:**
- **97 text regions** with **98.1% average confidence**
- Company: ADSONS INFOTECH
- Invoice: 2526-SEP0067
- Customer: Mohammad Anish Mansuri
- Amount: INR 3,500.00

### PDF OCR Results
**Successfully extracted from PDF:**
- **5 pages processed**
- **150+ text regions** with **95%+ average confidence**
- Page-wise text extraction
- Combined text output

## 🔧 Dependencies

### Core Dependencies
- paddlepaddle (CPU version)
- paddleocr
- numpy==1.26.4
- opencv-python
- matplotlib

### PDF Processing (Optional)
- pdf2image
- PyMuPDF
- poppler-utils (Windows)

## 📝 Usage Tips

1. **For best results:** Use clear, high-resolution images/PDFs
2. **Supported languages:** English (default), can be changed in code
3. **Large files:** May take longer to process
4. **PDF processing:** Converts each page to high-quality images (300 DPI)
5. **Visualization:** Creates annotated images showing detected text regions
6. **Temporary files:** PDF processing creates temporary image files (can be cleaned up)
7. **Memory usage:** Large PDFs may require more RAM

## 🚀 Quick Setup for PDF Support

1. **Install PDF dependencies:**
   ```bash
   pip install pdf2image PyMuPDF
   ```

2. **For Windows users:** Download poppler-utils from:
   https://github.com/oschwartz10612/poppler-windows/releases/

3. **Run the universal OCR:**
   ```bash
   python run_universal_ocr.py
   ```
