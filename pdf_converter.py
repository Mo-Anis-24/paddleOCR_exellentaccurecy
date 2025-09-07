#!/usr/bin/env python3
"""
PDF to Image Converter Module
=============================

This module handles converting PDF files to images.
Supports multiple PDF processing libraries for better compatibility.
"""

import os
import warnings
warnings.filterwarnings('ignore')

def convert_pdf_to_images(pdf_path, output_dir="temp_pdf_pages", dpi=300):
    """
    Convert PDF pages to images
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save converted images
        dpi (int): Resolution for image conversion
    
    Returns:
        list: List of image file paths, or None if failed
    """
    try:
        print(f"Converting PDF to images: {os.path.basename(pdf_path)}")
        print(f"Output directory: {output_dir}")
        print(f"DPI: {dpi}")
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ Created directory: {output_dir}")
        
        # Try pdf2image first
        try:
            from pdf2image import convert_from_path
            print("Using pdf2image library...")
            
            images = convert_from_path(pdf_path, dpi=dpi)
            image_paths = []
            
            for i, image in enumerate(images, 1):
                image_path = os.path.join(output_dir, f"page_{i:03d}.png")
                image.save(image_path, 'PNG')
                image_paths.append(image_path)
                print(f"✓ Page {i} saved as: page_{i:03d}.png")
            
            print(f"✓ Successfully converted {len(image_paths)} pages using pdf2image")
            return image_paths
            
        except ImportError:
            print("pdf2image not available, trying PyMuPDF...")
        except Exception as e:
            print(f"pdf2image failed: {e}")
            print("Trying PyMuPDF as backup...")
        
        # Fallback to PyMuPDF
        try:
            import fitz  # PyMuPDF
            print("Using PyMuPDF library...")
            
            doc = fitz.open(pdf_path)
            image_paths = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Convert to image with specified DPI
                zoom = dpi / 72.0  # Convert DPI to zoom factor
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                image_path = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
                pix.save(image_path)
                image_paths.append(image_path)
                print(f"✓ Page {page_num+1} saved as: page_{page_num+1:03d}.png")
            
            doc.close()
            print(f"✓ Successfully converted {len(image_paths)} pages using PyMuPDF")
            return image_paths
            
        except ImportError:
            print("❌ Error: Neither pdf2image nor PyMuPDF is installed")
            print("Please install: pip install pdf2image PyMuPDF")
            return None
        except Exception as e:
            print(f"❌ PyMuPDF failed: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return None

def get_pdf_info(pdf_path):
    """
    Get basic information about PDF file
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        dict: PDF information or None if failed
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        info = {
            'pages': len(doc),
            'title': doc.metadata.get('title', 'Unknown'),
            'author': doc.metadata.get('author', 'Unknown'),
            'subject': doc.metadata.get('subject', 'Unknown'),
            'creator': doc.metadata.get('creator', 'Unknown'),
            'producer': doc.metadata.get('producer', 'Unknown'),
            'creation_date': doc.metadata.get('creationDate', 'Unknown'),
            'modification_date': doc.metadata.get('modDate', 'Unknown')
        }
        doc.close()
        
        return info
        
    except Exception as e:
        print(f"Error getting PDF info: {e}")
        return None

def cleanup_temp_files(output_dir="temp_pdf_pages"):
    """
    Clean up temporary image files
    
    Args:
        output_dir (str): Directory containing temporary files
    """
    try:
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
            print(f"🧹 Cleaned up temporary files in: {output_dir}")
            return True
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {e}")
        return False

if __name__ == "__main__":
    # Test the module
    pdf_path = r'D:\paddlocr drug\petty cash 13th August 2025 (1).pdf'
    
    if os.path.exists(pdf_path):
        print("Testing PDF to Image Converter...")
        
        # Get PDF info
        info = get_pdf_info(pdf_path)
        if info:
            print(f"\nPDF Information:")
            print(f"Pages: {info['pages']}")
            print(f"Title: {info['title']}")
            print(f"Author: {info['author']}")
        
        # Convert to images
        image_paths = convert_pdf_to_images(pdf_path)
        if image_paths:
            print(f"\n✓ Conversion successful!")
            print(f"Created {len(image_paths)} image files")
        else:
            print(f"\n❌ Conversion failed!")
    else:
        print(f"PDF file not found: {pdf_path}")

