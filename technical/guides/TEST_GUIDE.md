# ConnectMe Pre-Prod Testing Guide

## 🎯 Current Status: Password Reset Fix Deployed

### What Was Fixed:
1. ✅ Password reset now uses stored `keycloak_id` from Django user model
2. ✅ Falls back to username lookup if `keycloak_id` is missing
3. ✅ Stores `keycloak_id` for future use when found
4. ✅ Enhanced error logging for debugging

---

## 📋 Manual Test Checklist

### Test 1: User Creation ✓
**Goal:** Verify new users can be created successfully

1. Navigate to: https://pre-prod.connectme.apps.totessoft.com/users
2. Click "Create New User" button
3. Fill in the form:
   - First Name: Test
   - Last Name: User
   - Email: testuser@example.com
   - Username: testuser
   - Password: TestPass123!
   - Confirm Password: TestPass123!
   - Role: Select appropriate role
   - Organization: Select organization
4. Click "Create User"
5. **Expected:** Success message appears, user appears in the list

**Status:** [ ] Pass [ ] Fail

---

### Test 2: Password Reset (NEW FIX) ✓
**Goal:** Verify password reset works for newly created users

1. Find the newly created user in the list
2. Click the **blue key icon** (🔑) next to the user
3. Enter a new password: `NewPass123!`
4. Confirm the password: `NewPass123!`
5. Click "Reset Password"
6. **Expected:** Success message "Password reset successfully"

**Status:** [ ] Pass [ ] Fail

**If it fails:**
- Check backend logs: `ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 50'`
- Look for "User not found in Keycloak" or other errors

---

### Test 3: Login with New User ✓
**Goal:** Verify the new user can log in with the reset password

1. Log out from the admin account
2. Navigate to: https://pre-prod.connectme.apps.totessoft.com
3. Click "Login"
4. Enter credentials:
   - Username: `testuser`
   - Password: `NewPass123!` (the password you just reset)
5. Click "Sign In"
6. **Expected:** Successfully logged in, redirected to dashboard

**Status:** [ ] Pass [ ] Fail

---

### Test 4: User Deactivation ✓
**Goal:** Verify user can be deactivated/archived

1. Log back in as admin
2. Navigate to: https://pre-prod.connectme.apps.totessoft.com/users
3. Find a test user
4. Click the **archive/delete button** (trash icon)
5. Confirm the action
6. **Expected:** User is marked as inactive/archived

**Status:** [ ] Pass [ ] Fail

---

### Test 5: User Reactivation ✓
**Goal:** Verify archived user can be reactivated

1. Find the archived user in the list
2. Click the **activate button**
3. Confirm the action
4. **Expected:** User is marked as active again

**Status:** [ ] Pass [ ] Fail

---

### Test 6: API Documentation ✓
**Goal:** Verify Swagger/ReDoc is accessible

1. Navigate to: https://pre-prod.connectme.be.totessoft.com/api/docs/
2. **Expected:** Swagger UI loads with API documentation
3. Navigate to: https://pre-prod.connectme.be.totessoft.com/api/redoc/
4. **Expected:** ReDoc UI loads with API documentation

**Status:** [ ] Pass [ ] Fail

---

## 🔍 Debugging Commands

### Check Backend Logs (Real-time)
```bash
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'
```

### Check Recent Backend Errors
```bash
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100 --no-pager'
```

### Check Backend Status
```bash
ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-backend'
```

### Check Frontend Status
```bash
ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-frontend'
```

### Test API Directly (with your token)
```bash
# Get token first (use your actual credentials)
TOKEN=$(curl -s -X POST "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-preprod-frontend" \
  -d "username=YOUR_USERNAME" \
  -d "password=YOUR_PASSWORD" \
  -d "grant_type=password" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Test user list
curl -H "Authorization: Bearer $TOKEN" \
  "https://pre-prod.connectme.be.totessoft.com/api/v1/users/users/"

# Test user stats
curl -H "Authorization: Bearer $TOKEN" \
  "https://pre-prod.connectme.be.totessoft.com/api/v1/users/users/stats/"
```

---

## 📊 Test Results Summary

**Date:** ___________

**Tester:** ___________

| Test | Status | Notes |
|------|--------|-------|
| User Creation | [ ] Pass [ ] Fail | |
| Password Reset | [ ] Pass [ ] Fail | |
| Login with New User | [ ] Pass [ ] Fail | |
| User Deactivation | [ ] Pass [ ] Fail | |
| User Reactivation | [ ] Pass [ ] Fail | |
| API Documentation | [ ] Pass [ ] Fail | |

**Overall Status:** [ ] All Pass [ ] Some Failed

---

## 🐛 Known Issues

None currently - all previous issues have been resolved!

---

## 📝 Notes

- Password must be at least 8 characters
- Users are soft-deleted (archived) and permanently deleted after 30 days
- Keycloak sync happens automatically during user creation and password reset
- All API endpoints are documented at `/api/docs/`

---

## 🎉 Success Criteria

All tests should pass with:
- ✅ Users can be created
- ✅ Passwords can be reset immediately after creation
- ✅ New users can log in with reset password
- ✅ Users can be archived and reactivated
- ✅ API documentation is accessible

---

## 📞 Support

If any tests fail, check:
1. Backend logs for detailed error messages
2. Browser console for frontend errors
3. Keycloak admin console for user sync status
4. Network tab in browser DevTools for API responses

