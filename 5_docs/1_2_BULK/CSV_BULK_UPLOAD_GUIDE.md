# 📊 CSV Bulk Upload System - User Guide

## Overview

The CSV Bulk Upload system allows you to process multiple claim queries in batch using a simple CSV file. The system uses Celery for background processing and provides real-time progress tracking.

---

## 🎯 Quick Start

### 1. Prepare Your CSV File

Create a CSV file with the following format:

```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,CHANTAL,KISA,05/10/1975,057896633
ZE59426196,JOHN,DOE,01/15/1980,123456789
```

**Required Fields:**
- `claim_number` - The claim number to search for
- `first_name` - Patient's first name
- `last_name` - Patient's last name
- `date_of_birth` - Patient's date of birth (MM/DD/YYYY format)
- `subscriber_id` - Insurance subscriber ID

**File Requirements:**
- Format: CSV (Comma Separated Values)
- Maximum file size: 10MB
- Encoding: UTF-8
- No maximum row limit (but keep reasonable for performance)

---

## 📤 Upload Process

### API Endpoint

```
POST /api/v1/claims/bulk/upload/
```

### Request

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data
```

**Body:**
```
file: (binary file)
```

### Example using cURL

```bash
curl -X POST https://connectme.be.totesoft.com/api/v1/claims/bulk/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@claims.csv"
```

### Example using Python

```python
import requests

url = "https://connectme.be.totesoft.com/api/v1/claims/bulk/upload/"
headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}
files = {
    "file": open("claims.csv", "rb")
}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

### Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "claims.csv",
  "status": "PENDING",
  "total_rows": 0,
  "processed_rows": 0,
  "success_count": 0,
  "failure_count": 0,
  "progress_percentage": 0,
  "created_at": "2025-10-10T11:20:00Z"
}
```

---

## 📊 Monitoring Progress

### Get Job Status

```
GET /api/v1/claims/csv-jobs/{job_id}/
```

**Example:**
```bash
curl https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Real-Time Progress

```
GET /api/v1/claims/csv-jobs/{job_id}/progress/
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PROCESSING",
  "total_rows": 100,
  "processed_rows": 45,
  "success_count": 43,
  "failure_count": 2,
  "progress_percentage": 45.0,
  "success_rate": 95.6,
  "celery_status": "PROGRESS",
  "celery_info": {
    "current": 45,
    "total": 100,
    "percent": 45
  }
}
```

### List All Jobs

```
GET /api/v1/claims/csv-jobs/
```

---

## 📥 Download Results

Once the job status is `COMPLETED`, you can download the results CSV:

```
GET /api/v1/claims/csv-jobs/{job_id}/results/
```

**Example:**
```bash
curl -O -J https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/550e8400-e29b-41d4-a716-446655440000/results/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Results CSV Format

```csv
row,claim_number,status,patient_name,total_charged,total_paid,processed_date,success
1,ZE59426195,Finalized,CHANTAL KISA,720.00,351.00,08/08/2025,True
2,ZE59426196,Pending,JOHN DOE,500.00,0.00,08/10/2025,True
3,ZE59426197,Error,JANE SMITH,,,False,"Claim not found"
```

**Fields:**
- `row` - Original row number from input CSV
- `claim_number` - Claim number from input
- `status` - Claim status (if found)
- `patient_name` - Patient name
- `total_charged` - Total charged amount
- `total_paid` - Total paid amount
- `processed_date` - Date claim was processed
- `success` - Whether the query was successful (True/False)
- `error` - Error message (if success=False)

---

## 🔄 Retry Failed Jobs

If a job fails, you can retry it:

```
POST /api/v1/claims/csv-jobs/{job_id}/retry/
```

**Example:**
```bash
curl -X POST https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/550e8400-e29b-41d4-a716-446655440000/retry/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📈 Job Statuses

- **PENDING** - Job is queued, waiting to start
- **PROCESSING** - Job is currently being processed
- **COMPLETED** - Job finished successfully
- **FAILED** - Job encountered an error
- **CANCELLED** - Job was manually cancelled

---

## ⚡ Performance

### Processing Speed
- ~10-20 claims per minute (depending on API response times)
- Processing is done in the background using Celery workers
- Multiple jobs can be processed simultaneously

### Limits
- File size: 10MB maximum
- Concurrent jobs: No hard limit (but be reasonable)
- Timeout: 30 minutes per job

---

## 🛠️ Troubleshooting

### Job Stuck in PENDING
- Check if Celery worker is running: `sudo systemctl status celery`
- Check Celery logs: `sudo journalctl -u celery -f`

### Job Failed
- Check the `error_log` field in the job details
- Review individual row errors in the error log
- Verify CSV format and required fields
- Retry the job after fixing issues

### Slow Processing
- Large files may take time - check progress regularly
- API rate limits may slow down processing
- Check backend logs for detailed timing information

---

## 🔒 Security

- All uploads require authentication (Bearer token)
- Files are stored securely on the server
- Only users in the same organization can access their jobs
- Results are automatically cleaned up after 30 days

---

## 📞 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/claims/bulk/upload/` | Upload CSV file |
| `GET` | `/api/v1/claims/csv-jobs/` | List all jobs |
| `GET` | `/api/v1/claims/csv-jobs/{id}/` | Get job details |
| `GET` | `/api/v1/claims/csv-jobs/{id}/progress/` | Get real-time progress |
| `GET` | `/api/v1/claims/csv-jobs/{id}/results/` | Download results CSV |
| `POST` | `/api/v1/claims/csv-jobs/{id}/retry/` | Retry failed job |

---

## 💡 Best Practices

1. **Test with small files first** - Upload a small CSV (5-10 rows) to test
2. **Monitor progress** - Use the progress endpoint to track job status
3. **Handle errors gracefully** - Check error_log for failed rows
4. **Download results promptly** - Results are kept for 30 days
5. **Validate your CSV** - Ensure all required fields are present and formatted correctly

---

## 📝 Example Workflow

### Step 1: Prepare CSV
```bash
cat > claims.csv << EOF
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,CHANTAL,KISA,05/10/1975,057896633
EOF
```

### Step 2: Upload
```bash
JOB_ID=$(curl -X POST https://connectme.be.totesoft.com/api/v1/claims/bulk/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@claims.csv" \
  | jq -r '.id')

echo "Job ID: $JOB_ID"
```

### Step 3: Monitor
```bash
watch -n 5 "curl -s https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/$JOB_ID/progress/ \
  -H \"Authorization: Bearer $TOKEN\" | jq"
```

### Step 4: Download Results
```bash
curl -O -J https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/$JOB_ID/results/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎉 You're Ready!

The CSV Bulk Upload system is now fully operational. Start by uploading a small test file and monitor its progress. If you encounter any issues, check the troubleshooting section or contact support.

**Happy bulk processing!** 🚀

