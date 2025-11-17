# Multi-Practice Support - TIN & Payer ID in Bulk Upload

## ✅ What Was Added

### 1. Multi-Practice CSV Format
The bulk upload now supports **TIN** and **Payer ID** columns for processing claims from multiple practices in one file.

**New CSV Format:**
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id,tin,payer_id,first_service_date,last_service_date
FE23924647,KIMBERLY,KURAK,02/06/1969,990139951,854203105,87726,2025-07-01,2025-07-01
```

### 2. Automatic Grouping & Batch Processing
- Claims are automatically grouped by (TIN, Payer ID)
- Each group is processed with a separate batch query
- Optimized for multi-practice/multi-payer scenarios

### 3. Backward Compatibility
- **With TIN/Payer ID**: Multi-practice mode (groups and processes separately)
- **Without TIN/Payer ID**: Single-practice mode (uses user's organization TIN)

---

## 🎯 Key Features

### Multi-Practice Mode
```python
# System automatically detects TIN and Payer ID columns
# Groups claims:
Group 1: TIN=854203105, PayerID=87726 → 50 claims
Group 2: TIN=123456789, PayerID=87726 → 30 claims
Group 3: TIN=854203105, PayerID=12345 → 20 claims

# Each group gets its own batch query
```

### Single-Practice Mode (Legacy)
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id,first_service_date,last_service_date
# No TIN/Payer columns → uses user's organization TIN
```

---

## 📋 CSV Format Specification

### Required Columns (Always):
- `claim_number` - UHC claim number
- `first_name` - Patient first name
- `last_name` - Patient last name
- `date_of_birth` - MM/DD/YYYY format
- `subscriber_id` - Insurance member ID

### Required for Multi-Practice:
- `tin` - Practice Tax ID Number (9 digits)
- `payer_id` - UHC Payer ID (e.g., 87726)

### Recommended (for auto-detection):
- `first_service_date` - YYYY-MM-DD or MM/DD/YYYY
- `last_service_date` - YYYY-MM-DD or MM/DD/YYYY

---

## 🔧 How It Works

### 1. CSV Upload
User uploads CSV with claims from multiple practices

### 2. Auto-Detection
```python
if CSV has 'tin' and 'payer_id' columns:
    → Multi-practice mode
    → Group claims by (TIN, Payer ID)
else:
    → Single-practice mode
    → Use user's organization TIN
```

### 3. Batch Processing Per Group
```
For each (TIN, Payer ID) group:
    1. Look up Practice (by TIN)
    2. Look up Payer Mapping (by TIN + Payer ID)
    3. Run batch query for this group
    4. Match claims from CSV
    5. Aggregate results
```

### 4. Consolidated Results
All groups are combined into one results file with success/failure status per claim

---

## 📊 Example Use Cases

### Use Case 1: Single Practice, Single Payer
```csv
# All claims same practice
claim_number,first_name,last_name,dob,subscriber_id,tin,payer_id,service_date
ABC123,JOHN,DOE,01/01/1980,123456789,854203105,87726,2025-07-01
```

### Use Case 2: Multiple Practices, Same Payer
```csv
# Claims from 2 practices, same UHC payer
claim_number,first_name,last_name,dob,subscriber_id,tin,payer_id,service_date
ABC123,JOHN,DOE,01/01/1980,123456789,854203105,87726,2025-07-01
XYZ789,JANE,SMITH,02/02/1975,987654321,123456789,87726,2025-07-02
```

### Use Case 3: Multiple Practices, Multiple Payers
```csv
# Claims from 2 practices, 2 different UHC payers
claim_number,first_name,last_name,dob,subscriber_id,tin,payer_id,service_date
ABC123,JOHN,DOE,01/01/1980,123456789,854203105,87726,2025-07-01
XYZ789,JANE,SMITH,02/02/1975,987654321,123456789,12345,2025-07-02
```

---

## ⚙️ Backend Implementation

### New Functions Added:

#### 1. `group_csv_by_practice_payer(csv_data)`
Groups CSV rows by (TIN, Payer ID) tuple

#### 2. Updated `process_csv_file()`
- Detects multi-practice mode
- Loops through each practice/payer group
- Processes each group with separate batch query
- Handles errors per group gracefully

#### 3. Updated `batch_query_claims()`
Now calls UHC API directly (not WorkflowEngine) for reliability

---

## 🚀 Performance

### Multi-Practice Example:
```
Total Claims: 1000
- Practice A, Payer 1: 600 claims → 1 batch query (~5 seconds)
- Practice B, Payer 1: 300 claims → 1 batch query (~3 seconds)
- Practice A, Payer 2: 100 claims → 1 batch query (~1 second)

Total Time: ~9 seconds (vs 1000+ seconds with individual queries)
Speedup: 111x faster!
```

---

## 📝 Template Updated

**File**: `csv-templates/real-claims-july-2025.csv`

Now includes TIN and Payer ID columns:
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id,tin,payer_id,first_service_date,last_service_date
FE23924647,KIMBERLY,KURAK,02/06/1969,990139951,854203105,87726,2025-07-01,2025-07-01
51545088,RANDALL,MOIR,11/14/1951,997068769,854203105,87726,2025-07-01,2025-07-01
51598988,TOMMY,HOWELL,08/23/1959,993889760-00,854203105,87726,2025-07-03,2025-07-03
51611599,MOSTAFA,KORDI,04/07/1960,939557438-00,854203105,87726,2025-07-03,2025-07-03
FE98163821,ZOEY,WILCOX,10/03/2004,916676926,854203105,87726,2025-07-02,2025-07-02
```

---

## ✅ Testing

### Test Scenarios:
1. ✅ Single practice CSV (backward compatible)
2. ✅ Multi-practice CSV with same payer
3. ✅ Multi-practice CSV with different payers
4. ✅ Mixed valid/invalid TINs (error handling)
5. ✅ Missing TIN/Payer (falls back to user's org)

---

## 🎉 Benefits

1. **Flexibility**: Upload claims from multiple practices at once
2. **Efficiency**: Still uses batch query optimization
3. **Scalability**: Handle large volumes across practices
4. **Reliability**: Direct UHC API calls
5. **Backward Compatible**: Old CSVs still work

---

*Feature implemented: October 15, 2025*
*Status: Ready for deployment*
