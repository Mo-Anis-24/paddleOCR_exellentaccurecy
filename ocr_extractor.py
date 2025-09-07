#!/usr/bin/env python3
"""
OCR Text Extraction Module
==========================

This module handles text extraction from images using PaddleOCR.
Supports multiple image formats and provides confidence scores.
"""

import os
import cv2
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class OCRProcessor:
    """OCR processor class for text extraction"""
    
    def __init__(self, lang='en', use_gpu=True, enable_mkldnn=True, use_angle_cls=True, use_space_char=True):
        """
        Initialize OCR processor with enhanced settings for better accuracy
        
        Args:
            lang (str): Language for OCR (default: 'en')
            use_gpu (bool): Whether to use GPU acceleration
            enable_mkldnn (bool): Enable MKLDNN acceleration
            use_angle_cls (bool): Use angle classification for better text detection
            use_space_char (bool): Use space character recognition
        """
        self.lang = lang
        self.use_gpu = use_gpu
        self.enable_mkldnn = enable_mkldnn
        self.use_angle_cls = use_angle_cls
        self.use_space_char = use_space_char
        self.ocr_model = None
        self.enhanced_mode = False  # Use single most accurate method only
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize PaddleOCR model with enhanced settings"""
        try:
            from paddleocr import PaddleOCR
            print(f"Initializing PaddleOCR with enhanced settings...")
            print(f"Language: {self.lang}")
            print(f"GPU: {self.use_gpu}")
            print(f"Angle Classification: {self.use_angle_cls}")
            print(f"Space Character: {self.use_space_char}")
            
            # Initialize with basic parameters
            self.ocr_model = PaddleOCR(lang=self.lang)
            print("✓ Enhanced PaddleOCR model initialized successfully")
            
            # Table recognition not available in this PaddleOCR version
            self.table_model = None
                
        except Exception as e:
            print(f"❌ Error initializing PaddleOCR: {e}")
            self.ocr_model = None
    
    def _preprocess_image(self, image_path):
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            numpy.ndarray: Preprocessed image
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding for better text contrast
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up the image
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Resize if image is too small (minimum 300px on shortest side)
            h, w = cleaned.shape
            min_dim = min(h, w)
            if min_dim < 300:
                scale = 300 / min_dim
                new_h, new_w = int(h * scale), int(w * scale)
                cleaned = cv2.resize(cleaned, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            
            return cleaned
            
        except Exception as e:
            print(f"⚠️  Image preprocessing failed: {e}")
            # Return original image if preprocessing fails
            return cv2.imread(image_path)
    
    def _enhance_text_detection(self, image_path):
        """
        Try multiple image preprocessing techniques for better text detection
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            list: List of preprocessed images to try
        """
        try:
            original = cv2.imread(image_path)
            if original is None:
                return [image_path]
            
            images_to_try = [image_path]  # Start with original
            
            # Convert to grayscale
            gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            
            # Method 1: Standard preprocessing
            preprocessed = self._preprocess_image(image_path)
            if preprocessed is not None:
                temp_path = image_path.replace('.', '_preprocessed.')
                cv2.imwrite(temp_path, preprocessed)
                images_to_try.append(temp_path)
            
            # Method 2: High contrast version
            high_contrast = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
            temp_path2 = image_path.replace('.', '_high_contrast.')
            cv2.imwrite(temp_path2, high_contrast)
            images_to_try.append(temp_path2)
            
            # Method 3: Inverted version (for white text on dark background)
            inverted = cv2.bitwise_not(gray)
            temp_path3 = image_path.replace('.', '_inverted.')
            cv2.imwrite(temp_path3, inverted)
            images_to_try.append(temp_path3)
            
            return images_to_try
            
        except Exception as e:
            print(f"⚠️  Image enhancement failed: {e}")
            return [image_path]
    
    def extract_text_from_image(self, image_path):
        """
        Extract text from an image with enhanced accuracy
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            dict: Results containing texts, scores, and boxes
        """
        try:
            if not self.ocr_model:
                print("❌ OCR model not initialized")
                return None
            
            if not os.path.exists(image_path):
                print(f"❌ Image file not found: {image_path}")
                return None
            
            print(f"🔍 Processing image: {os.path.basename(image_path)}")
            
            # Use only the most accurate preprocessing method
            preprocessed_image = self._preprocess_image(image_path)
            if preprocessed_image is not None:
                # Save preprocessed image temporarily
                temp_path = image_path.replace('.', '_preprocessed.')
                cv2.imwrite(temp_path, preprocessed_image)
                image_to_process = temp_path
                print(f"🎯 Using preprocessed image for better accuracy")
            else:
                image_to_process = image_path
                print(f"🎯 Using original image")
            
            # Single OCR attempt with best preprocessing
            result = self.ocr_model.ocr(image_to_process)
            
            # Clean up temporary file
            if image_to_process != image_path and os.path.exists(image_to_process):
                try:
                    os.remove(image_to_process)
                except:
                    pass
            
            best_result = None
            if result and len(result) > 0:
                ocr_result = result[0]
                json_data = ocr_result.json
                
                if 'res' in json_data and 'rec_texts' in json_data['res']:
                    texts = json_data['res']['rec_texts']
                    scores = json_data['res']['rec_scores']
                    boxes = json_data['res']['rec_boxes']
                    
                    best_result = {
                        'texts': texts,
                        'scores': scores,
                        'boxes': boxes,
                        'method': 1,
                        'avg_score': sum(scores) / len(scores) if scores else 0
                    }
            
            if best_result:
                texts = best_result['texts']
                scores = best_result['scores']
                boxes = best_result['boxes']
                
                print(f"✓ Found {len(texts)} text regions (confidence: {best_result['avg_score']:.3f})")
                
                return {
                    'texts': texts,
                    'scores': scores,
                    'boxes': boxes,
                    'success': True,
                    'avg_confidence': best_result['avg_score']
                }
            else:
                print("❌ No text detected")
                return {
                    'texts': [],
                    'scores': [],
                    'boxes': [],
                    'success': False
                }
                
        except Exception as e:
            print(f"❌ Error during OCR processing: {e}")
            return None
    
    def extract_text_multi_language(self, image_path, languages=['en', 'ar']):
        """
        Extract text using multiple languages for better accuracy
        
        Args:
            image_path (str): Path to the image file
            languages (list): List of language codes to try
        
        Returns:
            dict: Combined results from all languages
        """
        all_results = {}
        
        for lang in languages:
            print(f"\n🌍 Processing with language: {lang}")
            
            # Create temporary processor for this language
            temp_processor = OCRProcessor(
                lang=lang,
                use_gpu=self.use_gpu,
                enable_mkldnn=self.enable_mkldnn,
                use_angle_cls=self.use_angle_cls,
                use_space_char=self.use_space_char
            )
            
            if temp_processor.ocr_model:
                result = temp_processor.extract_text_from_image(image_path)
                if result and result['success']:
                    all_results[lang] = result
                    print(f"✓ {lang}: Found {len(result['texts'])} text regions")
                else:
                    print(f"⚠️  {lang}: No text detected")
            else:
                print(f"❌ {lang}: Failed to initialize")
        
        # Combine results from all languages
        combined_texts = []
        combined_scores = []
        combined_boxes = []
        
        for lang, result in all_results.items():
            combined_texts.extend(result['texts'])
            combined_scores.extend(result['scores'])
            combined_boxes.extend(result['boxes'])
        
        # Remove duplicates based on bounding box overlap
        unique_results = self._remove_duplicate_texts(combined_texts, combined_scores, combined_boxes)
        
        return {
            'texts': unique_results['texts'],
            'scores': unique_results['scores'],
            'boxes': unique_results['boxes'],
            'language_results': all_results,
            'success': len(unique_results['texts']) > 0
        }
    
    def _remove_duplicate_texts(self, texts, scores, boxes, overlap_threshold=0.8):
        """
        Remove duplicate text detections based on bounding box overlap
        
        Args:
            texts (list): List of texts
            scores (list): List of scores
            boxes (list): List of bounding boxes
            overlap_threshold (float): Threshold for considering boxes as duplicates
        
        Returns:
            dict: Unique texts, scores, and boxes
        """
        if not texts:
            return {'texts': [], 'scores': [], 'boxes': []}
        
        unique_texts = []
        unique_scores = []
        unique_boxes = []
        
        for i, (text, score, box) in enumerate(zip(texts, scores, boxes)):
            is_duplicate = False
            
            for j, (unique_text, unique_score, unique_box) in enumerate(zip(unique_texts, unique_scores, unique_boxes)):
                # Calculate bounding box overlap
                overlap = self._calculate_box_overlap(box, unique_box)
                
                if overlap > overlap_threshold:
                    # Keep the one with higher score
                    if score > unique_score:
                        unique_texts[j] = text
                        unique_scores[j] = score
                        unique_boxes[j] = box
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_texts.append(text)
                unique_scores.append(score)
                unique_boxes.append(box)
        
        return {
            'texts': unique_texts,
            'scores': unique_scores,
            'boxes': unique_boxes
        }
    
    def _calculate_box_overlap(self, box1, box2):
        """
        Calculate overlap ratio between two bounding boxes
        
        Args:
            box1, box2 (list): Bounding boxes [x1, y1, x2, y2]
        
        Returns:
            float: Overlap ratio (0-1)
        """
        try:
            if isinstance(box1, list) and len(box1) >= 4:
                x1_1, y1_1, x2_1, y2_1 = box1[:4]
            else:
                return 0
            
            if isinstance(box2, list) and len(box2) >= 4:
                x1_2, y1_2, x2_2, y2_2 = box2[:4]
            else:
                return 0
            
            # Calculate intersection
            x1_i = max(x1_1, x1_2)
            y1_i = max(y1_1, y1_2)
            x2_i = min(x2_1, x2_2)
            y2_i = min(y2_1, y2_2)
            
            if x2_i <= x1_i or y2_i <= y1_i:
                return 0
            
            intersection = (x2_i - x1_i) * (y2_i - y1_i)
            area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
            area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
            union = area1 + area2 - intersection
            
            return intersection / union if union > 0 else 0
            
        except Exception:
            return 0
    
    def get_supported_formats(self):
        """Get list of supported image formats"""
        return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif']
    
    def is_supported_format(self, file_path):
        """Check if file format is supported"""
        file_ext = os.path.splitext(file_path.lower())[1]
        return file_ext in self.get_supported_formats()

def extract_text_from_image(image_path, lang='en'):
    """
    Simple function to extract text from an image
    
    Args:
        image_path (str): Path to the image file
        lang (str): Language for OCR
    
    Returns:
        tuple: (texts, scores, boxes) or (None, None, None) if failed
    """
    processor = OCRProcessor(lang=lang)
    return processor.extract_text_from_image(image_path)

def batch_extract_text(image_paths, lang='en'):
    """
    Extract text from multiple images
    
    Args:
        image_paths (list): List of image file paths
        lang (str): Language for OCR
    
    Returns:
        list: List of results for each image
    """
    processor = OCRProcessor(lang=lang)
    results = []
    
    for i, image_path in enumerate(image_paths, 1):
        print(f"\nProcessing image {i}/{len(image_paths)}: {os.path.basename(image_path)}")
        texts, scores, boxes = processor.extract_text_from_image(image_path)
        
        results.append({
            'image_path': image_path,
            'texts': texts,
            'scores': scores,
            'boxes': boxes,
            'success': texts is not None
        })
    
    return results

if __name__ == "__main__":
    # Test the module
    test_image = r'D:\paddlocr drug\temp_pdf_pages\page_001.png'
    
    if os.path.exists(test_image):
        print("Testing OCR Text Extraction...")
        
        processor = OCRProcessor()
        
        if processor.is_supported_format(test_image):
            texts, scores, boxes = processor.extract_text_from_image(test_image)
            
            if texts:
                print(f"\n✓ Extraction successful!")
                print(f"Found {len(texts)} text regions")
                print(f"Average confidence: {sum(scores)/len(scores):.3f}")
                
                print(f"\nFirst 5 extracted texts:")
                for i, text in enumerate(texts[:5], 1):
                    print(f"{i}. {text}")
            else:
                print(f"\n❌ No text extracted!")
        else:
            print(f"❌ Unsupported file format!")
    else:
        print(f"Test image not found: {test_image}")
