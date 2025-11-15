# ConnectMe Pre-Prod Configuration Summary
**Date:** November 6, 2025  
**Environment:** Pre-Production

---

## ✅ Complete Configuration Status

### 1. Provider Configuration ✅

#### UnitedHealthcare (UHC)
- **Provider Code:** UHC
- **Provider Name:** UnitedHealthcare
- **Status:** Active
- **Database ID:** 1

#### OAuth2 Credentials
- **Client ID:** `<REDACTED_CLIENT_ID>`
- **Client Secret:** `<REDACTED_SECRET>` (encrypted in database)
- **Auth URL:** `https://apimarketplace.uhc.com/oauth/token`
- **Base URL:** `https://apimarketplace.uhc.com/Claims`
- **Auth Type:** OAuth 2.0
- **Timeout:** 30 seconds
- **Max Retries:** 3

---

### 2. Practice Configuration ✅

#### RSM Practice
- **Practice Name:** RSM
- **TIN (Tax ID):** 854203105
- **NPI:** (Not configured)
- **Status:** Active
- **Payer ID (UHC):** 87726

**Practice-Payer Mapping:**
- RSM (TIN: 854203105) → UnitedHealthcare (Payer ID: 87726)
- Status: Active
- Effective Date: 2025-11-06

---

### 3. Organization Configuration ✅

#### Pre-Prod Test Org
- **Organization Name:** Pre-Prod Test Org
- **TIN:** 854203105 (linked to RSM practice)
- **Status:** Active

**Purpose:** Default organization for pre-prod testing users

---

### 4. Transaction Configuration ✅

#### Claims Status Inquiry Transaction
- **Transaction Code:** CLAIM_STATUS
- **Transaction Name:** Claims Status Inquiry
- **Description:** Query claim status and payment information
- **Provider:** UnitedHealthcare
- **Requires Authentication:** Yes
- **Cache Duration:** 900 seconds (15 minutes)
- **Status:** Active

---

### 5. Workflow Configuration ✅

#### Workflow 1: Claims Summary
- **Workflow Code:** CLAIM_SUMMARY
- **Workflow Name:** Claims Summary
- **Execution Order:** 1 (runs first)
- **HTTP Method:** GET
- **API Endpoint:** `/remittance/v1/summary`
- **Retry Attempts:** 3
- **Continue on Error:** No
- **Status:** Active

**Parameters:**
- `tin` (header, required) - From practice configuration
- `payerId` (header, required) - From payer mapping
- `startDate` (header, required) - User input
- `endDate` (header, required) - User input

**Response Mapping:**
- `claims` → `$.data`
- `total_count` → `$.totalCount`

---

#### Workflow 2: Claim Detail
- **Workflow Code:** CLAIM_DETAIL
- **Workflow Name:** Claim Detail
- **Execution Order:** 2 (runs after summary)
- **HTTP Method:** GET
- **API Endpoint:** `/remittance/v1/detail`
- **Depends On:** Claims Summary workflow
- **Retry Attempts:** 3
- **Continue on Error:** Yes (optional step)
- **Status:** Active

**Parameters:**
- `tin` (header, required) - From practice configuration
- `payerId` (header, required) - From payer mapping
- `claimNumber` (query, required) - User input or from previous workflow

**Response Mapping:**
- `claim_details` → `$.data`
- `line_items` → `$.data.lineItems`

---

## 🔄 Workflow Execution Flow

```
User Request
    ↓
1. Claims Summary Workflow
   - GET /remittance/v1/summary
   - Headers: tin, payerId, startDate, endDate
   - Returns: List of claims
    ↓
2. Claim Detail Workflow (for each claim)
   - GET /remittance/v1/detail
   - Headers: tin, payerId
   - Query: claimNumber
   - Returns: Detailed claim information with line items
```

---

## 📊 Database Tables Populated

### Providers Table
| ID | Code | Name | Status |
|----|------|------|--------|
| 1 | UHC | UnitedHealthcare | Active |

### Provider Credentials Table
| ID | Provider | Auth Type | Client ID | Auth URL |
|----|----------|-----------|-----------|----------|
| 1 | UHC | oauth2 | 88cebd3e-... | https://apimarketplace.uhc.com/oauth/token |

### Practices Table
| TIN | Name | NPI | Status |
|-----|------|-----|--------|
| 854203105 | RSM | - | Active |

### Practice Payer Mappings Table
| Practice | Provider | Payer ID | Status |
|----------|----------|----------|--------|
| RSM | UHC | 87726 | Active |

### Transactions Table
| Code | Name | Provider | Status |
|------|------|----------|--------|
| CLAIM_STATUS | Claims Status Inquiry | UHC | Active |

### Workflows Table
| Code | Name | Order | Transaction | Status |
|------|------|-------|-------------|--------|
| CLAIM_SUMMARY | Claims Summary | 1 | CLAIM_STATUS | Active |
| CLAIM_DETAIL | Claim Detail | 2 | CLAIM_STATUS | Active |

