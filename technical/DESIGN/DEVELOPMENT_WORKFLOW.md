# Development Workflow Guide

## 📋 Overview

This guide explains how to develop locally and deploy to the remote production server.

---

## 🔄 Development Workflow

### **1. Local Development**

#### **Setup Local Environment**

**Backend:**
```bash
cd connectme-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt
cp .env.example .env
# Edit .env with your local settings
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd connectme-frontend
npm install
cp .env.example .env.local
# Edit .env.local with your local settings
npm run dev
```

#### **Local Environment Variables**

**Backend (.env):**
```env
DEBUG=True
SECRET_KEY=your-local-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/connectme_dev
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Keycloak
KEYCLOAK_SERVER_URL=https://auth.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-backend
KEYCLOAK_CLIENT_SECRET=your-client-secret

# Encryption
ENCRYPTION_KEY=your-local-encryption-key
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
NEXT_PUBLIC_APP_NAME=ConnectMe
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

---

### **2. Git Workflow**

#### **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

#### **Make Changes and Commit**
```bash
git add .
git commit -m "feat: your feature description"
```

#### **Push to GitHub**
```bash
git push origin feature/your-feature-name
```

#### **Create Pull Request**
- Go to GitHub
- Create PR from your feature branch to `main`
- Review and merge

---

### **3. Deployment to Production**

#### **Method 1: Git Pull on Server**

```bash
# SSH into server
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

# Backend
cd /var/www/connectme-backend
git pull origin main
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart connectme-backend

# Frontend
cd /var/www/connectme-frontend
git pull origin main
npm install
npm run build
pm2 restart connectme-frontend
```

#### **Method 2: Automated Deployment Script**

Create `deploy.sh`:
```bash
#!/bin/bash

# Deploy backend
ssh connectme@20.84.160.240 << 'ENDSSH'
cd /var/www/connectme-backend
git pull origin main
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart connectme-backend
ENDSSH

# Deploy frontend
ssh connectme@20.84.160.240 << 'ENDSSH'
cd /var/www/connectme-frontend
git pull origin main
npm install
npm run build
pm2 restart connectme-frontend
ENDSSH

echo "✅ Deployment complete!"
```

---

## 🔑 Key Files Synced from Production

The following files have been updated with production fixes:

### **Backend:**
- ✅ `apps/users/views.py` - Mock login with organization support
- ✅ `config/settings.py` - CORS, dotenv loading, allowed hosts
- ✅ `config/wsgi.py` - Fixed module path
- ✅ `config/asgi.py` - Fixed module path
- ✅ `config/urls.py` - Added log viewer

### **Frontend:**
- ✅ `src/app/auth/page.tsx` - Fixed API URL, added credentials
- ✅ `next.config.ts` - Ignore lint errors during build

### **Production-Only Files (Not in Git):**
- `/var/www/connectme-backend/.env`
- `/var/www/connectme-frontend/.env.production`
- `/var/www/connectme-backend/staticfiles/` (generated)

---

## 📝 Important Notes

### **Never Commit to Git:**
- `.env` files (use `.env.example` instead)
- `venv/` directory
- `node_modules/` directory
- `staticfiles/` directory
- `.next/` build directory
- Database files (`db.sqlite3`, `*.db`)
- SSL certificates
- API keys and secrets

### **Environment-Specific Settings:**

**Local Development:**
- Uses `DEBUG=True`
- Uses local database
- CORS allows `localhost:3000`
- No SSL required

**Production:**
- Uses `DEBUG=False`
- Uses PostgreSQL database
- CORS allows `connectme.apps.totesoft.com`
- SSL enabled

---

## 🚀 Quick Commands

### **Start Local Development:**
```bash
# Terminal 1: Backend
cd connectme-backend && source venv/bin/activate && python manage.py runserver

# Terminal 2: Frontend  
cd connectme-frontend && npm run dev
```

### **Deploy to Production:**
```bash
# From your local machine
./deploy.sh

# Or manually
ssh connectme@20.84.160.240 "cd /var/www/connectme-backend && git pull && sudo systemctl restart connectme-backend"
ssh connectme@20.84.160.240 "cd /var/www/connectme-frontend && git pull && npm run build && pm2 restart connectme-frontend"
```

### **Check Production Logs:**
```bash
# Backend logs
ssh connectme@20.84.160.240 "sudo journalctl -u connectme-backend -f"

# Frontend logs
ssh connectme@20.84.160.240 "pm2 logs connectme-frontend"
```

---

## ✅ Current Status

### **Local (Your Machine):**
- ✅ Backend code synced
- ✅ Frontend code synced
- 🔧 Need to set up local `.env` files

### **Production (Server):**
- ✅ Backend running: https://connectme.be.totesoft.com
- ✅ Frontend running: https://connectme.apps.totesoft.com
- ✅ SSL enabled
- ✅ All services auto-start on boot

---

## 🔧 Troubleshooting

### **CORS Errors:**
- Check `CORS_ALLOWED_ORIGINS` in backend `.env`
- Ensure frontend domain is included
- Restart backend after changes

### **Build Errors:**
- Frontend: Check `next.config.ts` has `ignoreDuringBuilds: true`
- Backend: Ensure all dependencies are installed

### **Deployment Failures:**
- Check git remote is correct
- Ensure SSH key has proper permissions
- Verify user has write access to deployment directories

---

**Last Updated:** January 9, 2025

