# User Management System

## Overview

Complete user management system with Keycloak integration, role-based access control (RBAC), and comprehensive admin interface.

---

## Features

### ✅ Backend Features
1. **User CRUD Operations**
   - Create, read, update, delete users
   - Soft delete (deactivate instead of removing)
   - Bulk import from CSV/JSON
   - Export to CSV
   
2. **Role Management**
   - Admin, Manager, Staff, Billing, API User, Read-Only
   - Permission-based access control
   - Role descriptions and capabilities

3. **Organization Management**
   - Multi-organization support
   - Organization-level user isolation
   - Organization statistics

4. **Security Features**
   - Account locking after failed attempts
   - Password reset
   - Activity logging
   - PHI access levels
   - API key management

5. **Keycloak Integration**
   - Single Sign-On (SSO)
   - User sync from Keycloak
   - JWT token handling
   - OAuth 2.0 flow

---

## API Endpoints

### User Management

#### List Users
```http
GET /api/v1/auth/users/
```

Query Parameters:
- `role`: Filter by role (admin, manager, staff, billing, api_user, read_only)
- `is_active`: Filter by active status (true/false)
- `team`: Filter by team ID
- `search`: Search by email, name, username
- `ordering`: Sort by field (email, first_name, last_name, created_at, last_login)

Response:
```json
[
  {
    "id": "uuid",
    "username": "john.doe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "organization": "uuid",
    "organization_name": "ABC Healthcare",
    "role": "staff",
    "phone": "+1234567890",
    "department": "Billing",
    "title": "Billing Specialist",
    "is_active": true,
    "is_staff": false,
    "permissions": ["query_claims", "query_eligibility", ...],
    "last_login": "2025-10-05T12:00:00Z",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

---

#### Get User Details
```http
GET /api/v1/auth/users/{id}/
```

Response:
```json
{
  "id": "uuid",
  "username": "john.doe",
  "email": "john.doe@example.com",
  ...
}
```

---

#### Create User
```http
POST /api/v1/auth/users/
```

Request:
```json
{
  "username": "john.doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "staff",
  "phone": "+1234567890",
  "department": "Billing",
  "title": "Billing Specialist"
}
```

Response:
```json
{
  "id": "uuid",
  "username": "john.doe",
  ...
}
```

---

#### Update User
```http
PATCH /api/v1/auth/users/{id}/
```

Request:
```json
{
  "first_name": "Johnny",
  "department": "Claims"
}
```

Response:
```json
{
  "id": "uuid",
  "first_name": "Johnny",
  "department": "Claims",
  ...
}
```

---

#### Deactivate User
```http
DELETE /api/v1/auth/users/{id}/
```

Response:
```json
{
  "message": "User deactivated successfully"
}
```

---

#### Activate User
```http
POST /api/v1/auth/users/{id}/activate/
```

Response:
```json
{
  "message": "User activated successfully"
}
```

---

#### Reset Password
```http
POST /api/v1/auth/users/{id}/reset_password/
```

Response:
```json
{
  "message": "Password reset email sent to user",
  "email": "john.doe@example.com"
}
```

---

#### Unlock Account
```http
POST /api/v1/auth/users/{id}/unlock_account/
```

Response:
```json
{
  "message": "Account unlocked successfully"
}
```

---

#### Get User Activity Log
```http
GET /api/v1/auth/users/{id}/activity_log/
```

Response:
```json
{
  "user": {...},
  "recent_queries": [...],
  "total_queries": 50
}
```

---

#### Bulk Import Users
```http
POST /api/v1/auth/users/bulk_import/
```

Request:
```json
{
  "users": [
    {
      "email": "user1@example.com",
      "first_name": "User",
      "last_name": "One",
      "role": "staff"
    },
    {
      "email": "user2@example.com",
      "first_name": "User",
      "last_name": "Two",
      "role": "billing"
    }
  ]
}
```

Response:
```json
{
  "message": "2 users created successfully",
  "created": 2,
  "errors": []
}
```

---

#### Export Users
```http
GET /api/v1/auth/users/export/
```

Response:
```json
{
  "users": [...],
  "count": 10
}
```

---

#### Get User Statistics
```http
GET /api/v1/auth/users/stats/
```

Response:
```json
{
  "total_users": 25,
  "active_users": 23,
  "inactive_users": 2,
  "by_role": {
    "Admin": 2,
    "Manager": 3,
    "Staff": 15,
    "Billing": 3,
    "API User": 1,
    "Read Only": 1
  },
  "recent_logins": 18
}
```

---

### Role & Permission Management

#### Get Available Roles
```http
GET /api/v1/auth/roles/
```

Response:
```json
{
  "roles": [
    {
      "value": "admin",
      "label": "Admin",
      "description": "Full system access, can manage users and settings"
    },
    {
      "value": "manager",
      "label": "Manager",
      "description": "Can manage team members and view all data"
    },
    ...
  ]
}
```

---

#### Get User Permissions
```http
GET /api/v1/auth/permissions/
```

Response:
```json
{
  "role": "staff",
  "is_admin": false,
  "is_manager": false,
  "can_manage_users": false,
  "can_view_all_claims": false,
  "can_export_data": false,
  "phi_access_level": "full",
  "max_queries_per_day": 50,
  "payer_scope": ["UHC"],
  "tin_scope": ["123456789"],
  "facility_scope": ["Facility A"]
}
```

---

### Keycloak Sync

#### Sync All Users from Keycloak
```http
POST /api/v1/auth/sync/keycloak/
```

Response:
```json
{
  "message": "User sync completed successfully",
  "synced": 25,
  "created": 5,
  "updated": 20,
  "errors": []
}
```

---

#### Sync Specific User to Keycloak
```http
POST /api/v1/auth/sync/keycloak/{user_id}/
```

Response:
```json
{
  "message": "User synced to Keycloak successfully",
  "user": {...}
}
```

---

## Roles & Permissions

### Admin
**Full System Access**

Permissions:
- ✅ View all data
- ✅ Manage users
- ✅ Manage organization
- ✅ Export data
- ✅ View audit logs
- ✅ Manage API keys

Can:
- Create/edit/delete any user
- Access all claims in organization
- Configure system settings
- View security logs
- Generate reports

---

### Manager
**Team Management & Oversight**

Permissions:
- ✅ View organization data
- ✅ Manage staff users
- ✅ Export data
- ✅ View reports

Can:
- Create/edit staff, billing, read-only users
- Cannot edit admin users
- Access all claims in organization
- Export data to CSV
- Assign team members

---

### Staff
**Standard User Access**

Permissions:
- ✅ Query claims
- ✅ Query eligibility
- ✅ Upload CSV
- ✅ View own history

Can:
- Search claims
- View claim details
- Export their own results
- Upload CSV for bulk queries
- Limited to own queries in history

---

### Billing
**Financial Data Access**

Permissions:
- ✅ View organization data
- ✅ Export data
- ✅ View reports
- ✅ Query claims

Can:
- Access all claims for billing
- Export financial data
- View payment reports
- Reconcile payments

---

### API User
**Programmatic Access**

Permissions:
- ✅ API access
- ✅ Query claims
- ✅ Query eligibility

Can:
- Use API keys for automation
- Query claims via API
- No web interface access
- Rate limited

---

### Read Only
**View Only Access**

Permissions:
- ✅ View own data

Can:
- View assigned claims only
- No export capability
- No modifications
- Limited reporting

---

## Django Admin Interface

### Accessing Admin Panel
URL: `https://yourdomain.com/admin/`

