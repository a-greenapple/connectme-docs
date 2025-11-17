# Frontend Filtering Enhancement Plan

## Overview
This document outlines the frontend enhancements needed to utilize the new advanced filtering capabilities implemented in the backend API.

---

## 🎯 Backend Filtering Capabilities (Already Implemented)

### Claims API (`/api/v1/claims/claims/`)
**Available Filters:**
- `status` - Filter by claim status (PAID, PENDING, DENIED, etc.)
- `provider` - Filter by provider (uhc, anthem, aetna, etc.)
- `claim_number` - Exact claim number match
- `min_amount` / `max_amount` - Payment amount range
- `min_billed` / `max_billed` - Billed amount range
- `service_date_from` / `service_date_to` - Service date range
- `payment_date_from` / `payment_date_to` - Payment date range
- `queried_after` / `queried_before` - Query date range
- `has_payment` - Boolean (true/false)
- `has_payment_date` - Boolean (true/false)
- `search` - Search claim numbers
- `ordering` - Sort by any field (prefix with `-` for descending)

### CSV Jobs API (`/api/v1/claims/csv-jobs/`)
**Available Filters:**
- `status` - Job status (PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED)
- `filename` - Search by filename
- `created_after` / `created_before` - Creation date range
- `completed_after` / `completed_before` - Completion date range
- `has_errors` - Boolean (true/false)
- `ordering` - Sort by any field

---

## 📋 Frontend Components to Create/Enhance

### 1. Claims Search View Enhancement

#### Current State (Based on Screenshots)
- ✅ Basic search card on dashboard
- ✅ Navigation menu with "Claims" section

#### Enhancements Needed
- 🔧 Advanced filter panel
- 🔧 Results table with sorting
- 🔧 Pagination controls
- 🔧 Export functionality

---

## 🎨 Component Architecture

```
src/
├── app/
│   ├── claims/
│   │   ├── page.tsx                    # Main claims search page
│   │   ├── [id]/
│   │   │   └── page.tsx                # Claim details page
│   │   └── bulk/
│   │       ├── page.tsx                # Bulk upload page
│   │       └── [jobId]/
│   │           └── page.tsx            # Job details page
│   └── ...
├── components/
│   ├── claims/
│   │   ├── ClaimsFilterPanel.tsx       # 🆕 Advanced filters
│   │   ├── ClaimsTable.tsx             # 🆕 Results table
│   │   ├── ClaimCard.tsx               # 🆕 Individual claim card
│   │   ├── ClaimDetailsModal.tsx       # 🆕 Details popup
│   │   └── ClaimExportButton.tsx       # 🆕 Export to CSV
│   ├── bulk/
│   │   ├── BulkJobsFilterPanel.tsx     # 🆕 Job filters
│   │   ├── BulkJobsTable.tsx           # ✅ Already exists
│   │   └── BulkJobDetails.tsx          # 🆕 Job details
│   ├── ui/
│   │   ├── DateRangePicker.tsx         # 🆕 Reusable date picker
│   │   ├── AmountRangeInput.tsx        # 🆕 Min/max amount
│   │   ├── StatusBadge.tsx             # 🆕 Status indicator
│   │   └── SearchInput.tsx             # 🆕 Debounced search
│   └── ...
├── lib/
│   ├── api/
│   │   ├── claims.ts                   # 🆕 Claims API client
│   │   ├── bulk.ts                     # 🆕 Bulk jobs API client
│   │   └── types.ts                    # 🆕 TypeScript types
│   └── hooks/
│       ├── useClaims.ts                # 🆕 Claims data hook
│       ├── useBulkJobs.ts              # 🆕 Bulk jobs hook
│       └── useDebounce.ts              # 🆕 Debounce hook
└── ...
```

---

## 🔧 Implementation Details

### 1. Claims Filter Panel Component

**File:** `src/components/claims/ClaimsFilterPanel.tsx`

