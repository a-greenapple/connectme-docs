# 🚀 Quick Deploy to Debian Server

**Time Required**: 30-45 minutes  
**Difficulty**: Moderate (automated script does most work)

---

## Prerequisites

✅ Debian 11 or 12 server with public IP  
✅ Domain name with DNS configured (A records)  
✅ SSH access to server  
✅ UHC API credentials  
✅ Keycloak realm configured

---

## Step 1: Upload Code to Server

From your local machine:

```bash
# Option A: Using rsync (recommended)
rsync -avz --exclude='node_modules' --exclude='venv' --exclude='.git' \
    /Users/ssiva/Documents/1_Data/AI/abce/connectme/ \
    user@your-server-ip:/var/www/connectme/

# Option B: Using Git
# First push your code to GitHub/GitLab, then on server:
ssh user@your-server-ip
cd /var/www
sudo mkdir -p connectme && sudo chown $USER:$USER connectme
git clone https://github.com/yourusername/connectme.git
```

---

## Step 2: Run Automated Setup

SSH into your server and run:

```bash
ssh user@your-server-ip

# Navigate to project
cd /var/www/connectme

# Make script executable
chmod +x deploy/debian-setup.sh

# Run setup (will ask for domain names)
sudo ./deploy/debian-setup.sh
```

The script will ask for:
- **Main domain**: e.g., `connectme.yourdomain.com`
- **API domain**: e.g., `api.connectme.yourdomain.com`
- **Email**: For SSL certificates

---

## Step 3: Configure Credentials

Edit the backend environment file:

```bash
sudo nano /var/www/connectme/backend/.env
```

Update these values:

```env
# Keycloak
KEYCLOAK_CLIENT_SECRET=your-actual-keycloak-backend-secret
KEYCLOAK_PUBLIC_KEY=your-actual-realm-public-key

# UHC API
UHC_API_KEY=your-actual-uhc-api-key
UHC_CLIENT_ID=your-actual-uhc-client-id
UHC_CLIENT_SECRET=your-actual-uhc-client-secret
```

Save and exit (Ctrl+X, then Y, then Enter).

---

## Step 4: Create Admin User

```bash
cd /var/www/connectme/backend
source venv/bin/activate
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: your-email@example.com
# Password: (create strong password)
```

---

## Step 5: Restart Services

```bash
sudo systemctl restart connectme-backend
sudo systemctl restart connectme-frontend
sudo systemctl restart connectme-celery

# Check status
sudo systemctl status connectme-backend
sudo systemctl status connectme-frontend
```

---

## Step 6: Test Deployment

### Test Backend API

```bash
curl https://api.connectme.yourdomain.com/admin/
# Should return HTML (Django admin login page)
```

### Test Frontend

Open browser:
```
https://connectme.yourdomain.com
```

Should see the Keycloak login page.

### Test UHC Connection

```bash
cd /var/www/connectme/backend
source venv/bin/activate
python manage.py shell
```

```python
import requests
response = requests.get('https://apimarketplace.uhc.com')
print(response.status_code)  # Should work (200 or 301)
exit()
```

---

## ✅ Success Checklist

- [ ] Backend API accessible at https://api.connectme.yourdomain.com/admin/
- [ ] Frontend accessible at https://connectme.yourdomain.com
- [ ] SSL certificates show valid (green padlock)
- [ ] Can login with Keycloak
- [ ] Claims search works without DNS errors
- [ ] No CORS errors in browser console

---

## 🔧 Common Issues & Fixes

### Issue: "Connection refused" on frontend

```bash
# Check if frontend is running
sudo systemctl status connectme-frontend

# View logs
sudo journalctl -u connectme-frontend -f

# Restart
sudo systemctl restart connectme-frontend
```

### Issue: "500 Internal Server Error" on backend

```bash
# Check backend logs
sudo tail -100 /var/log/connectme/backend-error.log

# Common fix: missing environment variables
sudo nano /var/www/connectme/backend/.env

# Restart backend
sudo systemctl restart connectme-backend
```

### Issue: SSL certificate errors

```bash
# Check certificate
sudo certbot certificates

# Renew if needed
sudo certbot renew --force-renewal

# Restart Nginx
sudo systemctl restart nginx
```

### Issue: Can't reach UHC API

```bash
# Test DNS
nslookup apimarketplace.uhc.com

# Test connection
curl -v https://apimarketplace.uhc.com

# If fails, check firewall
sudo ufw status
```

---

## 📊 Monitoring Commands

```bash
# Check all services
sudo systemctl status connectme-backend connectme-frontend connectme-celery

# View backend logs
sudo tail -f /var/log/connectme/backend-error.log

# View frontend logs
sudo tail -f /var/log/connectme/frontend.log

# View Nginx access logs
sudo tail -f /var/log/nginx/connectme.access.log

# Check disk space
df -h

# Check memory
free -h

# Check processes
ps aux | grep python
ps aux | grep node
```

---

## 🔐 Security Notes

After deployment:

1. **Change all default passwords**
2. **Set up regular backups**:
   ```bash
   sudo crontab -e
   # Add: 0 2 * * * /usr/local/bin/backup-connectme-db.sh
   ```
3. **Enable fail2ban** (optional but recommended):
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```
4. **Regular updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## 📚 Additional Resources

- Full guide: `/var/www/connectme/DEBIAN_DEPLOYMENT_GUIDE.md`
- Logs directory: `/var/log/connectme/`
- Service files: `/etc/systemd/system/connectme-*.service`
- Nginx config: `/etc/nginx/sites-available/connectme`

---

## 🆘 Need Help?

1. Check logs: `sudo journalctl -u connectme-backend -f`
2. Review full deployment guide: `DEBIAN_DEPLOYMENT_GUIDE.md`
3. Test individual components (Python, Node.js, PostgreSQL, Redis)
4. Verify environment variables in `.env` files

---

**Next**: After successful deployment, configure Keycloak users and test claims search!

**Estimated Total Time**: 30-45 minutes
**Status**: ✅ Ready to deploy

