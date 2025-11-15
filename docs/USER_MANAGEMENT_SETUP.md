# User Management Setup Guide

## Overview
ConnectMe User Management is integrated with Keycloak SSO for seamless authentication and user administration.

---

## 🎯 **Current Status**

### ✅ **Backend**
- **Keycloak Sync Implementation**: Auto-syncs users from Keycloak to Django on login
- **API Endpoints**: `/api/v1/users/` and `/api/v1/auth/users/` (both routes active)
- **Authentication**: Keycloak JWT tokens required
- **CRUD Operations**: Create, Read, Update, Delete users with Keycloak sync

### ✅ **Frontend**
- **User Management Page**: `/users` (accessible via Admin → User Management)
- **Keycloak Integration**: Role extraction from JWT tokens
- **Navigation**: Admin dropdown menu (visible to all authenticated users)

---

## 🔧 **Recent Fixes (Oct 16, 2025)**

### 1. **Missing API Route**
- **Issue**: 404 errors on `/api/v1/users/` endpoint
- **Fix**: Added route in `config/urls.py`
- **Status**: ✅ Fixed (returns 401 for unauthorized, indicating correct routing)

### 2. **Missing Dependencies**
- **Issue**: `django-sslserver` and `lucide-react` packages missing
- **Fix**: 
  - Added `django-sslserver>=0.22` to `requirements/base.txt`
  - Installed `lucide-react` on production frontend
- **Status**: ✅ Fixed

### 3. **Backend Import Errors**
- **Issue**: `APIView` and `RefreshToken` not imported in `views.py`
- **Fix**: Added missing imports
- **Status**: ✅ Fixed

### 4. **Stale Code on Production**
- **Issue**: Old `urls.py` referencing removed `DjangoLoginView`
- **Fix**: Cleared `__pycache__`, deployed updated files
- **Status**: ✅ Fixed

---

## 📡 **API Endpoints**

### User Management
```
GET    /api/v1/users/              # List all users
POST   /api/v1/users/              # Create new user
GET    /api/v1/users/{id}/         # Get user details
PUT    /api/v1/users/{id}/         # Update user
PATCH  /api/v1/users/{id}/         # Partial update
DELETE /api/v1/users/{id}/         # Delete user
POST   /api/v1/users/{id}/activate/    # Activate user
```

### Keycloak Sync
```
POST   /api/v1/users/sync/keycloak/           # Bulk sync from Keycloak
POST   /api/v1/users/sync/keycloak/{user_id}/ # Sync individual user
```

### Authentication
```
POST   /api/v1/auth/mock/login/     # Mock login (development)
GET    /api/v1/auth/profile/        # Get current user profile
POST   /api/v1/auth/logout/         # Logout user
```

---

## 🔐 **Authentication Flow**

1. **User logs in** via Keycloak (frontend)
2. **Keycloak issues JWT** token with user info and roles
3. **Frontend extracts role** from JWT token payload
4. **Backend validates JWT** on each API request
5. **Auto-sync**: Backend syncs user from Keycloak to Django on first login
6. **User Management**: Admin can manage users via UI, synced to both Django and Keycloak

---

## 🚀 **Accessing User Management**

### For End Users:
1. Navigate to: https://connectme.apps.totesoft.com
2. Login with Keycloak credentials
3. Click **Admin** → **User Management**

### For Admins:
- Same access as above
- Additional permissions for CRUD operations
- Can sync users from Keycloak

---

## 🔑 **Environment Variables**

### Backend (Required)
```bash
# Keycloak Admin API Access
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=your_admin_password

# Keycloak Configuration
KEYCLOAK_URL=https://api.connectme.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-backend
```

### Frontend
```bash
# API Base URL
NEXT_PUBLIC_API_BASE_URL=https://connectme.be.totesoft.com

# Keycloak Configuration
NEXT_PUBLIC_KEYCLOAK_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

---

## 📁 **Key Files**

### Backend
```
connectme-backend/
├── apps/users/
│   ├── api_views.py          # User Management ViewSet
│   ├── keycloak_sync.py      # Keycloak Admin API integration
│   ├── urls.py               # User management routes
│   └── views.py              # Auth views
├── apps/auth/
│   └── keycloak.py           # JWT validation & auto-sync
└── config/
    ├── settings.py           # Keycloak admin credentials
    └── urls.py               # API routing
```

### Frontend
```
connectme-frontend/
├── src/
│   ├── app/users/
│   │   └── page.tsx          # User Management UI
│   ├── components/
│   │   └── Navbar.tsx        # Navigation with Admin menu
│   ├── contexts/
│   │   └── AuthContext.tsx   # Auth state management
│   └── lib/
│       └── keycloak.ts       # Keycloak service with role extraction
```

---

## 🧪 **Testing**

### Test Backend Endpoints
```bash
# Test users endpoint (should return 401 without auth)
curl -s -w "\nStatus: %{http_code}\n" https://connectme.be.totesoft.com/api/v1/users/

# Test with mock login
curl -X POST https://connectme.be.totesoft.com/api/v1/auth/mock/login/
```

### Test Frontend
1. Open browser console (F12)
2. Navigate to https://connectme.apps.totesoft.com
3. Login with Keycloak credentials
4. Check for any errors in console
5. Navigate to Admin → User Management

---

## 🐛 **Known Issues**

### 1. Admin Menu Not Visible
- **Symptom**: Admin dropdown doesn't appear in navigation
- **Cause**: User role not populated in JWT token
- **Solution**: Check Keycloak role mappings, ensure roles are included in token

### 2. 401 Unauthorized on User Management
- **Symptom**: Cannot fetch users list
- **Cause**: Keycloak token not being sent or invalid
- **Solution**: Check localStorage for `kc_access_token`, re-login if expired

### 3. Celery Health Check Errors
- **Symptom**: `KeyError: 'health_check_monitor'` in celery logs
- **Status**: Non-critical, doesn't affect functionality
- **Fix**: Pending - need to add health_check_monitor task

---

## 📊 **Deployment Status**

### Production (https://connectme.apps.totesoft.com)
- ✅ Backend: Running (Gunicorn)
- ✅ Frontend: Running (PM2)
- ✅ User Management API: Active
- ✅ Keycloak Sync: Implemented
- ⚠️ Admin Menu: May not be visible (role issue)

### Local Development (http://localhost:3000)
- ✅ Backend: Running (Django dev server)
- ✅ Frontend: Running (Next.js dev server)
- ✅ User Management: Accessible at /users

---

## 🔄 **Deployment Commands**

### Full Deployment
```bash
./service.sh remote deploy
```

### Backend Only
```bash
./service.sh remote deploy backend
```

### Frontend Only
```bash
./service.sh remote deploy frontend
```

### Restart Services
```bash
./service.sh remote restart
```

### Check Status
```bash
./service.sh remote status
```

---

## 📝 **Change Log**

### Oct 16, 2025
- ✅ Fixed missing `/api/v1/users/` route
- ✅ Added `django-sslserver` dependency
- ✅ Fixed `APIView` import errors
- ✅ Deployed Keycloak sync implementation
- ✅ Fixed frontend `lucide-react` dependency
- ✅ Cleared Python cache issues
- ✅ Updated navigation to include User Management

---

## 🆘 **Support**

For issues or questions:
1. Check logs: `./service.sh remote logs backend`
2. Check status: `./service.sh remote status`
3. Review this documentation
4. Check browser console for frontend errors
5. Review backend logs for API errors

---

**Last Updated**: October 16, 2025  
**Status**: ✅ Operational (with known issues)

