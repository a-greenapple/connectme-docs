# Bulk Upload 401 Error Fix
**Date:** November 6, 2025  
**Status:** ✅ FIXED AND DEPLOYED

---

## 🐛 Problem

Bulk upload was failing with **401 Unauthorized** error in the console.

### Root Causes:

1. **Frontend Token Issue:**
   - Frontend was using `localStorage.getItem('access_token')`
   - Should be using `localStorage.getItem('kc_access_token')` (Keycloak token)
   - This caused the backend to receive `null` token

2. **Backend Authentication Issue:**
   - `BulkUploadView` had `permission_classes = [permissions.AllowAny]`
   - Then tried to fall back to a "test user" if anonymous
   - This created confusion and authentication failures

---

## ✅ Solution

### Frontend Changes (`src/app/bulk-upload/page.tsx`):

Changed all instances of `localStorage.getItem('access_token')` to `localStorage.getItem('kc_access_token')`:

```typescript
// ❌ BEFORE (6 instances):
'Authorization': `Bearer ${localStorage.getItem('access_token')}`

// ✅ AFTER:
'Authorization': `Bearer ${localStorage.getItem('kc_access_token')}`
```

**Fixed in these functions:**
1. ✅ `handleUpload` - Main upload function
2. ✅ `fetchJobStatus` - Check job progress
3. ✅ `fetchJobResults` - Get results (first instance)
4. ✅ `downloadResults` - Download CSV results
5. ✅ `cancelJob` - Cancel a job
6. ✅ `retryJob` - Retry a failed job

### Backend Changes (`apps/claims/views.py`):

Updated `BulkUploadView` to use proper Keycloak authentication:

```python
# ❌ BEFORE:
class BulkUploadView(APIView):
    permission_classes = [permissions.AllowAny]  # Wrong!
    
    def post(self, request):
        # Get user (fallback to test user if anonymous)
        if request.user.is_anonymous:
            user = User.objects.filter(email__icontains='test').first()
            if not user:
                return 401 Unauthorized
        else:
            user = request.user

# ✅ AFTER:
class BulkUploadView(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Use authenticated user
        user = request.user
        
        # Verify user has organization
        if not hasattr(user, 'organization') or not user.organization:
            return 403 Forbidden
```

---

## 🔐 Security Improvements

1. **Proper Authentication** - Now requires valid Keycloak JWT token
2. **No Anonymous Access** - Removed fallback to test user
3. **Organization Verification** - Ensures user has an organization before processing
4. **Consistent Token Usage** - All endpoints now use `kc_access_token`

---

## 🧪 Testing

### Test Bulk Upload:

1. **Login to pre-prod:**
   - Go to: https://pre-prod.connectme.apps.totessoft.com/login
   - Login with: `admin / admin123`

2. **Navigate to Bulk Upload:**
   - Go to: https://pre-prod.connectme.apps.totessoft.com/bulk-upload

3. **Upload CSV:**
   - Create a test CSV file:
     ```csv
     claim_number,first_name,last_name,date_of_birth
     FH65850583,CHANTAL,KISA,05/10/1975
     FH73828971,JOHN,DOE,01/15/1980
     ```
   - Click "Choose File" and select the CSV
   - Select provider: UHC
   - Click "Upload and Process"

4. **Verify:**
   - ✅ No 401 error in console
   - ✅ Upload succeeds
   - ✅ Job appears in the list
   - ✅ Celery processes the file
   - ✅ Results are available

---

## 📊 API Endpoint

### Bulk Upload Endpoint:
```
POST /api/v1/claims/bulk/upload/
Authorization: Bearer <kc_access_token>
Content-Type: multipart/form-data

Form Data:
- file: <CSV file>
- provider: "uhc"
- use_batch_query: true
- start_date: "2025-10-01" (optional)
- end_date: "2025-10-31" (optional)

Response (201 Created):
{
  "id": "uuid",
  "filename": "claims.csv",
  "status": "PENDING",
  "total_rows": 5,
  "processed_rows": 0,
  "success_count": 0,
  "failure_count": 0,
  "celery_task_id": "task-uuid",
  "created_at": "2025-11-06T...",
  ...
}
```

---

## 🚀 Deployment Status

| Component | Status | Changes |
|-----------|--------|---------|
| Frontend | ✅ Deployed | Fixed token key in 6 places |
| Backend | ✅ Deployed | Added Keycloak auth, removed AllowAny |
| Celery | ✅ Running | No changes needed |

---

## 📝 CSV Format

### Supported Formats:

**Option 1: With Claim Numbers**
```csv
claim_number,first_name,last_name,date_of_birth
FH65850583,CHANTAL,KISA,05/10/1975
FH73828971,JOHN,DOE,01/15/1980
```

**Option 2: Without Claim Numbers (Patient Search)**
```csv
first_name,last_name,date_of_birth,first_service_date,last_service_date
CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

**Option 3: With Practice ID**
```csv
practice_id,first_name,last_name,date_of_birth,first_service_date,last_service_date
1,CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
1,JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

---

## ✅ What's Working Now

1. ✅ **Bulk Upload** - CSV files upload successfully
2. ✅ **Authentication** - Proper Keycloak JWT validation
3. ✅ **Celery Processing** - Background tasks run correctly
4. ✅ **Job Tracking** - Can monitor progress
5. ✅ **Results Download** - Can download results CSV
6. ✅ **Error Handling** - Clear error messages

---

## 🎯 Related Files

### Frontend:
- `src/app/bulk-upload/page.tsx` - Main bulk upload page

### Backend:
- `apps/claims/views.py` - BulkUploadView class
- `apps/claims/tasks.py` - Celery task for processing CSV
- `apps/claims/models.py` - CSVJob model

### Services:
- Celery worker: `connectme-preprod-celery.service`
- Backend: `connectme-preprod-backend.service`
- Frontend: PM2 `connectme-preprod-frontend`

---

## 📖 For Users

**To use bulk upload:**

1. Prepare your CSV file with patient information
2. Login to ConnectMe
3. Go to "Bulk Upload" from the menu
4. Select your CSV file
5. Choose provider (UHC)
6. Click "Upload and Process"
7. Monitor progress in real-time
8. Download results when complete

---

**✅ Bulk Upload is now working correctly!**

Test it at: https://pre-prod.connectme.apps.totessoft.com/bulk-upload