```typescript
'use client';

import { useState } from 'react';
import { DateRangePicker } from '@/components/ui/DateRangePicker';
import { AmountRangeInput } from '@/components/ui/AmountRangeInput';

interface ClaimsFilterPanelProps {
  onFilterChange: (filters: ClaimFilters) => void;
  onReset: () => void;
}

export interface ClaimFilters {
  status?: string;
  provider?: string;
  claim_number?: string;
  min_amount?: number;
  max_amount?: number;
  min_billed?: number;
  max_billed?: number;
  service_date_from?: string;
  service_date_to?: string;
  payment_date_from?: string;
  payment_date_to?: string;
  has_payment?: boolean;
  has_payment_date?: boolean;
}

export function ClaimsFilterPanel({ onFilterChange, onReset }: ClaimsFilterPanelProps) {
  const [filters, setFilters] = useState<ClaimFilters>({});
  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterUpdate = (key: keyof ClaimFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleReset = () => {
    setFilters({});
    onReset();
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Filter Claims
        </h2>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          {isExpanded ? 'Hide Filters' : 'Show All Filters'}
        </button>
      </div>

      {/* Basic Filters (Always Visible) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <select
            value={filters.status || ''}
            onChange={(e) => handleFilterUpdate('status', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="PAID">Paid</option>
            <option value="PENDING">Pending</option>
            <option value="DENIED">Denied</option>
            <option value="PROCESSING">Processing</option>
            <option value="REJECTED">Rejected</option>
          </select>
        </div>

        {/* Provider Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Provider
          </label>
          <select
            value={filters.provider || ''}
            onChange={(e) => handleFilterUpdate('provider', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">All Providers</option>
            <option value="uhc">UnitedHealthcare</option>
            <option value="anthem">Anthem</option>
            <option value="aetna">Aetna</option>
            <option value="cigna">Cigna</option>
          </select>
        </div>

        {/* Claim Number Search */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Claim Number
          </label>
          <input
            type="text"
            value={filters.claim_number || ''}
            onChange={(e) => handleFilterUpdate('claim_number', e.target.value || undefined)}
            placeholder="Search claim number..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Advanced Filters (Collapsible) */}
      {isExpanded && (
        <div className="space-y-4 pt-4 border-t border-gray-200">
          {/* Service Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Service Date Range
            </label>
            <DateRangePicker
              startDate={filters.service_date_from}
              endDate={filters.service_date_to}
              onStartDateChange={(date) => handleFilterUpdate('service_date_from', date)}
              onEndDateChange={(date) => handleFilterUpdate('service_date_to', date)}
            />
          </div>

          {/* Payment Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Payment Date Range
            </label>
            <DateRangePicker
              startDate={filters.payment_date_from}
              endDate={filters.payment_date_to}
              onStartDateChange={(date) => handleFilterUpdate('payment_date_from', date)}
              onEndDateChange={(date) => handleFilterUpdate('payment_date_to', date)}
            />
          </div>

          {/* Amount Ranges */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Payment Amount Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Amount
              </label>
              <AmountRangeInput
                min={filters.min_amount}
                max={filters.max_amount}
                onMinChange={(value) => handleFilterUpdate('min_amount', value)}
                onMaxChange={(value) => handleFilterUpdate('max_amount', value)}
              />
            </div>

            {/* Billed Amount Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Billed Amount
              </label>
              <AmountRangeInput
                min={filters.min_billed}
                max={filters.max_billed}
                onMinChange={(value) => handleFilterUpdate('min_billed', value)}
                onMaxChange={(value) => handleFilterUpdate('max_billed', value)}
              />
            </div>
          </div>

          {/* Boolean Filters */}
          <div className="flex items-center space-x-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={filters.has_payment || false}
                onChange={(e) => handleFilterUpdate('has_payment', e.target.checked || undefined)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">Has Payment</span>
            </label>

            <label className="flex items-center">
              <input
                type="checkbox"
                checked={filters.has_payment_date || false}
                onChange={(e) => handleFilterUpdate('has_payment_date', e.target.checked || undefined)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">Has Payment Date</span>
            </label>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-end space-x-3 mt-4 pt-4 border-t border-gray-200">
        <button
          onClick={handleReset}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Reset Filters
        </button>
        <button
          onClick={() => onFilterChange(filters)}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Apply Filters
        </button>
      </div>
    </div>
  );
}
```

