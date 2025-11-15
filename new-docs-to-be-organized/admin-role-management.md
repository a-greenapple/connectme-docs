# Admin Role Management Guide

## Overview
The ConnectMe Healthcare portal uses role-based access control to restrict admin features like User Management to authorized users only.

## Role Assignment System

### Current Setup
- **Authentication**: Handled by Keycloak
- **Role Storage**: Roles can be stored in both Django database and Keycloak
- **Role Checking**: Frontend checks user roles from Keycloak token

### Admin Access Requirements

The Administration menu (containing User Management) is only visible to users with:

1. `user.role === 'admin'`
2. `user.role === 'manager'`
3. `user.roles` array containing `'admin'` or `'manager'`
4. Keycloak permission roles like `'user:admin'` or `'claim:admin'`

## How to Assign Admin Role

### Method 1: Backend Database Assignment
```bash
# SSH to server
ssh connectme@169.59.163.43

# Navigate to backend
cd /var/www/connectme-preprod-backend

# Activate virtual environment
source venv/bin/activate

# Run role assignment script
python assign_admin_role.py admin
```

### Method 2: Keycloak Assignment
1. Login to Keycloak admin console
2. Navigate to Users → [Username]
3. Go to Role Mappings tab
4. Assign 'admin' or 'manager' realm role
5. Save changes

## Testing Admin Access

### Check Current User Role
1. Open browser developer console (F12)
2. Login to https://pre-prod.connectme.apps.totessoft.com
3. Look for console logs:
   ```
   [Navbar] hasAdminAccess: true/false
   [Navbar] user.role: admin/manager/undefined
   [Navbar] user.roles: [array of roles]
   ```

### Expected Behavior
- **With admin role**: Administration menu visible in navigation
- **Without admin role**: Administration menu hidden
- **With admin access**: Can access User Management, System Logs, Settings

## Troubleshooting

### Administration Menu Not Visible

1. **Check Console Logs**
   - Open browser console
   - Refresh page
   - Look for `[Navbar] hasAdminAccess: false`

2. **Verify Role Assignment**
   ```bash
   # Check Django database
   cd /var/www/connectme-preprod-backend
   source venv/bin/activate
   python manage.py shell

   from apps.users.models import User
   user = User.objects.get(username='admin')
   print(f"Role: {user.role}")
   print(f"Is Staff: {user.is_staff}")
   ```

3. **Check Keycloak Token**
   - Login to the application
   - Open browser developer tools
   - Go to Application/Storage → Local Storage
   - Look for `kc_access_token`
   - Decode the JWT token to see role claims

### Common Issues

1. **Role in Django but not Keycloak**: User role needs to be synced to Keycloak
2. **Token doesn't contain role**: Keycloak client mappings need configuration
3. **Case sensitivity**: Ensure role names match exactly ('admin' not 'Admin')

## Role Hierarchy

```
admin (Full Access)
├── User Management (CRUD)
├── System Logs (View)
├── Settings (Modify)
└── All regular user features

manager (Limited Admin)
├── User Management (Read/Update)
├── System Logs (View)
└── All regular user features

staff (Regular User)
├── Dashboard
├── Claims Search
├── Workflow
└── Help
```

## Security Notes

- Admin roles should be assigned sparingly
- Regular audits of admin users recommended
- Role changes require re-authentication to take effect
- Console debug logs should be removed in production

## Scripts Available

- `assign_admin_role.py` - Assign admin role to Django user
- `create_admin.py` - Create new admin user with default org
- `test_role_management.py` - Test role assignments

## Status

**Current Status**: Role checking implemented and working
**Last Updated**: 2024-11-15
**Environment**: Pre-Production