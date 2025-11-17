# Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Manual Deployment](#manual-deployment)
4. [GitHub Actions CI/CD](#github-actions-cicd)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [SSL Configuration](#ssl-configuration)
8. [Monitoring](#monitoring)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Server Requirements
- **OS:** Ubuntu 22.04 LTS or later
- **CPU:** 4+ cores
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 50GB minimum, 100GB recommended (SSD)
- **Network:** Static IP address, ports 80/443 open

### Domain & DNS
- Domain name registered
- DNS A record pointing to server IP
- (Optional) www subdomain CNAME

### Access Requirements
- Root or sudo access to server
- SSH key for GitHub (if using private repo)
- UHC API credentials
- Keycloak server URL and credentials

---

## Server Setup

### Option 1: Automated Setup (Recommended)

```bash
# 1. Download setup script
wget https://raw.githubusercontent.com/yourorg/connectme/main/deploy/setup-server.sh

# 2. Edit configuration
nano setup-server.sh
# Change DOMAIN and EMAIL variables

# 3. Run setup script
chmod +x setup-server.sh
sudo ./setup-server.sh
```

The script will install and configure:
- ✅ Python 3.11 + virtual environment
- ✅ Node.js 20.x
- ✅ PostgreSQL 15
- ✅ Redis 7
- ✅ Nginx
- ✅ Systemd services
- ✅ SSL certificates (Let's Encrypt)

### Option 2: Manual Setup

See [MANUAL_SETUP.md](./MANUAL_SETUP.md) for step-by-step instructions.

---

## Manual Deployment

### 1. Clone Repository

```bash
# As root or with sudo
sudo su - connectme
cd /opt/connectme

# Clone repository
git clone https://github.com/yourorg/connectme.git .

# Or if private repo
git clone git@github.com:yourorg/connectme.git .
```

### 2. Configure Environment

```bash
# Create production environment file
cp .env.example .env.production

# Edit with your values
nano .env.production
```

Required environment variables (see [Environment Variables](#environment-variables) section).

### 3. Backend Setup

```bash
cd /opt/connectme/backend

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. Frontend Setup

```bash
cd /opt/connectme/frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 5. Start Services

```bash
# Enable services to start on boot
sudo systemctl enable connectme-backend
sudo systemctl enable connectme-frontend
sudo systemctl enable connectme-celery

# Start services
sudo systemctl start connectme-backend
sudo systemctl start connectme-frontend
sudo systemctl start connectme-celery

# Check status
sudo systemctl status connectme-backend
sudo systemctl status connectme-frontend
sudo systemctl status connectme-celery
```

### 6. Configure Nginx

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 7. Verify Deployment

```bash
# Check backend health
curl https://yourdomain.com/api/health/

# Check frontend
curl https://yourdomain.com/

# Check logs
sudo journalctl -u connectme-backend -f
sudo journalctl -u connectme-frontend -f
```

---

## GitHub Actions CI/CD

### Setup

1. **Add GitHub Secrets**

Go to your repository → Settings → Secrets and variables → Actions

Add the following secrets:

```
SSH_PRIVATE_KEY: Your SSH private key for server access
SERVER_HOST: yourdomain.com or server IP
SERVER_USER: connectme
APP_DIR: /opt/connectme
```

2. **Generate SSH Key**

```bash
# On your local machine
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions

# Copy private key to GitHub secrets
cat ~/.ssh/github_actions

# Add public key to server
ssh-copy-id -i ~/.ssh/github_actions.pub connectme@yourdomain.com
```

3. **Configure Server for Passwordless Sudo**

```bash
# On server as root
echo "connectme ALL=(ALL) NOPASSWD: /bin/systemctl restart connectme-backend" >> /etc/sudoers.d/connectme
echo "connectme ALL=(ALL) NOPASSWD: /bin/systemctl restart connectme-frontend" >> /etc/sudoers.d/connectme
echo "connectme ALL=(ALL) NOPASSWD: /bin/systemctl restart connectme-celery" >> /etc/sudoers.d/connectme
echo "connectme ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx" >> /etc/sudoers.d/connectme
echo "connectme ALL=(ALL) NOPASSWD: /bin/systemctl status *" >> /etc/sudoers.d/connectme

chmod 0440 /etc/sudoers.d/connectme
```

### Workflow

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:

1. **On every push to `main`:**
   - Run backend tests
   - Run frontend linting and build
   - Deploy to production server
   - Run health checks
   - Notify on success/failure

2. **Manual trigger:**
   - Go to Actions tab → Deploy to Production → Run workflow

### Rollback

If deployment fails, rollback to previous version:

```bash
# On server
cd /opt/connectme
git log --oneline -10  # Find previous commit
git reset --hard <commit-hash>

# Restart services
sudo systemctl restart connectme-backend
sudo systemctl restart connectme-frontend
```

---

## Environment Variables

### Backend (.env.production)

```bash
# Django
SECRET_KEY=<generate-with-python-secrets>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://connectme_user:PASSWORD@localhost:5432/connectme_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Keycloak
KEYCLOAK_SERVER_URL=https://auth.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-backend
KEYCLOAK_CLIENT_SECRET=<from-keycloak>

# UHC API
UHC_CLIENT_ID=<from-uhc>
UHC_CLIENT_SECRET=<from-uhc>
UHC_TOKEN_URL=https://apimarketplace.uhc.com/v1/oauthtoken
UHC_API_BASE_URL=https://apimarketplace.uhc.com/Claims

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-password>

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Frontend (.env.production)

```bash
# API
NEXT_PUBLIC_API_URL=https://yourdomain.com/api/v1

# Keycloak
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

### Generate Secret Key

```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(50))
```

---

## Database Setup

### Initial Setup

```bash
# Create database and user (done by setup script)
sudo -u postgres psql

CREATE DATABASE connectme_db;
CREATE USER connectme_user WITH PASSWORD 'your-secure-password';
ALTER ROLE connectme_user SET client_encoding TO 'utf8';
ALTER ROLE connectme_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE connectme_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE connectme_db TO connectme_user;
\q
```

### Run Migrations

```bash
cd /opt/connectme/backend
source ../venv/bin/activate
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Load Initial Data (Optional)

```bash
# If you have fixtures
python manage.py loaddata initial_data.json
```

---

## SSL Configuration

### Let's Encrypt (Recommended)

```bash
# Install certbot (done by setup script)
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal is configured via cron
```

### Manual Certificate

If using a purchased SSL certificate:

```bash
# Copy certificate files
sudo cp your-cert.crt /etc/ssl/certs/
sudo cp your-key.key /etc/ssl/private/

# Update Nginx configuration
sudo nano /etc/nginx/sites-available/connectme

# Change these lines:
ssl_certificate /etc/ssl/certs/your-cert.crt;
ssl_certificate_key /etc/ssl/private/your-key.key;

# Restart Nginx
sudo systemctl restart nginx
```

---

## Monitoring

### Service Status

```bash
# Check all services
sudo systemctl status connectme-backend
sudo systemctl status connectme-frontend
sudo systemctl status connectme-celery
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis
```

### Logs

```bash
# Backend logs
sudo journalctl -u connectme-backend -f

# Frontend logs
sudo journalctl -u connectme-frontend -f

# Celery logs
sudo journalctl -u connectme-celery -f

# Nginx logs
sudo tail -f /var/log/nginx/connectme_access.log
sudo tail -f /var/log/nginx/connectme_error.log

# Application logs
tail -f /var/log/connectme/backend-access.log
tail -f /var/log/connectme/backend-error.log
```

### Performance Monitoring

```bash
# CPU and memory usage
htop

# Disk usage
df -h

# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Redis info
redis-cli INFO
```

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/api/health/

# Frontend health
curl https://yourdomain.com/

# Database health
sudo -u postgres pg_isready

# Redis health
redis-cli ping
```

---

## Backup & Recovery

### Database Backup

```bash
# Create backup script
cat > /opt/connectme/backup-db.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/opt/connectme/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump connectme_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: db_$DATE.sql.gz"
EOF

chmod +x /opt/connectme/backup-db.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/connectme/backup-db.sh") | crontab -
```

### Restore Database

```bash
# Stop backend services
sudo systemctl stop connectme-backend
sudo systemctl stop connectme-celery

# Restore database
gunzip -c /opt/connectme/backups/db_20241005_020000.sql.gz | sudo -u postgres psql connectme_db

# Start services
sudo systemctl start connectme-backend
sudo systemctl start connectme-celery
```

### File Backup

```bash
# Backup media files
tar -czf /opt/connectme/backups/media_$(date +%Y%m%d).tar.gz /opt/connectme/backend/media/

# Backup to remote server (optional)
rsync -avz /opt/connectme/backups/ user@backup-server:/backups/connectme/
```

---

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
sudo journalctl -u connectme-backend -n 50

# Common issues:
# 1. Database connection
sudo -u postgres psql -c "\l"  # Check database exists

# 2. Environment variables
cat /opt/connectme/.env.production  # Verify settings

# 3. Permissions
ls -la /opt/connectme/backend
sudo chown -R connectme:connectme /opt/connectme

# 4. Port already in use
sudo lsof -i :8000
```

### Frontend Not Starting

```bash
# Check logs
sudo journalctl -u connectme-frontend -n 50

# Common issues:
# 1. Build failed
cd /opt/connectme/frontend
sudo -u connectme npm run build

# 2. Port already in use
sudo lsof -i :3000

# 3. Environment variables
cat /opt/connectme/.env.production
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check max connections
sudo -u postgres psql -c "SHOW max_connections;"

# Increase if needed
sudo nano /etc/postgresql/15/main/postgresql.conf
# max_connections = 200
sudo systemctl restart postgresql
```

### Redis Issues

```bash
# Check Redis is running
sudo systemctl status redis

# Check memory usage
redis-cli INFO memory

# Clear cache if needed
redis-cli FLUSHALL
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error log
sudo tail -f /var/log/nginx/error.log

# Common issues:
# 1. Port 80/443 already in use
sudo lsof -i :80
sudo lsof -i :443

# 2. SSL certificate issues
sudo certbot certificates
```

### SSL Certificate Renewal Failed

```bash
# Check certbot logs
sudo cat /var/log/letsencrypt/letsencrypt.log

# Manual renewal
sudo certbot renew --force-renewal

# Check certificate expiry
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

### High CPU/Memory Usage

```bash
# Check processes
htop

# Check Django processes
ps aux | grep gunicorn

# Restart services
sudo systemctl restart connectme-backend
sudo systemctl restart connectme-frontend

# Check for memory leaks
sudo journalctl -u connectme-backend | grep -i "memory"
```

### Slow Queries

```bash
# Enable slow query logging in PostgreSQL
sudo nano /etc/postgresql/15/main/postgresql.conf

# Add:
log_min_duration_statement = 1000  # Log queries > 1 second

# Restart PostgreSQL
sudo systemctl restart postgresql

# View slow queries
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

---

## Maintenance

### Update Dependencies

```bash
# Backend
cd /opt/connectme/backend
source ../venv/bin/activate
pip install --upgrade -r requirements.txt
python manage.py migrate
sudo systemctl restart connectme-backend

# Frontend
cd /opt/connectme/frontend
npm update
npm run build
sudo systemctl restart connectme-frontend
```

### Clear Cache

```bash
# Redis cache
redis-cli FLUSHALL

# Django cache
cd /opt/connectme/backend
source ../venv/bin/activate
python manage.py clear_cache
```

### Rotate Logs

```bash
# Configure logrotate
sudo nano /etc/logrotate.d/connectme

/var/log/connectme/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 connectme connectme
    sharedscripts
    postrotate
        systemctl reload connectme-backend > /dev/null 2>&1 || true
    endscript
}
```

---

## Security Checklist

- [ ] Firewall configured (UFW)
- [ ] SSH key-only authentication
- [ ] Fail2ban installed
- [ ] SSL certificates configured
- [ ] Database password strong and unique
- [ ] Django SECRET_KEY secure
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] CORS settings restrictive
- [ ] Regular security updates
- [ ] Backups automated and tested
- [ ] Monitoring and alerting configured

---

## Support

For issues or questions:
- **Documentation:** https://docs.yourorg.com
- **Email:** support@yourorg.com
- **GitHub Issues:** https://github.com/yourorg/connectme/issues

---

*Last Updated: October 2025*
*Version: 1.0*
