#!/usr/bin/env python3
"""
Universal OCR Text Extraction Tool
==================================

Extract text from images and PDF files using PaddleOCR.
Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF
"""

import os
import warnings
warnings.filterwarnings('ignore')

def detect_file_type(file_path):
    """Detect if file is image or PDF"""
    file_ext = os.path.splitext(file_path.lower())[1]
    
    image_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif']
    pdf_formats = ['.pdf']
    
    if file_ext in image_formats:
        return 'image'
    elif file_ext in pdf_formats:
        return 'pdf'
    else:
        return 'unknown'

def convert_pdf_to_images(pdf_path, output_dir="temp_pdf_pages"):
    """Convert PDF pages to images"""
    try:
        from pdf2image import convert_from_path
        import fitz  # PyMuPDF as backup
        
        print(f"Converting PDF to images...")
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Try pdf2image first
        try:
            images = convert_from_path(pdf_path, dpi=300)
            image_paths = []
            
            for i, image in enumerate(images, 1):
                image_path = os.path.join(output_dir, f"page_{i:03d}.png")
                image.save(image_path, 'PNG')
                image_paths.append(image_path)
            
            return image_paths
            
        except Exception as e:
            print(f"pdf2image failed, trying PyMuPDF...")
            
            # Fallback to PyMuPDF
            doc = fitz.open(pdf_path)
            image_paths = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                image_path = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
                pix.save(image_path)
                image_paths.append(image_path)
            
            doc.close()
            return image_paths
            
    except ImportError as e:
        print(f"Error: Required libraries not installed: {e}")
        print("Please install: pip install pdf2image PyMuPDF")
        return None
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return None

def extract_text_from_image(image_path):
    """Extract text from an image using PaddleOCR"""
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (reuse model if possible)
        if not hasattr(extract_text_from_image, 'ocr_model'):
            print("Initializing PaddleOCR...")
            extract_text_from_image.ocr_model = PaddleOCR(lang='en')
        
        # Run OCR
        result = extract_text_from_image.ocr_model.ocr(image_path)
        
        # Process results
        if result and len(result) > 0:
            ocr_result = result[0]
            
            # Extract text from the json attribute
            json_data = ocr_result.json
            if 'res' in json_data and 'rec_texts' in json_data['res']:
                texts = json_data['res']['rec_texts']
                scores = json_data['res']['rec_scores']
                boxes = json_data['res']['rec_boxes']
                return texts, scores, boxes
            else:
                return [], [], []
        else:
            return [], [], []
            
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return [], [], []

def process_image_file(image_path):
    """Process a single image file"""
    print(f"Processing image: {os.path.basename(image_path)}")
    
    texts, scores, boxes = extract_text_from_image(image_path)
    
    if texts:
        print(f"✓ Found {len(texts)} text regions")
        return {
            'type': 'image',
            'texts': texts,
            'scores': scores,
            'boxes': boxes,
            'total_regions': len(texts)
        }
    else:
        print("No text detected in image")
        return None

