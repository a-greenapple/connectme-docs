# CSV Bulk Upload - User Guide

## Overview

The CSV Bulk Upload feature allows you to process multiple claims at once by uploading a CSV file. The system will process each claim asynchronously and provide you with a downloadable results file.

---

## 🚀 Quick Start

### 1. Access the Bulk Upload Page

Navigate to: **`https://connectme.apps.totesoft.com/bulk-upload`**

Or use the navigation menu: **Claims** → **Bulk Upload**

### 2. Prepare Your CSV File

Create a CSV file with the following columns:

```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,John,Doe,1980-01-15,ABC123456
ZE59426196,Jane,Smith,1975-05-20,XYZ789012
ZE59426197,Bob,Johnson,1990-03-10,DEF345678
```

**Required Fields:**
- `claim_number` - The UHC claim number
- `first_name` - Patient's first name
- `last_name` - Patient's last name  
- `date_of_birth` - Format: YYYY-MM-DD
- `subscriber_id` - Subscriber/Member ID

**File Requirements:**
- Format: CSV (`.csv`)
- Maximum size: 10 MB
- Maximum rows: No hard limit, but processing time increases with size
- Encoding: UTF-8

### 3. Upload Your File

**Option A: Drag and Drop**
1. Drag your CSV file onto the upload area
2. The file name and size will be displayed
3. Click "Upload and Process"

**Option B: Browse Files**
1. Click "Browse Files" button
2. Select your CSV file from your computer
3. Click "Upload and Process"

### 4. Monitor Progress

Once uploaded, you'll see real-time progress:
- **Status**: Current state (Pending, Processing, Completed, Failed)
- **Progress Bar**: Visual indicator of completion
- **Statistics**:
  - ✅ Successful: Claims processed successfully
  - ❌ Failed: Claims that encountered errors
  - ⏳ Remaining: Claims yet to be processed

### 5. Download Results

When processing completes:
1. Find your job in the "Upload History" section
2. Click the **"Results"** button
3. A CSV file will be downloaded with detailed results

---

## 📊 Understanding Results

### Results CSV Format

```csv
row,claim_number,status,patient_name,total_charged,total_paid,processed_date,success,error_message
1,ZE59426195,Processed,John Doe,1500.00,1200.00,2025-10-10,true,
2,ZE59426196,Not Found,Jane Smith,,,false,Claim not found in system
3,ZE59426197,Processed,Bob Johnson,850.00,750.00,2025-10-10,true,
```

**Columns Explained:**
- `row` - Original row number from your input file
- `claim_number` - The claim number you searched for
- `status` - Processing status (Processed, Not Found, Error)
- `patient_name` - Full name of the patient
- `total_charged` - Total charged amount
- `total_paid` - Total paid amount
- `processed_date` - Date the claim was processed
- `success` - `true` if successful, `false` if failed
- `error_message` - Error details (if any)

---

## 🔄 Job Statuses

### **PENDING** ⏳
- Your file has been uploaded successfully
- Waiting in queue to be processed
- Usually transitions to PROCESSING within seconds

### **PROCESSING** 🔄
- Currently being processed
- Progress bar shows completion percentage
- Real-time updates every 3 seconds

### **COMPLETED** ✅
- All rows have been processed
- Results file is ready for download
- Shows success and failure counts

### **FAILED** ❌
- Processing encountered a critical error
- You can retry the job using the "Retry" button
- Check error logs for details

---

## 💡 Best Practices

### File Preparation
1. **Validate Data**: Ensure all required fields are filled
2. **Date Format**: Use YYYY-MM-DD (e.g., 1980-01-15)
3. **Remove Special Characters**: Avoid special characters in names
4. **Check for Duplicates**: Remove duplicate claim numbers
5. **Test Small First**: Start with 5-10 rows to verify format

### Optimal Upload Size
- **Small (< 50 rows)**: ~1-2 minutes processing time
- **Medium (50-200 rows)**: ~5-10 minutes processing time  
- **Large (200-500 rows)**: ~20-30 minutes processing time
- **Very Large (> 500 rows)**: Consider splitting into multiple files

### Error Handling
- If a job fails, download the results CSV to see which rows failed
- Fix the failed rows and create a new CSV with only those
- Upload the corrected file as a new job

---

## 🎯 Example Workflow

### Scenario: Processing 100 Claims

