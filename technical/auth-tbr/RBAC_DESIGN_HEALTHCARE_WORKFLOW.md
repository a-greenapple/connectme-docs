# 🏥 Healthcare Claims Workflow - Complete RBAC Design

## Executive Summary

**Purpose:** Single interface aggregating claims, eligibility, and care cost data from multiple systems (UHC, Availity, eCW, Tebra) with workflow management, query throttling, and team collaboration.

**Key Features:**
- Query history & 24-hour cache with approval workflow
- Internal work annotations (callbacks, follow-ups, notes)
- Team-based visibility and management
- Jira integration for KPIs and throughput tracking
- HIPAA-compliant audit logging

---

## 🎯 Role Architecture

### Hierarchy Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         ADMIN                                │
│  Full system access, tenant management, policy overrides    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌────────▼────────┐
│   TEAM_LEAD    │  │   AUDITOR   │  │ SYSTEM_INTEGRATION│
│ Team oversight │  │ Compliance  │  │ Service accounts │
└───────┬────────┘  └─────────────┘  └─────────────────┘
        │
┌───────▼────────┐
│    ANALYST     │
│ Core workflow  │
└───────┬────────┘
        │
┌───────▼────────┐
│   READ_ONLY    │
│ View dashboards│
└────────────────┘
```

---

## 🔐 Keycloak Role Structure

### 1. Realm Roles (Global Permissions)

#### **admin**
- **Description:** System administrator with full access
- **Composite of:**
  - All client roles
  - rbac:manage
  - policy:manage
  - tenant:manage
  - requery:approve
  - history:purge
- **Use cases:**
  - Manage users, teams, and roles
  - Override re-query policies
  - Configure system settings
  - Manage tenant configurations

#### **team_lead**
- **Description:** Team leader with oversight and approval authority
- **Composite of:**
  - claims:read
  - claims:detail
  - claims:export
  - eligibility:read
  - reports:generate
  - reports:view
  - work:annotate
  - work:assign
  - work:view_team
  - history:view
  - requery:request
  - requery:approve
- **Use cases:**
  - View all team member work
  - Approve re-queries within 24 hours
  - Assign work items
  - Generate team reports
  - Monitor team KPIs

#### **analyst**
- **Description:** Core user role for claims processing and workflow
- **Composite of:**
  - claims:read
  - claims:detail
  - claims:export
  - eligibility:read
  - reports:view
  - work:annotate
  - work:view_own
  - history:view_own
  - requery:request
- **Use cases:**
  - Query claims and eligibility (respecting cache)
  - Add internal notes and annotations
  - View own work items
  - Request re-query approval
  - Export data for analysis

#### **read_only**
- **Description:** View-only access to dashboards and cached data
- **Composite of:**
  - claims:read
  - eligibility:read
  - reports:view
  - work:view_own
- **Use cases:**
  - View cached results
  - Access dashboards
  - No re-query capability
  - No data modifications

#### **auditor**
- **Description:** Compliance and audit role
- **Composite of:**
  - history:view
  - reports:view
  - audit:view
  - logs:view
- **Use cases:**
  - Review audit logs
  - Access query history
  - Generate compliance reports
  - No PHI modifications

#### **system_integration**
- **Description:** Service account for automated processes
- **Composite of:**
  - claims:read
  - eligibility:read
  - work:create
  - jira:sync
  - webhook:receive
- **Use cases:**
  - Scheduled data refreshes
  - Jira synchronization
  - Webhook processing
  - Automated reporting

---

### 2. Client Roles (Fine-Grained Permissions)

Create these under client: **connectme-frontend**

#### **Claims Module**
```
claims:read              - View claims summary data
claims:detail            - View detailed claim information
claims:export            - Export claims data to CSV/Excel
claims:search            - Search claims by various criteria
claims:bulk              - Bulk query operations
```

#### **Eligibility Module**
```
eligibility:read         - View eligibility status
eligibility:detail       - View detailed eligibility info
eligibility:verify       - Initiate eligibility verification
eligibility:export       - Export eligibility data
```

#### **Cost Estimation Module** (Future)
```
cost:estimate            - Generate cost estimates
cost:view                - View cost estimation data
cost:export              - Export cost data
```

#### **Reporting Module**
```
reports:view             - View existing reports
reports:generate         - Generate new reports
reports:schedule         - Schedule automated reports
reports:export           - Export report data
reports:share            - Share reports with team
```

#### **Workflow Management**
```
work:view_own            - View own work items
work:view_team           - View team work items
work:annotate            - Add notes/annotations
work:assign              - Assign work to team members
work:create              - Create new work items
work:close               - Close/complete work items
work:reopen              - Reopen closed work items
```

#### **Jira Integration**
```
jira:sync                - Synchronize with Jira
jira:create              - Create Jira tickets
jira:update              - Update Jira tickets
jira:view                - View Jira integration status
```

#### **Query History & Governance**
```
history:view_own         - View own query history
history:view_team        - View team query history
history:view             - View all query history
history:purge            - Purge old query data
requery:request          - Request re-query approval
requery:approve          - Approve re-query requests
requery:override         - Override cache policy (admin)
```

#### **Audit & Compliance**
```
audit:view               - View audit logs
audit:export             - Export audit data
logs:view                - View system logs
logs:export              - Export log data
```

#### **Administration**
```
rbac:manage              - Manage roles and permissions
policy:manage            - Manage system policies
tenant:manage            - Manage tenant configurations
team:manage              - Manage teams
user:manage              - Manage users
```

---

## 👥 Keycloak Groups (Team Structure)

### Group Hierarchy

```
/teams
  /team:RCM-East
    - Attributes: region=east, payer_scope=UHC,Availity
  /team:RCM-West
    - Attributes: region=west, payer_scope=UHC
  /team:Eligibility
    - Attributes: specialty=eligibility
  /team:Billing
    - Attributes: specialty=billing, payer_scope=UHC,Availity,Aetna

