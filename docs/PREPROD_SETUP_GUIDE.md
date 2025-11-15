# Pre-Production Environment Setup Guide

## 📋 Overview

This guide walks you through setting up a complete pre-production environment for ConnectMe.

### Environment Details

**Production:**
- Server: 20.84.160.240
- Frontend: https://connectme.apps.totesoft.com
- Backend: https://connectme.be.totesoft.com
- Keycloak: https://auth.totesoft.com (realm: `connectme`)

**Pre-Production:**
- Server: 169.59.163.43
- Frontend: https://pre-prod.connectme.apps.totessoft.com
- Backend: https://pre-prod.connectme.be.totessoft.com
- Keycloak: https://auth.totessoft.com (realm: `connectme-preprod`)

---

## 🚀 Quick Start

Run these scripts in order:

```bash
cd scripts/preprod

# 1. Initial server setup (packages, database, directories)
./setup-preprod-server.sh

# 2. Configure environment variables
./configure-preprod-env.sh

# 3. Setup Nginx and SSL
./setup-preprod-nginx.sh

# 4. Copy production database and run migrations
./setup-preprod-database.sh

# 5. Start all services
./start-preprod-services.sh
```

---

## 📝 Detailed Setup Steps

### Prerequisites

1. **SSH Access**: Ensure you have SSH access to 169.59.163.43
   ```bash
   ssh connectme@169.59.163.43
   ```

2. **DNS Configuration**: Before running `setup-preprod-nginx.sh`, configure these A records:
   ```
   pre-prod.connectme.apps.totessoft.com    A    169.59.163.43
   pre-prod.connectme.be.totessoft.com      A    169.59.163.43
   ```

3. **Keycloak Setup**: Create a new realm and clients in Keycloak (see below)

---

### Step 1: Initial Server Setup

```bash
./setup-preprod-server.sh
```

This script will:
- ✅ Install system dependencies (Python, Node.js, PostgreSQL, Redis, Nginx)
- ✅ Create PostgreSQL database `connectme_preprod_db`
- ✅ Create directory structure in `/var/www/`
- ✅ Clone GitHub repositories
- ✅ Install Python and Node.js dependencies

**Duration**: ~10-15 minutes

---

### Step 2: Configure Environment Variables

```bash
./configure-preprod-env.sh
```

This script will:
- ✅ Generate Django secret key
- ✅ Create backend `.env` file
- ✅ Create frontend `.env.production` file
- ✅ Configure database connection
- ✅ Set Keycloak URLs

**Post-Script Actions**:
After running this script, you need to manually update:

1. **Keycloak Client Secret** (after creating Keycloak client):
   ```bash
   ssh connectme@169.59.163.43
   nano /var/www/connectme-preprod-backend/.env
   # Update: KEYCLOAK_CLIENT_SECRET=<your-secret-from-keycloak>
   ```

2. **UHC API Credentials** (if different from production):
   ```bash
   # Update: UHC_API_KEY, UHC_CLIENT_ID, UHC_CLIENT_SECRET
   ```

---

### Step 3: Setup Keycloak

#### 3.1 Create Pre-Prod Realm

1. Go to https://auth.totessoft.com (or wherever your Keycloak is hosted)
2. Login to admin console
3. Click **Create Realm**
   - Realm name: `connectme-preprod`
   - Enabled: Yes
   - Click **Create**

#### 3.2 Create Backend Client

1. In realm `connectme-preprod`, go to **Clients** → **Create client**
2. **General Settings**:
   - Client ID: `connectme-preprod-backend`
   - Client authentication: ON
   - Click **Next**
3. **Capability config**:
   - Client authentication: ON
   - Authorization: OFF
   - Authentication flow: Enable **Direct access grants**
   - Click **Next**
4. **Login settings**:
   - Click **Save**
5. Go to **Credentials** tab
   - Copy the **Client secret**
   - Update in backend `.env` file

#### 3.3 Create Frontend Client

1. Go to **Clients** → **Create client**
2. **General Settings**:
   - Client ID: `connectme-preprod-frontend`
   - Client authentication: OFF (public client)
   - Click **Next**
3. **Capability config**:
   - Standard flow: ON
   - Direct access grants: ON
   - Click **Next**
4. **Login settings**:
   - Valid redirect URIs:
     ```
     https://pre-prod.connectme.apps.totessoft.com/*
     http://localhost:3000/*
     ```
   - Valid post logout redirect URIs: (same as above)
   - Web origins: `+` (all valid redirect URIs)
   - Click **Save**

#### 3.4 Create Users

**Option A: Copy users from production realm**
- Use Keycloak export/import feature

**Option B: Create test users manually**
1. Go to **Users** → **Add user**
2. Create user: `admin@connectme.com`
3. Go to **Credentials** tab → **Set password**
4. Assign roles as needed

---

### Step 4: Setup Nginx and SSL

```bash
./setup-preprod-nginx.sh
```

**Prerequisites**: DNS must be configured and propagated!

This script will:
- ✅ Create Nginx configuration for backend (port 8001)
- ✅ Create Nginx configuration for frontend (port 3001)
- ✅ Obtain SSL certificates from Let's Encrypt
- ✅ Configure HTTPS

**Duration**: ~5 minutes

---

### Step 5: Setup Database

```bash
./setup-preprod-database.sh
```

This script will:
- ✅ Dump production database
- ✅ Copy to pre-prod server
- ✅ Restore to `connectme_preprod_db`
- ✅ Run Django migrations
- ✅ Collect static files

