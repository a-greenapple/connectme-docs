# 🚀 Server Setup Quickstart Guide

**Interactive guide to set up your Debian server in minutes!**

---

## 📋 Before You Start

### What You Need:

- [ ] **Debian Server** (IP address and SSH access)
- [ ] **Domain Names** configured with DNS A records:
  - `connectme.be.totesoft.com` → Your server IP
  - `connectme.apps.totesoft.com` → Your server IP
- [ ] **GitHub Repository** with your code
- [ ] **SSH Deployment Key** (already have it! ✅)
- [ ] **Email Address** for SSL certificates

### Estimated Time: 30-40 minutes (mostly automated)

---

## 🎯 Option 1: Automated Setup (Recommended)

### Step 1: Edit Configuration

Open the helper script and add your server details:

```bash
nano deploy/00-local-setup-helper.sh
```

**Edit these lines:**
```bash
SERVER_IP="123.45.67.89"           # Your server IP
SERVER_USER="root"                  # Your SSH username
SERVER_PORT="22"                    # SSH port

GITHUB_USER="yourusername"          # Your GitHub username
GITHUB_REPO="connectme"             # Your repo name
```

### Step 2: Run Automated Setup

From your local machine (Mac):

```bash
cd ~/Documents/1_Data/AI/abce/connectme

# Run the helper script
./deploy/00-local-setup-helper.sh
```

**What it does:**
1. ✅ Tests SSH connection to your server
2. ✅ Copies deployment key to server
3. ✅ Configures GitHub SSH access
4. ✅ Copies setup scripts to server
5. ✅ Optionally runs full server setup

**That's it!** The script will walk you through everything interactively.

---

## 🛠️ Option 2: Manual Step-by-Step

### Step 1: Test Connection

```bash
# From your Mac
ssh user@YOUR_SERVER_IP

# You should be able to connect
# If not, check your SSH credentials
```

### Step 2: Copy Deployment Key

```bash
# From your Mac
scp ~/Documents/Access/cursor/deployment_key_anchorvpn_be user@YOUR_SERVER_IP:~/.ssh/deployment_key

# Set permissions on server
ssh user@YOUR_SERVER_IP "chmod 700 ~/.ssh && chmod 600 ~/.ssh/deployment_key"
```

### Step 3: Configure GitHub SSH

```bash
# On your server
cat > ~/.ssh/config <<'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deployment_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
EOF
chmod 600 ~/.ssh/config

# Test GitHub connection
ssh -T git@github.com
# Should see: "Hi username! You've successfully authenticated..."
```

### Step 4: Upload Setup Scripts

```bash
# From your Mac
cd ~/Documents/1_Data/AI/abce/connectme
scp deploy/01-backend-setup.sh user@YOUR_SERVER_IP:/tmp/
scp deploy/02-frontend-setup.sh user@YOUR_SERVER_IP:/tmp/
```

### Step 5: Run Backend Setup

```bash
# SSH into server
ssh user@YOUR_SERVER_IP

# Run backend setup
sudo SSL_EMAIL=your@email.com bash /tmp/01-backend-setup.sh

# This will take 10-15 minutes
# It installs: PostgreSQL, Redis, Python, Nginx, SSL certificates
```

### Step 6: Run Frontend Setup

```bash
# On the same server or different one
sudo SSL_EMAIL=your@email.com bash /tmp/02-frontend-setup.sh

# This will take 10-15 minutes
# It installs: Node.js, PM2, Nginx, SSL certificates
```

### Step 7: Upload Your Code

```bash
# From your Mac
cd ~/Documents/1_Data/AI/abce/connectme

# Upload backend
rsync -avz --exclude='venv' --exclude='*.pyc' --exclude='__pycache__' \
    backend/ user@YOUR_SERVER_IP:/var/www/connectme-backend/

# Upload frontend
rsync -avz --exclude='node_modules' --exclude='.next' \
    frontend/ user@YOUR_SERVER_IP:/var/www/connectme-frontend/
```

