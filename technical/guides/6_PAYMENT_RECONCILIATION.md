# Payment Reconciliation System

## Overview

The Payment Reconciliation system provides a comprehensive view of how claim line items match up with payment drafts using UHC's ICN (Internal Control Number) suffix mapping system.

## Architecture

### Data Flow

```
Claim Summary API (clmXWalkData)
    ↓
ICN Suffix → Draft Number Mapping
    ↓
Line Items (by ICN suffix) ⟷ Payment Drafts
    ↓
Reconciliation Validation
```

### Key Components

1. **PaymentReconciliation Component** (`/frontend/src/components/claims/PaymentReconciliation.tsx`)
   - Main reconciliation UI
   - Side-by-side view of line items and payments
   - Drag-and-drop manual reconciliation
   - Global tally verification

2. **ClaimTreeView Integration** (`/frontend/src/components/claims/ClaimTreeView.tsx`)
   - Tree navigation for reconciliation section
   - Tab-based interface for quick access

## Data Structures

### ICN Suffix Mapping

UHC provides crosswalk data in the claim summary response:

```json
{
  "clmXWalkData": [
    {
      "clmIcnSufxCd": "01",
      "clmDrftNbr": "0104448309"
    },
    {
      "clmIcnSufxCd": "02",
      "clmDrftNbr": "0204448310"
    }
  ]
}
```

### Line Items Structure

Each line item includes:
- `icnSuffix`: Links to payment draft via crosswalk data
- `paidAmt`: Amount paid for this line item
- `srvcCode`/`procedureCd`: Service code
- `lineNbr`: Line item number
- `firstSrvcDt`: Service date

### Payment Structure

Each payment draft includes:
- `draftNbr`: Matches ICN suffix via crosswalk
- `draftAmt`: Amount paid in this draft
- `checkNbr`: Check number (multiple drafts can share one check)
- `paymentIssueDt`: Payment date

## Reconciliation Logic

### 1. Build Suffix-to-Draft Mapping

```typescript
const buildSuffixToDraftMap = () => {
  const map = new Map<string, string>();
  if (claim.claimSummary?.clmXWalkData) {
    claim.claimSummary.clmXWalkData.forEach((xwalk: any) => {
      const suffix = xwalk.clmIcnSufxCd;
      const draftNbr = xwalk.clmDrftNbr;
      if (suffix && draftNbr) {
        map.set(suffix, draftNbr);
      }
    });
  }
  return map;
};
```

### 2. Group Line Items by ICN Suffix

Line items are grouped by their ICN suffix, and the paid amounts are summed:

```typescript
const lineItemsBySuffix = new Map<string, any[]>();

claim.lineItems?.forEach((line: any) => {
  const suffix = line.icnSuffix || 'UNMAPPED';
  if (!lineItemsBySuffix.has(suffix)) {
    lineItemsBySuffix.set(suffix, []);
  }
  lineItemsBySuffix.get(suffix)?.push(line);
});
```

### 3. Match with Payment Drafts

For each ICN suffix:
- Find the corresponding draft number from crosswalk data
- Locate the payment draft with that draft number
- Sum all line items with that ICN suffix
- Compare sum with draft amount

```typescript
const lineItemsSum = lines.reduce((sum, line) => 
  sum + parseFloat(String(line.paidAmt || '0')), 0
);
const draftNbr = suffixToDraftMap.get(suffix);
const payment = claim.payments?.find((p: any) => p.draftNbr === draftNbr);
const draftAmount = parseFloat(String(payment?.draftAmt || '0'));
const matches = Math.abs(lineItemsSum - draftAmount) < 0.001; // Exact match
```

### 4. Global Tally Verification

Three values must match exactly:
1. Sum of all line item `paidAmt` values
2. Sum of all payment `draftAmt` values  
3. `totalPaidAmt` from claim summary

```typescript
const totalLineItemsSum = items.reduce((sum, item) => sum + item.lineItemsSum, 0);
const totalDraftSum = claim.payments?.reduce((sum: number, p: any) => 
  sum + parseFloat(String(p.draftAmt || '0')), 0
) || 0;
const totalPaidFromSummary = parseFloat(claim.claimSummary?.totalPaidAmt || '0');

const globalMatch = Math.abs(totalLineItemsSum - totalDraftSum) < 0.001 && 
                   Math.abs(totalLineItemsSum - totalPaidFromSummary) < 0.001;
```

## UI Features

### Global Tally Banner

Displays at the top of the reconciliation view:
- ✅ Green border if all amounts match
- ❌ Red border if there are discrepancies
- Shows three key totals: Line Items, Drafts, Summary
- Warns if any line items are unmapped

### Reconciliation Proof Table

Toggleable detailed view showing:
- ICN Suffix
- Draft Number
- Line Items Sum
- Draft Amount
- Status (✅/❌)
- Difference

### Side-by-Side View

