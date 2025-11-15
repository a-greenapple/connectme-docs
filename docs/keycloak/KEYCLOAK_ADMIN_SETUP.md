# Keycloak Admin Setup - URGENT FIX NEEDED

## Current Problem

The backend cannot create users in Keycloak because:
1. ❌ The admin credentials in `.env` are not working (401 Unauthorized)
2. ❌ Current credentials: `connectme / Qojsyb-fynwa1-johsyj` - **INVALID**

**Latest error from logs:**
```
ERROR Failed to get Keycloak admin token: 401 Client Error: Unauthorized
ERROR ❌ HTTP error creating Keycloak user vigneshr: 401 - {"error":"HTTP 401 Unauthorized"}
WARNING ⚠️ Failed to sync user vigneshr to Keycloak - user created in Django only
```

---

## Solution: Find Working Admin Credentials

### Step 1: Identify Working Credentials

Try logging into Keycloak Admin Console with different accounts:

**URL:** https://auth.totesoft.com/admin/

Try these accounts (in order):

1. **Master Realm Admin**
   - Username: `admin`
   - Password: `<your_master_admin_password>`
   - Realm: `master`

2. **ConnectMe Realm Admin**
   - Username: `admin` (or whatever admin user exists)
   - Password: `<password>`
   - Realm: `connectme-preprod`

3. **Other Admin Users**
   - Check if there are other admin users you know about

### Step 2: Once You Find Working Credentials

After you successfully log in, note down:
- ✅ Username: `__________`
- ✅ Password: `__________`
- ✅ Realm: `__________`

---

## Step 3: Update Backend Configuration

Once you have working credentials, run these commands:

```bash
# SSH into the server
ssh connectme@169.59.163.43

# Update the .env file with working credentials
sudo nano /var/www/connectme-preprod-backend/.env

# Change these lines:
KEYCLOAK_ADMIN_USERNAME=<working_username>
KEYCLOAK_ADMIN_PASSWORD=<working_password>

# Save and exit (Ctrl+X, Y, Enter)

# Restart the backend
sudo systemctl restart connectme-preprod-backend

# Check if it's running
sudo systemctl status connectme-preprod-backend
```

---

## Step 4: Grant Necessary Permissions

After logging into Keycloak Admin Console:

### If using Master Realm Admin:
- ✅ You already have all permissions
- ✅ Skip to Step 5

### If using ConnectMe Realm User:

1. **Log into Keycloak Admin Console**
   - https://auth.totesoft.com/admin/

2. **Go to the user's Role Mappings**
   - Select `connectme-preprod` realm (top left dropdown)
   - Click **Users** → Find your admin user
   - Click **Role Mappings** tab

3. **Assign these roles:**
   - Click **Assign role**
   - Filter by clients: `realm-management`
   - Select:
     - ✅ `manage-users`
     - ✅ `view-users`
     - ✅ `query-users`
     - ✅ `manage-realm` (optional, for full access)
   - Click **Assign**

---

## Step 5: Test User Creation

1. **Go to frontend:** https://pre-prod.connectme.apps.totessoft.com/users
2. **Click "Create New User"**
3. **Fill in the form:**
   - First Name: Test
   - Last Name: User
   - Email: testuser@example.com
   - Username: testuser
   - Password: TestPass123!
   - Confirm Password: TestPass123!
4. **Click "Create User"**

### Check Backend Logs:
```bash
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 50 --no-pager | grep -i keycloak'
```

### Expected Success:
```
INFO ✅ Successfully obtained Keycloak admin token
INFO ✅ Successfully created Keycloak user: testuser
INFO ✅ Keycloak user ID: <some-uuid>
```

### If Still Failing:
```
ERROR Failed to get Keycloak admin token: 401 Client Error: Unauthorized
```
→ Credentials are still wrong, go back to Step 1

```
ERROR ❌ HTTP error creating Keycloak user: 403 - Forbidden
```
→ User doesn't have permissions, go back to Step 4

---

## Alternative: Use Service Account (Best Practice)

If you can't find working user credentials, create a service account:

### 1. Create Service Account Client

1. Log into Keycloak Admin Console
2. Select `connectme-preprod` realm
3. Go to **Clients** → **Create client**
4. Fill in:
   - Client ID: `connectme-backend-service`
   - Client Protocol: `openid-connect`
   - Click **Next**
5. Enable:
   - ✅ Client authentication: ON
   - ✅ Service accounts roles: ON
   - ❌ Standard flow: OFF
   - ❌ Direct access grants: OFF
   - Click **Next**, then **Save**

### 2. Get Client Secret

1. Go to **Credentials** tab
2. Copy the **Client Secret**
3. Save it: `__________`

### 3. Assign Service Account Roles

1. Go to **Service Account Roles** tab
2. Click **Assign role**
3. Filter by clients: `realm-management`
4. Select:
   - ✅ `manage-users`
   - ✅ `view-users`
   - ✅ `query-users`
5. Click **Assign**

### 4. Update Backend Code

This requires modifying `keycloak_sync.py` to use client credentials grant instead of password grant.

---

## Quick Checklist

- [ ] Found working Keycloak admin credentials
- [ ] Updated `.env` file with correct credentials
- [ ] Restarted backend service
- [ ] Granted necessary permissions to the admin user
- [ ] Tested user creation in frontend
- [ ] Verified user exists in both Django and Keycloak

---

## Current Status

- ✅ Backend is running
- ✅ Frontend is accessible
- ✅ Users can log in
- ✅ Users can be created in Django
- ❌ **Users CANNOT be created in Keycloak** (401 Unauthorized)
- ❌ **Admin credentials are invalid**

---

## What We Need From You

**Please provide ONE of the following:**

1. **Working Keycloak admin credentials:**
   - Username: `__________`
   - Password: `__________`
   - Realm: `__________`

2. **Or tell us:**
   - Can you log into https://auth.totesoft.com/admin/ ?
   - If yes, with which username?

3. **Or:**
   - Create a service account as described above
   - Provide the client ID and secret

---

## Why This Is Important

Without working Keycloak credentials:
- ✅ Users are created in Django (database)
- ❌ Users are NOT created in Keycloak (SSO)
- ❌ New users CANNOT log in
- ❌ Password reset WILL NOT work

**Users created now will be "orphaned" in Django and won't be able to authenticate!**

