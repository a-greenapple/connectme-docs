# 🚀 ConnectMe Deployment Scripts

Automated deployment scripts for ConnectMe Healthcare Platform on Debian servers.

---

## 📋 Overview

| Script | Purpose | Domain | Port |
|--------|---------|--------|------|
| `01-backend-setup.sh` | Backend API + Database | `connectme.be.totesoft.com` | 443 (HTTPS only) |
| `02-frontend-setup.sh` | Frontend Next.js App | `connectme.apps.totesoft.com` | 443 (HTTPS only) |

---

## 🎯 Quick Start

### Prerequisites
- ✅ Debian 11 or 12 server (2 separate servers or 1 server for both)
- ✅ SSH root/sudo access
- ✅ DNS A records configured:
  - `connectme.be.totesoft.com` → Backend server IP
  - `connectme.apps.totesoft.com` → Frontend server IP
- ✅ Ports 22, 80, 443 accessible

### Step 1: Upload Scripts to Server

```bash
# From your local machine
scp deploy/01-backend-setup.sh user@backend-server:/tmp/
scp deploy/02-frontend-setup.sh user@frontend-server:/tmp/
```

### Step 2: Deploy Backend

```bash
# SSH into backend server
ssh user@backend-server

# Run backend setup
sudo bash /tmp/01-backend-setup.sh

# Upload backend code
rsync -avz --exclude='venv' --exclude='*.pyc' \
    backend/ user@backend-server:/var/www/connectme-backend/

# SSH back in and configure
ssh user@backend-server
cd /var/www/connectme-backend

# Edit environment
sudo nano .env
# Update: UHC_API_KEY, KEYCLOAK_CLIENT_SECRET, etc.

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Start service
sudo systemctl start connectme-backend
sudo systemctl enable connectme-backend
sudo systemctl status connectme-backend
```

### Step 3: Deploy Frontend

```bash
# SSH into frontend server
ssh user@frontend-server

# Run frontend setup
sudo bash /tmp/02-frontend-setup.sh

# Upload frontend code
rsync -avz --exclude='node_modules' --exclude='.next' \
    frontend/ user@frontend-server:/var/www/connectme-frontend/

# SSH back in and build
ssh user@frontend-server
cd /var/www/connectme-frontend

# Install dependencies
npm ci

# Build application
npm run build

# Start service
sudo systemctl start connectme-frontend
sudo systemctl enable connectme-frontend
sudo systemctl status connectme-frontend
```

---

## 🔧 What Each Script Does

### `01-backend-setup.sh`

**Infrastructure:**
- ✅ PostgreSQL 15+ with database `connectme_db`
- ✅ Redis for caching and Celery
- ✅ Python 3.11 with virtual environment
- ✅ Nginx reverse proxy (HTTPS only)
- ✅ Let's Encrypt SSL certificates
- ✅ UFW firewall configuration

**Services Created:**
- `connectme-backend.service` - Gunicorn workers
- `connectme-celery.service` - Background tasks

**Security:**
- HTTPS only (HTTP redirects to HTTPS)
- Security headers (HSTS, XSS protection)
- Rate limiting (10 req/s burst 20)
- Firewall: Only 22, 80, 443 open

### `02-frontend-setup.sh`

**Infrastructure:**
- ✅ Node.js 20 LTS
- ✅ PM2 process manager (cluster mode)
- ✅ Nginx reverse proxy (HTTPS only)
- ✅ Let's Encrypt SSL certificates
- ✅ UFW firewall configuration

**Services Created:**
- `connectme-frontend.service` - PM2 managed Next.js

**Features:**
- Static asset caching (1 year)
- Image optimization caching (7 days)
- Gzip compression
- HTTP/2 support

---

## 📂 Directory Structure After Deployment

### Backend Server
```
/var/www/connectme-backend/
├── manage.py
├── config/
├── apps/
├── venv/
├── staticfiles/
├── media/
├── .env (credentials)
└── logs/

/var/log/connectme/
├── backend-access.log
├── backend-error.log
└── celery-worker1.log

/etc/systemd/system/
├── connectme-backend.service
└── connectme-celery.service
```

### Frontend Server
```
/var/www/connectme-frontend/
├── package.json
├── next.config.js
├── src/
├── .next/ (build output)
├── node_modules/
├── .env.production
└── ecosystem.config.js (PM2)

/var/log/connectme/
├── frontend-out.log
└── frontend-error.log

/etc/systemd/system/
└── connectme-frontend.service
```

---

## 🔑 Environment Variables

### Backend (`.env`)
```env
SECRET_KEY=auto-generated
DEBUG=False
ALLOWED_HOSTS=connectme.be.totesoft.com

DATABASE_PASSWORD=auto-generated
KEYCLOAK_CLIENT_SECRET=CHANGE_THIS
UHC_API_KEY=CHANGE_THIS
UHC_CLIENT_ID=CHANGE_THIS
UHC_CLIENT_SECRET=CHANGE_THIS
```

### Frontend (`.env.production`)
```env
NEXT_PUBLIC_API_URL=https://connectme.be.totesoft.com
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

---

## 🧪 Testing Deployment

### Test Backend
```bash
# Health check
curl https://connectme.be.totesoft.com/health/

# Admin panel
curl https://connectme.be.totesoft.com/admin/

# API endpoint
curl https://connectme.be.totesoft.com/api/v1/

# Check service
sudo systemctl status connectme-backend

# View logs
sudo journalctl -u connectme-backend -f
tail -f /var/log/connectme/backend-error.log
```

### Test Frontend
```bash
# Homepage
curl https://connectme.apps.totesoft.com

# Check service
sudo systemctl status connectme-frontend

# View logs
sudo journalctl -u connectme-frontend -f
pm2 logs connectme-frontend

