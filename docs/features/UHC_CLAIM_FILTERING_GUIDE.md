# UHC Claim Filtering by Status and TIN - Guide

**Last Updated:** November 13, 2024

## 🎯 Question: Can you get a list of claims with specific status for different TINs in UHC?

**Short Answer:** Yes, but with limitations based on UHC API capabilities.

---

## 📊 UHC API Capabilities

### What UHC API Supports

Based on the current implementation, the UHC Claims API (`/api/claim/summary/byprovider/v2.0`) supports:

#### ✅ Supported Filters

1. **TIN (Tax ID Number)** - Required header parameter
   - Sent as: `tin` header
   - Example: `tin: 854203105`
   - **One TIN per request**

2. **Date Range** - Required header parameters
   - `firstServiceDt`: Start date (MM/DD/YYYY)
   - `lastServiceDt`: End date (MM/DD/YYYY)
   - Example: `firstServiceDt: 01/01/2024`, `lastServiceDt: 01/31/2024`

3. **Payer ID** - Required header parameter
   - Sent as: `payerId` header
   - Example: `payerId: 87726` (UHC payer ID)

4. **Patient Filters** (Optional)
   - `ptntFn`: Patient first name
   - `ptntLn`: Patient last name
   - `ptntDob`: Patient date of birth (MM/DD/YYYY)

#### ❌ NOT Directly Supported by UHC API

- **Claim Status Filter** - UHC API returns ALL claims in date range
- **Multiple TINs in single request** - Must make separate requests per TIN

---

## 🔍 Current Implementation

### How Claims Are Retrieved

```python
# Location: connectme-backend/apps/claims/api_views.py (line 222)

url = f"{credential.api_base_url}/api/claim/summary/byprovider/v2.0"

headers = {
    'Authorization': f'Bearer {uhc_token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'tin': practice.tin,                    # Single TIN
    'firstServiceDt': format_date(first_date),
    'lastServiceDt': format_date(last_date),
    'payerId': payer_mapping.payer_id
}

# Optional patient filters
if patient_first:
    headers['ptntFn'] = patient_first
if patient_last:
    headers['ptntLn'] = patient_last
if patient_dob:
    headers['ptntDob'] = format_date(patient_dob)
```

### Response Structure

UHC returns claims with status information:

```json
{
  "claims": [
    {
      "claimNumber": "2024010001",
      "claimStatus": "PAID",
      "claimSummary": {
        "totalChargedAmt": "1500.00",
        "totalPaidAmt": "1200.00",
        "processedDt": "01/15/2024"
      }
    },
    {
      "claimNumber": "2024010002",
      "claimStatus": "PENDING",
      "claimSummary": {
        "totalChargedAmt": "800.00",
        "totalPaidAmt": null,
        "processedDt": null
      }
    },
    {
      "claimNumber": "2024010003",
      "claimStatus": "DENIED",
      "claimSummary": {
        "totalChargedAmt": "500.00",
        "totalPaidAmt": "0.00",
        "processedDt": "01/20/2024"
      }
    }
  ]
}
```

---

## 💡 Solution: Filter Claims by Status for Multiple TINs

Since UHC API doesn't support:
1. Status filtering in the API call
2. Multiple TINs in one request

You need to implement **client-side filtering** and **multiple API calls**.

### Approach 1: Sequential Queries (Current Implementation)

**Make separate API calls for each TIN, then filter by status:**

```python
# Pseudo-code
results_by_status = {}

for tin in tin_list:
    # Query UHC for this TIN
    claims = query_uhc_claims(
        tin=tin,
        first_date='2024-01-01',
        last_date='2024-01-31'
    )
    
    # Filter by desired status
    for claim in claims:
        status = claim.get('claimStatus')
        if status not in results_by_status:
            results_by_status[status] = []
        
        results_by_status[status].append({
            'tin': tin,
            'claim': claim
        })

# Now you have claims grouped by status across all TINs
```

### Approach 2: Bulk Upload with Multiple TINs (Implemented)

The bulk upload feature already supports multiple TINs:

```csv
practice_tin,claim_number,first_name,last_name,date_of_birth,subscriber_id
854203105,2024010001,John,Smith,1980-01-15,12345678
854203105,2024010002,Jane,Doe,1975-06-20,87654321
260167522,2024020001,Bob,Johnson,1990-03-10,11223344
260167522,2024020002,Alice,Williams,1985-12-05,99887766
```

**Location:** `connectme-backend/apps/claims/tasks.py` (lines 461-536)

The system:
1. Groups claims by TIN
2. Makes one API call per TIN
3. Processes all claims
4. Returns results with status information

### Approach 3: Custom API Endpoint (Recommended)

Create a new endpoint that handles multi-TIN, status-filtered queries:

```python
# New endpoint: /api/v1/claims/search-by-status/

@api_view(['POST'])
def search_claims_by_status(request):
    """
    Search claims by status across multiple TINs
    
    POST /api/v1/claims/search-by-status/
    {
        "tins": ["854203105", "260167522"],
        "statuses": ["PAID", "PENDING"],
        "first_service_date": "2024-01-01",
        "last_service_date": "2024-01-31"
    }
    """
    tins = request.data.get('tins', [])
    statuses = request.data.get('statuses', [])
    first_date = request.data.get('first_service_date')
    last_date = request.data.get('last_service_date')
    
    results = []
    
    for tin in tins:
        # Get practice for this TIN
        practice = Practice.objects.get(tin=tin)
        
        # Query UHC
        claims = query_uhc_for_practice(practice, first_date, last_date)
        
        # Filter by status
        filtered_claims = [
            claim for claim in claims 
            if claim.get('claimStatus') in statuses
        ]
        
        results.extend(filtered_claims)
    
    return Response({
        'total_claims': len(results),
        'claims': results,
        'grouped_by_status': group_by_status(results)
    })
```