### Workflow Parameters Table
| Workflow | Parameter | Type | Source | Required |
|----------|-----------|------|--------|----------|
| CLAIM_SUMMARY | tin | header | config | Yes |
| CLAIM_SUMMARY | payerId | header | config | Yes |
| CLAIM_SUMMARY | startDate | header | user_input | Yes |
| CLAIM_SUMMARY | endDate | header | user_input | Yes |
| CLAIM_DETAIL | tin | header | config | Yes |
| CLAIM_DETAIL | payerId | header | config | Yes |
| CLAIM_DETAIL | claimNumber | query | user_input | Yes |

---

## 🧪 Testing Instructions

### 1. Test UHC Authentication
```bash
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python test_uhc_auth_methods.py
```

**Expected Output:**
```
✅ OAuth token obtained successfully
Token expires in: 3600 seconds
```

### 2. Test Claims API
```bash
python test_uhc_api.py
```

**Expected Output:**
```
✅ Claims summary retrieved
✅ Claim details retrieved
```

### 3. Test via Frontend
1. Navigate to: https://pre-prod.connectme.apps.totessoft.com/claims
2. Log in with admin credentials
3. Enter date range (e.g., last 30 days)
4. Click "Search Claims"
5. **Expected:** List of claims from UHC API

### 4. Test via Django Admin
1. Navigate to: https://pre-prod.connectme.be.totessoft.com/admin/
2. Log in with Django admin credentials
3. Check:
   - Providers → Should see UnitedHealthcare
   - Provider Credentials → Should see UHC credentials
   - Practices → Should see RSM
   - Practice Payer Mappings → Should see RSM → UHC mapping
   - Transactions → Should see Claims Status Inquiry
   - Workflows → Should see Claims Summary and Claim Detail

---

## 🔐 Security Notes

### Encrypted Data
- ✅ Client Secret is encrypted in database using `ENCRYPTION_KEY`
- ✅ OAuth tokens are not stored (fetched on-demand)
- ✅ All API calls use HTTPS

### Access Control
- ✅ Users can only access claims for their organization's TIN
- ✅ Admin users can manage all configurations
- ✅ API endpoints require authentication

---

## 📝 Configuration Files

### Backend Configuration
**File:** `/var/www/connectme-preprod-backend/.env`
```bash
# UHC API Configuration
UHC_PAYER_ID=87726
UHC_TIN=854203105
```

### Database Configuration
- All provider configurations are stored in PostgreSQL
- No hardcoded credentials in code
- All sensitive data is encrypted

---

## 🚀 API Endpoints

### Claims Summary
```
GET /api/v1/claims/uhc/summary/
Headers:
  - Authorization: Bearer <token>
  - tin: 854203105
  - payerId: 87726
  - startDate: 2025-10-01
  - endDate: 2025-11-06
```

### Claim Detail
```
GET /api/v1/claims/uhc/detail/
Headers:
  - Authorization: Bearer <token>
  - tin: 854203105
  - payerId: 87726
Query:
  - claimNumber: <claim_number>
```

---

## 🔄 Workflow Engine

The workflow engine automatically:
1. ✅ Retrieves OAuth token from UHC
2. ✅ Executes workflows in order
3. ✅ Passes data between workflows
4. ✅ Handles retries on failure
5. ✅ Logs all executions for audit
6. ✅ Caches results for performance

---

## 📈 Next Steps

### Immediate
- ✅ All configurations complete
- ✅ Ready for testing
- ✅ Ready for user acceptance testing

### Future Enhancements
1. **Add More Practices:**
   - Edit `setup_preprod_complete.py`
   - Add practice details to `PRACTICES` list
   - Run script again

2. **Add More Providers:**
   - Duplicate UHC configuration
   - Update credentials and endpoints
   - Configure workflows

3. **Add More Transactions:**
   - Eligibility checks
   - Prior authorizations
   - Claim submissions

4. **Monitoring:**
   - Set up workflow execution monitoring
   - Configure alerts for failures
   - Track API usage metrics

---

## 🎯 Success Criteria

- ✅ UHC provider configured
- ✅ OAuth2 credentials stored and encrypted
- ✅ RSM practice created
- ✅ Practice-payer mapping established
- ✅ Claims Status transaction configured
- ✅ Two workflows created (Summary + Detail)
- ✅ All workflow parameters defined
- ✅ Organization linked to practice
- ✅ Ready for claims processing

---

## 📞 Support

### Check Configuration
```bash
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py shell

# Check provider
from apps.providers.models import Provider
Provider.objects.all()

# Check practices
from apps.providers.models import Practice
Practice.objects.all()

# Check mappings
from apps.providers.models import PracticePayerMapping
PracticePayerMapping.objects.all()
```

### Troubleshooting
1. **OAuth fails:** Check credentials in Django Admin
2. **No claims returned:** Verify TIN and Payer ID
3. **Workflow fails:** Check workflow execution logs
4. **Permission denied:** Verify user's organization TIN

---

**Configuration completed successfully! 🎉**

