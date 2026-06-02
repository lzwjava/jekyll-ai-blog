---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Resolving Docker Overlay2 Removal Errors
translated: false
type: note
---

That error means Docker failed to remove the container’s overlay2 filesystem — the kernel/VM returned a low-level I/O error (`readdirent merged: bad message`). On macOS this usually happens when the Docker VM or overlay storage is in a bad state. Below are safe, ordered steps (from least destructive → more aggressive) you can try to recover.

**Important:** some commands below can remove data (images/volumes). I’ll mark destructive steps and show exact commands so you can copy/paste if you want.

---

# Quick checks (safe)

In a terminal, run:

```bash
# show container status and the problematic container id
docker ps -a --no-trunc | grep ccd89a3f36a1528cb923c90de8755faeb36e229c || true

# try a forced remove of the container
docker rm -f ccd89a3f36a1528cb923c90de8755faeb36e229c
```

If `docker rm -f` succeeds, you’re done. If it fails with the same overlay error, continue.

---

# Restart Docker (macOS Docker Desktop) — recommended next step (safe)

Quit Docker Desktop completely (use the whale icon → Quit) then start it again. Or from command line:

```bash
# macOS — restart Docker Desktop via AppleScript
osascript -e 'quit app "Docker"'
open -a Docker
```

After Docker restarts, try `docker compose down` or `docker rm -f <id>` again.

---

# Restart the host (very safe)

If a restart is possible, rebooting macOS often clears VM filesystem issues:

* Reboot the Mac, then start Docker Desktop and retry.

---

# If still failing — use Docker Desktop Troubleshoot actions (safe / medium)

Open Docker Desktop → Troubleshoot:

* Click **Restart Docker** (if you haven’t already).
* If that fails, try **Clean / Purge data** or **Reset to factory defaults** — **warning**: these remove images/containers/volumes. Use only if you can afford to lose local Docker data.

---

# If you’re on Docker Engine (Linux) or comfortable with manual cleanup (destructive)

**Only do this if you understand data loss risk.** Stop Docker daemon, remove overlay2 directory for the problematic id, then restart Docker.

```bash
# stop docker daemon (Linux)
sudo systemctl stop docker

# back up the overlay2 folder first (optional, if you have space)
sudo cp -a /var/lib/docker/overlay2/7acbf095f3537e4829397e10f2134499389c724d3378782a8882ff1299fc431f /root/overlay2-backup-7acbf095

# if backup done / not needed, remove the merged directory for that overlay:
sudo rm -rf /var/lib/docker/overlay2/7acbf095f3537e4829397e10f2134499389c724d3378782a8882ff1299fc431f

# (optionally) remove container metadata if necessary
# WARNING: only remove files you are certain correspond to the broken container
sudo rm -rf /var/lib/docker/containers/ccd89a3f36a1528cb923c90de8755faeb36e229cab353c2285222948197b8d18

# start docker
sudo systemctl start docker

# then try to clean up dangling items
docker system prune -a --volumes
```

Again: deleting files under `/var/lib/docker` is destructive and can break other containers if done incorrectly. Only use if you know what you’re deleting.

---

# Less-destructive cleanup that often helps

If you can’t delete the overlay directly or prefer a softer approach:

```bash
# try pruning unused objects
docker system prune -f
docker volume prune -f

# remove unused images/containers (be careful)
docker image prune -a -f
docker container prune -f
```

This can free space and sometimes lets Docker re-run remove operations successfully.

---

# If the problem recurs and you use Docker Desktop for Mac

* Consider increasing Docker VM disk size (Settings → Resources → Disk image size).
* If you rely on important local data, export volumes/containers first (`docker export`, `docker save`) before using Reset/Purge.

---

# Diagnostics to collect (if you want me to help further)

If none of above fixes it, share outputs of these (non-destructive) commands and I’ll suggest targeted next steps:

```bash
docker info
docker ps -a
docker compose version
docker version
# list overlay dirs (Linux)
ls -lah /var/lib/docker/overlay2 | head -n 40
```

(If you’re on macOS Docker Desktop, `ls /var/lib/docker` won’t show the VM contents — prefer restarting Docker Desktop or using the Troubleshoot UI.)

---

If you want, tell me whether you’re running **Docker Desktop on macOS** (most likely) or **Docker Engine on Linux** — I’ll give a shorter, tailored sequence. If you prefer, I can also produce a one-line checklist you can run in order.
