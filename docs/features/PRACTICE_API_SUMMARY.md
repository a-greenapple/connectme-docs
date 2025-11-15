# Practice API Implementation Summary
**Date:** November 6, 2025

## ✅ What Was Implemented

### Backend Changes:

#### 1. **Created Practice API** (`apps/providers/`)
- **`serializers.py`** - Created serializers for:
  - `ProviderSerializer` - Provider information
  - `PracticeSerializer` - Full practice details with payer mappings
  - `PracticeListSerializer` - Simplified list view
  - `PracticePayerMappingSerializer` - Payer mapping details

- **`api_views.py`** - Created ViewSets:
  - `PracticeViewSet` - Read-only API for practices
    - Automatically filters by user's organization TIN
    - Includes payer mappings in detail view
    - Custom action: `/practices/{id}/payer_mappings/`
  - `ProviderViewSet` - Read-only API for providers

- **`urls.py`** - Configured routes:
  - `/api/v1/providers/practices/` - List practices
  - `/api/v1/providers/practices/{id}/` - Practice detail
  - `/api/v1/providers/providers/` - List providers

#### 2. **Updated Main URLs** (`config/urls.py`)
- Added: `path('api/v1/providers/', include('apps.providers.urls'))`

---

## 📊 API Endpoints

### List Practices
```
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

### Practice Detail
```
GET /api/v1/providers/practices/1/
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "name": "RSM",
  "tin": "854203105",
  "npi": "",
  "address": "",
  "phone": "",
  "email": "",
  "is_active": true,
  "payer_mappings": [
    {
      "id": 1,
      "provider": 1,
      "provider_name": "UnitedHealthcare",
      "provider_code": "UHC",
      "payer_id": "87726",
      "is_active": true,
      "notes": "UHC Payer ID for RSM",
      "effective_date": "2025-11-06",
      "termination_date": null
    }
  ],
  "created_at": "2025-11-06T...",
  "updated_at": "2025-11-06T..."
}
```

### Practice Payer Mappings
```
GET /api/v1/providers/practices/1/payer_mappings/
Authorization: Bearer <token>

Response:
[
  {
    "id": 1,
    "provider": 1,
    "provider_name": "UnitedHealthcare",
    "provider_code": "UHC",
    "payer_id": "87726",
    "is_active": true,
    "notes": "UHC Payer ID for RSM",
    "effective_date": "2025-11-06",
    "termination_date": null
  }
]
```

---

## 🔐 Security Features

1. **Authentication Required** - All endpoints require valid JWT token
2. **Organization Filtering** - Users only see practices for their organization's TIN
3. **Read-Only** - Practices can only be managed via Django Admin
4. **Active Only** - Only active practices are returned

---

## 🎯 Next Steps for Frontend

### 1. **Add Practice Selector to Claims Search**

Update `connectme-frontend/src/app/claims/page.tsx`:

```typescript
// Add state for practices
const [practices, setPractices] = useState<Practice[]>([]);
const [selectedPractice, setSelectedPractice] = useState<string>('');

// Fetch practices on mount
useEffect(() => {
  const fetchPractices = async () => {
    const token = localStorage.getItem('kc_access_token');
    const response = await fetch(
      'https://pre-prod.connectme.be.totessoft.com/api/v1/providers/practices/',
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    const data = await response.json();
    setPractices(data);
    if (data.length > 0) {
      setSelectedPractice(data[0].id); // Default to first practice
    }
  };
  
  if (isAuthenticated) {
    fetchPractices();
  }
}, [isAuthenticated]);

// Add practice selector to search form
<select 
  value={selectedPractice}
  onChange={(e) => setSelectedPractice(e.target.value)}
  className="..."
>
  {practices.map(practice => (
    <option key={practice.id} value={practice.id}>
      {practice.name} (TIN: {practice.tin})
    </option>
  ))}
</select>
```

### 2. **Update Bulk Upload to Include Practice**

Add practice selector to bulk upload form:
- Show dropdown of available practices
- Include practice_id in CSV upload
- Display practice info in job results

### 3. **Show Practice Info in Claims Table**

Add practice column to claims results:
- Practice Name
- TIN
- Payer ID used for query

---

## 📝 CSV Format Updates

### Current Format (Hardcoded RSM):
```csv
claim_number,first_name,last_name,date_of_birth
FH65850583,CHANTAL,KISA,05/10/1975
```

### New Format (With Practice Selection):
```csv
practice_id,first_name,last_name,date_of_birth,first_service_date,last_service_date
1,CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
1,JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

**OR** use TIN directly:
```csv
tin,payer_id,first_name,last_name,date_of_birth,first_service_date,last_service_date
854203105,87726,CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
854203105,87726,JOHN,DOE,01/15/1980,10/01/2025,10/31/2025
```

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

# Get practice detail
curl -H "Authorization: Bearer $TOKEN" \
  "https://pre-prod.connectme.be.totessoft.com/api/v1/providers/practices/1/"

# Get payer mappings
curl -H "Authorization: Bearer $TOKEN" \
  "https://pre-prod.connectme.be.totessoft.com/api/v1/providers/practices/1/payer_mappings/"
```

---

## 🎯 Benefits

1. **Multi-Practice Support** - Users can select which practice to query
2. **No Hardcoding** - Practice info comes from database
3. **Scalable** - Easy to add more practices via Django Admin
4. **Secure** - Users only see their organization's practices
5. **Flexible** - Supports multiple payers per practice

---

## 📚 Documentation

### Django Admin:
- **Providers** → View/edit insurance providers (UHC, Aetna, etc.)
- **Practices** → View/edit healthcare practices (RSM, etc.)
- **Practice Payer Mappings** → Link practices to providers with payer IDs

### Adding a New Practice:
1. Go to Django Admin → Practices → Add Practice
2. Enter: Name, TIN, NPI (optional), contact info
3. Go to Practice Payer Mappings → Add Mapping
4. Select: Practice, Provider, enter Payer ID
5. Practice will now appear in API and frontend dropdown

---

## ✅ Deployment Status

- ✅ Backend API deployed to pre-prod
- ✅ Endpoints tested and working
- ✅ Authentication required
- ✅ Organization filtering active
- ⏳ Frontend integration pending

---

**Next: Update frontend to use the new Practice API!**

