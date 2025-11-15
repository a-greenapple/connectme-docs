# 📚 ConnectMe Documentation Hub

**Last Updated**: November 15, 2025  
**Version**: Pre-Production  
**Status**: Active Development

---

## 🚀 Quick Start Guides

### For New Users
- [**Quick Start Guide**](./5_docs/1_Guide/QUICK_REFERENCE.md) - Start here if you're new
- [**Complete Setup Guide**](./5_docs/1_Guide/COMPLETE_SETUP_AND_TEST_GUIDE.md) - Full system setup
- [**Frontend Quick Start**](./FRONTEND_QUICK_START.md) - Get the UI running

### For Developers
- [**Local Setup**](./LOCAL-SETUP.md) - Development environment setup
- [**Development Workflow**](./5_docs/DESIGN/DEVELOPMENT_WORKFLOW.md) - How to work on the project
- [**Git Branching Strategy**](./GIT_BRANCHING_STRATEGY.md) - Version control workflow

### For Administrators
- [**Admin Index**](./help/admin/index.md) - Admin documentation hub
- [**User Management Setup**](./docs/USER_MANAGEMENT_SETUP.md) - Configure users and roles
- [**Keycloak Admin Setup**](./KEYCLOAK_ADMIN_SETUP.md) - Authentication configuration

---

## 📋 Feature Documentation

### 1. Claims Management
- [**Claims UI Guide**](./CLAIMS_UI_GUIDE.md) - Using the claims interface
- [**How Claims Are Queried**](./5_docs/1_1_CLAIMS/HOW_CLAIMS_ARE_QUERIED.md) - Technical details
- [**Multi-Practice Support**](./5_docs/1_1_CLAIMS/MULTI_PRACTICE_TIN_PAYER_SUPPORT.md) - Multiple TINs/payers
- [**Payment Differences**](./5_docs/1_1_CLAIMS/PAYMENT_DIFFERENCE_EXPLANATION.md) - Understanding payment data
- [**Claims Filtering**](./CLAIMS_FILTERING_IMPLEMENTATION.md) - Filter by status
- [**UHC Claim Filtering**](./UHC_CLAIM_FILTERING_GUIDE.md) - UHC-specific filtering
- [**Line-Level Claim Codes**](./LINE_LEVEL_CLAIM_CODES.md) - Detailed claim codes

### 2. Bulk Upload System
- [**Quick Start - Bulk Upload**](./5_docs/1_2_BULK/QUICK_START_BULK_UPLOAD.md) - Get started quickly
- [**CSV Bulk Upload Guide**](./5_docs/1_2_BULK/CSV_BULK_UPLOAD_USER_GUIDE.md) - User guide
- [**Bulk Upload Template**](./BULK_UPLOAD_TEMPLATE_ADDED.md) - Download template
- [**Bulk Upload History**](./BULK_UPLOAD_HISTORY_FEATURES.md) - View past uploads
- [**CSV System Complete**](./5_docs/1_2_BULK/CSV_SYSTEM_COMPLETE.md) - Technical overview
- [**Bulk Optimization Plan**](./5_docs/1_2_BULK/BULK_OPTIMIZATION_PLAN.md) - Performance improvements

### 3. User Management & Authentication
- [**Keycloak Integration Guide**](./5_docs/keycloak/KEYCLOAK_INTEGRATION_GUIDE.md) - Full integration
- [**Keycloak Quick Start**](./5_docs/keycloak/KEYCLOAK_QUICK_START.md) - Fast setup
- [**Role Management**](./ROLE_MANAGEMENT_AUDIT.md) - Roles and permissions
- [**User Setup Quickstart**](./5_docs/TBR/3_USER_SETUP_QUICKSTART.md) - Create users
- [**Permissions Guide**](./help/admin/permissions.md) - Permission system
- [**Practice Access Model**](./NEW_PRACTICE_ACCESS_MODEL.md) - Practice-based access

### 4. Workflow System
- [**Workflow API Documentation**](./5_docs/workflow/WORKFLOW_API_DOCUMENTATION.md) - API reference
- [**Workflow Implementation**](./5_docs/workflow/WORKFLOW_IMPLEMENTATION_SUMMARY.md) - How it works
- [**Complete Workflow Guide**](./5_docs/1_Guide/COMPLETE_WORKFLOW_IMPLEMENTATION.md) - Full guide

