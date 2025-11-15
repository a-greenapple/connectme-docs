# Line-Level Claim Codes Display

## Summary
Enhanced the Line Items table to display claim codes at the individual line level with expandable rows.

---

## What Was Added

### Expandable Line Items with Claim Codes

Each line item in the **Line Items** tab now:
1. ✅ Shows a **code count badge** if the line has claim codes
2. ✅ Has an **expand/collapse arrow** to view line-specific codes
3. ✅ Displays **color-coded claim codes** similar to the claim-level codes section

---

## Visual Changes

### Before
```
┌──────┬──────────────┬────────────┬─────────┬─────────┬──────────┬──────────────┐
│ Line │ Service Code │ Date       │ Billed  │ Allowed │ Paid     │ Patient Resp │
├──────┼──────────────┼────────────┼─────────┼─────────┼──────────┼──────────────┤
│ 1    │ 99213        │ 05/15/2025 │ $150.00 │ $120.00 │ $100.00  │ $20.00       │
│ 2    │ 99214        │ 05/15/2025 │ $200.00 │ $180.00 │ $150.00  │ $30.00       │
└──────┴──────────────┴────────────┴─────────┴─────────┴──────────┴──────────────┘
```

### After
```
┌───┬──────┬──────────────────────────┬────────────┬─────────┬─────────┬──────────┬──────────────┐
│   │ Line │ Service Code             │ Date       │ Billed  │ Allowed │ Paid     │ Patient Resp │
├───┼──────┼──────────────────────────┼────────────┼─────────┼─────────┼──────────┼──────────────┤
│ ▶ │ 1    │ 99213 [2 codes]          │ 05/15/2025 │ $150.00 │ $120.00 │ $100.00  │ $20.00       │
│   │      │       ↑ Blue badge       │            │         │         │          │              │
├───┼──────┼──────────────────────────┼────────────┼─────────┼─────────┼──────────┼──────────────┤
│ ▶ │ 2    │ 99214 [3 codes]          │ 05/15/2025 │ $200.00 │ $180.00 │ $150.00  │ $30.00       │
└───┴──────┴──────────────────────────┴────────────┴─────────┴─────────┴──────────┴──────────────┘
```

### Expanded View
```
┌───┬──────┬──────────────────────────┬────────────┬─────────┬─────────┬──────────┬──────────────┐
│   │ Line │ Service Code             │ Date       │ Billed  │ Allowed │ Paid     │ Patient Resp │
├───┼──────┼──────────────────────────┼────────────┼─────────┼─────────┼──────────┼──────────────┤
│ ▼ │ 1    │ 99213 [2 codes]          │ 05/15/2025 │ $150.00 │ $120.00 │ $100.00  │ $20.00       │
├───┴──────┴──────────────────────────┴────────────┴─────────┴─────────┴──────────┴──────────────┤
│   LINE 1 - CLAIM CODES (2)                                                                      │
│                                                                                                  │
│   💬 [045]  REMARK                                                                              │
│   ║         CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE                                       │
│   ↑ Blue background with blue left border                                                       │
│                                                                                                  │
│   ⚠️ [002]  CARC                                                                                │
│   ║         COINSURANCE AMOUNT                                                                  │
│   ↑ Orange background with orange left border                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Features

### 1. **Code Count Badge**
- Displayed next to the service code
- Blue badge with white text
- Shows count: "2 codes" or "1 code"
- Only appears if line has claim codes

### 2. **Expand/Collapse Arrow**
- Left-most column
- Click to toggle line codes display
- Right arrow (▶) when collapsed
- Down arrow (▼) when expanded
- Only appears if line has claim codes

### 3. **Color-Coded Line Codes**
Similar to claim-level codes, but organized per line:

#### **💬 REMARK (Blue)**
- Background: Light blue (`bg-blue-50`)
- Border: Blue left border (`border-blue-500`)
- Badge: Dark blue (`bg-blue-600`)
- Icon: 💬

#### **⚠️ CARC (Orange)**
- Background: Light orange (`bg-orange-50`)
- Border: Orange left border (`border-orange-500`)
- Badge: Dark orange (`bg-orange-600`)
- Icon: ⚠️

#### **🔍 RARC (Purple)**
- Background: Light purple (`bg-purple-50`)
- Border: Purple left border (`border-purple-500`)
- Badge: Dark purple (`bg-purple-600`)
- Icon: 🔍
- *RARC = Remittance Advice Remark Code*

#### **📌 OTHER (Gray)**
- Background: Light gray (`bg-gray-50`)
- Border: Gray left border (`border-gray-400`)
- Badge: Dark gray (`bg-gray-600`)
- Icon: 📌

---

## Code Structure

### Data Source
Line codes come from the UHC Details API:
```json
{
  "claimsDetailInfo": [
    {
      "lines": [
        {
          "lineNbr": "1",
          "srvcCode": "99213",
          "billedAmt": "150.00",
          "allowdAmt": "120.00",
          "paidAmt": "100.00",
          "lineCodes": [
            {
              "type": "REMARK",
              "code": "045",
              "description": "CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE"
            },
            {
              "type": "CARC",
              "code": "002",
              "description": "COINSURANCE AMOUNT"
            }
          ]
        }
      ]
    }
  ]
}
```

### Frontend Implementation
- **Component:** `LineItemsContent` in `ClaimTreeView.tsx`
- **State Management:** `useState<Set<number>>` for tracking expanded lines
- **Rendering:** Nested table rows with conditional rendering

---

## User Workflow

### Step 1: Navigate to Line Items
```
Expand Claim → Click "Line Items" tab
```

### Step 2: Identify Lines with Codes
```
Look for blue badge: "2 codes", "3 codes", etc.
```

### Step 3: Expand Line to View Codes
```
Click the ▶ arrow in the left column
```

### Step 4: Review Line-Specific Codes
```
See color-coded codes with:
- Code number in badge
- Code type (REMARK, CARC, RARC, etc.)
- Full description
```

### Step 5: Collapse When Done
```
Click the ▼ arrow to collapse
```

---

## Benefits

### 1. **Granular Code Visibility**
- See exactly which codes apply to which line items
- No need to guess which claim-level codes apply to which services

### 2. **Better Understanding of Adjustments**
- Understand why specific line items were adjusted
- See line-specific remarks and explanations

### 3. **Improved Reconciliation**
- Match line-level adjustments to specific codes
- Easier to explain to patients why amounts differ

### 4. **Consistent UI**
- Same color coding as claim-level codes
- Familiar interaction pattern (expand/collapse)
- Professional, clean design

---

## Technical Details

### Files Modified
- `connectme-frontend/src/components/claims/ClaimTreeView.tsx`
  - Added `expandedLines` state to `LineItemsContent`
  - Added `toggleLine` function
  - Enhanced table with expand/collapse column
  - Added code count badge display
  - Added expandable row for line codes
  - Added color-coded code rendering

### No Backend Changes Required
- Line codes already included in API response
- Data structure: `line.lineCodes[]`
- Each code has: `type`, `code`, `description`

---

## Code Types Supported

| Type   | Description                          | Color  | Icon |
|--------|--------------------------------------|--------|------|
| REMARK | Informational messages               | Blue   | 💬   |
| CARC   | Claim Adjustment Reason Code         | Orange | ⚠️   |
| RARC   | Remittance Advice Remark Code        | Purple | 🔍   |
| OTHER  | Any other code types                 | Gray   | 📌   |

---

## Example Use Cases

### Use Case 1: Understanding Line-Level Adjustments
**Scenario:** A line item was billed at $200 but allowed at $150.

**Solution:** Expand the line to see:
```
⚠️ [045] CARC
   CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE OR 
   CONTRACTED/LEGISLATED FEE ARRANGEMENT.