**Left Panel: Line Items**
- Draggable cards for each line item
- Shows service code, ICN suffix, and paid amount
- Blue highlight on hover
- Cursor indicates draggable

**Right Panel: Payment Drafts**
- Grouped by check number
- Expandable to show individual drafts
- Draggable cards for each draft
- Green highlight on hover
- Shows multi-claim warning if check total exceeds draft total

### Multi-Claim Check Detection

When a check covers multiple claims:
```typescript
const checkTotal = payments.reduce((sum, p) => 
  sum + parseFloat(String(p.checkAmt || '0')), 0
);
const draftsTotal = payments.reduce((sum, p) => 
  sum + parseFloat(String(p.draftAmt || '0')), 0
);
const isMultiClaim = Math.abs(checkTotal - draftsTotal) > 0.01;
```

If detected:
- Yellow "Multi-Claim" badge
- Expandable view shows excess amount
- Explanation that check may cover other claims

### Drag-and-Drop Manual Reconciliation

Users can manually map line items to payment drafts:
1. Drag a line item from the left panel
2. Drop it on a payment draft in the right panel
3. System logs the manual mapping for future reference

```typescript
const handleDrop = (e: React.DragEvent, targetType: 'line' | 'payment', targetData: any) => {
  e.preventDefault();
  if (draggedItem) {
    console.log('Manual reconciliation:', { 
      from: draggedItem, 
      to: { type: targetType, data: targetData } 
    });
    // TODO: Save to backend for future queries
  }
};
```

## Provider Remittance Advice (PRA)

### 835 Remittance Files

UHC provides electronic remittance advice (835 files) that contain:
- Complete payment details
- All claims covered by a check
- Adjustment codes and reasons
- Provider-level summaries

### Integration

If available, a "View Remittance (PRA)" button appears in the reconciliation UI:

```typescript
{claim.remittanceUrl && (
  <a
    href={claim.remittanceUrl}
    target="_blank"
    rel="noopener noreferrer"
    className="inline-flex items-center px-4 py-2..."
  >
    <svg>...</svg>
    View Remittance (PRA)
  </a>
)}
```

The remittance document opens in a new tab for reference.

## Edge Cases

### 1. Unmapped Line Items

**Scenario**: Line item has no ICN suffix or suffix not in crosswalk data

**Handling**:
- Grouped under "UNMAPPED" category
- Shown in reconciliation table with ❌ status
- Warning displayed in global tally banner
- Can be manually mapped via drag-and-drop

### 2. Multi-Claim Checks

**Scenario**: Single check covers multiple claims

**Handling**:
- Check total > draft total for this claim
- Yellow "Multi-Claim" badge
- Expandable details show excess amount
- Explanation tooltip
- Link to remittance for full details

### 3. Rounding Differences

**Scenario**: Minor floating-point differences

**Handling**:
- Tolerance of ±$0.001 for matching
- Exact amounts still displayed to 2 decimal places
- Difference column shows absolute value

### 4. Missing Crosswalk Data

**Scenario**: Claim response lacks `clmXWalkData`

**Handling**:
- All line items marked as "UNMAPPED"
- Warning banner: "Tally unavailable - missing crosswalk data"
- Manual reconciliation still available via drag-and-drop

### 5. Partial Payments

**Scenario**: Not all line items have been paid yet

**Handling**:
- Line items with $0.00 paid amount shown separately
- Global tally reflects only paid amounts
- Status shows as incomplete until fully reconciled

## Testing Scenarios

### Test Case 1: Perfect Match
```json
{
  "lineItems": [
    { "icnSuffix": "01", "paidAmt": "100.00" },
    { "icnSuffix": "02", "paidAmt": "50.00" }
  ],
  "payments": [
    { "draftNbr": "001", "draftAmt": "100.00" },
    { "draftNbr": "002", "draftAmt": "50.00" }
  ],
  "clmXWalkData": [
    { "clmIcnSufxCd": "01", "clmDrftNbr": "001" },
    { "clmIcnSufxCd": "02", "clmDrftNbr": "002" }
  ],
  "totalPaidAmt": "150.00"
}
```
**Expected**: ✅ All tallies match

### Test Case 2: Mismatch
```json
{
  "lineItems": [
    { "icnSuffix": "01", "paidAmt": "100.00" }
  ],
  "payments": [
    { "draftNbr": "001", "draftAmt": "95.00" }
  ],
  "clmXWalkData": [
    { "clmIcnSufxCd": "01", "clmDrftNbr": "001" }
  ],
  "totalPaidAmt": "95.00"
}
```
**Expected**: ❌ Line item sum ($100) ≠ draft amount ($95)

### Test Case 3: Multi-Claim Check
```json
{
  "payments": [
    { 
      "checkNbr": "12345", 
      "checkAmt": "500.00",
      "draftNbr": "001", 
      "draftAmt": "150.00" 
    }
  ]
}
```
**Expected**: Yellow "Multi-Claim" badge, excess $350.00 shown

