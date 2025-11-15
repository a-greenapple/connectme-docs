# ConnectMe Healthcare Platform

A HIPAA-compliant healthcare platform for claims and eligibility management with Keycloak authentication.

---

## 🚀 Quick Start

### **Check Production Status:**
```bash
./service.sh remote status
```

### **Start Local Development:**
```bash
./service.sh local start
```

### **Deploy to Production:**
```bash
./service.sh remote deploy
```

---

## 📊 Live Production URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | https://connectme.apps.totesoft.com | Mock Login (no credentials) |
| **Backend API** | https://connectme.be.totesoft.com/api/v1/ | - |
| **Admin Panel** | https://connectme.be.totesoft.com/admin/ | admin / admin123 |
| **Audit Logs** | https://connectme.be.totesoft.com/admin/auditlog/logentry/ | admin / admin123 |

---

## 📁 Project Structure

```
connectme/
├── connectme-backend/       # Django backend
├── connectme-frontend/      # Next.js frontend
├── scripts/                 # Service management scripts
│   ├── local-start.sh      # Start local dev
│   ├── local-stop.sh       # Stop local dev
│   ├── local-logs.sh       # View local logs
│   ├── deploy.sh           # Deploy to production
│   ├── remote-restart.sh   # Restart production
│   ├── remote-status.sh    # Check production status
│   ├── remote-logs.sh      # View production logs
│   └── remote-stop.sh      # Stop production
├── service.sh              # Master service manager
├── QUICK_REFERENCE.md      # Command quick reference
├── DEVELOPMENT_WORKFLOW.md # Development guide
└── PRODUCTION_CHANGES.md   # Production changes log
```

---

## 🔧 Service Management

### **Master Command:**
```bash
./service.sh <environment> <action> [service]
```

### **Common Commands:**

| Task | Command |
|------|---------|
| **Start local dev** | `./service.sh local start` |
| **Check prod status** | `./service.sh remote status` |
| **Deploy to prod** | `./service.sh remote deploy` |
| **View prod logs** | `./service.sh remote logs backend` |
| **Restart prod** | `./service.sh remote restart` |

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for more examples.

---

## 🏗️ Architecture

### **Backend (Django + PostgreSQL)**
- Django 5.2 + Django REST Framework
- PostgreSQL 15 database
- Gunicorn WSGI server
- Keycloak authentication
- Audit logging with django-auditlog

### **Frontend (Next.js + React)**
- Next.js 15.5.4 with Turbopack
- TypeScript + Tailwind CSS
- PM2 process manager
- SSR and static generation

### **Infrastructure**
- Nginx reverse proxy
- Let's Encrypt SSL (auto-renewing)
- Debian 12 server
- Systemd service management

---

## 🔄 Development Workflow

### **1. Local Development**
```bash
# Start services
./service.sh local start

# Make changes to code
# Test at http://localhost:3000

# View logs if needed
./service.sh local logs both

# Stop when done
./service.sh local stop
```

### **2. Deploy to Production**
```bash
# Commit changes
git add .
git commit -m "Your changes"
git push origin main

# Deploy
./service.sh remote deploy

# Check status
./service.sh remote status

# Monitor logs
./service.sh remote logs backend -f
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Quick command reference |
| **[DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)** | Complete development guide |
| **[PRODUCTION_CHANGES.md](PRODUCTION_CHANGES.md)** | Production changes log |
| **[CURRENT_STATE.md](CURRENT_STATE.md)** | Current status summary |
| **[scripts/README.md](scripts/README.md)** | Script documentation |

---

## 🔐 Security

- SSL/TLS encryption on all production traffic
- CORS properly configured
- Keycloak SSO integration
- HIPAA-compliant audit logging
- Environment variables not in git
- Encrypted sensitive data

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL 15
- Gunicorn
- Keycloak
- Redis (optional)

**Frontend:**
- Node.js 20.x
- Next.js 15.5.4
- React 19
- TypeScript
- Tailwind CSS
- PM2

**Infrastructure:**
- Nginx 1.22.1
- Certbot (Let's Encrypt)
- Systemd
- Debian 12

---

## 📞 Server Information

- **IP:** 20.84.160.240
- **SSH:** `ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240`
- **User:** connectme
- **OS:** Debian 12 (Bookworm)
- **Resources:** 3.8GB RAM, 30GB Disk, 2 CPU cores

---

## 🔑 Important Files

### **Backend:**
- `config/settings.py` - Django settings
- `apps/users/views.py` - Authentication views
- `.env` - Environment variables (NOT in git)

### **Frontend:**
- `src/app/auth/page.tsx` - Authentication page
- `next.config.ts` - Build configuration
- `.env.local` - Local environment (NOT in git)
- `.env.production` - Production environment (NOT in git, on server)

---

## 🎯 First Time Setup

### **Local Development:**

1. **Backend:**
   ```bash
   cd connectme-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements/development.txt
   cp .env.example .env  # Edit with your settings
   python manage.py migrate
   ```

2. **Frontend:**
   ```bash
   cd connectme-frontend
   npm install
   cp .env.example .env.local  # Edit with your settings
   ```

3. **Start Services:**
   ```bash
   ./service.sh local start
   ```

---

## 🆘 Troubleshooting

### **Service won't start:**
```bash
./service.sh local logs both
```

### **Deployment failed:**
```bash
./service.sh remote logs backend -n 100
./service.sh remote status
```

### **CORS errors:**
```bash
# Check backend CORS settings
ssh connectme@20.84.160.240 "grep CORS /var/www/connectme-backend/.env"

# Restart backend
./service.sh remote restart backend
```

---

## 📖 Additional Resources

- **Keycloak Admin:** https://auth.totesoft.com/admin/
- **GitHub Backend:** https://github.com/a-greenapple/connectme-backend
- **GitHub Frontend:** https://github.com/a-greenapple/connectme-frontend

---

**Version:** 1.0.0  
**Last Updated:** January 9, 2025  
**Status:** ✅ Production Running

**Quick Help:** Run `./service.sh` for usage information
EOF
echo "✅ README.md created"
