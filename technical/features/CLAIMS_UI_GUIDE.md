# Claims UI Guide - Payment Mode & Claim Codes

## Overview
This guide shows how the new payment mode and claim codes features appear in the UI.

---

## 1. Payment Mode Display

### Location
**Payments Tab** → Expand any claim → Click "Payments" tab

### What You'll See

```
┌─────────────────────────────────────────────────────────────────┐
│  💳 Payments                                                     │
│  2 payment record(s) for this claim                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Check Number              Payment Mode                   │  │
│  │  123456789                 [EFT (Electronic)]             │  │
│  │                            ↑ Blue badge                   │  │
│  │  Check Amount              Draft Amount                   │  │
│  │  $1,234.56                 $1,234.56                      │  │
│  │                                                           │  │
│  │  Draft Number              Issue Date                     │  │
│  │  987654                    05/15/2025                     │  │
│  │                                                           │  │
│  │  Payee                                                    │  │
│  │  APPLE BILLING AND CREDENTIALING LLC                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Check Number              Payment Mode                   │  │
│  │  987654321                 [Check (Paper)]                │  │
│  │                            ↑ Green badge                  │  │
│  │  Check Amount              Draft Amount                   │  │
│  │  $567.89                   $567.89                        │  │
│  │  ...                                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Payment Mode Colors
- **🔵 EFT (Electronic)** - Blue badge with blue background
- **🟢 Check (Paper)** - Green badge with green background
- **⚪ N/A** - Gray badge (when indicator is missing)

---

## 2. Claim Codes Section

### Location
**Claim Codes Tab** → Expand any claim → Click "Claim Codes" tab

### Navigation
```
Left Sidebar:
  📋 Overview
  💰 Financial
  📄 Line Items (3)
  💳 Payments (2)
  📝 Claim Codes (4)  ← New section with count badge
  🕐 Timeline
  🔄 Reconciliation
  📦 Raw Data
```

### What You'll See

```
┌─────────────────────────────────────────────────────────────────┐
│  📝 Claim Codes & Remarks                                        │
│  4 code(s) associated with this claim                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  💬 Remarks (1)                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ║ [0038]  This claim was processed based on the allowed  │  │
│  │ ║         amount. Please do not bill the member any      │  │
│  │ ║         amount that is more than their cost share.     │  │
│  │ ↑ Blue left border                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ⚠️ Adjustment Reason Codes - CARC (3)                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ║ [045]  CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE   │  │
│  │ ║         OR CONTRACTED/LEGISLATED FEE ARRANGEMENT.       │  │
│  │ ↑ Orange left border                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ║ [002]  COINSURANCE AMOUNT                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ║ [253]  SEQUESTRATION - REDUCTION IN FEDERAL PAYMENT    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Code Categories

#### 1. **Remarks (Blue Theme)**
- **Icon:** 💬
- **Color:** Blue background with blue left border
- **Purpose:** Informational messages from the payer
- **Example:**
  ```
  [0038] This claim was processed based on the allowed amount.
         Please do not bill the member any amount that is more
         than their cost share.
  ```

#### 2. **Adjustment Reason Codes - CARC (Orange Theme)**
- **Icon:** ⚠️
- **Color:** Orange background with orange left border
- **Purpose:** Explains why claim amounts were adjusted
- **Examples:**
  ```
  [045] CHARGE EXCEEDS FEE SCHEDULE/MAXIMUM ALLOWABLE OR
        CONTRACTED/LEGISLATED FEE ARRANGEMENT.
  
  [002] COINSURANCE AMOUNT
  
  [253] SEQUESTRATION - REDUCTION IN FEDERAL PAYMENT
  ```

#### 3. **Other Codes (Gray Theme)**
- **Icon:** 📌
- **Color:** Gray background with gray left border
- **Purpose:** Any other code types from the payer
- **Format:** Includes code type label above description

---

## 3. Complete Claim View Workflow

