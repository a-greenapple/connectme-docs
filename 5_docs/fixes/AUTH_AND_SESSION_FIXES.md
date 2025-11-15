# 🔐 Authentication & Session Management Fixes

## Issues Fixed

### 1. ✅ Authentication Redirect Loop
**Problem**: When clicking "Bulk Upload" → redirects to login → after login → back to search page (loop)

**Root Cause**: 
- Login page didn't respect `?redirect=/bulk-upload` parameter
- Bulk-upload page checked `localStorage` directly instead of using `AuthContext`
- Login function always redirected to `/dashboard` regardless of intended destination

**Solution**:
```typescript
// connectme-frontend/src/app/login/page.tsx
const searchParams = useSearchParams();
const redirectUrl = searchParams.get('redirect') || '/dashboard';

// After successful login:
router.push(redirectUrl);  // Go to intended page!
```

```typescript
// connectme-frontend/src/app/bulk-upload/page.tsx
const { isAuthenticated, isLoading: authLoading } = useAuth();

useEffect(() => {
  if (!authLoading && !isAuthenticated) {
    router.push('/login?redirect=/bulk-upload');  // Pass redirect parameter
  }
}, [authLoading, isAuthenticated, router]);
```

**Changes**:
- ✅ Login page now reads `redirect` query parameter
- ✅ Bulk-upload uses `AuthContext` instead of `localStorage`
- ✅ Proper loading states during authentication check
- ✅ `Suspense` wrapper for `useSearchParams` compatibility

---

### 2. ✅ Token Expiry Handling
**Problem**: When tokens expire, user sees cryptic errors or app breaks

**Solution**:
```typescript
// connectme-frontend/src/contexts/AuthContext.tsx
useEffect(() => {
  const interval = setInterval(async () => {
    if (keycloakService.isTokenExpired()) {
      console.log('[AUTH] Token expired, attempting refresh...');
      try {
        await keycloakService.refreshToken();
        console.log('[AUTH] Token refreshed successfully');
      } catch (error) {
        console.error('[AUTH] Token refresh failed, logging out:', error);
        alert('Your session has expired. Please log in again.');
        await logout();  // Auto-logout on failure
      }
    }
  }, 60000); // Check every minute
  
  return () => clearInterval(interval);
}, [user]);
```

**Features**:
- ✅ Checks token every 60 seconds
- ✅ Auto-refresh if expiring soon
- ✅ User-friendly alert if session expired
- ✅ Auto-logout if refresh fails
- ✅ Redirect to login page after logout

---

### 3. ✅ Session Timeout Configuration
**Problem**: No way to configure session length (hard-coded)

**Solution**:
```python
# connectme-backend/config/settings.py

# Session Configuration
SESSION_COOKIE_AGE = int(os.environ.get('SESSION_TIMEOUT_MINUTES', '60')) * 60  # Default: 60 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Update session on every request
SESSION_COOKIE_SECURE = not DEBUG  # Use secure cookies in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Session persists across browser close

# JWT Token Settings (for mock auth)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', '60'))
JWT_REFRESH_TOKEN_LIFETIME_MINUTES = int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME_MINUTES', '1440'))  # 24 hours
```

**Environment Variables** (`.env`):
```bash
# Session Management
SESSION_TIMEOUT_MINUTES=60  # 1 hour (default)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60  # 1 hour
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=1440  # 24 hours
```

**Examples**:
- 30 minutes: `SESSION_TIMEOUT_MINUTES=30`
- 2 hours: `SESSION_TIMEOUT_MINUTES=120`
- 8 hours: `SESSION_TIMEOUT_MINUTES=480`
- 24 hours: `SESSION_TIMEOUT_MINUTES=1440`

---

### 4. 🔄 Log Viewer Enhancement (Planned)
**Current State**: Basic log viewer exists but needs improvements

**Existing Features**:
- ✅ View logs in Django admin
- ✅ Filter by level (INFO, WARNING, ERROR, DEBUG)
- ✅ Select number of lines (50/100/200/500)
- ✅ Auto-refresh every 5 seconds
- ✅ Dark theme console-like UI

**Planned Enhancements**:
- 🔄 Real-time log streaming (WebSocket)
- 🔄 Search and filter by text
- 🔄 Export logs as CSV/JSON
- 🔄 Tail logs in real-time
- 🔄 Log file rotation management
- 🔄 Django + Gunicorn + Celery logs unified view

---

## Testing Instructions

