# 🚀 Keycloak Complete Realm Import - One-Click Setup!

## ✅ What This Does

The `keycloak-realm-connectme-complete.json` file contains **EVERYTHING**:

- ✅ Both clients (connectme-frontend, connectme-backend)
- ✅ All 19 client roles with descriptions
- ✅ All 4 realm roles (admin, manager, staff, billing)
- ✅ All composite role relationships
- ✅ Protocol mappers for roles in JWT tokens
- ✅ Proper redirect URIs and CORS settings

**Result:** Complete RBAC system in ONE import! 🎉

---

## 🎯 Import Options

### Option A: Create New Realm (Recommended if "connectme" doesn't exist)

1. Go to: **https://auth.totesoft.com/admin/**
2. Click the realm dropdown (top-left)
3. Click **"Create Realm"**
4. Click **"Browse"** or drag-and-drop
5. Select: `keycloak-realm-connectme-complete.json`
6. Click **"Create"**

**Done!** Everything is imported automatically! 🎊

---

### Option B: Partial Import (If realm "connectme" already exists)

⚠️ **Warning:** This will merge with existing configuration

1. Go to: **https://auth.totesoft.com/admin/**
2. Select realm: **connectme**
3. Go to: **Realm settings** → **Action** dropdown (top-right)
4. Click **"Partial import"**
5. Click **"Browse"** and select: `keycloak-realm-connectme-complete.json`
6. **Import options:**
   - If a resource exists: **"Skip"** or **"Overwrite"** (your choice)
7. Click **"Import"**

---

### Option C: Replace Entire Realm (⚠️ Destructive)

⚠️ **Warning:** This will DELETE the existing "connectme" realm!

1. Export your current realm first (backup!)
2. Delete the existing "connectme" realm
3. Follow **Option A** above to create new realm

---

## 📋 After Import - Create Test User

The realm import doesn't include users (for security). Create one manually:

### Create Test User (2 minutes)

1. Go to: **Users** → **Add user**
2. Fill in:
   ```
   Username: testuser
   Email: test@connectme.com
   First name: Test
   Last name: User
   Email verified: ON (toggle)
   ```
3. Click **"Create"**

4. **Set Password** (Credentials tab):
   ```
   Password: testpass123
   Password confirmation: testpass123
   Temporary: OFF (toggle)
   ```
5. Click **"Set password"** → Confirm

6. **Assign Admin Role** (Role mapping tab):
   - Click **"Assign role"**
   - Select **"admin"** (realm role)
   - Click **"Assign"**

---

## 🧪 Verify Import

### Check 1: Clients Exist

1. Go to: **Clients**
2. Should see:
   - ✅ connectme-frontend (public)
   - ✅ connectme-backend (confidential)

### Check 2: Client Roles Exist

1. Go to: **Clients** → **connectme-frontend** → **Roles** tab
2. Should see 19 roles:
   - claim:read, claim:write, claim:delete, claim:admin
   - eligibility:read, eligibility:write, eligibility:admin
   - user:read, user:write, user:delete, user:admin
   - organization:read, organization:write, organization:admin
   - bulk:process, report:view, report:export
   - audit:view, settings:manage

### Check 3: Realm Roles Exist

1. Go to: **Realm roles**
2. Should see:
   - ✅ admin (composite - with all client roles)
   - ✅ manager (composite - with limited roles)
   - ✅ staff (composite - with basic roles)
   - ✅ billing (composite - with claims roles)

### Check 4: Composite Roles Configured

1. Go to: **Realm roles** → Click **"admin"**
2. Should see "Composite roles" is ON
3. Under "Associated roles" should see all client roles assigned

---

## 🧪 Test Authentication

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
    "roles": ["admin", "offline_access", "uma_authorization", "default-roles-connectme"]
  },
  "resource_access": {
    "connectme-frontend": {
      "roles": [
        "claim:admin",
        "eligibility:admin",
        "user:admin",
        "organization:admin",
        "bulk:process",
        "report:view",
        "report:export",
        "audit:view",
        "settings:manage"
      ]
    }
  }
}
```

---

## ✅ Success Checklist

- [ ] Realm "connectme" created/imported
- [ ] Client "connectme-frontend" exists
- [ ] Client "connectme-backend" exists
- [ ] 19 client roles exist in connectme-frontend
- [ ] 4 realm roles exist (admin, manager, staff, billing)
- [ ] Realm roles are composite (linked to client roles)
- [ ] Test user "testuser" created
- [ ] Test user has "admin" realm role
- [ ] Token test shows all roles
- [ ] Token test shows client roles under resource_access

---

## 🎉 Start Your Application!

Once everything is verified:

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_TESTING.sh
```

Then:
1. Open: http://localhost:3000
2. Login: `testuser` / `testpass123`
3. You should see the dashboard!

---

## 🔧 Troubleshooting

### Import Failed

**Error: "Realm with same name exists"**
- Use **Option B** (Partial Import) instead
- Or delete existing realm first

**Error: "Invalid JSON"**
- Make sure you selected the correct file
- File should be `keycloak-realm-connectme-complete.json`

### Roles Not Showing in Token

**Check:**
1. User has realm role assigned (e.g., "admin")
2. Realm role is composite and linked to client roles
3. Client has protocol mappers for roles

**Fix:**
1. Go to realm role → Verify "Composite roles" is ON
2. Go to client → Client scopes → Verify "roles" scope is included

### Can't Login

**Check:**
1. User exists
2. Password is set (not temporary)
3. User is enabled
4. Email verified is ON

---

## 💡 Pro Tips

### Backup First
Before importing, export your current realm:
1. Realm settings → Action → Export
2. Save the JSON file as backup

### Multiple Environments
You can import this realm into:
- Development Keycloak (localhost:8080)
- Staging Keycloak
- Production Keycloak (auth.totesoft.com)

Just change the redirect URIs after import if needed.

### Add More Users
After import, you can add more users:
- Assign different realm roles (manager, staff, billing)
- Each will automatically get the appropriate client roles

---

## 📊 What Gets Imported

| Component | Count | Details |
|-----------|-------|---------|
| Clients | 2 | connectme-frontend, connectme-backend |
| Client Roles | 19 | Granular permissions (claim:*, user:*, etc.) |
| Realm Roles | 4 | admin, manager, staff, billing |
| Composite Relationships | 8 | All properly linked |
| Protocol Mappers | 2 | Realm roles + Client roles in JWT |
| Redirect URIs | 4 | localhost + production |
| CORS Settings | ✅ | Configured for localhost + production |

---

## 🎊 You're Done!

**Total time:** 2-3 minutes (import + create user)

**Result:** Complete RBAC system ready to use!

**vs Manual Setup:** Saves ~15-20 minutes of role creation! 🚀

---

## 📚 Additional Resources

- **Manual Setup:** `KEYCLOAK_CREATE_ROLES_STEP_BY_STEP.md`
- **Quick Reference:** `ROLES_QUICK_REFERENCE.txt`
- **Role Integration:** `KEYCLOAK_ROLES_INTEGRATION.md`

---

**Ready to import? Just drag and drop the JSON file!** 🎉
