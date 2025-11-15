# Role Management Implementation Audit

## Summary
Comprehensive audit of role-based access control (RBAC) implementation across the ConnectMe platform.

---

## 1. Keycloak Configuration

### Realm Roles (from keycloak-realm-connectme-preprod-complete.json)

#### **Admin Role**
- **Name:** `admin`
- **Description:** "Full administrator access to all features"
- **Composite:** Yes
- **Client Permissions:**
  - `claim:admin`
  - `eligibility:admin`
  - `user:admin`
  - `organization:admin`
  - `bulk:process`
  - `report:view`
  - `report:export`
  - `audit:view`
  - `settings:manage`

#### **Manager Role**
- **Name:** `manager`
- **Description:** "Practice manager with elevated permissions"
- **Composite:** Yes
- **Client Permissions:**
  - `claim:read`
  - `claim:write`
  - `eligibility:read`
  - `user:read`
  - `bulk:process`
  - `report:view`

#### **Staff Role**
- **Name:** `staff`
- **Description:** "Staff member with basic access"
- **Composite:** Yes
- **Client Permissions:**
  - `claim:read`
  - `eligibility:read`

---

## 2. Backend Implementation

### User Model (`apps/users/models.py`)

#### Role Choices
```python
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('staff', 'Staff'),
    ('billing', 'Billing'),
    ('api_user', 'API User'),
    ('read_only', 'Read Only'),
]
```

#### Role Field
- **Type:** CharField
- **Max Length:** 50
- **Default:** 'staff'
- **Choices:** See above

---

### Authentication (`apps/auth/keycloak.py`)

#### Token Validation
- **Class:** `KeycloakAuthentication`
- **Method:** `validate_token(token)`
- **Signature Verification:** 
  - **Production:** Full JWT signature verification with Keycloak public key
  - **Pre-Prod/Dev:** Can skip signature verification (controlled by `KEYCLOAK_SKIP_SIGNATURE_VERIFICATION`)

#### User Creation/Update
- **Method:** `get_or_create_user(token_data)`
- **Extracts:**
  - `username` (from `preferred_username` or `sub`)
  - `email`
  - `first_name` (from `given_name`)
  - `last_name` (from `family_name`)

**⚠️ ISSUE IDENTIFIED:**
- **Role extraction is NOT implemented in the backend!**
- The backend does not extract roles from the Keycloak token
- User role defaults to 'staff' on creation
- Roles must be manually updated in Django admin or via API

---

### Permission Classes (`apps/users/permissions.py`)

#### 1. **IsAdminUser**
- **Check:** `user.role == 'admin'`
- **Use Case:** Admin-only actions

#### 2. **IsManagerOrAdmin**
- **Check:** `user.role in ['admin', 'manager']`
- **Use Case:** Manager/Admin actions

#### 3. **IsOwnerOrAdmin**
- **Check:** Admin can access all, users can access their own objects
- **Use Case:** Object-level permissions

#### 4. **CanManageUsers**
- **Check:** 
  - Admin: Can manage anyone
  - Manager: Can manage users in their org (except admins)
- **Use Case:** User management endpoints

#### 5. **CanViewPHI**
- **Check:** `user.phi_access_level in ['limited', 'full']`
- **Use Case:** PHI data access

#### 6. **CanAccessOrganization**
- **Check:** Admin can access all, users can access their org
- **Use Case:** Organization-level permissions

---

### Workflow Permissions (`apps/workflow/permissions.py`)

Uses `getattr(user, 'roles', [])` - expects a list of roles, but the User model has a single `role` field (string).

**⚠️ ISSUE IDENTIFIED:**
- Workflow permissions check for `'admin' in user.roles` (list)
- But User model has `user.role` (string)
- This mismatch could cause permission errors

---

## 3. Frontend Implementation

### Role Extraction (`src/lib/keycloak.ts`)

