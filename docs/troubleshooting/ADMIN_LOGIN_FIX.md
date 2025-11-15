# Admin Login Issue - Pre-Prod

## Problem
Cannot login to Pre-Prod using `admin` / `hufze7-coqrok-zUfwuf`

## Root Cause
The frontend is configured to use **Keycloak authentication**, not Django authentication. The admin user needs to exist in Keycloak, not just in Django.

## Current Status

### ✅ Django Admin User
- **Status:** EXISTS and password is CORRECT
- **Username:** admin
- **Password:** hufze7-coqrok-zUfwuf
- **Role:** admin
- **Can be used for:** Django admin panel only (not frontend login)

### ❌ Keycloak Admin User
- **Status:** DOES NOT EXIST or password is incorrect
- **Realm:** connectme-preprod
- **URL:** https://auth.totesoft.com

## Solutions

### Option 1: Create Admin User in Keycloak (RECOMMENDED)

#### Method A: Using the Script (Automated)
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./fix_admin_login.sh
```

The script will:
1. Connect to Keycloak admin API
2. Create/reset the admin user
3. Assign admin role
4. Add to admin group

#### Method B: Using Keycloak Admin Console (Manual)
1. Go to: https://auth.totesoft.com/admin
2. Login with Keycloak admin credentials
3. Select realm: `connectme-preprod`
4. Go to Users → Add User
5. Fill in:
   - Username: `admin`
   - Email: `admin@connectme.com`
   - First Name: `Admin`
   - Last Name: `User`
   - Email Verified: ON
   - Enabled: ON
6. Click "Create"
7. Go to "Credentials" tab
8. Set password: `hufze7-coqrok-zUfwuf`
9. Set "Temporary" to OFF
10. Click "Set Password"
11. Go to "Role Mappings" tab
12. Assign role: `admin`
13. Go to "Groups" tab
14. Join group: `admin` (if exists)

### Option 2: Use Different Credentials

If you have other Keycloak credentials that work, use those instead.

### Option 3: Access Django Admin Directly

If you only need backend access:
1. Go to: https://pre-prod.connectme.be.totessoft.com/admin/
2. Login with: `admin` / `hufze7-coqrok-zUfwuf`
3. This will work because Django admin uses Django authentication

## Keycloak Admin Credentials

From the server `.env` file:
```
KEYCLOAK_ADMIN_USERNAME=connectme
KEYCLOAK_ADMIN_PASSWORD=Qojsyb-fynwa1-johsyj
```

**Note:** These credentials are for Keycloak master realm admin, NOT for the connectme-preprod realm.

## Architecture

```
Frontend Login Flow:
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ 1. Visit login page
       ▼
┌─────────────────┐
│    Frontend     │
│  (Next.js)      │
└──────┬──────────┘
       │ 2. Redirect to Keycloak
       ▼
┌─────────────────┐
│   Keycloak      │
│ (auth.totesoft) │
└──────┬──────────┘
       │ 3. User enters credentials
       │ 4. Keycloak validates
       ▼
┌─────────────────┐
│   JWT Token     │
│ (with role)     │
└──────┬──────────┘
       │ 5. Token sent to frontend
       ▼
┌─────────────────┐
│    Frontend     │
│ Stores token    │
└──────┬──────────┘
       │ 6. API calls with token
       ▼
┌─────────────────┐
│    Backend      │
│ Validates token │
│ Extracts role   │
│ Creates/updates │
│ Django user     │
└─────────────────┘
```

## Why This Happens

1. **Frontend uses Keycloak:** The frontend is configured with:
   ```env
   NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
   NEXT_PUBLIC_KEYCLOAK_REALM=connectme-preprod
   NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-preprod-frontend
   ```

2. **Django user is separate:** The Django admin user exists in the database but is only used for:
   - Django admin panel access
   - Backend operations
   - NOT for frontend login

3. **Token-based auth:** When you login via frontend:
   - Frontend redirects to Keycloak
   - Keycloak authenticates user
   - Keycloak issues JWT token
   - Backend validates token and creates/updates Django user

## Testing After Fix

### 1. Test Frontend Login
```bash
# Open browser
https://pre-prod.connectme.apps.totessoft.com

# You should be redirected to:
https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/auth...

# Enter credentials:
Username: admin
Password: hufze7-coqrok-zUfwuf

# Should redirect back to frontend and be logged in
```

### 2. Verify Role
```bash
# Check Django user was created/updated with correct role
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python -c "
import os, django
os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"config.settings\")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username=\"admin\")
print(f\"Role: {admin.role}\")
print(f\"Is admin: {admin.role == \'admin\'}\")
"'
```

### 3. Test Admin Menu
- Login to frontend
- Admin menu should be visible (top right)
- Click "Admin" → Should see admin options

## Troubleshooting

### Issue: "Invalid credentials" in Keycloak
**Solution:**
- Verify user exists in Keycloak admin console
- Reset password in Keycloak
- Check "Temporary" is OFF
- Verify user is enabled

### Issue: "User not found" in Keycloak
**Solution:**
- Create user using Method B above
- Or run the fix_admin_login.sh script

### Issue: Can't access Keycloak admin console
**Solution:**
- Try credentials: `connectme` / `Qojsyb-fynwa1-johsyj`
- Contact system administrator
- Check if Keycloak is accessible: `curl https://auth.totesoft.com`

### Issue: Login works but no admin menu
**Solution:**
- Check user role in Django: should be 'admin'
- Check backend logs for role extraction
- Verify Keycloak user has 'admin' role or is in 'admin' group
- Logout and login again to sync role

## Quick Reference

| What | Where | Credentials |
|------|-------|-------------|
| Frontend | https://pre-prod.connectme.apps.totessoft.com | Keycloak users |
| Backend API | https://pre-prod.connectme.be.totessoft.com | Token-based |
| Django Admin | https://pre-prod.connectme.be.totessoft.com/admin/ | Django users |
| Keycloak Admin | https://auth.totesoft.com/admin | connectme / Qojsyb-fynwa1-johsyj |
| Keycloak Realm | connectme-preprod | - |

## Files

- `fix_admin_login.sh` - Automated script to create/reset admin user in Keycloak
- `ADMIN_LOGIN_FIX.md` - This documentation

---

**Last Updated:** November 11, 2025  
**Status:** Documented - Awaiting Keycloak admin access to implement fix

