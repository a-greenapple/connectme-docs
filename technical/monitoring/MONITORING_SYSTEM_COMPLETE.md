# 📊 Monitoring System - Complete Implementation

**Date:** October 14, 2025  
**Status:** ✅ **FULLY DEPLOYED**

---

## 🎯 Overview

Complete monitoring and maintenance system for ConnectMe, including real-time health checks, system statistics, automated schedulers, and log viewing capabilities.

---

## ✅ What Was Implemented

### **Phase 1: Monitoring Dashboard**

1. **Admin Monitoring Submenu**
   - URL: `https://connectme.be.totesoft.com/admin/monitoring/`
   - 4 tabs: Logs, Statistics, Schedulers, Health Check
   - AJAX-based content loading (no iframe auth issues)

2. **Enhanced Log Viewer**
   - Real-time log viewing from multiple sources
   - Sources: Gunicorn, Celery, Nginx
   - Features:
     - Auto-refresh every 10 seconds
     - Filter by log level (INFO, WARNING, ERROR, DEBUG)
     - Adjustable line count (50-1000)
     - Stats dashboard (Total, Errors, Warnings)
     - Color-coded log levels
     - Proper alignment and formatting

3. **System Statistics Dashboard**
   - Real-time metrics
   - Job statistics (today, week, month)
   - Performance metrics (avg processing time, success rate)
   - System health (CPU, memory, disk, DB, Celery, Redis)
   - User statistics

4. **Health Check API**
   - JSON endpoint for programmatic checks
   - Monitors: Database, Celery, Redis, Disk, Memory
   - Overall system health status

### **Phase 2: Celery Beat Schedulers**

1. **Scheduled Maintenance Tasks**
   - 6 automated tasks for system maintenance
   - Database migrations completed
   - Systemd service configured

2. **Scheduler Management UI**
   - View all scheduled tasks
   - See task details (name, schedule, last run, total runs)
   - Visual status indicators
   - Source badges (config vs database)

3. **Celery Beat Service**
   - Systemd service: `celery-beat.service`
   - Auto-starts on boot
   - Logs: `/var/log/celery/celery-beat.log`

---

## 📋 Scheduled Tasks

### Every 5 Minutes
- **`health_check_monitor`**
  - Monitors system health
  - Logs warnings for unhealthy components
  - Can be extended for alerting

### Every 30 Minutes
- **`cleanup_database_connections`**
  - Closes idle database connections
  - Prevents connection pool exhaustion

### Every Hour
- **`cleanup_expired_sessions`**
  - Removes expired Django sessions
  - Keeps session table clean

### Daily at 1 AM
- **`generate_performance_report`**
  - Creates daily performance metrics
  - Tracks job statistics

### Daily at 2 AM
- **`cleanup_old_csv_jobs`**
  - Removes CSV jobs older than 30 days
  - Keeps `COMPLETED`, `FAILED`, `CANCELLED` jobs for 30 days

### Daily at 3 AM
- **`cleanup_celery_task_results`**
  - Removes Celery task results older than 7 days
  - Prevents task result table bloat

---

## 🔍 How to Use

### Access Monitoring Dashboard

1. **Login to Django Admin**
   ```
   URL: https://connectme.be.totesoft.com/admin/
   ```

2. **Navigate to Monitoring**
   ```
   URL: https://connectme.be.totesoft.com/admin/monitoring/
   ```

3. **Use the Tabs**
   - **📋 Logs** - View real-time system logs
   - **📈 Statistics** - See job metrics and performance
   - **⏰ Schedulers** - View scheduled tasks
   - **💚 Health Check** - Check system health

### View Logs via SSH

```bash
# Celery Beat logs
ssh connectme@20.84.160.240
tail -f /var/log/celery/celery-beat.log

# Celery Worker logs
tail -f /var/log/celery/celery.service.log

# Gunicorn logs
tail -f /var/www/connectme-backend/logs/gunicorn-error.log
tail -f /var/www/connectme-backend/logs/gunicorn-access.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Check Service Status

```bash
# Celery Beat
sudo systemctl status celery-beat.service

