# 🎯 Create Keycloak Roles - Step by Step

## Part 1: Create Client Roles (10 minutes)

### Access Client Roles

1. Go to: **https://auth.totesoft.com/admin/**
2. Select realm: **connectme** (top-left dropdown)
3. Go to: **Clients** → Click **connectme-frontend**
4. Click the **Roles** tab

---

### Create Basic Roles (Copy-Paste These)

Click **Create role** and create each of these:

#### Claims Permissions
```
Role name: claim:read
Description: Read claims data
```

```
Role name: claim:write
Description: Create and update claims
```

```
Role name: claim:delete
Description: Delete claims
```

#### Eligibility Permissions
```
Role name: eligibility:read
Description: Read eligibility data
```

```
Role name: eligibility:write
Description: Create and update eligibility checks
```

#### User Management
```
Role name: user:read
Description: Read user data
```

```
Role name: user:write
Description: Create and update users
```

```
Role name: user:delete
Description: Delete users
```

#### Organization Management
```
Role name: organization:read
Description: Read organization data
```

```
Role name: organization:write
Description: Update organization settings
```

#### Other Permissions
```
Role name: bulk:process
Description: Process bulk CSV uploads
```

```
Role name: report:view
Description: View reports and analytics
```

```
Role name: report:export
Description: Export reports
```

```
Role name: audit:view
Description: View audit logs
```

```
Role name: settings:manage
Description: Manage system settings
```

---

### Create Composite Roles (Admin Roles)

Now create composite roles that combine the basic roles:

#### 1. claim:admin

1. Click **Create role**
2. **Role name:** `claim:admin`
3. **Description:** `Full claims administration`
4. Click **Save**
5. **Enable** "Composite roles" toggle
6. Under "Associated roles":
   - Click **Assign role**
   - Filter by: **Filter by clients** → Select **connectme-frontend**
   - Select these 3 roles:
     - ✅ claim:read
     - ✅ claim:write
     - ✅ claim:delete
   - Click **Assign**

#### 2. eligibility:admin

1. Click **Create role**
2. **Role name:** `eligibility:admin`
3. **Description:** `Full eligibility administration`
4. Click **Save**
5. **Enable** "Composite roles" toggle
6. Assign roles:
   - ✅ eligibility:read
   - ✅ eligibility:write

#### 3. user:admin

1. Click **Create role**
2. **Role name:** `user:admin`
3. **Description:** `Full user administration`
4. Click **Save**
5. **Enable** "Composite roles" toggle
6. Assign roles:
   - ✅ user:read
   - ✅ user:write
   - ✅ user:delete

#### 4. organization:admin

1. Click **Create role**
2. **Role name:** `organization:admin`
3. **Description:** `Full organization administration`
4. Click **Save**
5. **Enable** "Composite roles" toggle
6. Assign roles:
   - ✅ organization:read
   - ✅ organization:write

---

## Part 2: Create Realm Roles (5 minutes)

### Access Realm Roles

1. In the left menu, click **Realm roles**
2. Click **Create role**

---

### Create Realm Roles

#### 1. Admin Role

1. **Role name:** `admin`
2. **Description:** `Full administrator access to all features`
3. Click **Save**
4. **Enable** "Composite roles" toggle
5. Under "Associated roles":
   - Click **Assign role**
   - Filter by: **Filter by clients** → Select **connectme-frontend**
   - Select ALL these roles:
     - ✅ claim:admin
     - ✅ claim:read
     - ✅ claim:write
     - ✅ claim:delete
     - ✅ eligibility:admin
     - ✅ eligibility:read
     - ✅ eligibility:write
     - ✅ user:admin
     - ✅ user:read
     - ✅ user:write
     - ✅ user:delete
     - ✅ organization:admin
     - ✅ organization:read
     - ✅ organization:write
     - ✅ bulk:process
     - ✅ report:view
     - ✅ report:export
     - ✅ audit:view
     - ✅ settings:manage
   - Click **Assign**

#### 2. Manager Role

1. **Role name:** `manager`
2. **Description:** `Practice manager with elevated permissions`
3. Click **Save**
4. **Enable** "Composite roles" toggle
5. Assign roles (Filter by clients → connectme-frontend):
   - ✅ claim:read
   - ✅ claim:write
   - ✅ eligibility:read
   - ✅ user:read
   - ✅ bulk:process
   - ✅ report:view