### 5. Monitoring & Logging
- [**Complete Monitoring System**](./5_docs/monitoring/COMPLETE_MONITORING_SYSTEM.md) - Full monitoring
- [**Log Viewing Options**](./5_docs/TBR/7_LOG_VIEWING_OPTIONS.md) - View system logs
- [**Monitoring System Complete**](./5_docs/monitoring/MONITORING_SYSTEM_COMPLETE.md) - Technical details

---

## 🔧 Technical Documentation

### Backend
- [**Provider Architecture**](./connectme-backend/PROVIDER_ARCHITECTURE.md) - System architecture
- [**UHC API Success**](./connectme-backend/UHC_API_SUCCESS.md) - UHC integration
- [**UHC Configuration**](./connectme-backend/UHC_CONFIGURATION_SUMMARY.md) - UHC setup
- [**Claims Filtering API**](./connectme-backend/CLAIMS_FILTERING_API.md) - API endpoints
- [**Workflow Transaction Sequence**](./connectme-backend/WORKFLOW_TRANSACTION_SEQUENCE.md) - Transaction flow

### Frontend
- [**Reconciliation UI Guide**](./connectme-frontend/11_RECONCILIATION_UI_GUIDE.md) - Reconciliation UI
- [**Cursor Design Guide**](./connectme-frontend/12_CURSOR_DESIGN_GUIDE.md) - Design system
- [**Environment Setup**](./connectme-frontend/13_ENV_SETUP_GUIDE.md) - Frontend config
- [**Claims Logic**](./connectme-frontend/claims-logic/README.md) - Frontend claims logic

### API Documentation
- [**Practice API Summary**](./PRACTICE_API_SUMMARY.md) - Practice endpoints
- [**Test Backend API**](./5_docs/testing/TEST_BACKEND_API.md) - Backend testing
- [**Test Workflow API**](./5_docs/testing/TEST_WORKFLOW_API.md) - Workflow testing

---

## 🐛 Troubleshooting & Fixes

### Common Issues
- [**Fix Claim Search Timeout**](./help/troubleshooting/FIX_CLAIM_SEARCH_TIMEOUT.md) - Timeout errors
- [**Fix CORS Keycloak**](./help/troubleshooting/FIX_CORS_KEYCLOAK.md) - CORS issues
- [**Bulk Upload Empty Results**](./help/troubleshooting/BULK_UPLOAD_EMPTY_RESULTS_FIX.md) - Empty results
- [**Bulk Upload Fix**](./help/troubleshooting/BULK_UPLOAD_FIX.md) - General bulk issues
- [**Debug CORS Error**](./help/troubleshooting/DEBUG_CORS_ERROR.md) - CORS debugging
- [**Claims Search 403 Fix**](./CLAIMS_SEARCH_403_FIX.md) - Permission errors

### Authentication Issues
- [**Admin Login Fix**](./ADMIN_LOGIN_FIX.md) - Admin login problems
- [**Auth Issues Resolved**](./5_docs/TBR/1_AUTH_ISSUES_RESOLVED.md) - Authentication fixes
- [**JWT Auth Fixed**](./5_docs/fixes/JWT_AUTH_FIXED.md) - JWT token issues
- [**Fix Login Issue**](./5_docs/fixes/FIX_LOGIN_ISSUE.md) - General login problems
- [**Keycloak Permissions Fix**](./KEYCLOAK_PERMISSIONS_FIX.md) - Permission issues

### Browser Issues
- [**Firefox Issue Resolved**](./5_docs/browser-issues/FIREFOX_ISSUE_RESOLVED.md) - Firefox problems
- [**Firefox Load Failed Debug**](./5_docs/browser-issues/FIREFOX_LOAD_FAILED_DEBUG.md) - Loading issues

