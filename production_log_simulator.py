#!/usr/bin/env python3
"""
Production Log Simulator
Generates realistic logs from multiple applications and frameworks
"""

import random
import time
import threading
from datetime import datetime
from pathlib import Path
import json

class ProductionLogSimulator:
    def __init__(self, log_directory="logs"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.running = False
        
        # Application configurations
        self.applications = {
            "mobile-api": {
                "framework": "fastapi",
                "log_file": "mobile-api.log",
                "error_rate": 0.15,  # 15% chance of errors
                "request_rate": 3.0   # 3 requests per second average
            },
            "web-frontend": {
                "framework": "express",
                "log_file": "web-frontend.log", 
                "error_rate": 0.08,
                "request_rate": 5.0
            },
            "user-service": {
                "framework": "django",
                "log_file": "user-service.log",
                "error_rate": 0.12,
                "request_rate": 2.0
            },
            "payment-service": {
                "framework": "laravel",
                "log_file": "payment-service.log",
                "error_rate": 0.20,  # Higher error rate for critical service
                "request_rate": 1.5
            },
            "notification-service": {
                "framework": "fastapi",
                "log_file": "notification-service.log",
                "error_rate": 0.10,
                "request_rate": 4.0
            },
            "analytics-service": {
                "framework": "django",
                "log_file": "analytics-service.log",
                "error_rate": 0.05,
                "request_rate": 1.0
            },
            "admin-panel": {
                "framework": "laravel",
                "log_file": "admin-panel.log",
                "error_rate": 0.07,
                "request_rate": 0.5
            }
        }
        
        # Log message templates by framework and level
        self.log_templates = {
            "fastapi": {
                "info": [
                    "INFO: {timestamp} - {method} {endpoint} - {ip} - {status} - {response_time}ms",
                    "INFO: {timestamp} - User {user_id} authenticated successfully",
                    "INFO: {timestamp} - Cache hit for key: {cache_key}",
                    "INFO: {timestamp} - Database query executed in {query_time}ms",
                    "INFO: {timestamp} - Background task {task_id} completed",
                    "INFO: {timestamp} - API rate limit: {requests}/min for {ip}"
                ],
                "warning": [
                    "WARNING: {timestamp} - Slow query detected: {query_time}ms for {query}",
                    "WARNING: {timestamp} - High memory usage: {memory_percent}%",
                    "WARNING: {timestamp} - Rate limit approaching for {ip}: {rate}/min",
                    "WARNING: {timestamp} - Cache miss rate high: {miss_rate}%",
                    "WARNING: {timestamp} - Connection pool nearly full: {pool_size}/{max_pool}",
                    "WARNING: {timestamp} - Deprecated API endpoint accessed: {endpoint}"
                ],
                "error": [
                    "ERROR: {timestamp} - {method} {endpoint} - {ip} - 500 - {response_time}ms - {error}",
                    "ERROR: {timestamp} - Database connection failed: {db_error}",
                    "ERROR: {timestamp} - External API timeout: {api_name} ({timeout}s)",
                    "ERROR: {timestamp} - Validation failed for {field}: {value}",
                    "ERROR: {timestamp} - Authentication failed for user: {user_id}",
                    "ERROR: {timestamp} - File upload failed: {filename} - {file_error}"
                ],
                "critical": [
                    "CRITICAL: {timestamp} - Service unavailable: All workers down",
                    "CRITICAL: {timestamp} - Database connection pool exhausted",
                    "CRITICAL: {timestamp} - Memory usage critical: {memory_percent}%",
                    "CRITICAL: {timestamp} - Security breach detected from {ip}",
                    "CRITICAL: {timestamp} - Disk space critically low: {disk_space}% remaining"
                ]
            },
            "django": {
                "info": [
                    "[{timestamp}] INFO django.request: {method} {endpoint} - {status} [{response_time}ms]",
                    "[{timestamp}] INFO django.auth: User '{username}' logged in from {ip}",
                    "[{timestamp}] INFO django.db: Query executed in {query_time}ms",
                    "[{timestamp}] INFO django.cache: Cache key '{cache_key}' retrieved",
                    "[{timestamp}] INFO django.middleware: Middleware '{middleware}' processed",
                    "[{timestamp}] INFO django.signals: Signal '{signal}' emitted"
                ],
                "warning": [
                    "[{timestamp}] WARNING django.request: Slow request {endpoint} took {response_time}ms",
                    "[{timestamp}] WARNING django.db: Slow query: {query} ({query_time}ms)",
                    "[{timestamp}] WARNING django.security: Multiple failed login attempts from {ip}",
                    "[{timestamp}] WARNING django.cache: High cache miss rate: {miss_rate}%",
                    "[{timestamp}] WARNING django.middleware: Request timeout warning: {timeout}s"
                ],
                "error": [
                    "[{timestamp}] ERROR django.request: {method} {endpoint} - 500 - {error}",
                    "[{timestamp}] ERROR django.db: Database error: {db_error}",
                    "[{timestamp}] ERROR django.auth: Authentication failed for user '{username}'",
                    "[{timestamp}] ERROR django.views: View error in {view}: {view_error}",
                    "[{timestamp}] ERROR django.middleware: Middleware error: {middleware_error}"
                ],
                "critical": [
                    "[{timestamp}] CRITICAL django.security: Security breach attempt from {ip}",
                    "[{timestamp}] CRITICAL django.db: Database corruption detected",
                    "[{timestamp}] CRITICAL django.system: Out of memory condition",
                    "[{timestamp}] CRITICAL django.request: Service overloaded - rejecting requests"
                ]
            },
            "laravel": {
                "info": [
                    "[{timestamp}] local.INFO: {method} {endpoint} {{\"ip\":\"{ip}\",\"user_id\":{user_id}}}",
                    "[{timestamp}] local.INFO: User {user_id} logged in {{\"ip\":\"{ip}\"}}",
                    "[{timestamp}] local.INFO: Database query executed {{\"time\":{query_time}}}",
                    "[{timestamp}] local.INFO: Cache retrieved {{\"key\":\"{cache_key}\"}}",
                    "[{timestamp}] local.INFO: Job {job_name} processed {{\"queue\":\"{queue}\"}}",
                    "[{timestamp}] local.INFO: Mail sent {{\"to\":\"{email}\",\"subject\":\"{subject}\"}}"
                ],
                "warning": [
                    "[{timestamp}] local.WARNING: Slow query detected {{\"query\":\"{query}\",\"time\":{query_time}}}",
                    "[{timestamp}] local.WARNING: High memory usage {{\"usage\":\"{memory_percent}%\"}}",
                    "[{timestamp}] local.WARNING: Queue backlog {{\"jobs\":{queue_size}}}",
                    "[{timestamp}] local.WARNING: Failed job retry {{\"job\":\"{job_name}\",\"attempt\":{attempt}}}",
                    "[{timestamp}] local.WARNING: Rate limit warning {{\"ip\":\"{ip}\",\"hits\":{hits}}}"
                ],
                "error": [
                    "[{timestamp}] local.ERROR: {error} {{\"file\":\"{file}\",\"line\":{line}}}",
                    "[{timestamp}] local.ERROR: Database query failed {{\"query\":\"{query}\",\"error\":\"{db_error}\"}}",
                    "[{timestamp}] local.ERROR: Payment processing failed {{\"order_id\":{order_id},\"error\":\"{payment_error}\"}}",
                    "[{timestamp}] local.ERROR: File upload error {{\"file\":\"{filename}\",\"error\":\"{file_error}\"}}",
                    "[{timestamp}] local.ERROR: API call failed {{\"url\":\"{api_url}\",\"error\":\"{api_error}\"}}"
                ],
                "critical": [
                    "[{timestamp}] local.CRITICAL: Application down {{\"reason\":\"{reason}\"}}",
                    "[{timestamp}] local.CRITICAL: Database connection lost {{\"host\":\"{db_host}\"}}",
                    "[{timestamp}] local.CRITICAL: Security alert {{\"type\":\"{security_type}\",\"ip\":\"{ip}\"}}",
                    "[{timestamp}] local.CRITICAL: Disk space critical {{\"partition\":\"{partition}\",\"free\":\"{free_space}\"}}"
                ]
            },
            "express": {
                "info": [
                    "{timestamp} [INFO] {method} {endpoint} {status} {response_time}ms - {ip}",
                    "{timestamp} [INFO] User {user_id} authenticated - {ip}",
                    "{timestamp} [INFO] Static file served: {filename}",
                    "{timestamp} [INFO] Session created for user {user_id}",
                    "{timestamp} [INFO] Middleware '{middleware}' executed in {execution_time}ms",
                    "{timestamp} [INFO] WebSocket connection established - {ip}"
                ],
                "warning": [
                    "{timestamp} [WARN] Slow response: {endpoint} took {response_time}ms",
                    "{timestamp} [WARN] Memory usage high: {memory_percent}%", 
                    "{timestamp} [WARN] Too many requests from {ip}: {request_count}/min",
                    "{timestamp} [WARN] Large payload detected: {payload_size}MB",
                    "{timestamp} [WARN] Session store nearly full: {session_count} sessions"
                ],
                "error": [
                    "{timestamp} [ERROR] {method} {endpoint} 500 {response_time}ms - {error}",
                    "{timestamp} [ERROR] Database connection error: {db_error}",
                    "{timestamp} [ERROR] File not found: {filename}",
                    "{timestamp} [ERROR] Authentication failed for user {user_id}",
                    "{timestamp} [ERROR] External service error: {service_name} - {service_error}"
                ],
                "critical": [
                    "{timestamp} [CRITICAL] Server overload - rejecting connections",
                    "{timestamp} [CRITICAL] Database pool exhausted",
                    "{timestamp} [CRITICAL] Memory leak detected - restarting",
                    "{timestamp} [CRITICAL] Security breach from {ip} - blocking"
                ]
            }
        }
        
        # Sample data for templates
        self.sample_data = {
            "endpoints": ["/api/users", "/api/orders", "/api/products", "/api/auth", "/api/payments", 
                         "/api/notifications", "/dashboard", "/profile", "/checkout", "/search"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "ips": ["192.168.1.{}".format(i) for i in range(1, 255)],
            "errors": ["Internal Server Error", "Timeout Error", "Validation Error", "Connection Error", 
                      "Authentication Error", "Authorization Error", "Not Found Error"],
            "usernames": ["john_doe", "jane_smith", "admin", "test_user", "api_user"],
            "filenames": ["upload.jpg", "document.pdf", "data.csv", "image.png", "backup.zip"]
        }
    
    def generate_sample_values(self):
        """Generate random sample values for log templates"""
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": random.choice(self.sample_data["methods"]),
            "endpoint": random.choice(self.sample_data["endpoints"]),
            "ip": random.choice(self.sample_data["ips"]),
            "status": random.choice([200, 201, 400, 401, 403, 404, 500]),
            "response_time": random.randint(10, 2000),
            "user_id": random.randint(1, 10000),
            "cache_key": f"cache_{random.randint(1000, 9999)}",
            "query_time": random.randint(5, 500),
            "task_id": f"task_{random.randint(1000, 9999)}",
            "requests": random.randint(50, 150),
            "memory_percent": random.randint(60, 95),
            "rate": random.randint(80, 120),
            "miss_rate": random.randint(10, 40),
            "pool_size": random.randint(80, 100),
            "max_pool": 100,
            "error": random.choice(self.sample_data["errors"]),
            "db_error": "Connection timeout after 30s",
            "api_name": "external_api",
            "timeout": random.randint(10, 30),
            "field": "email",
            "value": "invalid_email",
            "filename": random.choice(self.sample_data["filenames"]),
            "file_error": "File size too large",
            "disk_space": random.randint(1, 10),
            "username": random.choice(self.sample_data["usernames"]),
            "query": "SELECT * FROM users WHERE id = ?",
            "middleware": "auth_middleware",
            "signal": "user_logged_in",
            "view": "UserProfileView",
            "view_error": "Template not found",
            "middleware_error": "Timeout in middleware",
            "job_name": "SendEmailJob",
            "queue": "default",
            "email": "user@example.com",
            "subject": "Welcome Email",
            "attempt": random.randint(1, 3),
            "hits": random.randint(90, 110),
            "file": "UserController.php",
            "line": random.randint(50, 200),
            "order_id": random.randint(10000, 99999),
            "payment_error": "Credit card declined",
            "api_url": "https://api.external.com/endpoint",
            "api_error": "Service unavailable",
            "reason": "Memory exhausted",
            "db_host": "db.example.com",
            "security_type": "SQL Injection Attempt",
            "partition": "/var/log",
            "free_space": "2GB",
            "execution_time": random.randint(1, 50),
            "request_count": random.randint(100, 200),
            "payload_size": random.randint(5, 50),
            "session_count": random.randint(800, 1000),
            "service_name": "external_payment_api",
            "service_error": "Gateway timeout"
        }
    
    def get_log_level(self, app_config):
        """Determine log level based on error rate"""
        rand = random.random()
        error_rate = app_config["error_rate"]
        
        if rand < error_rate * 0.1:  # 10% of errors are critical
            return "critical"
        elif rand < error_rate * 0.3:  # 30% of errors are errors
            return "error"
        elif rand < error_rate * 0.6:  # 60% of errors are warnings
            return "warning"
        else:
            return "info"
    
    def generate_log_entry(self, app_name, app_config):
        """Generate a single log entry for an application"""
        framework = app_config["framework"]
        level = self.get_log_level(app_config)
        
        # Get template and format with sample data
        templates = self.log_templates[framework][level]
        template = random.choice(templates)
        values = self.generate_sample_values()
        
        try:
            log_entry = template.format(**values)
            return log_entry
        except KeyError as e:
            # Fallback if template formatting fails
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"[{timestamp}] {level.upper()}: {app_name} - Sample log entry"
    
    def write_log_entry(self, app_name, app_config):
        """Write a log entry to the application's log file"""
        log_entry = self.generate_log_entry(app_name, app_config)
        log_file_path = self.log_directory / app_config["log_file"]
        
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def simulate_application(self, app_name, app_config):
        """Simulate logs for a single application"""
        print(f"🚀 Starting log simulation for {app_name} ({app_config['framework']})")
        
        while self.running:
            try:
                # Generate log entry
                self.write_log_entry(app_name, app_config)
                
                # Wait based on request rate (with some randomness)
                base_interval = 1.0 / app_config["request_rate"]
                actual_interval = base_interval * random.uniform(0.5, 2.0)
                time.sleep(actual_interval)
                
            except Exception as e:
                print(f"❌ Error in {app_name} simulator: {e}")
                time.sleep(1)
    
    def start_simulation(self):
        """Start the production log simulation"""
        print("🏭 Starting Production Log Simulator")
        print("=" * 50)
        
        self.running = True
        threads = []
        
        # Start a thread for each application
        for app_name, app_config in self.applications.items():
            thread = threading.Thread(
                target=self.simulate_application,
                args=(app_name, app_config),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        print(f"✅ Started {len(threads)} application simulators")
        print("📊 Generating logs in real-time...")
        print("🛑 Press Ctrl+C to stop")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping production log simulator...")
            self.stop_simulation()
    
    def stop_simulation(self):
        """Stop the log simulation"""
        self.running = False
        print("✅ Production log simulator stopped")
    
    def get_status(self):
        """Get current simulation status"""
        return {
            "running": self.running,
            "applications": list(self.applications.keys()),
            "log_directory": str(self.log_directory.absolute()),
            "total_apps": len(self.applications)
        }

def main():
    """Main function to run the production log simulator"""
    simulator = ProductionLogSimulator()
    
    try:
        simulator.start_simulation()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🔚 Cleanup complete")

if __name__ == "__main__":
    main()