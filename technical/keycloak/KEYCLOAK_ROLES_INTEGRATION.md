# 🔐 Keycloak Roles & Business Logic Integration

## Overview

Your application uses Keycloak roles for authorization and access control. Here's how they integrate:

---

## 🎭 Roles in Keycloak

### Realm Roles (Create These)

| Role | Description | Permissions |
|------|-------------|-------------|
| `admin` | Full administrator | All features, user management, settings |
| `manager` | Practice manager | View/edit claims, reports, bulk processing |
| `staff` | Staff member | View claims, basic search |
| `billing` | Billing specialist | Claims, payments, reports |

---

## 🔗 How Roles Integrate

### 1. **Frontend (React)**

The frontend receives roles in the JWT token and controls UI visibility:

```typescript
// In your React components
import { useAuth } from '@/contexts/AuthContext';

function AdminPanel() {
  const { user } = useAuth();
  
  // Check if user has admin role
  const hasAdminRole = user?.roles?.includes('admin');
  
  if (!hasAdminRole) {
    return <div>Access Denied</div>;
  }
  
  return <div>Admin Panel Content</div>;
}
```

**Current Implementation:**
- `src/contexts/AuthContext.tsx` - Stores user info with roles
- `src/lib/keycloak.ts` - Fetches user info including roles
- Roles are in: `user.realm_access.roles` or `user.roles`

### 2. **Backend (Django)**

The backend validates roles from the JWT token:

```python
# In your Django views
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Roles are extracted from JWT by KeycloakAuthentication
        user_roles = request.user.roles  # From JWT token
        return 'admin' in user_roles

# Use in views
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Only admins can access this
        return Response({'message': 'Admin data'})
```

**Current Implementation:**
- `apps/auth/keycloak.py` - Extracts roles from JWT
- Roles stored in: `request.user.roles` after authentication
- Django permissions check these roles

---

## 📊 Role-Based Access Control (RBAC)

### Frontend Routes

```typescript
// Example: Protect routes by role
const routes = {
  '/dashboard': ['admin', 'manager', 'staff', 'billing'],
  '/admin': ['admin'],
  '/claims': ['admin', 'manager', 'staff', 'billing'],
  '/bulk-upload': ['admin', 'manager'],
  '/users': ['admin'],
  '/settings': ['admin', 'manager'],
};
```

### Backend API Endpoints

```python
# Example: Protect endpoints by role
urlpatterns = [
    # Anyone authenticated
    path('claims/', ClaimsView.as_view()),  
    
    # Admin only
    path('admin/users/', AdminUsersView.as_view()),  
    
    # Admin or Manager
    path('bulk-upload/', BulkUploadView.as_view()),  
]
```

---

## 🔧 Implementation in Your Code

### 1. **Keycloak JWT Token Structure**

When a user logs in, they receive a JWT token like this:

```json
{
  "sub": "user-id-123",
  "preferred_username": "testuser",
  "email": "test@connectme.com",
  "realm_access": {
    "roles": ["admin", "offline_access", "uma_authorization"]
  },
  "resource_access": {
    "connectme-frontend": {
      "roles": ["user"]
    }
  }
}
```

### 2. **Frontend: Extract Roles**

Update `src/lib/keycloak.ts` to extract roles:

```typescript
export interface UserInfo {
  sub: string;
  preferred_username: string;
  email?: string;
  given_name?: string;
  family_name?: string;
  name?: string;
  roles?: string[];  // Add this
}

// In fetchUserInfo method:
async fetchUserInfo(accessToken?: string): Promise<UserInfo | null> {
  // ... existing code ...
  
  const userInfo: UserInfo = await response.json();
  
  // Decode JWT to get roles
  const tokenParts = token.split('.');
  const payload = JSON.parse(atob(tokenParts[1]));
  userInfo.roles = payload.realm_access?.roles || [];
  
  // Store user info
  localStorage.setItem(this.userInfoKey, JSON.stringify(userInfo));
  
  return userInfo;
}
```