### Recent Fixes
- [**Pagination Fix (Nov 15, 2025)**](./testcases/datequery-claimstatus-filterbased/TEST_PAGINATION_FIX.md) - UHC pagination
- [**Auth and Session Fixes**](./5_docs/fixes/AUTH_AND_SESSION_FIXES.md) - Session management
- [**Fixes Completed**](./5_docs/fixes/FIXES_COMPLETED.md) - All completed fixes

---

## 🧪 Testing

### Test Suites
- [**Testing Index**](./TESTING_INDEX.md) - Master testing index
- [**Testing Guide**](./5_docs/testing/TESTING_GUIDE.md) - How to test
- [**Test Results Summary**](./testing/TEST_RESULTS_SUMMARY.md) - Latest results
- [**Comprehensive Test Report**](./5_docs/testing/COMPREHENSIVE_TEST_REPORT.md) - Full report

### Specific Tests
- [**Status Filter Tests**](./testcases/datequery-claimstatus-filterbased/README.md) - Status filtering
- [**Pagination Tests**](./testcases/datequery-claimstatus-filterbased/TEST_PAGINATION_FIX.md) - Pagination testing
- [**Manual Test Checklist**](./testcases/datequery-claimstatus-filterbased/MANUAL_TEST_CHECKLIST.md) - Manual tests
- [**How to Run Tests**](./testcases/datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md) - Test execution

### Test Setup
- [**Playwright Setup**](./5_docs/testing/PLAYWRIGHT_SETUP_GUIDE.md) - E2E testing
- [**Testing Setup Complete**](./5_docs/testing/TESTING_SETUP_COMPLETE.md) - Test environment
- [**Quick Start Testing**](./5_docs/TBR/6_QUICK_START_TESTING.md) - Fast testing

---

## 🚀 Deployment

### Pre-Production
- [**Pre-Prod Setup Guide**](./docs/PREPROD_SETUP_GUIDE.md) - Pre-prod configuration
- [**Pre-Prod Configuration**](./PREPROD_CONFIGURATION.md) - Config details
- [**Pre-Prod Summary**](./docs/PREPROD_SUMMARY.md) - Current status
- [**UHC Pre-Prod Update**](./PREPROD_UHC_UPDATE_GUIDE.md) - UHC updates

### Production Planning
- [**TODO Before Production**](./TODO_BEFORE_PROD.md) - ⚠️ **MUST READ BEFORE PROD**
- [**Deployment Checklist**](./5_docs/TBR/5_DEPLOYMENT_CHECKLIST.md) - Pre-deployment checks
- [**Production Ready Docs**](./5_docs/1_1_CLAIMS/PRODUCTION_READY_DOCUMENTATION.md) - Prod readiness

### Deployment Guides
- [**Deployment Summary**](./DEPLOYMENT_SUMMARY.md) - Overview
- [**Deployment Status**](./DEPLOYMENT_STATUS.md) - Current status
- [**Quick Deploy Guide**](./5_docs/TBR/8_QUICK_DEPLOY_GUIDE.md) - Fast deployment
- [**Debian Deployment**](./5_docs/TBR/7_DEBIAN_DEPLOYMENT_GUIDE.md) - Debian-specific
- [**Server Setup Quickstart**](./5_docs/TBR/15_SERVER_SETUP_QUICKSTART.md) - Server setup
- [**SSH Deployment Key**](./5_docs/TBR/14_SSH_DEPLOYMENT_KEY_SETUP.md) - SSH keys

### Deployment Scripts
- [**Deployment Scripts README**](./scripts/deployment/10_DEPLOYMENT_SCRIPTS_README.md) - Script usage
- [**Pre-Prod Scripts**](./scripts/preprod/README.md) - Pre-prod scripts
- [**Git Sync Plan**](./scripts/GIT_SYNC_PLAN.md) - Code synchronization

---

## 📊 Status & Summaries

### Current Status
- [**Current State**](./5_docs/status-update/CURRENT_STATE.md) - Where we are now
- [**Current Status & Next Steps**](./5_docs/status-update/CURRENT_STATUS_AND_NEXT_STEPS.md) - Roadmap
- [**Final Status Report**](./5_docs/status-update/FINAL_STATUS_REPORT.md) - Latest status
- [**Complete Summary**](./COMPLETE_SUMMARY.md) - Overall summary

