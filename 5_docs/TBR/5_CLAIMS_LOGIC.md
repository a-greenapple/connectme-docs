# 5. Claims Logic Documentation

## Overview
This document explains the claims processing logic, reconciliation system, and payment workflow in the ConnectMe healthcare platform.

## Table of Contents
1. [UHC API Integration](#uhc-api-integration)
2. [Claims Processing Workflow](#claims-processing-workflow)
3. [Payment Reconciliation](#payment-reconciliation)
4. [Frontend Display Logic](#frontend-display-logic)
5. [Data Mapping](#data-mapping)
6. [Error Handling](#error-handling)

## UHC API Integration

### Three-API Workflow
The system integrates three UHC APIs in sequence:

1. **Claims Summary API** - Gets basic claim information
2. **Claims Details API** - Retrieves detailed line items
3. **Payment Status API** - Fetches payment information

### API Orchestration
```python
# Backend workflow in api_views.py
def search_claims(request):
    # 1. Call Claims Summary API
    summary_response = uhc_client.get_claims_summary(params)
    
    # 2. Extract transaction_id from summary
    transaction_id = summary_response.get('transactionId')
    
    # 3. Call Claims Details API
    details_response = uhc_client.get_claims_details(transaction_id)
    
    # 4. Call Payment Status API
    payment_response = uhc_client.get_payment_status(transaction_id)
    
    # 5. Combine all data
    return enriched_claim_data
```

## Claims Processing Workflow

### Data Enrichment Process
1. **Summary Data**: Basic claim information (status, amounts, dates)
2. **Details Data**: Line items with service codes and amounts
3. **Payment Data**: Check numbers, draft amounts, payment dates
4. **Reconciliation**: Cross-reference line items with payments

### Key Data Fields
- `totalChargedAmt`: Amount provider charged
- `totalAllowdAmt`: Amount insurance allowed
- `totalPaidAmt`: Amount insurance paid
- `totalPtntRespAmt`: Patient responsibility
- `clmXWalkData`: ICN suffix to draft number mapping

## Payment Reconciliation

### ICN Suffix Mapping
The reconciliation system uses ICN suffixes to map line items to payment drafts:

```javascript
// Frontend reconciliation logic
const suffixToDraftMap = new Map();
claim.claimSummary.clmXWalkData.forEach((xwalk) => {
  const suffix = xwalk.clmIcnSufxCd;
  const draftNbr = xwalk.clmDrftNbr;
  suffixToDraftMap.set(suffix, draftNbr);
});
```

### Line Item Grouping
Line items are grouped by ICN suffix:
```javascript
const suffixTotals = new Map();
claim.lineItems.forEach((line) => {
  const suffix = line.icnSuffix;
  const currentTotal = suffixTotals.get(suffix) || 0;
  suffixTotals.set(suffix, currentTotal + parseFloat(line.paidAmt));
});
```

### Reconciliation Validation
```javascript
// Compare line totals with draft amounts
suffixToDraftMap.forEach((draftNbr, suffix) => {
  const lineTotal = suffixTotals.get(suffix) || 0;
  const draftPayment = claim.payments.find(p => p.draftNbr === draftNbr);
  const draftAmount = draftPayment ? parseFloat(draftPayment.draftAmt) : 0;
  
  const matches = Math.abs(lineTotal - draftAmount) < 0.01;
  // Display ✅ or ❌ based on match
});
```

## Frontend Display Logic

### Side-by-Side Layout
- **Left Column**: Line Items with ICN suffix chips
- **Right Column**: Payment Records with draft information
- **Bottom Section**: Reconciliation table and JSON viewer

### Responsive Design
```css
/* Grid layout for side-by-side display */
.grid-cols-1.xl:grid-cols-2 {
  /* Single column on mobile/tablet */
  /* Two columns on desktop (≥1280px) */
}
```

### Visual Indicators
- **Green**: Patient balance = $0.00 (good news)
- **Red**: Patient balance > $0.00 (attention needed)
- **Purple**: ICN suffix chips for easy identification
- **Blue**: Paid amounts from insurance
- **Yellow**: Warning indicators and badges

## Data Mapping

### Claim Summary → Details → Payment
```python
# Backend data flow
claim_data = {
    'summary': summary_response,
    'details': details_response,
    'payments': payment_response,
    'reconciliation': {
        'suffix_mapping': clmXWalkData,
        'line_totals': calculated_totals,
        'draft_amounts': payment_drafts
    }
}
```

### Frontend Data Structure
```typescript
interface Claim {
  id: string;
  claimNumber: string;
  status: string;
  chargedAmount: string;
  allowedAmount: string;  // Key for payment breakdown
  paidAmount: string;
  patientBalance: string;
  lineItems: LineItem[];
  payments: Payment[];
  remarks: Remark[];
  carcCodes: CARCCode[];
  claimSummary: ClaimSummary;
}
```

## Error Handling

### API Error Processing
```python
# Backend error handling
if uhc_response.status_code != 200:
    try:
        error_data = uhc_response.json()
        if 'errors' in error_data:
            error_message = error_data['errors'][0].get('message', 'Unknown error')
            error_code = error_data['errors'][0].get('code', '')
            return f"[{error_code}] {error_message}"
    except:
        return uhc_response.text
```

### Frontend Error Display
- **Date Range Validation**: Max 90 days without patient filter
- **SSL Certificate Issues**: Bypassed in development mode
- **Hydration Mismatches**: Suppressed for browser extensions
- **Modal Rendering**: Uses React Portal for proper z-index

### Common Error Scenarios
1. **Date Range Too Large**: "First Service Date and Last Service Date should be within last 24 months"
2. **Invalid TIN**: Provider not found or unauthorized
3. **Transaction Timeout**: 24-hour limit on transaction_id validity
4. **Network Issues**: SSL handshake failures, connection timeouts

## Performance Considerations

### Caching Strategy
- **Backend**: Redis cache for API responses
- **Frontend**: Local storage for query history
- **Session**: JWT token caching

### Optimization Techniques
- **Parallel API Calls**: Details and Payment APIs called simultaneously
- **Lazy Loading**: Expanded details loaded on demand
- **Virtual Scrolling**: For large claim lists
- **Debounced Search**: Prevents excessive API calls

## Security Measures

### Data Protection
- **Field-level Encryption**: Sensitive data encrypted with Fernet
- **Audit Logging**: All API calls logged with timestamps
- **Access Control**: Role-based permissions via Keycloak
- **SSL/TLS**: All communications encrypted in transit

### HIPAA Compliance
- **Data Minimization**: Only necessary fields displayed
- **Access Logging**: User actions tracked and logged
- **Data Retention**: Configurable retention policies
- **Incident Response**: Automated alerting for security events

## Testing Scenarios

### Test Claims
- **ZE59426195**: Complex claim with multiple line items and payments
- **FF29426185**: Single payment with reconciliation testing
- **Various Statuses**: Pending, finalized, denied claims

### Validation Checks
1. **Amount Totals**: Charged = Paid + Patient + Adjustments
2. **Suffix Mapping**: All ICN suffixes have corresponding drafts
3. **Date Ranges**: Within 24-month API limit
4. **Status Consistency**: Summary and details status match

## Troubleshooting Guide

### Common Issues
1. **"Failed to retrieve claims"**: Check date range and TIN
2. **Empty payment details**: Verify transaction_id validity
3. **Reconciliation mismatches**: Check ICN suffix mapping
4. **Display errors**: Verify data structure and types

### Debug Tools
- **JSON Viewer**: Raw API responses for debugging
- **Console Logging**: Detailed error messages
- **Network Tab**: API call monitoring
- **React DevTools**: Component state inspection

## Future Enhancements

### Planned Features
1. **Remittance Integration**: 835 EDI file processing
2. **Bulk Operations**: CSV upload for multiple claims
3. **Advanced Filtering**: Date ranges, status filters
4. **Export Options**: PDF reports, Excel exports
5. **Real-time Updates**: WebSocket notifications

### API Improvements
1. **Caching Layer**: Redis for improved performance
2. **Rate Limiting**: Prevent API abuse
3. **Retry Logic**: Automatic retry for failed requests
4. **Circuit Breaker**: Prevent cascade failures

---

*This document is part of the ConnectMe healthcare platform documentation system. For updates and questions, refer to the main project documentation.*
