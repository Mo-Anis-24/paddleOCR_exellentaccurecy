#!/usr/bin/env python3
"""
Text Processing and Saving Module
=================================

This module handles text processing, formatting, and saving OCR results.
Provides various output formats and text analysis features.
"""

import os
import json
import csv
from datetime import datetime

class TextProcessor:
    """Text processor class for OCR results"""
    
    def __init__(self):
        """Initialize text processor"""
        self.results = []
        self.metadata = {}
    
    def add_result(self, page_num, texts, scores, boxes=None, image_path=None):
        """
        Add OCR result for a page
        
        Args:
            page_num (int): Page number
            texts (list): List of extracted texts
            scores (list): List of confidence scores
            boxes (list): List of bounding boxes
            image_path (str): Path to the original image
        """
        result = {
            'page': page_num,
            'texts': texts,
            'scores': scores,
            'boxes': boxes or [],
            'image_path': image_path,
            'text_count': len(texts),
            'avg_confidence': sum(scores) / len(scores) if scores else 0,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
    
    def get_statistics(self):
        """Get overall statistics"""
        if not self.results:
            return {}
        
        total_pages = len(self.results)
        total_texts = sum(r['text_count'] for r in self.results)
        all_scores = []
        for r in self.results:
            all_scores.extend(r['scores'])
        
        avg_confidence = sum(all_scores) / len(all_scores) if all_scores else 0
        
        return {
            'total_pages': total_pages,
            'total_text_regions': total_texts,
            'average_confidence': avg_confidence,
            'min_confidence': min(all_scores) if all_scores else 0,
            'max_confidence': max(all_scores) if all_scores else 0,
            'processing_time': datetime.now().isoformat()
        }
    
    def save_to_txt(self, output_file="extracted_text.txt"):
        """
        Save results to a text file
        
        Args:
            output_file (str): Output file path
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("OCR Text Extraction Results\n")
                f.write("=" * 50 + "\n")
                
                # Add metadata
                stats = self.get_statistics()
                f.write(f"Total Pages: {stats['total_pages']}\n")
                f.write(f"Total Text Regions: {stats['total_text_regions']}\n")
                f.write(f"Average Confidence: {stats['average_confidence']:.3f}\n")
                f.write(f"Processing Time: {stats['processing_time']}\n")
                f.write("=" * 50 + "\n\n")
                
                # Add page-wise results
                for result in self.results:
                    f.write(f"PAGE {result['page']}\n")
                    f.write("-" * 20 + "\n")
                    
                    if result['texts']:
                        for i, (text, score) in enumerate(zip(result['texts'], result['scores']), 1):
                            f.write(f"{i:3d}. {text}\n")
                            f.write(f"     Confidence: {score:.3f}\n\n")
                    else:
                        f.write("No text detected on this page.\n\n")
                    
                    f.write("\n")
                
                # Add all text combined
                f.write("ALL TEXT COMBINED\n")
                f.write("=" * 20 + "\n")
                all_texts = []
                for result in self.results:
                    all_texts.extend(result['texts'])
                
                for i, text in enumerate(all_texts, 1):
                    f.write(f"{i:3d}. {text}\n")
            
            print(f"✓ Text results saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving text file: {e}")
            return False
    
    def save_to_json(self, output_file="extracted_text.json"):
        """
        Save results to a JSON file
        
        Args:
            output_file (str): Output file path
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = {
                'metadata': self.get_statistics(),
                'results': self.results,
                'export_time': datetime.now().isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ JSON results saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving JSON file: {e}")
            return False
    
    
    
    def get_all_texts(self):
        """Get all extracted texts as a single list"""
        all_texts = []
        for result in self.results:
            all_texts.extend(result['texts'])
        return all_texts
    
    def get_texts_by_page(self, page_num):
        """Get texts for a specific page"""
        for result in self.results:
            if result['page'] == page_num:
                return result['texts']
        return []
    
    def search_text(self, search_term, case_sensitive=False):
        """
        Search for text containing the search term
        
        Args:
            search_term (str): Term to search for
            case_sensitive (bool): Whether search should be case sensitive
        
        Returns:
            list: List of matching results
        """
        matches = []
        search_term = search_term if case_sensitive else search_term.lower()
        
        for result in self.results:
            for i, text in enumerate(result['texts']):
                text_to_search = text if case_sensitive else text.lower()
                if search_term in text_to_search:
                    matches.append({
                        'page': result['page'],
                        'text_number': i + 1,
                        'text': text,
                        'confidence': result['scores'][i],
                        'box': result['boxes'][i] if i < len(result['boxes']) else None
                    })
        
        return matches

def save_text_results(results, output_file="extracted_text.txt"):
    """
    Simple function to save text results
    
    Args:
        results (dict): OCR results
        output_file (str): Output file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    processor = TextProcessor()
    
    if results['type'] == 'pdf':
        for page_result in results['page_results']:
            processor.add_result(
                page_result['page'],
                page_result['texts'],
                page_result['scores'],
                page_result.get('boxes', []),
                page_result.get('image_path')
            )
    else:
        processor.add_result(1, results['texts'], results['scores'], results.get('boxes', []))
    
    return processor.save_to_txt(output_file)

if __name__ == "__main__":
    # Test the module
    print("Testing Text Processing Module...")
    
    processor = TextProcessor()
    
    # Add sample results
    processor.add_result(1, ["Sample Text 1", "Sample Text 2"], [0.95, 0.87])
    processor.add_result(2, ["Sample Text 3", "Sample Text 4"], [0.92, 0.89])
    
    # Test statistics
    stats = processor.get_statistics()
    print(f"Statistics: {stats}")
    
    # Test saving
    processor.save_to_txt("test_output.txt")
    processor.save_to_json("test_output.json")
    processor.save_to_csv("test_output.csv")
    
    print("✓ Text processing module tested successfully!")
