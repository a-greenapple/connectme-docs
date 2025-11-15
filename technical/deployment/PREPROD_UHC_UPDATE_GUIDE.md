# Pre-Prod UHC Configuration Update Guide

## Overview
This guide explains how to update the UHC (UnitedHealthcare) API credentials in the pre-production database.

---

## 🔐 UHC Credentials

The following credentials are configured for the UHC API integration:

```
Client ID:     <REDACTED_CLIENT_ID>
Client Secret: <REDACTED_SECRET>
Auth URL:      https://apimarketplace.uhc.com/oauth/token
Base URL:      https://apimarketplace.uhc.com/Claims
```

---

## 📋 Option 1: Run Update Script on Pre-Prod Server (Recommended)

### Step 1: SSH into Pre-Prod Server
```bash
ssh ubuntu@your-preprod-server.com
```

### Step 2: Navigate to Backend Directory
```bash
cd /var/www/connectme-backend
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 4: Copy the Update Script
Create a file named `update_uhc_preprod.py` with the contents from:
`connectme-backend/update_uhc_preprod.py`

Or upload it:
```bash
# From your local machine
scp connectme-backend/update_uhc_preprod.py ubuntu@your-preprod-server.com:/var/www/connectme-backend/
```

### Step 5: Run the Update Script
```bash
python update_uhc_preprod.py
```

### Expected Output
```
================================================================================
🔧 Updating UHC Configuration in Pre-Prod Database
================================================================================

📋 Step 1: Checking UHC Provider...
   ✓ Found existing provider: UnitedHealthcare (ID: 1)

🔐 Step 2: Updating OAuth Credentials...
   ✓ Updating existing credential (ID: 1)
   ✓ Updated Client ID: old-id → <REDACTED_CLIENT_ID>

🔍 Step 3: Verifying Credentials...
   ✓ Client ID: <REDACTED_CLIENT_ID>
   ✓ Client Secret Length: 43 characters
   ✓ Client Secret (first 10): _zy8Q~_QT8...
   ✓ Client Secret (last 10): ...tqTvO-2dfp
   ✓ Active: True
   ✓ Auth Type: oauth2
   ✅ Verification: Secret matches!

🌐 Step 4: Updating API Endpoints...
   ✓ Auth URL: https://apimarketplace.uhc.com/oauth/token
   ✓ Base URL: https://apimarketplace.uhc.com/Claims

================================================================================
✅ UHC Configuration Updated Successfully!
================================================================================
```

---

## 📋 Option 2: Update via Django Admin UI

### Step 1: Access Django Admin
Navigate to: `https://your-preprod-domain.com/admin/`

### Step 2: Login
Use your admin credentials

### Step 3: Navigate to Provider Credentials
Go to: **Providers → Provider credentials**

### Step 4: Find UHC OAuth Credential
Look for: **UnitedHealthcare - oauth2 Credentials**

### Step 5: Update Fields
- **Client ID**: `<REDACTED_CLIENT_ID>`
- **Client Secret**: `<REDACTED_SECRET>`
- **Is Active**: ✓ (checked)

### Step 6: Update API Endpoints
Go to: **Providers → Provider API endpoints**

Update or create:
1. **Auth Endpoint**:
   - Provider: UnitedHealthcare
   - Endpoint Type: auth
   - URL: `https://apimarketplace.uhc.com/oauth/token`
   - Is Active: ✓

2. **Base Endpoint**:
   - Provider: UnitedHealthcare
   - Endpoint Type: base
   - URL: `https://apimarketplace.uhc.com/Claims`
   - Is Active: ✓

---

## 📋 Option 3: Update via Django Shell

### Step 1: SSH and Navigate
```bash
ssh ubuntu@your-preprod-server.com
cd /var/www/connectme-backend
source venv/bin/activate
```

### Step 2: Open Django Shell
```bash
python manage.py shell
```

### Step 3: Run Update Commands
```python
from apps.providers.models import Provider, ProviderCredential, ProviderAPIEndpoint

# Get UHC provider
provider = Provider.objects.get(code='UHC')

# Update credentials
credential = ProviderCredential.objects.get(provider=provider, auth_type='oauth2')
credential.client_id = "<REDACTED_CLIENT_ID>"
credential.client_secret = "<REDACTED>"
credential.is_active = True
credential.save()

# Update auth endpoint
auth_ep, _ = ProviderAPIEndpoint.objects.update_or_create(
    provider=provider,
    endpoint_type='auth',
    defaults={'url': 'https://apimarketplace.uhc.com/oauth/token', 'is_active': True}
)

# Update base endpoint
base_ep, _ = ProviderAPIEndpoint.objects.update_or_create(
    provider=provider,
    endpoint_type='base',
    defaults={'url': 'https://apimarketplace.uhc.com/Claims', 'is_active': True}
)

print("✅ Configuration updated!")
```

---

## 🧪 Testing the Configuration

### Test 1: Verify Database Update
```bash
python manage.py shell
```