#### 3. Staff Role

1. **Role name:** `staff`
2. **Description:** `Staff member with basic access`
3. Click **Save**
4. **Enable** "Composite roles" toggle
5. Assign roles (Filter by clients → connectme-frontend):
   - ✅ claim:read
   - ✅ eligibility:read

#### 4. Billing Role

1. **Role name:** `billing`
2. **Description:** `Billing specialist with claims and payment access`
3. Click **Save**
4. **Enable** "Composite roles" toggle
5. Assign roles (Filter by clients → connectme-frontend):
   - ✅ claim:read
   - ✅ claim:write
   - ✅ report:view

---

## Part 3: Create Test User (2 minutes)

### Create User

1. Go to: **Users** → **Add user**
2. Fill in:
   - **Username:** `testuser`
   - **Email:** `test@connectme.com`
   - **First name:** `Test`
   - **Last name:** `User`
   - **Email verified:** Toggle **ON**
3. Click **Create**

### Set Password

1. Click the **Credentials** tab
2. Click **Set password**
3. Fill in:
   - **Password:** `testpass123`
   - **Password confirmation:** `testpass123`
   - **Temporary:** Toggle **OFF**
4. Click **Save**
5. Confirm by clicking **Save password**

### Assign Admin Role

1. Click the **Role mapping** tab
2. Click **Assign role**
3. Select **admin** (realm role)
4. Click **Assign**

---

## ✅ Verification Checklist

### Client Roles (connectme-frontend)
- [ ] claim:read
- [ ] claim:write
- [ ] claim:delete
- [ ] claim:admin (composite)
- [ ] eligibility:read
- [ ] eligibility:write
- [ ] eligibility:admin (composite)
- [ ] user:read
- [ ] user:write
- [ ] user:delete
- [ ] user:admin (composite)
- [ ] organization:read
- [ ] organization:write
- [ ] organization:admin (composite)
- [ ] bulk:process
- [ ] report:view
- [ ] report:export
- [ ] audit:view
- [ ] settings:manage

### Realm Roles
- [ ] admin (with all client roles)
- [ ] manager (with limited client roles)
- [ ] staff (with basic client roles)
- [ ] billing (with claims client roles)

### Test User
- [ ] testuser created
- [ ] Password set to testpass123
- [ ] Admin role assigned

---

## 🧪 Test Your Configuration

### Test 1: Get Token

```bash
curl -X POST https://auth.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password"
```

**Expected:** JSON with `access_token`

### Test 2: Decode Token to See Roles

```bash
# Get token
TOKEN=$(curl -s -X POST https://auth.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password" | jq -r '.access_token')

# Decode and view roles
echo $TOKEN | cut -d'.' -f2 | base64 -d | jq '.realm_access.roles, .resource_access'
```

**Expected to see:**
```json
{
  "realm_access": {
    "roles": ["admin", "offline_access", "uma_authorization"]
  },
  "resource_access": {
    "connectme-frontend": {
      "roles": [
        "claim:admin",
        "claim:read",
        "claim:write",
        "claim:delete",
        "eligibility:admin",
        ...
      ]
    }
  }
}
```

---

## 💡 Quick Tips

### Creating Roles Faster

1. **Keep the tab open** - Don't close the roles page
2. **Use keyboard shortcuts:**
   - After clicking "Create role": Tab → Type name → Tab → Type description → Enter
3. **For composite roles:**
   - Create the role first
   - Then go back and add associated roles

### Common Issues

**Q: Can't find "Filter by clients"?**
**A:** Make sure you're assigning roles to a composite role, not creating a new one.

**Q: Don't see client roles when assigning?**
**A:** Make sure you selected "Filter by clients" and chose "connectme-frontend"

**Q: Composite roles not showing all permissions?**
**A:** Check that you assigned the roles correctly. Click the composite role and verify under "Associated roles"

---

## 🎉 You're Done!

Once all roles are created and assigned to testuser:

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_TESTING.sh
```

Then:
1. Open: http://localhost:3000
2. Login: `testuser` / `testpass123`
3. You should see the dashboard!

---

## 📊 Role Summary

**Total Roles to Create:**
- 19 Client roles (connectme-frontend)
- 4 Realm roles (admin, manager, staff, billing)
- 1 Test user with admin role

**Time:** ~15-20 minutes

**Result:** Complete role-based access control system! 🚀
