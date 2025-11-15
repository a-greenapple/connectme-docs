# 🔧 Bulk Upload Fixes & Monitoring System

## 📋 Overview

This document covers:
1. ✅ **Bulk Upload Fixes** - Resolved date range issues and failures
2. ✅ **Job Cancellation** - Added ability to cancel running/stuck jobs
3. ⏳ **Monitoring System** - Enhanced admin panel with logs, stats, and schedulers
4. ⏳ **Playwright Testing** - E2E testing setup and instructions

---

## 1. ✅ Bulk Upload Fixes

### Problem
- All bulk uploads were failing with "Claim not found in date range"
- Jobs taking 77k+ seconds (21+ hours!) were stuck
- No way to cancel stuck jobs

### Root Cause
- UHC API requires exact date ranges when claims were processed
- If dates don't match, claims won't be found
- No cancellation mechanism for long-running jobs

### Solution Implemented

#### A. Flexible Date Range Handling
```python
# connectme-backend/apps/claims/tasks.py

def batch_query_claims(engine, csv_data, start_date, end_date):
    try:
        # Try with dates first
        batch_result = engine.execute({
            'firstServiceDate': start_date,
            'lastServiceDate': end_date,
        })
    except Exception as date_error:
        logger.warning(f"⚠️ Batch query with dates failed: {date_error}")
        logger.info(f"🔄 Retrying without date constraints...")
        # Fallback: Try without dates (may return more results)
        batch_result = engine.execute({})
```

**Benefits**:
- ✅ Tries with dates first (faster, more precise)
- ✅ Falls back to no-date query if dates don't work
- ✅ Handles both scenarios gracefully

#### B. Job Cancellation System

**Database Changes**:
```python
# New fields in CSVJob model
cancelled_at = models.DateTimeField(null=True, blank=True)
cancelled_by = models.ForeignKey(User, ...)
status = 'CANCELLING' | 'CANCELLED'  # New statuses
```

**Backend Endpoint**:
```python
# POST /api/v1/claims/csv-jobs/{id}/cancel/

@action(detail=True, methods=['post'])
def cancel(self, request, pk=None):
    job.status = 'CANCELLING'
    job.cancelled_at = timezone.now()
    job.cancelled_by = request.user
    job.save()
    
    # Revoke Celery task
    current_app.control.revoke(job.celery_task_id, terminate=True)
```

**Task Cancellation Checks**:
```python
# Check every 5 rows
if job and i % 5 == 0:
    job.refresh_from_db()
    if job.status == 'CANCELLING':
        logger.warning(f"🛑 Job cancelled by user")
        job.status = 'CANCELLED'
        job.save()
        raise Exception("Job cancelled by user")
```

**Frontend UI**:
```typescript
// Cancel button for PENDING/PROCESSING jobs
{(job.status === 'PENDING' || job.status === 'PROCESSING') && (
  <button onClick={() => cancelJob(job.id)}>
    <XCircle /> Cancel
  </button>
)}
```

---

## 2. ✅ Job Cancellation Features

### User Flow
1. User uploads CSV → Job starts processing
2. User sees job stuck or taking too long
3. User clicks **"Cancel"** button
4. System:
   - Marks job as `CANCELLING`
   - Revokes Celery task
   - Task checks status every 5 rows
   - Stops processing and marks as `CANCELLED`

### Status Flow
```
PENDING → PROCESSING → CANCELLING → CANCELLED
                    ↓
                COMPLETED / FAILED
```

### UI Indicators
- **PENDING**: Clock icon (gray)
- **PROCESSING**: Spinner (blue)
- **CANCELLING**: Pulsing clock (yellow)
- **CANCELLED**: X icon (gray)
- **COMPLETED**: Check icon (green)
- **FAILED**: X icon (red)

---

## 3. ⏳ Enhanced Monitoring System (Next Step)

### Planned Features

#### A. Monitoring Submenu
```
Admin Panel
├── Dashboard
├── Monitoring ⭐ NEW
│   ├── Logs
│   ├── System Stats
│   ├── Schedulers
│   └── Health Checks
├── Users
└── Claims
```

#### B. System Stats Page
- **Active Jobs**: Count of PENDING/PROCESSING jobs
- **Completed Today**: Success rate
- **Failed Jobs**: Error breakdown
- **Average Processing Time**: Per job
- **Celery Workers**: Status and queue length
- **Database Stats**: Connections, queries/sec
- **API Response Times**: P50, P95, P99

#### C. Schedulers (Celery Beat)
Automated maintenance tasks:

**1. Cleanup Old Sessions**
```python
@periodic_task(run_every=crontab(hour=2, minute=0))
def cleanup_old_sessions():
    """Delete sessions older than 30 days"""
    cutoff = timezone.now() - timedelta(days=30)
    Session.objects.filter(expire_date__lt=cutoff).delete()
```

