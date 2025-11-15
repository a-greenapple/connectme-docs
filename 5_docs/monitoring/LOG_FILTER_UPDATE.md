# Log Viewer Enhancement - Source Filtering

## ✅ What Was Added

### New Feature: Source Filter
The monitoring logs now have a **Source Filter** dropdown to separate logs by service type.

### Filter Options:
- **📂 All Sources** - Shows all logs (Django, Celery, Nginx)
- **🐍 Django/Gunicorn** - Shows only Django/Gunicorn logs
- **⚙️ Celery Workers** - Shows only Celery worker logs
- **🌐 Nginx** - Shows only Nginx access/error logs

---

## 🎯 Why This Helps

### Before:
- All logs mixed together (Django + Celery + Nginx + System)
- Hard to focus on specific service issues
- SSL errors from bots cluttering the view

### After:
- **Separate logs by service**
- Filter out noise (e.g., ignore Nginx SSL bot errors)
- Focus on relevant logs for debugging

---

## 🔧 How to Use

1. Go to: `https://connectme.be.totesoft.com/admin/monitoring/`
2. Click the **Logs** tab
3. Use the **Source Filter** dropdown:
   ```
   📂 All Sources  ← Default (shows everything)
   🐍 Django/Gunicorn  ← Backend application logs
   ⚙️ Celery Workers  ← Background task logs
   🌐 Nginx  ← Web server logs (includes SSL errors)
   ```

---

## 📋 Examples

### Debugging Bulk Upload Issues:
1. Select **⚙️ Celery Workers**
2. Shows only task processing logs
3. See CSV processing, claim queries, errors

### Checking Backend API:
1. Select **🐍 Django/Gunicorn**
2. Shows API requests, responses, errors
3. No Celery or Nginx noise

### Investigating SSL Errors (like the one you saw):
1. Select **🌐 Nginx**
2. Shows web server logs
3. SSL errors from bots are visible here
   - These are **normal** - just external scanners
   - Not a problem with your application

---

## 🚫 About Those SSL Errors

```
SSL_do_handshake() failed (SSL: error:0A00006C:SSL routines::bad key share)
client: 212.102.40.218 (Turkey)
```

**This is NOT a problem!**
- External bots/scanners trying to connect
- Using incompatible SSL configurations
- Happens to all public web servers
- Your application is working fine

**To ignore these:**
- Select **🐍 Django/Gunicorn** or **⚙️ Celery Workers**
- This hides Nginx logs (where SSL errors appear)

---

## ✨ Combined Filtering

You can now combine multiple filters:

**Example 1: Celery Errors Only**
- Source: **⚙️ Celery Workers**
- Level: **ERROR**
- Lines: **500**

**Example 2: Recent Django Logs**
- Source: **🐍 Django/Gunicorn**
- Level: **All Levels**
- Lines: **200**

**Example 3: All Critical Issues**
- Source: **📂 All Sources**
- Level: **ERROR**
- Lines: **1000**

---

## 📊 What Each Source Contains

### 🐍 Django/Gunicorn
- API requests (claim search, bulk upload)
- Authentication/login
- Database queries
- View errors
- Application logic

### ⚙️ Celery Workers
- CSV file processing
- Background tasks
- Claim queries to UHC API
- Task success/failure
- Worker health

### 🌐 Nginx
- HTTP requests
- SSL handshakes
- Proxy errors
- Access logs
- Bot/scanner attempts (SSL errors)

---

## 🎉 Result

**Cleaner, more focused debugging!**
- No more mixed logs
- Easy to find relevant errors
- Faster troubleshooting

---

*Updated: October 15, 2025*