/facilities
  /facility:Hospital-A
    - Attributes: tin=123456789, npi=1234567890
  /facility:Clinic-B
    - Attributes: tin=987654321, npi=0987654321
```

### Group Attributes

Each group can have custom attributes for policy enforcement:

```json
{
  "region": "east",
  "payer_scope": ["UHC", "Availity"],
  "tin_scope": ["123456789", "987654321"],
  "facility_scope": ["Hospital-A", "Clinic-B"],
  "max_daily_queries": "100",
  "cache_override_allowed": "false"
}
```

---

## 🔒 User Attributes (Policy Enforcement)

Add these custom attributes to users:

```json
{
  "payer_scope": ["UHC", "Availity"],
  "tin_scope": ["123456789"],
  "facility_scope": ["Hospital-A"],
  "region": "east",
  "team": "RCM-East",
  "max_queries_per_day": "50",
  "requires_requery_approval": "true",
  "phi_access_level": "full"
}
```

These attributes will be included in JWT tokens for backend policy enforcement.

---

## 📋 Permission Matrix

| Role | Claims Read | Claims Detail | Eligibility | Reports Gen | Work Annotate | Team View | Requery Approve | Admin |
|------|------------|---------------|-------------|-------------|---------------|-----------|-----------------|-------|
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **team_lead** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **analyst** | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **read_only** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **auditor** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **system_integration** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 🔐 Policy Implementation

### 1. Re-Query Policy (24-Hour Cache)

**Backend Implementation:**

```python
# apps/claims/policies.py

from datetime import datetime, timedelta
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied

class RequeryPolicy:
    CACHE_DURATION = timedelta(hours=24)
    
    def can_requery(self, user, claim_number):
        """Check if user can re-query a claim"""
        cache_key = f"claim_query:{claim_number}:{user.organization_id}"
        last_query = cache.get(cache_key)
        
        if not last_query:
            # First query, allow it
            return True, None
        
        time_since_query = datetime.now() - last_query
        
        if time_since_query < self.CACHE_DURATION:
            # Within 24 hours, check permissions
            if self.has_requery_approval(user):
                return True, "Approved by admin/TL"
            else:
                # Check if there's a pending approval
                approval = RequeryApproval.objects.filter(
                    claim_number=claim_number,
                    requested_by=user,
                    status='approved',
                    created_at__gte=last_query
                ).first()
                
                if approval:
                    return True, f"Approved by {approval.approved_by.username}"
                else:
                    return False, f"Last queried {time_since_query.seconds // 3600}h ago. Request approval."
        
        # More than 24 hours, allow re-query
        return True, None
    
    def has_requery_approval(self, user):
        """Check if user has requery:approve permission"""
        return 'requery:approve' in user.roles or 'admin' in user.roles
    
    def record_query(self, user, claim_number):
        """Record query timestamp"""
        cache_key = f"claim_query:{claim_number}:{user.organization_id}"
        cache.set(cache_key, datetime.now(), timeout=86400)  # 24 hours
