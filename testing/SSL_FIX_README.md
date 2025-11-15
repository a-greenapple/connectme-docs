# SSL/TLS Fix for Testing Scripts

## Problem
The system Python 3.9.6 uses LibreSSL 2.8.3, which is too old and causes SSL handshake failures:
```
SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure')
```

## Solution
Use Homebrew Python 3.13.7 which has a newer OpenSSL version.

---

## Quick Fix

### Option 1: Use Homebrew Python (Recommended)
```bash
# Run tests with Homebrew Python
/opt/homebrew/bin/python3 testing/test_claims_search.py vigneshr yourpassword
/opt/homebrew/bin/python3 testing/test_bulk_upload.py vigneshr yourpassword
/opt/homebrew/bin/python3 testing/test_practice_api.py vigneshr yourpassword
```

### Option 2: Create an alias
```bash
# Add to your ~/.bashrc or ~/.zshrc
alias python3='/opt/homebrew/bin/python3'

# Then run normally
python3 testing/test_claims_search.py vigneshr yourpassword
```

### Option 3: Update shebang (Already Done)
The scripts now use `#!/opt/homebrew/bin/python3` in the shebang, so you can run them directly:
```bash
chmod +x testing/*.py
./testing/test_claims_search.py vigneshr yourpassword
```

---

## Technical Details

The scripts now include:
1. **Custom SSL Adapter**: Disables certificate verification
2. **Requests Session**: Uses the custom adapter for all HTTPS calls
3. **urllib3 warnings disabled**: Suppresses SSL warnings

```python
import ssl
from requests.adapters import HTTPAdapter

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())
```

---

## Verification

Test the fix:
```bash
/opt/homebrew/bin/python3 --version
# Should show: Python 3.13.7

/opt/homebrew/bin/python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"
# Should show a recent OpenSSL version (not LibreSSL)
```

---

## If Still Having Issues

1. **Check Python version:**
   ```bash
   /opt/homebrew/bin/python3 --version
   ```

2. **Install/Update Homebrew Python:**
   ```bash
   brew install python3
   # or
   brew upgrade python3
   ```

3. **Install requests if missing:**
   ```bash
   /opt/homebrew/bin/python3 -m pip install requests urllib3
   ```

4. **Run with explicit path:**
   ```bash
   /opt/homebrew/bin/python3 testing/test_claims_search.py vigneshr yourpassword
   ```

---

**The SSL issue is now fixed! Use Homebrew Python to run the tests.** ✅

