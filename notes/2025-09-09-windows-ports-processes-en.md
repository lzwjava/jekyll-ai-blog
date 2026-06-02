---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Managing Windows Ports and Processes
translated: false
type: note
---

On Windows, you can check which ports are being listened to — and by which process (PID) — using `netstat`, and then manage or kill those processes with `taskkill`. This is often needed when debugging backend projects like Java Spring Boot apps, Redis, or MySQL. Here’s how:

---

### 1. Check listening ports

Run **Command Prompt (cmd)** or **PowerShell** as Administrator:

```bash
netstat -ano | findstr LISTENING
```

* `-a` → show all connections and listening ports
* `-n` → show addresses and ports in numeric form
* `-o` → include PID (Process ID)

Example output:

```
TCP    0.0.0.0:8080     0.0.0.0:0     LISTENING     12345
TCP    0.0.0.0:3306     0.0.0.0:0     LISTENING     6789
```

Here:

* Port `8080` is used by PID `12345` (likely your Spring Boot app).
* Port `3306` is used by PID `6789` (MySQL).

---

### 2. Find which process that PID belongs to

You can match the PID to a process name:

```bash
tasklist | findstr 12345
```

Output might show:

```
java.exe                  12345 Console                    1     512,000 K
```

That means your Spring Boot app is running on port 8080.

---

### 3. Kill the process if needed

If you want to stop that process:

```bash
taskkill /PID 12345 /F
```

* `/PID` → specifies process ID
* `/F` → force kill

---

### 4. Typical ports for common backend services

* **Spring Boot (Java app):** 8080, 8081, etc.
* **MySQL:** 3306
* **Redis:** 6379
* **PostgreSQL:** 5432

So, if you see those ports in the `netstat` output, you’ll know which service is running.

---

👉 Pro tip: You can combine these into one command to directly find which process is using a given port (e.g., 8080):

```bash
netstat -ano | findstr :8080
```

Then take the PID and check it with `tasklist`.

---

Do you want me to also show you a **PowerShell one-liner** that directly maps ports to process names without needing to check separately with `tasklist`?
