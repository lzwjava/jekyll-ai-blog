---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Free Space in Broken Ubuntu System
translated: false
type: note
---

Question: In this situation (broken sudo, system low on space after massive CUPS logs, currently booting from Ubuntu live USB), what files or directories in /usr can I safely delete to free up some space?

Answer: 

Since you're already in the live USB environment (or can chroot into the broken system), you have full root access via the live session — this is the perfect time to free space before fixing sudo. The goal is to **delete large, non-critical, regeneratable or safely removable data** inside `/usr` without breaking the system further.

**Safest and most effective deletions in /usr (from live USB):**

1. **The huge CUPS log files** (by far the biggest win — likely 200–300 GB)  
   These are **not** in `/usr` — they are in `/var/log/cups/`, but since you asked about `/usr`, I'll list them anyway as priority #1:
   ```
   sudo rm -rf /mnt/root/var/log/cups/*
   # or just the big ones:
   sudo truncate -s 0 /mnt/root/var/log/cups/error_log*
   sudo truncate -s 0 /mnt/root/var/log/cups/access_log*
   sudo truncate -s 0 /mnt/root/var/log/cups/page_log*
   ```

2. **Large things actually inside /usr that are usually safe to remove or clear**

   - Old cached .deb packages (often 5–30 GB on long-running systems)
     ```
     sudo rm -rf /mnt/root/usr/share/doc/*               # documentation — usually 1–5 GB, safe
     sudo rm -rf /mnt/root/var/cache/apt/archives/*.deb  # downloaded packages — very safe, will re-download if needed
     sudo rm -rf /mnt/root/var/cache/apt/archives/partial/*
     ```

   - Locale data (if you only need English or a few languages)
     ```
     sudo rm -rf /mnt/root/usr/share/locale/{af,am,ar,as,az,be*,bg,bn*,bo*,br*,bs*,ca,cs,cy,da,de*,dz*,el,en_AU,en_CA,eo,es*,et*,eu*,fa*,fi,fr*,ga,gez*,gl*,gu*,haw,he*,hi*,hr,hu*,hy*,id*,is*,it*,ja*,ka*,kk*,km*,kn*,ko*,ku*,ky*,lo*,lt*,lv*,mg*,mi*,mk*,ml*,mn*,mr*,ms*,mt*,my*,nb*,ne*,nl*,nn*,no*,or*,pa*,pl,ps*,pt*,ro*,ru*,rw*,si*,sk*,sl*,sq*,sr*,sv*,sw*,ta*,te*,tg*,th*,ti*,tk*,tl*,tr*,tt*,uk*,ur*,uz*,vi*,wa*,xh*,yi*,yo*,zh*,zu*}
     ```
     (Keep only en*, zh*, your language — this can free 1–4 GB)

   - Man pages and info docs (regeneratable, often 500 MB–2 GB)
     ```
     sudo rm -rf /mnt/root/usr/share/man/*
     sudo rm -rf /mnt/root/usr/share/info/*
     ```

   - Unneeded icon themes / pixmaps (can be 1–3 GB)
     ```
     sudo rm -rf /mnt/root/usr/share/icons/*             # extreme — removes all icons, only do if desperate
     sudo rm -rf /mnt/root/usr/share/pixmaps/*
     ```

   - Old kernels (if many are installed — check first)
     ```
     ls -lh /mnt/root/boot/vmlinuz* /mnt/root/boot/initrd.img*
     sudo rm -f /mnt/root/boot/vmlinuz-OLDVERSION /mnt/root/boot/initrd.img-OLDVERSION
     ```
     (Only delete kernels older than your current one — keep at least the latest + one backup)

   - Snap cache / old revisions (if using snaps — often several GB)
     ```
     sudo rm -rf /mnt/root/var/lib/snapd/cache/*
     sudo rm -rf /mnt/root/var/lib/snapd/snaps/*.old   # old snap revisions
     ```

   - Python / pip cache (sometimes large)
     ```
     sudo rm -rf /mnt/root/usr/local/lib/python*/dist-packages/*/__pycache__/
     sudo rm -rf /mnt/root/root/.cache/pip/*
     ```

**Quick checklist – run these from live USB (replace /mnt/root with your mount point):**

```bash
# Highest impact first
sudo du -sh /mnt/root/var/log/cups/               # confirm size
sudo rm -rf /mnt/root/var/log/cups/*

sudo du -sh /mnt/root/var/cache/apt/archives/
sudo rm -rf /mnt/root/var/cache/apt/archives/*.deb

sudo du -sh /mnt/root/usr/share/locale/
# decide if you want to thin it out (see above)

sudo du -sh /mnt/root/usr/share/doc/
sudo rm -rf /mnt/root/usr/share/doc/*

# Check before deleting
sudo du -sh /mnt/root/boot/
# then selectively remove old kernels
```

**Things you MUST NOT delete in /usr (will break system badly):**

- /usr/bin, /usr/sbin, /usr/lib, /usr/libexec, /usr/lib64  
- /usr/share/applications, /usr/share/glib-2.0, /usr/share/mime  
- Anything containing libc, libstdc++, libgcc, openssl, ca-certificates, etc.  
- /usr/share/fonts (unless you know exactly what you're doing)

**After freeing space** → continue with the chroot + fix sudo steps from the previous message.

If you run `sudo du -sh /mnt/root/usr/* | sort -hr | head -20` you will see the actual largest directories and can decide more precisely.

References:  

- [Ask Ubuntu: How to free space on root partition](https://askubuntu.com/questions/19914/how-to-free-up-space-on-the-root-partition)
- [Ubuntu Community Help: Freeing disk space](https://help.ubuntu.com/community/FreeingUpDiskSpace)