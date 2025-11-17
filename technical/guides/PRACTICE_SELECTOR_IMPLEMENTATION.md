# Practice Selector Implementation
**Date:** November 6, 2025  
**Status:** ✅ DEPLOYED TO PRE-PROD

---

## 🎯 What Was Implemented

### Frontend Changes:

#### 1. **ClaimsSearchForm Component** (`src/components/claims/ClaimsSearchForm.tsx`)
- ✅ Added practice dropdown selector above date fields
- ✅ Fetches practices from `/api/v1/providers/practices/` on mount
- ✅ Auto-selects first practice by default
- ✅ Shows loading state while fetching practices
- ✅ Shows error if no practices found
- ✅ Passes `practiceId` to search handler
- ✅ Displays practice name and TIN in dropdown

**UI Features:**
```typescript
- Practice dropdown with label "Practice *"
- Shows: "RSM (TIN: 854203105)"
- Loading state: "Loading practices..."
- Error state: "No practices found. Please contact your administrator."
- Help text: "Select the practice for which to search claims"
```

#### 2. **Claims Page** (`src/app/claims/page.tsx`)
- ✅ Updated `handleSearch` to accept `practiceId` parameter
- ✅ Passes `practiceId` to API call

#### 3. **API Client** (`src/lib/api.ts`)
- ✅ Updated `searchClaims` interface to include `practiceId?: string`
- ✅ Sends `practiceId` to backend

---

### Backend Changes:

#### 1. **Practice API** (`apps/providers/`)
- ✅ Created `PracticeSerializer` - Full practice details with payer mappings
- ✅ Created `PracticeListSerializer` - Simplified list view
- ✅ Created `PracticeViewSet` - Read-only API endpoint
  - Filters by user's organization TIN
  - Returns only active practices
  - Includes payer mappings in detail view
- ✅ Registered routes in `apps/providers/urls.py`
- ✅ Added to main URLs: `/api/v1/providers/`

#### 2. **Claims Search API** (`apps/claims/api_views.py`)
- ✅ Updated `search_claims` to accept `practiceId` parameter
- ✅ Implements practice selection logic:
  - If `practiceId` provided: Use that practice
  - If no `practiceId`: Fall back to user's organization practice
  - Security: Verifies user has access to selected practice (same TIN)
- ✅ Better error handling for missing practices/mappings

**New Logic:**
```python
if practice_id:
    # Use specified practice
    practice = Practice.objects.get(id=practice_id, is_active=True)
    
    # Verify user has access (same organization TIN)
    if practice.tin != request.user.organization.tin:
        return 403 Forbidden
else:
    # Fall back to user's organization practice
    practice = Practice.objects.get(tin=request.user.organization.tin)
```

---

## 🔐 Security Features

1. **Authentication Required** - All endpoints require valid JWT token
2. **Organization Filtering** - Users only see practices for their organization's TIN
3. **Access Control** - Users cannot search claims for practices outside their organization
4. **Read-Only Practices** - Practices can only be managed via Django Admin

---

## 📊 API Endpoints

### List Practices
```bash
GET /api/v1/providers/practices/
Authorization: Bearer <token>

Response:
[
  {
    "id": 1,
    "name": "RSM",
    "tin": "854203105",
    "npi": "",
    "is_active": true
  }
]
```

### Search Claims with Practice
```bash
POST /api/v1/claims/search/
Authorization: Bearer <token>
Content-Type: application/json

{
  "firstServiceDate": "2025-10-01",
  "lastServiceDate": "2025-10-31",
  "practiceId": "1",              // NEW - optional
  "patientFirstName": "CHANTAL",  // optional
  "patientLastName": "KISA",      // optional
  "patientDob": "1975-05-10"      // optional
}
```

---

## 🎨 User Experience

### Before:
- Practice was hardcoded to RSM (TIN: 854203105)
- No way to select different practices
- Users couldn't see which practice they were searching

