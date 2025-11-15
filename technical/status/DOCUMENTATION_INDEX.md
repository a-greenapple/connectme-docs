# ConnectMe Documentation Index

**Last Updated:** November 13, 2024  
**Version:** 1.0

This is the master index for all ConnectMe project documentation. Documents are organized by category for easy navigation.

---

## 📚 Table of Contents

- [Quick Start Guides](#-quick-start-guides)
- [Admin & Configuration](#-admin--configuration)
- [Troubleshooting & Fixes](#-troubleshooting--fixes)
- [Features & Enhancements](#-features--enhancements)
- [Deployment & Infrastructure](#-deployment--infrastructure)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Development Guides](#-development-guides)
- [Sample Data & Templates](#-sample-data--templates)
- [Scripts & Automation](#-scripts--automation)
- [Help Documentation (User-Facing)](#-help-documentation-user-facing)

---

## 🚀 Quick Start Guides

### For New Users
- **[Help Portal](help/index.html)** - Interactive documentation portal
- **[User Guide](help/user/index.html)** - End-user documentation
- **[Getting Started](help/user/getting-started.html)** - First-time setup

### For Administrators
- **[Admin Guide](help/admin/index.html)** - Administrator overview
- **[Permissions Setup](help/admin/permissions.html)** - How to set user permissions
- **[User Management Setup](docs/USER_MANAGEMENT_SETUP.md)** - Complete setup guide

### For Developers
- **[Developer Guide](help/developer/index.html)** - Technical documentation
- **[Local Setup](LOCAL-SETUP.md)** - Development environment setup
- **[Frontend Quick Start](FRONTEND_QUICK_START.md)** - Frontend development guide

---

## ⚙️ Admin & Configuration

### User Management & Permissions
- **[Roles & Permissions Guide](help/admin/permissions.html)** - Complete permission setup (HTML)
- **[Roles & Permissions (MD)](help/admin/permissions.md)** - Markdown version
- **[Role Management Fixes Summary](ROLE_MANAGEMENT_FIXES_SUMMARY.md)** - Recent role fixes
- **[Role Management Audit](ROLE_MANAGEMENT_AUDIT.md)** - Role system audit
- **[Admin Login Fix](ADMIN_LOGIN_FIX.md)** - Fix admin login issues

### Keycloak Configuration
- **[Keycloak Admin Setup](KEYCLOAK_ADMIN_SETUP.md)** - Initial Keycloak setup
- **[Keycloak Permissions Fix](KEYCLOAK_PERMISSIONS_FIX.md)** - Permission configuration
- **[Keycloak CORS Fix](FIX_CORS_KEYCLOAK.md)** - CORS configuration
- **[Keycloak CORS Manual Fix](FIX_KEYCLOAK_CORS_MANUAL.md)** - Manual CORS setup
- **[Setup Keycloak Script](setup-keycloak.sh)** - Automated setup script
- **[Fix Admin Login Script](fix_admin_login.sh)** - Automated admin fix

### System Configuration
- **[Pre-Prod Configuration](PREPROD_CONFIGURATION.md)** - Pre-production setup
- **[Pre-Prod Setup Guide](docs/PREPROD_SETUP_GUIDE.md)** - Detailed setup
- **[Pre-Prod Summary](docs/PREPROD_SUMMARY.md)** - Environment summary
- **[Environment Example](env.example)** - Environment variables template

---

## 🔧 Troubleshooting & Fixes

### Common Issues
- **[Troubleshooting Guide](help/troubleshooting/index.html)** - Main troubleshooting hub
- **[Login Issues](help/troubleshooting/login-issues.html)** - Can't login? Start here
- **[CORS Errors](help/troubleshooting/cors-errors.html)** - CORS error solutions
- **[Timeout Errors](help/troubleshooting/timeout-errors.html)** - Timeout fixes

### Specific Fixes
- **[Quick CORS Fix](QUICK_FIX_CORS.md)** - One-page CORS fix
- **[Debug CORS Error](DEBUG_CORS_ERROR.md)** - CORS debugging guide
- **[Claim Search Timeout Fix](FIX_CLAIM_SEARCH_TIMEOUT.md)** - Timeout resolution
- **[Claims Search 403 Fix](CLAIMS_SEARCH_403_FIX.md)** - Permission error fix
- **[Bulk Upload Troubleshooting](TROUBLESHOOT_BULK_UPLOAD.md)** - Bulk upload diagnostics

### Recent Fixes (November 2024)
- **[Bulk Upload Empty Results Fix](BULK_UPLOAD_EMPTY_RESULTS_FIX.md)** ⭐ **NEW** - Fix for empty results display
- **[Bulk Upload Fix](BULK_UPLOAD_FIX.md)** - General bulk upload fixes

---

## ✨ Features & Enhancements

### Bulk Upload
- **[Bulk Upload Guide](help/user/bulk-upload.html)** - User guide
- **[Bulk Upload Template Added](BULK_UPLOAD_TEMPLATE_ADDED.md)** - Template feature
- **[Bulk Upload History Features](BULK_UPLOAD_HISTORY_FEATURES.md)** - History tracking
- **[Bulk Upload Empty Results Fix](BULK_UPLOAD_EMPTY_RESULTS_FIX.md)** ⭐ **LATEST FIX**

### Claims Management
- **[Claims Search Guide](help/user/claims-search.html)** - Search functionality
- **[Claims Display Updates](CLAIMS_DISPLAY_UPDATES.md)** - UI improvements
- **[Claims UI Guide](CLAIMS_UI_GUIDE.md)** - User interface guide
- **[Claims Filtering Implementation](CLAIMS_FILTERING_IMPLEMENTATION.md)** - Filter features
- **[Claims Enhancements Plan](CLAIMS_ENHANCEMENTS_PLAN.md)** - Future enhancements
- **[Line Level Claim Codes](LINE_LEVEL_CLAIM_CODES.md)** - Claim code details

### Practice Management
- **[Practice API Summary](PRACTICE_API_SUMMARY.md)** - API documentation
- **[Practice Selector Implementation](PRACTICE_SELECTOR_IMPLEMENTATION.md)** - Practice selection
- **[New Practice Access Model](NEW_PRACTICE_ACCESS_MODEL.md)** - Access control
- **[Adding Practices](ADDING_PRACTICES.md)** - How to add practices

### Frontend Enhancements
- **[Frontend Filtering Enhancement](FRONTEND_FILTERING_ENHANCEMENT.md)** - Filter improvements
- **[Frontend Quick Start](FRONTEND_QUICK_START.md)** - Development guide

---

## 🚢 Deployment & Infrastructure

### Deployment Guides
- **[Deployment Summary](DEPLOYMENT_SUMMARY.md)** - Deployment overview
- **[Deployment Status](DEPLOYMENT_STATUS.md)** - Current status
- **[Pre-Prod UHC Update Guide](PREPROD_UHC_UPDATE_GUIDE.md)** - UHC updates
- **[UHC Pre-Prod Update Summary](UHC_PREPROD_UPDATE_SUMMARY.md)** - Update summary

### CI/CD
- **[GitHub Actions Success](GITHUB_ACTIONS_SUCCESS.md)** - CI/CD setup
- **[Git Branching Strategy](GIT_BRANCHING_STRATEGY.md)** - Branch management
- **[Git Push Resolved](GIT_PUSH_RESOLVED.md)** - Git issue resolution
- **[Branching Setup Complete](BRANCHING_SETUP_COMPLETE.md)** - Branch setup

### Architecture
- **[Healthcare Architecture Doc](healthcare_arch_doc.html)** - System architecture
- **[Development Phases](dev_deployment_phases.html)** - Development roadmap

---

## 🧪 Testing & Quality Assurance

### Testing Guides
- **[Test Guide](TEST_GUIDE.md)** - Testing overview
- **[Testing Suite Summary](TESTING_SUITE_SUMMARY.md)** - Test suite details

### Test Scripts
- **[Test Bulk Claim Search](test_bulk_claim_search.py)** - Bulk search tests
- **[Test Role Management](test_role_management.py)** - Role testing (if exists)

### Test Results
- **[Test Results Directory](10_test-results/)** - All test results
- **[Test Fixes Summary](10_test-results/TEST_FIXES_SUMMARY.md)** - Test fixes

---

## 💻 Development Guides

### Setup & Configuration
- **[Local Setup](LOCAL-SETUP.md)** - Local development setup
- **[Frontend Quick Start](FRONTEND_QUICK_START.md)** - Frontend setup
- **[Environment Setup](env.example)** - Environment configuration

### Code Organization
- **[Backend Code](connectme-backend/)** - Django backend
- **[Frontend Code](connectme-frontend/)** - Next.js frontend
- **[Scripts Directory](scripts/)** - Utility scripts

### Documentation
- **[Complete Summary](COMPLETE_SUMMARY.md)** - Project summary
- **[Chat Summary](CHAT_SUMMARY.md)** - Development chat log

---

## 📄 Sample Data & Templates

### CSV Templates
- **[CSV Templates Directory](csv-templates/)** - All CSV templates
- **[Sample Bulk Claims (Real)](sample_bulk_claims_real.csv)** - Realistic test data
- **[Sample Bulk Claims (With Claim Numbers)](sample_bulk_claims_with_real_claim_numbers.csv)** - Quick test data
- **[Sample Data README](SAMPLE_DATA_README.md)** - How to use sample data

### Configuration Files
- **[Keycloak Config (Full)](keycloak-connectme-preprod-config.json)** - Complete config
- **[Keycloak Config (Simple)](keycloak-connectme-preprod-simple.json)** - Simplified config
- **[Environment Example](env.example)** - .env template

---

## 🤖 Scripts & Automation

### Admin Scripts
- **[Fix Admin Login](fix_admin_login.sh)** - Fix admin access
- **[Setup Keycloak](setup-keycloak.sh)** - Keycloak setup automation
- **[Service Script](service.sh)** - Service management

### Utility Scripts
- **[Scripts Directory](scripts/)** - All utility scripts
  - Deployment scripts
  - Database scripts
  - Testing scripts
  - Monitoring scripts

---

## 📖 Help Documentation (User-Facing)

### Main Portal
- **[Help Center](help/index.html)** ⭐ **START HERE** - Main documentation hub
- **[Help README](help/README.md)** - Documentation guide

### Admin Documentation
- **[Admin Overview](help/admin/index.html)** - Admin guide home
- **[Admin Overview (MD)](help/admin/index.md)** - Markdown version
- **[Permissions Guide](help/admin/permissions.html)** - Permission setup
- **[Permissions Guide (MD)](help/admin/permissions.md)** - Markdown version

### User Documentation
- **[User Overview](help/user/index.html)** - User guide home
- **[Getting Started](help/user/getting-started.html)** - First steps
- **[Claims Search](help/user/claims-search.html)** - Search guide
- **[Bulk Upload](help/user/bulk-upload.html)** - Bulk upload guide
- **[Workflow Management](help/user/workflow.html)** - Workflow guide
- **[Search History](help/user/history.html)** - History guide

### Developer Documentation
- **[Developer Overview](help/developer/index.html)** - Developer guide home
- **[API Reference](help/developer/api-reference.html)** - API docs
- **[Architecture](help/developer/architecture.html)** - System design
- **[Authentication](help/developer/authentication.html)** - Auth details
- **[Integration Guide](help/developer/integration.html)** - Integration
- **[Testing Guide](help/developer/testing.html)** - Testing

### Troubleshooting Documentation
- **[Troubleshooting Overview](help/troubleshooting/index.html)** - Main troubleshooting
- **[Login Issues](help/troubleshooting/login-issues.html)** - Login help
- **[CORS Errors](help/troubleshooting/cors-errors.html)** - CORS help
- **[Timeout Errors](help/troubleshooting/timeout-errors.html)** - Timeout help
- **[Bulk Upload Issues](help/troubleshooting/bulk-upload-issues.html)** - Bulk help
- **[FAQ](help/troubleshooting/faq.html)** - Frequently asked questions

---

## 🗂️ Legacy Documentation

Older documentation is organized in the `5_docs/` directory:

- **[5_docs/1_1_CLAIMS/](5_docs/1_1_CLAIMS/)** - Claims documentation archive
- **[5_docs/1_2_BULK/](5_docs/1_2_BULK/)** - Bulk upload documentation archive
- **[5_docs/1_Guide/](5_docs/1_Guide/)** - General guides archive
- **[5_docs/keycloak/](5_docs/keycloak/)** - Keycloak documentation archive
- **[5_docs/deployment/](5_docs/deployment/)** - Deployment documentation archive
- **[5_docs/fixes/](5_docs/fixes/)** - Historical fixes
- **[5_docs/testing/](5_docs/testing/)** - Testing documentation archive
- **[5_docs/TBR/](5_docs/TBR/)** - To be reviewed/refactored

---

## 🔍 Quick Reference

### Most Important Documents

1. **[Help Portal](help/index.html)** - Start here for all documentation
2. **[Admin Permissions Guide](help/admin/permissions.html)** - Set up user access
3. **[Bulk Upload Empty Results Fix](BULK_UPLOAD_EMPTY_RESULTS_FIX.md)** - Latest critical fix
4. **[Troubleshooting Guide](help/troubleshooting/index.html)** - Problem solving
5. **[Local Setup](LOCAL-SETUP.md)** - Development environment

### Recently Updated (November 13, 2024)

- ⭐ **[Bulk Upload Empty Results Fix](BULK_UPLOAD_EMPTY_RESULTS_FIX.md)** - Fix for empty results display
- ⭐ **[Help Portal](help/index.html)** - New interactive documentation hub
- ⭐ **[Admin Permissions Guide](help/admin/permissions.html)** - Complete permission setup
- ⭐ **[Troubleshooting Guides](help/troubleshooting/)** - Comprehensive troubleshooting

### Key Scripts

- **[fix_admin_login.sh](fix_admin_login.sh)** - Fix admin access issues
- **[setup-keycloak.sh](setup-keycloak.sh)** - Automate Keycloak setup
- **[service.sh](service.sh)** - Manage services

### Sample Data

- **[sample_bulk_claims_real.csv](sample_bulk_claims_real.csv)** - 20 realistic test claims
- **[sample_bulk_claims_with_real_claim_numbers.csv](sample_bulk_claims_with_real_claim_numbers.csv)** - 10 quick test claims

---

## 📞 Getting Help

### Documentation Issues
- Check the **[Help Portal](help/index.html)** first
- Review **[Troubleshooting Guides](help/troubleshooting/index.html)**
- Search this index for relevant documents

### Technical Support
- **Email:** support@totessoft.com
- **Documentation Feedback:** Submit via project repository

### Contributing to Documentation
- Follow the structure outlined in **[Help README](help/README.md)**
- Update this index when adding new documents
- Keep legacy docs in `5_docs/` directory

---

## 📊 Document Statistics

- **Total Documentation Files:** 100+
- **Help Portal Pages:** 20+
- **Troubleshooting Guides:** 10+
- **Sample Data Files:** 15+
- **Automation Scripts:** 50+

---

## 🔄 Maintenance

### Regular Updates
- Update this index when adding new documentation
- Archive old documents to `5_docs/` directory
- Keep "Recently Updated" section current
- Review and update legacy documentation quarterly

### Version History
- **v1.0** (November 13, 2024) - Initial organized documentation index

---

**ConnectMe Healthcare Claims Management System**  
**Documentation maintained by:** TotesSoft Development Team  
**Last Updated:** November 13, 2024

