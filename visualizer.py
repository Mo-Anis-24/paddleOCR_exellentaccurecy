#!/usr/bin/env python3
"""
Visualization Module
====================

This module handles creating visualizations for OCR results.
Creates annotated images showing detected text regions with bounding boxes.
"""

import os
import warnings
warnings.filterwarnings('ignore')

class VisualizationCreator:
    """Visualization creator class for OCR results"""
    
    def __init__(self, output_dir="visualizations"):
        """
        Initialize visualization creator
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        self.output_dir = output_dir
        self._create_output_dir()
    
    def _create_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created visualization directory: {self.output_dir}")
    
    def create_page_visualization(self, image_path, texts, scores, boxes, page_title=None):
        """
        Create visualization for a single page
        
        Args:
            image_path (str): Path to the original image
            texts (list): List of extracted texts
            scores (list): List of confidence scores
            boxes (list): List of bounding boxes
            page_title (str): Custom title for the visualization
        
        Returns:
            str: Path to saved visualization or None if failed
        """
        try:
            import cv2
            import matplotlib.pyplot as plt
            
            # Load and process image
            img = cv2.imread(image_path)
            if img is None:
                print(f"❌ Error: Could not load image: {image_path}")
                return None
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Create visualization
            plt.figure(figsize=(15, 15))
            plt.imshow(img)
            
            # Set title
            if page_title:
                plt.title(page_title, fontsize=16, fontweight='bold')
            else:
                plt.title(f'OCR Results - {os.path.basename(image_path)}', fontsize=16, fontweight='bold')
            
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
            output_path = os.path.join(self.output_dir, f"{page_name}_annotated.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()  # Close the figure to free memory
            
            print(f"✓ Visualization saved: {os.path.basename(output_path)}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return None
    
    def create_summary_visualization(self, image_paths, all_texts, all_scores, output_name="summary"):
        """
        Create a summary visualization showing all pages
        
        Args:
            image_paths (list): List of image paths
            all_texts (list): List of all extracted texts
            all_scores (list): List of all confidence scores
            output_name (str): Name for the output file
        
        Returns:
            str: Path to saved summary visualization or None if failed
        """
        try:
            import matplotlib.pyplot as plt
            
            # Create summary figure
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis('off')
            
            # Add summary information
            summary_text = f"""
OCR EXTRACTION SUMMARY
======================

Total Pages Processed: {len(image_paths)}
Total Text Regions Found: {len(all_texts)}
Average Confidence: {sum(all_scores)/len(all_scores):.3f}

Top 10 Most Confident Text Regions:
"""
            
            # Sort by confidence and get top 10
            text_score_pairs = list(zip(all_texts, all_scores))
            text_score_pairs.sort(key=lambda x: x[1], reverse=True)
            
            for i, (text, score) in enumerate(text_score_pairs[:10], 1):
                summary_text += f"{i:2d}. {text} ({score:.3f})\n"
            
            ax.text(0.1, 0.9, summary_text, transform=ax.transAxes, 
                   fontsize=12, verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
            
            plt.title('OCR Extraction Summary', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            # Save summary
            output_path = os.path.join(self.output_dir, f"{output_name}_summary.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✓ Summary visualization saved: {os.path.basename(output_path)}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating summary visualization: {e}")
            return None
    
    def create_confidence_histogram(self, all_scores, output_name="confidence_histogram"):
        """
        Create a histogram of confidence scores
        
        Args:
            all_scores (list): List of all confidence scores
            output_name (str): Name for the output file
        
        Returns:
            str: Path to saved histogram or None if failed
        """
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            plt.hist(all_scores, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.xlabel('Confidence Score')
            plt.ylabel('Frequency')
            plt.title('Distribution of OCR Confidence Scores')
            plt.grid(True, alpha=0.3)
            
            # Add statistics
            mean_score = sum(all_scores) / len(all_scores)
            plt.axvline(mean_score, color='red', linestyle='--', 
                       label=f'Mean: {mean_score:.3f}')
            plt.legend()
            
            plt.tight_layout()
            
            # Save histogram
            output_path = os.path.join(self.output_dir, f"{output_name}.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✓ Confidence histogram saved: {os.path.basename(output_path)}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating confidence histogram: {e}")
            return None

def create_visualization(image_path, texts, scores, boxes, output_dir="visualizations"):
    """
    Simple function to create a single visualization
    
    Args:
        image_path (str): Path to the image
        texts (list): List of texts
        scores (list): List of scores
        boxes (list): List of boxes
        output_dir (str): Output directory
    
    Returns:
        str: Path to saved visualization or None if failed
    """
    creator = VisualizationCreator(output_dir)
    return creator.create_page_visualization(image_path, texts, scores, boxes)

if __name__ == "__main__":
    # Test the module
    print("Testing Visualization Module...")
    
    creator = VisualizationCreator("test_visualizations")
    
    # Test with sample data
    test_texts = ["Sample Text 1", "Sample Text 2", "Sample Text 3"]
    test_scores = [0.95, 0.87, 0.92]
    test_boxes = [[100, 100, 200, 120], [100, 150, 200, 170], [100, 200, 200, 220]]
    
    print("✓ Visualization module loaded successfully")
    print("Ready to create visualizations!")