```python
from apps.providers.models import Provider, ProviderCredential

provider = Provider.objects.get(code='UHC')
credential = ProviderCredential.objects.get(provider=provider, auth_type='oauth2')

print(f"Client ID: {credential.client_id}")
print(f"Secret Length: {len(credential.client_secret)}")
print(f"Active: {credential.is_active}")
```

### Test 2: Test OAuth Authentication
```bash
python test_uhc_auth_methods.py
```

Expected output should show successful authentication with status 200.

### Test 3: Test Claims API
```bash
python test_uhc_api.py
```

This will test the full claims search workflow.

### Test 4: Test via Frontend
1. Navigate to: `https://your-preprod-domain.com/claims/search`
2. Enter search criteria:
   - First Service Date: 01/01/2024
   - Last Service Date: 01/31/2024
3. Click "Search Claims"
4. Verify results are returned

---

## 🔍 Verification Checklist

- [ ] UHC Provider exists in database
- [ ] OAuth credentials are updated
- [ ] Client ID matches: `<REDACTED_CLIENT_ID>`
- [ ] Client Secret is encrypted and stored
- [ ] Auth URL is: `https://apimarketplace.uhc.com/oauth/token`
- [ ] Base URL is: `https://apimarketplace.uhc.com/Claims`
- [ ] Credential is marked as active
- [ ] OAuth authentication test passes (status 200)
- [ ] Claims search API test passes
- [ ] Frontend claims search works
- [ ] Audit log shows credential update

---

## 🚨 Troubleshooting

### Issue: "Provider matching query does not exist"
**Solution**: Run the provider setup script first:
```bash
python setup_uhc_rsm.py
```

### Issue: "Authentication failed with 403 Forbidden"
**Possible Causes**:
1. Client Secret is incorrect
2. Client ID is incorrect
3. Credentials expired

**Solution**: Verify credentials in Azure Portal and update again.

### Issue: "Invalid Authorization header for this API"
**Solution**: UHC doesn't support Basic Auth. Ensure using OAuth 2.0 with client credentials in request body.

### Issue: "Encrypted secret doesn't decrypt correctly"
**Possible Causes**:
1. ENCRYPTION_KEY changed between encrypt/decrypt
2. Database encoding issue

**Solution**: 
```bash
# Check ENCRYPTION_KEY in .env
grep ENCRYPTION_KEY /var/www/connectme-backend/.env

# Re-save the credential to re-encrypt
python update_uhc_preprod.py
```

---

## 📊 Configuration Details

### Practice Configuration
- **Practice Name**: RSM
- **TIN**: 854203105
- **UHC Payer ID**: 87726

### Workflow Configuration
The following workflows are configured:

1. **Search Claims by Provider** (`/api/claim/summary/byprovider/v2.0`)
   - Search for claims by date range
   - Optional patient filters
   - Returns up to 50 claims per page

2. **Get Claim Details** (`/api/claim/detail/v2.0`)
   - Get detailed information for a specific claim
   - Includes line items, diagnosis codes, payment info

### API Limitations
- **Date Range**: Maximum 90 days
- **Lookback Period**: Last 24 months only
- **Results per Page**: Maximum 50 claims
- **Total Results**: Maximum 500 claims per search

---

## 📝 Audit Trail

All credential updates are automatically logged by django-auditlog. To view:

### Via Django Admin
Navigate to: **Audit Log → Log entries**
Filter by:
- Content Type: Provider credential
- Action: Update

### Via Django Shell
```python
from auditlog.models import LogEntry
from apps.providers.models import ProviderCredential

credential = ProviderCredential.objects.get(
    provider__code='UHC',
    auth_type='oauth2'
)

# Get all changes
for log in credential.history.all():
    print(f"{log.timestamp}: {log.action} by {log.actor}")
    print(f"  Changes: {log.changes}")
```

---

## 🔒 Security Notes

1. **Credential Encryption**: All secrets are encrypted using Fernet (symmetric encryption) before storage
2. **HIPAA Compliance**: Credential updates are logged for audit trail
3. **Access Control**: Only admin users can update provider credentials
4. **Secure Storage**: Never commit credentials to git or expose in logs
5. **Key Management**: ENCRYPTION_KEY must be consistent across environments

---

## 📞 Support

If you encounter issues:

1. Check the Django logs:
   ```bash
   tail -f /var/www/connectme-backend/logs/django.log
   ```

2. Check Celery logs (if using async tasks):
   ```bash
   tail -f /var/www/connectme-backend/logs/celery.log
   ```

3. Review audit logs in Django Admin

4. Contact system administrator with:
   - Error message
   - Timestamp
   - Steps to reproduce

---

## ✅ Post-Update Checklist

After updating the configuration:

- [ ] Run update script successfully
- [ ] Verify credentials in database
- [ ] Test OAuth authentication
- [ ] Test claims search API
- [ ] Test frontend claims search
- [ ] Check audit logs
- [ ] Document update in change log
- [ ] Notify team of update
- [ ] Monitor for API errors in logs
- [ ] Verify no impact on existing claims data

---

**Last Updated**: October 31, 2025
**Environment**: Pre-Production
**Provider**: UnitedHealthcare (UHC)
**Configuration Version**: 2.0

