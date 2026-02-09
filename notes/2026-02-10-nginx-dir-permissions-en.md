---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Nginx Directory Permissions Explained
translated: false
type: note
---

**Question:** Explain the permissions here for the nginx directory and its files:

lzw@to:~$ ls -alrt nginx  
total 28  
drwxr-x--- 81 lzw lzw 4096 Feb 10 02:53 ..  
drwxrwxr-x 2 lzw lzw 4096 Feb 10 02:56 .  
-rw-r--r-- 1 lzw lzw 412 Feb 10 02:58 access.log  
-rw-r--r-- 1 lzw lzw 14938 Feb 10 02:58 error.log

**Answer:**

This output shows a custom directory `/home/lzw/nginx` (or similar) that you probably created to store nginx logs when trying to run nginx fully as user `lzw`.  
Let’s break down every part of the permissions and ownership step by step.

### Directory listing explained line by line

1. `drwxr-x--- 81 lzw lzw 4096 Feb 10 02:53 ..`  
   - This is the **parent directory** (most likely `/home/lzw`).  
   - Permissions: `drwxr-x---`  
     - `d` → it is a directory  
     - Owner (lzw): rwx (read, write, execute)  
     - Group (lzw): r-x (read + execute, no write)  
     - Others: --- (nothing – no access at all)  
   → Only you (`lzw`) can write into your home folder. Other users (including www-data) cannot even list or enter it unless you give extra permissions.

2. `drwxrwxr-x 2 lzw lzw 4096 Feb 10 02:56 .`  
   - This is **the current directory** (`nginx` folder itself).  
   - Permissions: `drwxrwxr-x`  
     - Owner (lzw): rwx (full access)  
     - Group (lzw): rwx (full access – unusual, normally groups get r-x)  
     - Others: r-x (can list files and enter the folder, but cannot write)  
   → **Important:** Because “others” have `r-x`, the nginx process (when running as www-data) **can enter this folder and see the file names** — but only if it can also reach `/home/lzw` first (which currently blocks it with `---` for others).

3. `-rw-r--r-- 1 lzw lzw 412 Feb 10 02:58 access.log`  
   - Regular file (`-`)  
   - Permissions: `rw-r--r--`  
     - Owner (lzw): rw- (can read + write)  
     - Group (lzw): r-- (can only read)  
     - Others: r-- (everyone else can read)  
   → Any process (including www-data) that can reach the file **can read** it, but only you can write to it.

4. `-rw-r--r-- 1 lzw lzw 14938 Feb 10 02:58 error.log`  
   - Same as access.log: readable by everyone, writable only by owner `lzw`.

### Why this setup is causing problems right now

When nginx runs as **www-data** (default / correct way):

- www-data is **not** user `lzw`
- www-data is **not** in group `lzw` (your private group)
- Therefore www-data falls into the **“others”** category
- To read/write logs in `/home/lzw/nginx`, www-data needs:
  1. Execute (`x`) on `/home/lzw` → currently `---` for others → **blocked here**
  2. Execute (`x`) on `/home/lzw/nginx` → has `r-x` → ok
  3. Read (`r`) on the log files → has `r--` → ok
  4. Write (`w`) on the log files → has `r--` → **no write permission**

→ Main blocker: **no execute permission on your home directory** (`/home/lzw` has `---` for others).

### How to make it work (two clean options)

**Option 1 – Recommended: Let nginx use default logs again**

Undo the custom logs and custom user attempts:

```bash
# Remove any custom user line
sudo sed -i '/^user\s/d' /etc/nginx/nginx.conf

# Remove systemd override if you added User=lzw
sudo rm -f /etc/systemd/system/nginx.service.d/override.conf
sudo systemctl daemon-reload

# Restart normally (logs go back to /var/log/nginx/)
sudo nginx -t && sudo systemctl restart nginx
```

Then fix your movies folder access:

```bash
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads
sudo chmod g+x /home/lzw
```

**Option 2 – Keep custom logs in ~/nginx but make them writable by nginx**

If you want nginx (www-data) to write logs here:

```bash
# Allow nginx to enter your home
sudo chmod o+x /home/lzw

# Change group of the nginx folder and files to www-data
sudo chgrp -R www-data ~/nginx

# Give group write permission on files + execute on directory
sudo chmod -R g+rw ~/nginx/*.log
sudo chmod g+w ~/nginx
```

Or even simpler (but less secure):

```bash
sudo chmod -R o+rw ~/nginx
```

But again: using `/var/log/nginx/` with default setup is cleaner and more standard.

**Summary – current state in one sentence**

Your `~/nginx` folder and logs are readable by everyone, but nginx (www-data) cannot even reach your home directory yet, and also cannot write the logs because of missing group/write permissions.

**References:**

- None needed – this is standard Linux `ls -l` permission interpretation.