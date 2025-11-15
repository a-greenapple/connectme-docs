# 🔌 Connecting to Remote Redis from Local Machine

**Server**: `20.84.160.240`  
**Redis Port**: `6379`  
**Current Config**: Localhost-only (secure)

---

## ✅ Option 1: SSH Tunnel (Recommended - Most Secure)

### Method A: Simple SSH Tunnel
```bash
# Create SSH tunnel (keeps Redis secure on localhost)
ssh -i ~/Documents/Access/cursor/id_rsa_Debian \
    -L 6379:localhost:6379 \
    connectme@20.84.160.240

# Keep this terminal open, then in another terminal:
redis-cli -h localhost -p 6379
```

### Method B: Background SSH Tunnel
```bash
# Run tunnel in background
ssh -i ~/Documents/Access/cursor/id_rsa_Debian \
    -f -N -L 6379:localhost:6379 \
    connectme@20.84.160.240

# Connect to Redis
redis-cli -h localhost -p 6379

# To close tunnel later:
# Find the SSH process: ps aux | grep "6379:localhost:6379"
# Kill it: kill <PID>
```

### Method C: Using Custom Local Port
```bash
# If you have local Redis running on 6379, use different port
ssh -i ~/Documents/Access/cursor/id_rsa_Debian \
    -L 16379:localhost:6379 \
    connectme@20.84.160.240

# Connect to Redis on custom port
redis-cli -h localhost -p 16379
```

### Test Connection
```bash
# After creating tunnel, test it:
redis-cli -h localhost -p 6379 ping
# Should return: PONG

# Check server info
redis-cli -h localhost -p 6379 INFO server | head -10

# Monitor Redis commands in real-time
redis-cli -h localhost -p 6379 MONITOR
```

---

## ⚠️ Option 2: Open Redis to External Access (Less Secure)

**Only use this if you need persistent external access and understand the security risks.**

### Steps to Enable External Access

1. **Update Redis configuration**:
```bash
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

# Edit Redis config
sudo nano /etc/redis/redis.conf

# Change this line:
# FROM: bind 127.0.0.1 -::1
# TO:   bind 0.0.0.0 ::

# Set a strong password
# ADD: requirepass YOUR_STRONG_PASSWORD_HERE

# Save and exit (Ctrl+X, Y, Enter)

# Restart Redis
sudo systemctl restart redis
```

2. **Open firewall port** (Azure NSG):
- Go to Azure Portal
- Navigate to your VM's Network Security Group
- Add inbound rule:
  - Port: 6379
  - Protocol: TCP
  - Source: Your IP address (not 0.0.0.0/0!)
  - Action: Allow

3. **Connect from local**:
```bash
redis-cli -h 20.84.160.240 -p 6379 -a YOUR_PASSWORD
```

### Security Considerations for Option 2
- ❌ **Redis is exposed to the internet**
- ❌ **Vulnerable to brute force attacks**
- ❌ **Requires strong password**
- ❌ **Should restrict IP access in firewall**
- ✅ **Only use if SSH tunnel isn't feasible**

---

## 🐍 Python Connection Examples

### Using SSH Tunnel (Recommended)
```python
import redis
from sshtunnel import SSHTunnelForwarder

# Create SSH tunnel
tunnel = SSHTunnelForwarder(
    ('20.84.160.240', 22),
    ssh_username='connectme',
    ssh_pkey='~/Documents/Access/cursor/id_rsa_Debian',
    remote_bind_address=('127.0.0.1', 6379)
)

tunnel.start()

# Connect to Redis through tunnel
r = redis.Redis(
    host='localhost',
    port=tunnel.local_bind_port,
    decode_responses=True
)

print(r.ping())  # Should print: True

# Use Redis...
r.set('test_key', 'Hello from local!')
print(r.get('test_key'))

# Close tunnel when done
tunnel.stop()
```

### Direct Connection (if exposed)
```python
import redis

r = redis.Redis(
    host='20.84.160.240',
    port=6379,
    password='YOUR_PASSWORD',  # if set
    decode_responses=True
)

print(r.ping())
```

---

## 📊 Redis GUI Tools

### RedisInsight (Official Redis GUI)
1. Download: https://redis.com/redis-enterprise/redis-insight/
2. Create SSH tunnel: `ssh -L 6379:localhost:6379 ...`
3. Connect to: `localhost:6379`

### Another Redis Desktop Manager
1. Download: https://github.com/qishibo/AnotherRedisDesktopManager
2. Supports SSH tunneling built-in
3. Add connection:
   - Host: 20.84.160.240
   - Port: 6379
   - SSH Tunnel: Enable
   - SSH Host: 20.84.160.240
   - SSH User: connectme
   - SSH Key: ~/Documents/Access/cursor/id_rsa_Debian

---

## 🧪 Testing Celery Tasks from Local

Once tunnel is set up, you can monitor Celery tasks:

```bash
# Create SSH tunnel
ssh -i ~/Documents/Access/cursor/id_rsa_Debian \
    -L 6379:localhost:6379 \
    connectme@20.84.160.240

# In another terminal, monitor Redis
redis-cli -h localhost -p 6379 MONITOR

# Watch Celery tasks
redis-cli -h localhost -p 6379
> KEYS celery*
> LRANGE celery 0 -1
```

---

## 🔧 Quick Reference

### Start SSH Tunnel
```bash
# Simple (foreground)
ssh -i ~/Documents/Access/cursor/id_rsa_Debian -L 6379:localhost:6379 connectme@20.84.160.240

# Background (detached)
ssh -i ~/Documents/Access/cursor/id_rsa_Debian -f -N -L 6379:localhost:6379 connectme@20.84.160.240
```

### Connect to Redis
```bash
redis-cli -h localhost -p 6379
```

### Common Redis Commands
```bash
# Test connection
PING

# Get all keys
KEYS *

# Get key value
GET key_name

# Set key value
SET key_name "value"

# Delete key
DEL key_name

# Get server info
INFO

# Monitor all commands in real-time
MONITOR

# Flush all data (careful!)
FLUSHALL
```

### Stop SSH Tunnel
```bash
# If running in foreground: Ctrl+C

# If running in background:
ps aux | grep "6379:localhost:6379"
kill <PID>

# Or kill all SSH tunnels:
pkill -f "ssh.*6379"
```

---

## 💡 Recommendations

### For Development (Local Machine)
✅ **Use SSH Tunnel** - Most secure, no server config changes needed

### For Production Monitoring
✅ **Use SSH Tunnel** + RedisInsight GUI

### For CI/CD or External Services
⚠️ **Consider Redis Cloud** or **AWS ElastiCache** instead of exposing your server's Redis

---

## 🎯 Recommended Setup

**Best practice for your use case:**

1. Keep Redis on localhost (current config - secure ✅)
2. Use SSH tunnel when you need to connect from local
3. Install RedisInsight for GUI access
4. Never expose Redis directly to internet

**Quick command to get started:**
```bash
# Terminal 1: Create tunnel
ssh -i ~/Documents/Access/cursor/id_rsa_Debian -L 6379:localhost:6379 connectme@20.84.160.240

# Terminal 2: Connect and test
redis-cli -h localhost -p 6379 ping
```

That's it! 🎉

