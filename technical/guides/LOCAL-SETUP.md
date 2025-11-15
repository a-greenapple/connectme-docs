# Local Development Setup Guide

## 📋 Overview

Your local development environment is configured to use **SQLite** (not PostgreSQL).

### Current Configuration

**File:** `connectme-backend/config/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Database file location:** `connectme-backend/db.sqlite3`

---

## 🚀 How to Start Local Server

### Option 1: Using the Start Script (Recommended)

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# Start both backend and frontend
./scripts/local-start.sh
```

This will:
- ✅ Start Django backend on `http://localhost:8000`
- ✅ Start Next.js frontend on `http://localhost:3000`
- ✅ Run in background with logs

### Option 2: Manual Start (Backend Only)

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-backend

# Activate virtual environment
source venv/bin/activate

# Run migrations (first time only)
python manage.py migrate

# Create superuser (first time only)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

---

## 📋 First Time Setup

If this is your first time running the local server:

### 1. Create/Check .env file

```bash
cd connectme-backend

# If .env doesn't exist, copy from local.env
cp local.env .env
```

### 2. Run Migrations

```bash
source venv/bin/activate
python manage.py migrate
```

Expected output:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying users.0001_initial... OK
  Applying claims.0001_initial... OK
  ... (many more)
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)

### 4. Load Initial Data (Optional)

```bash
# Set up UHC provider configuration
python setup_uhc_rsm.py

# Update UHC credentials
python update_uhc_secret.py
```

---

## 🧪 Verify It's Working

### 1. Check Backend

```bash
# Start server
python manage.py runserver

# In another terminal, test:
curl http://localhost:8000/healthz/
```

Expected: `{"status":"ok","app":"connectme-backend","debug":true}`

### 2. Check Admin

Open browser: `http://localhost:8000/admin/`
- Login with your superuser credentials
- You should see the Django admin interface

### 3. Check API

Open browser: `http://localhost:8000/api/swagger/`
- You should see the Swagger UI with all API endpoints

---

## 📊 Database Info

### SQLite Database Location

```
connectme-backend/db.sqlite3
```

### View Database Contents

#### Option 1: Django Shell

```bash
python manage.py shell
```

```python
from apps.users.models import User
from apps.claims.models import Claim

# Count users
User.objects.count()

# Count claims
Claim.objects.count()

# List all users
for user in User.objects.all():
    print(f"{user.username} - {user.email}")
```

#### Option 2: SQLite Command Line

```bash
sqlite3 db.sqlite3

# List tables
.tables

# Query users
SELECT * FROM users_user;

# Exit
.quit
```

#### Option 3: DB Browser for SQLite (GUI)

- Download: https://sqlitebrowser.org/
- Open: `db.sqlite3`
- Browse tables visually

---

## 🔄 Common Commands

### Stop Server

```bash
# If using local-start.sh
./scripts/local-stop.sh

# If running manually
# Press Ctrl+C in the terminal
```

### View Logs

```bash
# If using local-start.sh
tail -f /tmp/connectme-backend.log

# If running manually
# Logs appear in terminal
```

### Reset Database

```bash
# Delete database
rm db.sqlite3

# Recreate
python manage.py migrate

# Create superuser again
python manage.py createsuperuser
```

### Run Tests

```bash
# All tests
python manage.py test

# Specific test file
python manage.py test test_claims_filtering

# With verbose output
python manage.py test -v 2
```

---

## ⚠️ Important Notes

### 1. SQLite vs PostgreSQL

**Local (SQLite):**
- ✅ No setup required
- ✅ File-based database
- ✅ Good for development
- ❌ Not for production
- ❌ Limited concurrent writes

**Pre-Prod/Prod (PostgreSQL):**
- ✅ Production-ready
- ✅ Better performance
- ✅ Concurrent connections
- ✅ Advanced features

### 2. Data Persistence

Your SQLite database (`db.sqlite3`) contains all your local data:
- Users
- Claims
- CSV Jobs
- Provider configurations
- Audit logs

**Backup your database:**
```bash
cp db.sqlite3 db.sqlite3.backup
```

### 3. Migrations

When you pull new code with database changes:
```bash
python manage.py migrate
```

---

## 🐛 Troubleshooting

### "No such table" Error

```bash
# Run migrations
python manage.py migrate
```

### "Database is locked" Error

```bash
# Stop all Django processes
pkill -f "python manage.py runserver"

# Restart
python manage.py runserver
```

### "Port 8000 already in use"

```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
kill -9 $(lsof -ti:8000)

# Or use different port
python manage.py runserver 8001
```

### Missing Dependencies

```bash
pip install -r requirements/base.txt
pip install -r requirements/development.txt
```

---

## ✅ Quick Start Checklist

- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] `.env` file exists (copy from `local.env`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Server starts (`python manage.py runserver`)
- [ ] Admin accessible (`http://localhost:8000/admin/`)
- [ ] API docs accessible (`http://localhost:8000/api/swagger/`)

---

**Your local server is ready to use with SQLite!** 🎉

