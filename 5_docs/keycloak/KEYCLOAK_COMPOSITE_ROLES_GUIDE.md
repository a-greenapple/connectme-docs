# 🔐 Keycloak Composite Roles - Complete Guide

## What Are Composite Roles?

**Composite roles** are "container" roles that automatically include other roles. When you assign a composite role to a user, they automatically get all the roles it contains.

**Example:**
- `admin` (realm role) = composite of 47 client roles
- When you assign `admin` to a user, they automatically get all 47 permissions
- No need to manually assign each individual role!

---

## ✅ What You've Done (Manual Assignment)

You successfully assigned individual client roles:
- ✅ `claim:read`
- ✅ `claim:write`
- ✅ `claim:delete`

This works! But for complex roles like `admin` or `team_lead`, you'd need to assign 20-40 roles individually. That's where composite roles help.

---

## 🎯 How to Create Composite Roles (Step-by-Step)

### Method 1: Using Realm Import (EASIEST - Recommended)

**This is already done if you imported the realm JSON!**

The file `keycloak-realm-connectme-workflow-complete.json` already has composite roles configured. When you import it:

1. Go to: https://auth.totesoft.com/admin/
2. Realm dropdown → "Create Realm" (or "Partial Import" if realm exists)
3. Upload: `keycloak-realm-connectme-workflow-complete.json`
4. Click "Create" or "Import"

✅ **All composite relationships are automatically created!**

To verify:
1. Go to: Realm roles → `admin`
2. Click "Composite roles" tab
3. You should see all 47 client roles listed

---

### Method 2: Manual Creation (If Import Didn't Work)

#### Step 1: Create the Realm Role

1. Go to: **Realm roles** (left sidebar)
2. Click **Create role**
3. Fill in:
   - **Role name:** `admin`
   - **Description:** `System administrator with full access`
4. Click **Save**

#### Step 2: Enable Composite Roles

1. After saving, you'll see the role details page
2. Look for the **"Composite roles"** toggle at the top
3. **Turn it ON** (slide to the right, should turn blue)

#### Step 3: Add Client Roles to Composite

Once composite is enabled, you'll see a new section:

1. Click **"Assign role"** button
2. **Filter by:** Change dropdown to **"Filter by clients"**
3. Select your client: **connectme-frontend**
4. You'll see all 47 client roles
5. Select the roles you want to include (for `admin`, select ALL)
6. Click **Assign**

#### Step 4: Verify

1. Go back to the role
2. Click **"Composite roles"** tab
3. You should see all assigned roles listed

---

## 📋 Composite Role Definitions

### 1. Admin Role (47 roles)

```
Realm Role: admin
Composite of:
  ✅ All 47 client roles from connectme-frontend
```

**To create:**
1. Realm roles → Create `admin`
2. Enable "Composite roles"
3. Assign role → Filter by clients → connectme-frontend
4. Select ALL roles → Assign

### 2. Team Lead Role (24 roles)

```
Realm Role: team_lead
Composite of:
  ✅ claims:read
  ✅ claims:detail
  ✅ claims:export
  ✅ claims:search
  ✅ eligibility:read
  ✅ eligibility:detail
  ✅ eligibility:verify
  ✅ reports:view
  ✅ reports:generate
  ✅ reports:export
  ✅ reports:share
  ✅ work:view_own
  ✅ work:view_team
  ✅ work:annotate
  ✅ work:assign
  ✅ work:create
  ✅ work:close
  ✅ work:reopen
  ✅ jira:view
  ✅ jira:update
  ✅ history:view_team
  ✅ requery:request
  ✅ requery:approve
  ✅ team:manage
```

### 3. Analyst Role (11 roles)

```
Realm Role: analyst
Composite of:
  ✅ claims:read
  ✅ claims:detail
  ✅ claims:export
  ✅ claims:search
  ✅ eligibility:read
  ✅ eligibility:detail
  ✅ eligibility:verify
  ✅ reports:view
  ✅ work:view_own
  ✅ work:annotate
  ✅ work:create
  ✅ jira:view
  ✅ history:view_own
  ✅ requery:request
```

### 4. Read Only Role (4 roles)

```
Realm Role: read_only
Composite of:
  ✅ claims:read
  ✅ eligibility:read
  ✅ reports:view
  ✅ work:view_own
```

### 5. Auditor Role (7 roles)

```
Realm Role: auditor
Composite of:
  ✅ history:view
  ✅ reports:view
  ✅ reports:generate
  ✅ audit:view
  ✅ audit:export
  ✅ logs:view
  ✅ logs:export
```

---

## 🔍 How to Check If Composite Roles Work

### Test 1: Check Role Composition

1. Go to: **Realm roles** → Select `admin`
2. Click **"Composite roles"** tab
3. You should see a list of all included roles
4. If empty, composite roles weren't set up

### Test 2: Check User's Effective Roles

1. Go to: **Users** → Select a user
2. Click **"Role mapping"** tab
3. You'll see two sections:
   - **Assigned roles:** Roles directly assigned to user
   - **Effective roles:** All roles user has (including composite)
4. If you assigned `admin`, effective roles should show all 47 client roles

### Test 3: Check JWT Token

1. Login as the user
2. Decode the JWT token (use jwt.io)
3. Look for `realm_access.roles` and `resource_access.connectme-frontend.roles`
4. You should see all the roles from the composite

---

## 🚀 Quick Setup for Testing (Recommended Path)

Since you've already assigned individual roles manually, here's the fastest way to test:

### Option A: Use What You Have (Simplest)

Keep your manual assignments for now:
- User has: `claim:read`, `claim:write`, `claim:delete`
- This is enough to test the basic functionality
- We can add composite roles later

### Option B: Import Full Realm (Most Complete)

1. **Backup current setup** (if needed):
   - Realm settings → Action → "Partial export"
   - Save the JSON file

2. **Import complete realm**:
   - Realm dropdown → "Create Realm"
   - Name: `connectme-test` (use different name to avoid conflicts)
   - Upload: `keycloak-realm-connectme-workflow-complete.json`
   - Click "Create"

3. **Create test user in new realm**:
   - Users → Add user
   - Username: `testuser`
   - Email: `test@connectme.com`
   - Email verified: ON
   - Save

4. **Assign composite role**:
   - User → Role mapping tab
   - Assign role → Select `analyst`
   - Done! User now has all 14 analyst permissions

---

## 🎯 For Your Current Testing

**Good news:** You don't need composite roles to test the workflow implementation!

The workflow models, policies, and admin interface work independently of Keycloak roles. Here's what we'll test:

### Phase 1: Backend Testing (No Keycloak needed)
✅ Database models
✅ Policy enforcement
✅ Django admin interface
✅ Work item management

### Phase 2: API Testing (Keycloak needed)
- API endpoints with JWT authentication
- Role-based permissions
- This is where composite roles become useful

**Recommendation:** Let's test Phase 1 first (backend), then we can set up composite roles properly for Phase 2 (API).

---

## 📝 Summary

**What you did:** ✅ Manually assigned 3 client roles
**What composite roles do:** Automatically assign many roles at once
**Do you need them now?** No, not for backend testing
**When do you need them?** When building API endpoints with role-based permissions

**Next step:** Let's run the backend tests!

```bash
cd backend
python test_workflow_setup.py
```

This will test all the workflow models and policies without needing Keycloak integration yet.