### Implementation Summaries
- [**Final Implementation Summary**](./5_docs/status-update/FINAL_IMPLEMENTATION_SUMMARY.md) - What's built
- [**Implementation Summary**](./5_docs/status-update/IMPLEMENTATION_SUMMARY.md) - Feature list
- [**Integration Status**](./5_docs/status-update/INTEGRATION_STATUS.md) - Integration status
- [**Frontend Implementation**](./5_docs/status-update/FRONTEND_IMPLEMENTATION_STATUS.md) - Frontend status

### Project Summaries
- [**Chat Summary**](./CHAT_SUMMARY.md) - Conversation history
- [**Documentation Organization**](./DOCUMENTATION_ORGANIZATION_SUMMARY.md) - Doc structure
- [**Testing Suite Summary**](./TESTING_SUITE_SUMMARY.md) - Testing overview

---

## 🔐 Security & Configuration

### SSL & Security
- [**SSL Setup Guide**](./connectme-backend/SSL_SETUP_GUIDE.md) - SSL configuration
- [**SSL Fix README**](./testing/SSL_FIX_README.md) - SSL troubleshooting

### Keycloak Configuration
- [**Keycloak Setup Guide**](./5_docs/keycloak/KEYCLOAK_SETUP_GUIDE.md) - Full setup
- [**Keycloak Docker Guide**](./5_docs/keycloak/KEYCLOAK_DOCKER_GUIDE.md) - Docker setup
- [**Keycloak Import Guide**](./5_docs/keycloak/KEYCLOAK_IMPORT_GUIDE.md) - Import realms
- [**Keycloak Realm Import**](./5_docs/keycloak/KEYCLOAK_REALM_IMPORT_GUIDE.md) - Realm configuration
- [**Keycloak Roles Integration**](./5_docs/keycloak/KEYCLOAK_ROLES_INTEGRATION.md) - Role setup
- [**Keycloak Sync Implementation**](./5_docs/keycloak/KEYCLOAK_SYNC_IMPLEMENTATION.md) - User sync
- [**Keycloak Create Roles**](./5_docs/keycloak/KEYCLOAK_CREATE_ROLES_STEP_BY_STEP.md) - Role creation
- [**Keycloak Composite Roles**](./5_docs/keycloak/KEYCLOAK_COMPOSITE_ROLES_GUIDE.md) - Advanced roles

---

## 📖 Reference Documentation

### Design & Architecture
- [**Design Confirmation**](./5_docs/DESIGN/DESIGN_CONFIRMATION_REQUIRED.md) - Design decisions
- [**Setup Complete System**](./5_docs/DESIGN/SETUP_COMPLETE_SYSTEM.md) - System overview
- [**Redis Local Access**](./5_docs/DESIGN/REDIS_LOCAL_ACCESS.md) - Redis configuration
- [**README Start Here**](./5_docs/DESIGN/README_START_HERE.md) - Design docs entry

### Sample Data
- [**Sample Data README**](./SAMPLE_DATA_README.md) - Test data
- [**Adding Practices**](./ADDING_PRACTICES.md) - Add new practices

### Enhancements & Plans
- [**Claims Enhancements Plan**](./CLAIMS_ENHANCEMENTS_PLAN.md) - Future improvements
- [**Frontend Filtering Enhancement**](./FRONTEND_FILTERING_ENHANCEMENT.md) - UI improvements
- [**Practice Selector Implementation**](./PRACTICE_SELECTOR_IMPLEMENTATION.md) - Practice selection

---

## 🎯 By Role

### For Administrators
1. [Admin Index](./help/admin/index.md)
2. [User Management Setup](./docs/USER_MANAGEMENT_SETUP.md)
3. [Keycloak Admin Setup](./KEYCLOAK_ADMIN_SETUP.md)
4. [Permissions Guide](./help/admin/permissions.md)
5. [Monitoring System](./5_docs/monitoring/COMPLETE_MONITORING_SYSTEM.md)