Login with superuser credentials.

---

### User Management in Admin

**Features:**
1. **List View**
   - Search by email, name, organization
   - Filter by role, active status, organization, date joined
   - Sort by any column
   - Bulk actions (activate, deactivate)

2. **User Details**
   - Authentication info (ID, username, email, password)
   - Personal information (name, phone, department, title)
   - Organization & role
   - Permissions (active, staff, superuser, groups)
   - Security (Keycloak ID, login IP, failed attempts, lockout)
   - Timestamps (last login, date joined, created, updated)

3. **Actions**
   - Edit user details
   - Reset password
   - Activate/deactivate
   - Change role
   - Unlock account
   - View activity log

---

### Organization Management in Admin

**Features:**
1. **List View**
   - Search by name, NPI, TIN
   - Filter by active status
   - View active users count

2. **Organization Details**
   - Basic info (name, NPI, TIN)
   - Address
   - Contact info (phone, email)
   - Active status
   - User count

3. **Actions**
   - Edit organization
   - Activate/deactivate
   - View users
   - Export data

---

## Security Features

### Account Locking
- After 5 failed login attempts
- Locks for 30 minutes
- Admin/Manager can unlock manually

### Password Requirements
- Minimum 8 characters
- Must include: uppercase, lowercase, number, special character
- Cannot be same as username or email
- Cannot be common password

### Password Reset
- Email sent to user with reset link
- Link expires in 24 hours
- User must verify email address

### PHI Access Levels

**None:**
- No access to Protected Health Information
- Can view de-identified data only

**Limited:**
- Can view partial PHI (initials, partial dates)
- Masked SSN, phone numbers
- Limited patient demographics

**Full:**
- Full access to all PHI
- Complete patient information
- Audit logged

---

## Best Practices

### User Creation
1. Use strong passwords
2. Assign minimum required role
3. Set appropriate PHI access level
4. Configure query limits
5. Assign to team if applicable
6. Set scope (payers, TINs, facilities)