def create_page_visualization(image_path, texts, scores, boxes, output_dir="petty_cash_visualizations"):
    """Create visualization for a single page"""
    try:
        import cv2
        import matplotlib.pyplot as plt
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load and process image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image for visualization: {image_path}")
            return None
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Create visualization
        plt.figure(figsize=(15, 15))
        plt.imshow(img)
        plt.title(f'Page {os.path.basename(image_path)} - OCR Results', fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # Add text annotations
        for i, (box, text, score) in enumerate(zip(boxes, texts, scores)):
            # Get center of bounding box
            if isinstance(box, list) and len(box) >= 4:
                x1, y1, x2, y2 = box
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
            else:
                center_x, center_y = 100, 100 + i * 30
            
            # Add annotation
            plt.annotate(f"{i+1}. {text}\n({score:.3f})", 
                        xy=(center_x, center_y), 
                        xytext=(10, 10), 
                        textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
                        fontsize=9,
                        ha='left',
                        fontweight='bold')
        
        plt.tight_layout()
        
        # Save annotated image
        page_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{page_name}_annotated.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()  # Close the figure to free memory
        
        return output_path
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None

def process_pdf_file(pdf_path):
    """Process a PDF file"""
    print(f"Processing PDF: {os.path.basename(pdf_path)}")
    
    # Convert PDF to images
    image_paths = convert_pdf_to_images(pdf_path)
    if not image_paths:
        print("❌ Failed to convert PDF to images")
        return None
    
    print(f"✓ Converted {len(image_paths)} pages to images")
    
    # Extract text from each page
    all_texts = []
    all_scores = []
    page_results = []
    visualization_paths = []
    
    for i, image_path in enumerate(image_paths, 1):
        print(f"📄 Processing Page {i}/{len(image_paths)}")
        
        texts, scores, boxes = extract_text_from_image(image_path)
        
        # Create visualization for this page
        if texts:
            print(f"   Creating visualization for page {i}...")
            viz_path = create_page_visualization(image_path, texts, scores, boxes)
            if viz_path:
                visualization_paths.append(viz_path)
                print(f"   ✓ Visualization saved: {os.path.basename(viz_path)}")
        
        page_results.append({
            'page': i,
            'texts': texts,
            'scores': scores,
            'count': len(texts),
            'image_path': image_path
        })
        
        all_texts.extend(texts)
        all_scores.extend(scores)
    
    return {
        'type': 'pdf',
        'all_texts': all_texts,
        'all_scores': all_scores,
        'page_results': page_results,
        'total_pages': len(image_paths),
        'total_regions': len(all_texts),
        'visualization_paths': visualization_paths
    }

def save_results(results, file_path, output_file="extracted_text.txt"):
    """Save extraction results to a file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Universal OCR Text Extraction Results\n")
            f.write("=" * 50 + "\n")
            f.write(f"File: {os.path.basename(file_path)}\n")
            f.write(f"Type: {results['type'].upper()}\n")
            
            if results['type'] == 'image':
                f.write(f"Text Regions: {results['total_regions']}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, (text, score) in enumerate(zip(results['texts'], results['scores']), 1):
                    f.write(f"{i:3d}. {text}\n")
                    f.write(f"     Confidence: {score:.3f}\n\n")
            
            elif results['type'] == 'pdf':
                f.write(f"Total Pages: {results['total_pages']}\n")
                f.write(f"Total Text Regions: {results['total_regions']}\n")
                f.write("=" * 50 + "\n\n")
                
                # Save page-wise results
                for page_result in results['page_results']:
                    f.write(f"PAGE {page_result['page']}\n")
                    f.write("-" * 20 + "\n")
                    
                    if page_result['texts']:
                        for i, (text, score) in enumerate(zip(page_result['texts'], page_result['scores']), 1):
                            f.write(f"{i:3d}. {text}\n")
                            f.write(f"     Confidence: {score:.3f}\n\n")
                    else:
                        f.write("No text detected on this page.\n\n")
                    
                    f.write("\n")
                
                # Save all text combined
                f.write("ALL TEXT COMBINED\n")
                f.write("=" * 20 + "\n")
                for i, text in enumerate(results['all_texts'], 1):
                    f.write(f"{i:3d}. {text}\n")
        
        print(f"✅ Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def cleanup_temp_files(output_dir="temp_pdf_pages"):
    """Clean up temporary image files"""
    try:
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
            print(f"🧹 Cleaned up temporary files")
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {e}")

def main():
    """Main function"""
    print("Universal OCR Text Extraction Tool")
    print("=" * 50)
    print("Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF")
    print("=" * 50)
    
    # File path - change this to your file
    file_path = r'C:\Users\ANIS MANSURI\Downloads\sample.pdf'  # Change this path
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        print("Please update the file_path variable with the correct path to your file.")
        return
    
    # Detect file type
    file_type = detect_file_type(file_path)
    print(f"📁 File type detected: {file_type.upper()}")
    
    if file_type == 'unknown':
        print("❌ Unsupported file format")
        return
    
    # Process file based on type
    if file_type == 'image':
        results = process_image_file(file_path)
    elif file_type == 'pdf':
        results = process_pdf_file(file_path)
    
    if results:
        # Save results
        save_results(results, file_path)
        
        # Print summary
        print(f"\n📊 Summary:")
        if results['type'] == 'image':
            print(f"   • Text regions found: {results['total_regions']}")
            if results['scores']:
                avg_confidence = sum(results['scores']) / len(results['scores'])
                print(f"   • Average confidence: {avg_confidence:.3f}")
        
        elif results['type'] == 'pdf':
            print(f"   • Total pages processed: {results['total_pages']}")
            print(f"   • Total text regions found: {results['total_regions']}")
            if results['all_scores']:
                avg_confidence = sum(results['all_scores']) / len(results['all_scores'])
                print(f"   • Average confidence: {avg_confidence:.3f}")
            
            # Print page-wise summary
            print(f"\n📄 Page-wise Results:")
            for page_result in results['page_results']:
                print(f"   • Page {page_result['page']}: {page_result['count']} text regions")
        
        # Show visualization info for PDFs
        if results['type'] == 'pdf' and 'visualization_paths' in results:
            print(f"\n🖼️  Visualizations created:")
            for viz_path in results['visualization_paths']:
                print(f"   • {os.path.basename(viz_path)}")
            print(f"   📁 All visualizations saved in: petty_cash_visualizations/")
        
        # Ask about cleanup for PDFs
        if results['type'] == 'pdf':
            cleanup = input(f"\n🧹 Do you want to delete temporary image files? (y/n): ").lower().strip()
            if cleanup == 'y':
                cleanup_temp_files()
        
        print(f"\n✅ Text extraction completed successfully!")
        print(f"📄 Results saved to: extracted_text.txt")
        
    else:
        print("❌ Failed to extract text from file")

if __name__ == "__main__":
    main()