```

**Frontend Implementation:**

```typescript
// src/lib/policies/requeryPolicy.ts

export interface RequeryCheckResult {
  allowed: boolean;
  reason?: string;
  lastQueryTime?: Date;
  requiresApproval: boolean;
}

export async function checkRequeryPermission(
  claimNumber: string
): Promise<RequeryCheckResult> {
  const response = await apiClient.post('/claims/check-requery/', {
    claim_number: claimNumber
  });
  
  return response.data;
}

export async function requestRequeryApproval(
  claimNumber: string,
  reason: string
): Promise<void> {
  await apiClient.post('/claims/request-requery-approval/', {
    claim_number: claimNumber,
    reason: reason
  });
}
```

### 2. Attribute-Based Access Control (ABAC)

**Backend Policy Enforcement:**

```python
# apps/core/policies.py

class ABACPolicy:
    def can_access_payer(self, user, payer_id):
        """Check if user can access data for this payer"""
        user_payers = user.attributes.get('payer_scope', [])
        return payer_id in user_payers or 'admin' in user.roles
    
    def can_access_tin(self, user, tin):
        """Check if user can access data for this TIN"""
        user_tins = user.attributes.get('tin_scope', [])
        return tin in user_tins or 'admin' in user.roles
    
    def can_access_facility(self, user, facility_id):
        """Check if user can access this facility"""
        user_facilities = user.attributes.get('facility_scope', [])
        return facility_id in user_facilities or 'admin' in user.roles
    
    def enforce_data_filter(self, user, queryset):
        """Filter queryset based on user attributes"""
        if 'admin' in user.roles:
            return queryset
        
        # Filter by payer scope
        payer_scope = user.attributes.get('payer_scope', [])
        if payer_scope:
            queryset = queryset.filter(payer_id__in=payer_scope)
        
        # Filter by TIN scope
        tin_scope = user.attributes.get('tin_scope', [])
        if tin_scope:
            queryset = queryset.filter(tin__in=tin_scope)
        
        # Filter by team
        if 'work:view_team' in user.roles:
            queryset = queryset.filter(
                Q(assigned_to=user) | Q(assigned_to__team=user.team)
            )
        elif 'work:view_own' in user.roles:
            queryset = queryset.filter(assigned_to=user)
        
        return queryset
```

### 3. Query Throttling

```python
# apps/claims/throttling.py

from rest_framework.throttling import UserRateThrottle

class DailyQueryThrottle(UserRateThrottle):
    def get_rate(self):
        """Get rate from user attributes or default"""
        user = self.request.user
        max_queries = user.attributes.get('max_queries_per_day', 50)
        return f'{max_queries}/day'
    
    def get_cache_key(self, request, view):
        """Cache key per user per day"""
        user_id = request.user.id
        date = datetime.now().strftime('%Y-%m-%d')
        return f'throttle_query:{user_id}:{date}'
```

---

## 📊 Database Schema Extensions

### 1. Query History Table

```python
# apps/claims/models.py

