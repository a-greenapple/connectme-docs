# Troubleshooting: Bulk Upload Not Returning Results

## 🔴 Problem
Bulk upload is not returning any results after uploading CSV file.

## 🔍 Possible Causes & Solutions

### 1. **CSV Format Issues**

#### Check Your CSV Format:
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
```

#### Common Issues:
- ❌ Wrong header names
- ❌ Missing required fields
- ❌ Wrong date format (must be YYYY-MM-DD)
- ❌ TIN not matching existing practice
- ❌ Extra spaces or special characters

#### Solution:
1. Download the template from the UI
2. Copy your data into the template
3. Save as CSV (not Excel format)

---

### 2. **No Matching Claims in System**

#### Symptoms:
- Upload succeeds
- Processing completes
- But 0 results returned

#### Cause:
The patient data you're searching for doesn't exist in the UHC system.

#### Solution:
Use real patient data that you know has claims, or test with known claim numbers.

---

### 3. **Authentication Issues**

#### Check:
```bash
# Open browser console (F12)
# Look for errors like:
- 401 Unauthorized
- 403 Forbidden
- Token expired
```

#### Solution:
1. Logout and login again
2. Clear browser cache
3. Try in incognito mode

---

### 4. **Backend Processing Errors**

#### Check Backend Logs:
```bash
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100 | grep -i "error\|exception"'
```

#### Common Errors:
- UHC API timeout
- Invalid credentials
- Rate limiting
- Network issues

---

### 5. **Celery Worker Not Processing**

#### Check Celery Status:
```bash
ssh connectme@169.59.163.43 'ps aux | grep celery | grep -v grep'
```

#### If Not Running:
```bash
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && celery -A config worker --loglevel=info &'
```

---

### 6. **Frontend Not Polling Results**

#### Check Browser Console:
```javascript
// Look for errors in Network tab
// Check if polling requests are being made
GET /api/v1/claims/csv-jobs/{job_id}/
```

#### Solution:
- Refresh the page
- Check if job appears in history sidebar
- Click "View" on the job

---

## 🧪 Step-by-Step Debugging

### Step 1: Verify Upload
1. Go to: https://pre-prod.connectme.apps.totessoft.com/bulk-upload
2. Upload CSV file
3. Check if job appears in history sidebar (left side)
4. Note the job status

**Expected**: Job should show "PENDING" or "PROCESSING"

---

### Step 2: Monitor Processing
1. Watch the history sidebar
2. Job should change from PENDING → PROCESSING → COMPLETED
3. Progress bar should update
4. Success/failure counts should increase

**Expected**: Job completes within 30-60 seconds for 10-20 rows

---

### Step 3: Check Results
1. When job shows "COMPLETED"
2. Click "View" button
3. Modal should open with results
4. Or click "Download" to get CSV

**Expected**: See list of claims with details

---

### Step 4: Check Browser Console
1. Press F12 to open DevTools
2. Go to Console tab
3. Look for errors (red text)
4. Go to Network tab
5. Look for failed requests (red status codes)

**Common Issues**:
- 401: Not authenticated
- 403: No permission
- 404: Endpoint not found
- 500: Server error
- Timeout: Request took too long

---

### Step 5: Check Backend Logs
```bash
# SSH into server
ssh connectme@169.59.163.43

# Check recent logs
sudo journalctl -u connectme-preprod-backend -n 100

# Watch logs in real-time
sudo journalctl -u connectme-preprod-backend -f
```

**Look for**:
- "Processing claim X/Y"
- "Details API success"
- "Payment API success"
- Any ERROR or WARNING messages

---

## 🔧 Quick Fixes

### Fix 1: Restart Celery
```bash
ssh connectme@169.59.163.43 'sudo systemctl restart connectme-preprod-backend'
```

### Fix 2: Clear Browser Cache
```
Chrome: Ctrl+Shift+Delete
Select: Cached images and files
Click: Clear data
```

### Fix 3: Re-login
```
1. Logout from app
2. Clear cookies
3. Login again
4. Try upload again
```

### Fix 4: Use Template
```
1. Click "Download Template" button
2. Fill in with your data
3. Save as CSV
4. Upload
```

---

## 📊 Expected Behavior

### Successful Upload Flow:

```
1. User uploads CSV
   ↓
2. File validated
   ↓
3. Job created (shows in history)
   ↓
4. Celery picks up job
   ↓
5. Processing starts (progress bar appears)
   ↓
6. For each row:
   - Search for patient
   - Get claim details
   - Get payment info
   ↓
7. Job completes
   ↓
8. Results available
   - Click "View" to see in modal
   - Click "Download" to get CSV
```

### Timeline:
- **Upload**: < 1 second
- **Queue**: < 5 seconds
- **Processing**: 2-3 seconds per row
- **Total**: 30-60 seconds for 20 rows

---

## 🎯 Test with Known Data

### Option 1: Use Sample File
```bash
# Download sample_bulk_claims_real.csv
# Upload to system
# Should process successfully
```

### Option 2: Single Row Test
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,Test,Patient,1980-01-01,2024-01-01
```

### Option 3: Check Existing Claims
```bash
# SSH to server
ssh connectme@169.59.163.43

# Check what claims exist
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py shell

# In Python shell:
from apps.claims.models import Claim
claims = Claim.objects.all()[:5]
for c in claims:
    print(f"Claim: {c.claim_number}, DOB: {c.patient_dob}, DOS: {c.service_date}")
```

---

## 📞 What to Check Right Now

### 1. Browser Console
- Open DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

### 2. History Sidebar
- Is the job showing in history?
- What status does it show?
- Is progress updating?

### 3. Job Details
- Click on the job in history
- What's the total rows?
- What's the success/failure count?
- Any error messages?

---

## 🚨 Common Error Messages

### "No practices found"
**Cause**: User not assigned to any practices
**Fix**: Admin needs to assign practices to user

### "Invalid TIN"
**Cause**: TIN doesn't match any practice
**Fix**: Use 854203105 or 260167522

### "Invalid date format"
**Cause**: Date not in YYYY-MM-DD format
**Fix**: Use 2024-01-15 format

### "Authentication failed"
**Cause**: Token expired or invalid
**Fix**: Logout and login again

### "Processing timeout"
**Cause**: Too many rows or slow API
**Fix**: Reduce batch size, try again

---

## 📋 Information Needed for Support

If still not working, provide:

1. **CSV file** (first 3 rows)
2. **Browser console errors** (screenshot)
3. **Network tab** (failed requests)
4. **Job status** (from history sidebar)
5. **Backend logs** (last 50 lines)

---

## ✅ Checklist

- [ ] CSV format is correct (use template)
- [ ] TIN matches existing practice (854203105 or 260167522)
- [ ] Dates in YYYY-MM-DD format
- [ ] Logged in successfully
- [ ] Job appears in history sidebar
- [ ] Celery worker is running
- [ ] No errors in browser console
- [ ] Waited for processing to complete (30-60 seconds)

---

**Last Updated**: November 12, 2025  
**Status**: Troubleshooting Guide

