#!/usr/bin/env python3
"""
PDF OCR Text Extraction Tool
============================

Extract text from PDF files by converting each page to image and using PaddleOCR.
Supports: PDF files with any number of pages.
"""

import os
import warnings
warnings.filterwarnings('ignore')

def convert_pdf_to_images(pdf_path, output_dir="pdf_pages"):
    """Convert PDF pages to images"""
    try:
        from pdf2image import convert_from_path
        import fitz  # PyMuPDF as backup
        
        print(f"Converting PDF to images: {pdf_path}")
        
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
                print(f"✓ Page {i} saved as: page_{i:03d}.png")
            
            return image_paths
            
        except Exception as e:
            print(f"pdf2image failed: {e}")
            print("Trying PyMuPDF as backup...")
            
            # Fallback to PyMuPDF
            doc = fitz.open(pdf_path)
            image_paths = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Convert to image with high DPI
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                image_path = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
                pix.save(image_path)
                image_paths.append(image_path)
                print(f"✓ Page {page_num+1} saved as: page_{page_num+1:03d}.png")
            
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
                return texts, scores
            else:
                return [], []
        else:
            return [], []
            
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return [], []

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF by converting to images and using OCR"""
    try:
        print("PDF OCR Text Extraction Tool")
        print("=" * 50)
        print(f"Processing PDF: {os.path.basename(pdf_path)}")
        print("=" * 50)
        
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            print(f"❌ Error: PDF file not found: {pdf_path}")
            return None
        
        # Convert PDF to images
        image_paths = convert_pdf_to_images(pdf_path)
        if not image_paths:
            print("❌ Failed to convert PDF to images")
            return None
        
        print(f"\n✓ Converted {len(image_paths)} pages to images")
        print("\nExtracting text from each page...")
        
        # Extract text from each page
        all_texts = []
        all_scores = []
        page_results = []
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"\n📄 Processing Page {i}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            texts, scores = extract_text_from_image(image_path)
            
            if texts:
                print(f"✓ Found {len(texts)} text regions on page {i}")
                all_texts.extend(texts)
                all_scores.extend(scores)
                page_results.append({
                    'page': i,
                    'texts': texts,
                    'scores': scores,
                    'count': len(texts)
                })
            else:
                print(f"⚠ No text found on page {i}")
                page_results.append({
                    'page': i,
                    'texts': [],
                    'scores': [],
                    'count': 0
                })
        
        return {
            'all_texts': all_texts,
            'all_scores': all_scores,
            'page_results': page_results,
            'total_pages': len(image_paths),
            'total_text_regions': len(all_texts)
        }
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def save_pdf_results(results, pdf_path, output_file="pdf_extracted_text.txt"):
    """Save PDF extraction results to a file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PDF OCR Text Extraction Results\n")
            f.write("=" * 50 + "\n")
            f.write(f"PDF File: {os.path.basename(pdf_path)}\n")
            f.write(f"Total Pages: {results['total_pages']}\n")
            f.write(f"Total Text Regions: {results['total_text_regions']}\n")
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
        
        print(f"\n✅ Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def cleanup_temp_files(output_dir="pdf_pages"):
    """Clean up temporary image files"""
    try:
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
            print(f"🧹 Cleaned up temporary files in: {output_dir}")
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {e}")

def main():
    """Main function for PDF OCR"""
    print("PDF OCR Text Extraction Tool")
    print("=" * 50)
    print("Supports: PDF files with any number of pages")
    print("=" * 50)
    
    # PDF path - change this to your PDF file
    pdf_path = r'C:\Users\ANIS MANSURI\Downloads\sample.pdf'  # Change this path
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found: {pdf_path}")
        print("Please update the pdf_path variable with the correct path to your PDF file.")
        return
    
    # Extract text from PDF
    results = extract_text_from_pdf(pdf_path)
    
    if results:
        # Save results
        save_pdf_results(results, pdf_path)
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"   • Total pages processed: {results['total_pages']}")
        print(f"   • Total text regions found: {results['total_text_regions']}")
        
        if results['all_scores']:
            avg_confidence = sum(results['all_scores']) / len(results['all_scores'])
            print(f"   • Average confidence: {avg_confidence:.3f}")
        
        # Print page-wise summary
        print(f"\n📄 Page-wise Results:")
        for page_result in results['page_results']:
            print(f"   • Page {page_result['page']}: {page_result['count']} text regions")
        
        # Ask about cleanup
        cleanup = input(f"\n🧹 Do you want to delete temporary image files? (y/n): ").lower().strip()
        if cleanup == 'y':
            cleanup_temp_files()
        
        print(f"\n✅ PDF text extraction completed successfully!")
        print(f"📄 Results saved to: pdf_extracted_text.txt")
        
    else:
        print("❌ Failed to extract text from PDF")

if __name__ == "__main__":
    main()
