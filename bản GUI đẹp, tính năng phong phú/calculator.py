import time
import re
from typing import Dict, Any, List, Tuple

class Calculator:
    def __init__(self):
        pass
        
    def calculate_wpm(self, user_input: str, elapsed_time: float) -> float:
        if not isinstance(user_input, str):
            raise ValueError("User input must be a string")
            
        if not isinstance(elapsed_time, (int, float)) or elapsed_time <= 0:
            return 0.0
            
        try:
            char_count = len(user_input.strip())
            minutes = elapsed_time / 60.0
            wpm = (char_count / 5.0) / minutes
            return max(0.0, round(wpm, 2))
        except (ZeroDivisionError, ValueError):
            return 0.0
            
    def calculate_accuracy(self, original_text: str, user_input: str) -> float:
        if not isinstance(original_text, str) or not isinstance(user_input, str):
            raise ValueError("Both inputs must be strings")
            
        if not original_text:
            return 100.0
            
        if not user_input:
            return 0.0
            
        try:
            correct_chars = 0
            total_chars = len(original_text)
            comparison_length = min(len(original_text), len(user_input))
            
            for i in range(comparison_length):
                if user_input[i] == original_text[i]:
                    correct_chars += 1
                    
            accuracy = (correct_chars / total_chars) * 100.0
            return max(0.0, min(100.0, round(accuracy, 2)))
            
        except (ZeroDivisionError, IndexError):
            return 0.0
            
    def calculate_error_rate(self, original_text: str, user_input: str) -> float:
        accuracy = self.calculate_accuracy(original_text, user_input)
        return round(100.0 - accuracy, 2)
        
    def calculate_characters_per_minute(self, user_input: str, elapsed_time: float) -> float:
        if not isinstance(user_input, str):
            raise ValueError("User input must be a string")
            
        if not isinstance(elapsed_time, (int, float)) or elapsed_time <= 0:
            return 0.0
            
        try:
            char_count = len(user_input.strip())
            minutes = elapsed_time / 60.0
            cpm = char_count / minutes
            return max(0.0, round(cpm, 2))
        except ZeroDivisionError:
            return 0.0
            
    def analyze_typing_errors(self, original_text: str, user_input: str) -> Dict[str, Any]:
        if not isinstance(original_text, str) or not isinstance(user_input, str):
            raise ValueError("Both inputs must be strings")
            
        try:
            errors = []
            missed_chars = []
            extra_chars = []
            
            comparison_length = min(len(original_text), len(user_input))
            
            for i in range(comparison_length):
                if user_input[i] != original_text[i]:
                    errors.append({
                        'position': i,
                        'expected': original_text[i],
                        'typed': user_input[i]
                    })
                    
            if len(user_input) < len(original_text):
                for i in range(len(user_input), len(original_text)):
                    missed_chars.append({
                        'position': i,
                        'character': original_text[i]
                    })
                    
            elif len(user_input) > len(original_text):
                for i in range(len(original_text), len(user_input)):
                    extra_chars.append({
                        'position': i,
                        'character': user_input[i]
                    })
                    
            return {
                'total_errors': len(errors),
                'character_errors': errors,
                'missed_characters': missed_chars,
                'extra_characters': extra_chars,
                'total_missed': len(missed_chars),
                'total_extra': len(extra_chars)
            }
            
        except Exception:
            return {
                'total_errors': 0,
                'character_errors': [],
                'missed_characters': [],
                'extra_characters': [],
                'total_missed': 0,
                'total_extra': 0
            }
            
    def calculate_keystroke_statistics(self, original_text: str, user_input: str, elapsed_time: float) -> Dict[str, Any]:
        if not isinstance(elapsed_time, (int, float)) or elapsed_time <= 0:
            elapsed_time = 1.0
            
        try:
            total_keystrokes = len(user_input)
            error_analysis = self.analyze_typing_errors(original_text, user_input)
            
            correct_keystrokes = total_keystrokes - error_analysis['total_errors']
            keystrokes_per_minute = (total_keystrokes / elapsed_time) * 60
            
            return {
                'total_keystrokes': total_keystrokes,
                'correct_keystrokes': correct_keystrokes,
                'incorrect_keystrokes': error_analysis['total_errors'],
                'keystrokes_per_minute': round(keystrokes_per_minute, 2),
                'keystroke_accuracy': round((correct_keystrokes / max(total_keystrokes, 1)) * 100, 2)
            }
            
        except Exception:
            return {
                'total_keystrokes': 0,
                'correct_keystrokes': 0,
                'incorrect_keystrokes': 0,
                'keystrokes_per_minute': 0.0,
                'keystroke_accuracy': 0.0
            }
            
    def calculate_word_statistics(self, original_text: str, user_input: str) -> Dict[str, Any]:
        try:
            original_words = re.findall(r'\b\w+\b', original_text.lower())
            user_words = re.findall(r'\b\w+\b', user_input.lower())
            
            total_words = len(original_words)
            typed_words = len(user_words)
            
            correct_words = 0
            comparison_length = min(len(original_words), len(user_words))
            
            for i in range(comparison_length):
                if original_words[i] == user_words[i]:
                    correct_words += 1
                    
            word_accuracy = (correct_words / max(total_words, 1)) * 100
            
            return {
                'total_words': total_words,
                'typed_words': typed_words,
                'correct_words': correct_words,
                'incorrect_words': typed_words - correct_words,
                'missed_words': max(0, total_words - typed_words),
                'word_accuracy': round(word_accuracy, 2)
            }
            
        except Exception:
            return {
                'total_words': 0,
                'typed_words': 0,
                'correct_words': 0,
                'incorrect_words': 0,
                'missed_words': 0,
                'word_accuracy': 0.0
            }
            
    def get_performance_rating(self, wpm: float, accuracy: float) -> str:
        try:
            wpm = float(wpm)
            accuracy = float(accuracy)
            
            if wpm >= 70 and accuracy >= 98:
                return "Expert"
            elif wpm >= 60 and accuracy >= 95:
                return "Advanced"
            elif wpm >= 45 and accuracy >= 90:
                return "Intermediate"
            elif wpm >= 30 and accuracy >= 85:
                return "Beginner+"
            elif wpm >= 15 and accuracy >= 75:
                return "Beginner"
            else:
                return "Needs Practice"
                
        except (ValueError, TypeError):
            return "Unknown"
            
    def calculate_comprehensive_stats(self, original_text: str, user_input: str, elapsed_time: float) -> Dict[str, Any]:
        try:
            basic_stats = {
                'wpm': self.calculate_wpm(user_input, elapsed_time),
                'accuracy': self.calculate_accuracy(original_text, user_input),
                'cpm': self.calculate_characters_per_minute(user_input, elapsed_time),
                'error_rate': self.calculate_error_rate(original_text, user_input),
                'elapsed_time': round(elapsed_time, 2)
            }
            
            error_analysis = self.analyze_typing_errors(original_text, user_input)
            keystroke_stats = self.calculate_keystroke_statistics(original_text, user_input, elapsed_time)
            word_stats = self.calculate_word_statistics(original_text, user_input)
            
            performance_rating = self.get_performance_rating(basic_stats['wpm'], basic_stats['accuracy'])
            
            return {
                'basic_stats': basic_stats,
                'error_analysis': error_analysis,
                'keystroke_stats': keystroke_stats,
                'word_stats': word_stats,
                'performance_rating': performance_rating,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'basic_stats': {'wpm': 0, 'accuracy': 0, 'cpm': 0, 'error_rate': 100, 'elapsed_time': 0},
                'error_analysis': {'total_errors': 0},
                'keystroke_stats': {'total_keystrokes': 0},
                'word_stats': {'total_words': 0},
                'performance_rating': 'Error',
                'timestamp': time.time(),
                'error_message': str(e)
            }