# Debian Server Deployment Guide

Complete guide to deploy ConnectMe Healthcare Platform on Debian 11/12 with proper SSL and domain setup.

---

## 📋 Prerequisites

### Server Requirements
- **OS**: Debian 11 (Bullseye) or Debian 12 (Bookworm)
- **RAM**: 4GB minimum (8GB recommended)
- **CPU**: 2 cores minimum
- **Disk**: 20GB minimum
- **Network**: Public IP with open ports 80, 443

### Domain Setup
- Domain name (e.g., `connectme.yourdomain.com`)
- DNS A record pointing to your server IP
- Subdomain for API (e.g., `api.connectme.yourdomain.com`) - optional

### Credentials Needed
- UHC API credentials (API key, TIN, Client ID, Client Secret)
- Keycloak realm: `connectme` at `https://auth.totesoft.com`
- GitHub repository access (if using private repo)

---

## 🚀 Quick Deployment (Automated)

### Step 1: Clone Repository

```bash
# SSH into your Debian server
ssh user@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install git if not present
sudo apt install -y git

# Setup SSH key for deployment
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Copy your deployment key to the server
# From your local machine, run:
# scp ~/Documents/Access/cursor/deployment_key_anchorvpn_be user@your-server-ip:~/.ssh/deployment_key
# Then back on the server:
chmod 600 ~/.ssh/deployment_key

# Add SSH config for GitHub
cat >> ~/.ssh/config <<EOF
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deployment_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
EOF
chmod 600 ~/.ssh/config

# Test SSH connection
ssh -T git@github.com

# Clone the repository using SSH
cd /var/www
sudo mkdir -p connectme
sudo chown $USER:$USER connectme
git clone git@github.com:yourusername/connectme.git
cd connectme
```

### Step 2: Run Automated Setup

```bash
# Make setup script executable
chmod +x deploy/debian-setup.sh

# Run the setup script
sudo ./deploy/debian-setup.sh
```

The script will:
- Install Python 3.11, Node.js 20, PostgreSQL, Redis, Nginx
- Set up virtual environments
- Configure systemd services
- Set up SSL with Let's Encrypt
- Configure firewall

### Step 3: Configure Environment

Edit the environment files:

```bash
# Backend environment
sudo nano /var/www/connectme/backend/.env
```

```env
# Django Settings
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=api.connectme.yourdomain.com,connectme.yourdomain.com

# Database
DATABASE_NAME=connectme_db
DATABASE_USER=connectme_user
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Keycloak
KEYCLOAK_URL=https://auth.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-backend
KEYCLOAK_CLIENT_SECRET=your-keycloak-backend-secret
KEYCLOAK_PUBLIC_KEY=your-keycloak-realm-public-key

# UHC API
UHC_API_KEY=your-uhc-api-key
UHC_CLIENT_ID=your-uhc-client-id
UHC_CLIENT_SECRET=your-uhc-client-secret
UHC_TIN=854203105
UHC_PAYER_ID=87726
UHC_BASE_URL=https://apimarketplace.uhc.com/Claims

# CORS
CORS_ALLOWED_ORIGINS=https://connectme.yourdomain.com

# Security
ENCRYPTION_KEY=generate-with-python-fernet
DATA_RETENTION_DAYS=2555
```

Frontend environment:

```bash
sudo nano /var/www/connectme/frontend/.env.production
```

```env
NEXT_PUBLIC_API_URL=https://api.connectme.yourdomain.com
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
NODE_ENV=production
```

### Step 4: Start Services

```bash
# Start backend
sudo systemctl start connectme-backend
sudo systemctl enable connectme-backend

# Start frontend
sudo systemctl start connectme-frontend
sudo systemctl enable connectme-frontend

# Check status
sudo systemctl status connectme-backend
sudo systemctl status connectme-frontend
```

---

## 📝 Manual Deployment (Step-by-Step)

If you prefer manual setup or the script fails, follow these detailed steps:

### 1. System Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git build-essential libssl-dev \
    libffi-dev python3-dev python3-pip python3-venv \
    postgresql postgresql-contrib redis-server nginx \
    certbot python3-certbot-nginx ufw
```

### 2. Install Node.js 20

```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version  # Should be v20.x
npm --version   # Should be 10.x
```

### 3. Install Python 3.11

```bash
# Debian 12 already has Python 3.11
python3 --version

# If on Debian 11, add deadsnakes PPA
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

### 4. Setup PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE connectme_db;
CREATE USER connectme_user WITH PASSWORD 'your-secure-password';
ALTER ROLE connectme_user SET client_encoding TO 'utf8';
ALTER ROLE connectme_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE connectme_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE connectme_db TO connectme_user;
\q
```

### 5. Setup Application Directory

```bash
# Create app directory
sudo mkdir -p /var/www/connectme
sudo chown $USER:$USER /var/www/connectme
cd /var/www/connectme

