# 🔐 Keycloak Docker Setup Guide

Complete guide for setting up Keycloak with Docker for both development and production.

---

## 📋 Table of Contents

1. [Quick Start (Development)](#quick-start-development)
2. [Production Deployment](#production-deployment)
3. [Configuration](#configuration)
4. [Realm Setup](#realm-setup)
5. [Backup & Restore](#backup--restore)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start (Development)

### Option 1: Docker Compose (Recommended)

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# Start Keycloak with PostgreSQL
docker-compose -f docker-compose-keycloak.yml up -d

# Wait for services to be ready (60 seconds)
echo "⏳ Waiting for Keycloak to start..."
sleep 60

# Check status
docker-compose -f docker-compose-keycloak.yml ps

# View logs
docker-compose -f docker-compose-keycloak.yml logs -f keycloak
```

**Access Keycloak:**
- URL: http://localhost:8080
- Admin Console: http://localhost:8080/admin/
- Username: `admin`
- Password: `admin`

### Option 2: Single Docker Command (Simple)

```bash
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:23.0 \
  start-dev
```

**⚠️ Note:** This uses H2 database (not recommended for production)

---

## 🏭 Production Deployment

### Prerequisites

1. **Domain name** (e.g., api.connectme.totesoft.com)
2. **SSL certificates** (Let's Encrypt recommended)
3. **Server with Docker & Docker Compose**
4. **Firewall configured** (ports 80, 443)

### Step 1: Prepare Environment

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# Copy environment template
cp keycloak.env.example keycloak.env

# Edit with your values
nano keycloak.env
```

**Update these values:**
```bash
KEYCLOAK_DB_PASSWORD=your_strong_password_here
KEYCLOAK_ADMIN_USER=admin
KEYCLOAK_ADMIN_PASSWORD=your_admin_password_here
KEYCLOAK_HOSTNAME=api.connectme.totesoft.com
```

### Step 2: Set Up SSL Certificates

#### Option A: Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot

# Get certificates
sudo certbot certonly --standalone \
  -d api.connectme.totesoft.com \
  --email admin@totesoft.com \
  --agree-tos

# Create certs directory
mkdir -p certs

# Copy certificates
sudo cp /etc/letsencrypt/live/api.connectme.totesoft.com/fullchain.pem certs/
sudo cp /etc/letsencrypt/live/api.connectme.totesoft.com/privkey.pem certs/
sudo chmod 644 certs/*.pem
```

#### Option B: Self-Signed (Testing Only)

```bash
mkdir -p certs

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout certs/privkey.pem \
  -out certs/fullchain.pem \
  -subj "/CN=api.connectme.totesoft.com"
```

### Step 3: Deploy Production Keycloak

```bash
# Load environment variables
export $(cat keycloak.env | xargs)

# Start production Keycloak
docker-compose -f docker-compose-keycloak-production.yml up -d

# Wait for startup
sleep 90

# Check status
docker-compose -f docker-compose-keycloak-production.yml ps

# View logs
docker-compose -f docker-compose-keycloak-production.yml logs -f
```

### Step 4: Verify Deployment

```bash
# Health check
curl https://api.connectme.totesoft.com/health/ready

# Should return: {"status":"UP"}
```

**Access Production Keycloak:**
- URL: https://api.connectme.totesoft.com
- Admin: https://api.connectme.totesoft.com/admin/

---

## ⚙️ Configuration

### Configure Realm & Client

After Keycloak is running, configure for ConnectMe:

```bash
# Access admin console
open http://localhost:8080/admin/  # Dev
# or
open https://api.connectme.totesoft.com/admin/  # Production

# Login with admin credentials
```

**1. Create Realm:**
- Click dropdown (top-left) → "Create Realm"
- Name: `connectme`
- Enabled: ON
- Click "Create"

**2. Create Client:**
- Go to: Clients → Create client
- Client ID: `connectme-frontend`
- Client Protocol: `openid-connect`
- Click "Next"

**Client Settings:**
```yaml
Access Type: public
Standard Flow: Enabled
Direct Access Grants: Enabled

Valid Redirect URIs:
  - http://localhost:3000/*
  - https://connectme.totesoft.com/*

Web Origins:
  - http://localhost:3000
  - https://connectme.totesoft.com

Valid Post Logout Redirect URIs:
  - http://localhost:3000/*
  - https://connectme.totesoft.com/*
```

**3. Create Test User:**
- Go to: Users → Add user
- Username: `testuser`
- Email: `test@connectme.com`
- First name: `Test`
- Last name: `User`
- Email verified: ON
- Click "Create"

**Set Password:**
- Go to: Credentials tab
- Set password: `testpass123`
- Temporary: OFF
- Click "Save"

**4. Create Roles:**
- Go to: Realm roles → Create role
- Create these roles:
  - `admin` - Administrator access
  - `manager` - Manager access
  - `staff` - Staff access
  - `billing` - Billing access

**5. Assign Roles to User:**
- Go to: Users → testuser → Role mappings
- Assign role: `admin`

---

## 🔄 Backup & Restore

### Automated Backup Script

Create `backup-keycloak.sh`:

```bash
#!/bin/bash

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER="keycloak-postgres"

mkdir -p $BACKUP_DIR

# Backup PostgreSQL database
docker exec $CONTAINER pg_dump -U keycloak keycloak > \
  "$BACKUP_DIR/keycloak_backup_$TIMESTAMP.sql"

# Compress backup
gzip "$BACKUP_DIR/keycloak_backup_$TIMESTAMP.sql"

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup completed: keycloak_backup_$TIMESTAMP.sql.gz"
```

```bash
chmod +x backup-keycloak.sh

# Run backup
./backup-keycloak.sh

# Schedule daily backups (crontab)
crontab -e
# Add: 0 2 * * * /path/to/backup-keycloak.sh
```

### Restore from Backup

```bash
# Stop Keycloak
docker-compose -f docker-compose-keycloak.yml down

# Restore database
gunzip -c backups/keycloak_backup_20241004_120000.sql.gz | \
  docker exec -i keycloak-postgres psql -U keycloak keycloak

# Start Keycloak
docker-compose -f docker-compose-keycloak.yml up -d
```

---

## 📊 Monitoring

### Health Checks

```bash
# Keycloak health
curl http://localhost:8080/health
curl http://localhost:8080/health/ready
curl http://localhost:8080/health/live

# Metrics (Prometheus format)
curl http://localhost:8080/metrics
```

### Container Status

```bash
# View running containers
docker-compose -f docker-compose-keycloak.yml ps

# View logs
docker-compose -f docker-compose-keycloak.yml logs -f

# Container stats
docker stats keycloak keycloak-postgres
```

### Database Monitoring

```bash
# Connect to PostgreSQL
docker exec -it keycloak-postgres psql -U keycloak

# Useful queries
SELECT COUNT(*) FROM user_entity;
SELECT COUNT(*) FROM credential;
SELECT * FROM realm;
```

---

## 🔧 Management Commands

### Start/Stop Services

```bash
# Start
docker-compose -f docker-compose-keycloak.yml up -d

# Stop
docker-compose -f docker-compose-keycloak.yml down

# Restart
docker-compose -f docker-compose-keycloak.yml restart

# Stop and remove volumes (⚠️ deletes data)
docker-compose -f docker-compose-keycloak.yml down -v
```

### Update Keycloak

```bash
# Pull latest image
docker-compose -f docker-compose-keycloak.yml pull

# Recreate containers
docker-compose -f docker-compose-keycloak.yml up -d --force-recreate
```

### View Logs

```bash
# All logs
docker-compose -f docker-compose-keycloak.yml logs -f

# Keycloak only
docker logs -f keycloak

# PostgreSQL only
docker logs -f keycloak-postgres

# Last 100 lines
docker logs --tail 100 keycloak
```

---

## 🐛 Troubleshooting

### Keycloak Won't Start

**Check logs:**
```bash
docker logs keycloak
```

**Common issues:**

1. **Port already in use:**
   ```bash
   lsof -ti:8080 | xargs kill -9
   ```

2. **Database connection failed:**
   ```bash
   # Check PostgreSQL is running
   docker ps | grep postgres
   
   # Check database logs
   docker logs keycloak-postgres
   ```

3. **Out of memory:**
   ```bash
   # Increase Docker memory limit
   # Docker Desktop → Settings → Resources → Memory
   ```

### Can't Access Admin Console

1. **Check Keycloak is running:**
   ```bash
   curl http://localhost:8080/health
   ```

2. **Check firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 8080/tcp
   ```

3. **Reset admin password:**
   ```bash
   docker exec -it keycloak /opt/keycloak/bin/kc.sh \
     user-password --username admin --password newpassword
   ```

### Database Issues

**Reset database (⚠️ deletes all data):**
```bash
docker-compose -f docker-compose-keycloak.yml down -v
docker volume rm keycloak-postgres-data
docker-compose -f docker-compose-keycloak.yml up -d
```

### Performance Issues

1. **Increase memory:**
   Edit `docker-compose-keycloak.yml`:
   ```yaml
   environment:
     JAVA_OPTS: "-Xms512m -Xmx2048m"
   ```

2. **Enable caching:**
   ```yaml
   KC_CACHE: ispn
   KC_CACHE_STACK: kubernetes
   ```

---

## 🔒 Security Best Practices

### Production Checklist

- [ ] Change default admin password
- [ ] Use strong database password
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Enable audit logging
- [ ] Regular security updates

### Hardening

```bash
# Disable unused features
KC_FEATURES_DISABLED: impersonation,admin-api

# Set secure headers
KC_HTTP_HEADERS_FRAME_OPTIONS: DENY
KC_HTTP_HEADERS_CONTENT_SECURITY_POLICY: "frame-ancestors 'none'"

# Require strong passwords
# Configure in Keycloak admin: Realm → Authentication → Password Policy
```

---

## 📚 Additional Resources

- **Keycloak Documentation:** https://www.keycloak.org/documentation
- **Docker Hub:** https://hub.docker.com/r/jboss/keycloak
- **GitHub Issues:** https://github.com/keycloak/keycloak/issues

---

## ✅ Quick Reference

### Development
```bash
docker-compose -f docker-compose-keycloak.yml up -d
```
URL: http://localhost:8080

### Production
```bash
docker-compose -f docker-compose-keycloak-production.yml up -d
```
URL: https://api.connectme.totesoft.com

### Backup
```bash
./backup-keycloak.sh
```

### Logs
```bash
docker logs -f keycloak
```

---

## 🎯 Next Steps

After Keycloak is running:

1. ✅ Configure realm and client (see Configuration section)
2. ✅ Create test user
3. ✅ Update frontend `.env.local`
4. ✅ Run `./START_TESTING.sh`
5. ✅ Test login flow

**Ready to configure?** See the [Configuration](#configuration) section above!

