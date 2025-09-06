#!/usr/bin/env python3
"""
Easy PaddleOCR Runner
=====================

Simple script to run OCR on any image file.
Just change the image_path variable and run!
"""

import os
import sys

# Add the current directory to path to import paddle_ocr
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from paddle_ocr import extract_text_from_image, save_results, visualize_results

def main():
    """Main function with easy image path configuration"""
    
    # ===========================================
    # CHANGE THIS PATH TO YOUR IMAGE FILE
    # ===========================================
    image_path = r'C:\Users\ANIS MANSURI\Downloads\WhatsApp Image 2025-09-04 at 20.19.32_400fb57a.jpg'
    
    # Supported formats: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF
    # ===========================================
    
    print("PaddleOCR Text Extraction Tool")
    print("=" * 50)
    print(f"Processing: {os.path.basename(image_path)}")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        print("Please check the file path and try again.")
        return
    
    # Extract text
    texts, scores, boxes = extract_text_from_image(image_path)
    
    if texts:
        # Save results
        save_results(texts, scores)
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"   • Total text regions found: {len(texts)}")
        if scores:
            print(f"   • Average confidence: {sum(scores)/len(scores):.3f}")
        
        # Print all extracted text
        print(f"\n📝 All extracted text:")
        print("-" * 50)
        for i, text in enumerate(texts, 1):
            print(f"{i:3d}. {text}")
        
        # Ask for visualization
        print(f"\n🖼️  Visualization Options:")
        show_viz = input("Do you want to create annotated image? (y/n): ").lower().strip()
        if show_viz == 'y':
            visualize_results(image_path, texts, scores, boxes)
            print("✅ Annotated image created successfully!")
        
        print(f"\n✅ Text extraction completed successfully!")
        print(f"📄 Results saved to: extracted_text.txt")
        
    else:
        print("❌ No text was extracted from the image")

if __name__ == "__main__":
    main()
