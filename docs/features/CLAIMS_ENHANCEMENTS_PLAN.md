# Claims Search & Bulk Upload Enhancement Plan

**Date:** October 31, 2025  
**Status:** 📋 Planning Phase

---

## Current State Analysis

### Claims Search View (`ClaimViewSet`)
**Current Features:**
- ✅ Basic claim listing (filtered by organization)
- ✅ Single claim status check
- ✅ Ordered by query date
- ✅ PHI encryption for SSN

**Limitations:**
- ❌ No advanced filtering (by date range, status, provider, amount)
- ❌ No search by patient info
- ❌ No pagination customization
- ❌ No export functionality
- ❌ No claim history tracking
- ❌ No bulk status refresh
- ❌ Limited sorting options

### Bulk Upload View (`BulkUploadView` & `CSVJobViewSet`)
**Current Features:**
- ✅ CSV file upload with provider selection
- ✅ Job tracking (PENDING, PROCESSING, COMPLETED, FAILED)
- ✅ Organization scoping
- ✅ File validation

**Limitations:**
- ❌ No real-time progress updates
- ❌ No partial success handling (all-or-nothing)
- ❌ No CSV template download
- ❌ No preview before processing
- ❌ No duplicate detection
- ❌ No retry for failed rows only
- ❌ Limited error reporting
- ❌ No batch size configuration
- ❌ Celery tasks not implemented (TODO comments)

---

## Proposed Enhancements

### 🔍 Part 1: Claims Search Enhancements

#### 1.1 Advanced Filtering
```python
# Add filter backends and custom filters
GET /api/v1/claims/claims/?status=PAID&provider=uhc&min_amount=100
GET /api/v1/claims/claims/?service_date_from=2024-01-01&service_date_to=2024-12-31
GET /api/v1/claims/claims/?search=claim_number_or_patient_name
GET /api/v1/claims/claims/?queried_after=2024-10-01
```

**Benefits:**
- Find specific claims quickly
- Generate reports by date range
- Track claims by status/provider
- Search by multiple criteria

#### 1.2 Bulk Status Refresh
```python
POST /api/v1/claims/claims/bulk_refresh/
{
  "claim_ids": ["uuid1", "uuid2", "uuid3"]
}

# Response:
{
  "total": 3,
  "updated": 2,
  "failed": 1,
  "results": [...]
}
```

**Benefits:**
- Update multiple claims at once
- Re-check stale claim statuses
- Batch operations for efficiency

#### 1.3 Export Functionality
```python
GET /api/v1/claims/claims/export/?format=csv&status=PAID
GET /api/v1/claims/claims/export/?format=xlsx&date_from=2024-01-01

# Returns downloadable file with filtered claims
```

**Benefits:**
- Generate reports for accounting
- Share data with external systems
- Backup claim records

#### 1.4 Claim History & Audit Trail
```python
GET /api/v1/claims/claims/{id}/history/

# Response:
{
  "claim_number": "12345",
  "status_changes": [
    {"status": "PENDING", "changed_at": "2024-01-01", "changed_by": "user1"},
    {"status": "PAID", "changed_at": "2024-01-15", "changed_by": "system"}
  ],
  "queries": [
    {"queried_at": "2024-01-01", "queried_by": "user1"},
    {"queried_at": "2024-01-15", "queried_by": "user2"}
  ]
}
```

**Benefits:**
- Track claim lifecycle
- Audit compliance (HIPAA)
- Identify patterns

#### 1.5 Enhanced Sorting & Pagination
```python
GET /api/v1/claims/claims/?ordering=-payment_amount&page_size=100
GET /api/v1/claims/claims/?ordering=service_date,-queried_at
```

**Benefits:**
- Find high-value claims
- Custom page sizes
- Multi-field sorting

#### 1.6 Aggregate Statistics
```python
GET /api/v1/claims/claims/stats/

# Response:
{
  "total_claims": 1250,
  "by_status": {
    "PAID": 800,
    "PENDING": 300,
    "DENIED": 150
  },
  "by_provider": {
    "uhc": 600,
    "aetna": 400,
    "cigna": 250
  },
  "financial_summary": {
    "total_billed": 500000.00,
    "total_paid": 450000.00,
    "total_pending": 50000.00
  },
  "date_range": {
    "earliest": "2024-01-01",
    "latest": "2024-12-31"
  }
}
```

**Benefits:**
- Dashboard metrics
- Quick overview
- Business intelligence

---

### 📤 Part 2: Bulk Upload Enhancements

