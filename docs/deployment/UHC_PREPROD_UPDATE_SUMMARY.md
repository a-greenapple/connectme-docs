# UHC Pre-Prod Configuration Update - Summary

## 📋 What Was Created

I've created tools to update the UHC configuration in your pre-production database:

### 1. **Update Script** (`connectme-backend/update_uhc_preprod.py`)
   - ✅ Standalone Python script
   - ✅ Updates OAuth credentials
   - ✅ Updates API endpoints
   - ✅ Verifies configuration
   - ✅ Provides detailed output

### 2. **Shell Script** (`scripts/preprod/update-uhc-config.sh`)
   - ✅ Automates remote deployment
   - ✅ SSH into pre-prod server
   - ✅ Runs update script
   - ✅ Cleans up after execution

### 3. **Comprehensive Guide** (`PREPROD_UHC_UPDATE_GUIDE.md`)
   - ✅ 3 different update methods
   - ✅ Testing procedures
   - ✅ Troubleshooting guide
   - ✅ Security notes
   - ✅ Verification checklist

---

## 🚀 Quick Start - How to Update

### Easiest Method: Run Script on Server

```bash
# 1. SSH into pre-prod
ssh ubuntu@your-preprod-server.com

# 2. Navigate to backend
cd /var/www/connectme-backend

# 3. Upload the script (from your local machine)
# scp connectme-backend/update_uhc_preprod.py ubuntu@server:/var/www/connectme-backend/

# 4. Activate venv
source venv/bin/activate

# 5. Run update
python update_uhc_preprod.py
```

**Expected Output:**
```
================================================================================
🔧 Updating UHC Configuration in Pre-Prod Database
================================================================================

📋 Step 1: Checking UHC Provider...
   ✓ Found existing provider: UnitedHealthcare (ID: 1)

🔐 Step 2: Updating OAuth Credentials...
   ✓ Updating existing credential (ID: 1)
   ✓ Updated Client ID

🔍 Step 3: Verifying Credentials...
   ✅ Verification: Secret matches!

🌐 Step 4: Updating API Endpoints...
   ✓ Auth URL: https://apimarketplace.uhc.com/oauth/token
   ✓ Base URL: https://apimarketplace.uhc.com/Claims

✅ UHC Configuration Updated Successfully!
```

---

## 🔐 Configuration Details

### Credentials Being Updated
```
Client ID:     <REDACTED_CLIENT_ID>
Client Secret: <REDACTED_SECRET>
Auth URL:      https://apimarketplace.uhc.com/oauth/token
Base URL:      https://apimarketplace.uhc.com/Claims
```

### What Gets Updated
1. **ProviderCredential** table:
   - `client_id` → Updated
   - `client_secret` → Updated (encrypted)
   - `is_active` → Set to True
   - `auth_type` → Set to 'oauth2'

2. **ProviderAPIEndpoint** table:
   - Auth endpoint URL
   - Base API URL
   - Both marked as active

---

## 🧪 Testing After Update

### Test 1: Verify in Database
```bash
python manage.py shell
```
```python
from apps.providers.models import ProviderCredential
cred = ProviderCredential.objects.get(provider__code='UHC', auth_type='oauth2')
print(f"Client ID: {cred.client_id}")
print(f"Active: {cred.is_active}")
```

### Test 2: Test OAuth Authentication
```bash
python test_uhc_auth_methods.py
```
Should return: `Status: 200` ✅

### Test 3: Test Claims API
```bash
python test_uhc_api.py
```

### Test 4: Test via Frontend
Navigate to: `https://your-preprod-domain.com/claims/search`
- Enter date range
- Click "Search Claims"
- Verify results appear

---

## ✅ Verification Checklist

After running the update, verify:

- [ ] Script completed without errors
- [ ] Client ID matches: `<REDACTED_CLIENT_ID>`
- [ ] Client Secret is encrypted (43 characters)
- [ ] Credential is marked as active
- [ ] Auth URL is correct
- [ ] Base URL is correct
- [ ] OAuth test returns status 200
- [ ] Claims search works in frontend
- [ ] Audit log shows the update

---

## 📁 Files Created

1. **`connectme-backend/update_uhc_preprod.py`**
   - Main update script
   - Run directly on pre-prod server

2. **`scripts/preprod/update-uhc-config.sh`**
   - Automated deployment script
   - Handles SSH and remote execution

3. **`PREPROD_UHC_UPDATE_GUIDE.md`**
   - Complete documentation
   - Multiple update methods
   - Troubleshooting guide

4. **`UHC_PREPROD_UPDATE_SUMMARY.md`** (this file)
   - Quick reference
   - Summary of changes

---

## 🔄 Alternative Update Methods

### Method 2: Django Admin UI
1. Go to: `https://your-preprod-domain.com/admin/`
2. Navigate to: **Providers → Provider credentials**
3. Find: **UnitedHealthcare - oauth2 Credentials**
4. Update Client ID and Secret
5. Save

### Method 3: Django Shell
```python
from apps.providers.models import Provider, ProviderCredential

provider = Provider.objects.get(code='UHC')
credential = ProviderCredential.objects.get(provider=provider, auth_type='oauth2')

credential.client_id = "<REDACTED_CLIENT_ID>"
credential.client_secret = "<REDACTED>"
credential.is_active = True
credential.save()

print("✅ Updated!")
```

---

## 🚨 Common Issues & Solutions

### Issue: Provider not found
**Solution**: Run `python setup_uhc_rsm.py` first

### Issue: Authentication fails (403)
**Solution**: Verify credentials are correct, check Azure Portal

### Issue: Encryption error
**Solution**: Ensure `ENCRYPTION_KEY` is set in `.env` file

---

## 📊 What This Enables

Once updated, your pre-prod environment will support:

✅ **Claims Search**
- Search by date range (up to 90 days)
- Optional patient filters
- Returns up to 50 claims per page

✅ **Claim Details**
- View full claim information
- Diagnosis and procedure codes
- Line-by-line breakdown
- Payment information

✅ **Bulk Upload**
- CSV file upload for bulk claims
- Async processing with Celery
- Error reporting and validation

---

## 🔒 Security Notes

- ✅ All secrets are encrypted using Fernet
- ✅ Updates are logged for HIPAA compliance
- ✅ Only admin users can modify credentials
- ✅ Credentials never exposed in logs or git

---

## 📞 Need Help?

If you encounter issues:

1. Check Django logs: `tail -f /var/www/connectme-backend/logs/django.log`
2. Review audit logs in Django Admin
3. Refer to `PREPROD_UHC_UPDATE_GUIDE.md` for detailed troubleshooting

---

## ✨ Next Steps

After updating the configuration:

1. ✅ Run the update script
2. ✅ Test OAuth authentication
3. ✅ Test claims search in frontend
4. ✅ Verify audit logs
5. ✅ Monitor for any API errors
6. ✅ Document the update

---

**Created**: October 31, 2025
**Environment**: Pre-Production
**Provider**: UnitedHealthcare (UHC)
**Status**: Ready to Deploy

