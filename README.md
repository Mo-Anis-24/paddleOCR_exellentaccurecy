# Universal OCR Text Extraction Tool - Modular Version

A comprehensive, modular OCR solution for extracting text from images and PDFs using PaddleOCR.

## 🏗️ Modular Architecture

The tool is now organized into separate, focused modules for better understanding and maintenance:

### 📁 Core Modules

#### 1. `pdf_converter.py` - PDF Processing
- **Purpose**: Convert PDF files to images for OCR processing
- **Features**:
  - PDF to image conversion using `pdf2image` and `PyMuPDF`
  - PDF metadata extraction
  - Temporary file cleanup
  - Multiple DPI support
- **Key Functions**:
  - `convert_pdf_to_images()` - Convert PDF pages to PNG images
  - `get_pdf_info()` - Extract PDF metadata
  - `cleanup_temp_files()` - Remove temporary files

#### 2. `ocr_extractor.py` - Text Extraction
- **Purpose**: Extract text from images using PaddleOCR
- **Features**:
  - Multi-language OCR support
  - Confidence scoring
  - Batch processing
  - Multiple image format support
- **Key Functions**:
  - `OCRProcessor` class - Main OCR processing class
  - `extract_text_from_image()` - Extract text from single image
  - `batch_extract_text()` - Process multiple images

#### 3. `visualizer.py` - Visualization Creation
- **Purpose**: Create visualizations showing OCR results
- **Features**:
  - Annotated images with bounding boxes
  - Confidence score display
  - Summary visualizations
  - Confidence histograms
- **Key Functions**:
  - `VisualizationCreator` class - Main visualization class
  - `create_page_visualization()` - Create single page visualization
  - `create_summary_visualization()` - Create summary charts

#### 4. `text_processor.py` - Text Processing & Saving
- **Purpose**: Process, format, and save OCR results
- **Features**:
  - Multiple output formats (TXT, JSON, CSV)
  - Text search functionality
  - Statistics generation
  - Page-wise organization
- **Key Functions**:
  - `TextProcessor` class - Main text processing class
  - `save_to_txt()` - Save as text file
  - `save_to_json()` - Save as JSON
  - `save_to_csv()` - Save as CSV
  - `search_text()` - Search within extracted text

#### 5. `main_ocr_app.py` - Main Application
- **Purpose**: Orchestrate all modules for complete OCR workflow
- **Features**:
  - Unified interface for all operations
  - Automatic file type detection
  - Complete workflow management
  - User-friendly output

## 🚀 Quick Start

### Method 1: Interactive OCR Tool (Recommended)
**The easiest way to use the tool - just run and follow the prompts!**

1. **Run the interactive tool:**
   ```bash
   python simple_ocr.py
   ```
   or double-click `run_simple_ocr.bat`

2. **Follow the prompts:**
   - Enter your file path (image or PDF)
   - Choose language (English, Chinese, French, etc.)
   - Choose whether to create visualizations
   - Set output file name
   - Confirm and let it process!

### Method 2: Advanced Application
**For users who want more control over settings**

1. **Run the main application:**
   ```bash
   python main_ocr_app.py
   ```
   or double-click `run_ocr.bat`

2. **The tool will ask you for:**
   - File path to process
   - OCR language preference
   - Visualization options
   - Output file names

### Method 3: Use Individual Modules
```python
# Example: Process a PDF
from pdf_converter import convert_pdf_to_images
from ocr_extractor import OCRProcessor
from visualizer import VisualizationCreator
from text_processor import TextProcessor

# Convert PDF to images
image_paths = convert_pdf_to_images("document.pdf")

# Extract text from each image
ocr = OCRProcessor()
results = []
for image_path in image_paths:
    texts, scores, boxes = ocr.extract_text_from_image(image_path)
    results.append({'texts': texts, 'scores': scores, 'boxes': boxes})

# Create visualizations
viz = VisualizationCreator("my_viz")
for i, (image_path, result) in enumerate(zip(image_paths, results)):
    viz.create_page_visualization(image_path, result['texts'], 
                                 result['scores'], result['boxes'])

# Save results
processor = TextProcessor()
for i, result in enumerate(results, 1):
    processor.add_result(i, result['texts'], result['scores'], result['boxes'])
processor.save_to_txt("output.txt")
```

## 📋 Supported Formats

### Input Formats
- **Images**: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF
- **Documents**: PDF

### Output Formats
- **Text**: `.txt` (human-readable)
- **Data**: `.json` (structured data)
- **Spreadsheet**: `.csv` (for analysis)
- **Visualizations**: `.png` (annotated images)

## 🎯 Enhanced Features

### Core Features
- ✅ **Multi-format Support**: Images and PDFs
- ✅ **Multi-language OCR**: English, Arabic, Chinese, French, etc.
- ✅ **Enhanced Accuracy**: Advanced PaddleOCR with optimized settings
- ✅ **Enhanced Text Detection**: Improved accuracy for various text types
- ✅ **Multi-language Processing**: Process English + Arabic simultaneously
- ✅ **GPU Acceleration**: Faster processing with CUDA support
- ✅ **Angle Classification**: Better text detection at various angles
- ✅ **Space Character Recognition**: Improved text spacing
- ✅ **Batch Processing**: Handle multiple files efficiently
- ✅ **Visualization**: See detected text regions with bounding boxes
- ✅ **Multiple Outputs**: TXT, JSON, CSV formats