class QueryHistory(models.Model):
    """Track all queries for audit and cache management"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    # Query details
    query_type = models.CharField(max_length=50)  # 'claim', 'eligibility', 'cost'
    resource_id = models.CharField(max_length=255)  # claim_number, member_id, etc.
    provider = models.CharField(max_length=50)  # 'UHC', 'Availity', etc.
    
    # Cache management
    cached_result = models.BooleanField(default=False)
    cache_hit = models.BooleanField(default=False)
    
    # Approval workflow
    required_approval = models.BooleanField(default=False)
    approval_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')],
        null=True
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='approved_queries'
    )
    approved_at = models.DateTimeField(null=True)
    
    # Metadata
    query_params = models.JSONField()
    response_summary = models.JSONField(null=True)
    execution_time_ms = models.IntegerField()
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    # Retention
    purge_after = models.DateTimeField()
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['organization', '-created_at']),
            models.Index(fields=['resource_id', '-created_at']),
            models.Index(fields=['purge_after']),
        ]
```

### 2. Work Item / Workflow Table

```python
# apps/workflow/models.py

class WorkItem(models.Model):
    """Internal workflow tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    # Work item details
    title = models.CharField(max_length=255)
    description = models.TextField()
    work_type = models.CharField(
        max_length=50,
        choices=[
            ('callback', 'Patient Callback'),
            ('follow_up', 'Follow-up Required'),
            ('denial', 'Denial Review'),
            ('appeal', 'Appeal Processing'),
            ('verification', 'Eligibility Verification'),
            ('other', 'Other')
        ]
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_work'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='delegated_work'
    )
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('waiting', 'Waiting'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )
    priority = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')],
        default='medium'
    )
    
    # Related data
    claim_number = models.CharField(max_length=255, null=True, blank=True)
    patient_name = models.CharField(max_length=255)
    patient_dob = models.DateField()
    payer = models.CharField(max_length=100)
    
    # Workflow metadata
    notes = models.JSONField(default=list)  # Array of note objects
    attachments = models.JSONField(default=list)
    tags = ArrayField(models.CharField(max_length=50), default=list)
    
    # Jira integration
    jira_ticket_id = models.CharField(max_length=50, null=True, blank=True)
    jira_sync_status = models.CharField(max_length=20, default='pending')
    jira_last_sync = models.DateTimeField(null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    
    # Audit
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_work'
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['assigned_to', 'status', '-created_at']),
            models.Index(fields=['team', 'status', '-created_at']),
            models.Index(fields=['claim_number']),
            models.Index(fields=['jira_ticket_id']),
        ]


class WorkItemNote(models.Model):
    """Notes/annotations on work items"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE, related_name='work_notes')
    
    content = models.TextField()
    note_type = models.CharField(
        max_length=50,
        choices=[
            ('comment', 'Comment'),
            ('callback', 'Callback Note'),
            ('resolution', 'Resolution'),
            ('escalation', 'Escalation'),
        ]
    )
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # PHI flag for audit
    contains_phi = models.BooleanField(default=False)
```

### 3. Re-Query Approval Table

```python
# apps/claims/models.py

class RequeryApproval(models.Model):
    """Track re-query approval requests"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    # Request details
    claim_number = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50)  # 'claim', 'eligibility'
    reason = models.TextField()
    
    # Requestor
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requery_requests'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    
    # Approval
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('denied', 'Denied'),
            ('expired', 'Expired')
        ],
        default='pending'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_requeries'
    )
    approved_at = models.DateTimeField(null=True)
    approval_notes = models.TextField(blank=True)
    
    # Expiration
    expires_at = models.DateTimeField()
    
    # Audit
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=['requested_by', 'status', '-requested_at']),
            models.Index(fields=['status', 'expires_at']),
        ]
```

### 4. Team Management

```python
# apps/users/models.py

