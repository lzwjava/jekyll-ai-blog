---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Stop Remote AI Processes
translated: false
type: note
---

To stop a long-running process initiated by OpenClaw (or any AI agent) on a remote machine (like `192.168.1.36` or `47.107.70.224`) from your current laptop—especially if the web interface is unresponsive—you have a few options:

---

### **1. SSH into the Remote Machine**

If you have SSH access to the remote machine, you can log in and manually stop the process.

#### **Steps:**

1. **SSH into the remote machine:**

   ```bash
   ssh user@192.168.1.36
   ```

   (Replace `user` with the actual username.)

2. **Find the process:**
   Use `ps`, `top`, or `htop` to locate the running process:

   ```bash
   ps aux | grep ollama
   ```

   or

   ```bash
   sudo systemctl status ollama
   ```

3. **Stop the process:**
   - If it's a systemd service:

     ```bash
     sudo systemctl stop ollama
     ```

   - If it's a regular process, use `kill`:

     ```bash
     kill -9 <PID>
     ```

     (Replace `<PID>` with the actual process ID.)

---

### **2. Use Systemd (if applicable)**

If the process is managed by systemd (as in your log), you can stop it remotely via SSH:

```bash
ssh user@192.168.1.36 "sudo systemctl stop ollama"
```

---

### **3. Web Interface Timeout**

If the web interface is unresponsive, it may be due to:

- The process consuming all resources.
- A crash or hang.

In this case, **SSH is your best option** to regain control.

---

### **4. Automate via Script (if you have access)**

If you frequently need to stop such processes, create a script on the remote machine and trigger it via SSH:

```bash
ssh user@192.168.1.36 "/path/to/stop_script.sh"
```

---

### **5. Web Chat Limitations**

If you're asking whether you can stop the process **directly from a web chat interface** (like a chatbot or OpenClaw's UI):

- **No**, unless the web interface provides a built-in "stop" button or API endpoint.
- If the UI is frozen, you must use SSH or another remote access method.

---

### **Fixing the Immediate Issue**

From your log, the problem is:
> `Service is crash-looping — Ollama panics with $HOME is not defined.`

#### **Solution:**

Edit the systemd service file for Ollama and set the `HOME` environment variable:

```bash
sudo systemctl edit ollama
```

Add:

```
[Service]
Environment="HOME=/home/your_user"
```

Then restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

**Let me know if you need help with any of these steps!**
Would you like a step-by-step guide for any specific part?
