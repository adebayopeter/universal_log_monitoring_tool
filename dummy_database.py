from datetime import datetime
from typing import Dict, List, Optional
import threading


class DummyDatabase:
    def __init__(self):
        self.lock = threading.Lock()
        self.storage = {
            'entries': [],
            'statistics': {
                'total_entries': 0,
                'error_count': 0,
                'warning_count': 0,
                'info_count': 0,
                'debug_count': 0,
                'last_processed': None
            }
        }
    
    def add_log_entry(self, level: str, message: str, source: str = 'app.log', framework: str = 'unknown') -> bool:
        """Add a log entry to the database"""
        with self.lock:
            entry = {
                'timestamp': datetime.now(),
                'level': level.lower(),
                'message': message,
                'source': source,
                'framework': framework,
                'alert_sent': False
            }
            
            self.storage['entries'].append(entry)
            self.storage['statistics']['total_entries'] += 1
            self.storage['statistics']['last_processed'] = datetime.now()
            
            # Update level-specific counters
            level_key = f"{level.lower()}_count"
            if level_key in self.storage['statistics']:
                self.storage['statistics'][level_key] += 1
            
            return True
    
    def get_recent_entries(self, limit: int = 100) -> List[Dict]:
        """Get recent log entries"""
        with self.lock:
            return self.storage['entries'][-limit:]
    
    def get_entries_by_level(self, level: str, limit: int = 50) -> List[Dict]:
        """Get entries filtered by log level"""
        with self.lock:
            filtered = [entry for entry in self.storage['entries'] 
                       if entry['level'] == level.lower()]
            return filtered[-limit:]
    
    def get_statistics(self) -> Dict:
        """Get current statistics"""
        with self.lock:
            return self.storage['statistics'].copy()
    
    def mark_alert_sent(self, entry_index: int) -> bool:
        """Mark that an alert has been sent for this entry"""
        with self.lock:
            if 0 <= entry_index < len(self.storage['entries']):
                self.storage['entries'][entry_index]['alert_sent'] = True
                return True
            return False
    
    def get_unalerted_errors(self) -> List[Dict]:
        """Get error entries that haven't had alerts sent"""
        with self.lock:
            return [entry for entry in self.storage['entries'] 
                   if entry['level'] in ['error', 'critical'] and not entry['alert_sent']]
    
    def clear_old_entries(self, keep_last: int = 1000):
        """Keep only the most recent entries to prevent memory issues"""
        with self.lock:
            if len(self.storage['entries']) > keep_last:
                self.storage['entries'] = self.storage['entries'][-keep_last:]
    
    def get_summary(self) -> str:
        """Get a summary string of the current state"""
        stats = self.get_statistics()
        return f"""
            Database Summary:
            - Total entries: {stats['total_entries']}
            - Errors: {stats['error_count']}
            - Warnings: {stats['warning_count']}  
            - Info: {stats['info_count']}
            - Debug: {stats['debug_count']}
            - Last processed: {stats['last_processed']}
        """


# Global instance
db = DummyDatabase()