class Team(models.Model):
    """Team/group management"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)  # 'RCM-East', 'RCM-West'
    description = models.TextField(blank=True)
    
    # Team lead
    team_lead = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_teams'
    )
    
    # Attributes for ABAC
    payer_scope = ArrayField(models.CharField(max_length=50), default=list)
    tin_scope = ArrayField(models.CharField(max_length=15), default=list)
    facility_scope = ArrayField(models.CharField(max_length=100), default=list)
    region = models.CharField(max_length=50, blank=True)
    
    # Limits
    max_daily_queries = models.IntegerField(default=100)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Add to User model
class User(AbstractUser):
    # ... existing fields ...
    
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name='members'
    )
    
    # User attributes for ABAC
    payer_scope = ArrayField(models.CharField(max_length=50), default=list)
    tin_scope = ArrayField(models.CharField(max_length=15), default=list)
    facility_scope = ArrayField(models.CharField(max_length=100), default=list)
    max_queries_per_day = models.IntegerField(default=50)
    phi_access_level = models.CharField(
        max_length=20,
        choices=[('none', 'None'), ('limited', 'Limited'), ('full', 'Full')],
        default='full'
    )
```

---

## 🔄 Jira Integration Schema

```python
# apps/integrations/models.py

class JiraConfig(models.Model):
    """Jira integration configuration per organization"""
    
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    
    jira_url = models.URLField()
    jira_project_key = models.CharField(max_length=50)
    jira_api_token_encrypted = models.BinaryField()
    jira_username = models.CharField(max_length=255)
    
    # Sync settings
    sync_enabled = models.BooleanField(default=True)
    sync_interval_minutes = models.IntegerField(default=15)
    last_sync = models.DateTimeField(null=True)
    
    # Field mappings
    field_mappings = models.JSONField(default=dict)
    # Example:
    # {
    #   "work_type": "customfield_10001",
    #   "claim_number": "customfield_10002",
    #   "payer": "customfield_10003"
    # }
    
    is_active = models.BooleanField(default=True)


class JiraSyncLog(models.Model):
    """Track Jira synchronization"""
    
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    jira_ticket_id = models.CharField(max_length=50)
    
    sync_type = models.CharField(
        max_length=20,
        choices=[('create', 'Create'), ('update', 'Update'), ('status', 'Status Change')]
    )
    sync_status = models.CharField(
        max_length=20,
        choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')]
    )
    error_message = models.TextField(blank=True)
    
    synced_at = models.DateTimeField(auto_now_add=True)
    synced_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

---

## 📈 KPI & Metrics Tables

```python
# apps/analytics/models.py

class UserMetrics(models.Model):
    """Daily user performance metrics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Query metrics
    total_queries = models.IntegerField(default=0)
    cache_hits = models.IntegerField(default=0)
    cache_misses = models.IntegerField(default=0)
    requery_requests = models.IntegerField(default=0)
    
    # Work item metrics
    work_items_created = models.IntegerField(default=0)
    work_items_completed = models.IntegerField(default=0)
    work_items_assigned = models.IntegerField(default=0)
    
    # Time metrics
    avg_response_time_ms = models.IntegerField(default=0)
    total_active_time_minutes = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]


class TeamMetrics(models.Model):
    """Daily team performance metrics"""
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    
    # Throughput
    total_queries = models.IntegerField(default=0)
    work_items_completed = models.IntegerField(default=0)
    avg_completion_time_hours = models.FloatField(default=0)
    
    # Quality
    requery_rate = models.FloatField(default=0)  # Percentage
    approval_rate = models.FloatField(default=0)
    
    # Jira sync
    jira_tickets_created = models.IntegerField(default=0)
    jira_sync_failures = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['team', 'date']
```

---

## 🎯 Implementation Checklist

### Phase 1: Keycloak Setup (Week 1)
- [ ] Create all realm roles
- [ ] Create all client roles
- [ ] Set up composite role relationships
- [ ] Create team groups with attributes
- [ ] Configure user attributes
- [ ] Test role assignments

### Phase 2: Database Schema (Week 1-2)
- [ ] Create QueryHistory model
- [ ] Create WorkItem and WorkItemNote models
- [ ] Create RequeryApproval model
- [ ] Create Team model
- [ ] Update User model with attributes
- [ ] Create Jira integration models
- [ ] Create metrics models
- [ ] Run migrations

### Phase 3: Backend Policies (Week 2-3)
- [ ] Implement RequeryPolicy
- [ ] Implement ABACPolicy
- [ ] Implement query throttling
- [ ] Add permission decorators to views
- [ ] Implement approval workflow API
- [ ] Add audit logging middleware

### Phase 4: Frontend Integration (Week 3-4)
- [ ] Update AuthContext to include roles/attributes
- [ ] Implement permission-based UI rendering
- [ ] Add re-query approval request UI
- [ ] Build work item dashboard
- [ ] Add team view for team leads
- [ ] Implement approval workflow UI

### Phase 5: Jira Integration (Week 4-5)
- [ ] Implement Jira API client
- [ ] Build sync service
- [ ] Add webhook handlers
- [ ] Implement field mapping
- [ ] Add sync monitoring

### Phase 6: Analytics & KPIs (Week 5-6)
- [ ] Implement metrics collection
- [ ] Build KPI dashboard
- [ ] Add team performance reports
- [ ] Implement query analytics
- [ ] Add compliance reports

---

## 📚 Next Steps

I'll now create:
1. Updated Keycloak realm export with all new roles
2. Django models for all tables
3. Policy implementation code
4. API endpoints for approval workflow
5. Frontend components for work management
6. Jira integration service
7. Metrics and KPI tracking

**Ready to proceed?** Let me know if you'd like me to generate any of these components!
