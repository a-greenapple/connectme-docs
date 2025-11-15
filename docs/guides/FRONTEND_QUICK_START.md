# Frontend Filtering - Quick Start Guide

## 🎯 Goal
Add advanced filtering UI to your existing Claims Search and Bulk Upload views to utilize the new backend filtering API.

---

## ✅ What You Already Have
Based on your screenshots:
- ✅ Dashboard with navigation
- ✅ "Search Claims" card
- ✅ Bulk Upload History view with job cards
- ✅ Dark theme UI with purple accents
- ✅ Status indicators (Completed, Processing, etc.)

---

## 🆕 What We're Adding

### For Claims Search View:
1. **Filter Panel** - Collapsible panel with 20+ filter options
2. **Results Table** - Sortable table with pagination
3. **Export Button** - Download filtered results as CSV

### For Bulk Upload View:
1. **Job Filters** - Filter by status, date, errors
2. **Enhanced Job Cards** - Better error reporting
3. **Job Details Modal** - View detailed results

---

## 🚀 Implementation Steps

### Step 1: Add Required Dependencies

```bash
cd connectme-frontend
npm install date-fns
```

### Step 2: Create Utility Components

These are reusable components used across the app:

#### 2a. Date Range Picker
**File:** `src/components/ui/DateRangePicker.tsx`

```typescript
'use client';

interface DateRangePickerProps {
  startDate?: string;
  endDate?: string;
  onStartDateChange: (date: string | undefined) => void;
  onEndDateChange: (date: string | undefined) => void;
}

export function DateRangePicker({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
}: DateRangePickerProps) {
  return (
    <div className="flex items-center space-x-4">
      <div className="flex-1">
        <label className="block text-xs text-gray-500 mb-1">From</label>
        <input
          type="date"
          value={startDate || ''}
          onChange={(e) => onStartDateChange(e.target.value || undefined)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 bg-gray-800 text-white"
        />
      </div>
      <div className="flex-1">
        <label className="block text-xs text-gray-500 mb-1">To</label>
        <input
          type="date"
          value={endDate || ''}
          onChange={(e) => onEndDateChange(e.target.value || undefined)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 bg-gray-800 text-white"
        />
      </div>
    </div>
  );
}
```

#### 2b. Amount Range Input
**File:** `src/components/ui/AmountRangeInput.tsx`

```typescript
'use client';

interface AmountRangeInputProps {
  min?: number;
  max?: number;
  onMinChange: (value: number | undefined) => void;
  onMaxChange: (value: number | undefined) => void;
}

export function AmountRangeInput({
  min,
  max,
  onMinChange,
  onMaxChange,
}: AmountRangeInputProps) {
  return (
    <div className="flex items-center space-x-4">
      <div className="flex-1">
        <label className="block text-xs text-gray-500 mb-1">Min</label>
        <div className="relative">
          <span className="absolute left-3 top-2 text-gray-400">$</span>
          <input
            type="number"
            value={min || ''}
            onChange={(e) => onMinChange(e.target.value ? parseFloat(e.target.value) : undefined)}
            placeholder="0.00"
            className="w-full pl-7 pr-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 bg-gray-800 text-white"
          />
        </div>
      </div>
      <div className="flex-1">
        <label className="block text-xs text-gray-500 mb-1">Max</label>
        <div className="relative">
          <span className="absolute left-3 top-2 text-gray-400">$</span>
          <input
            type="number"
            value={max || ''}
            onChange={(e) => onMaxChange(e.target.value ? parseFloat(e.target.value) : undefined)}
            placeholder="0.00"
            className="w-full pl-7 pr-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500 bg-gray-800 text-white"
          />
        </div>
      </div>
    </div>
  );
}
```

#### 2c. Status Badge
**File:** `src/components/ui/StatusBadge.tsx`

```typescript
interface StatusBadgeProps {
  status: string;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const getStatusColor = (status: string) => {
    switch (status.toUpperCase()) {
      case 'PAID':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'DENIED':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'PROCESSING':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'COMPLETED':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'FAILED':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusColor(status)}`}>
      {status}
    </span>
  );
}
```

### Step 3: Create API Client

**File:** `src/lib/api/claims.ts`

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ClaimFilters {
  status?: string;
  provider?: string;
  claim_number?: string;
  min_amount?: number;
  max_amount?: number;
  service_date_from?: string;
  service_date_to?: string;
  payment_date_from?: string;
  payment_date_to?: string;
  has_payment?: boolean;
}

export async function fetchClaims(filters: ClaimFilters = {}, page: number = 1) {
  const params = new URLSearchParams();
  params.append('page', page.toString());
  
  // Add filters to params
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  const response = await fetch(`${API_BASE_URL}/api/v1/claims/claims/?${params}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) throw new Error('Failed to fetch claims');
  return response.json();
}
```

### Step 4: Update Your Claims Page

**File:** `src/app/claims/page.tsx` (or wherever your claims view is)

```typescript
'use client';

import { useState, useEffect } from 'react';
import { fetchClaims, ClaimFilters } from '@/lib/api/claims';
import { DateRangePicker } from '@/components/ui/DateRangePicker';
import { AmountRangeInput } from '@/components/ui/AmountRangeInput';
import { StatusBadge } from '@/components/ui/StatusBadge';