# Clone repository using SSH (with deployment key)
# Make sure you've set up SSH key as shown in Quick Deployment section above
git clone git@github.com:yourusername/connectme.git .

# Or if uploading manually (alternative method):
# From your local machine:
# rsync -avz --exclude='node_modules' --exclude='venv' --exclude='.next' \
#   ~/Documents/1_Data/AI/abce/connectme/ user@server:/var/www/connectme/
```

### 6. Setup Backend

```bash
cd /var/www/connectme/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/base.txt
pip install gunicorn

# Create .env file (see Step 3 above)
nano .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test backend
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 7. Setup Frontend

```bash
cd /var/www/connectme/frontend

# Install dependencies
npm ci --production

# Create .env.production file (see Step 3 above)
nano .env.production

# Build frontend
npm run build

# Test frontend
npm run start
```

### 8. Configure Nginx

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/connectme
```

```nginx
# Backend API configuration
server {
    listen 80;
    server_name api.connectme.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.connectme.yourdomain.com;

    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/api.connectme.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.connectme.yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_session_timeout 10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /var/www/connectme/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/connectme/backend/media/;
        expires 7d;
    }

    # API proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Logging
    access_log /var/log/nginx/api.connectme.access.log;
    error_log /var/log/nginx/api.connectme.error.log;
}

