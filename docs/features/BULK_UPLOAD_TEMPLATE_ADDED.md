# Bulk Upload Template Feature Added

## ✅ What Was Added

### 1. Download Template Button
Added a "Download Template" button to the bulk upload page that allows users to download a sample CSV file with the correct format.

### 2. CSV Template Format
The template includes the following fields:

| Field | Description | Required | Format |
|-------|-------------|----------|--------|
| **practice_tin** | Practice Tax ID Number | ✅ Yes | 9 digits (e.g., 854203105) |
| **patient_first_name** | Patient's first name | ✅ Yes | Text |
| **patient_last_name** | Patient's last name | ✅ Yes | Text |
| **patient_dob** | Patient date of birth | ✅ Yes | YYYY-MM-DD (e.g., 1980-01-15) |
| **date_of_service** | Date of service | ❌ Optional | YYYY-MM-DD (e.g., 2024-01-10) |

### 3. Sample Template Content
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
854203105,Jane,Doe,1975-06-20,2024-01-15
260167522,Bob,Johnson,1990-03-10,2024-01-20
260167522,Alice,Williams,1985-12-05,2024-01-25
```

### 4. UI Enhancements
- **Download Template Button**: Purple button with download icon in the top-right of the upload section
- **Format Requirements Box**: Blue info box showing all required fields and their formats
- **Helpful Tip**: Reminder to download the template for correct format

---

## 📸 What Users Will See

### Bulk Upload Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Upload CSV File                    [Download Template] 📥   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📋 CSV Format Requirements:                                 │
│  • practice_tin: Practice Tax ID Number (required)          │
│  • patient_first_name: Patient first name (required)        │
│  • patient_last_name: Patient last name (required)          │
│  • patient_dob: Date of birth YYYY-MM-DD (required)         │
│  • date_of_service: Service date YYYY-MM-DD (optional)      │
│                                                              │
│  💡 Tip: Click "Download Template" to get sample CSV        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              📄 Drop your CSV file here                      │
│                  or click to browse                          │
│                                                              │
│              Maximum file size: 10MB                         │
│                                                              │
│                  [Browse Files]                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 How to Use

### For Users:

1. **Go to Bulk Upload Page**
   - Navigate to: https://pre-prod.connectme.apps.totessoft.com/bulk-upload

2. **Download Template**
   - Click the "Download Template" button (top-right)
   - A file named `bulk_claims_template.csv` will be downloaded

3. **Fill in Your Data**
   - Open the template in Excel, Google Sheets, or any CSV editor
   - Replace the sample data with your actual patient information
   - Make sure to use the correct TIN for each practice

4. **Upload the File**
   - Drag and drop the CSV file onto the upload area
   - Or click "Browse Files" to select it
   - Click "Upload" to start processing

---

## 📋 Practice TINs

Current practices in the system:

| Practice Name | TIN |
|---------------|-----|
| RSM | 854203105 |
| BALIGA FP | 260167522 |

---

## 🔍 Example Use Cases

### Use Case 1: Search Multiple Patients in One Practice
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
854203105,Jane,Doe,1975-06-20,2024-01-15
854203105,Bob,Johnson,1990-03-10,2024-01-20
```

### Use Case 2: Search Across Multiple Practices
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
260167522,Jane,Doe,1975-06-20,2024-01-15
854203105,Bob,Johnson,1990-03-10,2024-01-20
260167522,Alice,Williams,1985-12-05,2024-01-25
```

### Use Case 3: Search Without Date of Service
```csv
practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,
854203105,Jane,Doe,1975-06-20,
```

---

## 🛠️ Technical Details

### Files Modified
- **Frontend**: `connectme-frontend/src/app/bulk-upload/page.tsx`
  - Added `downloadTemplate()` function
  - Added "Download Template" button
  - Updated CSV format requirements display

### Implementation
```typescript
const downloadTemplate = () => {
  // Create sample CSV template with all fields
  const template = `practice_tin,patient_first_name,patient_last_name,patient_dob,date_of_service
854203105,John,Smith,1980-01-15,2024-01-10
854203105,Jane,Doe,1975-06-20,2024-01-15
260167522,Bob,Johnson,1990-03-10,2024-01-20
260167522,Alice,Williams,1985-12-05,2024-01-25`

  // Create blob and download
  const blob = new Blob([template], { type: 'text/csv;charset=utf-8;' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'bulk_claims_template.csv'
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}
```

---

## ✅ Testing Checklist

- [x] Template downloads correctly
- [x] Template has correct headers
- [x] Template has sample data
- [x] Format requirements are clearly displayed
- [x] Button is visible and accessible
- [x] Frontend deployed to pre-prod
- [x] Frontend restarted

---

## 📝 Notes

### Date Format
- All dates must be in **YYYY-MM-DD** format
- Examples: `2024-01-15`, `1980-06-20`
- ❌ Wrong: `01/15/2024`, `15-01-2024`

### TIN Format
- Must be exactly 9 digits
- No dashes or spaces
- Examples: `854203105`, `260167522`
- ❌ Wrong: `85-4203105`, `85 4203105`

### Required vs Optional Fields
- **Required**: practice_tin, patient_first_name, patient_last_name, patient_dob
- **Optional**: date_of_service
- If date_of_service is empty, the system will search for all claims for that patient

---

## 🚀 Deployment

**Status**: ✅ **DEPLOYED TO PRE-PROD**

**URL**: https://pre-prod.connectme.apps.totessoft.com/bulk-upload

**Deployed**: November 12, 2025

---

## 💡 Future Enhancements

Potential improvements for future releases:

1. **Multiple Template Options**
   - Template with claim numbers
   - Template for eligibility checks
   - Template for specific date ranges

2. **Validation**
   - Client-side CSV validation before upload
   - Show errors for invalid formats
   - Highlight problematic rows

3. **Practice Dropdown**
   - Auto-populate TIN from practice dropdown
   - Reduce manual data entry errors

4. **Bulk Edit**
   - Edit CSV directly in the browser
   - No need to download and re-upload

---

**Last Updated**: November 12, 2025  
**Version**: 1.0  
**Status**: ✅ Live in Pre-Production

