# 🚀 Quick Reference Card - ConnectMe Healthcare

## 🔐 Authentication & Session Management

### Test Authentication Redirect (PRIORITY #1)
```bash
1. Firefox → https://connectme.apps.totesoft.com/bulk-upload
2. Should redirect to: /login?redirect=/bulk-upload
3. After login → Should go to: /bulk-upload ✅
   (NOT /dashboard or /claims ❌)
```

### Session Timeout Settings
```bash
# Default
SESSION_TIMEOUT_MINUTES=60  # 1 hour

# SSH to server
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

# Edit configuration
cd /var/www/connectme-backend
nano .env

# Restart
sudo systemctl restart connectme-backend
```

### Token Expiry Behavior
- Checks every 60 seconds
- Auto-refresh if possible
- Alert + logout if refresh fails
- Console logs: `[AUTH] Token expired...`

---

## 🖥️ Server Access

### SSH Connection
```bash
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240
```

### Service Management
```bash
# Frontend
pm2 status
pm2 restart connectme-frontend
pm2 logs connectme-frontend

# Backend
sudo systemctl status connectme-backend
sudo systemctl restart connectme-backend
sudo journalctl -fu connectme-backend

# Kill stuck processes
sudo pkill -f gunicorn
```

---

## 📦 Deployment

### Frontend
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-frontend

# Build locally
npm run build

# Deploy
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  src/app/login/page.tsx \
  connectme@20.84.160.240:/var/www/connectme-frontend/src/app/login/

# Rebuild on server
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 \
  "cd /var/www/connectme-frontend && npm run build && pm2 restart connectme-frontend"
```

### Backend
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-backend

# Deploy
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  config/settings.py \
  connectme@20.84.160.240:/var/www/connectme-backend/config/

# Restart
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 \
  "sudo systemctl restart connectme-backend"
```

---

## 🐛 Debugging

### Browser Console
```javascript
// Good signs
[DEBUG] Fetching jobs with token: mock_access_token_...
[LOGIN] Already authenticated, redirecting to: /bulk-upload
[DEBUG] Response status: 200 OK

// Problem signs
[DEBUG] Fetching jobs with token: NO TOKEN
403 Forbidden
Invalid token: Not enough segments
```

### Backend Logs
```bash
# Real-time logs
ssh connectme@20.84.160.240
sudo journalctl -fu connectme-backend

# Last 50 lines
sudo journalctl -xeu connectme-backend -n 50 --no-pager
```

### Check Services
```bash
# Frontend
pm2 status
pm2 logs connectme-frontend --lines 50

# Backend  
sudo systemctl status connectme-backend
sudo ps aux | grep gunicorn

# Check port
sudo netstat -tulpn | grep 8000
```

---

## 🔧 Common Issues & Fixes

### Issue: Redirect Loop
```bash
# Clear browser cache + localStorage
# Hard refresh (Ctrl+Shift+R)
# Try incognito window
```

### Issue: "load failed" in Firefox
```bash
# Check console: [DEBUG] Fetching jobs with token: NO TOKEN
# → Need to log in first
```

### Issue: Backend won't start
```bash
ssh connectme@20.84.160.240
sudo pkill -f gunicorn
sleep 3
sudo systemctl start connectme-backend
sudo systemctl status connectme-backend
```

### Issue: Port already in use
```bash
# Find process
sudo lsof -i :8000

# Kill it
sudo kill -9 <PID>

# Or kill all Gunicorn
sudo pkill -f gunicorn
```

---

## 🌐 URLs

### Production
- **Frontend**: https://connectme.apps.totesoft.com
- **Backend API**: https://connectme.be.totesoft.com/api/v1/
- **Admin**: https://connectme.be.totesoft.com/admin/
- **Logs**: https://connectme.be.totesoft.com/admin/logs/

### API Endpoints
```bash
# Health check
curl https://connectme.be.totesoft.com/api/v1/health/

# Claims search
curl https://connectme.be.totesoft.com/api/v1/claims/search/

# CSV jobs
curl https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/
```

---

## 📊 System Info

### Server
- **IP**: 20.84.160.240
- **OS**: Debian 6.1
- **User**: connectme
- **SSH Key**: ~/Documents/Access/cursor/id_rsa_Debian

### Paths
- **Frontend**: /var/www/connectme-frontend
- **Backend**: /var/www/connectme-backend
- **Media**: /var/www/connectme-backend/media
- **Logs**: /var/log/ (systemd journal)

### Services
- **Frontend**: PM2 (connectme-frontend) on port 3000
- **Backend**: Gunicorn on port 8000 (internal)
- **Nginx**: Reverse proxy on port 443
- **PostgreSQL**: Database on port 5432
- **Redis**: Celery broker on port 6379
- **Celery**: Background worker (CSV processing)

---

## 📝 Environment Variables

### Session Timeout
```bash
SESSION_TIMEOUT_MINUTES=60              # Django session (default)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60    # JWT access token
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=1440  # JWT refresh (24 hours)
```

### Keycloak
```bash
KEYCLOAK_SERVER_URL=https://auth.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-frontend
KEYCLOAK_CLIENT_SECRET=<secret>
```

### Database
```bash
DB_NAME=connectme_db
DB_USER=connectme
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=5432
```

---

## 🧪 Testing Checklist

- [ ] Clear browser cache + localStorage
- [ ] Go to /bulk-upload (not logged in)
- [ ] Verify redirect to /login?redirect=/bulk-upload
- [ ] Log in (mock or Keycloak)
- [ ] Verify redirect back to /bulk-upload ✅
- [ ] Check console for [DEBUG] messages
- [ ] Upload a CSV file
- [ ] Verify bulk upload works
- [ ] Wait 1 minute (token expiry check)
- [ ] Verify no errors in console

---

## 📚 Documentation

1. **AUTH_AND_SESSION_FIXES.md** - Technical details
2. **FIREFOX_ISSUE_RESOLVED.md** - Firefox debugging
3. **DEPLOYMENT_SUCCESS.md** - Deployment summary
4. **QUICK_REFERENCE.md** - This file (quick reference)

---

## 💡 Tips

### Speed up testing
```bash
# Reduce session timeout for testing
SESSION_TIMEOUT_MINUTES=5

# Check logs in real-time
sudo journalctl -fu connectme-backend | grep -E "ERROR|WARNING|INFO"

# Monitor PM2
pm2 monit
```

### Debug authentication
```javascript
// In browser console
localStorage.getItem('access_token')  // Check if token exists
localStorage.getItem('user')          // Check user info
```

### Clear everything
```bash
# Browser: F12 → Application → Clear storage
# OR
localStorage.clear()
sessionStorage.clear()
# Then hard refresh (Ctrl+Shift+R)
```

---

**Last Updated**: Sunday, October 12, 2025  
**Status**: Ready for User Testing
