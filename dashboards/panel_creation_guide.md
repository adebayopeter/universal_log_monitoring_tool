# 📊 Grafana Panel Creation Guide for Log Monitoring

## Quick Setup: Import Dashboard

### **Option 1: Import Complete Dashboard**
1. Copy the content from `dashboards/production_monitoring_dashboard.json`
2. In Grafana: **+ → Import → Paste JSON → Import**
3. Select your Prometheus data source
4. Done! ✅

### **Option 2: Manual Panel Creation (Step-by-Step)**

---

## 🚨 Panel 1: Critical System Status (Stat Panel)

**Purpose**: Show critical errors and total error count at a glance

### Steps:
1. **Add Panel → Stat**
2. **Query A**: `sum(log_entries_total{level="critical"})`
3. **Query B**: `sum(log_entries_total{level="error"})`
4. **Panel Settings**:
   - Title: "🚨 Critical System Status"
   - Display: List
   - Value: Last
5. **Thresholds**:
   - Green: 0
   - Yellow: 1
   - Red: 5
6. **Field Override**:
   - Display name: A="Critical", B="Errors"

---

## 📊 Panel 2: Live Error Rate (Time Series)

**Purpose**: Real-time error rate monitoring per application/framework

### Steps:
1. **Add Panel → Time series**
2. **Query**: `rate(log_errors_total[1m]) * 60`
3. **Legend**: `{{source}} - {{framework}}`
4. **Panel Settings**:
   - Title: "📊 Live Error Rate (per minute)"
   - Y-axis: "Errors/min"
5. **Visual Options**:
   - Line width: 2
   - Fill opacity: 10%
   - Point size: 4
6. **Thresholds**:
   - Yellow: 3 errors/min
   - Red: 10 errors/min

---

## 🏗️ Panel 3: Application Health Status (Stat Panel)

**Purpose**: Show which applications are actively logging (UP/DOWN)

### Steps:
1. **Add Panel → Stat**
2. **Query**: `count by (source) (rate(log_entries_total[1m]) > 0)`
3. **Panel Settings**:
   - Title: "🏗️ Applications Health Status"
   - Display: List
4. **Value Mappings**:
   - 0 → "DOWN" (Red)
   - 1 → "UP" (Green)
5. **Legend**: `{{source}}`

---

## 🌍 Panel 4: Framework Distribution (Pie Chart)

**Purpose**: Show log distribution across different frameworks

### Steps:
1. **Add Panel → Pie chart**
2. **Query**: `sum by (framework) (log_entries_total)`
3. **Panel Settings**:
   - Title: "🌍 Framework Distribution"
4. **Legend**: `{{framework}}`
5. **Display Options**:
   - Show legend: true
   - Show tooltip: true

---

## 📱 Panel 5: Application Log Volume (Time Series - Stacked)

**Purpose**: Show log volume trends per application over time

### Steps:
1. **Add Panel → Time series**
2. **Query**: `rate(log_entries_total[1m]) * 60`
3. **Legend**: `{{source}}`
4. **Panel Settings**:
   - Title: "📱 Application Log Volume"
5. **Visual Options**:
   - Stack series: Normal
   - Fill opacity: 50%

---

## ⚠️ Panel 6: Warning Trends (Bar Chart)

**Purpose**: Show warning patterns across services

### Steps:
1. **Add Panel → Time series**
2. **Query**: `rate(log_warnings_total[5m]) * 60`
3. **Legend**: `{{source}} - {{framework}}`
4. **Panel Settings**:
   - Title: "⚠️ Warning Trends"
5. **Visual Options**:
   - Draw style: Bars
   - Bar alignment: Center

---

## 🔥 Panel 7: Critical Services Monitor

**Purpose**: Focus on payment and user services (business critical)

### Steps:
1. **Add Panel → Time series**
2. **Query**: `rate(log_entries_total{source=~"payment-service.log|user-service.log",level=~"error|critical"}[1m]) * 60`
3. **Legend**: `{{source}} - {{level}}`
4. **Panel Settings**:
   - Title: "🔥 Critical Services Monitor"
5. **Thresholds**:
   - Green: 0
   - Yellow: 1
   - Red: 3

---

## 📈 Panel 8: Log Processing Performance

**Purpose**: Monitor the log parser's performance

### Steps:
1. **Add Panel → Time series**
2. **Query A**: `histogram_quantile(0.95, rate(log_processing_seconds_bucket[5m]))`
3. **Query B**: `histogram_quantile(0.50, rate(log_processing_seconds_bucket[5m]))`
4. **Panel Settings**:
   - Title: "📈 Log Processing Performance"
   - Y-axis unit: seconds
5. **Legend**: A="95th percentile", B="50th percentile"

---

## 💾 Panel 9: Log File Sizes

**Purpose**: Monitor disk usage and log file growth

### Steps:
1. **Add Panel → Stat**
2. **Query**: `log_file_size_bytes`
3. **Panel Settings**:
   - Title: "💾 Log File Sizes"
   - Unit: bytes
4. **Thresholds**:
   - Green: < 1MB
   - Yellow: 1MB - 10MB  
   - Red: > 10MB
5. **Legend**: `{{filename}}`

---

## 🎯 Panel 10: Alert Summary

**Purpose**: Overview of alerting activity

### Steps:
1. **Add Panel → Stat**
2. **Query A**: `sum(log_alerts_sent_total)`
3. **Query B**: `sum(rate(log_alerts_sent_total[1h]) * 3600)`
4. **Panel Settings**:
   - Title: "🎯 Alert Summary"
   - Display: List
5. **Legend**: A="Total Alerts", B="Alerts/Hour"

---

# 🔧 Advanced Panel Configurations

## Variable Templates

Add these variables for dynamic filtering:

### Application Filter:
- **Name**: `application`
- **Type**: Query
- **Query**: `label_values(log_entries_total, source)`
- **Multi-value**: Yes
- **Include All**: Yes

### Framework Filter:
- **Name**: `framework` 
- **Type**: Query
- **Query**: `label_values(log_entries_total, framework)`
- **Multi-value**: Yes
- **Include All**: Yes

## Time Range Templates

- **Quick Ranges**: 5m, 15m, 30m, 1h, 3h, 6h, 12h, 24h
- **Refresh**: 5s, 10s, 30s, 1m, 5m

## Panel Links

Add links between panels:
- Click on application → filter other panels
- Click on error → jump to detailed logs
- Click on framework → show framework-specific dashboard

---

# 📊 Custom Queries for Specific Use Cases

## Business Metrics:
```promql
# Payment success rate
(rate(log_entries_total{source="payment-service.log",level="info"}[5m]) / rate(log_entries_total{source="payment-service.log"}[5m])) * 100

# User login rate
rate(log_entries_total{source="user-service.log",level="info"}[5m]) * 60

# API response time trends
histogram_quantile(0.95, rate(log_processing_seconds_bucket{source=~".*-api.log"}[5m]))
```

## Performance Metrics:
```promql
# Top error-prone applications
topk(5, sum by (source) (rate(log_errors_total[1h])))

# Framework error comparison
sum by (framework) (rate(log_errors_total[1h])) / sum by (framework) (rate(log_entries_total[1h])) * 100

# Fastest growing log files
topk(3, increase(log_file_size_bytes[1h]))
```

## Alerting Queries:
```promql
# Service health check
up{job="log-parser"}

# Memory usage from logs
increase(log_entries_total{level="warning"}[5m]) > 10

# Critical error spike
increase(log_entries_total{level="critical"}[1m]) > 0
```

This guide will help you create a comprehensive monitoring dashboard that scales with your production environment! 🎯