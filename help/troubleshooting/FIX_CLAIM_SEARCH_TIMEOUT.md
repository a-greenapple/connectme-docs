# Fix Claim Search Timeout Issue

## 🔴 Problem
```
timeout of 30000ms exceeded
code: "ECONNABORTED"
```

Claim search is failing because:
1. Frontend timeout: **30 seconds**
2. Backend processing time: **30-60 seconds** (for 12 claims with external API calls)
3. Backend timeout: 120 seconds ✅

## 🎯 Root Cause

The backend is making **sequential API calls** to UHC:
- For each claim: 1 Details API call + 1 Payment API call
- For 12 claims: 24 API calls sequentially
- Each API call takes 1-2 seconds
- Total time: 30-60 seconds

The frontend times out at 30 seconds before the backend finishes.

## ✅ Solutions

### Solution 1: Increase Frontend Timeout (QUICK FIX)

Update the Axios timeout in the frontend:

**File:** `connectme-frontend/src/lib/api.ts` (or wherever Axios is configured)

```typescript
// Current (30 seconds)
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30000, // ❌ Too short
  withCredentials: true,
});

// Change to (120 seconds to match backend)
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 120000, // ✅ 120 seconds
  withCredentials: true,
});
```

**Or for claim search specifically:**

```typescript
// In the claim search function
const response = await api.post('/api/v1/claims/search/', searchParams, {
  timeout: 120000, // 120 seconds for claim search
});
```

### Solution 2: Make Search Asynchronous (BETTER)

Convert claim search to async processing:

1. **Submit search** → Returns task ID immediately
2. **Poll for results** → Check status every 2 seconds
3. **Display results** → When ready

**Backend changes needed:**
```python
# Use Celery for async processing
@shared_task
def search_claims_async(search_params):
    # Existing search logic
    return results

# API endpoint
def search_claims(request):
    task = search_claims_async.delay(request.data)
    return Response({'task_id': task.id, 'status': 'processing'})
```

**Frontend changes needed:**
```typescript
// Submit search
const { task_id } = await api.post('/api/v1/claims/search/', params);

// Poll for results
const pollResults = async (taskId) => {
  const { status, results } = await api.get(`/api/v1/claims/search/${taskId}/`);
  if (status === 'completed') {
    return results;
  } else if (status === 'processing') {
    await sleep(2000);
    return pollResults(taskId);
  }
};
```

### Solution 3: Optimize Backend (BEST LONG-TERM)

Make API calls in parallel instead of sequential:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def search_claims(request):
    claims = get_matching_claims(request.data)
    
    # Process claims in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(enrich_claim_data, claim)
            for claim in claims
        ]
        enriched_claims = [f.result() for f in futures]
    
    return Response(enriched_claims)
```

This would reduce processing time from 30-60s to 5-10s.

## 🚀 Quick Fix Implementation

### Step 1: Find Axios Configuration

```bash
ssh connectme@169.59.163.43 'grep -r "timeout.*30000" /var/www/connectme-preprod-frontend/src/ 2>/dev/null | head -5'
```

### Step 2: Update Timeout

```bash
# Find the file
ssh connectme@169.59.163.43 'find /var/www/connectme-preprod-frontend/src -name "*.ts" -o -name "*.tsx" | xargs grep -l "axios.create\|timeout: 30000" | head -5'

# Update the timeout (example)
ssh connectme@169.59.163.43 'sed -i "s/timeout: 30000/timeout: 120000/g" /var/www/connectme-preprod-frontend/src/lib/api.ts'
```

### Step 3: Rebuild Frontend

```bash
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-frontend && npm run build'
ssh connectme@169.59.163.43 'pm2 restart connectme-preprod-frontend'
```

## 🧪 Testing

After applying the fix:

1. **Clear browser cache**
2. **Go to claim search**
3. **Search for claims**
4. **Wait up to 2 minutes** (should complete in 30-60 seconds)
5. **Results should appear** ✅

## 📊 Performance Metrics

| Metric | Current | After Quick Fix | After Optimization |
|--------|---------|-----------------|-------------------|
| Frontend Timeout | 30s ❌ | 120s ✅ | 120s ✅ |
| Backend Processing | 30-60s | 30-60s | 5-10s ✅ |
| User Experience | Fails | Works (slow) | Fast ✅ |

## 🔍 Monitoring

Watch the backend logs during search:

```bash
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f | grep -i "claim\|search"'
```

You'll see:
```
Processing claim 1/12...
Processing claim 2/12...
...
Processing claim 12/12...
```

Each claim takes ~2-5 seconds.

## 💡 Recommendations

### Short-term (Today):
1. ✅ Increase frontend timeout to 120 seconds
2. ✅ Add loading indicator with progress
3. ✅ Show "This may take up to 2 minutes..." message

### Medium-term (This Week):
1. Implement async search with polling
2. Add caching for claim details
3. Batch API calls where possible

### Long-term (This Month):
1. Optimize backend to use parallel processing
2. Implement Redis caching
3. Pre-fetch common searches
4. Add pagination (search fewer claims at once)

## 🛠️ Implementation Script

```bash
#!/bin/bash

echo "🔧 Fixing Claim Search Timeout"
echo ""

# Find axios config
echo "📍 Finding Axios configuration..."
AXIOS_FILE=$(ssh connectme@169.59.163.43 'find /var/www/connectme-preprod-frontend/src -name "api.ts" -o -name "axios.ts" | head -1')

if [ -z "$AXIOS_FILE" ]; then
    echo "❌ Could not find Axios configuration file"
    echo "Please manually update timeout in frontend Axios config"
    exit 1
fi

echo "✅ Found: $AXIOS_FILE"
echo ""

# Backup
echo "💾 Creating backup..."
ssh connectme@169.59.163.43 "cp $AXIOS_FILE ${AXIOS_FILE}.backup"

# Update timeout
echo "🔧 Updating timeout to 120 seconds..."
ssh connectme@169.59.163.43 "sed -i 's/timeout: 30000/timeout: 120000/g' $AXIOS_FILE"

# Rebuild
echo "🏗️  Rebuilding frontend..."
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-frontend && npm run build'

# Restart
echo "🔄 Restarting frontend..."
ssh connectme@169.59.163.43 'pm2 restart connectme-preprod-frontend'

echo ""
echo "✅ Fix applied!"
echo ""
echo "🧪 Test by:"
echo "1. Clear browser cache"
echo "2. Go to claim search"
echo "3. Search should now complete (may take 30-60 seconds)"
echo ""
```

---

**Priority:** High  
**Effort:** 5 minutes (Quick Fix) / 2 hours (Async) / 1 day (Optimization)  
**Impact:** Unblocks claim search immediately

