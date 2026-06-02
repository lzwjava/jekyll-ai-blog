---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Fixing Docker OverlayFS Removal Error
translated: false
type: note
---

The error you're seeing, specifically the line:
`Error response from daemon: container ccd89a3f36a1528cb923c90de8755faeb36e229cab353c2285222948197b8d18: driver "overlay2" failed to remove root filesystem: readdirnames /var/lib/docker/overlay2/7acbf095f3537e4829397e10f2134499389c724d3378782a8882ff1299fc431f/merged: readdirent merged: bad message`
indicates an **issue with Docker's storage driver**, specifically **OverlayFS (overlay2)**, which is often related to a corrupted filesystem state on your host machine. This usually happens when the Docker daemon can't access or properly clean up the container's files.

Here's a step-by-step approach to fix this, starting with the least invasive methods.

-----

## 1\. Stop and Force Remove the Container

The container `chat-mongodb` failed to remove. You'll need to target that specific container.

### A. Try a Force Removal

Attempt to remove the container again, but this time use the force flag (`-f`) to ensure it's not running and to try a more aggressive removal:

```bash
docker rm -f chat-mongodb
```

or use the container ID:

```bash
docker rm -f ccd89a3f36a1528cb923c90de8755faeb36e229cab353c2285222948197b8d18
```

### B. Stop the Docker Compose Stack

If the container is part of a larger stack you are trying to tear down (which the `[+] Running 3/3` suggests), try stopping the services gracefully first before attempting removal again:

```bash
docker compose stop
# Then try the original command again
# e.g., docker compose down
```

-----

## 2\. Restart the Docker Daemon

A simple restart of the Docker service can often clear up transient storage driver errors and lock files.

### For Linux systems (using systemd):

```bash
sudo systemctl restart docker
```

### For Docker Desktop (macOS/Windows):

1.  Click the **Docker icon** in your system tray/menu bar.
2.  Navigate to **Troubleshoot** (or **Settings** $\rightarrow$ **Daemon** $\rightarrow$ **Restart**).
3.  Click **Restart**.

After the restart, try removing the container again.

-----

## 3\. Manually Clean Up the Corrupted Directory

**⚠️ WARNING:** This step involves direct manipulation of Docker's internal file structure and should **only be performed as a last resort** and **while the Docker daemon is STOPPED**. Incorrect manual deletion can cause further corruption.

The error points to a specific directory within the OverlayFS storage: `/var/lib/docker/overlay2/7acbf095f3537e4829397e10f2134499389c724d3378782a8882ff1299fc431f/merged`.

1.  **Stop the Docker daemon:**

    ```bash
    sudo systemctl stop docker
    ```

2.  **Manually remove the problematic directory:**

    ```bash
    # Only remove the directory shown in YOUR error message
    sudo rm -rf /var/lib/docker/overlay2/7acbf095f3537e4829397e10f2134499389c724d3378782a8882ff1299fc431f
    ```

    *If you cannot find the exact directory, you might need to try a more general cleanup (see the next step).*

3.  **Start the Docker daemon:**

    ```bash
    sudo systemctl start docker
    ```

4.  **Try removing the container/stack again.**

-----

## 4\. Prune Unused Data

If the above steps fail, you can use Docker's built-in cleanup commands. This command removes all stopped containers, all networks not used by at least one container, all dangling images, and all build cache.

```bash
docker system prune
```

**Note:** This command will ask for confirmation and remove data you might want to keep if it's not actively used (e.g., stopped containers). Use `-a` to remove all unused images (not just dangling ones).
