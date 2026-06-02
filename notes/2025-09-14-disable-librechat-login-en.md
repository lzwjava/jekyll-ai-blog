---
audio: false
date: 2025-09-14
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Disable LibreChat Login Authentication
translated: false
type: note
---

To make **LibreChat** work without requiring frequent logins (or disable login entirely), you can adjust the authentication settings. Here are the steps to resolve the issue:

---

### **1. Disable Authentication (No Login Required)**
If you want **LibreChat to be completely open** (no login at all), modify the configuration:

#### **Option A: Environment Variables (Recommended)**
Set the following in your `.env` file (or environment variables):
```env
# Disable authentication entirely
AUTHENTICATION=false
```
Then restart LibreChat:
```bash
docker compose down && docker compose up -d  # If using Docker
# OR
npm run build && npm run start  # If running locally
```

#### **Option B: Modify `config.yaml`**
If you're using a `config.yaml` file, add:
```yaml
auth:
  enabled: false
```

---

### **2. Fix Frequent Logout Issues (If You Still Want Login)**
If you **want to keep authentication** but fix the frequent logout problem, try these solutions:

#### **A. Increase Session/Cookie Expiry**
Modify the session settings in `.env`:
```env
# Extend session timeout (in seconds, e.g., 7 days = 604800)
SESSION_EXPIRY=604800

# Ensure cookies are secure (if using HTTPS)
COOKIE_SECURE=true  # Set to false if testing on HTTP
COOKIE_SAME_SITE=lax
```

#### **B. Use a Persistent Session Store**
By default, LibreChat may use in-memory sessions (which reset on restart). Switch to a **database-backed session store** (e.g., Redis or PostgreSQL):

1. **Install Redis** (if not already installed):
   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```
2. Update `.env`:
   ```env
   SESSION_STORE=redis
   REDIS_URL=redis://localhost:6379
   ```

#### **C. Check Reverse Proxy Settings (If Using Nginx/Apache)**
If you're behind a proxy (e.g., Nginx), ensure:
- Cookies are properly forwarded.
- `ProxyPass` includes `cookie` directives.

Example Nginx config:
```nginx
location / {
    proxy_pass http://localhost:3080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cookie_path / /;  # Ensure cookies are not scoped incorrectly
}
```

#### **D. Clear Browser Cache & Test in Incognito**
Sometimes, browser cache/corrupted cookies cause issues. Try:
- Clearing cookies for `librechat.example.com`.
- Testing in **Incognito Mode** or a different browser.

---

### **3. Debugging Cookie Issues**
If cookies are still not persisting:
1. **Check browser DevTools** (`F12` > **Application** > **Cookies**) to see if `connect.sid` (or similar) is being set.
2. **Verify `SameSite` attribute** (should be `Lax` or `None` if cross-site).
3. **Ensure `Domain` is correct** (e.g., `.example.com` for subdomains).

---

### **4. Update LibreChat**
If you're on an older version, bugs might be fixed in newer releases:
```bash
git pull origin main
docker compose down && docker compose up -d --build
```

---

### **Final Notes**
- **Security Warning**: Disabling auth (`AUTHENTICATION=false`) makes LibreChat **publicly accessible**. Only do this for trusted/internal networks.
- **HTTPS Required**: If using cookies, ensure your site is **HTTPS** (or set `COOKIE_SECURE=false` for testing).
