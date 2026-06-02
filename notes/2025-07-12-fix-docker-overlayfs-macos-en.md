---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Fix Docker OverlayFS Corruption on macOS
translated: false
type: note
---

The error you're seeing, `driver "overlay2" failed to remove root filesystem: readdirnames /var/lib/docker/overlay2/.../merged: readdirent merged: bad message`, indicates a deep corruption within Docker's storage mechanism (OverlayFS) that is often caused by an interrupted operation or a host machine filesystem issue.

Since you're on **macOS** (which runs Docker Desktop), the Docker daemon and its storage are managed inside a dedicated **Linux Virtual Machine (VM)**. You don't have direct access to `/var/lib/docker/overlay2` like you would on native Linux, making the fix simpler and safer by focusing on the Docker Desktop app itself.

Here is the safest and most effective sequence of steps to resolve this on macOS:

-----

## 1\. Force-Stop and Force-Remove the Container

The container that failed is `chat-mongodb` (ID: `ccd89a3f36a1528cb923c90de8755faeb36e229cab353c2285222948197b8d18`). First, try a forced removal using its name or ID.

1. **Stop the entire stack** (to ensure no background process is holding a lock):

    ```bash
    docker compose stop
    ```

2. **Force-remove the specific container** using the `-f` flag:

    ```bash
    docker rm -f chat-mongodb
    # OR using the ID:
    # docker rm -f ccd89a3f36a1528cb923c90de8755faeb36e229cab353c2285222948197b8d18
    ```

3. **Try running your original command again** (`docker compose down` or equivalent). If the error persists, move to step 2.

-----

## 2\. Restart Docker Desktop

A simple restart often clears up transient lock issues or corrupted states within the internal VM.

### Option A: Using the Menu Bar (Recommended)

1. Click the **Docker Whale icon** in your macOS menu bar.
2. Select **Restart**.

### Option B: Using the Terminal

You can force quit and reopen the application:

```bash
killall Docker && open /Applications/Docker.app
```

After Docker restarts, wait about 30 seconds for it to fully start, then try running your original command again.

-----

## 3\. Clear Docker's Cache and Unused Data (Prune)

If the restart fails, a powerful cleanup command can often resolve deeper corruption issues by removing unused or "dangling" components that might be related to the error.

**WARNING:** This command removes all stopped containers, unused networks, and dangling images. If you have containers you want to keep stopped (but not removed), back them up or skip this step.

Run the following command in your terminal:

```bash
docker system prune -a --volumes
```

* **`-a`** (all) removes all unused images (not just dangling ones).
* **`--volumes`** removes unused anonymous volumes (which might be the source of the `overlay2` corruption).

You will be asked to confirm. Type `y` and press Enter. After the prune completes, try running your original command again.

-----

## 4\. Factory Reset Docker Desktop

This is the **last resort** as it will **delete all your containers, images, and volumes** (including any local data you have stored in non-mounted volumes). It forces a completely fresh start of the internal Docker VM.

1. Click the **Docker Whale icon** in your macOS menu bar.
2. Go to **Settings (or Preferences)** $\rightarrow$ **Troubleshoot**.
3. Click **Reset to factory settings...**

After the reset, Docker will restart with a clean slate, and you should be able to run your `docker compose up` command to rebuild your environment.