---

## 📋 Common Claim Statuses

Based on UHC API responses:

| Status | Description |
|--------|-------------|
| `PAID` | Claim has been paid |
| `PENDING` | Claim is being processed |
| `DENIED` | Claim was denied |
| `PARTIAL` | Partially paid |
| `REJECTED` | Claim was rejected |
| `APPEALED` | Claim is under appeal |
| `RESUBMITTED` | Claim was resubmitted |

---

## 🚀 Recommended Implementation

### Option 1: Use Existing Bulk Upload (Quick Solution)

1. **Create CSV with multiple TINs:**
   ```csv
   practice_tin,claim_number,first_name,last_name,date_of_birth
   854203105,2024010001,John,Smith,1980-01-15
   260167522,2024020001,Bob,Johnson,1990-03-10
   ```

2. **Upload via bulk upload page**
   - System automatically groups by TIN
   - Makes optimized API calls
   - Returns results with status

3. **Filter results by status in UI:**
   - Results show claim status
   - Use frontend filtering to show only desired statuses

### Option 2: Create Custom Report Endpoint (Better Solution)

1. **Create new API endpoint:**
   - `/api/v1/reports/claims-by-status/`
   - Accepts multiple TINs and statuses
   - Returns aggregated results

2. **Add to frontend:**
   - New "Status Report" page
   - Multi-select for TINs
   - Multi-select for statuses
   - Date range picker
   - Export to CSV

3. **Implementation:**
   ```python
   # connectme-backend/apps/claims/report_views.py
   
   @api_view(['POST'])
   @permission_classes([IsAuthenticated])
   def claims_status_report(request):
       """
       Generate claims status report for multiple TINs
       """
       tins = request.data.get('tins', [])
       statuses = request.data.get('statuses', [])
       start_date = request.data.get('start_date')
       end_date = request.data.get('end_date')
       
       # Validate inputs
       if not tins or not start_date or not end_date:
           return Response({'error': 'Missing required fields'}, 
                         status=400)
       
       results = []
       
       for tin in tins:
           try:
               practice = Practice.objects.get(tin=tin)
               payer_mapping = PracticePayerMapping.objects.get(
                   practice=practice,
                   provider__name='UHC',
                   is_active=True
               )
               credential = payer_mapping.provider.credentials.first()
               
               # Query UHC
               claims = batch_query_claims(
                   practice, payer_mapping, credential,
                   start_date, end_date
               )
               
               # Filter by status
               for claim_number, claim_data in claims.items():
                   claim_status = claim_data.get('claimStatus', '')
                   
                   if not statuses or claim_status in statuses:
                       results.append({
                           'tin': tin,
                           'practice_name': practice.name,
                           'claim_number': claim_number,
                           'status': claim_status,
                           'charged_amount': claim_data.get('claimSummary', {}).get('totalChargedAmt'),
                           'paid_amount': claim_data.get('claimSummary', {}).get('totalPaidAmt'),
                           'processed_date': claim_data.get('claimSummary', {}).get('processedDt'),
                       })
           
           except Exception as e:
               logger.error(f"Error processing TIN {tin}: {e}")
               continue
       
       # Group results by status
       grouped = {}
       for result in results:
           status = result['status']
           if status not in grouped:
               grouped[status] = []
           grouped[status].append(result)
       
       return Response({
           'total_claims': len(results),
           'claims': results,
           'grouped_by_status': grouped,
           'summary': {
               status: len(claims) 
               for status, claims in grouped.items()
           }
       })
   ```

---

## 📊 Example Use Cases

### Use Case 1: Find All PAID Claims for Multiple Practices

```bash
POST /api/v1/reports/claims-by-status/
{
  "tins": ["854203105", "260167522", "123456789"],
  "statuses": ["PAID"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

**Response:**
```json
{
  "total_claims": 45,
  "summary": {
    "PAID": 45
  },
  "claims": [
    {
      "tin": "854203105",
      "practice_name": "ABC Medical",
      "claim_number": "2024010001",
      "status": "PAID",
      "charged_amount": "1500.00",
      "paid_amount": "1200.00",
      "processed_date": "01/15/2024"
    },
    // ... more claims
  ]
}
```

### Use Case 2: Find All PENDING and DENIED Claims

```bash
POST /api/v1/reports/claims-by-status/
{
  "tins": ["854203105"],
  "statuses": ["PENDING", "DENIED"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

---

## ⚠️ Limitations & Considerations

### API Rate Limits
- UHC API has rate limits (typically 100 requests/minute)
- For many TINs, implement rate limiting and queuing

### Performance
- Each TIN requires a separate API call
- 10 TINs = 10 API calls (can take 10-30 seconds)
- Consider caching results

### Data Freshness
- UHC data updates daily
- No real-time status updates
- Cache results for 24 hours

---

## 🎯 Summary

**Can you filter claims by status for different TINs?**

✅ **YES**, but requires:
1. **Multiple API calls** - One per TIN (UHC limitation)
2. **Client-side filtering** - Filter by status after retrieval
3. **Custom implementation** - Not built-in to UHC API

**Best Approach:**
- Use bulk upload for ad-hoc queries
- Create custom report endpoint for regular reporting
- Implement caching for frequently accessed data

---

## 📚 Related Documentation

- [Bulk Upload Guide](help/user/bulk-upload.html)
- [Claims Search Guide](help/user/claims-search.html)
- [API Reference](help/developer/api-reference.html)
- [Practice Management](PRACTICE_API_SUMMARY.md)

---

**Need Help?**
- Email: support@totessoft.com
- Documentation: [Help Portal](help/index.html)

