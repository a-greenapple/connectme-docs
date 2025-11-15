# 📊 ConnectMe Log Viewing Options

**Last Updated**: October 13, 2025

---

## 🔍 Available Logging Options

### 1. **SSH Terminal Access** (Primary Method)

#### Backend Logs (Real-time)
```bash
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240
sudo journalctl -u connectme-backend -f
```

#### Backend Logs (Last 100 lines)
```bash
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -n 100"
```

#### Celery Logs (Real-time)
```bash
ssh connectme@20.84.160.240 "tail -f /var/log/celery/celery.service.log"
```

#### Filter Errors Only
```bash
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend | grep -i error | tail -50"
```

---

### 2. **Health Check Script** (Automated Monitoring)

Run the automated health check script:
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./health-check-monitor.sh
```

**Features**:
- ✅ Checks backend, frontend, database, SSL
- ✅ Measures response times
- ✅ Saves logs to `/tmp/connectme-health-YYYYMMDD.log`
- ✅ Supports email and Slack alerts

**Schedule** (optional):
```bash
# Run every 5 minutes
*/5 * * * * /path/to/health-check-monitor.sh
```

---

### 3. **Admin Panel Logs** (Requires superuser login)

URL: https://connectme.be.totesoft.com/admin/logs/

Login with your superuser credentials to access the admin log viewer.

---

### 4. **Quick Log Commands**

#### Check Recent Errors (Last 10 minutes)
```bash
ssh connectme@20.84.160.240 "sudo journalctl --since '10 minutes ago' | grep -i error"
```

#### Check Service Status
```bash
ssh connectme@20.84.160.240 "systemctl status connectme-backend celery redis --no-pager"
```

#### View Application Logs with Context
```bash
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend --since today"
```

---

## 📝 Common Log Patterns

### Finding Specific Issues

**Authentication Errors**:
```bash
sudo journalctl -u connectme-backend | grep -i "auth\|login\|token"
```

**Database Errors**:
```bash
sudo journalctl -u connectme-backend | grep -i "database\|postgres\|connection"
```

**API Errors**:
```bash
sudo journalctl -u connectme-backend | grep -i "api\|endpoint\|404\|500"
```

**Celery Task Errors**:
```bash
tail -500 /var/log/celery/celery.service.log | grep -i "error\|failed\|exception"
```

---

## 🎯 Quick Troubleshooting

### Problem: Can't see recent logs
**Solution**:
```bash
# Refresh services
ssh connectme@20.84.160.240 "sudo systemctl restart connectme-backend celery"

# Check logs immediately
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -n 50"
```

### Problem: Too many logs to read
**Solution**:
```bash
# Filter by time
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend --since '1 hour ago'"

# Filter by level
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -p err"  # errors only
```

### Problem: Need to save logs for analysis
**Solution**:
```bash
# Download logs to local machine
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend --since today" > backend-logs-$(date +%Y%m%d).log
```

---

## 🔄 Setting Up Web Log Viewer (Future Enhancement)

To set up a web-based log viewer, you can:

1. **Option A: Use Portainer** (if Docker is available)
2. **Option B: Install GoAccess** (real-time log analyzer)
3. **Option C: Set up ELK Stack** (Elasticsearch, Logstash, Kibana)
4. **Option D: Use Papertrail/Loggly** (cloud-based log management)

Contact DevOps team if you need help setting these up.

---

## 📊 Log File Locations

| Service | Log Location |
|---------|--------------|
| Backend (Gunicorn) | `sudo journalctl -u connectme-backend` |
| Celery | `/var/log/celery/celery.service.log` |
| Nginx | `/var/log/nginx/access.log` and `/var/log/nginx/error.log` |
| Redis | `sudo journalctl -u redis` |
| PostgreSQL | `/var/log/postgresql/` |

---

## 🚀 Quick Reference Card

```bash
# View logs live
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -f"

# Last 100 lines
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -n 100"

# Only errors
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -p err"

# Since specific time
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend --since '2025-10-13 10:00:00'"

# Health check
./health-check-monitor.sh

# Service status
ssh connectme@20.84.160.240 "systemctl status connectme-backend"
```

---

**Note**: Web-based log viewer at `/logs/` requires additional permissions configuration. Use SSH terminal access or health check script for immediate log viewing needs.
