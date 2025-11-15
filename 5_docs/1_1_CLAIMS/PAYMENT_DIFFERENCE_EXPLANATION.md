# Understanding Payment Differences: Charged vs Paid

## The Question
**"CHARGED $565.00 → Paid $260.82"**

Why is there a $304.18 difference?

## Available Data in UHC API

Based on the UHC Claims API, we have access to the following fields that explain payment differences:

### 1. **Claim Codes** (Most Important!)
The API provides `claimCodes` array with different types:

#### **CARC (Claim Adjustment Reason Codes)**
- Standard industry codes explaining WHY adjustments were made
- Example: Code "45" = "CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE OR CONTRACTED/LEGISLATED FEE ARRANGEMENT"
- These are the PRIMARY reason for payment differences

#### **REMARK Codes**
- Additional explanations and context
- Example: "YL" = "Benefits based on provider's contracted rate... Patient not responsible for difference..."

#### **PEND Codes**
- Pending reasons
- Example: "2T" = "PROCESSED ACCORDING TO SUBROGATION"

#### **CHEC Codes**
- Check-level messages
- Example: "CAD805" = "INTEREST HAS BEEN APPLIED TO THIS CLAIM"

### 2. **Financial Breakdown Fields**

From the API response, we have:

```javascript
{
  "totalChargedAmt": "565.00",      // What provider billed
  "totalAllowdAmt": "260.82",       // Contracted/allowed amount
  "totalPaidAmt": "260.82",         // What insurance paid
  "totalPtntRespAmt": "0.00",       // Patient responsibility
  "deductibleAmt": "0.00",          // Deductible applied
  "totalCopayAmt": "0.00",          // Copay amount
  "totalCoinsAmt": "0.00",          // Coinsurance amount
}
```

### 3. **Line-Level Details**

Each service line has:
```javascript
{
  "billedAmt": "565.00",            // Line billed amount
  "allowdAmt": "260.82",            // Line allowed amount
  "paidAmt": "260.82",              // Line paid amount
  "totalMemResp": "0.00",           // Patient responsibility
  "claimCodes": [...]               // Line-level adjustment codes
}
```

## Common Reasons for Payment Differences

### 1. **Contractual Adjustment** (Most Common)
- **Code**: CARC 45
- **Reason**: Provider's charge exceeds contracted rate
- **Example**: Provider bills $565, contract allows $260.82
- **Patient Impact**: NOT responsible for $304.18 difference
- **Formula**: `Charged - Allowed = Contractual Adjustment`

### 2. **Deductible**
- Patient hasn't met annual deductible
- Insurance doesn't pay until deductible is met
- **Patient IS responsible** for this amount

### 3. **Copay**
- Fixed amount patient pays per visit/service
- **Patient IS responsible** for this amount

### 4. **Coinsurance**
- Percentage of allowed amount patient pays
- Example: 20% coinsurance on $260.82 = $52.16
- **Patient IS responsible** for this amount

### 5. **Non-Covered Services**
- Service not covered by insurance plan
- **Patient IS responsible** for full amount

### 6. **Coordination of Benefits (COB)**
- Other insurance pays first
- UHC pays secondary amount

## What We Can Display

### Option 1: Simple Breakdown (Recommended)
```
┌─────────────────────────────────────────────────────┐
│ Financial Summary                                   │
├─────────────────────────────────────────────────────┤
│ Charged:              $565.00                       │
│ Allowed:              $260.82                       │
│ ─────────────────────────────────                  │
│ Contractual Adj:     -$304.18  ℹ️                   │
│ ─────────────────────────────────                  │
│ Insurance Paid:       $260.82                       │
│ Patient Balance:        $0.00  ✅                   │
└─────────────────────────────────────────────────────┘

ℹ️ Contractual Adjustment: Provider's contracted rate
   with insurance. You are NOT responsible for this.
```

### Option 2: Detailed with Codes
```
┌─────────────────────────────────────────────────────┐
│ Payment Breakdown                                   │
├─────────────────────────────────────────────────────┤
│ Provider Charged:     $565.00                       │
│ Insurance Allowed:    $260.82                       │
│                                                     │
│ Adjustments:                                        │
│ ├─ Contractual:      -$304.18                      │
│ │  └─ CARC 45: Charge exceeds contracted rate     │
│ ├─ Deductible:          $0.00                      │
│ ├─ Copay:               $0.00                      │
│ └─ Coinsurance:         $0.00                      │
│                                                     │
│ Insurance Paid:       $260.82  ✅                   │
│ Patient Owes:           $0.00  ✅                   │
└─────────────────────────────────────────────────────┘

📋 Claim Codes:
  • CARC 45: Charge exceeds fee schedule
  • REMARK YL: Benefits based on contracted rate
```

