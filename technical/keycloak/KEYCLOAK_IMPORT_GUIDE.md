# 🔐 Keycloak Import Guide

## Files Created

I've created 3 JSON files for you to import into Keycloak:

1. **`keycloak-client-frontend.json`** - Frontend client configuration
2. **`keycloak-client-backend.json`** - Backend API client configuration  
3. **`keycloak-roles-complete.json`** - Complete role hierarchy

---

## 📋 Import Instructions

### Step 1: Access Keycloak Admin

1. Go to: **https://auth.totesoft.com/admin/**
2. Login with your admin credentials
3. Select realm: **connectme**

---

### Step 2: Import Frontend Client

**Option A: Via UI (Recommended)**

1. Go to: **Clients** → **Import client**
2. Click **Browse** or drag-and-drop
3. Select: `keycloak-client-frontend.json`
4. Click **Save**

**Option B: Manual Creation (if import fails)**

1. Go to: **Clients** → **Create client**
2. Copy settings from `keycloak-client-frontend.json`
3. Key settings:
   - Client ID: `connectme-frontend`
   - Client authentication: **OFF** (public client)
   - Standard flow: **ON**
   - Direct access grants: **ON**
   - Valid redirect URIs: `http://localhost:3000/*`, `https://connectme.totesoft.com/*`
   - Web origins: `http://localhost:3000`, `https://connectme.totesoft.com`

---

### Step 3: Create Client Roles for Frontend

Since Keycloak doesn't import client roles via client JSON, create them manually:

1. Go to: **Clients** → **connectme-frontend** → **Roles** tab
2. Click **Create role**
3. Create these roles:

**Claims Permissions:**
- `claim:read` - Read claims data
- `claim:write` - Create/update claims
- `claim:delete` - Delete claims
- `claim:admin` - Full claims admin (composite of above 3)

**Eligibility Permissions:**
- `eligibility:read` - Read eligibility
- `eligibility:write` - Create/update eligibility
- `eligibility:admin` - Full eligibility admin (composite)

**User Management:**
- `user:read` - Read users
- `user:write` - Create/update users
- `user:delete` - Delete users
- `user:admin` - Full user admin (composite)

**Organization:**
- `organization:read` - Read organization
- `organization:write` - Update organization
- `organization:admin` - Full org admin (composite)

**Other Permissions:**
- `bulk:process` - Process bulk uploads
- `report:view` - View reports
- `report:export` - Export reports
- `audit:view` - View audit logs
- `settings:manage` - Manage settings

**For composite roles (like `claim:admin`):**
1. Create the role
2. Go to role details
3. Enable **Composite roles**
4. Add associated roles (e.g., `claim:read`, `claim:write`, `claim:delete`)

---

### Step 4: Import Backend Client (Optional)

1. Go to: **Clients** → **Import client**
2. Select: `keycloak-client-backend.json`
3. Click **Save**
4. Go to **Credentials** tab
5. Copy the **Client secret** (you'll need this for Django)

---

### Step 5: Create Realm Roles

1. Go to: **Realm roles** → **Create role**
2. Create these roles:

**Admin Role:**
- Name: `admin`
- Description: Full administrator access
- Composite: **ON**
- Associated client roles (connectme-frontend):
  - `claim:admin`
  - `eligibility:admin`
  - `user:admin`
  - `organization:admin`
  - `bulk:process`
  - `report:view`
  - `audit:view`
  - `settings:manage`

**Manager Role:**
- Name: `manager`
- Description: Practice manager
- Composite: **ON**
- Associated client roles (connectme-frontend):
  - `claim:read`
  - `claim:write`
  - `eligibility:read`
  - `user:read`
  - `bulk:process`
  - `report:view`

**Staff Role:**
- Name: `staff`
- Description: Staff member
- Composite: **ON**
- Associated client roles (connectme-frontend):
  - `claim:read`
  - `eligibility:read`

**Billing Role:**
- Name: `billing`
- Description: Billing specialist
- Composite: **ON**
- Associated client roles (connectme-frontend):
  - `claim:read`
  - `claim:write`
  - `report:view`

---

### Step 6: Create Test User

1. Go to: **Users** → **Add user**
2. User details:
   - Username: `testuser`
   - Email: `test@connectme.com`
   - First name: `Test`
   - Last name: `User`
   - Email verified: **ON**
3. Click **Create**

4. Set password (Credentials tab):
   - Password: `testpass123`
   - Temporary: **OFF**
   - Click **Set password**

5. Assign roles (Role mapping tab):
   - Click **Assign role**
   - Filter: **Filter by clients**
   - Select realm role: `admin`
   - Click **Assign**

---

## 🧪 Test Configuration

### Test 1: Get Token

```bash
curl -X POST https://auth.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password" | jq
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

# Decode token (view payload)
echo $TOKEN | cut -d'.' -f2 | base64 -d | jq
```

**Look for:**
```json
{
  "realm_access": {
    "roles": ["admin", ...]
  },
  "resource_access": {
    "connectme-frontend": {
      "roles": ["claim:admin", "claim:read", ...]
    }
  }
}
```

### Test 3: Test with Application

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_TESTING.sh
```

Then:
1. Open: http://localhost:3000
2. Login: `testuser` / `testpass123`
3. Check browser console for user object with roles

---

## 📊 Role Hierarchy

```
admin (Realm Role)
├── claim:admin (Client Role)
│   ├── claim:read
│   ├── claim:write
│   └── claim:delete
├── eligibility:admin
│   ├── eligibility:read
│   └── eligibility:write
├── user:admin
│   ├── user:read
│   ├── user:write
│   └── user:delete
├── organization:admin
│   ├── organization:read
│   └── organization:write
├── bulk:process
├── report:view
├── report:export
├── audit:view
└── settings:manage

manager (Realm Role)
├── claim:read
├── claim:write
├── eligibility:read
├── user:read
├── bulk:process
└── report:view

staff (Realm Role)
├── claim:read
└── eligibility:read

billing (Realm Role)
├── claim:read
├── claim:write
└── report:view
```

---

## 🔧 Quick Setup Script

If you prefer, here's a quick reference for manual setup:

```bash
# Realm Roles
admin, manager, staff, billing

# Client Roles (connectme-frontend)
claim:read, claim:write, claim:delete, claim:admin
eligibility:read, eligibility:write, eligibility:admin
user:read, user:write, user:delete, user:admin
organization:read, organization:write, organization:admin
bulk:process, report:view, report:export
audit:view, settings:manage

# Test User
Username: testuser
Password: testpass123
Realm Role: admin
```

---

## ✅ Verification Checklist

- [ ] Frontend client `connectme-frontend` created
- [ ] Backend client `connectme-backend` created (optional)
- [ ] All client roles created for `connectme-frontend`
- [ ] Composite roles configured (claim:admin, etc.)
- [ ] Realm roles created (admin, manager, staff, billing)
- [ ] Realm roles linked to client roles
- [ ] Test user created
- [ ] Test user has `admin` realm role
- [ ] Token test successful (shows roles)
- [ ] Application login works

---

## 🎉 Ready to Test!

Once all steps are complete:

```bash
./START_TESTING.sh
```

Login with: `testuser` / `testpass123`

---

## 📚 Additional Resources

- **Role Integration:** `KEYCLOAK_ROLES_INTEGRATION.md`
- **Configuration Steps:** `KEYCLOAK_CONFIG_STEPS.md`
- **Docker Guide:** `KEYCLOAK_DOCKER_GUIDE.md`

---

**Need help?** The roles are already configured in the JSON files. Just import and assign to users!