**2. Cleanup Stuck Jobs**
```python
@periodic_task(run_every=crontab(minute='*/15'))
def cleanup_stuck_jobs():
    """Mark jobs stuck for > 2 hours as FAILED"""
    cutoff = timezone.now() - timedelta(hours=2)
    stuck_jobs = CSVJob.objects.filter(
        status='PROCESSING',
        processing_started_at__lt=cutoff
    )
    for job in stuck_jobs:
        job.status = 'FAILED'
        job.error_log = [{'error': 'Job timed out after 2 hours'}]
        job.save()
```

**3. Archive Old Results**
```python
@periodic_task(run_every=crontab(hour=3, minute=0))
def archive_old_results():
    """Archive CSV results older than 90 days"""
    cutoff = timezone.now() - timedelta(days=90)
    old_jobs = CSVJob.objects.filter(
        created_at__lt=cutoff,
        status='COMPLETED'
    )
    # Move to archive storage
```

**4. Health Check Alerts**
```python
@periodic_task(run_every=crontab(minute='*/5'))
def health_check_alert():
    """Alert if system is unhealthy"""
    if not check_database_connection():
        send_alert("Database connection failed")
    if not check_celery_workers():
        send_alert("No Celery workers available")
```

#### D. Scheduler Management UI
```
Schedulers Dashboard
┌─────────────────────────────────────────────────────────────┐
│ Task Name              | Status  | Last Run    | Next Run   │
├─────────────────────────────────────────────────────────────┤
│ cleanup_old_sessions   | ✅ OK   | 2h ago      | 22h        │
│ cleanup_stuck_jobs     | ✅ OK   | 5m ago      | 10m        │
│ archive_old_results    | ✅ OK   | 1h ago      | 23h        │
│ health_check_alert     | ⚠️ WARN | 2m ago      | 3m         │
└─────────────────────────────────────────────────────────────┘

Actions: [Run Now] [Disable] [View Logs] [Configure]
```

---

## 4. ⏳ Playwright Testing Setup

### Installation
```bash
cd connectme-frontend
npm install --save-dev @playwright/test
npx playwright install
```

### Configuration
```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'https://connectme.apps.totesoft.com',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
})
```

### Test Examples

#### Bulk Upload Test
```typescript
// e2e/bulk-upload.spec.ts
test('should upload CSV and cancel job', async ({ page }) => {
  await page.goto('/bulk-upload')
  
  // Upload file
  await page.setInputFiles('input[type="file"]', 'test.csv')
  await page.click('text=Upload and Process')
  
  // Wait for job to appear
  await page.waitForSelector('text=PROCESSING')
  
  // Cancel job
  await page.click('button:has-text("Cancel")')
  
  // Verify cancellation
  await expect(page.locator('text=CANCELLED')).toBeVisible()
})
```

#### Claims Search Test
```typescript
// e2e/claims-search.spec.ts
test('should search claims successfully', async ({ page }) => {
  await page.goto('/claims')
  
  // Fill search form
  await page.fill('[name="claimNumber"]', 'FG53171076')
  await page.fill('[name="startDate"]', '2025-01-01')
  await page.fill('[name="endDate"]', '2025-12-31')
  
  // Submit search
  await page.click('button:has-text("Search")')
  
  // Verify results
  await expect(page.locator('text=FG53171076')).toBeVisible()
})
```

### Running Tests
```bash
# Run all tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run specific browser
npx playwright test --project=chromium

# Run specific test
npx playwright test e2e/bulk-upload.spec.ts

# Debug mode
npx playwright test --debug

# Generate report
npx playwright show-report
```

### CI/CD Integration
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run tests
        run: npm run test:e2e
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 5. 📊 Monitoring Dashboard Design

