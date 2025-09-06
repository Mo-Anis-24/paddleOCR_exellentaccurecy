#!/usr/bin/env python3
"""
PaddleOCR Text Extraction Tool
==============================

Simple script to extract text from images using PaddleOCR.
Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP and other common formats.
Just run: python paddle_ocr.py
"""

import os
import warnings
warnings.filterwarnings('ignore')

def check_image_format(image_path):
    """Check if the image format is supported"""
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif']
    file_ext = os.path.splitext(image_path.lower())[1]
    return file_ext in supported_formats

def extract_text_from_image(image_path):
    """Extract text from an image using PaddleOCR"""
    try:
        from paddleocr import PaddleOCR
        
        print("Initializing PaddleOCR...")
        ocr_model = PaddleOCR(lang='en')
        
        print(f"Processing image: {image_path}")
        
        # Check if image exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Check if image format is supported
        if not check_image_format(image_path):
            print("Warning: Image format might not be supported. Trying anyway...")
        
        # Run OCR
        result = ocr_model.ocr(image_path)
        
        # Process results
        if result and len(result) > 0:
            ocr_result = result[0]
            print(f"\n✓ Found OCR result")
            
            # Extract text from the json attribute
            json_data = ocr_result.json
            if 'res' in json_data and 'rec_texts' in json_data['res']:
                texts = json_data['res']['rec_texts']
                scores = json_data['res']['rec_scores']
                boxes = json_data['res']['rec_boxes']
                
                print(f"✓ Found {len(texts)} text regions")
                
                # Print extracted text
                for i, (text, score) in enumerate(zip(texts, scores), 1):
                    print(f"{i:3d}. {text} (Confidence: {score:.3f})")
                
                return texts, scores, boxes
            else:
                print("No text found in OCR result")
                return None, None, None
        else:
            print("No text detected in the image")
            return None, None, None
            
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return None, None, None

def visualize_results(image_path, texts, scores, boxes):
    """Visualize OCR results on the original image"""
    try:
        import cv2
        import matplotlib.pyplot as plt
        
        # Load and process image
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not load image for visualization")
            return
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Create visualization
        plt.figure(figsize=(15, 15))
        plt.imshow(img)
        plt.title('PaddleOCR Text Detection Results', fontsize=16, fontweight='bold')
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
        output_path = f"annotated_{os.path.basename(image_path)}"
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Annotated image saved as: {output_path}")
        
        # Try to show, but don't fail if it doesn't work
        try:
            plt.show()
        except:
            print("Note: Could not display image, but saved successfully")
        
        plt.close()  # Close the figure to free memory
        
    except Exception as e:
        print(f"Error during visualization: {e}")

def save_results(texts, scores, output_file="extracted_text.txt"):
    """Save extracted text to a file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PaddleOCR Text Extraction Results\n")
            f.write("=" * 40 + "\n\n")
            
            if texts:
                for i, (text, score) in enumerate(zip(texts, scores), 1):
                    f.write(f"{i:3d}. {text}\n")
                    f.write(f"     Confidence: {score:.3f}\n\n")
            else:
                f.write("No text detected in the image.\n")
        
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    """Main function"""
    print("PaddleOCR Text Extraction Tool")
    print("=" * 40)
    print("Supports: JPG, JPEG, PNG, BMP, TIFF, WEBP, GIF")
    print("=" * 40)
    
    # Image path - change this to your image path
    image_path = r'C:\Users\ANIS MANSURI\Downloads\WhatsApp Image 2025-09-04 at 20.19.32_400fb57a.jpg'
    
    # Extract text
    texts, scores, boxes = extract_text_from_image(image_path)
    
    if texts:
        # Save results
        save_results(texts, scores)
        
        # Print summary
        print(f"\nSummary:")
        print(f"- Total text regions found: {len(texts)}")
        if scores:
            print(f"- Average confidence: {sum(scores)/len(scores):.3f}")
        
        # Print all extracted text
        print(f"\nAll extracted text:")
        print("-" * 30)
        for text in texts:
            print(text)
        
        # Ask for visualization
        show_viz = input("\nDo you want to see the visualization? (y/n): ").lower().strip()
        if show_viz == 'y':
            visualize_results(image_path, texts, scores, boxes)
    else:
        print("No text was extracted from the image")

if __name__ == "__main__":
    main()
