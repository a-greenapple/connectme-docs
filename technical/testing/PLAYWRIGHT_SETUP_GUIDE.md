# 🎭 Playwright E2E Testing Setup Guide

## Quick Start (5 minutes)

### 1. Install Playwright
```bash
cd connectme-frontend
npm install --save-dev @playwright/test
npx playwright install
```

### 2. Run Existing Tests
```bash
# Run all tests
npm run test:e2e

# Run with UI (interactive mode)
npm run test:e2e:ui

# Run specific test
npx playwright test e2e/01-login.spec.ts

# Debug mode
npx playwright test --debug
```

### 3. View Test Results
```bash
# Open HTML report
npx playwright show-report
```

---

## 📁 Test Structure

```
connectme-frontend/
├── e2e/
│   ├── 01-login.spec.ts           ✅ Already exists
│   ├── 02-claims-search.spec.ts   ✅ Already exists
│   ├── 03-bulk-upload.spec.ts     ✅ Already exists
│   ├── 04-job-cancellation.spec.ts  ⏳ To be added
│   └── 05-batch-optimization.spec.ts ⏳ To be added
├── playwright.config.ts           ✅ Already configured
└── package.json                   ✅ Scripts already added
```

---

## 🧪 Writing New Tests

### Example: Job Cancellation Test
```typescript
// e2e/04-job-cancellation.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Job Cancellation', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('[name="username"]', 'test.analyst')
    await page.fill('[name="password"]', 'test123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('should cancel a running job', async ({ page }) => {
    // Navigate to bulk upload
    await page.goto('/bulk-upload')
    
    // Upload CSV file
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles('test-data/large-test.csv')
    
    // Start processing
    await page.click('button:has-text("Upload and Process")')
    
    // Wait for job to start
    await expect(page.locator('text=PROCESSING')).toBeVisible({ timeout: 5000 })
    
    // Click cancel button
    await page.click('button:has-text("Cancel")')
    
    // Verify cancellation
    await expect(page.locator('text=CANCELLING')).toBeVisible({ timeout: 3000 })
    await expect(page.locator('text=CANCELLED')).toBeVisible({ timeout: 10000 })
    
    // Verify job stopped
    const duration = await page.locator('[data-testid="job-duration"]').textContent()
    expect(parseInt(duration || '0')).toBeLessThan(30) // Should stop quickly
  })

  test('should not allow cancelling completed jobs', async ({ page }) => {
    await page.goto('/bulk-upload')
    
    // Find a completed job
    const completedJob = page.locator('[data-status="COMPLETED"]').first()
    await expect(completedJob).toBeVisible()
    
    // Verify no cancel button
    await expect(completedJob.locator('button:has-text("Cancel")')).not.toBeVisible()
  })
})
```

### Example: Batch Optimization Test
```typescript
// e2e/05-batch-optimization.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Batch Query Optimization', () => {
  test('should use batch query for bulk upload', async ({ page }) => {
    await page.goto('/bulk-upload')
    
    // Set date range
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - 90)
    await page.fill('[name="startDate"]', startDate.toISOString().split('T')[0])
    
    const endDate = new Date()
    await page.fill('[name="endDate"]', endDate.toISOString().split('T')[0])
    
    // Enable batch query
    await page.check('[name="useBatchQuery"]')
    
    // Upload file
    await page.setInputFiles('input[type="file"]', 'test-data/bulk-test.csv')
    await page.click('button:has-text("Upload and Process")')
    
    // Monitor processing time
    const startTime = Date.now()
    await expect(page.locator('text=COMPLETED')).toBeVisible({ timeout: 30000 })
    const processingTime = Date.now() - startTime
    
    // Verify fast processing (should be < 20 seconds for 10 claims)
    expect(processingTime).toBeLessThan(20000)
  })
})
```

---

## 🎯 Test Selectors Best Practices

### Use Data Attributes
```typescript
// ❌ Bad: Using text or classes
await page.click('.btn-primary')
await page.click('button:has-text("Submit")')

// ✅ Good: Using data-testid
await page.click('[data-testid="submit-button"]')
```

### Add to Components
```tsx
// In your React components
<button data-testid="cancel-job-button" onClick={cancelJob}>
  Cancel
</button>

<div data-testid="job-status" data-status={job.status}>
  {job.status}
</div>
```

---

## 🚀 Running Tests in CI/CD

### GitHub Actions
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
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd connectme-frontend
          npm ci
      
      - name: Install Playwright
        run: |
          cd connectme-frontend
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd connectme-frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: connectme-frontend/playwright-report/
```

---

## 📊 Monitoring Test Results

### HTML Report
```bash
# Generate and open report
npx playwright show-report
```

### CI/CD Integration
- Tests run automatically on every push
- Reports uploaded as artifacts
- Failed tests block merges
- Screenshots/videos captured on failures

---

## 🐛 Debugging Tests

### Debug Mode
```bash
# Run with debugger
npx playwright test --debug

# Run specific test with debugger
npx playwright test e2e/04-job-cancellation.spec.ts --debug
```

### Screenshots on Failure
```typescript
test('my test', async ({ page }) => {
  // Automatically captures screenshot on failure
  await page.goto('/bulk-upload')
  await expect(page.locator('text=Upload')).toBeVisible()
})
```

### Video Recording
```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    video: 'on-first-retry', // Record video on first retry
    screenshot: 'only-on-failure', // Screenshot on failure
  },
})
```

---

## 🎯 Quick Commands Reference

```bash
# Install
npm install --save-dev @playwright/test
npx playwright install

# Run tests
npm run test:e2e              # All tests
npm run test:e2e:ui           # Interactive UI
npm run test:e2e:headed       # Show browser
npm run test:e2e:debug        # Debug mode

# Specific tests
npx playwright test e2e/04-job-cancellation.spec.ts
npx playwright test --grep "cancel"

# Reports
npx playwright show-report

# Update snapshots
npx playwright test --update-snapshots

# Generate tests (codegen)
npx playwright codegen https://connectme.apps.totesoft.com
```

---

## 📝 Next Steps

1. **Add Test Data**
   ```bash
   mkdir -p connectme-frontend/test-data
   cp uhc-bulk-real-claims.csv connectme-frontend/test-data/
   ```

2. **Write New Tests**
   - Job cancellation (04-job-cancellation.spec.ts)
   - Batch optimization (05-batch-optimization.spec.ts)
   - Results modal (06-results-modal.spec.ts)

3. **Add Data Attributes**
   - Add `data-testid` to key UI elements
   - Makes tests more reliable and maintainable

4. **Set Up CI/CD**
   - Add GitHub Actions workflow
   - Configure test reporting
   - Set up failure notifications

---

## 🎉 Summary

Playwright is **already installed and configured** in your project!

**To start testing:**
```bash
cd connectme-frontend
npm run test:e2e:ui
```

**To add new tests:**
1. Create file in `e2e/` directory
2. Write test using examples above
3. Run with `npm run test:e2e`

**Documentation:** https://playwright.dev/docs/intro

---

Ready to write comprehensive E2E tests! 🚀

