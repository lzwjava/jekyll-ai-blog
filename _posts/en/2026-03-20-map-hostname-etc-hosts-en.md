---
audio: false
generated: true
image: false
lang: en
layout: post
title: Map Hostname in etc hosts File
translated: false
type: note
---

Question: How to add a record in `/etc/hosts` so I can easily access `http://192.168.1.36:3001/dashboard`?

Answer:

You can map a custom hostname (like `myapp.local`) to your IP (`192.168.1.36`) using the `/etc/hosts` file. This lets you access your service using a friendly name instead of the raw IP.

### Step-by-step

#### 1. Open `/etc/hosts` with root privileges

```bash
sudo nano /etc/hosts
```

(or use `vim` if you prefer)

#### 2. Add a new entry at the bottom

```
192.168.1.36   myapp.local
```

#### 3. Save and exit

* In nano: `Ctrl + O` → Enter → `Ctrl + X`

#### 4. Access your app

Now you can open:

```
http://myapp.local:3001/dashboard
```

---

### Notes

* The `/etc/hosts` file only maps **hostname → IP**, not ports or paths.
  So you still need to include `:3001/dashboard` in the URL.

* If you want multiple names:

```
192.168.1.36   myapp.local dashboard.local api.local
```

* If it doesn’t work immediately, flush DNS cache:

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

---

### Optional (Cleaner URLs)

If you want to access **without port/path**, like:

```
http://myapp.local
```

You’ll need a **reverse proxy** (e.g., Nginx):

Example:

```nginx
server {
    listen 80;
    server_name myapp.local;

    location / {
        proxy_pass http://192.168.1.36:3001/dashboard;
    }
}
```

---

If you want, I can help you set up Nginx or a local dev DNS setup (like `dnsmasq`) for a more scalable solution.
