---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Stop CUPS Printing Service Guide
translated: false
type: note
---

**Question:** What is cups.service/stop in Ubuntu?

**Answer:**

`cups.service/stop` refers to **stopping the CUPS printing service** on Ubuntu using systemd (the most common way to control services).

### What is CUPS?
CUPS stands for **Common UNIX Printing System**. It is the standard printing system on Ubuntu (and most Linux distributions, as well as macOS).
It handles:
- Managing local and network printers
- Processing print jobs
- Printer discovery (especially via `cups-browsed`)
- The web interface for printer administration (http://localhost:631)

The systemd service is called **`cups.service`** and runs the main CUPS daemon (`cupsd`).

### What does `cups.service/stop` mean?
It means executing the command to **immediately stop** the CUPS service.

The actual command is:

```bash
sudo systemctl stop cups.service
```

(or shorter: `sudo systemctl stop cups`)

### What happens when you stop it?
- The CUPS daemon (`cupsd`) is terminated.
- No new print jobs can be sent or processed.
- Pending jobs in the queue usually stay in the queue (they resume after restart).
- Printer discovery / auto-adding of network printers stops (if using `cups-browsed`).
- The CUPS web interface (port 631) becomes unavailable.
- Printing from applications fails until the service is started again.

### Common related commands

| Purpose                          | Command                                      | Notes |
|-------------------------------|----------------------------------------------|-------|
| Stop CUPS now                 | `sudo systemctl stop cups`                   | Immediate stop |
| Start CUPS                    | `sudo systemctl start cups`                  | - |
| Restart CUPS                  | `sudo systemctl restart cups`                | Most common when troubleshooting |
| Prevent start on boot         | `sudo systemctl disable cups`                | Still can be started manually |
| Allow start on boot again     | `sudo systemctl enable cups`                 | - |
| Check status                  | `sudo systemctl status cups`                 | Shows running/stopped + recent logs |
| Stop + disable (no auto-start)| `sudo systemctl stop cups`<br>`sudo systemctl disable cups` | Common on servers |

**Note about modern Ubuntu versions (22.04+ / 24.04+):**
Sometimes CUPS is delivered as a **snap** package (especially `cups` and `cups-browsed`). In that case `systemctl` may not work and you need:

```bash
sudo snap stop cups
sudo snap disable cups
```

Check which version you have with:

```bash
systemctl status cups.service
# or
snap list | grep cups
```

**References:**

- [Ubuntu Server Documentation - CUPS](https://documentation.ubuntu.com/server/how-to/networking/cups-print-server)
- [Ask Ubuntu - How to stop and disable CUPS](https://askubuntu.com/questions/1463463/how-to-stop-and-disable-cups-service-in-ubuntu-22-04)
- [OpenPrinting CUPS project](https://openprinting.github.io/cups)
