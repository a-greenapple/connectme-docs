# ⚡ Quick Start: Testing ConnectMe

Get up and running with testing in 5 minutes!

---

## 🎯 For Developers

### 1. Run All Tests Locally (2 minutes)

```bash
# Clone and setup (if needed)
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# Frontend tests
cd connectme-frontend
npm install --legacy-peer-deps
npm test                    # Unit tests (7 tests)
npm run test:e2e           # E2E tests (requires running app)

# Backend tests
cd ../connectme-backend
source venv/bin/activate
python manage.py test      # Unit tests
pytest tests/test_api_integration.py -v  # API tests (11 tests)
```

### 2. Quick Verification (30 seconds)

```bash
# Health check
./health-check-monitor.sh

# Or just check endpoints
curl https://connectme.be.totesoft.com/health/
curl https://connectme.apps.totesoft.com
```

---

## 📱 For QA/Testers

### Manual Test Checklist (5 minutes)

1. **Login**
   - Go to: https://connectme.apps.totesoft.com
   - Login with: `test.analyst` / `ConnectMe2025!`
   - ✅ Should redirect to dashboard

2. **Claims Search**
   - Fill date range (last 30 days)
   - Click Search
   - ✅ Should show results or "no data"

3. **Bulk Upload**
   - Navigate to Bulk Upload
   - Upload CSV file
   - ✅ Should process and show results in table

4. **View Logs**
   - Go to: https://connectme.be.totesoft.com/logs/
   - ✅ Should display log viewer

---

## 🚀 For DevOps

### Production Health Check (1 minute)

```bash
# Quick check
./health-check-monitor.sh

# Detailed check with logs
ssh connectme@20.84.160.240 << 'EOF'
  echo "=== Service Status ==="
  sudo systemctl status connectme-backend --no-pager | head -5
  sudo systemctl status celery --no-pager | head -5
  pm2 status
  
  echo -e "\n=== Recent Errors ==="
  sudo journalctl --since '10 minutes ago' | grep -i error | tail -5
EOF
```

### Run Smoke Tests After Deployment

```bash
cd connectme-backend
pytest tests/test_api_integration.py -v -k "test_health_check or test_mock_login"
```

---

## 🔄 Automated Testing (CI/CD)

### GitHub Actions runs automatically on every push to `main`:

1. ✅ Backend linting & tests
2. ✅ Frontend linting & tests
3. ✅ E2E tests (Playwright)
4. ✅ Build verification
5. ✅ Deploy to production
6. ✅ Health checks
7. ✅ Smoke tests

**View results**: https://github.com/a-greenapple/connectme-frontend/actions

---

## 🎯 Test Coverage Summary

| Component | Tests | Status |
|-----------|-------|--------|
| Frontend Unit | 7 tests | ✅ All passing |
| Frontend E2E | 15+ scenarios | ✅ Configured |
| Backend API | 11 tests | ✅ All passing |
| Health Checks | 7 checks | ✅ Active |

---

## 📊 View Test Reports

**Frontend Coverage**:
```bash
cd connectme-frontend
npm run test:coverage
open coverage/lcov-report/index.html
```

**E2E Test Report**:
```bash
cd connectme-frontend
npm run test:e2e:report
```

**Backend Coverage**:
```bash
cd connectme-backend
coverage run --source='.' manage.py test
coverage html
open htmlcov/index.html
```

---

## 🆘 Quick Troubleshooting

### Problem: Tests fail locally
```bash
# Clean and reinstall
cd connectme-frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm test
```

### Problem: E2E tests timeout
```bash
# Run in headed mode to see what's happening
npm run test:e2e:headed
```

### Problem: API tests fail
```bash
# Check backend is accessible
curl -v https://connectme.be.totesoft.com/health/

# Check authentication
curl -X POST https://connectme.be.totesoft.com/api/v1/auth/mock/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test.analyst","password":"ConnectMe2025!"}'
```

---

## 🎓 Learn More

- Full documentation: `4_TESTING_STRATEGY.md`
- Deployment guide: `5_DEPLOYMENT_CHECKLIST.md`
- CI/CD config: `.github/workflows/deploy.yml`

---

**Remember: Tests are your safety net. Run them often!** 🛡️