---

### 2. Claims Table Component

**File:** `src/components/claims/ClaimsTable.tsx`

```typescript
'use client';

import { useState } from 'react';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { ClaimDetailsModal } from './ClaimDetailsModal';

interface Claim {
  id: string;
  claim_number: string;
  status: string;
  provider: string;
  patient_dob: string;
  service_date: string;
  payment_date: string | null;
  billed_amount: string;
  paid_amount: string;
  queried_at: string;
}

interface ClaimsTableProps {
  claims: Claim[];
  isLoading: boolean;
  onSort: (field: string) => void;
  sortField?: string;
  sortDirection?: 'asc' | 'desc';
}

export function ClaimsTable({ 
  claims, 
  isLoading, 
  onSort, 
  sortField, 
  sortDirection 
}: ClaimsTableProps) {
  const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);

  const handleSort = (field: string) => {
    onSort(field);
  };

  const SortIcon = ({ field }: { field: string }) => {
    if (sortField !== field) {
      return <span className="text-gray-400">⇅</span>;
    }
    return sortDirection === 'asc' ? <span>↑</span> : <span>↓</span>;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (claims.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No claims found</h3>
        <p className="mt-1 text-sm text-gray-500">
          Try adjusting your filters or search criteria.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  onClick={() => handleSort('claim_number')}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center space-x-1">
                    <span>Claim Number</span>
                    <SortIcon field="claim_number" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('status')}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center space-x-1">
                    <span>Status</span>
                    <SortIcon field="status" />
                  </div>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Provider
                </th>
                <th
                  onClick={() => handleSort('service_date')}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center space-x-1">
                    <span>Service Date</span>
                    <SortIcon field="service_date" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('billed_amount')}
                  className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center justify-end space-x-1">
                    <span>Billed</span>
                    <SortIcon field="billed_amount" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('paid_amount')}
                  className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center justify-end space-x-1">
                    <span>Paid</span>
                    <SortIcon field="paid_amount" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('payment_date')}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                >
                  <div className="flex items-center space-x-1">
                    <span>Payment Date</span>
                    <SortIcon field="payment_date" />
                  </div>
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {claims.map((claim) => (
                <tr key={claim.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {claim.claim_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <StatusBadge status={claim.status} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 uppercase">
                    {claim.provider}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(claim.service_date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                    ${parseFloat(claim.billed_amount).toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
                    ${parseFloat(claim.paid_amount).toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {claim.payment_date 
                      ? new Date(claim.payment_date).toLocaleDateString()
                      : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => setSelectedClaim(claim)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Claim Details Modal */}
      {selectedClaim && (
        <ClaimDetailsModal
          claim={selectedClaim}
          onClose={() => setSelectedClaim(null)}
        />
      )}
    </>
  );
}
```

---

### 3. API Client

**File:** `src/lib/api/claims.ts`

