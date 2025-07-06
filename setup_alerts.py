#!/usr/bin/env python3
"""
Setup script for Grafana alerts and notifications
"""

import json
import time
import requests
from pathlib import Path


class GrafanaAlertSetup:
    def __init__(self, grafana_url="http://localhost:3000", username="admin", password="admin"):
        self.grafana_url = grafana_url
        self.auth = (username, password)
        self.headers = {"Content-Type": "application/json"}
    
    def wait_for_grafana(self, max_attempts=30):
        """Wait for Grafana to be available"""
        print("⏳ Waiting for Grafana to be available...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.grafana_url}/api/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Grafana is available")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
            print(f"   Attempt {attempt + 1}/{max_attempts}...")
        
        print("❌ Grafana is not available")
        return False
    
    def create_data_source(self):
        """Create Prometheus data source"""
        print("📊 Setting up Prometheus data source...")
        
        data_source = {
            "name": "Prometheus",
            "type": "prometheus",
            "url": "http://localhost:9090",
            "access": "proxy",
            "isDefault": True
        }
        
        try:
            response = requests.post(
                f"{self.grafana_url}/api/datasources",
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(data_source)
            )
            
            if response.status_code in [200, 409]:  # 409 means already exists
                print("✅ Prometheus data source configured")
                return True
            else:
                print(f"❌ Failed to create data source: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating data source: {e}")
            return False
    
    def create_notification_channel_email(self):
        """Create email notification channel"""
        print("📧 Setting up email notification channel...")
        
        notification_channel = {
            "name": "email-alerts",
            "type": "email",
            "settings": {
                "addresses": "admin@example.com",
                "singleEmail": False,
                "subject": "🚨 Log Monitoring Alert"
            }
        }
        
        try:
            response = requests.post(
                f"{self.grafana_url}/api/alert-notifications",
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(notification_channel)
            )
            
            if response.status_code in [200, 409]:
                print("✅ Email notification channel created")
                return True
            else:
                print(f"❌ Failed to create email channel: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating email channel: {e}")
            return False
    
    def create_webhook_notification(self):
        """Create webhook notification for console alerts"""
        print("🔗 Setting up webhook notification...")
        
        webhook_channel = {
            "name": "console-webhook",
            "type": "webhook",
            "settings": {
                "url": "http://localhost:8000/alert-webhook",
                "httpMethod": "POST",
                "title": "Log Alert: {{ .CommonLabels.alertname }}",
                "body": "{{ json . }}"
            }
        }
        
        try:
            response = requests.post(
                f"{self.grafana_url}/api/alert-notifications",
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(webhook_channel)
            )
            
            if response.status_code in [200, 409]:
                print("✅ Webhook notification channel created")
                return True
            else:
                print(f"❌ Failed to create webhook channel: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating webhook channel: {e}")
            return False
    
    def setup(self):
        """Setup complete alerting system"""
        print("🚨 Setting up Grafana Alerting System")
        print("=" * 50)
        
        if not self.wait_for_grafana():
            return False
        
        success = True
        success &= self.create_data_source()
        success &= self.create_notification_channel_email()
        success &= self.create_webhook_notification()
        
        if success:
            print("\n✅ Alert setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Open Grafana at http://localhost:3000")
            print("2. Go to Alerting → Alert Rules")
            print("3. Create new alert rules using these queries:")
            print("   - High Error Rate: rate(log_errors_total[5m]) * 60 > 5")
            print("   - Critical Errors: increase(log_entries_total{level=\"critical\"}[1m]) > 0")
            print("   - Service Down: rate(log_entries_total{source=~\".*-service.log\"}[5m]) == 0")
            print("4. Assign notification channels to your alert rules")
        else:
            print("\n❌ Alert setup failed")
        
        return success


def main():
    """Main function"""
    setup = GrafanaAlertSetup()
    setup.setup()


if __name__ == "__main__":
    main()
