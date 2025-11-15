# 🔐 Keycloak Docker - Quick Start

## 🚀 **1-Command Setup**

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./setup-keycloak.sh
```

**That's it!** The script will:
- ✅ Check Docker is installed
- ✅ Start Keycloak with PostgreSQL
- ✅ Wait for services to be ready
- ✅ Open admin console
- ✅ Show you next steps

---

## 📋 **What You Get**

### Development Mode (Default)
- **URL:** http://localhost:8080
- **Admin:** http://localhost:8080/admin/
- **Username:** `admin`
- **Password:** `admin`
- **Database:** PostgreSQL (persistent)
- **Ready for:** Local development & testing

### Production Mode (Optional)
- **URL:** https://your-domain.com
- **HTTPS:** SSL certificates required
- **Database:** PostgreSQL with backups
- **Ready for:** Production deployment

---

## ⚡ **Quick Commands**

### Start Keycloak
```bash
./setup-keycloak.sh
```

### Check Status
```bash
docker-compose -f docker-compose-keycloak.yml ps
```

### View Logs
```bash
docker-compose -f docker-compose-keycloak.yml logs -f
```

### Stop Keycloak
```bash
docker-compose -f docker-compose-keycloak.yml down
```

### Restart Keycloak
```bash
docker-compose -f docker-compose-keycloak.yml restart
```

---

## 🎯 **After Starting Keycloak**

### Step 1: Access Admin Console
```bash
open http://localhost:8080/admin/
```
Login: `admin` / `admin`

### Step 2: Create Realm
1. Click dropdown (top-left) → "Create Realm"
2. Name: `connectme`
3. Click "Create"

### Step 3: Create Client
1. Go to: **Clients** → "Create client"
2. **Client ID:** `connectme-frontend`
3. Click "Next"
4. **Client authentication:** OFF (public client)
5. **Standard flow:** ON
6. **Direct access grants:** ON
7. Click "Save"

**Configure Redirect URIs:**
1. Go to client settings
2. **Valid redirect URIs:** 
   - `http://localhost:3000/*`
   - `https://connectme.totesoft.com/*`
3. **Web origins:**
   - `http://localhost:3000`
   - `https://connectme.totesoft.com`
4. Click "Save"

### Step 4: Create Test User
1. Go to: **Users** → "Add user"
2. **Username:** `testuser`
3. **Email:** `test@connectme.com`
4. **First name:** `Test`
5. **Last name:** `User`
6. **Email verified:** ON
7. Click "Create"

**Set Password:**
1. Go to: **Credentials** tab
2. Click "Set password"
3. **Password:** `testpass123`
4. **Temporary:** OFF
5. Click "Save"

### Step 5: Update Frontend Config
```bash
# Update frontend/.env.local
echo 'NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080' >> frontend/.env.local
```

### Step 6: Test!
```bash
./START_TESTING.sh
```

---

## 📊 **Container Management**

### View All Containers
```bash
docker ps
```

### Stop All
```bash
docker-compose -f docker-compose-keycloak.yml down
```

### Remove Everything (⚠️ Deletes Data)
```bash
docker-compose -f docker-compose-keycloak.yml down -v
```

### Backup Database
```bash
docker exec keycloak-postgres pg_dump -U keycloak keycloak > keycloak_backup.sql
```

### Restore Database
```bash
cat keycloak_backup.sql | docker exec -i keycloak-postgres psql -U keycloak keycloak
```

---

## 🔧 **Troubleshooting**

### Port 8080 Already in Use
```bash
# Find what's using port 8080
lsof -ti:8080

# Kill the process
lsof -ti:8080 | xargs kill -9

# Or change Keycloak port in docker-compose-keycloak.yml:
ports:
  - "8081:8080"  # Use 8081 instead
```

### Can't Access Admin Console
```bash
# Check if Keycloak is running
docker ps | grep keycloak

# Check logs
docker logs keycloak

# Restart
docker-compose -f docker-compose-keycloak.yml restart
```

### Forgot Admin Password
```bash
# Reset admin password
docker exec -it keycloak /opt/keycloak/bin/kc.sh \
  user-password --username admin --password newpassword
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs keycloak-postgres

# Restart both services
docker-compose -f docker-compose-keycloak.yml restart
```

---

## 🏭 **Production Deployment**

### Use Production Config

```bash
# Run setup script and choose option 2
./setup-keycloak.sh
# Select: 2) Production

# Or manually:
docker-compose -f docker-compose-keycloak-production.yml up -d
```

### Requirements
- ✅ Domain name (e.g., api.connectme.totesoft.com)
- ✅ SSL certificates (Let's Encrypt or purchased)
- ✅ Firewall configured (ports 80, 443)
- ✅ Environment variables set (keycloak.env)

### Get SSL Certificates (Let's Encrypt)
```bash
# Install certbot
brew install certbot  # macOS
# or
sudo apt-get install certbot  # Linux

# Get certificates
sudo certbot certonly --standalone \
  -d api.connectme.totesoft.com \
  --email admin@totesoft.com \
  --agree-tos

# Copy to project
mkdir -p certs
sudo cp /etc/letsencrypt/live/api.connectme.totesoft.com/fullchain.pem certs/
sudo cp /etc/letsencrypt/live/api.connectme.totesoft.com/privkey.pem certs/
chmod 644 certs/*.pem
```

---

## 📚 **Full Documentation**

For detailed configuration, backup strategies, and advanced topics:

📖 **See:** `KEYCLOAK_DOCKER_GUIDE.md`

---

## ✅ **Verification Checklist**

After setup, verify:

- [ ] Can access http://localhost:8080
- [ ] Can login to admin console (admin/admin)
- [ ] Created realm "connectme"
- [ ] Created client "connectme-frontend"
- [ ] Created test user "testuser"
- [ ] Test login works:
  ```bash
  curl -X POST http://localhost:8080/realms/connectme/protocol/openid-connect/token \
    -d "client_id=connectme-frontend" \
    -d "username=testuser" \
    -d "password=testpass123" \
    -d "grant_type=password"
  ```
- [ ] Frontend `.env.local` updated
- [ ] Application login works

---

## 🎊 **Success!**

Once all steps are complete:

```bash
# Start your application
./START_TESTING.sh

# Login at http://localhost:3000
# Use: testuser / testpass123
```

**Enjoy your fully working Keycloak authentication! 🚀**