1. **Prepare CSV** (5 minutes)
   - Export claim numbers from your system
   - Add patient information
   - Validate data format

2. **Upload** (30 seconds)
   - Drag CSV file to upload area
   - Click "Upload and Process"
   - Confirm upload success

3. **Monitor** (10-15 minutes)
   - Watch progress bar
   - Note any errors in real-time
   - Progress updates every 3 seconds

4. **Download Results** (1 minute)
   - Click "Results" button when complete
   - Open in Excel/Google Sheets
   - Review success and failure counts

5. **Handle Failures** (if any)
   - Filter for `success = false`
   - Fix data issues
   - Re-upload failed rows

---

## ⚠️ Common Issues & Solutions

### Issue: "Please select a CSV file"
**Solution**: Ensure your file has a `.csv` extension

### Issue: "File size must be less than 10MB"
**Solution**: Split your file into smaller chunks of 500-1000 rows each

### Issue: Job stuck in "PENDING" status
**Solution**: 
- Wait 30 seconds (server might be processing other jobs)
- Refresh the page
- Contact support if stuck for > 5 minutes

### Issue: All rows failing
**Solution**:
- Check CSV format matches required columns exactly
- Verify date format is YYYY-MM-DD
- Ensure claim numbers are valid UHC format

### Issue: Some rows failing
**Solution**:
- Download results CSV
- Check `error_message` column for specific errors
- Common errors:
  - "Claim not found" - Invalid claim number
  - "Invalid date format" - Date format incorrect
  - "Missing required field" - Empty required field

---

## 📞 Support & Troubleshooting

### Need Help?
- **Email**: support@totesoft.com
- **Documentation**: `/docs/bulk-upload`
- **System Status**: Check if services are running

### Reporting Issues
When reporting an issue, include:
1. Job ID (found in upload history)
2. Input CSV file (first 5 rows)
3. Error message screenshot
4. Time of upload

---

## 🔒 Security & Privacy

- ✅ All uploads are encrypted in transit (HTTPS)
- ✅ Files are stored securely on the server
- ✅ Only you can access your uploaded files and results
- ✅ Files are automatically deleted after 30 days
- ✅ Authentication required for all operations

---

## 📈 Performance Tips

### To maximize processing speed:
1. **Upload during off-peak hours** (early morning/late evening)
2. **Split large files** into multiple smaller uploads
3. **Use valid data** to reduce API retry overhead
4. **Keep rows under 1000** per file for faster processing

### Expected Processing Times:
- **Authentication**: ~2 seconds
- **Per Claim**: ~8-10 seconds (including API calls)
- **Overhead**: ~5 seconds per file

**Example**: 100 claims = ~15 minutes total

---

## 🎓 Advanced Features

### Retry Failed Jobs
1. Find the failed job in history
2. Click "Retry" button
3. System will re-process all rows
4. Previous results are preserved

### Bulk Download
- Download results for multiple jobs
- Use browser's download manager
- Results are timestamped

### Progress Monitoring
- Real-time updates every 3 seconds
- No need to refresh the page
- Percentage-based progress bar

---

## 📝 Sample CSV Templates

### Template 1: Basic Claims
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,John,Doe,1980-01-15,ABC123456
```

### Template 2: Multiple Claims
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,John,Doe,1980-01-15,ABC123456
ZE59426196,Jane,Smith,1975-05-20,XYZ789012
ZE59426197,Bob,Johnson,1990-03-10,DEF345678
ZE59426198,Alice,Williams,1985-07-22,GHI456789
ZE59426199,Charlie,Brown,1992-11-30,JKL567890
```

**Download Template**: [claims-template.csv](#)

---

## ✅ Checklist Before Upload

- [ ] CSV file has correct column names
- [ ] All required fields are filled
- [ ] Date format is YYYY-MM-DD
- [ ] File size is under 10 MB
- [ ] Claim numbers are valid UHC format
- [ ] No special characters in data
- [ ] File is saved as UTF-8 encoding

---

## 🚀 Next Steps

After successfully processing your bulk upload:

1. **Review Results**: Check the results CSV for any failures
2. **Fix Errors**: Correct any failed rows and re-upload
3. **Export Reports**: Use results for billing/reporting
4. **Schedule Regular Uploads**: Create a workflow for regular bulk processing

---

**Last Updated**: October 10, 2025  
**Version**: 1.0  
**Feature Status**: Production Ready ✅