#### Method: `fetchUserInfo()`
```typescript
// Extract role from JWT token
const tokenPayload = JSON.parse(atob(token.split('.')[1]));

// Priority 1: Check groups
if (tokenPayload.groups && tokenPayload.groups.length > 0) {
  userInfo.role = tokenPayload.groups[0];
  userInfo.roles = tokenPayload.groups;
}
// Priority 2: Fall back to realm roles
else {
  userInfo.role = tokenPayload.realm_access?.roles?.[0] || 'user';
  userInfo.roles = tokenPayload.realm_access?.roles || [];
}
```

**✅ WORKING:** Frontend correctly extracts roles from Keycloak token

---

### Role-Based UI (`src/components/Navbar.tsx`)

#### Admin Menu Restriction
```typescript
// Skip admin menu for non-admin users
if (item.adminOnly && user?.role !== 'admin' && user?.role !== 'manager') {
  return null;
}
```

**✅ WORKING:** Admin menu hidden for staff users

---

### Authentication Context (`src/contexts/AuthContext.tsx`)

Stores user info including role in:
- State: `user` object
- LocalStorage: `kc_user_info`

**✅ WORKING:** Role persisted across page refreshes

---

## 4. API Endpoints Using Permissions

### User Management (`apps/users/api_views.py`)
- **List Users:** `IsAuthenticated` ✅
- **Create User:** `CanManageUsers` ✅
- **Update User:** `CanManageUsers` ✅
- **Delete User:** `IsAdminUser` ✅

### Claims (`apps/claims/api_views.py`)
- **Search Claims:** `IsAuthenticated` ✅
- **Bulk Upload:** `IsAuthenticated` ✅

### Providers (`apps/providers/api_views.py`)
- **List Practices:** `IsAuthenticated` ✅
- **Practice Access:** Filtered by user's assigned practices ✅

### Workflow (`apps/workflow/views.py`)
- **Dashboard:** `IsAuthenticated` ✅
- **Work Items:** Custom permissions (CanViewWorkItem, CanManageWorkItem) ⚠️

---

## 5. Issues Identified

### 🔴 **Critical Issues**

#### 1. **Backend Does NOT Extract Roles from Keycloak**
**Problem:**
- `KeycloakAuthentication.get_or_create_user()` does not extract role from token
- User role defaults to 'staff' on creation
- Roles must be manually updated

**Impact:**
- New users from Keycloak always get 'staff' role
- Admin/Manager roles not automatically assigned
- Manual intervention required for every new user

**Solution:**
```python
def get_or_create_user(self, token_data):
    # ... existing code ...
    
    # Extract role from token
    role = 'staff'  # default
    
    # Check groups first (more specific)
    if 'groups' in token_data and token_data['groups']:
        # Extract role from group name (e.g., "/admin" -> "admin")
        group = token_data['groups'][0].strip('/').lower()
        if group in dict(User.ROLE_CHOICES):
            role = group
    # Fall back to realm roles
    elif 'realm_access' in token_data and 'roles' in token_data['realm_access']:
        roles = token_data['realm_access']['roles']
        for r in roles:
            if r.lower() in dict(User.ROLE_CHOICES):
                role = r.lower()
                break
    
    # Get or create user with role
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,  # ADD THIS
        }
    )
    
    # Update role if changed
    if not created and user.role != role:
        user.role = role
        user.save()
```

---

#### 2. **Workflow Permissions Use Wrong Role Attribute**
**Problem:**
- Workflow permissions check `'admin' in user.roles` (list)
- User model has `user.role` (string)
- Mismatch causes permission checks to fail

**Impact:**
- Workflow permissions may not work correctly
- Admin users might not have admin access to workflow features

**Solution:**
Update `apps/workflow/permissions.py` to use `user.role` instead of `user.roles`:
```python
# Before:
if 'admin' in getattr(user, 'roles', []):

# After:
if getattr(user, 'role', '') == 'admin':
```

---

### ⚠️ **Medium Issues**

#### 3. **No Role Synchronization**
**Problem:**
- If a user's role changes in Keycloak, it's not updated in Django
- User must logout/login for role changes to take effect
- Even then, backend won't update the role

**Impact:**
- Role changes require manual database updates
- Inconsistency between Keycloak and Django

**Solution:**
- Implement role sync in `get_or_create_user()`
- Update user role on every authentication