### Advanced Features
- ✅ **Modular Design**: Use individual components
- ✅ **Duplicate Detection**: Remove overlapping text regions
- ✅ **Confidence Analysis**: Quality metrics and scoring
- ✅ **Statistics**: Detailed processing statistics
- ✅ **Search**: Find specific text within results
- ✅ **Page-wise Results**: Organized by page
- ✅ **Temporary File Management**: Automatic cleanup
- ✅ **Error Handling**: Robust error recovery

### Enhanced OCR Settings
- ✅ **DB++ Detection Algorithm**: Improved text detection accuracy
- ✅ **SVTR Recognition Model**: Better text recognition
- ✅ **Lower Detection Thresholds**: Capture more text regions
- ✅ **Optimized Image Processing**: Better handling of various image qualities
- ✅ **Enhanced Bounding Box Fitting**: More accurate text boundaries

## 📊 Example Output

### Text File (`extracted_text.txt`)
```
OCR Text Extraction Results
==================================================
Total Pages: 18
Total Text Regions: 1500
Average Confidence: 0.867
Processing Time: 2025-01-14T10:30:00

PAGE 1
--------------------
  1. CREDIT PERIOD
     Confidence: 0.945
  2. TOTAL PURCHASING
     Confidence: 0.923
...

ALL TEXT COMBINED
====================
  1. CREDIT PERIOD
  2. TOTAL PURCHASING
  3. 10935.94
...
```

### JSON File (`extracted_text.json`)
```json
{
  "metadata": {
    "total_pages": 18,
    "total_text_regions": 1500,
    "average_confidence": 0.867
  },
  "results": [
    {
      "page": 1,
      "texts": ["CREDIT PERIOD", "TOTAL PURCHASING"],
      "scores": [0.945, 0.923],
      "boxes": [[100, 100, 200, 120], [100, 150, 200, 170]]
    }
  ]
}
```

## 🔧 Dependencies

### Core Dependencies
```
paddlepaddle-gpu==3.0.0
paddleocr
numpy==1.26.4
opencv-python
matplotlib
Pillow
```

### PDF Processing Dependencies
```
pdf2image
PyMuPDF
```

### Installation
```bash
# Install core dependencies
pip install paddlepaddle-gpu==3.0.0 paddleocr numpy==1.26.4 opencv-python matplotlib Pillow

# Install PDF dependencies
pip install pdf2image PyMuPDF

# For Windows users: Install Poppler
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
# Extract and add 'bin' folder to system PATH
```

## 🎨 Customization

### Language Support
```python
# Change language in main_ocr_app.py
language = 'ch'  # Chinese
language = 'fr'  # French
language = 'de'  # German
# See PaddleOCR documentation for full language list
```

### Visualization Customization
```python
# Customize visualization in visualizer.py
plt.figure(figsize=(20, 20))  # Larger images
plt.title('Custom Title', fontsize=20)  # Custom title
# Modify colors, fonts, etc.
```

### Output Customization
```python
# Customize text processing in text_processor.py
def custom_format_text(texts, scores):
    # Your custom formatting logic
    return formatted_text
```

## 🐛 Troubleshooting

### Common Issues

1. **PaddleOCR Import Error**
   ```bash
   pip install paddleocr --upgrade
   ```

2. **PDF Conversion Error**
   ```bash
   pip install pdf2image PyMuPDF
   # For Windows: Install Poppler
   ```

3. **CUDA/GPU Issues**
   ```bash
   pip uninstall paddlepaddle-gpu
   pip install paddlepaddle  # CPU version
   ```

4. **Memory Issues**
   - Reduce DPI in `pdf_converter.py`
   - Process fewer pages at once
   - Use smaller image sizes

## 📁 File Structure

```
paddlocr drug/
├── main_ocr_app.py          # Main application
├── pdf_converter.py        # PDF processing module
├── ocr_extractor.py        # Text extraction module
├── visualizer.py           # Visualization module
├── text_processor.py       # Text processing module
├── run_ocr.bat            # Windows batch file
├── requirements.txt        # Dependencies
├── README.md              # This file
├── petty_cash_visualizations/  # Generated visualizations
├── extracted_text.txt      # Generated text output
├── extracted_text.json     # Generated JSON output
├── extracted_text.csv      # Generated CSV output
└── temp_pdf_pages/        # Temporary PDF images
```

## 🚀 Usage Examples

### Example 1: Process Single Image
```python
from main_ocr_app import OCRApplication

app = OCRApplication()
results = app.process_image("document.jpg")
app.save_results(results, "output.txt")
```

### Example 2: Process PDF with Custom Settings
```python
from main_ocr_app import OCRApplication

app = OCRApplication(lang='ch')  # Chinese OCR
results = app.process_pdf("document.pdf", 
                         create_visualizations=True,
                         output_dir="my_viz")
app.save_results(results, "chinese_text.txt")
```

### Example 3: Use Individual Modules
```python
from pdf_converter import convert_pdf_to_images
from ocr_extractor import OCRProcessor

# Convert PDF
images = convert_pdf_to_images("doc.pdf", dpi=200)

# Extract text
ocr = OCRProcessor()
for img in images:
    texts, scores, boxes = ocr.extract_text_from_image(img)
    print(f"Found {len(texts)} text regions")
```

## 📈 Performance Tips

1. **For Large PDFs**: Use lower DPI (150-200) to reduce memory usage
2. **For High Accuracy**: Use higher DPI (300+) for better text recognition
3. **For Speed**: Process images in batches
4. **For Memory**: Clean up temporary files regularly

## 🤝 Contributing

This modular design makes it easy to:
- Add new file format support
- Implement custom visualization styles
- Add new output formats
- Integrate with other OCR engines
- Create specialized processing pipelines

## 📄 License

This project uses PaddleOCR, which is licensed under the Apache License 2.0.