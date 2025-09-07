#!/usr/bin/env python3
"""
Main OCR Application
====================

This is the main application that combines all modules to provide
a complete OCR solution for both images and PDFs.
"""

import os
import sys
import shutil
from datetime import datetime

# Import our custom modules
from pdf_converter import convert_pdf_to_images, get_pdf_info, cleanup_temp_files
from ocr_extractor import OCRProcessor, batch_extract_text
from visualizer import VisualizationCreator
from text_processor import TextProcessor

class OCRApplication:
    """Main OCR application class"""
    
    def __init__(self, lang='en', use_multi_language=False, use_gpu=True):
        """
        Initialize the OCR application with enhanced features
        
        Args:
            lang (str): Primary language for OCR processing
            use_multi_language (bool): Whether to use multi-language detection
            use_gpu (bool): Whether to use GPU acceleration
        """
        self.lang = lang
        self.use_multi_language = use_multi_language
        self.use_gpu = use_gpu
        
        # Initialize OCR processor with enhanced settings
        self.ocr_processor = OCRProcessor(
            lang=lang,
            use_gpu=use_gpu,
            enable_mkldnn=True,
            use_angle_cls=True,
            use_space_char=True
        )
        
        self.text_processor = TextProcessor()
        self.visualizer = None
        self.output_base_dir = "ocr_outputs"
        self._ensure_output_directory()
        
        print("🚀 Enhanced OCR Application Initialized")
        print(f"Primary Language: {lang}")
        print(f"Multi-language: {'Yes' if use_multi_language else 'No'}")
        print(f"GPU Acceleration: {'Yes' if use_gpu else 'No'}")
        print(f"Enhanced Features: Angle Classification, Space Character, Multi-language Support")
        print("=" * 50)
    
    def _ensure_output_directory(self):
        """Ensure the output directory exists"""
        if not os.path.exists(self.output_base_dir):
            os.makedirs(self.output_base_dir)
            print(f"📁 Created output directory: {self.output_base_dir}")
    
    def _create_session_folder(self, file_path):
        """
        Create a unique session folder for this extraction
        
        Args:
            file_path (str): Path to the input file
        
        Returns:
            str: Path to the session folder
        """
        # Get file name without extension
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create session folder name
        session_name = f"{base_name}_{timestamp}"
        session_path = os.path.join(self.output_base_dir, session_name)
        
        # Create the folder
        os.makedirs(session_path, exist_ok=True)
        
        print(f"📁 Created session folder: {session_path}")
        return session_path
    
    def _ask_cleanup_old_outputs(self):
        """
        Ask user if they want to clean up old output folders
        
        Returns:
            bool: True if user wants to cleanup, False otherwise
        """
        try:
            # Count existing output folders
            if os.path.exists(self.output_base_dir):
                folders = [f for f in os.listdir(self.output_base_dir) 
                          if os.path.isdir(os.path.join(self.output_base_dir, f))]
                
                if len(folders) > 5:  # Only ask if there are more than 5 folders
                    print(f"\n🧹 Found {len(folders)} previous output folders in {self.output_base_dir}")
                    response = input("Do you want to clean up old output folders? (y/n): ").lower().strip()
                    
                    if response in ['y', 'yes']:
                        return True
                    else:
                        print("Keeping all previous outputs.")
                        return False
            
            return False
            
        except Exception as e:
            print(f"⚠️  Error checking old outputs: {e}")
            return False
    
    def _cleanup_old_outputs(self):
        """Clean up old output folders, keeping only the 3 most recent"""
        try:
            if not os.path.exists(self.output_base_dir):
                return
            
            # Get all folders with their modification times
            folders = []
            for item in os.listdir(self.output_base_dir):
                item_path = os.path.join(self.output_base_dir, item)
                if os.path.isdir(item_path):
                    mtime = os.path.getmtime(item_path)
                    folders.append((item_path, mtime))
            
            # Sort by modification time (newest first)
            folders.sort(key=lambda x: x[1], reverse=True)
            
            # Keep only the 3 most recent folders
            if len(folders) > 3:
                folders_to_delete = folders[3:]
                deleted_count = 0
                
                for folder_path, _ in folders_to_delete:
                    try:
                        shutil.rmtree(folder_path)
                        deleted_count += 1
                        print(f"🗑️  Deleted old output: {os.path.basename(folder_path)}")
                    except Exception as e:
                        print(f"⚠️  Could not delete {folder_path}: {e}")
                
                if deleted_count > 0:
                    print(f"✅ Cleaned up {deleted_count} old output folders")
            
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")
    
    def process_image(self, image_path, create_visualization=True, output_dir="visualizations"):
        """
        Process a single image file
        
        Args:
            image_path (str): Path to the image file
            create_visualization (bool): Whether to create visualization
            output_dir (str): Directory for visualizations
        
        Returns:
            dict: Processing results
        """
        # Create session folder for organized output
        session_folder = self._create_session_folder(image_path)
        
        # Set up output directories
        if output_dir == "visualizations":
            output_dir = os.path.join(session_folder, "visualizations")
        
        print(f"\n📷 Processing Image: {os.path.basename(image_path)}")
        print(f"📁 Output folder: {session_folder}")
        print("-" * 40)
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return None
        
        # Check if format is supported
        if not self.ocr_processor.is_supported_format(image_path):
            print(f"❌ Unsupported file format: {image_path}")
            return None
        
        # Extract text with enhanced features
        if self.use_multi_language:
            print("🌍 Using multi-language detection (English + Arabic)")
            ocr_result = self.ocr_processor.extract_text_multi_language(image_path, ['en', 'ar'])
        else:
            print(f"🔤 Using single language: {self.lang}")
            ocr_result = self.ocr_processor.extract_text_from_image(image_path)
        
        if not ocr_result or not ocr_result['success']:
            print("❌ Failed to extract text")
            return None
        
        texts = ocr_result['texts']
        scores = ocr_result['scores']
        boxes = ocr_result['boxes']
        
        # Create results
        results = {
            'type': 'image',
            'file_path': image_path,
            'session_folder': session_folder,
            'texts': texts,
            'scores': scores,
            'boxes': boxes,
            'text_count': len(texts),
            'avg_confidence': sum(scores) / len(scores) if scores else 0,
            'multi_language': self.use_multi_language,
            'language_results': ocr_result.get('language_results', {})
        }
        
        # Add to text processor
        self.text_processor.add_result(1, texts, scores, boxes, image_path)
        
        # Create visualization if requested
        if create_visualization and texts:
            self.visualizer = VisualizationCreator(output_dir)
            viz_path = self.visualizer.create_page_visualization(
                image_path, texts, scores, boxes,
                f"OCR Results - {os.path.basename(image_path)}"
            )
            results['visualization_path'] = viz_path
        
        # Save results to session folder
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_file = os.path.join(session_folder, f"{base_name}_extracted_text.txt")
        self.save_results(output_file)
        
        print(f"✅ Successfully processed image")
        print(f"   Text regions found: {len(texts)}")
        print(f"   Average confidence: {results['avg_confidence']:.3f}")
        
        return results
    
    def process_pdf(self, pdf_path, create_visualizations=True, output_dir="pdf_visualizations"):
        """
        Process a PDF file
        
        Args:
            pdf_path (str): Path to the PDF file
            create_visualizations (bool): Whether to create visualizations
            output_dir (str): Directory for visualizations
        
        Returns:
            dict: Processing results
        """
        print(f"\n📄 Processing PDF: {os.path.basename(pdf_path)}")
        print("-" * 40)
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return None
        
        # Get PDF info
        pdf_info = get_pdf_info(pdf_path)
        if pdf_info:
            print(f"📊 PDF Information:")
            print(f"   Pages: {pdf_info['pages']}")
            print(f"   Title: {pdf_info['title']}")
            print(f"   Author: {pdf_info['author']}")
        
        # Convert PDF to images
        print(f"\n🔄 Converting PDF to images...")
        image_paths = convert_pdf_to_images(pdf_path)
        
        if not image_paths:
            print("❌ Failed to convert PDF to images")
            return None
        
        print(f"✅ Converted {len(image_paths)} pages to images")
        
        # Initialize visualizer if needed
        if create_visualizations:
            self.visualizer = VisualizationCreator(output_dir)
        
        # Process each page
        page_results = []
        all_texts = []
        all_scores = []
        visualization_paths = []
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"\n📄 Processing Page {i}/{len(image_paths)}")
            
            # Extract text from page
            ocr_result = self.ocr_processor.extract_text_from_image(image_path)
            
            if ocr_result and ocr_result['success']:
                texts = ocr_result['texts']
                scores = ocr_result['scores']
                boxes = ocr_result['boxes']
                page_result = {
                    'page': i,
                    'texts': texts,
                    'scores': scores,
                    'boxes': boxes,
                    'image_path': image_path,
                    'count': len(texts)
                }
                page_results.append(page_result)
                
                # Add to text processor
                self.text_processor.add_result(i, texts, scores, boxes, image_path)
                
                # Collect all texts and scores
                all_texts.extend(texts)
                all_scores.extend(scores)
                
                # Create visualization if requested
                if create_visualizations:
                    viz_path = self.visualizer.create_page_visualization(
                        image_path, texts, scores, boxes,
                        f"Page {i} - OCR Results"
                    )
                    if viz_path:
                        visualization_paths.append(viz_path)
                
                print(f"   ✓ Found {len(texts)} text regions")
            else:
                print(f"   ❌ Failed to extract text from page {i}")
        
        # Create results
        results = {
            'type': 'pdf',
            'file_path': pdf_path,
            'total_pages': len(image_paths),
            'page_results': page_results,
            'all_texts': all_texts,
            'all_scores': all_scores,
            'total_regions': len(all_texts),
            'avg_confidence': sum(all_scores) / len(all_scores) if all_scores else 0,
            'visualization_paths': visualization_paths
        }
        
        print(f"\n✅ Successfully processed PDF")
        print(f"   Total pages: {len(image_paths)}")
        print(f"   Total text regions: {len(all_texts)}")
        print(f"   Average confidence: {results['avg_confidence']:.3f}")
        
        return results
    
    def save_results(self, results, output_file="extracted_text.txt"):
        """
        Save processing results
        
        Args:
            results (dict): Processing results
            output_file (str): Output file path
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not results:
            print("❌ No results to save")
            return False
        
        print(f"\n💾 Saving results...")
        
        # Save text results
        success = self.text_processor.save_to_txt(output_file)
        
        # Also save JSON for detailed analysis
        base_name = os.path.splitext(output_file)[0]
        self.text_processor.save_to_json(f"{base_name}.json")
        
        return success
    
    def cleanup(self):
        """Clean up temporary files"""
        print(f"\n🧹 Cleaning up temporary files...")
        cleanup_temp_files()
    
    def get_statistics(self):
        """Get processing statistics"""
        return self.text_processor.get_statistics()

def get_user_input():
    """Get user input for file path and settings"""
    print("🔍 Universal OCR Text Extraction Tool")
    print("=" * 50)
    print("Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF, PDF")
    print("=" * 50)
    
    # Get file path from user
    while True:
        file_path = input("\n📁 Enter the path to your file (image or PDF): ").strip()
        
        # Remove quotes if user added them
        file_path = file_path.strip('"').strip("'")
        
        if not file_path:
            print("❌ Please enter a file path")
            continue
            
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            print("Please check the path and try again")
            continue
            
        # Check file extension
        file_ext = os.path.splitext(file_path.lower())[1]
        if file_ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif']:
            print(f"❌ Unsupported file type: {file_ext}")
            print("Supported formats: PDF, JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF")
            continue
            
        break
    
    # Get language preference
    print(f"\n🌍 OCR Language Options:")
    print("   en - English (default)")
    print("   ar - Arabic")
    print("   ch - Chinese")
    print("   fr - French")
    print("   de - German")
    print("   es - Spanish")
    print("   ja - Japanese")
    print("   ko - Korean")
    print("   ru - Russian")
    print("   multi - Multi-language (English + Arabic)")
    
    language = input("\n🔤 Enter language code (or press Enter for English): ").strip().lower()
    if not language:
        language = 'en'
    
    # Check for multi-language option
    use_multi_language = False
    if language == 'multi':
        use_multi_language = True
        language = 'en'  # Primary language
    
    # Get GPU preference
    use_gpu = input("\n⚡ Use GPU acceleration? (y/n, default: y): ").strip().lower()
    use_gpu = use_gpu != 'n'
    
    # Get visualization preference
    create_visualizations = input("\n🖼️  Create visualizations? (y/n, default: y): ").strip().lower()
    create_visualizations = create_visualizations != 'n'
    
    # Get output file name
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    default_output = f"{base_name}_extracted_text.txt"
    output_file = input(f"\n💾 Output file name (or press Enter for '{default_output}'): ").strip()
    if not output_file:
        output_file = default_output
    
    # Get visualization directory name
    if create_visualizations:
        default_viz_dir = f"{base_name}_visualizations"
        visualization_dir = input(f"\n📁 Visualization folder name (or press Enter for '{default_viz_dir}'): ").strip()
        if not visualization_dir:
            visualization_dir = default_viz_dir
    else:
        visualization_dir = None
    
    return file_path, language, use_multi_language, use_gpu, create_visualizations, visualization_dir, output_file

def main():
    """Main function"""
    try:
        # Get user input
        file_path, language, use_multi_language, use_gpu, create_visualizations, visualization_dir, output_file = get_user_input()
        
        print(f"\n📋 Processing Configuration:")
        print(f"   File: {os.path.basename(file_path)}")
        print(f"   Language: {language}")
        print(f"   Multi-language: {'Yes (English + Arabic)' if use_multi_language else 'No'}")
        print(f"   GPU Acceleration: {'Yes' if use_gpu else 'No'}")
        print(f"   Visualizations: {'Yes' if create_visualizations else 'No'}")
        if create_visualizations:
            print(f"   Visualization folder: {visualization_dir}")
        print(f"   Output file: {output_file}")
        
        confirm = input(f"\n✅ Proceed with these settings? (y/n, default: y): ").strip().lower()
        if confirm == 'n':
            print("❌ Operation cancelled by user")
            return
        
        print(f"\n🚀 Starting Enhanced OCR processing...")
        print("=" * 50)
        
        # Initialize application with enhanced features
        app = OCRApplication(
            lang=language,
            use_multi_language=use_multi_language,
            use_gpu=use_gpu
        )
        
        # Ask about cleanup before processing
        if app._ask_cleanup_old_outputs():
            app._cleanup_old_outputs()
        
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
            # Save results
            app.save_results(results, output_file)
            
            # Print summary
            stats = app.get_statistics()
            print(f"\n📊 FINAL SUMMARY")
            print("=" * 30)
            print(f"Total Pages: {stats['total_pages']}")
            print(f"Total Text Regions: {stats['total_text_regions']}")
            print(f"Average Confidence: {stats['average_confidence']:.3f}")
            print(f"Min Confidence: {stats['min_confidence']:.3f}")
            print(f"Max Confidence: {stats['max_confidence']:.3f}")
            
            # Show visualization info
            if results['type'] == 'pdf' and 'visualization_paths' in results:
                print(f"\n🖼️  Visualizations created:")
                for viz_path in results['visualization_paths']:
                    print(f"   • {os.path.basename(viz_path)}")
                print(f"   📁 All visualizations saved in: {visualization_dir}/")
            
            # Ask about cleanup
            if results['type'] == 'pdf':
                cleanup = input(f"\n🧹 Do you want to delete temporary image files? (y/n): ").lower().strip()
                if cleanup == 'y':
                    app.cleanup()
            
            print(f"\n✅ Processing completed successfully!")
            print(f"📄 Results saved to: {output_file}")
            
            # Show sample extracted texts
            if results['type'] == 'pdf' and results['all_texts']:
                print(f"\n📝 Sample extracted texts:")
                print("-" * 40)
                for text in results['all_texts'][:10]:
                    print(f"• {text}")
                if len(results['all_texts']) > 10:
                    print(f"... and {len(results['all_texts']) - 10} more")
            elif results['type'] == 'image' and results['texts']:
                print(f"\n📝 Extracted texts:")
                print("-" * 40)
                for text in results['texts'][:10]:
                    print(f"• {text}")
                if len(results['texts']) > 10:
                    print(f"... and {len(results['texts']) - 10} more")
        
        else:
            print("❌ Failed to process file")
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Operation cancelled by user")
        print("Cleaning up temporary files...")
        try:
            cleanup_temp_files()
        except:
            pass
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Cleaning up temporary files...")
        try:
            cleanup_temp_files()
        except:
            pass

if __name__ == "__main__":
    main()
