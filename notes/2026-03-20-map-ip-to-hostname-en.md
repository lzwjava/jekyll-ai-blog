---
audio: false
generated: true
image: false
lang: en
layout: post
title: Map IP to Hostname in Hosts
translated: false
type: note
---

Question: How can I add a record in `/etc/hosts` so I can easily access `http://192.168.1.36:3001/dashboard`?

Answer:

You can map the IP address to a custom domain name in your local `/etc/hosts` file. This lets you replace the IP with something easier to remember.

---

## 1. Edit `/etc/hosts`

Open terminal and run:

```bash
sudo nano /etc/hosts
```

(You can use `vim` or any editor you prefer.)

---

## 2. Add a new record

At the bottom of the file, add a line like:

```bash
192.168.1.36    mydashboard.local
```

---

## 3. Save and exit

* In `nano`:
  Press `Ctrl + O` → Enter → `Ctrl + X`

---

## 4. Access it in browser

Now instead of:

```
http://192.168.1.36:3001/dashboard
```

You can use:

```
http://mydashboard.local:3001/dashboard
```

---

## 5. (Optional) Flush DNS cache

Sometimes changes apply instantly, but if not:

### macOS:

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

### Linux (if using systemd-resolved):

```bash
sudo systemd-resolve --flush-caches
```

---

## Key Notes

* `/etc/hosts` only maps **hostname → IP**, not ports
  → You still need `:3001` in the URL
* This works **only on your local machine**
* `.local` is commonly used, but you can use any name (e.g., `dashboard.test`)

---

## Bonus Tip (Cleaner URL)

If you want to access without `:3001`, like:

```
http://mydashboard.local/dashboard
```

You’ll need a reverse proxy (e.g., Nginx) to map port 80 → 3001.

---

If you want, I can show you a **1-minute Nginx config** to remove the port entirely.