```typescript
import { ClaimFilters } from '@/components/claims/ClaimsFilterPanel';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ClaimsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Claim[];
}

export interface Claim {
  id: string;
  claim_number: string;
  status: string;
  provider: string;
  patient_dob: string;
  service_date: string;
  payment_date: string | null;
  billed_amount: string;
  paid_amount: string;
  queried_at: string;
  user: number;
  organization: number;
}

export async function fetchClaims(
  filters: ClaimFilters = {},
  page: number = 1,
  ordering?: string
): Promise<ClaimsResponse> {
  // Build query parameters
  const params = new URLSearchParams();
  
  // Pagination
  params.append('page', page.toString());
  
  // Filters
  if (filters.status) params.append('status', filters.status);
  if (filters.provider) params.append('provider', filters.provider);
  if (filters.claim_number) params.append('search', filters.claim_number);
  if (filters.min_amount) params.append('min_amount', filters.min_amount.toString());
  if (filters.max_amount) params.append('max_amount', filters.max_amount.toString());
  if (filters.min_billed) params.append('min_billed', filters.min_billed.toString());
  if (filters.max_billed) params.append('max_billed', filters.max_billed.toString());
  if (filters.service_date_from) params.append('service_date_from', filters.service_date_from);
  if (filters.service_date_to) params.append('service_date_to', filters.service_date_to);
  if (filters.payment_date_from) params.append('payment_date_from', filters.payment_date_from);
  if (filters.payment_date_to) params.append('payment_date_to', filters.payment_date_to);
  if (filters.has_payment !== undefined) params.append('has_payment', filters.has_payment.toString());
  if (filters.has_payment_date !== undefined) params.append('has_payment_date', filters.has_payment_date.toString());
  
  // Ordering
  if (ordering) params.append('ordering', ordering);
  
  const response = await fetch(`${API_BASE_URL}/api/v1/claims/claims/?${params.toString()}`, {
    headers: {
      'Content-Type': 'application/json',
      // Add authentication header here
      // 'Authorization': `Bearer ${token}`,
    },
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch claims');
  }
  
  return response.json();
}

export async function exportClaims(filters: ClaimFilters = {}): Promise<Blob> {
  const params = new URLSearchParams();
  
  // Add all filters
  if (filters.status) params.append('status', filters.status);
  if (filters.provider) params.append('provider', filters.provider);
  // ... add all other filters
  
  const response = await fetch(`${API_BASE_URL}/api/v1/claims/claims/export/?${params.toString()}`, {
    headers: {
      // Add authentication header
    },
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to export claims');
  }
  
  return response.blob();
}
```

---

### 4. React Hook for Claims

**File:** `src/lib/hooks/useClaims.ts`

```typescript
import { useState, useEffect } from 'react';
import { fetchClaims, ClaimsResponse, Claim } from '@/lib/api/claims';
import { ClaimFilters } from '@/components/claims/ClaimsFilterPanel';

export function useClaims(initialFilters: ClaimFilters = {}) {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ClaimFilters>(initialFilters);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [ordering, setOrdering] = useState<string>('-queried_at');

  const loadClaims = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetchClaims(filters, page, ordering);
      setClaims(response.results);
      setTotalCount(response.count);
      setHasNext(!!response.next);
      setHasPrevious(!!response.previous);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadClaims();
  }, [filters, page, ordering]);

  const handleFilterChange = (newFilters: ClaimFilters) => {
    setFilters(newFilters);
    setPage(1); // Reset to first page when filters change
  };

  const handleSort = (field: string) => {
    // Toggle sort direction if clicking the same field
    if (ordering === field) {
      setOrdering(`-${field}`);
    } else if (ordering === `-${field}`) {
      setOrdering(field);
    } else {
      setOrdering(field);
    }
  };

  const handleReset = () => {
    setFilters({});
    setPage(1);
    setOrdering('-queried_at');
  };

  return {
    claims,
    isLoading,
    error,
    filters,
    page,
    totalCount,
    hasNext,
    hasPrevious,
    ordering,
    setPage,
    handleFilterChange,
    handleSort,
    handleReset,
    refresh: loadClaims,
  };
}
```

---

### 5. Main Claims Page

**File:** `src/app/claims/page.tsx`