### After:
- ✅ Practice dropdown at top of search form
- ✅ Shows all practices user has access to
- ✅ Clear display: "RSM (TIN: 854203105)"
- ✅ Auto-selects first practice
- ✅ Remembers selection during session
- ✅ Clear error messages if practice not found

---

## 🧪 Testing

### Test Practice API:
```bash
# Get token
TOKEN=$(curl -s -X POST "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -d "client_id=connectme-preprod-frontend" \
  -d "username=admin" \
  -d "password=admin123" \
  -d "grant_type=password" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# List practices
curl -H "Authorization: Bearer $TOKEN" \
  "https://pre-prod.connectme.be.totessoft.com/api/v1/providers/practices/"
```

### Test Claims Search with Practice:
```bash
curl -X POST "https://pre-prod.connectme.be.totessoft.com/api/v1/claims/search/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstServiceDate": "2025-10-01",
    "lastServiceDate": "2025-10-31",
    "practiceId": "1",
    "patientFirstName": "CHANTAL",
    "patientLastName": "KISA"
  }'
```

---

## 📝 CSV Format Updates

### For Bulk Upload (Future Enhancement):

**Option 1: Use Practice ID**
```csv
practice_id,first_name,last_name,date_of_birth,first_service_date,last_service_date
1,CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
1,JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

**Option 2: Use TIN Directly**
```csv
tin,payer_id,first_name,last_name,date_of_birth,first_service_date,last_service_date
854203105,87726,CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
854203105,87726,JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

---

## 🚀 Deployment Status

| Component | Status | URL |
|-----------|--------|-----|
| Backend API | ✅ Deployed | `https://pre-prod.connectme.be.totessoft.com` |
| Frontend | ✅ Deployed | `https://pre-prod.connectme.apps.totessoft.com` |
| Practice API | ✅ Working | `/api/v1/providers/practices/` |
| Claims Search | ✅ Updated | `/api/v1/claims/search/` |

---

## 📚 How to Add More Practices

### Via Django Admin:

1. **Add Practice:**
   - Go to: Django Admin → Providers → Practices → Add Practice
   - Enter: Name, TIN, NPI (optional), contact info
   - Save

2. **Add Payer Mapping:**
   - Go to: Django Admin → Providers → Practice Payer Mappings → Add Mapping
   - Select: Practice, Provider (e.g., UHC), enter Payer ID
   - Save

3. **Practice appears in dropdown automatically!**
   - Users with matching organization TIN will see it
   - No code changes needed

---

## ✅ Benefits

1. **Multi-Practice Support** - Users can select which practice to query
2. **No Hardcoding** - Practice info comes from database
3. **Scalable** - Easy to add more practices via Django Admin
4. **Secure** - Users only see their organization's practices
5. **Flexible** - Supports multiple payers per practice
6. **Better UX** - Clear visibility of which practice is being searched
7. **Backward Compatible** - Falls back to user's organization if no practice selected

---

## 🎯 Next Steps (Optional Enhancements)

1. **Bulk Upload Practice Selector**
   - Add practice dropdown to bulk upload form
   - Include practice_id in CSV validation

2. **Practice Info in Results**
   - Show practice name/TIN in claims table
   - Add practice column to results

3. **Multi-Practice Search**
   - Allow searching multiple practices at once
   - Aggregate results from multiple practices

4. **Practice Dashboard**
   - Show practice-specific statistics
   - Claims by practice, success rates, etc.

---

## 📖 Documentation

### For Users:
- Practice dropdown appears at top of claims search form
- Select your practice before searching
- Only practices you have access to will appear

### For Admins:
- Add practices via Django Admin → Providers → Practices
- Link practices to payers via Practice Payer Mappings
- Users automatically see practices matching their organization TIN

---

**✅ Implementation Complete and Deployed!**

Test it now at: https://pre-prod.connectme.apps.totessoft.com/claims

