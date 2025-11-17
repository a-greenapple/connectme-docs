# 🧪 ConnectMe Testing Strategy & Documentation

**Last Updated**: October 13, 2025  
**Status**: ✅ Fully Implemented

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Testing Pyramid](#testing-pyramid)
3. [Test Types](#test-types)
4. [Running Tests](#running-tests)
5. [CI/CD Integration](#cicd-integration)
6. [Automated Monitoring](#automated-monitoring)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

ConnectMe implements a comprehensive testing strategy with multiple layers:

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test API endpoints and workflows
- **E2E Tests**: Test complete user journeys
- **Health Checks**: Monitor system health in production

### Testing Stack

**Frontend:**
- Jest for unit tests
- React Testing Library for component tests
- Playwright for E2E browser tests
- MSW for API mocking (installed, optional)

**Backend:**
- Pytest for unit & integration tests
- Django test framework
- Requests library for API testing

**Monitoring:**
- Custom health check script
- Django log viewer
- GitHub Actions for CI/CD

---

## 🔺 Testing Pyramid

```
                    /\
                   /  \
                  / E2E \          ← Few, comprehensive user flows
                 /--------\
                /   API    \       ← Medium, test all endpoints
               /  Integration\
              /--------------\
             /   Unit Tests   \    ← Many, fast, isolated
            /------------------\
```

### Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All critical API endpoints
- **E2E Tests**: All major user workflows

---

## 🧩 Test Types

### 1. Frontend Unit Tests

**Location**: `connectme-frontend/src/**/__tests__/`

**Framework**: Jest + React Testing Library

**Example**:
```typescript
import { render, screen } from '@testing-library/react'
import BulkUploadPage from '../page'

test('renders upload area', () => {
  render(<BulkUploadPage />)
  expect(screen.getByText(/upload/i)).toBeInTheDocument()
})
```

**Run**:
```bash
cd connectme-frontend
npm test                    # Run all tests
npm run test:watch         # Watch mode
npm run test:coverage      # With coverage report
```

---

### 2. Frontend E2E Tests

**Location**: `connectme-frontend/e2e/`

**Framework**: Playwright

**Test Files**:
- `01-login.spec.ts` - Authentication flow
- `02-claims-search.spec.ts` - Claims search functionality
- `03-bulk-upload.spec.ts` - CSV upload workflow

**Run**:
```bash
cd connectme-frontend

# Install browsers (first time only)
npm run playwright:install

# Run tests
npm run test:e2e           # Headless mode
npm run test:e2e:headed    # See browser
npm run test:e2e:ui        # Interactive UI mode
npm run test:e2e:debug     # Debug mode

# View report
npm run test:e2e:report
```

**Configuration**: `playwright.config.ts`

---

### 3. Backend Unit Tests

**Location**: `connectme-backend/apps/*/tests/`

**Framework**: Django Test Framework

**Run**:
```bash
cd connectme-backend
source venv/bin/activate

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.claims
python manage.py test apps.users

# With coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

### 4. Backend API Integration Tests

**Location**: `connectme-backend/tests/test_api_integration.py`

**Framework**: Pytest + Requests

**Tests**:
- Health check endpoints
- Authentication flow
- Claims search API
- Bulk upload API
- CORS configuration
- Environment verification

**Run**:
```bash
cd connectme-backend
source venv/bin/activate

pip install pytest requests

# Run all API tests
pytest tests/test_api_integration.py -v

# Run specific test class
pytest tests/test_api_integration.py::TestHealthEndpoints -v

# Run with detailed output
pytest tests/test_api_integration.py -v --tb=short
```

---

### 5. Health Check Monitoring

**Location**: `health-check-monitor.sh`

**Purpose**: Automated system health monitoring

**Checks**:
- ✅ Backend health endpoint
- ✅ Database connection
- ✅ Frontend accessibility
- ✅ API endpoints (status codes)
- ✅ SSL certificate validity
- ✅ Response times

**Run Manually**:
```bash
./health-check-monitor.sh
```

**Run with Alerts** (optional):
```bash
# Email alerts
ALERT_EMAIL="admin@example.com" ./health-check-monitor.sh

# Slack alerts
SLACK_WEBHOOK="https://hooks.slack.com/..." ./health-check-monitor.sh
```

**Schedule with Cron** (every 5 minutes):
```bash
*/5 * * * * /path/to/health-check-monitor.sh
```

---

## 🚀 Running Tests

### Quick Test Commands

**Run Everything Locally**:
```bash
# Frontend
cd connectme-frontend
npm test && npm run test:e2e

# Backend
cd connectme-backend
python manage.py test && pytest tests/test_api_integration.py -v

# Health check
./health-check-monitor.sh
```

**Production Verification**:
```bash
# After deployment, verify system health
./health-check-monitor.sh

# Run API integration tests against production
cd connectme-backend
pytest tests/test_api_integration.py -v
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/deploy.yml`

**Pipeline**:
```
1. Test Backend
   ├─ Linting (flake8)
   ├─ Unit tests (Django)
   ├─ API integration tests (Pytest)
   └─ Migration checks

2. Test Frontend
   ├─ Linting (ESLint)
   ├─ Unit tests (Jest)
   ├─ E2E tests (Playwright)
   └─ Build verification

3. Deploy (if tests pass)
   ├─ Deploy backend
   ├─ Deploy frontend
   ├─ Health checks
   └─ Smoke tests
```

**Triggers**:
- Push to `main` branch
- Manual trigger via GitHub Actions UI

**Required Secrets**:
```bash
PRODUCTION_HOST=20.84.160.240
PRODUCTION_USER=connectme
SSH_PRIVATE_KEY=<your-ssh-key>
```

---

## 📊 Automated Monitoring

### Log Viewer

**URL**: https://connectme.be.totesoft.com/logs/

**Features**:
- Real-time log viewing
- Filter by log level (INFO, WARNING, ERROR)
- Search functionality
- Download logs

### Manual Log Access

```bash
# Backend logs (real-time)
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -f"

# Celery logs
ssh connectme@20.84.160.240 "tail -f /var/log/celery/celery.service.log"

# Recent errors
ssh connectme@20.84.160.240 "sudo journalctl --since '1 hour ago' | grep -i error"
```

---

## ✅ Best Practices

### 1. Test Naming Conventions

```typescript
// Good
test('should display error message when login fails')
test('should upload CSV and show in history')

// Bad
test('test1')
test('it works')
```

### 2. Test Independence

Each test should:
- Set up its own data
- Clean up after itself
- Not depend on other tests
- Run in any order

### 3. Mock External Services

```typescript
// Mock UHC API calls
beforeEach(() => {
  global.fetch = jest.fn()
})
```

### 4. Use Descriptive Assertions

```typescript
// Good
expect(claimNumber).toBe('ZE59426195')
expect(response.status).toBe(200)

// Bad
expect(x).toBeTruthy()
```

### 5. Test Edge Cases

- Empty inputs
- Invalid data
- Network errors
- Authentication failures
- Large datasets

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Playwright Browser Installation Fails**

```bash
# Solution: Install with dependencies
npx playwright install --with-deps

# Or system-specific
npx playwright install-deps
```

#### 2. **Jest Tests Fail with "TextEncoder not defined"**

✅ Already fixed with `jest.polyfills.js`

#### 3. **E2E Tests Timeout**

```bash
# Increase timeout in playwright.config.ts
timeout: 60000  // 60 seconds
```

#### 4. **API Integration Tests Fail**

Check:
- Backend is running and accessible
- Authentication credentials are correct
- Network connectivity to production

#### 5. **Health Check Fails**

```bash
# Debug with verbose output
bash -x ./health-check-monitor.sh

# Check individual endpoints
curl -v https://connectme.be.totesoft.com/health/
```

---

## 📈 Test Coverage

### View Coverage Reports

**Frontend**:
```bash
cd connectme-frontend
npm run test:coverage
open coverage/lcov-report/index.html
```

**Backend**:
```bash
cd connectme-backend
coverage run --source='.' manage.py test
coverage html
open htmlcov/index.html
```

---

## 🎯 Testing Checklist

Before deploying to production:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] E2E tests pass for critical flows
- [ ] Health check script passes
- [ ] No linting errors
- [ ] Coverage meets thresholds
- [ ] Manual smoke test performed
- [ ] Logs checked for errors

---

## 📚 Additional Resources

### Documentation
- [Playwright Docs](https://playwright.dev)
- [Jest Docs](https://jestjs.io)
- [Pytest Docs](https://docs.pytest.org)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)

### Test Examples
- Frontend: `connectme-frontend/src/**/__tests__/`
- Backend: `connectme-backend/apps/*/tests/`
- E2E: `connectme-frontend/e2e/`
- API: `connectme-backend/tests/test_api_integration.py`

### Getting Help

1. Check test output and error messages
2. Review logs at https://connectme.be.totesoft.com/logs/
3. Run health check script for system status
4. Check CI/CD pipeline in GitHub Actions

---

## 🚀 Quick Reference

```bash
# Frontend Tests
npm test                    # Unit tests
npm run test:e2e           # E2E tests
npm run test:all           # All tests

# Backend Tests
python manage.py test      # Unit tests
pytest tests/ -v           # Integration tests

# Health Check
./health-check-monitor.sh  # System health

# View Logs
# https://connectme.be.totesoft.com/logs/

# CI/CD
# Push to main → Automatic testing & deployment
```

---

**Testing is not just about finding bugs—it's about confidence in your code!** 🎯