### 3. **Backend: Extract Roles**

Your `apps/auth/keycloak.py` already extracts roles:

```python
class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # ... existing code ...
        
        # Extract roles from token
        roles = payload.get('realm_access', {}).get('roles', [])
        
        # Attach to user object
        user.roles = roles
        
        return (user, None)
```

### 4. **Create Permission Classes**

Create `apps/auth/permissions.py`:

```python
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'roles') and 'admin' in request.user.roles

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'roles'):
            return False
        return any(role in request.user.roles for role in ['admin', 'manager'])

class IsBillingOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'roles'):
            return False
        return any(role in request.user.roles for role in ['admin', 'billing'])
```

### 5. **Use in Views**

```python
from rest_framework.views import APIView
from apps.auth.permissions import IsAdmin, IsManagerOrAdmin

class BulkUploadView(APIView):
    permission_classes = [IsManagerOrAdmin]
    
    def post(self, request):
        # Only admins and managers can upload
        return Response({'status': 'success'})

class UserManagementView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Only admins can manage users
        return Response({'users': []})
```

---

## 🎯 Business Logic Integration

### Example 1: Claims Access

```python
# Backend
class ClaimsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        
        if 'admin' in user.roles:
            # Admins see all claims
            return Claim.objects.all()
        elif 'manager' in user.roles:
            # Managers see their organization's claims
            return Claim.objects.filter(organization=user.organization)
        else:
            # Staff see only their own claims
            return Claim.objects.filter(user=user)
```

### Example 2: Bulk Processing

```python
# Backend
class BulkProcessingView(APIView):
    permission_classes = [IsManagerOrAdmin]
    
    def post(self, request):
        # Only managers and admins can do bulk processing
        csv_file = request.FILES['file']
        # Process CSV...
        return Response({'status': 'processing'})
```

### Example 3: Frontend UI

```typescript
// Frontend
function Dashboard() {
  const { user } = useAuth();
  const isAdmin = user?.roles?.includes('admin');
  const isManager = user?.roles?.includes('manager');
  
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Everyone sees this */}
      <ClaimsSearch />
      
      {/* Only managers and admins see this */}
      {(isManager || isAdmin) && <BulkUpload />}
      
      {/* Only admins see this */}
      {isAdmin && <UserManagement />}
    </div>
  );
}
```

---

## 📋 Configuration Checklist

- [ ] Create realm roles in Keycloak
- [ ] Assign roles to users
- [ ] Update frontend to extract roles from JWT
- [ ] Create Django permission classes
- [ ] Apply permissions to API views
- [ ] Test role-based access

---

## 🧪 Testing Roles

### Test with curl

```bash
# Get token for testuser (with admin role)
TOKEN=$(curl -s -X POST https://auth.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password" | jq -r '.access_token')

# Decode token to see roles
echo $TOKEN | cut -d'.' -f2 | base64 -d | jq '.realm_access.roles'

# Test API with token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/claims/
```

### Test in Frontend

1. Login as `testuser`
2. Open browser console
3. Check: `localStorage.getItem('kc_user_info')`
4. Should see roles in the user object

---

## 🎉 Summary

**Roles are integrated at multiple levels:**

1. **Keycloak** - Defines and assigns roles
2. **JWT Token** - Carries roles to frontend/backend
3. **Frontend** - Controls UI visibility based on roles
4. **Backend** - Enforces permissions on API endpoints
5. **Database** - Filters data based on roles

**Your current setup already supports this!** You just need to:
1. Create the roles in Keycloak
2. Assign them to users
3. Use them in your business logic

---

## 📚 Next Steps

1. **Configure Keycloak** - Create client, users, and roles
2. **Test Authentication** - Verify token contains roles
3. **Implement Permissions** - Add role checks to views
4. **Test Access Control** - Verify different roles see different data

**Ready to configure Keycloak?** Follow the checklist above! 🚀
