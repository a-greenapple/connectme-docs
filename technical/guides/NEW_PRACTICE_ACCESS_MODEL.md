# New Practice Access Model

## 🎯 Overview

We've moved from **TIN-based matching** to a **many-to-many relationship** between Users and Practices.

---

## 📊 Old Model vs New Model

### ❌ **Old Model (TIN Matching)**

```
User → Organization (has TIN) → Practice (has TIN)
                ↓                      ↓
           TIN: 854203105         TIN: 854203105
                └──────── MATCH ────────┘
```

**Problems:**
- Organization needed a TIN (but it's a billing company, not a practice)
- Users could only access practices with matching TIN
- Had to create separate organizations for each practice TIN
- Inflexible - couldn't give users access to multiple practices with different TINs

---

### ✅ **New Model (Many-to-Many)**

```
┌─────────────────────────────────────────┐
│  Organization                           │
│  "Apple Billing and Credentialing LLC"  │
│  (No TIN needed!)                       │
└─────────────────────────────────────────┘
                    │
                    │ has many
                    ▼
            ┌───────────────┐
            │     USER      │
            │               │
            │  - username   │
            │  - role       │
            └───────────────┘
                    │
                    │ many-to-many
                    ▼
        ┌──────────────────────────┐
        │   user_practices table   │  ← Junction table
        │                          │
        │  user_id  | practice_id  │
        │  ---------|------------- │
        │  uuid-1   |      1       │  vigneshr → RSM
        │  uuid-1   |      2       │  vigneshr → PFP
        │  uuid-2   |      1       │  admin → RSM
        │  uuid-2   |      2       │  admin → PFP
        └──────────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │   PRACTICE   │
            │              │
            │  - name      │
            │  - TIN       │  ← TIN stays with practice
            │  - NPI       │
            └──────────────┘
```

**Benefits:**
- ✅ Organization doesn't need TIN/NPI
- ✅ Users can access multiple practices with different TINs
- ✅ Flexible assignment (admin can assign any practice to any user)
- ✅ Clear separation: Organization = billing company, Practice = healthcare facility

---

## 🗄️ Database Schema

### **User Model** (apps/users/models.py)

```python
class User(AbstractUser):
    organization = ForeignKey(Organization)  # Just for grouping
    role = CharField  # admin, staff, manager, etc.
    
    # NEW: Many-to-many relationship with practices
    practices = ManyToManyField('providers.Practice', 
                                related_name='users',
                                help_text='Practices this user can access')
```

### **Organization Model** (apps/users/models.py)

```python
class Organization(models.Model):
    name = CharField  # "Apple Billing and Credentialing LLC"
    # TIN and NPI removed - not needed!
    address, phone, email...
```

### **Practice Model** (apps/providers/models.py)

```python
class Practice(models.Model):
    name = CharField  # "RSM", "PFP"
    tin = CharField   # Practice TIN (stays here)
    npi = CharField   # Practice NPI (stays here)
    address, phone, email...
```

### **Junction Table** (auto-created by Django)

```sql
CREATE TABLE users_user_practices (
    id INTEGER PRIMARY KEY,
    user_id UUID REFERENCES users_user(id),
    practice_id INTEGER REFERENCES practices(id),
    UNIQUE(user_id, practice_id)
);
```

---

## 🔧 How to Use

### **1. Run Migration**

```bash
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
source venv/bin/activate

# Run migration to add practices field
python manage.py migrate

# Assign all practices to all users
python assign_practices_to_users.py
```

---

### **2. Assign Practices to a User**

#### **Option A: Assign ALL practices to a user**

```python
from apps.users.models import User
from apps.providers.models import Practice

user = User.objects.get(username='vigneshr')
practices = Practice.objects.filter(is_active=True)
user.practices.set(practices)  # Assign all practices

print(f"{user.username} can now access: {[p.name for p in user.practices.all()]}")
```

#### **Option B: Assign SPECIFIC practices to a user**

```python
user = User.objects.get(username='vigneshr')
rsm = Practice.objects.get(name='RSM')
pfp = Practice.objects.get(name='PFP')

user.practices.add(rsm, pfp)  # Add specific practices
# or
user.practices.set([rsm, pfp])  # Replace all with these

print(f"{user.username} can access: {[p.name for p in user.practices.all()]}")
```

#### **Option C: Remove practice access**

```python
user = User.objects.get(username='vigneshr')
pfp = Practice.objects.get(name='PFP')

user.practices.remove(pfp)  # Remove PFP access
```

---

### **3. Check User's Practice Access**

```python
user = User.objects.get(username='vigneshr')

# Get all practices user can access
accessible_practices = user.practices.filter(is_active=True)
for practice in accessible_practices:
    print(f"  - {practice.name} (TIN: {practice.tin})")

# Check if user can access a specific practice
pfp = Practice.objects.get(name='PFP')
if user.practices.filter(id=pfp.id).exists():
    print(f"{user.username} CAN access {pfp.name}")
else:
    print(f"{user.username} CANNOT access {pfp.name}")
```

---

### **4. Get All Users for a Practice**

```python
practice = Practice.objects.get(name='RSM')

# Get all users who can access this practice
users_with_access = practice.users.all()
for user in users_with_access:
    print(f"  - {user.username} ({user.role})")
```

---

## 🔐 Access Control Logic

### **In the Backend** (apps/claims/api_views.py)

```python
# When user searches claims for a practice
if practice_id:
    practice = Practice.objects.get(id=practice_id)
    
    # Check access
    is_admin = request.user.role == 'admin'
    if not is_admin:
        # Check if user has access via many-to-many
        if not request.user.practices.filter(id=practice_id).exists():
            return Response({'error': 'You do not have access to this practice'})
```

**Access Rules:**
1. **Admin users** → Can access ALL practices (no restrictions)
2. **Non-admin users** → Can only access practices in their `user.practices` list
3. **Users with no practices assigned** → Get error message

---

## 📋 Example Scenarios

### **Scenario 1: All users access all practices**

```python
# Assign all practices to all users
for user in User.objects.filter(deleted_at__isnull=True):
    practices = Practice.objects.filter(is_active=True)
    user.practices.set(practices)
```

**Result:** Everyone can see RSM and PFP in the dropdown

---

### **Scenario 2: Separate teams for different practices**

```python
# RSM team
rsm_users = ['user1', 'user2', 'user3']
rsm_practice = Practice.objects.get(name='RSM')
for username in rsm_users:
    user = User.objects.get(username=username)
    user.practices.add(rsm_practice)

# PFP team
pfp_users = ['user4', 'user5']
pfp_practice = Practice.objects.get(name='PFP')
for username in pfp_users:
    user = User.objects.get(username=username)
    user.practices.add(pfp_practice)
```

**Result:** 
- user1, user2, user3 → Only see RSM
- user4, user5 → Only see PFP

---

### **Scenario 3: Manager with access to multiple practices**

```python
manager = User.objects.get(username='manager')
manager.practices.set(Practice.objects.all())  # All practices
```

**Result:** Manager sees all practices in dropdown

---

## 🚀 Deployment Steps

### **Step 1: Upload Files**

```bash
# Upload updated files
scp connectme-backend/apps/users/models.py connectme@169.59.163.43:/var/www/connectme-preprod-backend/apps/users/
scp connectme-backend/apps/users/migrations/0005_add_user_practices_m2m.py connectme@169.59.163.43:/var/www/connectme-preprod-backend/apps/users/migrations/
scp connectme-backend/apps/claims/api_views.py connectme@169.59.163.43:/var/www/connectme-preprod-backend/apps/claims/
scp connectme-backend/assign_practices_to_users.py connectme@169.59.163.43:/var/www/connectme-preprod-backend/
```

### **Step 2: Run Migration**

```bash
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py migrate
```

### **Step 3: Assign Practices**

```bash
python assign_practices_to_users.py
```

### **Step 4: Restart Backend**

```bash
sudo systemctl restart connectme-preprod-backend
```

---

## ✅ Benefits Summary

| Feature | Old Model (TIN Match) | New Model (M2M) |
|---------|----------------------|-----------------|
| Organization needs TIN | ❌ Yes | ✅ No |
| User access multiple TINs | ❌ No | ✅ Yes |
| Flexible assignment | ❌ No | ✅ Yes |
| Clear separation | ❌ No | ✅ Yes |
| Easy to manage | ❌ No | ✅ Yes |

---

## 🎯 Next Steps

1. ✅ Run migration
2. ✅ Assign practices to users
3. ✅ Test in pre-prod
4. ✅ Update user management UI to show/edit practice assignments
5. ✅ Remove TIN/NPI from Organization model (optional cleanup)

---

**The new model is cleaner, more flexible, and makes more sense!** 🎉