**Duration**: ~5-10 minutes (depends on database size)

**Note**: This copies ALL production data. To start with a fresh database instead:
```bash
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

---

### Step 6: Start Services

```bash
./start-preprod-services.sh
```

This script will:
- ✅ Create systemd service for backend (Gunicorn on port 8001)
- ✅ Create systemd service for Celery worker
- ✅ Build frontend production bundle
- ✅ Create PM2 configuration for frontend (port 3001)
- ✅ Start all services

**Duration**: ~3-5 minutes

---

## ✅ Verification

After setup, verify everything works:

### 1. Check Services

```bash
ssh connectme@169.59.163.43

# Backend status
sudo systemctl status connectme-preprod-backend

# Celery status
sudo systemctl status connectme-preprod-celery

# Frontend status
pm2 list

# Check if services are listening on correct ports
sudo ss -tulpn | grep -E ':(8001|3001)'
```

### 2. Test URLs

- Frontend: https://pre-prod.connectme.apps.totessoft.com
- Backend API: https://pre-prod.connectme.be.totessoft.com/api/v1/
- Backend Health: https://pre-prod.connectme.be.totessoft.com/health/

### 3. Test Login

1. Go to https://pre-prod.connectme.apps.totessoft.com/login
2. Login with your Keycloak credentials
3. Verify you can access the dashboard

---

## 🔄 Updating Pre-Prod

### Update from GitHub

```bash
ssh connectme@169.59.163.43

# Update backend
cd /var/www/connectme-preprod-backend
git pull origin main
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart connectme-preprod-backend
sudo systemctl restart connectme-preprod-celery

# Update frontend
cd /var/www/connectme-preprod-frontend
git pull origin main
npm install
npm run build
pm2 restart connectme-preprod-frontend
```

### Sync Database from Production

```bash
# From your local machine
cd scripts/preprod
./setup-preprod-database.sh
```

---

## 🐛 Troubleshooting

### Issue: Services won't start

**Check logs**:
```bash
# Backend logs
sudo journalctl -u connectme-preprod-backend -n 50

# Celery logs
sudo journalctl -u connectme-preprod-celery -n 50
tail -f /var/www/connectme-preprod-backend/logs/celery.log

# Frontend logs
pm2 logs connectme-preprod-frontend

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Issue: SSL certificate fails

**Check DNS**:
```bash
# Verify DNS propagation
nslookup pre-prod.connectme.apps.totessoft.com
nslookup pre-prod.connectme.be.totessoft.com

# Should return: 169.59.163.43
```

**Manual SSL setup**:
```bash
ssh connectme@169.59.163.43
sudo certbot --nginx -d pre-prod.connectme.be.totessoft.com
sudo certbot --nginx -d pre-prod.connectme.apps.totessoft.com
```

### Issue: Frontend shows "API connection error"

**Check backend is running**:
```bash
curl https://pre-prod.connectme.be.totessoft.com/api/v1/
```

**Check CORS configuration**:
```bash
ssh connectme@169.59.163.43
nano /var/www/connectme-preprod-backend/.env
# Verify: CORS_ALLOWED_ORIGINS includes pre-prod frontend URL
```

### Issue: Keycloak authentication fails

**Verify Keycloak client configuration**:
1. Check client ID matches in `.env` files
2. Verify redirect URIs are correct
3. Ensure Direct access grants is enabled
4. Check client secret is correct

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Pre-Prod Server                       │
│                   169.59.163.43                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │   Nginx (Port 443)   │    │   Nginx (Port 443)   │  │
│  │   SSL Termination    │    │   SSL Termination    │  │
│  │ pre-prod.be.*.com    │    │ pre-prod.apps.*.com  │  │
│  └──────┬───────────────┘    └───────┬──────────────┘  │
│         │                             │                 │
│         ▼                             ▼                 │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │  Gunicorn:8001       │    │  Next.js:3001        │  │
│  │  Django Backend      │    │  React Frontend      │  │
│  └──────┬───────────────┘    └───────┬──────────────┘  │
│         │                             │                 │
│         ▼                             │                 │
│  ┌──────────────────────┐             │                 │
│  │  PostgreSQL:5432     │◄────────────┘                 │
│  │  connectme_preprod_db│                               │
│  └──────────────────────┘                               │
│                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │  Celery Worker       │◄───│  Redis:6379          │  │
│  │  (Task Queue)        │    │  (Message Broker)    │  │
│  └──────────────────────┘    └──────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
                         │
                         │ JWT Auth
                         ▼
            ┌─────────────────────────┐
            │  Keycloak               │
            │  auth.totessoft.com     │
            │  Realm: connectme-preprod│
            └─────────────────────────┘
```

---

## 📋 Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| Nginx (HTTPS) | 443 | SSL termination |
| Nginx (HTTP) | 80 | Redirect to HTTPS |
| Gunicorn | 8001 | Django backend |
| Next.js | 3001 | React frontend |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Celery message broker |

---

## 🔐 Security Notes

1. **Firewall**: Ensure only ports 80 and 443 are open to the internet
2. **Database**: PostgreSQL should only accept local connections
3. **Redis**: Should only bind to localhost
4. **Environment Variables**: Never commit `.env` files to Git
5. **SSL**: Certificates auto-renew via certbot cron job

---

## 🆘 Support

For issues or questions:
1. Check logs (see Troubleshooting section)
2. Verify service status
3. Check DNS configuration
4. Review Keycloak settings
5. Compare with production configuration

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Let's Encrypt](https://letsencrypt.org/getting-started/)

