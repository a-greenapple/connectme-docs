# 🔑 SSH Deployment Key Setup Guide

Complete guide to set up SSH deployment key for secure git operations on your Debian server.

**Your Key Location**: `~/Documents/Access/cursor/deployment_key_anchorvpn_be`

---

## 📋 Overview

This guide shows you how to:
1. Copy your existing deployment key to the server
2. Configure SSH to use the key for GitHub
3. Clone and manage the repository securely

---

## 🚀 Quick Setup (From Local Machine)

### Step 1: Copy Deployment Key to Server

From your **local machine** (Mac):

```bash
# Copy the deployment key to your server
scp ~/Documents/Access/cursor/deployment_key_anchorvpn_be user@your-server-ip:~/.ssh/deployment_key

# If you also have a public key (.pub file), copy it too:
scp ~/Documents/Access/cursor/deployment_key_anchorvpn_be.pub user@your-server-ip:~/.ssh/deployment_key.pub
```

### Step 2: Configure SSH on Server

Now **SSH into your server**:

```bash
ssh user@your-server-ip
```

Then run these commands **on the server**:

```bash
# Set proper permissions on SSH directory
chmod 700 ~/.ssh

# Set proper permissions on the key
chmod 600 ~/.ssh/deployment_key

# Create SSH config for GitHub
cat > ~/.ssh/config <<'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deployment_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
EOF

# Set proper permissions on config
chmod 600 ~/.ssh/config
```

### Step 3: Test SSH Connection

```bash
# Test GitHub SSH connection
ssh -T git@github.com

# You should see:
# Hi yourusername! You've successfully authenticated, but GitHub does not provide shell access.
```

### Step 4: Clone Repository

```bash
# Navigate to deployment directory
cd /var/www
sudo mkdir -p connectme
sudo chown $USER:$USER connectme

# Clone using SSH (replace with your actual repo URL)
git clone git@github.com:yourusername/connectme.git
cd connectme
```

---

## 🔐 Security Best Practices

### Verify Key Fingerprint

Before first connection, verify GitHub's SSH key fingerprint:

```bash
# GitHub's RSA fingerprint (as of 2024):
# SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8
```

### Restrict Key Permissions

```bash
# Key file permissions
ls -la ~/.ssh/deployment_key
# Should show: -rw------- (600)

# SSH directory permissions
ls -lad ~/.ssh
# Should show: drwx------ (700)
```

### Test Key Works

```bash
# Test SSH with verbose output
ssh -Tv git@github.com

# Should show successful authentication
```

---

## 📦 Alternative: Using HTTPS with Token

If you prefer HTTPS over SSH:

### Step 1: Generate GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Generate and copy token

### Step 2: Clone with Token

```bash
# Clone using HTTPS with token
git clone https://YOUR_TOKEN@github.com/yourusername/connectme.git
```

### Step 3: Store Credentials (Optional)

```bash
# Store credentials in git credential helper
git config --global credential.helper store

# First git operation will prompt for username and token
# Then credentials will be saved
```

---

## 🛠️ Troubleshooting

### Issue: Permission Denied (publickey)

**Symptoms:**
```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

**Solutions:**

```bash
# 1. Check key permissions
ls -la ~/.ssh/deployment_key
chmod 600 ~/.ssh/deployment_key

# 2. Verify SSH config
cat ~/.ssh/config

# 3. Test with verbose output
ssh -Tv git@github.com

# 4. Ensure key is loaded
ssh-add -l
# If not loaded, add it:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/deployment_key
```

### Issue: Host Key Verification Failed

**Symptoms:**
```
Host key verification failed.
fatal: Could not read from remote repository.
```

**Solutions:**

```bash
# 1. Accept GitHub's host key
ssh-keyscan github.com >> ~/.ssh/known_hosts

# 2. Or, one-time bypass (already in our config):
# StrictHostKeyChecking no
```

### Issue: Wrong Repository URL

**Check current remote URL:**

```bash
cd /var/www/connectme
git remote -v

# Should show:
# origin  git@github.com:yourusername/connectme.git (fetch)
# origin  git@github.com:yourusername/connectme.git (push)
```

**Change to SSH if using HTTPS:**

```bash
git remote set-url origin git@github.com:yourusername/connectme.git
```

---

## 🔄 Daily Operations

### Pull Latest Changes

```bash
cd /var/www/connectme
git pull origin main