### For Developers
1. [Local Setup](./LOCAL-SETUP.md)
2. [Development Workflow](./5_docs/DESIGN/DEVELOPMENT_WORKFLOW.md)
3. [Provider Architecture](./connectme-backend/PROVIDER_ARCHITECTURE.md)
4. [Testing Guide](./5_docs/testing/TESTING_GUIDE.md)
5. [Git Branching Strategy](./GIT_BRANCHING_STRATEGY.md)

### For End Users
1. [Quick Reference](./5_docs/1_Guide/QUICK_REFERENCE.md)
2. [Claims UI Guide](./CLAIMS_UI_GUIDE.md)
3. [CSV Bulk Upload Guide](./5_docs/1_2_BULK/CSV_BULK_UPLOAD_USER_GUIDE.md)
4. [Troubleshooting](./help/troubleshooting/)

### For DevOps
1. [Deployment Checklist](./5_docs/TBR/5_DEPLOYMENT_CHECKLIST.md)
2. [Server Setup Quickstart](./5_docs/TBR/15_SERVER_SETUP_QUICKSTART.md)
3. [Deployment Scripts](./scripts/deployment/10_DEPLOYMENT_SCRIPTS_README.md)
4. [Monitoring System](./5_docs/monitoring/COMPLETE_MONITORING_SYSTEM.md)
5. [TODO Before Prod](./TODO_BEFORE_PROD.md) ⚠️

---

## 🆘 Need Help?

### Quick Links
- **Can't find something?** Check [Help README](./help/README.md)
- **Authentication issues?** See [Auth Issues Resolved](./5_docs/TBR/1_AUTH_ISSUES_RESOLVED.md)
- **Deployment problems?** Check [Deployment Status](./DEPLOYMENT_STATUS.md)
- **Testing questions?** See [Testing Index](./TESTING_INDEX.md)
- **API questions?** Check [Practice API Summary](./PRACTICE_API_SUMMARY.md)

### Troubleshooting by Topic
- **Claims**: [Claims Search 403 Fix](./CLAIMS_SEARCH_403_FIX.md)
- **Bulk Upload**: [Bulk Upload Fix](./help/troubleshooting/BULK_UPLOAD_FIX.md)
- **CORS**: [Fix CORS Keycloak](./help/troubleshooting/FIX_CORS_KEYCLOAK.md)
- **Timeout**: [Fix Claim Search Timeout](./help/troubleshooting/FIX_CLAIM_SEARCH_TIMEOUT.md)
- **Login**: [Fix Login Issue](./5_docs/fixes/FIX_LOGIN_ISSUE.md)

---

## 📝 Recent Updates

### November 15, 2025
- ✅ **Pagination Fix**: Added UHC API pagination support (up to 500 claims)
- ✅ **Status Filter**: Pre-filter claims before fetching details
- ✅ **CI/CD Planning**: Documented requirements for production
- 📋 **TODO Before Prod**: Created comprehensive production checklist

### Previous Updates
- [Claims Display Updates](./CLAIMS_DISPLAY_UPDATES.md)
- [Bulk Upload Template Added](./BULK_UPLOAD_TEMPLATE_ADDED.md)
- [Role Management Fixes](./ROLE_MANAGEMENT_FIXES_SUMMARY.md)
- [GitHub Actions Success](./GITHUB_ACTIONS_SUCCESS.md)

---

## 🗂️ Documentation Folders

- **`/5_docs/`** - Main documentation (organized by topic)
- **`/help/`** - User help documentation
- **`/docs/`** - Setup and configuration guides
- **`/scripts/`** - Deployment and utility scripts
- **`/testcases/`** - Test cases and test documentation
- **`/testing/`** - Testing guides and results
- **`/10_test-results/`** - Test execution results

---

## 🔍 Search Tips

Can't find what you need? Try searching for:
- **"Quick"** - Fast start guides
- **"Fix"** - Troubleshooting guides
- **"Setup"** - Configuration guides
- **"API"** - API documentation
- **"Guide"** - Step-by-step guides
- **"Summary"** - Overview documents

---

**📌 Bookmark this page** - It's your central hub for all ConnectMe documentation!

**Last Updated**: November 15, 2025  
**Maintained By**: Development Team  
**Questions?** Check the troubleshooting section or review recent updates above.

