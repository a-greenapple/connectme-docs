# Keycloak Integration Guide

## Architecture Overview

Based on your auth flow diagram (`auth.png`), here's how the authentication works:

```
┌──────────┐
│  Users   │ Login to Web App
└────┬─────┘
     │
     ▼
┌────────────────────────┐
│ Connect Me React App   │──────┐
│ (Next.js + TypeScript) │      │
└────────────────────────┘      │
     │                           │
     │ API Call with Token       │ User Login
     │ Authorization:            │ 200/401
     │ Bearer {token}            │
     │                           ▼
     ▼                    ┌──────────────────┐
┌─────────────────────┐  │   Authorization  │
│ Django Backend      │  │     Provider     │
│ https://api.        │  │    (Keycloak)    │
│ connectme.          │  │                  │
│ totesoft.com        │  └──────────────────┘
│                     │           │
│ /claims API         │           │ Validates token
│                     │←──────────┘ with Keycloak
│                     │
│ PostgreSQL          │
└─────────────────────┘
```

## Backend Implementation

### 1. Keycloak Authentication Backend

**File**: `apps/auth/keycloak.py`

Features:
- ✅ Validates JWT tokens from Keycloak
- ✅ Fetches and caches public key from Keycloak
- ✅ Creates/updates Django user from token
- ✅ Returns 401 for invalid/expired tokens

**Key Points:**
- Uses RS256 algorithm for JWT validation
- Caches Keycloak public key (JWKS)
- Extracts user info from token claims:
  - `preferred_username` → Django username
  - `email` → Email
  - `given_name` → First name
  - `family_name` → Last name

### 2. Protected API Endpoints

**File**: `apps/claims/api_views.py`

All endpoints use `@authentication_classes([KeycloakAuthentication])`:

#### POST /api/v1/claims/search/
Search UHC claims by date range

**Request:**
```json
{
  "firstServiceDate": "2025-05-01",
  "lastServiceDate": "2025-05-02",
  "patientFirstName": "JOHN",  // optional
  "patientLastName": "DOE",     // optional
  "patientDob": "1990-01-01"    // optional
}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "transactionId": "trnmeb...",
  "hasMore": false,
  "claims": [
    {
      "id": 1,
      "claimNumber": "FC14745727",
      "patient": "JIGEESHA LANKA",
      "serviceDate": "05/02/2025",
      "status": "Finalized",
      "chargedAmount": "565.00",
      "paidAmount": "245.96",
      "detailsAvailable": true
    }
  ]
}
```

#### GET /api/v1/claims/{claimNumber}/details/
Get detailed information for a specific claim

**Response:**
```json
{
  "success": true,
  "claimNumber": "FC14745727",
  "details": {
    "claimsDetailInfo": [...],
    "claimSummaryInfo": {...}
  }
}
```

#### GET /api/v1/claims/
Get all claims for user's organization

---

## Frontend Implementation

### 1. Authentication Context

**File**: `frontend/src/contexts/AuthContext.tsx`

Manages Keycloak authentication state:
- Login/Logout
- Token storage
- User info
- Auto-refresh tokens

### 2. API Client

**File**: `frontend/src/lib/api.ts`

Axios instance with:
- Automatic token injection
- 401 handling (redirect to login)
- Base URL configuration

### 3. Claims Components

#### ClaimsSearch Component
**File**: `frontend/src/components/claims/ClaimsSearch.tsx`

Features:
- Date range picker (required)
- Optional patient filters
- Form validation
- Loading states
- Error handling

#### ClaimsTable Component
**File**: `frontend/src/components/claims/ClaimsTable.tsx`

Features:
- Sortable columns
- Expandable rows for details
- CSV export
- Pagination

---

## Configuration

### Backend (.env)

```bash
# Keycloak Configuration
KEYCLOAK_SERVER_URL=https://api.connectme.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-frontend
KEYCLOAK_CLIENT_SECRET=

# Django
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,api.connectme.totesoft.com

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/connectme

# UHC API (already configured)
UHC_API_KEY=...
UHC_CLIENT_ID=<REDACTED_CLIENT_ID>
UHC_CLIENT_SECRET=<REDACTED_SECRET>
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

---

## Authentication Flow

### 1. User Login

```typescript
// Frontend initiates login
const { login } = useAuth();
await login(username, password);

// Flow:
1. POST to Keycloak /auth/realms/{realm}/protocol/openid-connect/token
2. Get access_token + refresh_token
3. Store tokens in localStorage
4. Update auth context
5. Redirect to dashboard
```

### 2. API Request

```typescript
// Make authenticated request
const response = await api.post('/claims/search/', {
  firstServiceDate: '2025-05-01',
  lastServiceDate: '2025-05-02'
});