### Role Assignment
1. Start with least privilege
2. Upgrade role as needed
3. Document role changes
4. Review roles quarterly
5. Remove unused accounts

### Security
1. Enable MFA in Keycloak
2. Regular password changes
3. Monitor failed login attempts
4. Review audit logs weekly
5. Disable inactive users promptly

### Data Access
1. Limit scope to necessary payers
2. Restrict TIN access
3. Set facility boundaries
4. Configure query limits
5. Review access quarterly

---

## Troubleshooting

### User Can't Log In

**Check:**
1. Account active? (`is_active=True`)
2. Account locked? (failed attempts)
3. Keycloak user exists?
4. Email verified in Keycloak?
5. Correct password?

**Solutions:**
1. Activate user in Django admin
2. Unlock account: `POST /users/{id}/unlock_account/`
3. Sync from Keycloak: `POST /sync/keycloak/`
4. Reset password: `POST /users/{id}/reset_password/`

---

### User Can't Access Features

**Check:**
1. User role permissions
2. PHI access level
3. Organization access
4. Scope restrictions (payers, TINs)
5. Query limits reached?

**Solutions:**
1. Upgrade role if justified
2. Adjust PHI access level
3. Update scope settings
4. Increase query limits
5. Check permission errors in logs

---

### Sync Issues with Keycloak

**Check:**
1. Keycloak server accessible?
2. Credentials correct?
3. User exists in Keycloak?
4. Email matches?

**Solutions:**
1. Test Keycloak connection
2. Verify credentials in .env
3. Create user in Keycloak
4. Match emails exactly
5. Manual sync: `POST /sync/keycloak/{user_id}/`

---

## Testing

### Test User Creation

```bash
# Create test user
curl -X POST https://yourdomain.com/api/v1/auth/users/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test.user",
    "email": "test.user@example.com",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "role": "staff"
  }'
```

---

### Test User List

```bash
# List all users
curl https://yourdomain.com/api/v1/auth/users/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by role
curl "https://yourdomain.com/api/v1/auth/users/?role=staff" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Search users
curl "https://yourdomain.com/api/v1/auth/users/?search=john" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Test Bulk Import

```bash
# Import multiple users
curl -X POST https://yourdomain.com/api/v1/auth/users/bulk_import/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "users": [
      {
        "email": "user1@example.com",
        "first_name": "User",
        "last_name": "One",
        "role": "staff"
      },
      {
        "email": "user2@example.com",
        "first_name": "User",
        "last_name": "Two",
        "role": "billing"
      }
    ]
  }'
```

---

### Test User Statistics

```bash
# Get user stats
curl https://yourdomain.com/api/v1/auth/users/stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Database Schema

### User Model

```python
class User(AbstractUser):
    id = UUIDField(primary_key=True)
    organization = ForeignKey(Organization)
    role = CharField(choices=ROLE_CHOICES)
    keycloak_id = UUIDField(unique=True)
    team = ForeignKey(Team, null=True)
    
    # ABAC attributes
    payer_scope = JSONField(default=list)
    tin_scope = JSONField(default=list)
    facility_scope = JSONField(default=list)
    max_queries_per_day = IntegerField(default=50)
    phi_access_level = CharField(choices=[...])
    
    # Profile
    phone = CharField(max_length=20)
    department = CharField(max_length=100)
    title = CharField(max_length=100)
    
    # Security
    last_login_ip = GenericIPAddressField()
    failed_login_attempts = IntegerField(default=0)
    account_locked_until = DateTimeField()
    password_changed_at = DateTimeField()
    
    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

---

## Migration Guide

### Adding New Role

1. Update `ROLE_CHOICES` in `models.py`
2. Add permissions in `get_permissions()` method
3. Update role descriptions in `api_views.py`
4. Create migration: `python manage.py makemigrations`
5. Apply migration: `python manage.py migrate`
6. Update frontend role selector
7. Update documentation

---

### Changing User Organization

```python
# Move user to different organization
user = User.objects.get(email='user@example.com')
new_org = Organization.objects.get(npi='9876543210')
user.organization = new_org
user.save()
```

---

### Bulk User Creation

```python
# Create multiple users programmatically
from apps.users.models import User, Organization

org = Organization.objects.get(npi='1234567890')

users_data = [
    {'email': 'user1@example.com', 'first_name': 'User', 'last_name': 'One', 'role': 'staff'},
    {'email': 'user2@example.com', 'first_name': 'User', 'last_name': 'Two', 'role': 'billing'},
]

for user_data in users_data:
    User.objects.create_user(
        username=user_data['email'],
        organization=org,
        **user_data
    )
```

---

## Support

For issues or questions:
- **Documentation:** https://docs.yourorg.com
- **Email:** support@yourorg.com
- **GitHub Issues:** https://github.com/yourorg/connectme/issues

---

*Last Updated: October 2025*
*Version: 1.0*
