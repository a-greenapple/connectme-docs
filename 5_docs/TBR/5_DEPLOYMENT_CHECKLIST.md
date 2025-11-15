# 🚀 ConnectMe Deployment Checklist

**Last Updated**: October 13, 2025

Use this checklist before every deployment to ensure a smooth release.

---

## Pre-Deployment

### Code Quality
- [ ] All new code has been reviewed
- [ ] No commented-out code or debug statements
- [ ] Environment variables are properly set
- [ ] Secrets are not hardcoded

### Testing
- [ ] All unit tests pass locally
- [ ] All integration tests pass
- [ ] E2E tests pass for critical flows
- [ ] Manual testing completed for new features
- [ ] Regression testing performed

### Configuration
- [ ] `.env.production` is up to date on server
- [ ] Database migrations are ready
- [ ] Static files are generated
- [ ] ALLOWED_HOSTS includes production domains

### Documentation
- [ ] README is updated
- [ ] API documentation is current
- [ ] Changelog is updated
- [ ] Deployment notes prepared

---

## Deployment Process

### 1. Backend Deployment

```bash
# SSH to server
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

# Navigate to backend
cd /var/www/connectme-backend

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart connectme-backend
sudo systemctl restart celery
```

### 2. Frontend Deployment

```bash
# On server
cd /var/www/connectme-frontend

# Pull latest code
git pull origin main

# Install dependencies
npm ci --legacy-peer-deps

# Build
npm run build

# Restart PM2
pm2 restart connectme-frontend
```

### 3. Post-Deployment Checks

```bash
# Check service status
sudo systemctl status connectme-backend
sudo systemctl status celery
pm2 status

# Run health check
./health-check-monitor.sh

# Check logs
sudo journalctl -u connectme-backend -n 50
tail -50 /var/log/celery/celery.service.log
pm2 logs connectme-frontend --lines 50
```

---

## Post-Deployment Verification

### Manual Tests
- [ ] Can access frontend (https://connectme.apps.totesoft.com)
- [ ] Can log in with test account
- [ ] Claims search works
- [ ] Bulk upload works
- [ ] Results display correctly
- [ ] Log viewer accessible

### Automated Tests
- [ ] Health check passes
- [ ] API integration tests pass
- [ ] E2E smoke tests pass

### Monitoring
- [ ] Check error logs for new issues
- [ ] Monitor response times
- [ ] Verify SSL certificates
- [ ] Check database connections

---

## Rollback Plan

If deployment fails:

```bash
# Backend rollback
cd /var/www/connectme-backend
git reset --hard <previous-commit-sha>
python manage.py migrate
sudo systemctl restart connectme-backend

# Frontend rollback
cd /var/www/connectme-frontend
git reset --hard <previous-commit-sha>
npm run build
pm2 restart connectme-frontend
```

---

## Emergency Contacts

- **Server Issues**: Check logs and restart services
- **Database Issues**: Verify connections and migrations
- **Frontend Issues**: Check PM2 logs and rebuild
- **API Issues**: Check backend logs and Celery status

---

## Common Issues & Fixes

### Issue: "DisallowedHost" Error
**Fix**: Add domain to `ALLOWED_HOSTS` in `.env`

### Issue: Frontend shows "load failed"
**Fix**: Check `NEXT_PUBLIC_API_BASE_URL` in `.env.production`

### Issue: 403 Forbidden on API calls
**Fix**: Verify authentication and permissions

### Issue: Celery tasks not processing
**Fix**: `sudo systemctl restart celery`

---

**Always test in a staging environment first!** 🛡️

