#!/usr/bin/env python3
"""
Easy Universal OCR Runner
=========================

Simple script to run OCR on any image or PDF file.
Just change the file_path variable and run!
"""

import os
import sys

# Add the current directory to path to import universal_ocr
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_ocr import detect_file_type, process_image_file, process_pdf_file, save_results, cleanup_temp_files

def main():
    """Main function with easy file path configuration"""
    
    # ===========================================
    # CHANGE THIS PATH TO YOUR FILE
    # ===========================================
    file_path = r'D:\paddlocr drug\petty cash 13th August 2025 (1).pdf'  # Change this path
    
    # Supported formats: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF
    # ===========================================
    
    print("Universal OCR Text Extraction Tool")
    print("=" * 60)
    print("Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF")
    print("=" * 60)
    print(f"Processing: {os.path.basename(file_path)}")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        print("Please check the file path and try again.")
        return
    
    # Detect file type
    file_type = detect_file_type(file_path)
    print(f"📁 File type detected: {file_type.upper()}")
    
    if file_type == 'unknown':
        print("❌ Unsupported file format")
        print("Supported formats: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF")
        return
    
    # Process file based on type
    if file_type == 'image':
        print("\n🖼️  Processing Image...")
        results = process_image_file(file_path)
    elif file_type == 'pdf':
        print("\n📄 Processing PDF...")
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
        
        # Show first few lines of extracted text
        if results['type'] == 'image' and results['texts']:
            print(f"\n📝 First few extracted texts:")
            print("-" * 40)
            for i, text in enumerate(results['texts'][:5], 1):
                print(f"{i}. {text}")
            if len(results['texts']) > 5:
                print(f"... and {len(results['texts']) - 5} more")
        
        elif results['type'] == 'pdf' and results['all_texts']:
            print(f"\n📝 First few extracted texts:")
            print("-" * 40)
            for i, text in enumerate(results['all_texts'][:5], 1):
                print(f"{i}. {text}")
            if len(results['all_texts']) > 5:
                print(f"... and {len(results['all_texts']) - 5} more")
        
    else:
        print("❌ Failed to extract text from file")

if __name__ == "__main__":
    main()
