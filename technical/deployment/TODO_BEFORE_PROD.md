# TODO Before Production Deployment

**Created**: November 15, 2025  
**Status**: Pre-Production Environment Active  
**Target**: Production Deployment (Future)

---

## ✅ Completed (Pre-Prod)

### 1. Pagination Fix for UHC Claims API
- **Issue**: Status filter was missing claims beyond first 50 results
- **Fix**: Added pagination loop to fetch all pages (up to 500 claims)
- **Commit**: `4ab8693` - "Fix: Add pagination support for UHC Summary API"
- **Deployed**: November 15, 2025 to Pre-Prod
- **Status**: ✅ Live in Pre-Prod

---

## 🔴 CRITICAL - Must Complete Before Production

### 1. Set Up CI/CD Pipeline (GitHub Actions)

#### Current State
- ❌ Backend: Placeholder workflow exists but not functional
- ❌ Frontend: No CI/CD workflows at all
- ❌ GitHub CLI: Token expired (account: ishanku)

#### Required Actions

##### A. Backend CI/CD Setup
**File**: `connectme-backend/.github/workflows/deploy-preprod.yml`

1. **Configure GitHub Secrets** (in repository settings):
   ```
   PREPROD_HOST=169.59.163.43
   PREPROD_USER=connectme
   PREPROD_SSH_KEY=<private SSH key for connectme@169.59.163.43>
   PROD_HOST=<production server IP>
   PROD_USER=<production server user>
   PROD_SSH_KEY=<production SSH key>
   ```

2. **Activate Deployment Steps** (currently commented out in lines 26-42):
   - Uncomment SSH deployment action
   - Test with pre-prod first
   - Add production workflow with approval gate

3. **Add Health Checks**:
   - Verify service started successfully
   - Check `/health/` endpoint returns 200
   - Rollback on failure

##### B. Frontend CI/CD Setup
**Create**: `connectme-frontend/.github/workflows/deploy-preprod.yml`

1. **Create workflow file**:
   ```yaml
   name: Deploy Frontend Pre-Prod
   on:
     push:
       branches: [ main ]
     workflow_dispatch:
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Deploy to Pre-Prod
           uses: appleboy/ssh-action@v1.0.3
           with:
             host: ${{ secrets.PREPROD_HOST }}
             username: ${{ secrets.PREPROD_USER }}
             key: ${{ secrets.PREPROD_SSH_KEY }}
             script: |
               cd /var/www/connectme-preprod-frontend
               git pull origin main
               npm install
               npm run build
               pm2 restart connectme-preprod-frontend
         - name: Health Check
           run: |
             sleep 10
             curl -f https://pre-prod.connectme.apps.totessoft.com || exit 1
   ```

2. **Create production workflow** with manual approval

##### C. Fix GitHub CLI Authentication
```bash
gh auth login -h github.com
# Follow prompts to re-authenticate
gh auth status  # Verify
```

##### D. Automated Testing in CI/CD
1. **Add test stage before deployment**:
   - Run Django tests (`python manage.py test`)
   - Run frontend tests (`npm test`)
   - Linting checks
   - Security scans

2. **Add smoke tests after deployment**:
   - Health check endpoints
   - Critical API endpoints
   - Frontend loads successfully

##### E. Deployment Approval Gates (Production Only)
1. **Require manual approval** for production deployments
2. **Add deployment notifications** (Slack/Email)
3. **Implement rollback mechanism**

---

## 📋 Testing Requirements Before Prod

### 1. Pagination Fix Testing
- [ ] Test with date range returning >50 claims
- [ ] Test with date range returning >100 claims
- [ ] Verify all DENIED claims are found across multiple pages
- [ ] Test with different status filters (PAID, PENDING, etc.)
- [ ] Verify performance with max 500 claims

### 2. Full Regression Testing
- [ ] User authentication (Keycloak)
- [ ] Role-based access control
- [ ] Claims search (all scenarios)
- [ ] Bulk upload
- [ ] User management
- [ ] Monitoring dashboard
- [ ] Logs viewer

### 3. Performance Testing
- [ ] Load testing with concurrent users
- [ ] API response times under load
- [ ] Database query optimization
- [ ] Frontend bundle size optimization

### 4. Security Audit
- [ ] Penetration testing
- [ ] HIPAA compliance review
- [ ] Secrets management audit
- [ ] SSL/TLS configuration
- [ ] CORS policy review

---

## 🚀 Production Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] CI/CD fully configured and tested
- [ ] Backup strategy in place
- [ ] Rollback plan documented
- [ ] Monitoring/alerting configured
- [ ] Documentation updated

### Deployment Day
- [ ] Database backup
- [ ] Deploy during maintenance window
- [ ] Monitor logs in real-time
- [ ] Verify health checks
- [ ] Smoke test critical features
- [ ] Notify stakeholders

### Post-Deployment
- [ ] Monitor for 24 hours
- [ ] Check error rates
- [ ] Verify performance metrics
- [ ] User acceptance testing
- [ ] Document any issues

---

## 📞 Contacts & Resources

### GitHub Repositories
- Backend: https://github.com/a-greenapple/connectme-backend
- Frontend: https://github.com/a-greenapple/connectme-frontend

### Servers
- **Pre-Prod**: 169.59.163.43 (connectme@)
  - Backend: https://pre-prod.connectme.be.totessoft.com
  - Frontend: https://pre-prod.connectme.apps.totessoft.com
- **Production**: TBD

### Key Files
- Backend workflow: `.github/workflows/deploy-preprod.yml`
- Backend service: `/etc/systemd/system/connectme-preprod-backend.service`
- Frontend PM2: `pm2 list` (connectme-preprod-frontend)

---

## 📝 Notes

### Current Manual Deployment Process
```bash
# Backend
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
git pull origin main
sudo systemctl restart connectme-preprod-backend

# Frontend
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-frontend
git pull origin main
npm install
npm run build
pm2 restart connectme-preprod-frontend
```

### Known Issues
1. GitHub CLI token expired (needs re-authentication)
2. CI/CD workflows are placeholders only
3. No automated testing in deployment pipeline
4. No rollback mechanism configured

---

**Last Updated**: November 15, 2025  
**Next Review**: Before production deployment planning

