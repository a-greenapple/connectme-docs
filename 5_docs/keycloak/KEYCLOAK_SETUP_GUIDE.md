# Keycloak Setup Guide

## Quick Start - Using Your Existing Keycloak

Based on your auth flow, your Keycloak is at: `https://api.connectme.totesoft.com`

### Step 1: Verify Keycloak Access

```bash
# Check if Keycloak is accessible
curl https://api.connectme.totesoft.com/realms/connectme/.well-known/openid-configuration
```

If this returns JSON with endpoints, your Keycloak is ready!

---

## Configuration Steps

### 1. Create/Verify Realm

**Realm Name**: `connectme`

1. Login to Keycloak Admin Console
2. Go to: Realms → Create Realm (or select existing)
3. Name: `connectme`
4. Enabled: ON
5. Save

### 2. Create Client for Frontend

**Client ID**: `connectme-frontend`

Configuration:
```
Client ID: connectme-frontend
Client Protocol: openid-connect
Access Type: public
Standard Flow Enabled: ON
Direct Access Grants Enabled: ON
Valid Redirect URIs:
  - https://connectme.totesoft.com/*
  - http://localhost:3000/*
Web Origins:
  - https://connectme.totesoft.com
  - http://localhost:3000
```

### 3. Create Client for Backend (Optional)

**Client ID**: `connectme-backend`

Configuration:
```
Client ID: connectme-backend
Access Type: confidential
Service Accounts Enabled: ON
```

### 4. Create Test User

1. Go to: Users → Add User
2. Username: `testuser`
3. Email: `test@connectme.com`
4. First Name: `Test`
5. Last Name: `User`
6. Email Verified: ON
7. Save

8. Go to: Credentials tab
9. Set Password: `testpass123`
10. Temporary: OFF
11. Save

### 5. Create Roles

1. Go to: Roles → Add Role
2. Create roles:
   - `admin` - Full access
   - `manager` - View and edit
   - `staff` - View only

### 6. Assign Roles to User

1. Go to: Users → testuser → Role Mappings
2. Assign role: `admin`

---

## Testing Keycloak

### Get Token via Password Grant

```bash
curl -X POST https://api.connectme.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password"
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cC...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cC...",
  "token_type": "Bearer"
}
```

### Verify Token

```bash
# Decode token (use jwt.io or)
echo "eyJhbGciOiJSUzI1NiIsInR5cC..." | cut -d'.' -f2 | base64 -d | python3 -m json.tool
```

---

## Environment Variables

### Backend (.env)

```bash
# Keycloak
KEYCLOAK_SERVER_URL=https://api.connectme.totesoft.com
KEYCLOAK_REALM=connectme
KEYCLOAK_CLIENT_ID=connectme-frontend
KEYCLOAK_CLIENT_SECRET=  # Not needed for public client

# CORS
CORS_ALLOWED_ORIGINS=https://connectme.totesoft.com,http://localhost:3000
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

---

## If Keycloak is NOT Set Up Yet

### Option 1: Use Docker (Fastest)

```bash
# Run Keycloak in Docker
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest \
  start-dev

# Access at: http://localhost:8080
# Login: admin / admin
```

### Option 2: Use Existing Production Keycloak

If you already have Keycloak at `https://api.connectme.totesoft.com`:

1. Ask your DevOps/Admin for:
   - Realm name
   - Client ID
   - Admin access to create users

2. Follow configuration steps above

---

## Troubleshooting

### "Realm does not exist"

**Solution**: Create realm named `connectme` in Keycloak admin

### "Invalid client credentials"

**Solution**: 
1. Verify client ID matches exactly
2. For public clients, no secret needed
3. For confidential clients, copy secret from Keycloak

### "Invalid redirect URI"

**Solution**: Add all possible redirect URIs to client configuration:
- `http://localhost:3000/*`
- `https://connectme.totesoft.com/*`

### CORS Errors

**Solution**: Add web origins in Keycloak client configuration:
- `http://localhost:3000`
- `https://connectme.totesoft.com`

---

## Quick Verification Checklist

- [ ] Keycloak accessible at configured URL
- [ ] Realm `connectme` exists
- [ ] Client `connectme-frontend` created
- [ ] Test user created with password
- [ ] Can get token via curl/Postman
- [ ] Token contains expected claims (preferred_username, email)
- [ ] CORS configured for frontend domains

---

## Next: Frontend Integration

Once Keycloak is verified, we'll integrate it into the React frontend.

**Ready?** Let me know if Keycloak is set up, or if you need help with any step!