### Logs Page (Enhanced)
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 System Logs                                              │
├─────────────────────────────────────────────────────────────┤
│ Service: [Backend ▼] [Celery] [Nginx]                      │
│ Level:   [All ▼] [ERROR] [WARNING] [INFO]                  │
│ Lines:   [100 ▼] [500] [1000] [All]                        │
│ Search:  [________________]  [🔍 Filter]  [↻ Auto-refresh] │
├─────────────────────────────────────────────────────────────┤
│ [2025-10-13 14:30:15] INFO  - Job started: abc123          │
│ [2025-10-13 14:30:20] WARN  - Batch query failed, retrying │
│ [2025-10-13 14:30:25] INFO  - Job completed: abc123        │
└─────────────────────────────────────────────────────────────┘
```

### Stats Page
```
┌─────────────────────────────────────────────────────────────┐
│ 📈 System Statistics                                        │
├─────────────────────────────────────────────────────────────┤
│ Jobs Today                                                  │
│ ├─ Total: 127                                               │
│ ├─ Completed: 98 (77%)                                      │
│ ├─ Failed: 15 (12%)                                         │
│ ├─ Cancelled: 8 (6%)                                        │
│ └─ Processing: 6 (5%)                                       │
│                                                             │
│ Performance                                                 │
│ ├─ Avg Processing Time: 12.3s                               │
│ ├─ P95 Processing Time: 45.2s                               │
│ ├─ Success Rate: 86.7%                                      │
│ └─ API Response Time: 234ms                                 │
│                                                             │
│ System Health                                               │
│ ├─ Database: ✅ Healthy (45 connections)                    │
│ ├─ Celery: ✅ 4 workers active                              │
│ ├─ Redis: ✅ Healthy (2.3GB used)                           │
│ └─ Disk Space: ⚠️ 78% used (22GB free)                     │
└─────────────────────────────────────────────────────────────┘
```

### Schedulers Page
```
┌─────────────────────────────────────────────────────────────┐
│ ⏰ Scheduled Tasks                                          │
├─────────────────────────────────────────────────────────────┤
│ cleanup_old_sessions                                        │
│ ├─ Status: ✅ Running                                       │
│ ├─ Schedule: Daily at 2:00 AM                               │
│ ├─ Last Run: 2h ago (Success)                               │
│ ├─ Next Run: in 22h                                         │
│ └─ Actions: [▶️ Run Now] [⏸️ Pause] [📊 View Logs]         │
│                                                             │
│ cleanup_stuck_jobs                                          │
│ ├─ Status: ✅ Running                                       │
│ ├─ Schedule: Every 15 minutes                               │
│ ├─ Last Run: 5m ago (Success - 2 jobs cleaned)             │
│ ├─ Next Run: in 10m                                         │
│ └─ Actions: [▶️ Run Now] [⏸️ Pause] [📊 View Logs]         │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 🚀 Deployment Instructions

### Step 1: Deploy Backend Changes
```bash
cd connectme-backend

# Upload files
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  apps/claims/models.py \
  apps/claims/tasks.py \
  apps/claims/views.py \
  apps/claims/migrations/0004_add_cancel_fields.py \
  connectme@20.84.160.240:/var/www/connectme-backend/apps/claims/

# Run migrations
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 << 'EOF'
cd /var/www/connectme-backend
source venv/bin/activate
python manage.py migrate claims
sudo systemctl restart connectme-backend
sudo systemctl restart celery
EOF
```

### Step 2: Deploy Frontend Changes
```bash
cd connectme-frontend

# Upload file
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  src/app/bulk-upload/page.tsx \
  connectme@20.84.160.240:/var/www/connectme-frontend/src/app/bulk-upload/

# Rebuild and restart
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 << 'EOF'
cd /var/www/connectme-frontend
npm run build
pm2 restart connectme-frontend
EOF
```

### Step 3: Test
```bash
# Test cancellation
./test-job-cancellation.sh

# Test bulk upload with flexible dates
./test-bulk-optimization.sh
```

---

## 7. 📝 Testing Checklist

### Manual Testing
- [ ] Upload CSV with 3 claims
- [ ] Click "Cancel" button while processing
- [ ] Verify job status changes to "CANCELLING" then "CANCELLED"
- [ ] Verify job stops processing
- [ ] Upload CSV again with wider date range (last 180 days)
- [ ] Verify claims are found
- [ ] Check backend logs for fallback messages

### Playwright Testing
- [ ] Install Playwright: `npm install --save-dev @playwright/test`
- [ ] Run tests: `npm run test:e2e`
- [ ] Review test report: `npx playwright show-report`
- [ ] Add new tests for cancellation feature

---

## 8. 🎯 Summary

### ✅ Completed
1. **Flexible Date Range Handling**
   - Tries with dates first
   - Falls back to no-date query
   - Handles both scenarios gracefully

2. **Job Cancellation System**
   - Database fields: `cancelled_at`, `cancelled_by`, `CANCELLING` status
   - Backend endpoint: `POST /csv-jobs/{id}/cancel/`
   - Task cancellation checks every 5 rows
   - Celery task revocation
   - Frontend Cancel button
   - Status indicators (CANCELLING, CANCELLED)

### ⏳ Next Steps
1. **Enhanced Monitoring** (2-3 hours)
   - Create monitoring submenu
   - Add system stats page
   - Implement scheduler management
   - Add health check dashboard

2. **Celery Beat Schedulers** (1-2 hours)
   - Setup Celery Beat
   - Implement cleanup tasks
   - Add scheduler UI
   - Configure alerts

3. **Playwright Testing** (1 hour)
   - Install and configure
   - Write E2E tests
   - Integrate with CI/CD
   - Document test procedures

---

## 9. 🔗 Related Documentation

- [8_BULK_UPLOAD_OPTIMIZATION.md](8_BULK_UPLOAD_OPTIMIZATION.md) - Batch query optimization
- [7_LOG_VIEWING_OPTIONS.md](7_LOG_VIEWING_OPTIONS.md) - Log viewing guide
- [4_TESTING_STRATEGY.md](4_TESTING_STRATEGY.md) - Overall testing strategy

---

**Status**: ✅ Bulk upload fixes and cancellation complete. Ready for monitoring enhancements!

