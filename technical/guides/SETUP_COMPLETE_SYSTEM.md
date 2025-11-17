# 🚀 Complete System Setup Guide

## Understanding the Architecture

### Django + Keycloak: Why Both?

**Keycloak (Authentication):**
- Handles login/logout
- Issues JWT tokens
- Manages passwords
- Provides SSO

**Django (Authorization + Business Logic):**
- Validates JWT tokens from Keycloak
- Links Keycloak users to organizations
- Manages permissions and data access
- Processes business logic (claims, workflows)

**The Flow:**
```
1. User logs in → Keycloak
2. Keycloak returns JWT token
3. Frontend sends token to Django API
4. Django validates token with Keycloak
5. Django looks up user in its database
6. Django checks user's organization
7. Django processes request with organization context
```

---

## 🔧 Setup Steps

### Step 1: Create Django User for Keycloak User

The Keycloak user (`test.analyst`) needs a corresponding Django user:

```bash
cd backend
python create_keycloak_user.py
```

This will:
- ✅ Create/update `test.analyst` user in Django
- ✅ Link user to an organization
- ✅ Set organization TIN (854203105 for RSM)

### Step 2: Verify UHC Configuration

Check if UHC provider is configured:

```bash
cd backend
python manage.py shell
```

Then run:
```python
from apps.providers.models import Provider, ProviderCredential

# Check if UHC provider exists
try:
    provider = Provider.objects.get(code='UHC')
    print(f"✅ Provider: {provider.name}")
    print(f"   Code: {provider.code}")
    print(f"   Active: {provider.is_active}")
    
    # Check credentials
    cred = ProviderCredential.objects.get(provider=provider, is_active=True)
    print(f"\n✅ Credentials:")
    print(f"   API Base URL: {cred.api_base_url}")
    print(f"   Client ID: {cred.client_id}")
    print(f"   Has Secret: {'Yes' if cred.client_secret else 'No'}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nRun: python setup_uhc_rsm.py")
```

If UHC is not configured, run:
```bash
python setup_uhc_rsm.py
```

### Step 3: Update UHC Credentials in Django Admin

1. Go to: http://localhost:8000/admin/
2. Login with admin credentials
3. Go to: **Providers** → **Provider credentials**
4. Find UHC credential
5. Update:
   - **API Base URL**: `https://api.uhc.com` (or your UHC API URL)
   - **Client ID**: Your UHC client ID
   - **Client Secret**: Your UHC client secret
   - **OAuth Token URL**: `https://api.uhc.com/oauth/token`
6. Save

---

## 🧪 Test the Complete Flow

### Test 1: Verify Django User

```bash
cd backend
python manage.py shell
```

```python
from apps.users.models import User

user = User.objects.get(username='test.analyst')
print(f"User: {user.username}")
print(f"Organization: {user.organization.name if user.organization else 'None'}")
print(f"TIN: {user.organization.tin if user.organization else 'None'}")
```

Expected output:
```
User: test.analyst
Organization: Test Healthcare Organization
TIN: 854203105
```

### Test 2: Test Login and Get Token

1. Open browser: http://localhost:3000/login
2. Login with: `test.analyst` / `test123`
3. Open DevTools (F12) → Console
4. Run: `localStorage.getItem('kc_access_token')`
5. Copy the token

### Test 3: Test Backend API with Token

Replace `YOUR_TOKEN` with the token from step 2:

```bash
curl -X POST http://localhost:8000/api/v1/claims/search/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstServiceDate": "2025-05-01",
    "lastServiceDate": "2025-05-02"
  }'
```

### Test 4: Test from Frontend

1. Go to: http://localhost:3000/claims
2. Enter dates:
   - First Service Date: 2025-05-01
   - Last Service Date: 2025-05-02
3. Click "Search Claims"

---

## 🐛 Common Errors & Solutions

### Error 1: "User is not associated with a practice"

**Cause:** Django user doesn't have an organization

**Solution:**
```bash
cd backend
python create_keycloak_user.py
```

### Error 2: "Provider matching query does not exist"

**Cause:** UHC provider not configured

**Solution:**
```bash
cd backend
python setup_uhc_rsm.py
```

### Error 3: "Practice matching query does not exist"

**Cause:** No practice linked to user's organization

**Solution:**
```bash
cd backend
python manage.py shell
```

```python
from apps.users.models import Organization
from apps.providers.models import Practice, Provider

org = Organization.objects.get(name="Test Healthcare Organization")
provider = Provider.objects.get(code='UHC')

practice, created = Practice.objects.get_or_create(
    organization=org,
    defaults={
        'name': org.name,
        'tin': org.tin,
        'npi': org.npi,
        'is_active': True
    }
)

print(f"Practice: {practice.name}")
```

### Error 4: "OAuth token failed"

**Cause:** Invalid UHC credentials

**Solution:**
1. Go to Django admin
2. Update UHC credentials with valid client_id and client_secret
3. Make sure API Base URL is correct

### Error 5: "PracticePayerMapping matching query does not exist"

**Cause:** Practice not linked to UHC payer

**Solution:**
```bash
cd backend
python manage.py shell
```

```python
from apps.providers.models import Practice, Provider, PracticePayerMapping

practice = Practice.objects.first()
provider = Provider.objects.get(code='UHC')

mapping, created = PracticePayerMapping.objects.get_or_create(
    practice=practice,
    provider=provider,
    defaults={
        'payer_id': '87726',  # UHC Payer ID
        'payer_name': 'UnitedHealthcare',
        'is_active': True
    }
)

print(f"Mapping: {mapping.payer_name} - {mapping.payer_id}")
```

---

## 📋 Complete Setup Checklist

- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Keycloak user created (`test.analyst`)
- [ ] Django user created (`test.analyst`)
- [ ] User linked to organization
- [ ] Organization has TIN
- [ ] UHC provider configured
- [ ] UHC credentials updated
- [ ] Practice created for organization
- [ ] Practice linked to UHC payer
- [ ] Can login to frontend
- [ ] Can get JWT token
- [ ] Backend validates token
- [ ] Can search claims

---

## 🎯 Quick Fix Script

Run this to set up everything:

```bash
cd backend

# 1. Create Django user
python create_keycloak_user.py

# 2. Setup UHC provider
python setup_uhc_rsm.py

# 3. Update credentials in Django admin
# Go to: http://localhost:8000/admin/providers/providercredential/
# Update client_id and client_secret

# 4. Test
python manage.py shell
```

Then in shell:
```python
from apps.users.models import User
from apps.providers.models import Provider, Practice, PracticePayerMapping

# Verify user
user = User.objects.get(username='test.analyst')
print(f"✅ User: {user.username}, Org: {user.organization.name}")

# Verify provider
provider = Provider.objects.get(code='UHC')
print(f"✅ Provider: {provider.name}")

# Verify practice
practice = Practice.objects.get(organization=user.organization)
print(f"✅ Practice: {practice.name}, TIN: {practice.tin}")

# Verify mapping
mapping = PracticePayerMapping.objects.get(practice=practice, provider=provider)
print(f"✅ Mapping: {mapping.payer_name}, Payer ID: {mapping.payer_id}")

print("\n🎉 All configured! Ready to search claims!")
```

---

## 🚀 You're Ready!

After completing the setup:

1. ✅ Login at http://localhost:3000/login
2. ✅ Go to http://localhost:3000/claims
3. ✅ Search for claims
4. ✅ See results!

---

**Need help? Check the backend terminal for error messages!**
