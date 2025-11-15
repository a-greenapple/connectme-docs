# Claims Search 403 Error - Quick Fix Guide
**Error:** `Failed to load resource: the server responded with a status of 403 (Forbidden)`  
**Message:** `"Authentication credentials were not provided."`

---

## 🔍 Diagnosis

Run the diagnostic script:
```bash
python3 testing/diagnose_auth_issue.py
```

This will test:
1. ✅ Token generation from Keycloak
2. ✅ Practice API with token
3. ✅ Claims search API with token

---

## 🔧 Quick Fixes

### Fix 1: Clear Browser Cache and Re-login

1. **Hard refresh** the page: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
2. **Clear localStorage:**
   - Open browser console (F12)
   - Run: `localStorage.clear()`
   - Refresh page
3. **Re-login:**
   - Go to: https://pre-prod.connectme.apps.totessoft.com/login
   - Login again

### Fix 2: Check Token in Browser

1. Open browser console (F12)
2. Check if token exists:
   ```javascript
   localStorage.getItem('kc_access_token')
   ```
3. If `null`, you need to re-login
4. If token exists, check if it's valid:
   ```javascript
   // Check expiration
   const expiresAt = localStorage.getItem('kc_expires_at');
   const now = Date.now();
   console.log('Token expired:', now > parseInt(expiresAt));
   ```

### Fix 3: Verify Backend is Running

```bash
# Check backend status
ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-backend'

# Check recent logs
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 50 --no-pager'
```

### Fix 4: Check Keycloak Authentication Class

The backend needs to use `KeycloakAuthentication`. Verify:

```bash
ssh connectme@169.59.163.43 'grep -r "KeycloakAuthentication" /var/www/connectme-preprod-backend/apps/claims/api_views.py'
```

Should show:
```python
from apps.auth.keycloak import KeycloakAuthentication
@authentication_classes([KeycloakAuthentication])
```

---

## 🐛 Common Issues

### Issue 1: Token Not Being Sent

**Symptoms:**
- 403 error
- "Authentication credentials were not provided"

**Solution:**
- Check browser console for errors
- Verify `kc_access_token` exists in localStorage
- Re-login if token is missing

### Issue 2: Token Expired

**Symptoms:**
- 401 error
- "Token has expired"

**Solution:**
- The frontend should auto-refresh
- If not, clear localStorage and re-login

### Issue 3: CORS Error

**Symptoms:**
- CORS policy error in console
- Preflight request fails

**Solution:**
```bash
# Check CORS settings in backend
ssh connectme@169.59.163.43 'grep -A 5 "CORS_ALLOWED_ORIGINS" /var/www/connectme-preprod-backend/config/settings.py'
```

Should include: `https://pre-prod.connectme.apps.totessoft.com`

### Issue 4: Backend Authentication Not Configured

**Symptoms:**
- 403 even with valid token
- Backend logs show "Forbidden"

**Solution:**
Check if `KeycloakAuthentication` is imported and used:

```python
# In apps/claims/api_views.py
from apps.auth.keycloak import KeycloakAuthentication

@api_view(['POST'])
@authentication_classes([KeycloakAuthentication])
@permission_classes([IsAuthenticated])
def search_claims(request):
    ...
```

---

## 📊 Testing

### Manual Test in Browser Console

```javascript
// Get token
const token = localStorage.getItem('kc_access_token');
console.log('Token:', token ? token.substring(0, 30) + '...' : 'NOT FOUND');

// Test claims search
fetch('https://pre-prod.connectme.be.totessoft.com/api/v1/claims/search/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    firstServiceDate: '2025-10-01',
    lastServiceDate: '2025-10-31',
    practiceId: '1'
  })
})
.then(r => r.json())
.then(d => console.log('Response:', d))
.catch(e => console.error('Error:', e));
```

### Automated Test

```bash
python3 testing/test_claims_search.py
```

---

## 🔍 Debug Backend

### Check Authentication Flow

```bash
# Monitor backend logs while testing
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'

# Then try searching claims in the frontend
# Look for:
# - "JWT] Attempting to authenticate token"
# - "JWT] User found"
# - Any 403/401 errors
```

### Check Practice Configuration

```bash
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell << EOF
from apps.providers.models import Practice, PracticePayerMapping

# Check practices
practices = Practice.objects.filter(is_active=True)
print(f"Active Practices: {practices.count()}")
for p in practices:
    print(f"  - {p.name} (ID: {p.id}, TIN: {p.tin})")
    mappings = PracticePayerMapping.objects.filter(practice=p, is_active=True)
    for m in mappings:
        print(f"    → {m.provider.name} (Payer ID: {m.payer_id})")
EOF
'
```

---

## ✅ Verification Steps

After applying fixes:

1. ✅ **Login works** - Can login successfully
2. ✅ **Token exists** - `localStorage.getItem('kc_access_token')` returns token
3. ✅ **Practice dropdown appears** - Shows "RSM (TIN: 854203105)"
4. ✅ **Claims search works** - No 403 error
5. ✅ **Results display** - Claims are shown (or "No claims found")

---

## 🚨 If Nothing Works

1. **Restart backend:**
   ```bash
   ssh connectme@169.59.163.43 'sudo systemctl restart connectme-preprod-backend'
   ```

2. **Restart frontend:**
   ```bash
   ssh connectme@169.59.163.43 'pm2 restart connectme-preprod-frontend'
   ```

3. **Check all services:**
   ```bash
   ssh connectme@169.59.163.43 '
   echo "Backend:" && sudo systemctl status connectme-preprod-backend --no-pager | head -10
   echo ""
   echo "Frontend:" && pm2 status
   echo ""
   echo "Celery:" && sudo systemctl status connectme-preprod-celery --no-pager | head -10
   '
   ```

4. **Run diagnostic script:**
   ```bash
   python3 testing/diagnose_auth_issue.py
   ```

---

## 📞 Need Help?

If the issue persists:
1. Run: `python3 testing/diagnose_auth_issue.py`
2. Capture backend logs: `ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 200 --no-pager' > backend_logs.txt`
3. Capture browser console output (screenshot)
4. Share all outputs for debugging

---

**Most Common Fix:** Clear browser cache, clear localStorage, and re-login! 🔄

