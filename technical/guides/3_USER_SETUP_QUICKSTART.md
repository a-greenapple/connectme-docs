# User Management - Quick Start Guide

## Initial Setup Before Staging

Follow these steps to set up user management for your staging environment.

---

## Step 1: Create Initial Organization

```bash
# SSH into your server
ssh connectme@your-server.com

# Activate Python environment
cd /opt/connectme/backend
source ../venv/bin/activate

# Open Django shell
python manage.py shell
```

```python
from apps.users.models import Organization

# Create your organization
org = Organization.objects.create(
    name="Your Healthcare Organization",
    npi="1234567890",  # Your actual NPI
    tin="123456789",   # Your actual TIN
    address_line1="123 Main St",
    city="Your City",
    state="CA",
    zip_code="12345",
    phone="555-1234",
    email="admin@yourorg.com",
    active=True
)

print(f"Organization created: {org.id}")
```

---

## Step 2: Create Initial Admin User

```python
from apps.users.models import User

# Create admin user
admin = User.objects.create_superuser(
    username="admin",
    email="admin@yourorg.com",
    password="ChangeThisPassword123!",  # Change this!
    first_name="Admin",
    last_name="User",
    organization=org,
    role="admin"
)

print(f"Admin user created: {admin.email}")
```

---

## Step 3: Create Keycloak Users

### Option A: Manual (Recommended for Testing)

1. Go to your Keycloak admin console: `https://auth.totesoft.com/admin/`
2. Select realm: `connectme`
3. Go to Users → Add user
4. Fill in:
   - Username: `admin@yourorg.com`
   - Email: `admin@yourorg.com`
   - First name: `Admin`
   - Last name: `User`
   - Email verified: ON
5. Click "Create"
6. Go to "Credentials" tab
7. Set password: `ChangeThisPassword123!`
8. Temporary: OFF
9. Click "Set Password"

Repeat for additional users.

---

### Option B: Import from JSON

Create `users.json`:
```json
{
  "users": [
    {
      "username": "admin@yourorg.com",
      "email": "admin@yourorg.com",
      "firstName": "Admin",
      "lastName": "User",
      "emailVerified": true,
      "enabled": true,
      "credentials": [
        {
          "type": "password",
          "value": "ChangeThisPassword123!",
          "temporary": false
        }
      ],
      "realmRoles": ["user"],
      "clientRoles": {
        "connectme-frontend": ["admin", "claims:admin"]
      }
    }
  ]
}
```

Import in Keycloak:
1. Go to realm settings
2. Click "Import"
3. Upload `users.json`

---

## Step 4: Test Login

```bash
# Test with Django admin
curl -X POST https://your-server.com/api/v1/auth/mock/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourorg.com",
    "password": "ChangeThisPassword123!"
  }'
```

If successful, you'll get:
```json
{
  "user": {...},
  "access_token": "...",
  "refresh_token": "..."
}
```

---

## Step 5: Create Additional Users via API

```bash
# Get access token first
TOKEN="your-access-token-from-login"

# Create manager user
curl -X POST https://your-server.com/api/v1/auth/users/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "manager",
    "email": "manager@yourorg.com",
    "password": "ManagerPass123!",
    "password_confirm": "ManagerPass123!",
    "first_name": "John",
    "last_name": "Manager",
    "role": "manager",
    "department": "Operations"
  }'

# Create staff user
curl -X POST https://your-server.com/api/v1/auth/users/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "staff.user",
    "email": "staff@yourorg.com",
    "password": "StaffPass123!",
    "password_confirm": "StaffPass123!",
    "first_name": "Jane",
    "last_name": "Staff",
    "role": "staff",
    "department": "Billing"
  }'

# Create billing user
curl -X POST https://your-server.com/api/v1/auth/users/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "billing.user",
    "email": "billing@yourorg.com",
    "password": "BillingPass123!",
    "password_confirm": "BillingPass123!",
    "first_name": "Bob",
    "last_name": "Billing",
    "role": "billing",
    "department": "Finance"
  }'
```

---

## Step 6: Bulk Import Users (Optional)

Create `users_import.csv`:
```csv
email,first_name,last_name,role,department
analyst1@yourorg.com,Alice,Analyst,staff,Claims
analyst2@yourorg.com,Bob,Smith,staff,Claims
supervisor@yourorg.com,Carol,Supervisor,manager,Operations
readonly@yourorg.com,David,Viewer,read_only,Reports
```

Convert to JSON and import:
```bash
curl -X POST https://your-server.com/api/v1/auth/users/bulk_import/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "users": [
      {
        "email": "analyst1@yourorg.com",
        "first_name": "Alice",
        "last_name": "Analyst",
        "role": "staff"
      },
      {
        "email": "analyst2@yourorg.com",
        "first_name": "Bob",
        "last_name": "Smith",
        "role": "staff"
      },
      {
        "email": "supervisor@yourorg.com",
        "first_name": "Carol",
        "last_name": "Supervisor",
        "role": "manager"
      },
      {
        "email": "readonly@yourorg.com",
        "first_name": "David",
        "last_name": "Viewer",
        "role": "read_only"
      }
    ]
  }'
```