# Celery Worker
sudo systemctl status celery.service

# Check if services are running
sudo systemctl is-active celery-beat.service
sudo systemctl is-active celery.service
```

### Restart Services

```bash
# Restart Celery Beat
sudo systemctl restart celery-beat.service

# Restart Celery Worker
sudo systemctl restart celery.service

# Reload Gunicorn (manual restart)
kill -HUP $(cat /var/run/gunicorn.pid)
```

---

## 📁 Key Files

### Backend Files
```
connectme-backend/
├── apps/core/
│   ├── scheduled_tasks.py         # Scheduled task definitions
│   ├── monitoring_views.py        # Monitoring dashboard views
│   ├── admin_views.py             # Log viewer views
│   └── simple_log_viewer.py       # Public log viewer
├── config/
│   ├── celery.py                  # Celery & Beat configuration
│   ├── settings.py                # Django settings (INSTALLED_APPS)
│   └── urls.py                    # URL routing
└── templates/admin/monitoring/
    ├── dashboard.html             # Main monitoring dashboard
    ├── stats.html                 # Statistics page
    ├── schedulers.html            # Schedulers management UI
    └── health.html                # Health check page
```

### System Files
```
/etc/systemd/system/
├── celery-beat.service            # Celery Beat systemd service
└── celery.service                 # Celery Worker systemd service

/var/log/celery/
├── celery-beat.log                # Celery Beat logs
└── celery.service.log             # Celery Worker logs

