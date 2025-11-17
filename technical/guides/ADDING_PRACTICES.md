# Adding Practices to Pre-Prod

This guide explains how to add practice data from production to pre-prod.

---

## 🚀 Quick Method: Using the Script

### Step 1: Edit the Practice List

Edit `connectme-backend/add_practices_to_preprod.py` and update the `PRACTICES` list:

```python
PRACTICES = [
    {
        'name': 'RSM',
        'tin': '854203105',
        'npi': '',
        'payer_id': '87726',  # UHC Payer ID
    },
    {
        'name': 'Your Practice Name',
        'tin': '123456789',
        'npi': '1234567890',
        'address_line1': '123 Main St',
        'city': 'New York',
        'state': 'NY',
        'zip_code': '10001',
        'phone': '555-1234',
        'email': 'practice@example.com',
        'payer_id': '87726',
    },
    # Add more practices...
]
```

### Step 2: Upload and Run the Script

```bash
# Upload the script
scp connectme-backend/add_practices_to_preprod.py connectme@169.59.163.43:/var/www/connectme-preprod-backend/

# Run the script
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python add_practices_to_preprod.py'
```

---

## 📋 Manual Method: Using Django Shell

If you prefer to add practices manually:

```bash
ssh connectme@169.59.163.43
cd /var/www/connectme-preprod-backend
source venv/bin/activate
python manage.py shell
```

Then in the Django shell:

```python
from apps.providers.models import Practice, PracticePayerMapping, Provider
from apps.users.models import Organization

# Get UHC provider
uhc = Provider.objects.get(name='UnitedHealthcare')

# Create practice
practice = Practice.objects.create(
    name='Your Practice Name',
    tin='123456789',
    npi='1234567890',
    address_line1='123 Main St',
    city='New York',
    state='NY',
    zip_code='10001',
    phone='555-1234',
    email='practice@example.com',
    is_active=True
)

# Create payer mapping
PracticePayerMapping.objects.create(
    practice=practice,
    provider=uhc,
    payer_id='87726',  # UHC Payer ID
    is_active=True
)

# Create organization with matching TIN
Organization.objects.create(
    name='Your Practice Name',
    tin='123456789',
    is_active=True
)

print(f"✅ Created practice: {practice.name}")
```

---

## 📊 Importing from CSV

If you have a CSV file with practice data:

### Step 1: Prepare CSV File

Create a file `practices.csv`:

```csv
name,tin,npi,address_line1,city,state,zip_code,phone,email,payer_id
Practice 1,123456789,1234567890,123 Main St,New York,NY,10001,555-1234,practice1@example.com,87726
Practice 2,987654321,0987654321,456 Oak Ave,Boston,MA,02101,555-5678,practice2@example.com,87726
```

### Step 2: Create Import Script

```python
#!/usr/bin/env python3
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.providers.models import Practice, PracticePayerMapping, Provider
from apps.users.models import Organization

uhc = Provider.objects.get(name='UnitedHealthcare')

with open('practices.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Create practice
        practice, created = Practice.objects.update_or_create(
            tin=row['tin'],
            defaults={
                'name': row['name'],
                'npi': row.get('npi', ''),
                'address_line1': row.get('address_line1', ''),
                'city': row.get('city', ''),
                'state': row.get('state', ''),
                'zip_code': row.get('zip_code', ''),
                'phone': row.get('phone', ''),
                'email': row.get('email', ''),
                'is_active': True,
            }
        )
        
        # Create payer mapping
        PracticePayerMapping.objects.update_or_create(
            practice=practice,
            provider=uhc,
            defaults={
                'payer_id': row.get('payer_id', '87726'),
                'is_active': True,
            }
        )
        
        # Create organization
        Organization.objects.update_or_create(
            tin=row['tin'],
            defaults={
                'name': row['name'],
                'is_active': True,
            }
        )
        
        print(f"✅ {'Created' if created else 'Updated'}: {row['name']}")
```

---

## 🔍 Viewing Current Practices

To see what practices are currently in pre-prod:

```bash
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "
from apps.providers.models import Practice, PracticePayerMapping

for p in Practice.objects.filter(is_active=True):
    print(f\"{p.name} (TIN: {p.tin})\")
    for m in PracticePayerMapping.objects.filter(practice=p, is_active=True):
        print(f\"  - Payer ID: {m.payer_id}\")
"'
```

---

## 📝 Practice Data Fields

### Required Fields:
- **name**: Practice name
- **tin**: Tax Identification Number (9 digits)

### Optional Fields:
- **npi**: National Provider Identifier (10 digits)
- **address_line1**: Street address
- **address_line2**: Apartment, suite, etc.
- **city**: City
- **state**: State (2-letter code)
- **zip_code**: ZIP code
- **phone**: Phone number
- **email**: Email address
- **payer_id**: UHC Payer ID (default: 87726)

---

## ⚠️ Important Notes

1. **TIN is the unique identifier** - practices are matched by TIN
2. **Each practice needs a payer mapping** to work with UHC API
3. **Create matching organizations** so users can be assigned to practices
4. **Default UHC Payer ID is 87726** - verify this is correct for your practices
5. **The script uses `update_or_create`** - safe to run multiple times

---

## 🧪 Testing After Adding Practices

After adding practices, test that they appear in the UI:

1. **Login to pre-prod:** https://pre-prod.connectme.apps.totessoft.com
2. **Go to Claims Search**
3. **Check the Practice dropdown** - your new practices should appear
4. **Try searching claims** with the new practice selected

Or use the test script:

```bash
/opt/homebrew/bin/python3 testing/test_practice_api.py admin manage
```

---

## 📞 Need Help?

If you encounter issues:

1. Check backend logs:
   ```bash
   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 50'
   ```

2. Verify database connection:
   ```bash
   ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py dbshell'
   ```

3. Run Django migrations:
   ```bash
   ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py migrate'
   ```

---

**Ready to add your practices!** 🎉