---

## Step 7: Verify User Setup

```bash
# List all users
curl https://your-server.com/api/v1/auth/users/ \
  -H "Authorization: Bearer $TOKEN" | jq

# Get user statistics
curl https://your-server.com/api/v1/auth/users/stats/ \
  -H "Authorization: Bearer $TOKEN" | jq

# Get available roles
curl https://your-server.com/api/v1/auth/roles/ \
  -H "Authorization: Bearer $TOKEN" | jq
```

Expected output:
```json
{
  "total_users": 5,
  "active_users": 5,
  "inactive_users": 0,
  "by_role": {
    "Admin": 1,
    "Manager": 1,
    "Staff": 2,
    "Billing": 1,
    "API User": 0,
    "Read Only": 0
  },
  "recent_logins": 1
}
```

---

## Step 8: Configure Keycloak Roles

For each user in Keycloak:

1. Go to Users → Select user
2. Go to "Role Mapping" tab
3. Assign client roles from `connectme-frontend`:
   - Admin users: `admin`, `claims:admin`, `claims:read`, `claims:export`
   - Manager users: `manager`, `claims:read`, `claims:export`
   - Staff users: `staff`, `claims:read`
   - Billing users: `billing`, `claims:read`, `claims:export`
   - Read-only users: `read_only`, `claims:read`

---

## Step 9: Test User Access

### Test Admin Access
```bash
# Login as admin
curl -X POST https://your-server.com/api/v1/auth/keycloak/callback/ \
  -H "Content-Type: application/json" \
  -d '{"code": "auth-code-from-keycloak"}'

# Test admin actions
curl https://your-server.com/api/v1/auth/users/stats/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Test Manager Access
```bash
# Login as manager
# Test manager actions
curl https://your-server.com/api/v1/auth/users/?role=staff \
  -H "Authorization: Bearer $MANAGER_TOKEN"
```

### Test Staff Access
```bash
# Login as staff
# Test claims search
curl https://your-server.com/api/v1/claims/search/ \
  -H "Authorization: Bearer $STAFF_TOKEN" \
  -d '{...}'
```

---

## Step 10: Security Checklist

- [ ] Changed default admin password
- [ ] Created at least 3 users (admin, manager, staff)
- [ ] Assigned correct roles in Django
- [ ] Assigned correct roles in Keycloak
- [ ] Tested login for each role
- [ ] Tested permissions for each role
- [ ] Configured MFA in Keycloak (recommended)
- [ ] Set password expiration policy (recommended)
- [ ] Enabled audit logging (recommended)

---

## Common Issues & Solutions

### Issue: User can't log in

**Solution:**
1. Check user is active: `is_active=True`
2. Check Keycloak user exists and is enabled
3. Check email matches between Django and Keycloak
4. Check password is correct
5. Check account is not locked

```python
# Unlock user
from apps.users.models import User
user = User.objects.get(email='user@yourorg.com')
user.failed_login_attempts = 0
user.account_locked_until = None
user.save()
```

---

### Issue: Permission denied

**Solution:**
1. Check user role is correct
2. Check Keycloak roles are assigned
3. Check endpoint permissions
4. Check organization matches

```python
# Update user role
user = User.objects.get(email='user@yourorg.com')
user.role = 'manager'
user.save()
```

---

### Issue: Keycloak sync not working

**Solution:**
1. Check Keycloak URL in .env
2. Check client credentials
3. Manually sync:

```bash
curl -X POST https://your-server.com/api/v1/auth/sync/keycloak/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## Recommended User Structure for Testing

```
Admin (1 user)
  └── Can do everything

Managers (2-3 users)
  └── Team leads, supervisors
  └── Can manage staff
  └── Can view all data

Staff (5-10 users)
  └── Claims processors
  └── Can search claims
  └── Can upload CSV

Billing (2-3 users)
  └── Financial staff
  └── Can view payments
  └── Can export data

Read-Only (1-2 users)
  └── Auditors, viewers
  └── Can only view
  └── No modifications
```

---

## Next Steps

After user setup:
1. Test login with each role
2. Verify permissions work correctly
3. Test claims search with staff user
4. Test user management with manager
5. Test bulk operations with admin
6. Configure password policies in Keycloak
7. Enable MFA in Keycloak
8. Set up audit logging
9. Create user documentation
10. Train users on system

---

## Quick Reference

### User Roles & Capabilities

| Role | Create Users | View All Claims | Export Data | Manage Settings |
|------|-------------|-----------------|-------------|-----------------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| Manager | Staff only | ✅ | ✅ | ❌ |
| Staff | ❌ | Own only | Own only | ❌ |
| Billing | ❌ | ✅ | ✅ | ❌ |
| API User | ❌ | Via API | Via API | ❌ |
| Read Only | ❌ | Assigned only | ❌ | ❌ |

---

## Support

For help with user setup:
- **Documentation:** USER_MANAGEMENT.md
- **Email:** support@yourorg.com
- **Issues:** GitHub Issues

---

*Last Updated: October 2025*
*Version: 1.0*