### Test Case 4: Unmapped Line Items
```json
{
  "lineItems": [
    { "icnSuffix": null, "paidAmt": "100.00" }
  ],
  "clmXWalkData": []
}
```
**Expected**: Line item shown as "UNMAPPED", warning in banner

## Future Enhancements

### 1. Transaction History Caching

Store claim queries in the database for 24 hours:

```python
# backend/apps/claims/models.py
class ClaimQuery(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    tin = models.CharField(max_length=20)
    first_service_date = models.DateField()
    last_service_date = models.DateField()
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['expires_at']),
        ]
```

**Benefits**:
- Avoid re-querying UHC for same data
- Support pagination without re-authentication
- Enable audit trail of queries

### 2. Manual Reconciliation Persistence

Save user's manual mappings:

```python
class ManualReconciliation(models.Model):
    claim_number = models.CharField(max_length=50)
    line_item_number = models.IntegerField()
    draft_number = models.CharField(max_length=20)
    mapped_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

**Benefits**:
- Preserve institutional knowledge
- Audit trail of manual interventions
- Train ML models for auto-mapping

### 3. 835 Remittance Parser

Parse and store 835 EDI files:

```python
from edi835parser import parse_835

class RemittanceFile(models.Model):
    check_number = models.CharField(max_length=50)
    file_path = models.FileField(upload_to='remittances/')
    parsed_data = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**Benefits**:
- Automatic cross-validation
- Enhanced multi-claim check handling
- Historical payment analysis

### 4. Reconciliation Analytics

Dashboard showing:
- Average reconciliation success rate
- Common unmapped scenarios
- Processing time metrics
- Multi-claim check frequency

### 5. Smart Matching Suggestions

ML-powered suggestions for unmapped line items:
- Pattern recognition from historical data
- Similarity matching based on amounts
- Provider-specific mapping rules

## Security Considerations

### PHI Protection

Reconciliation data contains:
- Patient service dates
- Payment amounts
- Provider information

**Safeguards**:
- All data encrypted in transit (SSL/TLS)
- Encrypted at rest in database
- Audit logging of all access
- HIPAA-compliant data retention policies

### Access Control

Reconciliation features require:
- `claims:read` permission for viewing
- `claims:detail` permission for detailed reconciliation
- `claims:export` permission for downloading proof tables

### Audit Trail

Log all reconciliation activities:
```python
audit_log.objects.create(
    user=request.user,
    action='view_reconciliation',
    claim_number=claim.claimNumber,
    details={
        'matched': reconciliation.globalMatch,
        'total_amount': reconciliation.totalLineItemsSum
    }
)
```

## Troubleshooting

### Issue: All Line Items Show as UNMAPPED

**Possible Causes**:
1. Missing `clmXWalkData` in API response
2. ICN suffix field empty on line items
3. Crosswalk data uses different field names

**Resolution**:
1. Check API response for `clmXWalkData` array
2. Verify line items have `icnSuffix` populated
3. Use drag-and-drop for manual mapping
4. Contact UHC support if crosswalk data consistently missing

### Issue: Global Tally Doesn't Match

**Possible Causes**:
1. Rounding differences beyond tolerance
2. Partial payment (not all line items paid)
3. Adjustment applied at claim level

**Resolution**:
1. Check "Show Proof" table for per-draft details
2. Review CARC codes in Financial Breakdown
3. Compare with remittance advice (835)
4. Verify `totalPaidAmt` from claim summary

### Issue: Multi-Claim Check Confusion

**Possible Causes**:
1. Check covers multiple claims from multiple providers
2. Draft amounts don't equal check total

**Resolution**:
1. View remittance advice to see all claims
2. Check total is informational only
3. Focus on draft amounts for this claim's reconciliation

## API Reference

### Frontend Component Props

```typescript
interface PaymentReconciliationProps {
  claim: Claim;  // Full claim object with lineItems, payments, claimSummary
}
```

### Claim Object Structure

```typescript
interface Claim {
  // ... other fields ...
  lineItems?: Array<{
    icnSuffix: string;
    paidAmt: string;
    srvcCode?: string;
    procedureCd?: string;
    lineNbr: number;
    firstSrvcDt: string;
  }>;
  payments?: Array<{
    draftNbr: string;
    draftAmt: string;
    checkNbr: string;
    checkAmt: string;
    paymentIssueDt: string;
  }>;
  claimSummary?: {
    totalPaidAmt: string;
    clmXWalkData: Array<{
      clmIcnSufxCd: string;
      clmDrftNbr: string;
    }>;
  };
  remittanceUrl?: string;
}
```

## Related Documentation

- [5_CLAIMS_LOGIC.md](./5_CLAIMS_LOGIC.md) - Overall claims processing workflow
- [4_EDGE_CASES.md](./4_EDGE_CASES.md) - Common error scenarios
- UHC API Documentation - Claims Summary, Details, Payment Status APIs

