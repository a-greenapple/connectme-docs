# Keycloak Permissions Fix

## Problem
The `connectme` user in Keycloak can authenticate but gets **403 Forbidden** when trying to create users.

**Error from logs:**
```
INFO Keycloak create user response status: 403
ERROR ❌ HTTP error creating Keycloak user test: 403 - {"error":"HTTP 403 Forbidden"}
WARNING ⚠️ Failed to sync user test to Keycloak - user created in Django only
```

## Solution
Grant the `connectme` user the necessary permissions to manage users in the `connectme-preprod` realm.

---

## Step-by-Step Fix

### Option 1: Use Master Realm Admin (RECOMMENDED)

1. **Log in to Keycloak Admin Console**
   - URL: https://auth.totesoft.com/admin/
   - Use the **master realm admin** credentials (not the `connectme` user)

2. **Update the `.env` file on the server**
   ```bash
   ssh connectme@169.59.163.43
   sudo nano /var/www/connectme-preprod-backend/.env
   ```

3. **Change these lines:**
   ```bash
   # FROM:
   KEYCLOAK_ADMIN_USERNAME=connectme
   KEYCLOAK_ADMIN_PASSWORD=connectme1415
   
   # TO (use master realm admin):
   KEYCLOAK_ADMIN_USERNAME=admin
   KEYCLOAK_ADMIN_PASSWORD=<master_admin_password>
   ```

4. **Restart the backend**
   ```bash
   sudo systemctl restart connectme-preprod-backend
   ```

---

### Option 2: Grant Permissions to `connectme` User

If you prefer to keep using the `connectme` user, grant it the necessary permissions:

1. **Log in to Keycloak Admin Console**
   - URL: https://auth.totesoft.com/admin/
   - Select **Master** realm (top left dropdown)

2. **Navigate to the `connectme` user**
   - Click **Users** in the left sidebar
   - Search for `connectme`
   - Click on the user

3. **Go to Role Mappings**
   - Click the **Role Mappings** tab
   - Click **Assign role** button

4. **Filter by clients**
   - In the "Filter by clients" dropdown, select **realm-management**

5. **Assign the following roles:**
   - ✅ `manage-users` (REQUIRED)
   - ✅ `view-users` (REQUIRED)
   - ✅ `query-users` (REQUIRED)
   - ✅ `create-client` (optional, for future features)
   - ✅ `manage-realm` (optional, for full admin access)

6. **Save and restart backend**
   ```bash
   ssh connectme@169.59.163.43
   sudo systemctl restart connectme-preprod-backend
   ```

---

### Option 3: Create a Service Account (BEST PRACTICE)

For production, it's better to use a service account:

1. **Create a new client in `connectme-preprod` realm**
   - Name: `connectme-backend-admin`
   - Client Protocol: `openid-connect`
   - Access Type: `confidential`
   - Service Accounts Enabled: `ON`
   - Authorization Enabled: `OFF`

2. **Get the client secret**
   - Go to **Credentials** tab
   - Copy the **Secret**

3. **Assign service account roles**
   - Go to **Service Account Roles** tab
   - Filter by clients: `realm-management`
   - Assign: `manage-users`, `view-users`, `query-users`

4. **Update `.env` file**
   ```bash
   KEYCLOAK_CLIENT_ID=connectme-backend-admin
   KEYCLOAK_CLIENT_SECRET=<copied_secret>
   # Remove KEYCLOAK_ADMIN_USERNAME and KEYCLOAK_ADMIN_PASSWORD
   ```

5. **Update `keycloak_sync.py` to use client credentials grant**
   (This would require code changes)

---

## Quick Test

After applying the fix, test user creation:

1. **Go to the frontend**
   - https://pre-prod.connectme.apps.totessoft.com/users

2. **Create a new user**
   - Fill in all fields
   - Click "Create User"

3. **Check backend logs**
   ```bash
   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 50 --no-pager | grep -i keycloak'
   ```

4. **Expected success log:**
   ```
   INFO ✅ Successfully created Keycloak user: <username>
   INFO ✅ Keycloak user ID: <keycloak_id>
   ```

5. **Verify in Keycloak**
   - Log in to Keycloak Admin Console
   - Go to `connectme-preprod` realm → Users
   - Search for the newly created user
   - User should exist with correct details

---

## Which Option Should You Choose?

| Option | Pros | Cons | Recommended For |
|--------|------|------|-----------------|
| **Option 1: Master Admin** | ✅ Works immediately<br>✅ Full permissions | ❌ Uses powerful admin account<br>❌ Less secure | Quick fix, testing |
| **Option 2: Grant Permissions** | ✅ Uses existing user<br>✅ More secure than master | ❌ Requires manual setup | Development, pre-prod |
| **Option 3: Service Account** | ✅ Most secure<br>✅ Best practice<br>✅ No password needed | ❌ Requires code changes<br>❌ More complex setup | Production |

**For now, I recommend Option 1 or Option 2** to get things working quickly.

---

## Current Status

- ✅ User creation works in Django (user is saved to database)
- ❌ User creation fails in Keycloak (403 Forbidden)
- ✅ Code has been updated to try master realm first
- ⏳ Waiting for Keycloak permissions to be granted

---

## Next Steps

1. Choose one of the options above
2. Apply the fix
3. Restart the backend
4. Test user creation
5. Verify the user exists in both Django and Keycloak