#### 2.1 Real-Time Progress Updates (WebSocket/SSE)
```python
# WebSocket connection for live updates
ws://api/v1/claims/jobs/{job_id}/progress/

# Messages:
{
  "type": "progress",
  "processed": 50,
  "total": 100,
  "success": 45,
  "failed": 5,
  "current_row": 50
}
```

**Benefits:**
- Live feedback during processing
- Better UX for large files
- No need to poll for status

#### 2.2 Partial Success Handling
```python
# Job completes even if some rows fail
{
  "job_id": "uuid",
  "status": "COMPLETED_WITH_ERRORS",
  "total_rows": 100,
  "successful": 95,
  "failed": 5,
  "failed_rows": [
    {
      "row_number": 23,
      "data": {...},
      "error": "Invalid SSN format"
    },
    ...
  ]
}
```

**Benefits:**
- Don't lose successful rows
- Identify specific failures
- Retry only failed rows

#### 2.3 CSV Template Download
```python
GET /api/v1/claims/upload/template/?provider=uhc

# Returns CSV with:
# - Correct column headers
# - Example data
# - Validation rules in comments
```

**Benefits:**
- Reduce upload errors
- Standardize format
- User guidance

#### 2.4 Upload Preview & Validation
```python
POST /api/v1/claims/upload/preview/
{
  "file": <file>,
  "provider": "uhc"
}

# Response:
{
  "valid": true,
  "total_rows": 100,
  "sample_rows": [...],  # First 5 rows
  "validation_warnings": [
    "Row 23: SSN format unusual but valid",
    "Row 45: Old service date (>2 years)"
  ],
  "estimated_processing_time": "2 minutes"
}
```

**Benefits:**
- Catch errors before processing
- Preview data
- Confirm before submission

#### 2.5 Duplicate Detection
```python
# Automatically detect duplicates
{
  "duplicates_found": 5,
  "duplicate_strategy": "skip",  # or "update" or "error"
  "duplicates": [
    {
      "row": 10,
      "claim_number": "12345",
      "existing_claim_id": "uuid",
      "action": "skipped"
    }
  ]
}
```

**Benefits:**
- Prevent duplicate claims
- Update existing claims
- Data integrity

#### 2.6 Retry Failed Rows
```python
POST /api/v1/claims/jobs/{job_id}/retry_failed/

# Retries only the rows that failed
# Creates new job or updates existing
```

**Benefits:**
- Fix errors and reprocess
- No need to re-upload entire file
- Efficient error recovery

#### 2.7 Batch Size Configuration
```python
POST /api/v1/claims/upload/
{
  "file": <file>,
  "provider": "uhc",
  "batch_size": 50,  # Process 50 rows at a time
  "priority": "high"  # Queue priority
}
```

**Benefits:**
- Control processing speed
- Manage API rate limits
- Prioritize urgent uploads

#### 2.8 Enhanced Error Reporting
```python
GET /api/v1/claims/jobs/{job_id}/errors/

# Response:
{
  "error_summary": {
    "validation_errors": 3,
    "api_errors": 2,
    "network_errors": 1
  },
  "errors_by_type": {
    "Invalid SSN": 2,
    "API timeout": 2,
    "Missing required field": 2
  },
  "detailed_errors": [
    {
      "row_number": 23,
      "error_type": "validation",
      "error_code": "INVALID_SSN",
      "error_message": "SSN must be 9 digits",
      "field": "patient_ssn",
      "value": "12-345",
      "suggestion": "Remove hyphens and ensure 9 digits"
    }
  ],
  "downloadable_error_report": "/api/v1/claims/jobs/{job_id}/errors/download/"
}
```

**Benefits:**
- Understand failure patterns
- Fix data issues
- Better error messages

#### 2.9 Scheduled Bulk Processing
```python
POST /api/v1/claims/upload/schedule/
{
  "file": <file>,
  "provider": "uhc",
  "schedule_for": "2024-11-01T02:00:00Z",  # Off-peak hours
  "recurrence": "weekly"  # Optional: recurring uploads
}
```

**Benefits:**
- Process during off-peak hours
- Automated recurring uploads
- Better resource management

---

## Implementation Priority

### 🔥 Phase 1: High Priority (Week 1-2)
1. **Advanced Filtering** (1.1) - Most requested feature
2. **Partial Success Handling** (2.2) - Critical for UX
3. **Enhanced Error Reporting** (2.8) - Reduces support burden
4. **CSV Template Download** (2.3) - Prevents upload errors

### 🚀 Phase 2: Medium Priority (Week 3-4)
5. **Bulk Status Refresh** (1.2) - Useful for stale claims
6. **Upload Preview & Validation** (2.4) - Improves data quality
7. **Duplicate Detection** (2.5) - Data integrity
8. **Retry Failed Rows** (2.6) - Error recovery

