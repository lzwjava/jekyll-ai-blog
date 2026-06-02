---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix CUPS DBus Permissions Error
translated: false
type: note
---

Question: From the tail of error_log, it shows "File /usr/lib/cups/notifier/ddbus has insecure permissions" and "notifier for subscription went away retrying". Why is this happening and how to fix it?

Answer:

The messages you see are extremely common and directly explain the massive log growth (300 GB in your case):

- **"File \"/usr/lib/cups/notifier/dbus\" has insecure permissions"** (note: it's usually spelled **dbus**, not ddbus — probably a small typo in your message)
  CUPS refuses to use the dbus notifier because the file has overly permissive settings (typically 0777 = -rwxrwxrwx or similar, instead of the secure 0755 = -rwxr-xr-x).

- **"Notifier for subscription dbus:// went away, retrying!"**
  Because the notifier binary is rejected due to bad permissions, the dbus subscription process fails instantly → CUPS immediately retries in a tight loop → this logs the warning/error pair thousands of times per second → huge error_log file in minutes to hours.

This loop started because the original chown -R command you ran on /usr/ (from the npm prefix mistake) changed ownership/permissions on many files, including /usr/lib/cups/notifier/dbus (and possibly the whole /usr/lib/cups/notifier directory).

**Fix steps** (do them in this order)

1. **Stop CUPS immediately** to stop the logging flood and free CPU/disk I/O

   ```
   sudo systemctl stop cups
   # or if systemctl doesn't work yet:
   sudo service cups stop
   ```

2. **Free space right now** (truncate is safer than rm if you want to keep old logs)

   ```
   sudo truncate -s 0 /var/log/cups/error_log
   # or delete it:
   sudo rm -f /var/log/cups/error_log*
   ```

3. **Fix the permissions on the notifier file**
   The correct permissions are usually **755** (executable by owner, readable/executable by others) and owned by **root:root** (or sometimes daemon:lp / lp:lp on some distros — but root:root is safe and common).
   Run:

   ```
   sudo chown root:root /usr/lib/cups/notifier/dbus
   sudo chmod 755 /usr/lib/cups/notifier/dbus
   ```

   If the whole notifier directory was affected, also fix it (safe overkill):

   ```
   sudo chown -R root:root /usr/lib/cups/notifier
   sudo chmod -R 755 /usr/lib/cups/notifier
   ```

4. **(Optional but often needed) Clear stuck subscriptions**
   Broken subscriptions can keep retrying even after fix:

   ```
   sudo rm -f /etc/cups/subscriptions.conf*
   sudo systemctl restart cups   # or sudo service cups restart
   ```

5. **Restart CUPS and verify**

   ```
   sudo systemctl start cups
   sudo systemctl status cups
   ```

   Then watch the log briefly:

   ```
   tail -f /var/log/cups/error_log
   ```

   The repeating errors should stop. If printing still doesn't work, go to <http://localhost:631> and check/delete problematic printers.

**If sudo still doesn't work** (from your earlier chown damage):
Use the live USB / recovery mode method from before to run these chown/chmod commands as root.

**Prevention / better defaults**
After recovery, set a less verbose log level in `/etc/cups/cupsd.conf` (or `/etc/cups/cupsd.conf.d/` files):

```
LogLevel warn
```

Then restart CUPS.

If you don't use printing at all, you can disable CUPS permanently:

```
sudo systemctl disable --now cups
```

This exact issue (dbus notifier permissions + retry loop) has filled drives with 50–250+ GB logs in countless Ubuntu/Debian/Mint reports over the years — almost always from recursive chown/chmod mistakes in /usr.

References:

- [Ask Ubuntu: cupsd using 100% CPU, creating large (80GB+) error_log](https://askubuntu.com/questions/648807/cupsd-using-100-cpu-creating-large-80gb-error-log)
- [GitHub apple/cups issue: CUPS filled my drive with giant error_log file](https://github.com/apple/cups/issues/5804)
- [Stack Overflow: Disk space rapidly decreased because /var/log/cups/error_log has become huge](https://stackoverflow.com/questions/15939532/disk-space-rapidly-decreased-because-var-log-cups-error-log-has-become-huge)
- [Linux Mint Forums: Error log has filled my hard disk](https://forums.linuxmint.com/viewtopic.php?t=284580)
