#!/usr/bin/env python3
"""
Simple Interactive OCR Tool
===========================

A simple, user-friendly OCR tool that asks for user input
and processes images or PDFs.
"""

import os
import sys
from main_ocr_app import OCRApplication, get_user_input

def simple_ocr():
    """Simple OCR interface"""
    print("🔍 Simple OCR Text Extraction Tool")
    print("=" * 40)
    print("This tool will extract text from your images or PDFs")
    print("=" * 40)
    
    try:
        # Get user input
        file_path, language, use_multi_language, use_gpu, create_visualizations, visualization_dir, output_file = get_user_input()
        
        print(f"\n🚀 Processing your file...")
        print("Please wait, this may take a few minutes...")
        
        # Initialize and run OCR with enhanced features
        app = OCRApplication(
            lang=language,
            use_multi_language=use_multi_language,
            use_gpu=use_gpu
        )
        
        # Detect file type and process
        file_ext = os.path.splitext(file_path.lower())[1]
        
        if file_ext == '.pdf':
            results = app.process_pdf(file_path, create_visualizations, visualization_dir)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif']:
            results = app.process_image(file_path, create_visualizations, visualization_dir)
        else:
            print(f"❌ Unsupported file type: {file_ext}")
            return
        
        if results:
            # Results are already saved by the process methods
            
            # Show results
            print(f"\n✅ SUCCESS!")
            print("=" * 20)
            if 'session_folder' in results:
                print(f"📁 All files saved in: {results['session_folder']}")
            else:
                print(f"📄 Text extracted and saved to: {output_file}")
            
            if results['type'] == 'pdf':
                print(f"📊 Processed {results['total_pages']} pages")
                print(f"📝 Found {results['total_regions']} text regions")
                print(f"🎯 Average confidence: {results['avg_confidence']:.1%}")
                
                if create_visualizations and 'visualization_paths' in results:
                    print(f"🖼️  Visualizations saved in: {visualization_dir}/")
                    print(f"   Created {len(results['visualization_paths'])} visualization images")
            else:
                print(f"📝 Found {len(results['texts'])} text regions")
                print(f"🎯 Average confidence: {results['avg_confidence']:.1%}")
                
                if create_visualizations and 'visualization_path' in results:
                    print(f"🖼️  Visualization saved: {os.path.basename(results['visualization_path'])}")
            
            # Ask about cleanup for PDFs
            if results['type'] == 'pdf':
                cleanup = input(f"\n🧹 Delete temporary files? (y/n): ").lower().strip()
                if cleanup == 'y':
                    app.cleanup()
                    print("✓ Temporary files cleaned up")
            
            # Show sample text
            print(f"\n📝 Sample extracted text:")
            print("-" * 30)
            if results['type'] == 'pdf' and results['all_texts']:
                for i, text in enumerate(results['all_texts'][:5], 1):
                    print(f"{i}. {text}")
                if len(results['all_texts']) > 5:
                    print(f"... and {len(results['all_texts']) - 5} more")
            elif results['type'] == 'image' and results['texts']:
                for i, text in enumerate(results['texts'][:5], 1):
                    print(f"{i}. {text}")
                if len(results['texts']) > 5:
                    print(f"... and {len(results['texts']) - 5} more")
        
        else:
            print("❌ Failed to extract text from your file")
            print("Please check if the file contains readable text")
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Operation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your file and try again")

def main():
    """Main function"""
    while True:
        try:
            simple_ocr()
            
            # Ask if user wants to process another file
            print(f"\n" + "=" * 40)
            another = input("🔄 Process another file? (y/n): ").strip().lower()
            if another != 'y':
                print("👋 Thank you for using OCR Tool!")
                break
            print("\n" + "=" * 40)
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()