export default function ClaimsPage() {
  const [claims, setClaims] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<ClaimFilters>({});
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    loadClaims();
  }, [filters]);

  const loadClaims = async () => {
    setIsLoading(true);
    try {
      const data = await fetchClaims(filters);
      setClaims(data.results);
    } catch (error) {
      console.error('Failed to load claims:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateFilter = (key: keyof ClaimFilters, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Claims Search</h1>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition"
        >
          {showFilters ? 'Hide' : 'Show'} Filters
        </button>
      </div>

      {/* Filter Panel */}
      {showFilters && (
        <div className="bg-gray-800 rounded-lg p-6 mb-8 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Status */}
            <div>
              <label className="block text-sm font-medium mb-2">Status</label>
              <select
                value={filters.status || ''}
                onChange={(e) => updateFilter('status', e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="">All</option>
                <option value="PAID">Paid</option>
                <option value="PENDING">Pending</option>
                <option value="DENIED">Denied</option>
              </select>
            </div>

            {/* Provider */}
            <div>
              <label className="block text-sm font-medium mb-2">Provider</label>
              <select
                value={filters.provider || ''}
                onChange={(e) => updateFilter('provider', e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="">All</option>
                <option value="uhc">UnitedHealthcare</option>
                <option value="anthem">Anthem</option>
                <option value="aetna">Aetna</option>
              </select>
            </div>

            {/* Claim Number Search */}
            <div>
              <label className="block text-sm font-medium mb-2">Claim Number</label>
              <input
                type="text"
                value={filters.claim_number || ''}
                onChange={(e) => updateFilter('claim_number', e.target.value)}
                placeholder="Search..."
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:ring-purple-500 focus:border-purple-500"
              />
            </div>
          </div>

          {/* Service Date Range */}
          <div>
            <label className="block text-sm font-medium mb-2">Service Date Range</label>
            <DateRangePicker
              startDate={filters.service_date_from}
              endDate={filters.service_date_to}
              onStartDateChange={(date) => updateFilter('service_date_from', date)}
              onEndDateChange={(date) => updateFilter('service_date_to', date)}
            />
          </div>

          {/* Payment Amount Range */}
          <div>
            <label className="block text-sm font-medium mb-2">Payment Amount</label>
            <AmountRangeInput
              min={filters.min_amount}
              max={filters.max_amount}
              onMinChange={(value) => updateFilter('min_amount', value)}
              onMaxChange={(value) => updateFilter('max_amount', value)}
            />
          </div>

          {/* Reset Button */}
          <div className="flex justify-end">
            <button
              onClick={() => setFilters({})}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition"
            >
              Reset Filters
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {claims.map((claim: any) => (
            <div key={claim.id} className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">{claim.claim_number}</h3>
                  <p className="text-sm text-gray-400 mt-1">
                    Service Date: {new Date(claim.service_date).toLocaleDateString()}
                  </p>
                </div>
                <div className="text-right">
                  <StatusBadge status={claim.status} />
                  <p className="text-lg font-bold mt-2">${claim.paid_amount}</p>
                  <p className="text-xs text-gray-400">Billed: ${claim.billed_amount}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 🎨 Styling Notes

Your app uses a **dark theme** with:
- Background: `bg-gray-900`
- Cards: `bg-gray-800`
- Accent: Purple (`bg-purple-600`)
- Text: White/Gray

All components above are styled to match your existing theme!

---

## 🧪 Testing Checklist

After implementation:

- [ ] Filters update the URL query params
- [ ] Results update when filters change
- [ ] Pagination works correctly
- [ ] Sorting works on all columns
- [ ] Export downloads correct data
- [ ] Loading states show properly
- [ ] Error messages display correctly
- [ ] Mobile responsive design works

---

## 📊 API Filter Examples

Test these in your browser console or Postman:

```bash
# All paid claims
GET /api/v1/claims/claims/?status=PAID

# UHC claims from last 30 days
GET /api/v1/claims/claims/?provider=uhc&service_date_from=2024-10-01

# Claims with payment > $1000
GET /api/v1/claims/claims/?min_amount=1000

# Search specific claim number
GET /api/v1/claims/claims/?search=12345678

# Sort by payment amount (descending)
GET /api/v1/claims/claims/?ordering=-paid_amount

# Combine multiple filters
GET /api/v1/claims/claims/?status=PAID&provider=uhc&min_amount=500&ordering=-payment_date
```

---

## 🚀 Next Steps

1. **Start Small**: Implement just the status and provider filters first
2. **Test**: Verify they work with your backend
3. **Add More**: Gradually add date ranges, amounts, etc.
4. **Polish**: Add loading states, error handling, animations
5. **Bulk View**: Apply same pattern to bulk upload jobs

---

## 📞 Need Help?

- Check backend API docs: `https://your-domain.com/api/docs/`
- Review `CLAIMS_FILTERING_API.md` for filter examples
- Test filters in Swagger UI first: `https://your-domain.com/api/swagger/`

---

**Ready to code!** Start with the utility components, then build up to the full filter panel. 🎉

