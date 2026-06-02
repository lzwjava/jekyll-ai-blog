---
audio: false
generated: true
image: false
lang: en
layout: post
title: Identify Processes Listening on Specific Ports
translated: false
type: note
---

**Question:** How do I find out which process or application is listening on port 18789?

**Answer:**

## How to Find Which Process Is Listening on Port 18789

Replace `18789` in each command below with any port number you want to check.

---

## 🐧 Linux / macOS

### Method 1: `ss` (Recommended — Modern)

`ss` is the recommended modern tool to find which process is listening on a specific port.

```bash
sudo ss --listening --numeric --processes sport :18789
```

Short form:

```bash
sudo ss -lntp sport :18789
```

Sample output:

```
Netid  State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
tcp    LISTEN  0       128     0.0.0.0:18789        0.0.0.0:*          users:(("myapp",pid=12345,fd=7))
```

---

### Method 2: `lsof`

`lsof` lists all open files in a Linux system; since network ports are treated as files, you can use it with `-i :port_number` to find the process using that port.

```bash
sudo lsof -i :18789
```

Sample output:

```
COMMAND   PID   USER   FD   TYPE  DEVICE  SIZE/OFF  NODE  NAME
myapp   12345   root    3u  IPv4   19373       0t0   TCP   *:18789 (LISTEN)
```

The output shows the **process name**, **PID**, **owner user**, and **file descriptor**.

---

### Method 3: `netstat`

`netstat` is the traditional tool for displaying network connections and is still widely used.

```bash
sudo netstat -tulpn | grep :18789
```

Options explained:

| Option | Meaning |
|---|---|
| `-t` | TCP connections |
| `-u` | UDP connections |
| `-l` | Listening sockets only |
| `-p` | Show PID/program name |
| `-n` | Show numeric ports (no DNS resolution) |

> **Note:** `netstat` may not be installed by default on newer distros. Install with: `sudo apt install net-tools`

---

### Method 4: `fuser`

```bash
sudo fuser -v 18789/tcp
```

Sample output:

```
                     USER        PID ACCESS COMMAND
18789/tcp:           root      12345 F....  myapp
```

---

## 🪟 Windows

### Method 1: `netstat` in Command Prompt (Run as Administrator)

```cmd
netstat -ano | findstr :18789
```

Sample output:

```
TCP    0.0.0.0:18789    0.0.0.0:0    LISTENING    12345
```

The last number is the **PID**. Then find the process name:

```cmd
tasklist /FI "PID eq 12345"
```

### Method 2: PowerShell (One-liner)

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 18789).OwningProcess
```

This directly outputs the **process name** without needing to look up the PID separately.

---

## Quick Reference Summary

| OS | Command |
|---|---|
| Linux (modern) | `sudo ss -lntp sport :18789` |
| Linux (lsof) | `sudo lsof -i :18789` |
| Linux (netstat) | `sudo netstat -tulpn \| grep :18789` |
| Windows CMD | `netstat -ano \| findstr :18789` |
| Windows PowerShell | `Get-NetTCPConnection -LocalPort 18789` |

> 💡 If **nothing is returned**, it means **no process is currently listening** on port 18789.

**References:**

- [TecMint: Find Which Process is Listening on a Port](https://www.tecmint.com/find-out-which-process-listening-on-a-particular-port/)
- [Baeldung: Finding the PID of the Process Using a Specific Port](https://www.baeldung.com/linux/find-process-using-port)
- [Linux Audit: How to See Which Process is Using a Port](https://linux-audit.com/networking/faq/how-to-see-which-process-is-using-a-port/)
- [nixCraft: How to Check if Port Is in Use on Linux](https://www.cyberciti.biz/faq/unix-linux-check-if-port-is-in-use-command/)
