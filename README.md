# ConnectMe Documentation

**Official documentation for the ConnectMe healthcare claims management platform**

🌐 **View Documentation**: [https://a-greenapple.github.io/connectme-docs/](https://a-greenapple.github.io/connectme-docs/)

---

## 📚 Quick Links

- **[Documentation Hub](./index.html)** - Main documentation portal
- **[Quick Start Guide](./5_docs/1_Guide/QUICK_REFERENCE.md)** - Get started quickly
- **[Admin Guide](./help/admin/index.md)** - For administrators
- **[Troubleshooting](./help/troubleshooting/)** - Common issues and fixes
- **[TODO Before Production](./docs/deployment/TODO_BEFORE_PROD.md)** - ⚠️ Production checklist

---

## 📖 Documentation Structure

```
connectme-docs/
├── index.html                      # Main documentation hub (GitHub Pages)
├── DOCUMENTATION_HUB.md           # Markdown version of hub
├── docs/                          # Main documentation
│   ├── guides/                    # Setup and quick start guides
│   ├── features/                  # Feature documentation
│   ├── deployment/                # Deployment guides
│   ├── troubleshooting/          # Fixes and solutions
│   ├── testing/                   # Testing documentation
│   ├── keycloak/                  # Authentication docs
│   └── git/                       # Git workflow
├── 5_docs/                        # Organized technical docs
│   ├── 1_1_CLAIMS/               # Claims system
│   ├── 1_2_BULK/                 # Bulk upload
│   ├── 1_Guide/                  # Comprehensive guides
│   ├── keycloak/                 # Keycloak integration
│   ├── monitoring/               # System monitoring
│   ├── testing/                  # Test documentation
│   └── workflow/                 # Workflow system
├── help/                          # User help documentation
│   ├── admin/                    # Admin help
│   └── troubleshooting/          # User troubleshooting
├── testcases/                     # Test cases and scripts
└── testing/                       # Test results and guides
```

---

## 🚀 Local Development

To view the documentation locally:

```bash
# Clone the repository
git clone https://github.com/a-greenapple/connectme-docs.git
cd connectme-docs

# Open in browser
open index.html
```

---

## 🌐 GitHub Pages

This documentation is automatically published to GitHub Pages at:
**https://a-greenapple.github.io/connectme-docs/**

Any push to the `main` branch will automatically update the live documentation.

---

## 📝 Contributing

To update documentation:

1. Edit the relevant `.md` or `.html` files
2. Commit and push to `main` branch
3. GitHub Pages will automatically rebuild (usually within 1-2 minutes)

---

## 📋 Documentation Categories

### For New Users
- Quick Start Guide
- Frontend Quick Start
- Complete Setup Guide

### For Administrators
- Admin Index
- User Management Setup
- Keycloak Admin Setup
- Monitoring System

### For Developers
- Local Setup
- Provider Architecture
- API Documentation
- Testing Guide

### For DevOps
- Deployment Checklist
- Server Setup
- Deployment Scripts
- TODO Before Production ⚠️

---

## 🆘 Need Help?

- **Can't find something?** Use the search in the [Documentation Hub](./index.html)
- **Found an issue?** Open an issue in the main ConnectMe repository
- **Have a question?** Check the [Troubleshooting](./help/troubleshooting/) section

---

## 📌 Related Repositories

- **[connectme-backend](https://github.com/a-greenapple/connectme-backend)** - Backend API
- **[connectme-frontend](https://github.com/a-greenapple/connectme-frontend)** - Frontend UI

---

**Last Updated**: November 15, 2025  
**Maintained By**: ConnectMe Development Team
