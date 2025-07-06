# 🎯 Dashboard Quick Start Guide

## 🚀 Automatic Setup (Recommended)

### **Step 1: Setup Dashboards Automatically**
```bash
# Import all dashboards automatically
python setup_dashboards.py
```

This will create:
- ✅ Prometheus data source
- ✅ Production monitoring dashboard
- ✅ Payment service dashboard  
- ✅ Mobile API dashboard
- ✅ Alert monitoring dashboard

### **Step 2: Access Your Dashboards**
Open Grafana at `http://localhost:3000` (admin/admin)

---

## 📊 Available Dashboards

### **1. 🏭 Production Log Monitoring Dashboard**
**Purpose**: Overall system monitoring
**Key Panels**:
- 🚨 Critical system status
- 📊 Live error rate timeline
- 🏗️ Application health status
- 🌍 Framework distribution pie chart
- 📱 Application log volume trends
- ⚠️ Warning trends analysis
- 🔥 Critical services monitor
- 📈 Log processing performance
- 💾 Log file size monitoring
- 🎯 Alert summary

**Best For**: Operations teams, daily monitoring

---

### **2. 💳 Payment Service Dashboard**
**Purpose**: Business-critical payment monitoring
**Key Panels**:
- 💳 Payment service health status
- 🚨 Payment errors (last 5 minutes)
- 💰 Payment success rate percentage
- ⚡ Payment volume per minute
- 📊 Payment error trends
- 💳 Payment processing timeline
- 🔥 Critical payment issues log

**Best For**: Business stakeholders, payment operations

---

### **3. 📱 Mobile API Dashboard**
**Purpose**: Mobile application API monitoring
**Key Panels**:
- 📱 API health status
- 📊 API request rate
- ⚠️ Error rate percentage
- 🚀 FastAPI performance metrics
- 📈 Mobile API traffic patterns
- 🔍 API error analysis

**Best For**: Mobile development teams, API monitoring

---

### **4. 🚨 Alert & System Health Dashboard**
**Purpose**: System monitoring and alert management
**Key Panels**:
- 🟢 System health overview
- 🚨 Active alerts summary
- 📊 Alert rate timeline
- 🔥 Critical services status
- ⚡ Error rate by service
- 📈 System performance metrics
- 💾 Log file growth rate
- 🎯 Alert frequency heatmap

**Best For**: DevOps teams, incident response

---

## 🔧 Manual Setup (Alternative)

If you prefer manual setup, follow the detailed guide in `dashboards/panel_creation_guide.md`

### **Import Individual Dashboards**:
1. Open Grafana → **+ → Import**
2. Copy content from JSON files in `dashboards/` folder
3. Paste JSON → **Import**
4. Select Prometheus data source

---

## 📈 Key Metrics to Monitor

### **🔴 Critical Alerts (Immediate Action)**
```promql
increase(log_entries_total{level="critical"}[1m]) > 0
```

### **🟡 High Error Rate (Warning)**
```promql
rate(log_errors_total[5m]) * 60 > 5
```

### **🟢 Service Health (Good)**
```promql
rate(log_entries_total{source=~".*-service.log"}[1m]) > 0
```

### **💰 Payment Success Rate**
```promql
(sum(rate(log_entries_total{source="payment-service.log",level="info"}[5m])) / sum(rate(log_entries_total{source="payment-service.log"}[5m]))) * 100
```

---

## 🎨 Customization Tips

### **Add New Applications**:
1. Add logs files: `new-app.log`
2. Update queries: `{source="new-app.log"}`
3. Create specific dashboard panels

### **Modify Alert Thresholds**:
- **Green**: Normal operation
- **Yellow**: Warning (investigate)
- **Red**: Critical (immediate action)

### **Time Ranges**:
- **Real-time**: 5m-15m (operations)
- **Trends**: 1h-6h (analysis)
- **Historical**: 24h+ (reporting)

---

## 🔍 Troubleshooting

### **No Data in Panels?**
1. Check Prometheus is scraping: `http://localhost:9090/targets`
2. Verify log parser is running: `curl http://localhost:8000/metrics`
3. Ensure logs are being generated: `tail -f logs/*.log`

### **Dashboard Import Failed?**
1. Check Grafana is running: `http://localhost:3000`
2. Verify Prometheus data source exists
3. Try manual JSON import

### **Queries Not Working?**
1. Test in Prometheus: `http://localhost:9090/graph`
2. Check metric names: `curl http://localhost:8000/metrics`
3. Verify time ranges and filters

---

## 🎯 Next Steps

1. **Setup Alerts**: Use `setup_alerts.py` for notification channels
2. **Create Custom Panels**: Follow `panel_creation_guide.md`
3. **Monitor Business Metrics**: Focus on payment success rates
4. **Scale Monitoring**: Add more applications and services

Your production-ready monitoring dashboards are now live! 🚀