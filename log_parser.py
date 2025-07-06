import re
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dummy_database import db


class LogPatterns:
    """Define regex patterns for log parsing"""
    
    # Log level patterns
    PATTERNS = {
        'critical': r'\[CRITICAL\]|\bCRITICAL\b|\bFATAL\b|\bFatal\b',
        'error': r'\[ERROR\]|\bERROR\b|\bException\b|\bFailed\b|\bError\b',
        'warning': r'\[WARN\]|\[WARNING\]|\bWARN\b|\bWarning\b',
        'info': r'\[INFO\]|\bINFO\b|\bStarted\b|\bCompleted\b',
        'debug': r'\[DEBUG\]|\bDEBUG\b'
    }
    
    # Framework-specific patterns
    FRAMEWORK_PATTERNS = {
        'laravel': r'laravel\.\w+:',
        'django': r'django\.\w+:',
        'express': r'express\.\w+:',
        'spring': r'org\.springframework',
        'flask': r'flask\.\w+'
    }


class LogMetrics:
    """Prometheus' metrics for log monitoring"""
    
    def __init__(self):
        self.log_entries_total = Counter(
            'log_entries_total',
            'Total number of log entries processed',
            ['level', 'source', 'framework']
        )
        
        self.error_count = Counter(
            'log_errors_total',
            'Total number of error-level log entries',
            ['source', 'framework']
        )
        
        self.warning_count = Counter(
            'log_warnings_total',
            'Total number of warning-level log entries',
            ['source', 'framework']
        )
        
        self.processing_time = Histogram(
            'log_processing_seconds',
            'Time spent processing log entries'
        )
        
        self.file_size = Gauge(
            'log_file_size_bytes',
            'Size of log files being monitored',
            ['filename']
        )
        
        self.alerts_sent = Counter(
            'log_alerts_sent_total',
            'Total number of alerts sent',
            ['level', 'type']
        )


