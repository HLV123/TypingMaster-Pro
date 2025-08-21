import json
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class StatisticsManager:
    def __init__(self, stats_file: str = "typing_stats.json"):
        self.stats_file = stats_file
        self.data = self._load_statistics()
        
    def _load_statistics(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if self._validate_data_structure(data):
                        return data
                        
            return self._create_empty_structure()
            
        except (json.JSONDecodeError, IOError, KeyError):
            return self._create_empty_structure()
            
    def _create_empty_structure(self) -> Dict[str, Any]:
        return {
            'results': [],
            'session_data': {},
            'preferences': {},
            'created_at': time.time(),
            'last_updated': time.time()
        }
        
    def _validate_data_structure(self, data: Dict) -> bool:
        required_keys = ['results', 'session_data', 'preferences']
        return all(key in data for key in required_keys)
        
    def _save_statistics(self) -> None:
        try:
            self.data['last_updated'] = time.time()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise Exception(f"Failed to save statistics: {str(e)}")
            
    def save_result(self, result: Dict[str, Any]) -> None:
        if not isinstance(result, dict):
            raise ValueError("Result must be a dictionary")
            
        required_fields = ['wpm', 'accuracy', 'time']
        if not all(field in result for field in required_fields):
            raise ValueError(f"Result must contain fields: {required_fields}")
            
        try:
            validated_result = {
                'wpm': float(result['wpm']),
                'accuracy': float(result['accuracy']),
                'time': float(result['time']),
                'text_length': int(result.get('text_length', 0)),
                'user_length': int(result.get('user_length', 0)),
                'timestamp': time.time(),
                'date': datetime.now().isoformat()
            }
            
            if validated_result['wpm'] < 0 or validated_result['accuracy'] < 0:
                raise ValueError("WPM and accuracy must be non-negative")
                
            if validated_result['accuracy'] > 100:
                validated_result['accuracy'] = 100.0
                
            self.data['results'].append(validated_result)
            self._save_statistics()
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid result data: {str(e)}")
            
    def get_statistics(self) -> Dict[str, Any]:
        try:
            results = self.data.get('results', [])
            
            if not results:
                return {
                    'total_tests': 0,
                    'avg_wpm': 0.0,
                    'best_wpm': 0.0,
                    'avg_accuracy': 0.0,
                    'best_accuracy': 0.0,
                    'total_time': 0.0,
                    'recent_results': [],
                    'results': []
                }
                
            wpm_values = [r['wpm'] for r in results if 'wpm' in r]
            accuracy_values = [r['accuracy'] for r in results if 'accuracy' in r]
            time_values = [r['time'] for r in results if 'time' in r]
            
            stats = {
                'total_tests': len(results),
                'avg_wpm': round(sum(wpm_values) / len(wpm_values), 2) if wpm_values else 0.0,
                'best_wpm': round(max(wpm_values), 2) if wpm_values else 0.0,
                'avg_accuracy': round(sum(accuracy_values) / len(accuracy_values), 2) if accuracy_values else 0.0,
                'best_accuracy': round(max(accuracy_values), 2) if accuracy_values else 0.0,
                'total_time': round(sum(time_values), 2) if time_values else 0.0,
                'recent_results': sorted(results, key=lambda x: x.get('timestamp', 0), reverse=True),
                'results': results
            }
            
            return stats
            
        except Exception as e:
            return {
                'total_tests': 0,
                'avg_wpm': 0.0,
                'best_wpm': 0.0,
                'avg_accuracy': 0.0,
                'best_accuracy': 0.0,
                'total_time': 0.0,
                'recent_results': [],
                'results': [],
                'error': str(e)
            }
            
    def get_progress_data(self, days: int = 30) -> Dict[str, Any]:
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            recent_results = [
                r for r in self.data.get('results', [])
                if r.get('timestamp', 0) >= cutoff_time
            ]
            
            if not recent_results:
                return {'dates': [], 'wpm_values': [], 'accuracy_values': []}
                
            sorted_results = sorted(recent_results, key=lambda x: x.get('timestamp', 0))
            
            dates = []
            wpm_values = []
            accuracy_values = []
            
            for result in sorted_results:
                timestamp = result.get('timestamp', 0)
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                dates.append(date_str)
                wpm_values.append(result.get('wpm', 0))
                accuracy_values.append(result.get('accuracy', 0))
                
            return {
                'dates': dates,
                'wpm_values': wpm_values,
                'accuracy_values': accuracy_values,
                'total_sessions': len(sorted_results)
            }
            
        except Exception:
            return {'dates': [], 'wpm_values': [], 'accuracy_values': [], 'total_sessions': 0}
            
    def get_daily_stats(self, date: Optional[str] = None) -> Dict[str, Any]:
        try:
            if date is None:
                target_date = datetime.now().date()
            else:
                target_date = datetime.fromisoformat(date).date()
                
            daily_results = []
            for result in self.data.get('results', []):
                if 'timestamp' in result:
                    result_date = datetime.fromtimestamp(result['timestamp']).date()
                    if result_date == target_date:
                        daily_results.append(result)
                        
            if not daily_results:
                return {
                    'date': target_date.isoformat(),
                    'total_tests': 0,
                    'total_time': 0.0,
                    'avg_wpm': 0.0,
                    'best_wpm': 0.0,
                    'avg_accuracy': 0.0,
                    'best_accuracy': 0.0
                }
                
            wpm_values = [r['wpm'] for r in daily_results]
            accuracy_values = [r['accuracy'] for r in daily_results]
            time_values = [r['time'] for r in daily_results]
            
            return {
                'date': target_date.isoformat(),
                'total_tests': len(daily_results),
                'total_time': round(sum(time_values), 2),
                'avg_wpm': round(sum(wpm_values) / len(wpm_values), 2),
                'best_wpm': round(max(wpm_values), 2),
                'avg_accuracy': round(sum(accuracy_values) / len(accuracy_values), 2),
                'best_accuracy': round(max(accuracy_values), 2)
            }
            
        except Exception:
            return {
                'date': datetime.now().date().isoformat(),
                'total_tests': 0,
                'total_time': 0.0,
                'avg_wpm': 0.0,
                'best_wpm': 0.0,
                'avg_accuracy': 0.0,
                'best_accuracy': 0.0
            }
            
    def get_personal_bests(self) -> Dict[str, Any]:
        try:
            results = self.data.get('results', [])
            
            if not results:
                return {
                    'best_wpm_record': None,
                    'best_accuracy_record': None,
                    'longest_session': None,
                    'most_characters': None
                }
                
            best_wpm = max(results, key=lambda x: x.get('wpm', 0))
            best_accuracy = max(results, key=lambda x: x.get('accuracy', 0))
            longest_session = max(results, key=lambda x: x.get('time', 0))
            most_characters = max(results, key=lambda x: x.get('user_length', 0))
            
            return {
                'best_wpm_record': {
                    'wpm': best_wpm.get('wpm', 0),
                    'accuracy': best_wpm.get('accuracy', 0),
                    'date': datetime.fromtimestamp(best_wpm.get('timestamp', 0)).strftime('%Y-%m-%d') if 'timestamp' in best_wpm else 'Unknown'
                },
                'best_accuracy_record': {
                    'accuracy': best_accuracy.get('accuracy', 0),
                    'wpm': best_accuracy.get('wpm', 0),
                    'date': datetime.fromtimestamp(best_accuracy.get('timestamp', 0)).strftime('%Y-%m-%d') if 'timestamp' in best_accuracy else 'Unknown'
                },
                'longest_session': {
                    'time': longest_session.get('time', 0),
                    'wpm': longest_session.get('wpm', 0),
                    'date': datetime.fromtimestamp(longest_session.get('timestamp', 0)).strftime('%Y-%m-%d') if 'timestamp' in longest_session else 'Unknown'
                },
                'most_characters': {
                    'characters': most_characters.get('user_length', 0),
                    'wpm': most_characters.get('wpm', 0),
                    'date': datetime.fromtimestamp(most_characters.get('timestamp', 0)).strftime('%Y-%m-%d') if 'timestamp' in most_characters else 'Unknown'
                }
            }
            
        except Exception:
            return {
                'best_wpm_record': None,
                'best_accuracy_record': None,
                'longest_session': None,
                'most_characters': None
            }
            
    def clear_all_data(self) -> None:
        try:
            self.data = self._create_empty_structure()
            self._save_statistics()
        except Exception as e:
            raise Exception(f"Failed to clear data: {str(e)}")
            
    def export_data(self, filename: Optional[str] = None) -> str:
        try:
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"typing_stats_export_{timestamp}.json"
                
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'statistics': self.get_statistics(),
                'raw_data': self.data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
                
            return filename
            
        except Exception as e:
            raise Exception(f"Failed to export data: {str(e)}")
            
    def import_data(self, filename: str) -> None:
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File not found: {filename}")
                
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
                
            if 'raw_data' in imported_data and self._validate_data_structure(imported_data['raw_data']):
                self.data = imported_data['raw_data']
                self._save_statistics()
            else:
                raise ValueError("Invalid import file format")
                
        except Exception as e:
            raise Exception(f"Failed to import data: {str(e)}")
            
    def get_file_info(self) -> Dict[str, Any]:
        try:
            file_exists = os.path.exists(self.stats_file)
            file_size = os.path.getsize(self.stats_file) if file_exists else 0
            
            return {
                'file_exists': file_exists,
                'file_size_bytes': file_size,
                'file_path': os.path.abspath(self.stats_file),
                'total_results': len(self.data.get('results', [])),
                'created_at': self.data.get('created_at'),
                'last_updated': self.data.get('last_updated')
            }
            
        except Exception:
            return {
                'file_exists': False,
                'file_size_bytes': 0,
                'file_path': '',
                'total_results': 0,
                'created_at': None,
                'last_updated': None
            }