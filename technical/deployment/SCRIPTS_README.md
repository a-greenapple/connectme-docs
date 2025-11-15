# Service Management Scripts

This directory contains scripts to manage ConnectMe services in both local and production environments.

---

## 📋 Available Scripts

### **Local Development Scripts**

| Script | Purpose | Usage |
|--------|---------|-------|
| `local-start.sh` | Start backend and frontend locally | `./scripts/local-start.sh` |
| `local-stop.sh` | Stop local services | `./scripts/local-stop.sh` |
| `local-logs.sh` | View local logs | `./scripts/local-logs.sh [backend\|frontend\|both]` |

### **Remote Production Scripts**

| Script | Purpose | Usage |
|--------|---------|-------|
| `deploy.sh` | Deploy to production | `./scripts/deploy.sh [backend\|frontend\|both]` |
| `remote-restart.sh` | Restart production services | `./scripts/remote-restart.sh [backend\|frontend\|both]` |
| `remote-status.sh` | Check production status | `./scripts/remote-status.sh` |
| `remote-logs.sh` | View production logs | `./scripts/remote-logs.sh [backend\|frontend\|nginx\|all]` |
| `remote-stop.sh` | Stop production services | `./scripts/remote-stop.sh [backend\|frontend\|both]` |

---

## 🚀 Quick Start

### **First Time Setup**

1. **Make scripts executable:**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Set up local environment:**
   ```bash
   # See DEVELOPMENT_WORKFLOW.md for detailed setup
   ./scripts/local-start.sh
   ```

---

## 📖 Usage Examples

### **Local Development**

```bash
# Start local services
./scripts/local-start.sh

# View logs
./scripts/local-logs.sh both

# Stop services
./scripts/local-stop.sh
```

### **Production Deployment**

```bash
# Check production status
./scripts/remote-status.sh

# Deploy changes
./scripts/deploy.sh both

# Restart services
./scripts/remote-restart.sh both

# View logs (follow mode)
./scripts/remote-logs.sh backend -f

# View last 100 lines
./scripts/remote-logs.sh frontend -n 100
```

---

## 🔧 Script Details

### **local-start.sh**
Starts Django (port 8000) and Next.js (port 3000) in background processes.

**Features:**
- ✅ Checks if ports are already in use
- ✅ Creates log files in `/tmp/`
- ✅ Saves PIDs for later stopping
- ✅ Verifies environment files exist

**Logs:**
- Backend: `/tmp/connectme-backend.log`
- Frontend: `/tmp/connectme-frontend.log`

---

### **local-stop.sh**
Stops local services gracefully.

**Features:**
- ✅ Kills processes by PID
- ✅ Kills any remaining processes on ports 8000 and 3000
- ✅ Cleans up PID files

---

### **local-logs.sh**
View local development logs.

**Options:**
- `backend` - Backend logs only
- `frontend` - Frontend logs only
- `both` - Both logs (default)

**Usage:**
```bash
./scripts/local-logs.sh backend
```

---

### **deploy.sh**
Deploy code to production server.

**What it does:**
1. SSH into production server
2. Pull latest code from GitHub
3. Install dependencies
4. Run migrations (backend)
5. Collect static files (backend)
6. Build production bundle (frontend)
7. Restart services

**Usage:**
```bash
# Deploy everything
./scripts/deploy.sh

# Deploy backend only
./scripts/deploy.sh backend

# Deploy frontend only
./scripts/deploy.sh frontend
```

---

### **remote-restart.sh**
Restart services on production server.

**What it does:**
- Backend: `systemctl restart connectme-backend`
- Frontend: `pm2 restart connectme-frontend`
- Verifies services started successfully

**Usage:**
```bash
# Restart both
./scripts/remote-restart.sh

# Restart backend only
./scripts/remote-restart.sh backend
```

---

### **remote-status.sh**
Check status of all production services.

**Shows:**
- ✅ Backend service status and uptime
- ✅ Frontend service status and uptime
- ✅ PostgreSQL status
- ✅ Nginx status
- ✅ Disk usage
- ✅ Memory usage
- ✅ SSL certificate expiry

**Usage:**
```bash
./scripts/remote-status.sh
```

---

### **remote-logs.sh**
View production logs.

**Options:**
- `backend` - Django/Gunicorn logs
- `frontend` - PM2/Next.js logs
- `nginx` - Nginx access and error logs
- `all` - Last 50 lines of all logs (default)

**Flags:**
- `-f`, `--follow` - Follow logs in real-time
- `-n`, `--lines N` - Show last N lines

**Usage:**
```bash
# Follow backend logs
./scripts/remote-logs.sh backend -f

# Show last 100 frontend logs
./scripts/remote-logs.sh frontend -n 100

# Show all recent logs
./scripts/remote-logs.sh all
```

---

### **remote-stop.sh**
Stop production services (⚠️ USE WITH CAUTION).

**What it does:**
- Stops backend systemd service
- Stops frontend PM2 process
- Requires confirmation

**Usage:**
```bash
./scripts/remote-stop.sh both
```

---

## 🔒 Security Notes

- Scripts use SSH key authentication
- Default SSH key: `~/Documents/Access/cursor/id_rsa_Debian`
- Server: `connectme@20.84.160.240`
- No passwords required

---

## 🐛 Troubleshooting

### **Permission Denied**
```bash
chmod +x scripts/*.sh
```

### **SSH Connection Failed**
Check that your SSH key exists:
```bash
ls -la ~/Documents/Access/cursor/id_rsa_Debian
```

### **Service Won't Start**
Check logs:
```bash
./scripts/remote-logs.sh backend -n 100
```

---

## 📝 Adding New Scripts

When creating new scripts:

1. Add shebang: `#!/bin/bash`
2. Set error handling: `set -e`
3. Add help function: `show_help()`
4. Use color codes for better UX
5. Make executable: `chmod +x scripts/your-script.sh`
6. Document in this README

---

## 🔄 Workflow Summary

```
┌─────────────┐
│ Local Dev   │  ./local-start.sh
│ (Port 8000) │  Make changes
│ (Port 3000) │  Test locally
└──────┬──────┘
       │
       ├─ git commit & push
       │
       ▼
┌─────────────┐
│   GitHub    │  Code repository
│   Repos     │  Version control
└──────┬──────┘
       │
       ├─ ./deploy.sh
       │
       ▼
┌─────────────┐
│ Production  │  ./remote-status.sh
│  (20.84...  │  ./remote-logs.sh -f
│   240)      │  ./remote-restart.sh
└─────────────┘
```

---

**Last Updated:** January 9, 2025  
**Maintained by:** ConnectMe Team