# PM2 monitoring
pm2 monit
```

### Test UHC API Connection
```bash
# From backend server
cd /var/www/connectme-backend
source venv/bin/activate
python manage.py shell

# In Python shell:
>>> import requests
>>> response = requests.get('https://apimarketplace.uhc.com')
>>> print(response.status_code)  # Should work (not DNS error)
>>> exit()
```

---

## 🔄 Service Management

### Backend Commands
```bash
# Start/Stop/Restart
sudo systemctl start connectme-backend
sudo systemctl stop connectme-backend
sudo systemctl restart connectme-backend

# Enable/Disable autostart
sudo systemctl enable connectme-backend
sudo systemctl disable connectme-backend

# View status
sudo systemctl status connectme-backend

# View logs (live)
sudo journalctl -u connectme-backend -f

# Reload Nginx
sudo nginx -t && sudo systemctl reload nginx
```

### Frontend Commands
```bash
# Start/Stop/Restart
sudo systemctl start connectme-frontend
sudo systemctl stop connectme-frontend
sudo systemctl restart connectme-frontend

# PM2 commands (as deployment user)
pm2 status
pm2 logs connectme-frontend
pm2 restart connectme-frontend
pm2 reload connectme-frontend  # Zero-downtime restart
pm2 monit

# View logs
tail -f /var/log/connectme/frontend-out.log
```

---

## 🔐 SSL Certificate Management

### Auto-Renewal
Certbot auto-renewal is configured via systemd timer:
```bash
# Check renewal timer
sudo systemctl status certbot.timer

# Test renewal (dry run)
sudo certbot renew --dry-run

# Force renewal
sudo certbot renew --force-renewal
```

### Manual Certificate Commands
```bash
# Check certificates
sudo certbot certificates

# Renew specific domain
sudo certbot renew --cert-name connectme.be.totesoft.com

# Revoke certificate
sudo certbot revoke --cert-name connectme.be.totesoft.com
```

---

## 📊 Monitoring & Logs

### Backend Monitoring
```bash
# System status
/usr/local/bin/monitor-connectme-backend  # (if you add this script)

# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='connectme_db';"

# Redis status
redis-cli ping
redis-cli info stats

# Nginx access logs
tail -f /var/log/nginx/connectme-backend-access.log

# Error logs
tail -f /var/log/connectme/backend-error.log
```

### Frontend Monitoring
```bash
# PM2 dashboard
pm2 monit

# PM2 status
pm2 status

# Memory usage
pm2 list | grep connectme-frontend

# Nginx logs
tail -f /var/log/nginx/connectme-frontend-access.log
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check logs
sudo journalctl -u connectme-backend -n 100

# Check database connection
cd /var/www/connectme-backend
source venv/bin/activate
python manage.py dbshell

# Check environment
sudo cat /var/www/connectme-backend/.env

# Test Gunicorn manually
cd /var/www/connectme-backend
source venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

### Frontend Won't Start
```bash
# Check PM2 logs
pm2 logs connectme-frontend --lines 50

# Restart PM2
pm2 restart connectme-frontend

# Rebuild
cd /var/www/connectme-frontend
npm run build

# Test manually
npm run start
```

### SSL Certificate Issues
```bash
# Check certificate
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run

# Check Nginx config
sudo nginx -t

# Restart services
sudo systemctl restart nginx
```

### Database Connection Errors
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l | grep connectme_db

# Reset password
sudo -u postgres psql
postgres=# ALTER USER connectme_user WITH PASSWORD 'new_password';
postgres=# \q

# Update .env file
sudo nano /var/www/connectme-backend/.env
```

---

## 🔄 Updates & Deployment

### Backend Update
```bash
# Upload new code
rsync -avz --exclude='venv' backend/ user@server:/var/www/connectme-backend/

# SSH in
ssh user@server
cd /var/www/connectme-backend

# Backup database first!
sudo -u postgres pg_dump connectme_db > backup_$(date +%Y%m%d).sql

# Run migrations
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart connectme-backend
```

### Frontend Update
```bash
# Upload new code
rsync -avz --exclude='node_modules' --exclude='.next' \
    frontend/ user@server:/var/www/connectme-frontend/

# SSH in
ssh user@server
cd /var/www/connectme-frontend

# Rebuild
npm ci
npm run build

# Zero-downtime reload
pm2 reload connectme-frontend
```

---

## 🆘 Emergency Procedures

### Rollback Backend
```bash
# Restore database backup
sudo -u postgres psql connectme_db < backup_20241006.sql

# Revert code (if using git)
cd /var/www/connectme-backend
git checkout <previous-commit>

# Restart
sudo systemctl restart connectme-backend
```

### Rollback Frontend
```bash
# Revert code
cd /var/www/connectme-frontend
git checkout <previous-commit>

# Rebuild
npm run build

# Reload
pm2 reload connectme-frontend
```

---

## 📞 Support

### Useful Commands Cheat Sheet
```bash
# Status check
sudo systemctl status connectme-backend connectme-frontend

# View all logs
sudo journalctl -xe

# Disk space
df -h

# Memory
free -h

# Nginx test
sudo nginx -t

# Database password
sudo cat /root/.connectme_db_password
```

---

## 🎓 Additional Resources

- **Backend Domain**: https://connectme.be.totesoft.com
- **Frontend Domain**: https://connectme.apps.totesoft.com
- **Keycloak**: https://auth.totesoft.com
- **Deployment Guides**: See `DEBIAN_DEPLOYMENT_GUIDE.md` and `QUICK_DEPLOY_GUIDE.md`

---

**Version**: 1.0  
**Last Updated**: October 7, 2025  
**Tested On**: Debian 11 (Bullseye), Debian 12 (Bookworm)

