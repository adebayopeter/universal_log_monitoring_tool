# 🔍 Universal Log Monitoring Tool

> **A lightweight, framework-agnostic log monitoring solution with real-time alerting and beautiful dashboards**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Grafana](https://img.shields.io/badge/Grafana-Compatible-orange.svg)](https://grafana.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-Compatible-red.svg)](https://prometheus.io)

## 🎯 Overview

The Universal Log Monitoring Tool is a production-ready monitoring solution that works with **any web application framework**. It provides real-time log analysis, intelligent alerting, and comprehensive dashboards - all without requiring complex setup or expensive infrastructure.

### ✨ Key Features

- 🌐 **Framework Agnostic**: Works with Laravel, Django, FastAPI, Express.js, Spring Boot, and more
- ⚡ **Real-time Monitoring**: Instant log processing with file watching
- 🚨 **Smart Alerting**: Pattern-based alerts with multiple notification channels
- 📊 **Beautiful Dashboards**: Pre-built Grafana dashboards for production monitoring
- 🏗️ **Production Simulator**: Realistic log generation for testing and demos
- 🔧 **Easy Setup**: Get running in under 5 minutes
- 📈 **Scalable**: From single apps to microservices architectures

### 🎬 Quick Demo

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/universal-log-monitoring-tool.git
cd universal-log-monitoring-tool
pip install -r requirements.txt

# 2. Start monitoring stack
python log_parser.py &
python production_log_simulator.py &

# 3. Setup dashboards
python setup_dashboards.py

# 4. Open Grafana at http://localhost:3000 (admin/admin)
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Application   │───▶│   Log Parser     │───▶│   Prometheus    │
│   Log Files     │    │   (Python)       │    │   (Metrics)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Alerting      │◀───│  In-Memory DB    │    │    Grafana      │
│   (Email/Slack) │    │   (Storage)      │    │  (Dashboards)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **2GB RAM** minimum
- **macOS, Linux, or Windows** (WSL recommended for Windows)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/universal-log-monitoring-tool.git
cd universal-log-monitoring-tool

# Install Python dependencies
pip install -r requirements.txt

# Install Ansible (if not already installed)
pip install ansible
```

### 2. Download Monitoring Stack

Download the latest versions:

- **Prometheus**: https://prometheus.io/download/
- **Grafana**: https://grafana.com/grafana/download  
- **Node Exporter**: https://prometheus.io/download/#node_exporter

Extract them to their respective directories:
```
prometheus/prometheus-x.x.x/
grafana/grafana-vx.x.x/
node_exporter/node_exporter-x.x.x/
```

### 3. Start the Monitoring Stack

```bash
# Terminal 1: Start Node Exporter
./node_exporter/node_exporter-*/node_exporter

# Terminal 2: Start Prometheus
./prometheus/prometheus-*/prometheus --config.file=prometheus.yml

# Terminal 3: Start Grafana
./grafana/grafana-v*/bin/grafana-server

# Terminal 4: Start Log Parser
python log_parser.py

# Terminal 5: Generate Test Logs
python production_log_simulator.py
```

### 4. Setup Dashboards & Alerts

```bash
# Import dashboards automatically
python setup_dashboards.py

# Setup alert notifications
python setup_alerts.py
```

### 5. Access Your Monitoring

- **Grafana Dashboards**: http://localhost:3000 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090
- **Log Parser Metrics**: http://localhost:8000/metrics

## 📊 Dashboards

### 🏭 Production Monitoring Dashboard
Comprehensive overview of your entire system:
- Real-time error rates and trends
- Application health status
- Framework distribution analysis
- Alert summary and system performance

### 💳 Payment Service Dashboard  
Business-critical payment monitoring:
- Payment success rates
- Transaction volume tracking
- Error analysis and trends
- Critical payment alerts

### 📱 Mobile API Dashboard
Mobile application monitoring:
- API request rates and performance
- Error rate analysis
- FastAPI-specific metrics
- Mobile traffic patterns

### 🚨 Alert & System Health Dashboard
System monitoring and incident response:
- Component health status
- Alert frequency analysis
- Performance metrics
- Log file growth monitoring

## 🛠️ Supported Frameworks

The tool automatically detects and works with:

| Framework | Log Format | Status |
|-----------|------------|---------|
| **Laravel** | `[timestamp] local.LEVEL: message` | ✅ Supported |
| **Django** | `[timestamp] LEVEL django.module: message` | ✅ Supported |
| **FastAPI** | `LEVEL: timestamp - message` | ✅ Supported |
| **Express.js** | `timestamp [LEVEL] message` | ✅ Supported |
| **Spring Boot** | `timestamp LEVEL --- [thread] class : message` | 🔄 Coming Soon |
| **Flask** | `timestamp LEVEL message` | 🔄 Coming Soon |

## 🔧 Configuration

### Adding New Applications

1. **Create log files** in the `logs/` directory:
   ```bash
   touch logs/your-app.log
   ```

2. **Update monitoring** - the log parser automatically detects new log files

3. **Create custom dashboard** using the provided templates

### Custom Alert Rules

Edit `grafana_alert_config.json` to add new alerts:

```json
{
  "name": "Custom Error Alert",
  "query": "rate(log_errors_total{source=\"your-app.log\"}[5m]) * 60",
  "condition": "> 3",
  "description": "Alert when your app has more than 3 errors per minute"
}
```

### Environment Variables

```bash
# Grafana Configuration
GRAFANA_URL=http://localhost:3000
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# Prometheus Configuration  
PROMETHEUS_URL=http://localhost:9090

# Log Parser Configuration
LOG_DIRECTORY=logs
METRICS_PORT=8000
```

## 📈 Production Deployment

### Docker Deployment (Recommended)

```dockerfile
# Dockerfile example
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "log_parser.py"]
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: log-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: log-monitoring
  template:
    metadata:
      labels:
        app: log-monitoring
    spec:
      containers:
      - name: log-parser
        image: your-registry/log-monitoring:latest
        ports:
        - containerPort: 8000