# If using a different branch:
git pull origin develop
```

### Check Repository Status

```bash
cd /var/www/connectme
git status
git log --oneline -10
```

### Update Submodules (if any)

```bash
git submodule update --init --recursive
git submodule update --remote
```

---

## 📝 Complete Deployment Workflow

### Initial Setup (One-Time)

```bash
# 1. From local machine: Copy key
scp ~/Documents/Access/cursor/deployment_key_anchorvpn_be user@server:~/.ssh/deployment_key

# 2. On server: Set permissions
ssh user@server
chmod 700 ~/.ssh
chmod 600 ~/.ssh/deployment_key

# 3. On server: Configure SSH
cat > ~/.ssh/config <<'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/deployment_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
EOF
chmod 600 ~/.ssh/config

# 4. On server: Test connection
ssh -T git@github.com

# 5. On server: Clone repository
cd /var/www
sudo mkdir -p connectme
sudo chown $USER:$USER connectme
git clone git@github.com:yourusername/connectme.git
cd connectme
```

### Deployment Updates

```bash
# 1. Pull latest code
cd /var/www/connectme
git pull origin main

# 2. Backend updates
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart connectme-backend

# 3. Frontend updates
cd ../frontend
npm ci
npm run build
pm2 reload connectme-frontend

# 4. Verify services
sudo systemctl status connectme-backend
pm2 status
```

---

## 🔑 Key Management

### Rotate Deployment Key

If you need to change the key:

```bash
# 1. Generate new key (on your local machine)
ssh-keygen -t ed25519 -C "deployment@connectme" -f ~/Documents/Access/cursor/deployment_key_new

# 2. Add new public key to GitHub
cat ~/Documents/Access/cursor/deployment_key_new.pub

# 3. Copy new key to server
scp ~/Documents/Access/cursor/deployment_key_new user@server:~/.ssh/deployment_key_new

# 4. On server: Update SSH config
ssh user@server
mv ~/.ssh/deployment_key ~/.ssh/deployment_key.old
mv ~/.ssh/deployment_key_new ~/.ssh/deployment_key
chmod 600 ~/.ssh/deployment_key

# 5. Test new key
ssh -T git@github.com
```

### Backup Key

```bash
# From local machine - backup to secure location
cp ~/Documents/Access/cursor/deployment_key_anchorvpn_be ~/Documents/Access/cursor/BACKUP_deployment_key_$(date +%Y%m%d)

# Encrypt backup (recommended)
gpg -c ~/Documents/Access/cursor/BACKUP_deployment_key_$(date +%Y%m%d)
```

---

## 📚 Related Documentation

- **Deployment Guide**: `7_DEBIAN_DEPLOYMENT_GUIDE.md`
- **Quick Deploy**: `8_QUICK_DEPLOY_GUIDE.md`
- **Deployment Scripts**: `10_DEPLOYMENT_SCRIPTS_README.md`
- **Master Index**: `0_DOCUMENTATION_INDEX.md`

---

## ✅ Verification Checklist

Before proceeding with deployment, ensure:

- [ ] SSH key copied to server (`~/.ssh/deployment_key`)
- [ ] Key permissions set to 600
- [ ] SSH config created with GitHub settings
- [ ] SSH connection test successful (`ssh -T git@github.com`)
- [ ] Repository cloned successfully
- [ ] Git operations work (pull, status, etc.)

---

## 🆘 Quick Reference

### Key Locations

| Location | Purpose |
|----------|---------|
| Local: `~/Documents/Access/cursor/deployment_key_anchorvpn_be` | Original deployment key |
| Server: `~/.ssh/deployment_key` | Deployed key on server |
| Server: `~/.ssh/config` | SSH configuration |
| Server: `~/.ssh/known_hosts` | Verified host keys |

### Common Commands

```bash
# Test SSH
ssh -T git@github.com

# Clone repo
git clone git@github.com:yourusername/connectme.git

# Pull updates
git pull origin main

# Check remote URL
git remote -v

# Change to SSH URL
git remote set-url origin git@github.com:yourusername/connectme.git
```

---

**Last Updated**: October 7, 2025  
**Status**: ✅ Ready to Use

