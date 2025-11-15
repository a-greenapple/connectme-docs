# Sample Bulk Claims Data

## 📋 Available Sample Files

### 1. `sample_bulk_claims_real.csv`
**20 rows** with realistic patient data for testing bulk upload.

**Practices:**
- **RSM** (TIN: 854203105) - 10 patients
- **BALIGA FP** (TIN: 260167522) - 10 patients

**Data includes:**
- Realistic patient names
- Valid date formats (YYYY-MM-DD)
- Date of birth (1975-1995 range)
- Date of service (January-February 2024)

---

### 2. `sample_bulk_claims_with_real_claim_numbers.csv`
**10 rows** with simplified patient names for easy testing.

**Use this for:**
- Quick testing
- Verifying bulk upload functionality
- Testing practice filtering

---

## 🎯 How to Use

### Method 1: Download from UI
1. Go to: https://pre-prod.connectme.apps.totessoft.com/bulk-upload
2. Click "Download Template" button
3. Fill in with your data
4. Upload

### Method 2: Use Sample Files
1. Download one of the sample CSV files above
2. Optionally modify the data
3. Upload to bulk upload page

### Method 3: Create Your Own
Use this format:
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
260167522,Jane,Doe,1975-06-20,2024-01-15
```

---

## 📊 Practice Information

| Practice Name | TIN | NPI | Location |
|---------------|-----|-----|----------|
| RSM | 854203105 | - | - |
| BALIGA FP | 260167522 | - | - |

---

## 🧪 Testing Scenarios

### Scenario 1: Single Practice
Upload only RSM (854203105) patients:
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
854203105,Mary,Johnson,1975-06-20,2024-01-15
854203105,Robert,Williams,1990-03-10,2024-01-20
```

### Scenario 2: Multiple Practices
Upload mixed practices:
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
260167522,Jane,Doe,1975-06-20,2024-01-15
854203105,Bob,Johnson,1990-03-10,2024-01-20
260167522,Alice,Williams,1985-12-05,2024-01-25
```

### Scenario 3: Without Date of Service
Test searching without specific service dates:
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,
854203105,Mary,Johnson,1975-06-20,
```

### Scenario 4: Large Batch (100+ rows)
For performance testing, duplicate the sample data multiple times.

---

## ⚠️ Important Notes

### Date Formats
- **DOB Format**: YYYY-MM-DD (e.g., 1980-01-15)
- **Service Date Format**: YYYY-MM-DD (e.g., 2024-01-10)
- ❌ **Wrong**: 01/15/1980, 15-01-1980, Jan 15 1980

### Required Fields
- ✅ **practice_tin** - Must match existing practice
- ✅ **patient_first_name** - Required
- ✅ **patient_last_name** - Required
- ✅ **patient_dob** - Required in YYYY-MM-DD format
- ❌ **date_of_service** - Optional

### TIN Validation
- Must be exactly 9 digits
- Must match an existing practice in the system
- No dashes or spaces

---

## 🔍 Expected Results

### Successful Upload
```
✅ File uploaded successfully
📊 Processing 20 rows
⏳ Estimated time: 30-60 seconds
```

### Processing
```
🔄 Processing claim 1/20...
🔄 Processing claim 2/20...
...
✅ Completed: 18 successful, 2 failed
```

### Results
- **Success**: Claims found and details retrieved
- **Failure**: Patient not found or no claims for date range

---

## 📈 Performance Expectations

| Rows | Expected Time | Notes |
|------|---------------|-------|
| 10 | 15-30 seconds | Quick test |
| 20 | 30-60 seconds | Standard batch |
| 50 | 1-2 minutes | Medium batch |
| 100 | 2-4 minutes | Large batch |
| 500+ | 10-20 minutes | Very large batch |

**Note**: Processing time depends on:
- Number of claims per patient
- External API response time
- Server load

---

## 🛠️ Troubleshooting

### Issue: "Invalid TIN"
**Solution**: Use 854203105 or 260167522

### Issue: "Invalid date format"
**Solution**: Use YYYY-MM-DD format (e.g., 2024-01-15)

### Issue: "No claims found"
**Solution**: 
- Try without date_of_service
- Check patient details are correct
- Verify practice TIN is correct

### Issue: "Processing timeout"
**Solution**:
- Reduce batch size
- Try again (may be temporary)
- Check server status

---

## 📝 Sample Data Details

### Patient Demographics
- **Age Range**: 29-49 years old (born 1975-1995)
- **Service Dates**: January-February 2024
- **Names**: Common US names for easy identification

### Data Distribution
- **RSM (854203105)**: 10 patients
  - 5 Male names (John, Robert, Michael, William, David)
  - 5 Female names (Mary, Patricia, Jennifer, Linda, Barbara)

- **BALIGA FP (260167522)**: 10 patients
  - 5 Male names (James, Joseph, Charles, Christopher, Daniel)
  - 5 Female names (Susan, Jessica, Sarah, Nancy, Karen)

---

## 🔐 Privacy & Security

### Test Data
- ✅ All names are fictional
- ✅ All dates are generated for testing
- ✅ No real patient information
- ✅ Safe for development/testing

### Real Data
- ❌ Never use real patient data in test files
- ❌ Never commit real PHI to version control
- ❌ Never share real patient information
- ✅ Always use de-identified or synthetic data

---

## 📚 Additional Resources

### Documentation
- `BULK_UPLOAD_TEMPLATE_ADDED.md` - Template feature documentation
- `BULK_UPLOAD_HISTORY_FEATURES.md` - History tracking features
- `FIX_CLAIM_SEARCH_TIMEOUT.md` - Performance optimization

### Test Scripts
- `test_bulk_claim_search.py` - Automated testing script
- `testing/test_bulk_upload.py` - Bulk upload tests

---

## ✅ Quick Start

1. **Download sample file**:
   ```bash
   # Use sample_bulk_claims_real.csv
   ```

2. **Upload to system**:
   - Go to: https://pre-prod.connectme.apps.totessoft.com/bulk-upload
   - Drag and drop the CSV file
   - Click "Upload"

3. **Monitor progress**:
   - Watch the progress bar
   - Check history sidebar for status
   - View results when complete

4. **Download results**:
   - Click "View" to see details
   - Click "Download" to get CSV with results

---

**Last Updated**: November 12, 2025  
**Files Created**: 2 sample CSV files  
**Total Sample Records**: 30 patients