### Step 8: Configure & Start

```bash
# SSH into server
ssh user@YOUR_SERVER_IP

# Backend configuration
cd /var/www/connectme-backend
nano .env  # Edit with your API keys

# Run migrations
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Start backend
sudo systemctl start connectme-backend
sudo systemctl enable connectme-backend

# Frontend configuration
cd /var/www/connectme-frontend
nano .env.production  # Edit API URL

# Build and start
npm ci
npm run build
sudo systemctl start connectme-frontend
sudo systemctl enable connectme-frontend
```

---

## 🧪 Verify Setup

### Test Backend

```bash
# Health check
curl https://connectme.be.totesoft.com/health/

# Admin panel
curl https://connectme.be.totesoft.com/admin/

# Check service
sudo systemctl status connectme-backend

# View logs
sudo journalctl -u connectme-backend -f
```

### Test Frontend

```bash
# Homepage
curl https://connectme.apps.totesoft.com

# Check service
sudo systemctl status connectme-frontend

# PM2 status
pm2 status

# View logs
pm2 logs connectme-frontend
```

---

## 🎯 Interactive Setup Session

**Want me to help you through this live?**

Please provide:

1. **Server IP**: `_______________`
2. **SSH Username**: `_______________`
3. **SSH Port**: `_______________` (default: 22)
4. **GitHub Username**: `_______________`
5. **GitHub Repo**: `_______________`
6. **Email for SSL**: `_______________`

Then I can:
- Generate custom commands for YOUR server
- Walk you through each step
- Help troubleshoot any issues
- Verify everything is working

---

## 📚 Detailed Guides

If you need more information:

| Document | Purpose |
|----------|---------|
| **14_SSH_DEPLOYMENT_KEY_SETUP.md** | SSH key setup details |
| **7_DEBIAN_DEPLOYMENT_GUIDE.md** | Complete deployment guide |
| **10_DEPLOYMENT_SCRIPTS_README.md** | Script documentation |
| **0_DOCUMENTATION_INDEX.md** | Master index |

---

## 🆘 Common Issues

### Issue: Can't SSH to Server

```bash
# Check connection
ping YOUR_SERVER_IP

# Try with verbose
ssh -v user@YOUR_SERVER_IP

# Check if port is open
nc -zv YOUR_SERVER_IP 22
```

### Issue: GitHub Authentication Failed

```bash
# On server, check key
ls -la ~/.ssh/deployment_key

# Test GitHub
ssh -Tv git@github.com

# Check SSH config
cat ~/.ssh/config
```

### Issue: Domain Not Resolving

```bash
# Check DNS
nslookup connectme.be.totesoft.com
dig connectme.be.totesoft.com

# Should show your server IP
```

### Issue: SSL Certificate Failed

```bash
# Make sure ports 80 and 443 are open
sudo ufw status

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Try certbot manually
sudo certbot --nginx -d connectme.be.totesoft.com
```

---

## ✅ Checklist

- [ ] Server accessible via SSH
- [ ] DNS A records configured
- [ ] Deployment key copied to server
- [ ] GitHub SSH working
- [ ] Backend setup complete
- [ ] Frontend setup complete
- [ ] Code uploaded
- [ ] Environment configured
- [ ] Migrations run
- [ ] Services started
- [ ] SSL certificates obtained
- [ ] Backend API responding
- [ ] Frontend app loading

---

## 🎉 Success!

Once all checks pass:

✅ Backend: `https://connectme.be.totesoft.com/admin/`
✅ Frontend: `https://connectme.apps.totesoft.com`
✅ Services: Running and enabled
✅ SSL: Valid certificates
✅ Ready for production! 🚀

---

**Next Steps**: 
- Create users in Keycloak
- Configure UHC API credentials
- Test claims workflow
- Set up monitoring

---

**Last Updated**: October 7, 2025  
**Status**: ✅ Ready to Use  
**Support**: See `0_DOCUMENTATION_INDEX.md` for all guides

