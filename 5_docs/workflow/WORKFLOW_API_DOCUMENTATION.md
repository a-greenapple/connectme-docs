# 🔄 Workflow Management API Documentation

## Overview

Complete REST API for healthcare workflow management, including work items, teams, query history, and re-query approval workflow.

**Base URL:** `http://localhost:8000/api/v1/workflow/`

**Authentication:** All endpoints require JWT token from Keycloak

---

## 📋 Table of Contents

1. [Team Management](#team-management)
2. [Work Item Management](#work-item-management)
3. [Query History](#query-history)
4. [Re-Query Approval Workflow](#re-query-approval-workflow)
5. [Dashboard & Statistics](#dashboard--statistics)
6. [Query Limits](#query-limits)

---

## 🏢 Team Management

### List Teams

```http
GET /api/v1/workflow/teams/
```

**Query Parameters:**
- `is_active` (boolean): Filter by active status

**Response:**
```json
[
  {
    "id": "uuid",
    "organization": "uuid",
    "name": "RCM East Team",
    "code": "RCM-East",
    "description": "Revenue Cycle Management - East Region",
    "team_lead": "uuid",
    "team_lead_name": "John Doe",
    "payer_scope": ["UHC", "Availity"],
    "tin_scope": ["854203105"],
    "facility_scope": [],
    "region": "east",
    "max_daily_queries": 100,
    "is_active": true,
    "member_count": 5,
    "active_work_count": 12,
    "created_at": "2024-10-04T10:00:00Z",
    "updated_at": "2024-10-04T10:00:00Z"
  }
]
```

### Get Team Details

```http
GET /api/v1/workflow/teams/{id}/
```

### Get Team Members

```http
GET /api/v1/workflow/teams/{id}/members/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "username": "analyst1",
    "email": "analyst1@example.com",
    "full_name": "Jane Smith",
    "role": "analyst"
  }
]
```

### Get Team Work Items

```http
GET /api/v1/workflow/teams/{id}/work_items/
```

**Query Parameters:**
- `status` (string): Filter by status (new, in_progress, waiting, completed, cancelled)

---

## 📝 Work Item Management

### List Work Items

```http
GET /api/v1/workflow/work-items/
```

**Query Parameters:**
- `status` (string): Filter by status
- `priority` (string): Filter by priority (low, medium, high, urgent)
- `work_type` (string): Filter by type (callback, follow_up, denial, appeal, etc.)
- `assigned_to` (string): Filter by assignee (`me` for current user, or user ID)
- `team` (uuid): Filter by team
- `overdue` (boolean): Filter overdue items

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Follow up on denied claim",
    "work_type": "denial",
    "status": "new",
    "priority": "high",
    "assigned_to": "uuid",
    "assigned_to_name": "Jane Smith",
    "team": "uuid",
    "team_name": "RCM East Team",
    "claim_number": "CLM123456",
    "patient_name": "John Doe",
    "payer": "UHC",
    "due_date": "2024-10-07T00:00:00Z",
    "created_at": "2024-10-04T10:00:00Z",
    "age_hours": 48,
    "is_overdue": false,
    "note_count": 3,
    "jira_ticket_id": "CONN-123"
  }
]
```

### Get Work Item Details

```http
GET /api/v1/workflow/work-items/{id}/
```

**Response includes nested notes and attachments:**
```json
{
  "id": "uuid",
  "organization": "uuid",
  "team": "uuid",
  "team_name": "RCM East Team",
  "title": "Follow up on denied claim",
  "description": "Claim denied due to missing documentation",
  "work_type": "denial",
  "status": "new",
  "priority": "high",
  "assigned_to": "uuid",
  "assigned_to_name": "Jane Smith",
  "assigned_by": "uuid",
  "assigned_by_name": "Team Lead",
  "claim_number": "CLM123456",
  "patient_name": "John Doe",
  "patient_dob": "1980-01-01",
  "payer": "UHC",
  "tin": "854203105",
  "tags": ["denial", "urgent", "documentation"],
  "jira_ticket_id": "CONN-123",
  "jira_sync_status": "synced",
  "jira_last_sync": "2024-10-04T10:00:00Z",
  "created_at": "2024-10-04T10:00:00Z",
  "updated_at": "2024-10-04T10:00:00Z",
  "due_date": "2024-10-07T00:00:00Z",
  "completed_at": null,
  "created_by": "uuid",
  "created_by_name": "Team Lead",
  "age_hours": 48,
  "is_overdue": false,
  "notes": [
    {
      "id": "uuid",
      "content": "Contacted provider for documentation",
      "note_type": "comment",
      "created_by": "uuid",
      "created_by_name": "Jane Smith",
      "created_at": "2024-10-04T11:00:00Z",
      "contains_phi": false
    }
  ],
  "attachments": []
}
```

### Create Work Item

```http
POST /api/v1/workflow/work-items/
```

**Request Body:**
```json
{
  "team": "uuid",
  "title": "Patient callback required",
  "description": "Patient needs to provide additional insurance information",
  "work_type": "callback",
  "status": "new",
  "priority": "medium",
  "assigned_to": "uuid",
  "claim_number": "CLM789012",
  "patient_name": "Jane Smith",
  "patient_dob": "1975-05-15",
  "payer": "Availity",
  "tin": "854203105",
  "tags": ["callback", "insurance"],
  "due_date": "2024-10-05T00:00:00Z"
}
```

### Update Work Item

```http
PATCH /api/v1/workflow/work-items/{id}/
```

### Add Note to Work Item

```http
POST /api/v1/workflow/work-items/{id}/add_note/
```

**Request Body:**
```json
{
  "content": "Called patient, left voicemail",
  "note_type": "callback",
  "contains_phi": false
}
```

### Assign Work Item

```http
POST /api/v1/workflow/work-items/{id}/assign/
```

**Request Body:**
```json
{
  "user_id": "uuid"
}
```

### Change Work Item Status

```http
POST /api/v1/workflow/work-items/{id}/change_status/
```

**Request Body:**
```json
{
  "status": "in_progress"
}
```

---

## 📊 Query History

### List Query History

```http
GET /api/v1/workflow/query-history/
```

**Query Parameters:**
- `query_type` (string): Filter by type (claim, eligibility, cost, bulk)
- `provider` (string): Filter by provider (UHC, Availity)
- `user` (string): Filter by user (`me` for current user, or user ID)
- `date_from` (datetime): Filter from date
- `date_to` (datetime): Filter to date

**Response:**
```json
[
  {
    "id": "uuid",
    "user": "uuid",
    "user_name": "Jane Smith",
    "organization": "uuid",
    "query_type": "claim",
    "resource_id": "CLM123456",
    "provider": "UHC",
    "cached_result": true,
    "cache_hit": false,
    "required_approval": false,
    "approval_status": null,
    "approved_by": null,
    "approved_by_name": null,
    "approved_at": null,
    "query_params": {
      "claim_number": "CLM123456",
      "patient_ssn": "***-**-3333",
      "patient_dob": "1980-01-01"
    },
    "response_summary": {
      "status": "PAID",
      "amount": 1200.00
    },
    "execution_time_ms": 250,
    "created_at": "2024-10-04T10:00:00Z",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "purge_after": "2026-10-04T10:00:00Z"
  }
]
```

### Get Query Statistics

```http
GET /api/v1/workflow/query-history/stats/
```

**Response:**
```json
{
  "total_queries": 1250,
  "today_queries": 45,
  "cache_hit_rate": 67.5,
  "avg_execution_time_ms": 320,
  "by_provider": [
    {
      "provider": "UHC",
      "count": 800
    },
    {
      "provider": "Availity",
      "count": 450
    }
  ],
  "by_query_type": [
    {
      "query_type": "claim",
      "count": 950
    },
    {
      "query_type": "eligibility",
      "count": 300
    }
  ]
}
```

---

## ✅ Re-Query Approval Workflow

### List Approval Requests

```http
GET /api/v1/workflow/requery-approvals/
```

**Query Parameters:**
- `status` (string): Filter by status (pending, approved, denied, expired)

**Response:**
```json
[
  {
    "id": "uuid",
    "claim_number": "CLM123456",
    "resource_type": "claim",
    "reason": "Patient called with updated information",
    "requested_by": "uuid",
    "requested_by_name": "Jane Smith",
    "requested_at": "2024-10-04T10:00:00Z",
    "status": "pending",
    "approved_by": null,
    "approved_by_name": null,
    "approved_at": null,
    "approval_notes": "",
    "expires_at": "2024-10-05T10:00:00Z",
    "is_expired": false,
    "organization": "uuid"
  }
]
```

### Get Pending Approvals

```http
GET /api/v1/workflow/requery-approvals/pending/
```

Returns only pending approvals for current user's team (team leads) or all (admins).

### Request Re-Query Approval

```http
POST /api/v1/workflow/request-requery/
```

**Request Body:**
```json
{
  "resource_type": "claim",
  "resource_id": "CLM123456",
  "reason": "Patient called with updated insurance information"
}
```

**Response:**
```json
{
  "id": "uuid",
  "claim_number": "CLM123456",
  "resource_type": "claim",
  "reason": "Patient called with updated insurance information",
  "requested_by": "uuid",
  "requested_by_name": "Jane Smith",
  "requested_at": "2024-10-04T10:00:00Z",
  "status": "pending",
  "expires_at": "2024-10-05T10:00:00Z",
  "is_expired": false
}
```

### Check Re-Query Permission

```http
POST /api/v1/workflow/check-requery/
```

**Request Body:**
```json
{
  "resource_type": "claim",
  "resource_id": "CLM123456"
}
```

**Response:**
```json
{
  "allowed": false,
  "reason": "Last queried 2h ago. Wait 22h or request approval."
}
```

### Approve Re-Query Request

```http
POST /api/v1/workflow/requery-approvals/{id}/approve/
```

**Requires:** `requery:approve` role or `admin`

**Request Body:**
```json
{
  "approval_notes": "Approved - patient has new insurance card"
}
```

### Deny Re-Query Request

```http
POST /api/v1/workflow/requery-approvals/{id}/deny/
```

**Requires:** `requery:approve` role or `admin`

**Request Body:**
```json
{
  "approval_notes": "Denied - insufficient reason provided"
}
```

---

## 📈 Dashboard & Statistics

### Get Dashboard Stats

```http
GET /api/v1/workflow/dashboard/
```

**Response:**
```json
{
  "my_work_items": 5,
  "team_work_items": 12,
  "pending_approvals": 3,
  "queries_today": 15,
  "queries_remaining": 35,
  "overdue_items": 1
}
```

### Get My Work Items

```http
GET /api/v1/workflow/dashboard/my-work/
```

**Query Parameters:**
- `status` (string): Filter by status (default: active items only)

Returns work items assigned to current user.

### Get Team Work Items

```http
GET /api/v1/workflow/dashboard/team-work/
```

**Query Parameters:**
- `status` (string): Filter by status (default: active items only)

Returns work items for current user's team (requires team membership).

---

## 🔢 Query Limits

### Get Query Limits

```http
GET /api/v1/workflow/query-limits/
```

**Response:**
```json
{
  "user": {
    "used": 15,
    "limit": 50,
    "remaining": 35,
    "allowed": true
  },
  "team": {
    "used": 45,
    "limit": 100,
    "remaining": 55,
    "allowed": true
  }
}
```

---

## 🔐 Authentication

All endpoints require JWT authentication from Keycloak.

**Header:**
```
Authorization: Bearer <jwt_token>
```

**Roles Required:**

| Endpoint | Minimum Role |
|----------|-------------|
| GET /teams/ | Any authenticated user |
| POST /teams/ | `admin` or `team_lead` |
| GET /work-items/ | `work:view_own` or `work:view_team` |
| POST /work-items/ | `work:create` |
| GET /query-history/ | `history:view_own`, `history:view_team`, or `history:view` |
| POST /requery-approvals/ | `requery:request` |
| POST /requery-approvals/{id}/approve/ | `requery:approve` or `admin` |
| GET /dashboard/ | Any authenticated user |

---

## 📝 Error Responses

### 400 Bad Request
```json
{
  "error": "status is required"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 429 Too Many Requests
```json
{
  "detail": "Daily query limit exceeded (50/50). Resets at midnight."
}
```

---

## 🧪 Testing the API

### Using cURL

```bash
# Get dashboard stats
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/workflow/dashboard/

# List my work items
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/workflow/dashboard/my-work/

# Create work item
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "team": "team-uuid",
    "title": "Test work item",
    "description": "Test description",
    "work_type": "callback",
    "status": "new",
    "priority": "medium",
    "patient_name": "Test Patient",
    "patient_dob": "1980-01-01",
    "payer": "UHC"
  }' \
  http://localhost:8000/api/v1/workflow/work-items/

# Check re-query permission
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "claim",
    "resource_id": "CLM123456"
  }' \
  http://localhost:8000/api/v1/workflow/check-requery/
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/workflow"
TOKEN = "your-jwt-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Get dashboard
response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
print(response.json())

# List work items
response = requests.get(
    f"{BASE_URL}/work-items/",
    headers=headers,
    params={"status": "new", "assigned_to": "me"}
)
print(response.json())

# Request re-query approval
response = requests.post(
    f"{BASE_URL}/request-requery/",
    headers=headers,
    json={
        "resource_type": "claim",
        "resource_id": "CLM123456",
        "reason": "Patient provided updated information"
    }
)
print(response.json())
```

---

## 📚 Additional Resources

- **RBAC Design:** See `RBAC_DESIGN_HEALTHCARE_WORKFLOW.md`
- **Keycloak Setup:** See `KEYCLOAK_COMPOSITE_ROLES_GUIDE.md`
- **Policy Implementation:** See `backend/apps/workflow/policies.py`
- **Models:** See `backend/apps/workflow/models.py`

---

## 🎯 Next Steps

1. **Test with Postman/Insomnia:** Import the API endpoints
2. **Integrate with Frontend:** Use these endpoints in React components
3. **Set up Keycloak:** Configure roles and test authentication
4. **Monitor Usage:** Check Django admin for work items and query history

---

**Last Updated:** October 4, 2024
**API Version:** 1.0
**Base URL:** `http://localhost:8000/api/v1/workflow/`