---

#### 4. **No Client-Level Permissions**
**Problem:**
- Keycloak has fine-grained client permissions (e.g., `claim:admin`, `bulk:process`)
- Backend only checks role, not specific permissions
- Frontend doesn't check specific permissions

**Impact:**
- Cannot implement fine-grained access control
- All admins have all permissions (no separation of duties)

**Solution:**
- Extract `resource_access` from Keycloak token
- Store client permissions in User model or cache
- Check specific permissions in permission classes

---

### ✅ **Working Features**

1. **Frontend Role Extraction** - Correctly extracts roles from Keycloak token
2. **Frontend UI Restrictions** - Admin menu hidden for non-admin users
3. **Backend Permission Classes** - Well-defined permission classes
4. **User Model** - Has role field with appropriate choices
5. **Practice Access Control** - Many-to-many relationship working

---

## 6. Testing Checklist

### Backend Role Management
- [ ] Create user in Keycloak with 'admin' role
- [ ] Login via frontend
- [ ] Check if Django user has 'admin' role (currently fails ❌)
- [ ] Create user in Keycloak with 'manager' role
- [ ] Login via frontend
- [ ] Check if Django user has 'manager' role (currently fails ❌)
- [ ] Create user in Keycloak with 'staff' role
- [ ] Login via frontend
- [ ] Check if Django user has 'staff' role (works by default ✅)

### Frontend Role Restrictions
- [x] Login as admin → See admin menu ✅
- [x] Login as manager → See admin menu ✅
- [x] Login as staff → Admin menu hidden ✅

### API Permissions
- [ ] Admin user can access `/api/v1/users/users/` ✅
- [ ] Manager user can access `/api/v1/users/users/` ✅
- [ ] Staff user cannot access `/api/v1/users/users/` (should test)
- [ ] Admin user can create/update/delete users ✅
- [ ] Manager user can create/update users (but not admins) ✅
- [ ] Staff user cannot create/update/delete users (should test)

### Workflow Permissions
- [ ] Admin user can view all work items (needs fixing ⚠️)
- [ ] Manager user can view team work items (needs fixing ⚠️)
- [ ] Staff user can view assigned work items (needs fixing ⚠️)

---

## 7. Recommended Fixes

### Priority 1: Fix Backend Role Extraction
**File:** `connectme-backend/apps/auth/keycloak.py`
**Method:** `get_or_create_user()`
**Action:** Extract role from Keycloak token and set on user

### Priority 2: Fix Workflow Permissions
**File:** `connectme-backend/apps/workflow/permissions.py`
**Action:** Change `user.roles` (list) to `user.role` (string)

### Priority 3: Add Role Sync
**File:** `connectme-backend/apps/auth/keycloak.py`
**Method:** `get_or_create_user()`
**Action:** Update user role on every authentication

### Priority 4: Add Client Permission Support
**Files:** 
- `connectme-backend/apps/users/models.py` (add permissions field)
- `connectme-backend/apps/auth/keycloak.py` (extract permissions)
- Permission classes (check specific permissions)

---

## 8. Current State Summary

### ✅ **What's Working:**
1. Keycloak authentication
2. Frontend role extraction and UI restrictions
3. Backend permission classes (structure)
4. Practice-based access control

### ❌ **What's NOT Working:**
1. Backend role extraction from Keycloak
2. Workflow permissions (role attribute mismatch)
3. Role synchronization
4. Fine-grained client permissions

### ⚠️ **Workarounds Currently Needed:**
1. Manually set user roles in Django admin after first login
2. Manually update roles when changed in Keycloak

---

## 9. Next Steps

1. **Implement backend role extraction** (Priority 1)
2. **Fix workflow permissions** (Priority 2)
3. **Test all permission scenarios**
4. **Document role assignment process**
5. **Consider implementing client-level permissions** (future enhancement)

---

**Date:** November 9, 2025  
**Status:** 🟡 **Partially Implemented** - Frontend works, backend needs fixes  
**Risk Level:** 🔴 **High** - Security implications if roles not properly enforced