### 💡 Phase 3: Nice to Have (Week 5-6)
9. **Export Functionality** (1.3) - Reporting
10. **Aggregate Statistics** (1.6) - Dashboard
11. **Real-Time Progress** (2.1) - Advanced UX
12. **Batch Size Configuration** (2.7) - Performance tuning

### 🎯 Phase 4: Future Enhancements
13. **Claim History & Audit Trail** (1.4) - Compliance
14. **Scheduled Bulk Processing** (2.9) - Automation
15. **Enhanced Sorting** (1.5) - Power user features

---

## Technical Implementation Notes

### Database Changes Needed
```python
# Add indexes for filtering
class Claim(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status', '-queried_at']),
            models.Index(fields=['organization', 'provider', '-service_date']),
            models.Index(fields=['organization', '-payment_amount']),
        ]

# Add status history tracking
class ClaimStatusHistory(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=50, null=True)
    new_status = models.CharField(max_length=50)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

# Add failed row tracking for CSVJob
class CSVJobFailedRow(models.Model):
    job = models.ForeignKey(CSVJob, on_delete=models.CASCADE, related_name='failed_rows')
    row_number = models.IntegerField()
    row_data = models.JSONField()
    error_type = models.CharField(max_length=50)
    error_message = models.TextField()
    error_code = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### New Serializers Needed
```python
# ClaimFilterSerializer - for advanced filtering
# ClaimExportSerializer - for CSV/Excel export
# CSVPreviewSerializer - for upload preview
# CSVJobProgressSerializer - for real-time updates
# ClaimStatsSerializer - for aggregate statistics
```

### Celery Tasks to Implement
```python
# tasks.py
@shared_task(bind=True)
def process_csv_file_with_progress(self, job_id):
    """Process CSV with progress updates"""
    # Implement actual processing
    # Update job progress in real-time
    # Handle partial failures
    
@shared_task
def bulk_refresh_claims(claim_ids):
    """Refresh multiple claims in background"""
    
@shared_task
def generate_export_file(filter_params, format):
    """Generate export file asynchronously"""
```

### API Endpoints to Add
```python
# urls.py additions
router.register(r'claims', ClaimViewSet, basename='claim')

# Additional claim endpoints
path('claims/stats/', ClaimStatsView.as_view()),
path('claims/export/', ClaimExportView.as_view()),
path('claims/<uuid:pk>/history/', ClaimHistoryView.as_view()),

# Enhanced bulk upload endpoints
path('upload/template/', CSVTemplateView.as_view()),
path('upload/preview/', CSVPreviewView.as_view()),
path('jobs/<uuid:pk>/retry_failed/', CSVJobRetryView.as_view()),
path('jobs/<uuid:pk>/errors/', CSVJobErrorsView.as_view()),
path('jobs/<uuid:pk>/progress/', CSVJobProgressView.as_view()),  # WebSocket
```

---

## Testing Strategy

### Unit Tests
- Filter combinations
- Export formats
- Validation logic
- Duplicate detection
- Error handling

### Integration Tests
- Full CSV upload flow
- Partial failure scenarios
- Bulk refresh operations
- Export generation

### Performance Tests
- Large CSV files (10K+ rows)
- Concurrent uploads
- Filter query performance
- Export generation time

---

## Security Considerations

1. **PHI Protection**
   - Ensure all exports maintain encryption
   - Audit log for all data access
   - Rate limiting on bulk operations

2. **File Upload Security**
   - Validate file types and sizes
   - Scan for malicious content
   - Limit concurrent uploads per user

3. **API Rate Limiting**
   - Prevent abuse of bulk operations
   - Throttle export requests
   - Monitor for unusual patterns

---

## User Experience Improvements

1. **Progress Indicators**
   - Show upload progress
   - Display processing status
   - Estimate completion time

2. **Error Messages**
   - Clear, actionable errors
   - Suggestions for fixes
   - Links to documentation

3. **Bulk Operations**
   - Confirm before large operations
   - Allow cancellation
   - Provide rollback options

---

## Questions for Discussion

1. **Real-Time Updates**: WebSocket vs. Server-Sent Events vs. Polling?
2. **Export Limits**: Max rows per export? Async for large exports?
3. **Duplicate Strategy**: Default behavior (skip/update/error)?
4. **Batch Size**: Default and max batch sizes?
5. **Retention**: How long to keep failed row details?
6. **Notifications**: Email/SMS for completed jobs?

---

**Ready to start implementation?** Let me know which phase or specific feature you'd like to tackle first!

