# Roles & Permissions Guide

**Control access to ConnectMe features using role-based permissions.**

This guide explains how to configure user roles in both Keycloak and Django to control what users can see and do.

## 🎯 How to See User Management in Frontend

> **Quick Answer:** To see the User Management menu in the frontend, a user must have either `admin` or `manager` role assigned in Keycloak.

### Frontend Permission Requirements

The "⚙️ Admin" menu (which includes User Management) is only visible to users with specific roles:

- ✅ **admin** role - Full access to all admin features
- ✅ **manager** role - Access to user management within their organization
- ❌ **staff, billing, api_user, read_only** - Cannot see admin menu

### Backend API Permission Requirements

The User Management API endpoints require `IsManagerOrAdmin` permission:

- **List Users:** admin or manager
- **Create User:** admin or manager
- **Update User:** admin or manager
- **Delete User:** admin only
- **Reset Password:** admin or manager

## 🔧 How to Set User Permissions

### Option 1: Set Role in Keycloak (Recommended)

1. **Login to Keycloak Admin Console**
   - URL: `https://auth.totesoft.com`
   - Use your Keycloak admin credentials

2. **Navigate to the User**
   - Select realm: `connectme-preprod`
   - Go to: **Users** → Find user → Click **Edit**

3. **Assign Role via Groups (Preferred)**
   - Go to **Groups** tab
   - Click **Join Group**
   - Select `/admin` or `/manager` group
   - Click **Join**

4. **Alternative: Assign via Realm Roles**
   - Go to **Role Mappings** tab
   - Under **Realm Roles**, assign `admin` or `manager`

5. **User Must Re-login**
   - Changes take effect after logout/login

### Option 2: Set Role in Django (Temporary)

1. **SSH to Server**
   ```bash
   ssh connectme@169.59.163.43
   ```

2. **Access Django Shell**
   ```bash
   cd /var/www/connectme-preprod-backend
   source venv/bin/activate
   python manage.py shell
   ```

3. **Update User Role**
   ```python
   from apps.users.models import User

   # Find user
   user = User.objects.get(username='your_username')

   # Set role
   user.role = 'admin'  # or 'manager'
   user.save()

   print(f"✅ User {user.username} role set to: {user.role}")
   ```

⚠️ **Important:** Django-only changes will be overwritten by Keycloak on next login. Always set roles in Keycloak for permanent effect.

## 📊 Available Roles

| Role | Code | Access Level | Use Case |
|------|------|-------------|----------|
| **Administrator** | `admin` | Full System Access | System administrators, IT staff |
| **Manager** | `manager` | Organization-wide | Department managers, supervisors |
| **Staff** | `staff` | Standard User | Healthcare staff, claims processors |
| **Billing** | `billing` | Financial Data | Billing department staff |
| **API User** | `api_user` | Programmatic Only | Automated systems, integrations |
| **Read Only** | `read_only` | View Only | Auditors, external reviewers |

## 🔐 Permission Matrix

| Feature | Admin | Manager | Staff | Billing | API User | Read Only |
|---------|-------|---------|-------|---------|----------|-----------|
| **View Dashboard** | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Search Claims** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Bulk Upload** | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| **View History** | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Workflow Management** | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Approve Workflow** | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **User Management** | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Delete Users** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **System Settings** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **View Audit Logs** | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Export Data** | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |
| **API Access** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## 🔍 How Roles Are Extracted

The system extracts roles from Keycloak tokens in this priority order:

1. **Keycloak Groups** (e.g., `/admin`, `/manager`) - **Highest Priority**
2. **Realm Access Roles** (e.g., `admin`, `manager`) - **Fallback**
3. **Default:** `staff` if no valid role found

💡 **Best Practice:** Use Keycloak Groups for role assignment. They are more specific and easier to manage than realm roles.

## ✅ Verification Steps

### 1. Check Frontend Role Display
1. Login to the frontend
2. Open browser console (F12)
3. Look for: `[Navbar] User role: <your_role>`

### 2. Verify Keycloak Token
1. Open browser console (F12)
2. Run: `localStorage.getItem('kc_access_token')`
3. Copy the token
4. Go to [jwt.io](https://jwt.io)
5. Paste token and check `groups` or `realm_access.roles` fields

### 3. Check Django Database
```bash
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py shell

from apps.users.models import User
user = User.objects.get(username='your_username')
print(f"Role: {user.role}")
```

## 🐛 Troubleshooting

### User Can't See Admin Menu
- ✓ Verify role is set to `admin` or `manager` in Keycloak
- ✓ User must logout and login again for changes to take effect
- ✓ Clear browser cache and localStorage
- ✓ Check browser console for role value

### Role Changes Not Taking Effect
- ✓ Ensure role is set in Keycloak (not just Django)
- ✓ User must re-authenticate (logout/login)
- ✓ Check Keycloak token includes the role
- ✓ Verify frontend is reading role from token correctly

### Permission Denied Errors
- ✓ Check user's role in Django database
- ✓ Verify API endpoint permission requirements
- ✓ Check backend logs for permission errors
- ✓ Ensure user is in correct organization

## 📚 Related Documentation

- [User Management Guide](user-management.md)
- [Keycloak Configuration](keycloak-config.md)
- [Troubleshooting Login Issues](../troubleshooting/login-issues.md)
- [Authentication Technical Details](../developer/authentication.md)

---

[← Back to Admin Guide](index.md) | [Home](../index.html)