### Option 3: Visual Progress Bar
```
┌─────────────────────────────────────────────────────┐
│ $565.00 Charged                                     │
│ ████████████████████████████████████████████░░░░░░░ │
│ ↓                                                   │
│ $260.82 Allowed (46% of charged)                   │
│ ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ↓                                                   │
│ $260.82 Paid by Insurance                          │
│ ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ↓                                                   │
│ $0.00 Patient Balance ✅                            │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│                                                     │
│ Why the difference?                                 │
│ • Contractual Adjustment: $304.18                  │
│   (Provider's contracted rate with UHC)            │
│   You are NOT responsible for this amount          │
└─────────────────────────────────────────────────────┘
```

## Recommended Implementation

### Step 1: Add "Allowed Amount" to Display
Currently showing:
- Charged: $565.00
- Paid: $260.82

Should show:
- Charged: $565.00
- **Allowed: $260.82** ← NEW
- Insurance Paid: $260.82
- Patient Balance: $0.00

### Step 2: Calculate and Show Adjustments
```javascript
const contractualAdjustment = chargedAmount - allowedAmount;
const patientResponsibility = deductible + copay + coinsurance;
```

### Step 3: Display Claim Codes
- Parse `claimCodes` array
- Group by type (CARC, REMARK, etc.)
- Show with descriptions
- Highlight CARC codes (most important)

### Step 4: Add Tooltips/Explanations
- Hover over "Contractual Adjustment" → Show explanation
- Hover over CARC code → Show full description
- Link to "Why is my payment different?" help article

## Data We Already Have

✅ `totalChargedAmt` (Charged)
✅ `totalAllowdAmt` (Allowed) ← KEY FIELD!
✅ `totalPaidAmt` (Paid)
✅ `totalPtntRespAmt` (Patient Balance)
✅ `deductibleAmt` (Deductible)
✅ `totalCopayAmt` (Copay)
✅ `totalCoinsAmt` (Coinsurance)
✅ `claimCodes` array (CARC, REMARK, etc.)

## What We Need to Do

1. **Extract `totalAllowdAmt` from API response**
   - Currently not being sent to frontend
   - This is the KEY to explaining the difference

2. **Parse and display claim codes**
   - Already extracting REMARK codes
   - Need to also show CARC codes (adjustment reasons)

3. **Calculate adjustments**
   - Contractual: `charged - allowed`
   - Patient responsibility: `deductible + copay + coinsurance`

4. **Add visual breakdown section**
   - Show the flow: Charged → Allowed → Paid → Patient Balance
   - Explain each step

## Example Real Data

From your claim:
```javascript
{
  "totalChargedAmt": "565.00",
  "totalAllowdAmt": "260.82",      // ← We need this!
  "totalPaidAmt": "260.82",
  "totalPtntRespAmt": "0.00",
  "claimCodes": [
    {
      "type": "CARC",
      "code": "45",
      "description": "CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE OR CONTRACTED /LEGISLATED FEE ARRANGEMENT."
    },
    {
      "type": "REMARK",
      "code": "YL",
      "description": "Benefits for this claim are based on the provider's contracted rate... Patient is not responsible for the difference..."
    }
  ]
}
```

**Explanation**:
- Provider charged $565.00
- Insurance contract allows $260.82 (46% of charged)
- **Contractual adjustment: $304.18** (provider writes this off)
- Insurance paid the full allowed amount: $260.82
- Patient owes: $0.00
- **CARC 45** explains why: charge exceeds contracted rate
- **REMARK YL** confirms: patient not responsible for difference

## Next Steps

Would you like me to:

1. ✅ **Add "Allowed Amount" field** to the display?
2. ✅ **Show contractual adjustment** calculation?
3. ✅ **Display CARC codes** prominently (not just REMARK)?
4. ✅ **Add visual breakdown** section?
5. ✅ **Add tooltips** explaining each field?

All the data is already available in the API response - we just need to extract and display it properly!

