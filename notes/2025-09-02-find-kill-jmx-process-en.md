---
audio: false
generated: true
image: false
lang: en
layout: post
title: Find and Kill JMX Port Process
translated: false
type: note
---

Got it — you want to check which Java program on Windows has opened a **JMX remote agent** on port `9091`, and then kill it if necessary. Here’s how you can do it step by step:

---

### 1. Find the Process Using Port 9091

Open **Command Prompt** (as Administrator if possible), and run:

```cmd
netstat -ano | findstr :9091
```

This shows something like:

```
  TCP    0.0.0.0:9091    0.0.0.0:0    LISTENING    12345
```

* The last column (`12345` here) is the **PID (Process ID)**.

---

### 2. Identify Which Program That PID Belongs To

Now map the PID to the actual program:

```cmd
tasklist /FI "PID eq 12345"
```

This will show something like:

```
Image Name                     PID   Session Name        Mem Usage
========================= ======== ================ ============
java.exe                    12345 Console           200,000 K
```

If it’s a Java process, you can get even more detail:

```cmd
wmic process where processid=12345 get CommandLine
```

That prints the **command line** used to launch the JVM — you’ll see the JMX flags (`-Dcom.sun.management.jmxremote.port=9091`), which confirms it’s the JMX remote agent.

---

### 3. Kill the Process

If you’ve confirmed it’s safe to stop, you can kill it:

```cmd
taskkill /PID 12345 /F
```

* `/PID` specifies the process ID.
* `/F` forces termination.

---

### 4. Alternative with PowerShell

If you prefer PowerShell, you can run:

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 9091).OwningProcess
```

To kill directly:

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 9091).OwningProcess -Force
```

---

🔎 Summary:

1. `netstat -ano | findstr :9091` → get PID
2. `tasklist /FI "PID eq <PID>"` → see which program
3. `wmic process where processid=<PID> get CommandLine` → see JVM flags
4. `taskkill /PID <PID> /F` → kill

---

Do you want me to also show you how to **check multiple JVMs at once** for JMX agent ports (so you can see if others are running on ports like 9090, 9999, etc.)?
