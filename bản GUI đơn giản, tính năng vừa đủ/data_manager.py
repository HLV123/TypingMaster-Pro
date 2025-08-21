import random
import os
from typing import List, Dict, Any

class DataManager:
    def __init__(self, txt_file: str = "DATA.txt"):
        self.txt_file = txt_file
        self.texts = []
        self._load_texts()
        
    def _load_texts(self) -> None:
        self.texts = self._load_from_txt(self.txt_file)
        
    def _load_from_txt(self, filename: str) -> List[str]:
        texts = []
        
        if not os.path.exists(filename):
            return texts
            
        # Try multiple encoding formats
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    
                for line in lines:
                    line = line.strip()
                    if line and len(line) >= 10:
                        texts.append(line)
                        
                if texts:
                    return texts
                    
            except (UnicodeDecodeError, IOError):
                continue
                
        return texts
                
    def _save_to_txt(self, filename: str, texts: List[str]) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for text in texts:
                    f.write(text + '\n')
        except IOError as e:
            raise Exception(f"Failed to save to {filename}: {str(e)}")
            
    def get_random_text(self) -> str:
        if not self.texts:
            return ""
            
        selected_text = random.choice(self.texts)
        
        if not isinstance(selected_text, str):
            raise ValueError("Invalid text format")
            
        return selected_text.strip()
        
    def add_text(self, text: str) -> None:
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
            
        cleaned_text = text.strip()
        
        if len(cleaned_text) < 10:
            raise ValueError("Text must be at least 10 characters long")
            
        if len(cleaned_text) > 5000:
            raise ValueError("Text must be less than 5000 characters")
            
        if cleaned_text in self.texts:
            raise ValueError("This text already exists")
            
        self.texts.append(cleaned_text)
        self._save_to_txt(self.txt_file, self.texts)
        
    def import_txt_file(self, filepath: str) -> int:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        try:
            imported_texts = self._load_from_txt(filepath)
            
            if not imported_texts:
                raise ValueError("No valid texts found in file. Make sure each line contains at least 10 characters.")
                
            new_texts_count = 0
            
            for text in imported_texts:
                if text not in self.texts and len(text) >= 10:
                    self.texts.append(text)
                    new_texts_count += 1
                    
            if new_texts_count > 0:
                self._save_to_txt(self.txt_file, self.texts)
                
            return new_texts_count
            
        except Exception as e:
            raise Exception(f"Failed to import file: {str(e)}")
            
    def get_all_texts(self) -> List[str]:
        return self.texts.copy()
        
    def remove_text(self, index: int) -> None:
        if not isinstance(index, int) or index < 0 or index >= len(self.texts):
            raise ValueError("Invalid text index")
            
        self.texts.pop(index)
        self._save_to_txt(self.txt_file, self.texts)
        
    def clear_all_texts(self) -> None:
        self.texts = []
        self._save_to_txt(self.txt_file, self.texts)
            
    def get_text_by_length(self, min_length: int = 0, max_length: int = 10000) -> str:
        filtered_texts = [
            text for text in self.texts 
            if min_length <= len(text) <= max_length
        ]
        
        if not filtered_texts:
            return self.get_random_text()
            
        return random.choice(filtered_texts)
        
    def search_texts(self, keyword: str) -> List[str]:
        if not isinstance(keyword, str) or not keyword.strip():
            return []
            
        keyword = keyword.lower().strip()
        
        matching_texts = [
            text for text in self.texts
            if keyword in text.lower()
        ]
        
        return matching_texts
        
    def get_statistics_summary(self) -> Dict[str, Any]:
        return {
            'total_texts': len(self.texts),
            'txt_file_exists': os.path.exists(self.txt_file),
            'avg_text_length': self._calculate_average_length(),
            'shortest_text': min(len(text) for text in self.texts) if self.texts else 0,
            'longest_text': max(len(text) for text in self.texts) if self.texts else 0
        }
        
    def _calculate_average_length(self) -> float:
        if not self.texts:
            return 0.0
        return round(sum(len(text) for text in self.texts) / len(self.texts), 1)
        
    def reload_texts(self) -> None:
        self._load_texts()
        
    def export_texts(self, filename: str) -> None:
        if not self.texts:
            raise ValueError("No texts to export")
            
        try:
            self._save_to_txt(filename, self.texts)
        except Exception as e:
            raise Exception(f"Failed to export texts: {str(e)}")