```

### Scaling Considerations

- **Multiple log files**: The parser automatically handles multiple applications
- **High volume**: Implements log rotation and memory management
- **Distributed setup**: Use Prometheus federation for multiple instances
- **Production databases**: Replace in-memory storage with PostgreSQL/Redis

## 🚨 Alerting

### Built-in Alert Rules

1. **High Error Rate**: `> 5 errors/minute`
2. **Critical Errors**: Any critical log entry
3. **Service Down**: No logs for 1+ minutes
4. **Memory Warnings**: High warning message frequency
5. **Log Growth**: Rapid file size increase

### Notification Channels

- **Email**: SMTP configuration
- **Slack**: Webhook integration
- **Webhook**: Custom HTTP endpoints
- **Console**: Terminal notifications

### Example Slack Integration

```json
{
  "name": "slack-alerts",
  "type": "slack", 
  "settings": {
    "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "channel": "#alerts",
    "title": "🚨 Production Alert: {{ .CommonLabels.alertname }}"
  }
}
```

## 🧪 Testing & Development

### Run Tests

```bash
# Unit tests
python -m pytest tests/

# Integration tests  
python tests/test_integration.py

# Load testing
python tests/load_test.py
```

### Development Mode

```bash
# Start with debug logging
DEBUG=true python log_parser.py

# Generate test logs
python -c "
import time
while True:
    with open('logs/test.log', 'a') as f:
        f.write(f'[ERROR] Test error at {time.time()}\n')
    time.sleep(1)
"
```

## 📚 API Reference

### Metrics Endpoints

- `GET /metrics` - Prometheus metrics
- `POST /alert-webhook` - Grafana alert webhook
- `GET /health` - Health check endpoint
- `GET /status` - Parser status and statistics

### Example Metrics

```prometheus
# Log entries by level and framework
log_entries_total{level="error",framework="django",source="user-service.log"} 42

# Processing performance
log_processing_seconds_bucket{le="0.1"} 1000

# File sizes
log_file_size_bytes{filename="payment-service.log"} 1048576
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/universal-log-monitoring-tool.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
```

### Submitting Changes

1. **Create an issue** describing the feature/bug
2. **Fork the repository** and create a feature branch
3. **Make your changes** with tests and documentation
4. **Submit a pull request** with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Prometheus** team for the excellent metrics system
- **Grafana** team for the beautiful dashboards
- **Python Watchdog** for file monitoring capabilities
- **FastAPI, Django, Laravel, Express** communities for inspiration

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/universal-log-monitoring-tool/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/universal-log-monitoring-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/universal-log-monitoring-tool/discussions)
- **Email**: your-email@domain.com

## 🗺️ Roadmap

### Version 2.0 (Coming Soon)
- [ ] Docker Compose setup
- [ ] Kubernetes Helm charts
- [ ] Advanced ML-based anomaly detection
- [ ] More framework support (Spring Boot, Flask)
- [ ] Real-time log streaming dashboard

### Version 3.0 (Future)
- [ ] Distributed log aggregation
- [ ] Custom dashboard builder
- [ ] Advanced alerting rules engine
- [ ] Multi-tenant support

---

**Made with ❤️ by the community, for the community**

⭐ **Star this repo** if you find it useful!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/universal-log-monitoring-tool.svg)](https://github.com/yourusername/universal-log-monitoring-tool/stargazers)