/var/run/celery/
└── celery-beat.pid                # Celery Beat PID file
```

### Deployment Scripts
```
connectme/
├── deploy-monitoring-phase1.sh    # Phase 1 deployment
└── deploy-monitoring-phase2.sh    # Phase 2 deployment
```

---

## 🔧 Configuration

### Celery Beat Schedule (config/celery.py)

```python
app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'cleanup_expired_sessions',
        'schedule': crontab(minute=0),  # Every hour
    },
    'cleanup-old-csv-jobs': {
        'task': 'cleanup_old_csv_jobs',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'cleanup-database-connections': {
        'task': 'cleanup_database_connections',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'health-check-monitor': {
        'task': 'health_check_monitor',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'cleanup-celery-task-results': {
        'task': 'cleanup_celery_task_results',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'generate-performance-report': {
        'task': 'generate_performance_report',
        'schedule': crontab(hour=1, minute=0),  # Daily at 1 AM
    },
}
```

### Installed Apps (config/settings.py)

```python
THIRD_PARTY_APPS = [
    # ...
    'django_celery_beat',     # Celery Beat scheduler
    'django_celery_results',  # Celery results backend
]
```

---

## 🔍 Verification

### Check Deployment

```bash
# 1. Check services are running
ssh connectme@20.84.160.240
sudo systemctl is-active celery-beat.service    # Should output: active
sudo systemctl is-active celery.service         # Should output: active

# 2. Check Celery Beat is scheduling tasks
tail -f /var/log/celery/celery-beat.log

# Expected output:
# [2025-10-14 01:10:00,000: INFO/MainProcess] Scheduler: Sending due task cleanup_expired_sessions
# [2025-10-14 01:15:00,000: INFO/MainProcess] Scheduler: Sending due task health_check_monitor

# 3. Check tasks are being executed
tail -f /var/log/celery/celery.service.log

# Expected output:
# [2025-10-14 01:10:00,123: INFO/ForkPoolWorker-1] Task cleanup_expired_sessions succeeded
# [2025-10-14 01:15:00,456: INFO/ForkPoolWorker-2] Task health_check_monitor succeeded
```

### Test Monitoring UI

1. Go to: `https://connectme.be.totesoft.com/admin/monitoring/`
2. Verify all tabs load correctly
3. Check logs are displayed in the Logs tab
4. Check statistics are shown in the Statistics tab
5. Verify schedulers are listed in the Schedulers tab
6. Confirm health check shows system status

---

## 🐛 Troubleshooting

### Celery Beat Not Starting

```bash
# Check service status
sudo systemctl status celery-beat.service

# View detailed logs
sudo journalctl -u celery-beat.service -n 50

# Check permissions
ls -la /var/run/celery/
ls -la /var/log/celery/

# Ensure directories exist
sudo mkdir -p /var/run/celery
sudo chown connectme:connectme /var/run/celery
sudo mkdir -p /var/log/celery
sudo chown connectme:connectme /var/log/celery
```

### Tasks Not Running

```bash
# Check if Celery Worker is running
sudo systemctl status celery.service

# Check if tasks are registered
cd /var/www/connectme-backend
source venv/bin/activate
python -c "from celery import current_app; print(list(current_app.tasks.keys()))"

# Manually trigger a task to test
cd /var/www/connectme-backend
source venv/bin/activate
python manage.py shell
>>> from apps.core.scheduled_tasks import cleanup_expired_sessions
>>> cleanup_expired_sessions.delay()
```

### Monitoring UI Not Loading

```bash
# Check Gunicorn is running
ps aux | grep gunicorn

# Check for errors in Gunicorn logs
tail -f /var/www/connectme-backend/logs/gunicorn-error.log

# Reload Gunicorn
kill -HUP $(cat /var/run/gunicorn.pid 2>/dev/null || pgrep -f "gunicorn.*config.wsgi")
```

---

## 📊 Database Tables

### Django Celery Beat Tables
- `django_celery_beat_periodictask` - Scheduled tasks
- `django_celery_beat_crontabschedule` - Cron schedules
- `django_celery_beat_intervalschedule` - Interval schedules
- `django_celery_beat_solarschedule` - Solar schedules
- `django_celery_beat_periodictasks` - Scheduler state

### Django Celery Results Tables
- `django_celery_results_taskresult` - Task execution results
- `django_celery_results_chordcounter` - Chord counters
- `django_celery_results_groupresult` - Group results

---

## 🎯 Benefits

1. **Automated Maintenance**
   - No manual cleanup required
   - System stays healthy automatically

2. **Real-time Monitoring**
   - View logs in browser
   - See system health at a glance
   - Track performance metrics

3. **Proactive Alerts**
   - Health checks run every 5 minutes
   - Warnings logged for issues
   - Can be extended for email/Slack alerts

4. **Resource Management**
   - Old data automatically cleaned up
   - Database connections managed
   - Storage space conserved

5. **Visibility**
   - All scheduled tasks visible in UI
   - Easy to see what's running when
   - Track task execution history

---

## 🚀 Future Enhancements

1. **Alerting System**
   - Email alerts for critical issues
   - Slack/Discord integration
   - SMS alerts for downtime

2. **Advanced Metrics**
   - Prometheus/Grafana integration
   - Custom metric dashboards
   - Historical trend analysis

3. **Task Management**
   - Enable/disable tasks from UI
   - Adjust schedules dynamically
   - Manual task triggering via UI

4. **Performance Optimization**
   - Query optimization based on metrics
   - Auto-scaling recommendations
   - Resource usage predictions

---

## ✅ Summary

The monitoring system is **fully deployed and operational**. All scheduled tasks are running, logs are accessible via the web UI, and system health is being monitored automatically.

**Key URLs:**
- Monitoring Dashboard: `https://connectme.be.totesoft.com/admin/monitoring/`
- Django Admin: `https://connectme.be.totesoft.com/admin/`

**Key Commands:**
```bash
# Check status
sudo systemctl status celery-beat.service

# View logs
tail -f /var/log/celery/celery-beat.log

# Restart if needed
sudo systemctl restart celery-beat.service
```

**All systems operational!** 🚀

