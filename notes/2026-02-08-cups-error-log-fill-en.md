---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: CUPS Error Log Fills Disk Fast
translated: false
type: note
---

Question: Why did /var/log/cups grow very large (occupying around 300 GB of log files) and cause the system to run out of space?

Answer:

The most common reason **/var/log/cups** (especially **error_log**) grows to hundreds of GB is that CUPS enters a **rapid error-loop** and logs the same error message thousands of times per second.

Typical causes include:

- A **misconfigured / unreachable network printer** (most frequent)
  CUPS repeatedly tries to connect, ping, probe status, or send keep-alive/notifications → fails → logs error → repeats forever
  Classic repeating messages:
  - `Notifier for subscription dbus:// went away, retrying...` (very common on Ubuntu/Debian)
  - `Unable to connect to printer... retrying`
  - IPP backend errors, LPD timeouts, authentication failures, etc.

- Broken **printer subscription / notification system** (dbus notifier dies or misbehaves)
  CUPS keeps retrying dbus subscriptions in a tight loop.

- Snap-based or conflicting CUPS installation (e.g., snap firefox → pulls snapd → sometimes installs/conflicts with system CUPS)
  This has caused massive repeated logging in some reported cases.

- Very verbose logging level (`LogLevel debug` or `debug2`) + high activity/failure rate
  (less common for 300 GB, but makes small problems much worse)

- Very old stuck print jobs or bad filters/backends spamming status updates

**Why 300 GB is possible**
A single line is ~100–200 bytes. At 10–1000 lines/second (easy in tight loops), it fills space very quickly:

- ~100 lines/sec → ~1 GB/hour → ~24 GB/day
- Faster loops (dbus retry storms) can reach several GB per hour.

**Immediate emergency actions** (when disk is already full)

1. Stop CUPS immediately to halt logging

   ```
   sudo systemctl stop cups
   # or if systemd is broken due to no space:
   sudo service cups stop
   ```

2. Free space by truncating or deleting the huge log

   ```
   sudo truncate -s 0 /var/log/cups/error_log
   # or
   sudo rm -f /var/log/cups/error_log
   ```

3. Restart CUPS (only after fixing root cause)

   ```
   sudo systemctl start cups
   ```

**Long-term prevention**

- Find and remove/fix the problematic printer in CUPS
  → <http://localhost:631> → Administration → Manage Printers → delete suspicious ones

- Lower log level in `/etc/cups/cupsd.conf`

  ```
  LogLevel warn        # or error / info (instead of debug)
  ```

  Then restart CUPS:

  ```
  sudo systemctl restart cups
  ```

- Set max log file size (if your CUPS version supports it via cupsd.conf or cupsctl)
  Example (some distros / web interface): limit to 10–50 MB

- Disable printers you don't use
  `sudo lpadmin -x printer-name`

- Check journal if using systemd-journald (sometimes errors go there too)
  `journalctl -u cups`

**Most people in this situation** eventually discover one misconfigured network printer (or an old removed one still defined in CUPS) was the root cause.

If you can share the **last 20–50 lines** of `/var/log/cups/error_log` (after `tail -n 50 /var/log/cups/error_log`), it usually reveals exactly which printer or backend is looping.

References:

- [Ask Ubuntu: Log files (CUPS) grow so fast!](https://askubuntu.com/questions/237019/log-files-cups-grow-so-fast)
- [Stack Overflow: Disk space rapidly decreased because /var/log/cups/error_log has become huge](https://stackoverflow.com/questions/15939532/disk-space-rapidly-decreased-because-var-log-cups-error-log-has-become-huge)
- [Unix & Linux Stack Exchange: CUPS Error log quickly filling up](https://unix.stackexchange.com/questions/709935/cups-error-log-quickly-filling-up)
- [Reddit: Cups Error = Big system log](https://www.reddit.com/r/linuxquestions/comments/1luefu1/cups_error_big_system_log)
