#!/usr/bin/env python3
"""
Dashboard setup script for Grafana
Automatically imports all dashboard configurations
"""

import json
import requests
import time
from pathlib import Path

class GrafanaDashboardSetup:
    def __init__(self, grafana_url="http://localhost:3000", username="admin", password="admin"):
        self.grafana_url = grafana_url
        self.auth = (username, password)
        self.headers = {"Content-Type": "application/json"}
        self.dashboards_dir = Path("dashboards")
    
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
        """Create Prometheus data source if it doesn't exist"""
        print("📊 Setting up Prometheus data source...")
        
        # Check if data source already exists
        try:
            response = requests.get(
                f"{self.grafana_url}/api/datasources/name/Prometheus",
                auth=self.auth
            )
            if response.status_code == 200:
                print("✅ Prometheus data source already exists")
                return True
        except:
            pass
        
        # Create new data source
        data_source = {
            "name": "Prometheus",
            "type": "prometheus",
            "url": "http://localhost:9090",
            "access": "proxy",
            "isDefault": True,
            "basicAuth": False
        }
        
        try:
            response = requests.post(
                f"{self.grafana_url}/api/datasources",
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(data_source)
            )
            
            if response.status_code in [200, 409]:
                print("✅ Prometheus data source created")
                return True
            else:
                print(f"❌ Failed to create data source: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating data source: {e}")
            return False
    
    def import_dashboard(self, dashboard_file):
        """Import a single dashboard from JSON file"""
        print(f"📊 Importing dashboard: {dashboard_file.name}")
        
        try:
            with open(dashboard_file, 'r') as f:
                dashboard_json = json.load(f)
            
            # Prepare import payload
            import_payload = {
                "dashboard": dashboard_json["dashboard"],
                "overwrite": True,
                "inputs": [
                    {
                        "name": "DS_PROMETHEUS",
                        "type": "datasource",
                        "pluginId": "prometheus",
                        "value": "Prometheus"
                    }
                ]
            }
            
            response = requests.post(
                f"{self.grafana_url}/api/dashboards/import",
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(import_payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                dashboard_url = f"{self.grafana_url}/d/{result['uid']}"
                print(f"✅ Dashboard imported: {dashboard_url}")
                return True, dashboard_url
            else:
                print(f"❌ Failed to import {dashboard_file.name}: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"❌ Error importing {dashboard_file.name}: {e}")
            return False, None
    
    def import_all_dashboards(self):
        """Import all dashboard JSON files from dashboards directory"""
        print("📊 Importing all dashboards...")
        
        if not self.dashboards_dir.exists():
            print("❌ Dashboards directory not found")
            return False
        
        dashboard_files = list(self.dashboards_dir.glob("*.json"))
        if not dashboard_files:
            print("❌ No dashboard JSON files found")
            return False
        
        imported_dashboards = []
        failed_imports = []
        
        for dashboard_file in dashboard_files:
            success, url = self.import_dashboard(dashboard_file)
            if success:
                imported_dashboards.append((dashboard_file.name, url))
            else:
                failed_imports.append(dashboard_file.name)
        
        print(f"\n📊 Dashboard Import Summary:")
        print(f"✅ Successfully imported: {len(imported_dashboards)}")
        print(f"❌ Failed imports: {len(failed_imports)}")
        
        if imported_dashboards:
            print("\n🎯 Access your dashboards:")
            for name, url in imported_dashboards:
                print(f"   • {name}: {url}")
        
        if failed_imports:
            print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        
        return len(failed_imports) == 0
    
    def setup(self):
        """Complete dashboard setup"""
        print("🎯 Setting up Grafana Dashboards")
        print("=" * 50)
        
        if not self.wait_for_grafana():
            return False
        
        if not self.create_data_source():
            return False
        
        # Small delay to ensure data source is ready
        time.sleep(2)
        
        success = self.import_all_dashboards()
        
        if success:
            print("\n🎉 All dashboards imported successfully!")
            print(f"\n🎯 Open Grafana: {self.grafana_url}")
            print("📊 Available dashboards:")
            print("   • Production Log Monitoring Dashboard")
            print("   • Payment Service Monitoring")
            print("   • Mobile API Monitoring")
            print("   • Alert & System Health Dashboard")
        else:
            print("\n⚠️ Some dashboards failed to import")
        
        return success

def main():
    """Main function"""
    setup = GrafanaDashboardSetup()
    setup.setup()

if __name__ == "__main__":
    main()