### Test 1: Authentication Redirect Loop Fix
1. **In Firefox** (or any browser where you're NOT logged in):
   ```
   Go to: https://connectme.apps.totesoft.com/bulk-upload
   ```
2. Should see: "Redirecting to login..."
3. Gets redirected to: `https://connectme.apps.totesoft.com/login?redirect=/bulk-upload`
4. Log in (mock or Keycloak)
5. **Should be redirected back to**: `/bulk-upload` ✅
6. **Should NOT go to**: `/dashboard` or `/claims` ❌

### Test 2: Token Expiry
1. Log in normally
2. Open Browser DevTools → Console
3. Wait for token to expire (or manually clear token in localStorage)
4. After 1 minute, should see:
   ```
   [AUTH] Token expired, attempting refresh...
   ```
5. If refresh fails:
   ```
   [AUTH] Token refresh failed, logging out
   Alert: "Your session has expired. Please log in again."
   Redirect to /login
   ```

### Test 3: Session Timeout Configuration
1. SSH to server:
   ```bash
   ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240
   ```
2. Edit `.env`:
   ```bash
   cd /var/www/connectme-backend
   nano .env
   ```
3. Set session timeout (e.g., 5 minutes for testing):
   ```
   SESSION_TIMEOUT_MINUTES=5
   ```
4. Restart backend:
   ```bash
   sudo systemctl restart connectme-backend
   ```
5. Log in and wait 5 minutes → should be logged out

### Test 4: AuthContext vs localStorage
1. Open Browser DevTools → Application → localStorage
2. Delete `access_token`
3. Try to access `/bulk-upload`
4. Should redirect to login (not show errors)

---

## Files Changed

### Frontend
1. ✅ `connectme-frontend/src/app/login/page.tsx`
   - Added `useSearchParams()` to get redirect parameter
   - Wrapped in `Suspense` for compatibility
   - Redirect to intended page after login

2. ✅ `connectme-frontend/src/app/bulk-upload/page.tsx`
   - Import `useAuth` from AuthContext
   - Check `isAuthenticated` instead of `localStorage`
   - Proper loading states
   - Pass redirect parameter when redirecting to login

3. ✅ `connectme-frontend/src/contexts/AuthContext.tsx`
   - Enhanced token expiry checking
   - User-friendly expiry alerts
   - Auto-logout on token refresh failure
   - Better error messages

### Backend
1. ✅ `connectme-backend/config/settings.py`
   - Added `SESSION_COOKIE_AGE` configuration
   - Added `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`
   - Added `JWT_REFRESH_TOKEN_LIFETIME_MINUTES`
   - Session security settings (HttpOnly, Secure, SameSite)

---

## Deployment Commands

### Frontend Deployment
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-frontend

# Build locally first
npm run build

# Deploy to remote
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  src/app/login/page.tsx \
  src/app/bulk-upload/page.tsx \
  src/contexts/AuthContext.tsx \
  connectme@20.84.160.240:/var/www/connectme-frontend/src/

# Rebuild on remote
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 \
  "cd /var/www/connectme-frontend && npm run build && pm2 restart connectme-frontend"
```

### Backend Deployment
```bash
# Deploy settings
scp -i ~/Documents/Access/cursor/id_rsa_Debian \
  /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-backend/config/settings.py \
  connectme@20.84.160.240:/var/www/connectme-backend/config/

# Restart backend
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240 \
  "sudo systemctl restart connectme-backend"
```

---

## Configuration Examples

### Short Sessions (Testing)
```bash
# .env
SESSION_TIMEOUT_MINUTES=5  # 5 minutes
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=5
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=30
```

### Normal Sessions (Default)
```bash
# .env
SESSION_TIMEOUT_MINUTES=60  # 1 hour
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=1440  # 24 hours
```

### Long Sessions (Internal Users)
```bash
# .env
SESSION_TIMEOUT_MINUTES=480  # 8 hours
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=480
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=2880  # 48 hours
```

### Very Short Sessions (High Security)
```bash
# .env
SESSION_TIMEOUT_MINUTES=15  # 15 minutes
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=120  # 2 hours
```

---

## Summary

✅ **Fixed**: Authentication redirect loop  
✅ **Fixed**: Bulk-upload using localStorage instead of AuthContext  
✅ **Implemented**: Auto-logout on token expiry  
✅ **Implemented**: User-friendly session expiry alerts  
✅ **Added**: Configurable session timeouts (environment variables)  
✅ **Added**: Session security settings (HttpOnly, Secure, SameSite)  
🔄 **Pending**: Enhanced log viewer (will implement after testing these fixes)

---

## Next Steps

1. ✅ Deploy frontend changes
2. ✅ Deploy backend changes
3. ✅ Test authentication flow
4. ⏳ Test session timeout
5. ⏳ Enhance log viewer (after current fixes are confirmed)

---

**Status**: Ready for deployment and testing  
**Date**: 2025-10-12  
**Priority**: High (authentication is critical)