# Frontend configuration
server {
    listen 80;
    server_name connectme.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name connectme.yourdomain.com;

    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/connectme.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/connectme.yourdomain.com/privkey.pem;

    # SSL configuration (same as above)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Next.js frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets
    location /_next/static {
        proxy_cache STATIC;
        proxy_pass http://127.0.0.1:3000;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Logging
    access_log /var/log/nginx/connectme.access.log;
    error_log /var/log/nginx/connectme.error.log;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/connectme /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Setup SSL Certificates

```bash
# Install certbot plugin for Nginx
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificates (do this BEFORE editing Nginx config with SSL)
sudo certbot --nginx -d connectme.yourdomain.com -d api.connectme.yourdomain.com

# Follow prompts:
# - Enter email address
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (option 2)

# Verify auto-renewal
sudo certbot renew --dry-run
```

### 10. Create Systemd Services

**Backend Service:**

```bash
sudo nano /etc/systemd/system/connectme-backend.service
```

```ini
[Unit]
Description=ConnectMe Backend (Gunicorn)
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/connectme/backend
Environment="PATH=/var/www/connectme/backend/venv/bin"
ExecStart=/var/www/connectme/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    --access-logfile /var/log/connectme/backend-access.log \
    --error-logfile /var/log/connectme/backend-error.log \
    --log-level info \
    config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Frontend Service:**

```bash
sudo nano /etc/systemd/system/connectme-frontend.service
```

```ini
[Unit]
Description=ConnectMe Frontend (Next.js)
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/connectme/frontend
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/npm run start
Restart=always
RestartSec=5
StandardOutput=append:/var/log/connectme/frontend.log
StandardError=append:/var/log/connectme/frontend-error.log

[Install]
WantedBy=multi-user.target
```

**Celery Worker Service (for async tasks):**

```bash
sudo nano /etc/systemd/system/connectme-celery.service
```

```ini
[Unit]
Description=ConnectMe Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/connectme/backend
Environment="PATH=/var/www/connectme/backend/venv/bin"
ExecStart=/var/www/connectme/backend/venv/bin/celery -A config multi start worker \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/connectme/celery-%n%I.log \
    --loglevel=INFO
ExecStop=/var/www/connectme/backend/venv/bin/celery -A config multi stopwait worker \
    --pidfile=/var/run/celery/%n.pid
ExecReload=/var/www/connectme/backend/venv/bin/celery -A config multi restart worker \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/connectme/celery-%n%I.log \
    --loglevel=INFO
Restart=always

[Install]
WantedBy=multi-user.target
```

Create log directories:

```bash
sudo mkdir -p /var/log/connectme
sudo mkdir -p /var/run/celery
sudo chown www-data:www-data /var/log/connectme
sudo chown www-data:www-data /var/run/celery
```

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable connectme-backend connectme-frontend connectme-celery
sudo systemctl start connectme-backend connectme-frontend connectme-celery

# Check status
sudo systemctl status connectme-backend
sudo systemctl status connectme-frontend
sudo systemctl status connectme-celery
```

### 11. Configure Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (important!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status verbose
```

### 12. Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/connectme
```

```
/var/log/connectme/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload connectme-backend > /dev/null 2>&1 || true
        systemctl reload connectme-frontend > /dev/null 2>&1 || true
    endscript
}
```

---

## 🧪 Testing Deployment

### 1. Test Backend API

```bash
# Health check
curl https://api.connectme.yourdomain.com/health/

# Admin panel
https://api.connectme.yourdomain.com/admin/

# API endpoints
curl https://api.connectme.yourdomain.com/api/v1/
```

### 2. Test Frontend

Open browser and visit:
```
https://connectme.yourdomain.com
```

Should see the login page with Keycloak integration.

### 3. Test UHC API Connection

```bash
# SSH into server
cd /var/www/connectme/backend
source venv/bin/activate
python manage.py shell
```

```python
import requests
response = requests.get('https://apimarketplace.uhc.com')
print(response.status_code)  # Should be 200 or similar
```

### 4. Test Claims Search

1. Login with Keycloak credentials
2. Navigate to Claims page
3. Search for claims with date range
4. Should see results without errors

---

## 🔧 Troubleshooting

### Backend Won't Start

```bash
# Check logs
sudo journalctl -u connectme-backend -f

# Check Gunicorn errors
sudo tail -f /var/log/connectme/backend-error.log

# Test manually
cd /var/www/connectme/backend
source venv/bin/activate
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend Won't Start

```bash
# Check logs
sudo journalctl -u connectme-frontend -f

# Check build
cd /var/www/connectme/frontend
npm run build

# Test manually
npm run start
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U connectme_user -d connectme_db -h localhost

# Check credentials in .env file
```

### SSL Certificate Issues

```bash
# Renew certificates manually
sudo certbot renew --force-renewal

# Check certificate expiry
sudo certbot certificates
```

### UHC API Connection Issues

```bash
# Test DNS resolution
nslookup apimarketplace.uhc.com

# Test connection
curl -v https://apimarketplace.uhc.com

# Check firewall
sudo ufw status
```

---

## 📊 Monitoring

### Setup Monitoring Script

```bash
sudo nano /usr/local/bin/monitor-connectme.sh
```

```bash
#!/bin/bash
echo "=== ConnectMe Health Check ==="
echo "Backend: $(systemctl is-active connectme-backend)"
echo "Frontend: $(systemctl is-active connectme-frontend)"
echo "Celery: $(systemctl is-active connectme-celery)"
echo "PostgreSQL: $(systemctl is-active postgresql)"
echo "Redis: $(systemctl is-active redis)"
echo "Nginx: $(systemctl is-active nginx)"
echo ""
echo "=== Disk Usage ==="
df -h /var/www/connectme
echo ""
echo "=== Memory Usage ==="
free -h
echo ""
echo "=== Recent Backend Errors ==="
sudo tail -20 /var/log/connectme/backend-error.log
```

```bash
chmod +x /usr/local/bin/monitor-connectme.sh

# Run it
/usr/local/bin/monitor-connectme.sh
```

### Setup Cron Jobs

```bash
crontab -e
```

```cron
# Daily database backup
0 2 * * * /usr/local/bin/backup-connectme-db.sh

# Weekly certificate renewal check
0 3 * * 0 certbot renew --quiet

# Daily log cleanup
0 4 * * * find /var/log/connectme -name "*.log" -mtime +30 -delete
```

---

## 🔐 Security Checklist

- [ ] SSL certificates installed and auto-renewing
- [ ] Firewall enabled (UFW) with only necessary ports
- [ ] Strong database passwords
- [ ] Django SECRET_KEY changed from default
- [ ] DEBUG=False in production
- [ ] PostgreSQL listening only on localhost
- [ ] Regular security updates (`apt upgrade`)
- [ ] Fail2ban installed for brute-force protection
- [ ] Regular backups configured
- [ ] Audit logging enabled
- [ ] HIPAA compliance measures in place

---

## 📦 Backup Strategy

### Database Backup Script

```bash
sudo nano /usr/local/bin/backup-connectme-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/connectme"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
sudo -u postgres pg_dump connectme_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/connectme/backend/media/

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
chmod +x /usr/local/bin/backup-connectme-db.sh
```

---

## 🚀 Next Steps After Deployment

1. ✅ Configure Keycloak users and roles
2. ✅ Import initial data (providers, credentials)
3. ✅ Test claims search with real data
4. ✅ Set up monitoring and alerts
5. ✅ Configure backup schedule
6. ✅ Document deployment for team
7. ✅ Set up staging environment (optional)

---

**Deployment Status**: Ready for Production ✅
**Estimated Time**: 2-3 hours for manual setup, 30 minutes for automated
**Support**: Check logs in `/var/log/connectme/` and systemd journals

