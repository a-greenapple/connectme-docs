# 🔧 Frontend Server Troubleshooting Guide

## Issue: Cannot connect to http://localhost:3000

### Quick Fix - Option 1: Use the Startup Script

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_FRONTEND.sh
```

This will:
- Check if dependencies are installed
- Start the Next.js dev server
- Show you all available URLs

---

### Quick Fix - Option 2: Manual Start

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend
npm run dev
```

Wait for the message:
```
✓ Ready in X.Xs
○ Local:        http://localhost:3000
```

---

## Common Issues & Solutions

### 1. Port 3000 Already in Use

**Error:** `Port 3000 is already in use`

**Solution A - Kill the process:**
```bash
lsof -ti:3000 | xargs kill -9
npm run dev
```

**Solution B - Use a different port:**
```bash
PORT=3001 npm run dev
```

---

### 2. Dependencies Not Installed

**Error:** `Cannot find module 'next'` or similar

**Solution:**
```bash
cd frontend
npm install
npm run dev
```

---

### 3. Node Version Issues

**Error:** `Unsupported engine` or version errors

**Check your Node version:**
```bash
node --version
```

**Required:** Node.js 18.x or higher

**Update if needed:**
```bash
# Using nvm
nvm install 20
nvm use 20

# Or download from nodejs.org
```

---

### 4. TypeScript Errors

**Error:** TypeScript compilation errors

**Solution:**
```bash
cd frontend
npm run build
# Fix any errors shown
npm run dev
```

---

### 5. Environment Variables Missing

**Error:** Keycloak or API connection issues

**Check `.env.local` exists:**
```bash
cd frontend
ls -la .env.local
```

**If missing, create it:**
```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
EOF
```

---

### 6. Cache Issues

**Error:** Stale cache or build errors

**Solution:**
```bash
cd frontend
rm -rf .next
rm -rf node_modules
npm install
npm run dev
```

---

### 7. Turbopack Issues

**Error:** Turbopack-related errors

**Solution - Disable Turbopack:**

Edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

Then:
```bash
npm run dev
```

---

## Verification Steps

### 1. Check Server Status

```bash
# Check if process is running
lsof -ti:3000

# Check if server responds
curl http://localhost:3000
```

### 2. Check Logs

Look for these messages when starting:
```
✓ Ready in X.Xs
○ Local:        http://localhost:3000
```

### 3. Test in Browser

Open these URLs:
- http://localhost:3000 (should redirect to /dashboard or /login)
- http://localhost:3000/login
- http://localhost:3000/dashboard

---

## Still Not Working?

### Check All Services

1. **Backend running?**
   ```bash
   curl http://localhost:8000/admin/
   ```

2. **Keycloak accessible?**
   ```bash
   curl https://auth.totesoft.com
   ```

3. **Frontend dependencies installed?**
   ```bash
   cd frontend
   ls node_modules | wc -l
   # Should show 200+ packages
   ```

### Get Detailed Logs

```bash
cd frontend
DEBUG=* npm run dev
```

### Check System Resources

```bash
# Check available memory
vm_stat

# Check disk space
df -h

# Check CPU usage
top -l 1 | grep "CPU usage"
```

---

## Alternative: Use Production Build

If dev server keeps failing, try production mode:

```bash
cd frontend
npm run build
npm start
```

This will start on http://localhost:3000 in production mode.

---

## Getting Help

If none of these work, provide:

1. **Node version:** `node --version`
2. **npm version:** `npm --version`
3. **OS:** `uname -a`
4. **Error message:** Full error from terminal
5. **Package.json:** Contents of `frontend/package.json`

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm install` | Install dependencies |
| `lsof -ti:3000` | Check what's on port 3000 |
| `kill -9 $(lsof -ti:3000)` | Kill process on port 3000 |

---

**Most Common Solution:**

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend
npm install
npm run dev
```

Then open: **http://localhost:3000**

---

Last Updated: October 4, 2024
