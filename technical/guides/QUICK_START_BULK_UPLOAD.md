# Quick Start: CSV Bulk Upload

## 🚀 Get Started in 3 Minutes

### Step 1: Access the Upload Page
Open your browser and go to:
```
https://connectme.apps.totesoft.com/bulk-upload
```

### Step 2: Prepare Your CSV
Create a file named `claims.csv` with this format:
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id
ZE59426195,John,Doe,1980-01-15,ABC123456
```

[Download Template](../claims-template.csv)

### Step 3: Upload & Process
1. **Drag** your CSV file to the upload area (or click "Browse Files")
2. Click **"Upload and Process"**
3. Watch the **real-time progress bar**
4. Click **"Results"** button when complete

---

## 📥 What You Get

After processing, you'll receive a results CSV like this:

```csv
row,claim_number,status,patient_name,total_charged,total_paid,processed_date,success,error_message
1,ZE59426195,Processed,John Doe,1500.00,1200.00,2025-10-10,true,
```

---

## 💡 Pro Tips

- **Test Small First**: Start with 5-10 claims to verify format
- **Max File Size**: 10 MB (~2000 claims)
- **Processing Time**: ~10 seconds per claim
- **Live Updates**: Progress updates every 3 seconds automatically

---

## ❓ Need Help?

- **Full User Guide**: [CSV_BULK_UPLOAD_USER_GUIDE.md](./CSV_BULK_UPLOAD_USER_GUIDE.md)
- **Technical Docs**: [CSV_SYSTEM_COMPLETE.md](./CSV_SYSTEM_COMPLETE.md)
- **Support**: support@totesoft.com

---

## ✅ System Status

🟢 **All Systems Operational**

- Backend API: https://connectme.be.totesoft.com
- Frontend UI: https://connectme.apps.totesoft.com
- Celery Workers: 2 active
- Redis Broker: Connected
- Processing: ~6 claims/minute

---

That's it! You're ready to process claims in bulk. 🎉