### Step 1: Search for Claims
```
Claims Search Page
  ↓
Select Practice: [RSM ▼]
Date Range: 05/01/2025 - 05/31/2025
  ↓
[Search Claims]
```

### Step 2: View Results
```
Claims Results Table
┌──────────────┬─────────┬──────────┬────────┬─────────┬─────────┐
│ Claim Number │ Patient │ Service  │ Status │ Charged │ Paid    │
├──────────────┼─────────┼──────────┼────────┼─────────┼─────────┤
│ ▶ 12345678   │ John D  │ 05/15/25 │ Final  │ $500.00 │ $400.00 │
│   ↑ Click to expand                                            │
└──────────────┴─────────┴──────────┴────────┴─────────┴─────────┘
```

### Step 3: Expand Claim Details
```
┌─────────────────────────────────────────────────────────────────┐
│  LEFT SIDEBAR (20%)           │  RIGHT PANEL (80%)              │
├───────────────────────────────┼─────────────────────────────────┤
│  Claim 12345678               │  TABS:                          │
│  John Doe                     │  [Overview] [Financial]         │
│                               │  [Line Items] [Payments]        │
│  📋 Overview                  │  [Claim Codes] [Timeline]       │
│  💰 Financial                 │  [Reconciliation]               │
│  📄 Line Items (3)            │                                 │
│  💳 Payments (2)              │  ← Click any tab to view        │
│  📝 Claim Codes (4) ← NEW!    │                                 │
│  🕐 Timeline                  │  CONTENT AREA:                  │
│  🔄 Reconciliation            │  [Details displayed here]       │
│  📦 Raw Data                  │                                 │
└───────────────────────────────┴─────────────────────────────────┘
```

### Step 4: View Payment Mode
```
Click "Payments" tab
  ↓
See payment records with mode badges:
  - EFT (Electronic) - Blue
  - Check (Paper) - Green
```

### Step 5: View Claim Codes
```
Click "Claim Codes" tab
  ↓
See organized code sections:
  - Remarks (Blue)
  - CARC codes (Orange)
  - Other codes (Gray)
```

---

## 4. Key Features

### Payment Mode
✅ **Visible at a glance** - Color-coded badges  
✅ **Clear labeling** - "EFT (Electronic)" or "Check (Paper)"  
✅ **Consistent placement** - Always next to check number  

### Claim Codes
✅ **Organized by type** - Remarks, CARC, Other  
✅ **Color-coded** - Blue, Orange, Gray themes  
✅ **Full descriptions** - No truncation  
✅ **Count badges** - Shows total codes in navigation  
✅ **Empty state** - Clear message when no codes  

---

## 5. Mobile Responsiveness

Both features are fully responsive:
- Payment mode badges scale appropriately
- Claim codes stack vertically on smaller screens
- Navigation remains accessible
- Text remains readable

---

## 6. Accessibility

- **Color + Text:** Not relying on color alone (includes text labels)
- **Keyboard Navigation:** All tabs and sections keyboard accessible
- **Screen Readers:** Proper semantic HTML and ARIA labels
- **Contrast:** All text meets WCAG AA standards

---

## 7. Browser Compatibility

Tested and working on:
- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Safari 17+
- ✅ Edge 120+

---

## 8. Performance

- **No additional API calls** - Data already included in claim response
- **Lazy rendering** - Only active tab content is rendered
- **Optimized filtering** - Client-side filtering of claim codes
- **Fast navigation** - Instant tab switching

---

## Need Help?

If you don't see the new features:
1. **Hard refresh** the page (Ctrl+F5 or Cmd+Shift+R)
2. **Clear browser cache**
3. **Check that you're on pre-prod:** `https://pre-prod.connectme.apps.totessoft.com`
4. **Verify claim has payment data** - Some claims may not have payments yet

---

**Last Updated:** November 9, 2025  
**Version:** 1.0  
**Environment:** Pre-Production