class AlertWebhookHandler(BaseHTTPRequestHandler):
    """Handle incoming webhook alerts from Grafana"""
    
    def do_POST(self):
        if self.path == '/alert-webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                alert_data = json.loads(post_data.decode('utf-8'))
                self.process_alert(alert_data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                
            except Exception as e:
                print(f"❌ Error processing webhook: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def process_alert(self, alert_data):
        """Process incoming alert from Grafana"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n🚨 GRAFANA ALERT RECEIVED [{timestamp}] 🚨")
        print(f"   Status: {alert_data.get('status', 'unknown')}")
        print(f"   Title: {alert_data.get('title', 'No title')}")
        print(f"   Message: {alert_data.get('message', 'No message')}")
        print("─" * 60)
    
    def log_message(self, format, *args):
        # Suppress default HTTP server logs
        pass

class LogFileHandler(FileSystemEventHandler):
    """Handle file system events for log files"""
    
    def __init__(self, log_parser):
        self.log_parser = log_parser
        self.last_position = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix == '.log':
            self.log_parser.process_new_lines(file_path)


class LogParser:
    """Main log parser class"""
    
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = Path(log_directory)
        self.patterns = LogPatterns()
        self.metrics = LogMetrics()
        self.file_positions = {}
        self.running = False
        self.observer = None
        
        # Ensure log directory exists
        self.log_directory.mkdir(exist_ok=True)
        
        print(f"🚀 Log Parser initialized")
        print(f"📁 Monitoring directory: {self.log_directory.absolute()}")
    
    def detect_framework(self, line: str) -> str:
        """Detect framework from log line"""
        # Check for framework patterns in log content
        for framework, pattern in self.patterns.FRAMEWORK_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                return framework
        
        # Check for framework indicators in log format
        if re.search(r'\[.*\] local\.(INFO|WARNING|ERROR|CRITICAL):', line):
            return 'laravel'
        elif re.search(r'\[.*\] (INFO|WARNING|ERROR|CRITICAL) django\.', line):
            return 'django'
        elif re.search(r'(INFO|WARNING|ERROR|CRITICAL):', line) and 'FastAPI' in line:
            return 'fastapi'
        elif re.search(r'\[.*\] \[(INFO|WARN|ERROR|CRITICAL)\]', line):
            return 'express'
            
        return 'unknown'
    
    def detect_application(self, source: str) -> str:
        """Detect application name from source file"""
        if source == 'app.log':
            return 'legacy-app'
        
        # Extract app name from filename (e.g., mobile-api.log -> mobile-api)
        app_name = source.replace('.log', '')
        return app_name
    
    def detect_log_level(self, line: str) -> Optional[str]:
        """Detect log level from line"""
        for level, pattern in self.patterns.PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                return level
        return None
    
    def process_log_line(self, line: str, source: str) -> bool:
        """Process a single log line"""
        start_time = time.time()
        
        try:
            # Clean the line
            line = line.strip()
            if not line:
                return False
            
            # Detect level, framework, and application
            level = self.detect_log_level(line)
            framework = self.detect_framework(line)
            application = self.detect_application(source)
            
            if level:
                # Store in database
                db.add_log_entry(
                    level=level,
                    message=line,
                    source=source,
                    framework=framework
                )
                
                # Update metrics
                self.metrics.log_entries_total.labels(
                    level=level,
                    source=source,
                    framework=framework
                ).inc()
                
                if level in ['error', 'critical']:
                    self.metrics.error_count.labels(
                        source=source,
                        framework=framework
                    ).inc()
                    self.send_alert(level, line, source, framework)
                
                elif level == 'warning':
                    self.metrics.warning_count.labels(
                        source=source,
                        framework=framework
                    ).inc()
                
                # Log the detection
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"🔍 [{timestamp}] {level.upper()} detected in {application} ({framework})")
                print(f"   └─ {line[:100]}{'...' if len(line) > 100 else ''}")
                
                return True
        
        except Exception as e:
            print(f"❌ Error processing line: {e}")
            return False
        
        finally:
            # Record processing time
            processing_time = time.time() - start_time
            self.metrics.processing_time.observe(processing_time)
    
    def send_alert(self, level: str, message: str, source: str, framework: str):
        """Send alert for critical/error messages"""
        alert_type = "console"  # For now, just console alerts
        
        # Update alert metrics
        self.metrics.alerts_sent.labels(level=level, type=alert_type).inc()
        
        # Console alert
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n🚨 ALERT [{timestamp}] 🚨")
        print(f"Level: {level.upper()}")
        print(f"Source: {source}")
        print(f"Framework: {framework}")
        print(f"Message: {message}")
        print("-" * 60)
    
    def process_new_lines(self, file_path: Path):
        """Process new lines added to a file"""
        try:
            file_str = str(file_path)
            
            # Update file size metric
            if file_path.exists():
                file_size = file_path.stat().st_size
                self.metrics.file_size.labels(filename=file_path.name).set(file_size)
            
            # Get current position
            current_pos = self.file_positions.get(file_str, 0)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(current_pos)
                new_lines = f.readlines()
                
                # Update position
                self.file_positions[file_str] = f.tell()
                
                # Process new lines
                for line in new_lines:
                    self.process_log_line(line, file_path.name)
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    def process_existing_files(self):
        """Process existing log files on startup"""
        print("Processing existing log files...")
        
        log_files = list(self.log_directory.glob("*.log"))
        if not log_files:
            print("No existing log files found")
            return
        
        for log_file in log_files:
            print(f"Processing: {log_file.name}")
            self.process_new_lines(log_file)
    
    def start_monitoring(self):
        """Start monitoring log files"""
        print("Starting log file monitoring...")
        
        # Process existing files first
        self.process_existing_files()
        
        # Start file system monitoring
        self.observer = Observer()
        handler = LogFileHandler(self)
        self.observer.schedule(handler, str(self.log_directory), recursive=False)
        
        self.observer.start()
        self.running = True
        
        print(f"Monitoring started for {self.log_directory}")
        print("Metrics available at: http://localhost:8000/metrics")
        print("Press Ctrl+C to stop")
        
        try:
            while self.running:
                time.sleep(1)
                
                # Periodic cleanup
                if int(time.time()) % 300 == 0:  # Every 5 minutes
                    db.clear_old_entries(1000)
                    
        except KeyboardInterrupt:
            print("Stopping log parser...")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring log files"""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("Log parser stopped")
    
    def get_status(self) -> Dict:
        """Get current parser status"""
        return {
            'running': self.running,
            'monitored_files': len(self.file_positions),
            'database_stats': db.get_statistics(),
            'log_directory': str(self.log_directory.absolute())
        }


def main():
    """Main function"""
    print("🔧 Universal Log Monitoring Tool - Log Parser")
    print("=" * 50)
    
    # Start Prometheus metrics server
    print("📊 Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)
    
    # Initialize and start log parser
    parser = LogParser()
    
    try:
        parser.start_monitoring()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("Cleanup complete")


if __name__ == "__main__":
    main()