```typescript
'use client';

import { ClaimsFilterPanel } from '@/components/claims/ClaimsFilterPanel';
import { ClaimsTable } from '@/components/claims/ClaimsTable';
import { ClaimExportButton } from '@/components/claims/ClaimExportButton';
import { useClaims } from '@/lib/hooks/useClaims';

export default function ClaimsPage() {
  const {
    claims,
    isLoading,
    error,
    filters,
    page,
    totalCount,
    hasNext,
    hasPrevious,
    ordering,
    setPage,
    handleFilterChange,
    handleSort,
    handleReset,
  } = useClaims();

  const sortField = ordering.startsWith('-') ? ordering.slice(1) : ordering;
  const sortDirection = ordering.startsWith('-') ? 'desc' : 'asc';

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Claims Search</h1>
          <p className="mt-2 text-sm text-gray-600">
            Search and filter claims across all providers
          </p>
        </div>
        <ClaimExportButton filters={filters} />
      </div>

      {/* Filter Panel */}
      <ClaimsFilterPanel 
        onFilterChange={handleFilterChange}
        onReset={handleReset}
      />

      {/* Results Summary */}
      {!isLoading && (
        <div className="mb-4 text-sm text-gray-600">
          Showing {claims.length} of {totalCount} claims
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Claims Table */}
      <ClaimsTable
        claims={claims}
        isLoading={isLoading}
        onSort={handleSort}
        sortField={sortField}
        sortDirection={sortDirection}
      />

      {/* Pagination */}
      {totalCount > 0 && (
        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={() => setPage(page - 1)}
            disabled={!hasPrevious}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page {page}
          </span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={!hasNext}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## 📦 Required Dependencies

Add these to your `package.json`:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.0.0",
    "typescript": "^5.0.0",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

---

## 🎯 Implementation Checklist

### Phase 1: Core Components (Week 1)
- [ ] Create `ClaimsFilterPanel` component
- [ ] Create `ClaimsTable` component
- [ ] Create `useClaims` hook
- [ ] Create API client functions
- [ ] Test with backend API

### Phase 2: UI Components (Week 2)
- [ ] Create `DateRangePicker` component
- [ ] Create `AmountRangeInput` component
- [ ] Create `StatusBadge` component
- [ ] Create `SearchInput` with debouncing
- [ ] Add loading states and error handling

### Phase 3: Bulk Jobs Enhancement (Week 3)
- [ ] Create `BulkJobsFilterPanel`
- [ ] Enhance existing bulk jobs table
- [ ] Add job details view
- [ ] Add error reporting view

### Phase 4: Polish & Testing (Week 4)
- [ ] Add export functionality
- [ ] Add responsive design
- [ ] Add keyboard shortcuts
- [ ] Add unit tests
- [ ] Add E2E tests
- [ ] Performance optimization

---

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   cd connectme-frontend
   npm install date-fns
   ```

2. **Set Environment Variables**
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=https://your-preprod-domain.com
   ```

3. **Create Components**
   - Start with `ClaimsFilterPanel`
   - Then `ClaimsTable`
   - Then the main page

4. **Test with Backend**
   - Ensure backend is running
   - Test each filter parameter
   - Verify pagination works

---

## 📊 Expected User Flow

1. **User lands on Claims page**
   - Sees filter panel (collapsed by default)
   - Sees table with recent claims (default: last 50, sorted by query date desc)

2. **User applies filters**
   - Selects status: "PAID"
   - Selects provider: "UHC"
   - Sets date range: Last 30 days
   - Clicks "Apply Filters"

3. **Results update**
   - Table shows filtered claims
   - Count updates: "Showing 25 of 25 claims"
   - Can sort by clicking column headers

4. **User clicks "View Details"**
   - Modal opens with full claim details
   - Shows diagnosis codes, procedures, payments

5. **User exports results**
   - Clicks "Export to CSV"
   - Downloads file with filtered results

---

## 🔒 Security Considerations

1. **Authentication**
   - All API calls must include auth token
   - Handle 401/403 responses gracefully

2. **PII Protection**
   - Don't log patient data
   - Mask SSN in display
   - Secure local storage

3. **HIPAA Compliance**
   - Audit all data access
   - Session timeouts
   - Secure data transmission

---

## 📞 Support

For implementation help:
1. Refer to backend API docs: `/api/docs/`
2. Check `CLAIMS_FILTERING_API.md` for filter examples
3. Test filters using Swagger UI first

---

**Ready to implement!** Start with the `ClaimsFilterPanel` component and build from there. 🚀