```

### Use Case 2: Patient Responsibility Explanation
**Scenario:** Patient owes $30 on a specific line.

**Solution:** Expand the line to see:
```
⚠️ [002] CARC
   COINSURANCE AMOUNT

💬 [0038] REMARK
   This claim was processed based on the allowed amount.
   Please do not bill the member any amount that is more
   than their cost share.
```

### Use Case 3: Multiple Lines with Different Codes
**Scenario:** Claim has 5 line items, each with different adjustments.

**Solution:** Each line shows its own code count badge. Expand only the lines you need to investigate.

---

## Performance Considerations

- **Lazy Rendering:** Only expanded lines render their codes
- **Efficient State:** Uses `Set<number>` for O(1) lookup
- **No API Calls:** All data already in claim response
- **Smooth Animations:** CSS transitions for expand/collapse

---

## Accessibility

- ✅ **Keyboard Navigation:** Arrow buttons are keyboard accessible
- ✅ **Screen Readers:** Proper semantic HTML and ARIA labels
- ✅ **Color + Text:** Not relying on color alone (includes icons and text)
- ✅ **Focus Management:** Clear focus states on interactive elements

---

## Browser Compatibility

Tested and working on:
- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Safari 17+
- ✅ Edge 120+

---

## Comparison: Claim-Level vs. Line-Level Codes

### Claim-Level Codes (Claim Codes Tab)
- **Location:** Dedicated "Claim Codes" tab
- **Scope:** Applies to the entire claim
- **Use Case:** Overall claim adjustments, general remarks
- **Example:** "Claim processed based on allowed amount"

### Line-Level Codes (Line Items Tab)
- **Location:** Expandable rows in "Line Items" tab
- **Scope:** Applies to specific service line
- **Use Case:** Line-specific adjustments, procedure-level remarks
- **Example:** "Charge exceeds fee schedule for CPT 99213"

---

## Future Enhancements (Potential)

1. **Expand All / Collapse All** buttons
2. **Filter lines by code type** (show only lines with CARC codes)
3. **Export line codes to CSV**
4. **Search/filter codes** within expanded lines
5. **Link to code definitions** (external reference)

---

## Testing Checklist

- [x] Lines without codes: No arrow, no badge
- [x] Lines with codes: Arrow visible, badge shows count
- [x] Click arrow: Expands to show codes
- [x] Click arrow again: Collapses codes
- [x] Multiple lines expanded: All work independently
- [x] Color coding: Correct colors for each code type
- [x] Responsive design: Works on mobile/tablet
- [x] No console errors
- [x] No linting errors

---

## Deployment

**Date:** November 9, 2025  
**Environment:** Pre-Production  
**Status:** ✅ **DEPLOYED**

### Deployment Steps Completed:
1. ✅ Updated `ClaimTreeView.tsx` with expandable line items
2. ✅ No linting errors
3. ✅ Deployed to pre-prod server
4. ✅ Frontend rebuilt successfully
5. ✅ PM2 restarted successfully

---

## How to Test

1. Go to: https://pre-prod.connectme.apps.totessoft.com/claims
2. Search for claims (any date range)
3. Expand a claim
4. Click **"Line Items"** tab
5. Look for lines with blue badge (e.g., "2 codes")
6. Click the **▶ arrow** to expand
7. See color-coded line-level claim codes
8. Click the **▼ arrow** to collapse

---

## Documentation

- **Technical Details:** This file
- **UI Guide:** `CLAIMS_UI_GUIDE.md` (to be updated)
- **Implementation:** `CLAIMS_DISPLAY_UPDATES.md`

---

**Line-level claim codes are now fully integrated!** 🎉

