# 🔐 Keycloak Configuration - Quick Reference

## ✅ Keycloak is Running!

**URL:** http://localhost:8080  
**Admin Console:** http://localhost:8080/admin/  
**Login:** admin / admin

---

## 📋 Configuration Steps (5 minutes)

### Step 1: Create Realm

1. Open: http://localhost:8080/admin/
2. Login: `admin` / `admin`
3. Click dropdown (top-left, says "master")
4. Click "Create Realm"
5. **Realm name:** `connectme`
6. Click "Create"

✅ You should now see "connectme" in the dropdown

---

### Step 2: Create Client

1. In the left menu, click **"Clients"**
2. Click **"Create client"** button
3. **General Settings:**
   - Client type: `OpenID Connect`
   - Client ID: `connectme-frontend`
   - Click **"Next"**

4. **Capability config:**
   - Client authentication: **OFF** (toggle to off)
   - Authorization: **OFF**
   - Authentication flow:
     - ✅ Standard flow
     - ✅ Direct access grants
   - Click **"Next"**

5. **Login settings:**
   - Root URL: `http://localhost:3000`
   - Valid redirect URIs: `http://localhost:3000/*`
   - Valid post logout redirect URIs: `http://localhost:3000/*`
   - Web origins: `http://localhost:3000`
   - Click **"Save"**

✅ Client created successfully!

---

### Step 3: Create Test User

1. In the left menu, click **"Users"**
2. Click **"Add user"** button
3. **User details:**
   - Username: `testuser`
   - Email: `test@connectme.com`
   - First name: `Test`
   - Last name: `User`
   - Email verified: **ON** (toggle to on)
4. Click **"Create"**

✅ User created!

---

### Step 4: Set User Password

1. You should now be on the user details page
2. Click the **"Credentials"** tab
3. Click **"Set password"** button
4. **Password settings:**
   - Password: `testpass123`
   - Password confirmation: `testpass123`
   - Temporary: **OFF** (toggle to off)
5. Click **"Save"**
6. Confirm by clicking **"Save password"**

✅ Password set!

---

### Step 5: (Optional) Create Roles

1. In the left menu, click **"Realm roles"**
2. Click **"Create role"**
3. Create these roles:
   - Role name: `admin`
   - Description: `Administrator access`
   - Click "Save"

Repeat for:
- `manager` - Manager access
- `staff` - Staff access
- `billing` - Billing access

---

### Step 6: (Optional) Assign Roles to User

1. Go to **Users** → Find `testuser` → Click on username
2. Click **"Role mapping"** tab
3. Click **"Assign role"**
4. Select `admin` role
5. Click **"Assign"**

✅ User has admin role!

---

## 🧪 Test Configuration

### Test 1: Get Token via curl

```bash
curl -X POST http://localhost:8080/realms/connectme/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password"
```

**Expected:** JSON response with `access_token`

### Test 2: Use Test Script

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./TEST_KEYCLOAK.sh
```

**Expected:** ✅ All tests pass

---

## 🚀 Start Your Application

Once Keycloak is configured:

```bash
# Test Keycloak connection
./TEST_KEYCLOAK.sh

# Start backend and frontend
./START_TESTING.sh

# Or manually:
# Terminal 1 - Backend
cd backend && venv/bin/python manage.py runserver 8000

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open browser
open http://localhost:3000
```

**Login with:**
- Username: `testuser`
- Password: `testpass123`

---

## 📊 Useful Commands

### Check Keycloak Status
```bash
docker-compose -f docker-compose-keycloak.yml ps
```

### View Logs
```bash
docker logs -f keycloak
```

### Restart Keycloak
```bash
docker-compose -f docker-compose-keycloak.yml restart
```

### Stop Keycloak
```bash
docker-compose -f docker-compose-keycloak.yml down
```

### Start Keycloak
```bash
docker-compose -f docker-compose-keycloak.yml up -d
```

---

## 🐛 Troubleshooting

### Can't access admin console

**Check if Keycloak is running:**
```bash
curl http://localhost:8080/health/ready
```

**Check logs:**
```bash
docker logs keycloak
```

### Forgot admin password

**Reset password:**
```bash
docker exec -it keycloak /opt/keycloak/bin/kc.sh \
  user-password --username admin --password newpassword
```

### Token request fails

**Verify:**
1. Realm name is exactly: `connectme`
2. Client ID is exactly: `connectme-frontend`
3. User exists with correct password
4. Client authentication is OFF (public client)

---

## ✅ Configuration Checklist

- [ ] Keycloak running on http://localhost:8080
- [ ] Can access admin console
- [ ] Realm "connectme" created
- [ ] Client "connectme-frontend" created
- [ ] Client redirect URIs configured
- [ ] User "testuser" created
- [ ] User password set to "testpass123"
- [ ] Can get token via curl
- [ ] `./TEST_KEYCLOAK.sh` passes
- [ ] Frontend `.env.local` updated
- [ ] Application login works

---

## 🎉 All Done!

Once all steps are complete, your Keycloak is fully configured and ready!

**Next:** Run `./START_TESTING.sh` and test your application!

**Documentation:**
- Quick Start: `KEYCLOAK_QUICK_START.md`
- Full Guide: `KEYCLOAK_DOCKER_GUIDE.md`
- Deployment: `🎉_KEYCLOAK_DOCKER_READY.md`