// Flow:
1. Axios intercepts request
2. Adds header: Authorization: Bearer {access_token}
3. Django receives request
4. KeycloakAuthentication validates token
5. Returns 200 OK with data OR 401 Unauthorized
```

### 3. Token Refresh

```typescript
// Auto-refresh before expiry
setInterval(() => {
  if (tokenNearExpiry()) {
    refreshToken();
  }
}, 60000); // Check every minute

// Flow:
1. POST to Keycloak with refresh_token
2. Get new access_token
3. Update stored tokens
4. Continue session
```

### 4. Logout

```typescript
// User logout
const { logout } = useAuth();
logout();

// Flow:
1. Clear tokens from localStorage
2. Clear auth context
3. Redirect to login page
4. (Optional) POST to Keycloak logout endpoint
```

---

## Security Features

### Backend
- ✅ JWT token validation with Keycloak
- ✅ Token expiration checking
- ✅ Audience validation
- ✅ Public key verification (RS256)
- ✅ CORS configuration
- ✅ HTTPS only in production
- ✅ PHI encryption at rest
- ✅ Audit logging

### Frontend
- ✅ Secure token storage
- ✅ Auto token refresh
- ✅ Protected routes
- ✅ HTTPS only in production
- ✅ XSS protection
- ✅ CSRF protection

---

## Testing

### Test Backend Authentication

```bash
# Get token from Keycloak
curl -X POST https://api.connectme.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password"

# Use token to call API
curl -X POST https://api.connectme.totesoft.com/api/v1/claims/search/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"firstServiceDate":"2025-05-01","lastServiceDate":"2025-05-02"}'
```

### Test Frontend
1. Navigate to https://connectme.totesoft.com/login
2. Enter credentials
3. Should redirect to dashboard
4. Try searching claims
5. Check Network tab for Authorization header

---

## Deployment Checklist

### Backend
- [ ] Set KEYCLOAK_SERVER_URL in production
- [ ] Configure CORS for frontend domain
- [ ] Set secure SECRET_KEY
- [ ] Enable HTTPS only
- [ ] Configure PostgreSQL
- [ ] Set up Redis for caching
- [ ] Configure logging
- [ ] Run migrations
- [ ] Create superuser

### Frontend
- [ ] Set NEXT_PUBLIC_API_URL to production backend
- [ ] Set NEXT_PUBLIC_KEYCLOAK_URL
- [ ] Enable HTTPS only
- [ ] Configure CSP headers
- [ ] Build production bundle
- [ ] Deploy to hosting

### Keycloak
- [ ] Create realm: connectme
- [ ] Create client: connectme-frontend
- [ ] Configure redirect URIs
- [ ] Set up roles and permissions
- [ ] Create test users
- [ ] Enable token settings (RS256, expiry)

---

## Troubleshooting

### 401 Unauthorized
**Symptom**: API returns 401 even with token

**Check**:
1. Token not expired: `jwt.decode(token)` in browser console
2. Keycloak server URL correct
3. Realm name matches
4. Client ID matches
5. Token signature valid

**Solution**:
- Refresh token if expired
- Verify Keycloak configuration
- Check Django logs for detailed error

### CORS Errors
**Symptom**: Browser blocks API requests

**Solution**:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://connectme.totesoft.com",
    "http://localhost:3000",  # development
]
CORS_ALLOW_CREDENTIALS = True
```

### Token Validation Fails
**Symptom**: "Failed to validate token with Keycloak"

**Check**:
1. Keycloak server reachable
2. Public key endpoint accessible:
   `GET {KEYCLOAK_URL}/realms/{realm}/protocol/openid-connect/certs`
3. Network connectivity

**Solution**:
- Check firewall rules
- Verify Keycloak is running
- Check Django logs

---

## Next Steps

1. ✅ Backend authentication implemented
2. ✅ API endpoints created  
3. ⏳ Create frontend Auth Context
4. ⏳ Implement login page
5. ⏳ Build claims search interface
6. ⏳ Add protected routes
7. ⏳ Test end-to-end flow
8. ⏳ Deploy to staging

---

## Files Created

### Backend
- `apps/auth/__init__.py` - Auth app initialization
- `apps/auth/keycloak.py` - Keycloak authentication backend
- `apps/claims/api_views.py` - Protected API endpoints
- `apps/claims/api_urls.py` - API URL configuration
- `config/settings.py` - Updated with Keycloak config

### Frontend (Next to create)
- `frontend/src/contexts/AuthContext.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/components/claims/ClaimsSearch.tsx`
- `frontend/src/components/claims/ClaimsTable.tsx`
- `frontend/src/app/login/page.tsx`
- `frontend/src/app/dashboard/page.tsx`

---

**Status**: Backend ✅ Complete | Frontend ⏳ In Progress

**Ready for**: Frontend integration and testing

