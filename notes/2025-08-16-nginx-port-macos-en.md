---
audio: false
generated: true
image: false
lang: en
layout: post
title: Change Nginx Port on macOS Guide
translated: false
type: note
---

You want Nginx on macOS to listen on a **different port** than its default (80 for HTTP, 443 for HTTPS). Here's a clear step-by-step guide:

---

### 1. Locate your Nginx configuration file

* If you installed via **Homebrew**, the default config is usually:

  ```
  /usr/local/etc/nginx/nginx.conf
  ```

  or, on Apple Silicon:

  ```
  /opt/homebrew/etc/nginx/nginx.conf
  ```

* If you installed manually, it may be `/usr/local/nginx/conf/nginx.conf`.

---

### 2. Edit the `listen` directive

1. Open the config in a text editor:

   ```bash
   nano /opt/homebrew/etc/nginx/nginx.conf
   ```

2. Find the `server` block:

   ```nginx
   server {
       listen 80;
       server_name localhost;

       location / {
           root   html;
           index  index.html index.htm;
       }
   }
   ```

3. Change `listen 80;` to your desired port, e.g., 8080:

   ```nginx
   listen 8080;
   ```

---

### 3. Test the configuration

Run:

```bash
nginx -t
```

* If it says `syntax is ok` and `test is successful`, your config is valid.
* If there are errors, check the line numbers it reports.

---

### 4. Restart Nginx

* If installed via Homebrew:

```bash
brew services restart nginx
```

* Or manually:

```bash
sudo nginx -s reload
```

---

### 5. Access via new port

* In your browser or curl:

```
http://localhost:8080
```

---

**Extra Notes:**

* Ports **<1024** require `sudo` on macOS. So using ports like 80 will need root, but 8080 or 3000 does not.
* If you want to run multiple Nginx servers simultaneously, each **must have a unique port**.

---

I can also give a **quick trick to temporarily run Nginx on any port without editing nginx.conf** using a command line flag. It’s handy for testing. Do you want me to show that?
