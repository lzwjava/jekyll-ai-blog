---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Troubleshooting LibreChat Localhost Access
translated: false
type: note
---

### Troubleshooting LibreChat Access on localhost:3080

Based on your logs, the Docker images pulled successfully (after some initial timeouts and retries), and 6 components started: the default network, `vectordb`, `chat-mongodb`, `chat-meilisearch`, `rag_api`, and `LibreChat`. However, the `api` service (which typically serves the backend on port 3080) isn't listed in the started containers—this is likely why you can't access the site. The `LibreChat` container is probably the frontend, which depends on the `api` backend.

The UID/GID warnings suggest potential permission issues that could prevent the `api` container from starting properly. Here's a step-by-step guide to diagnose and fix this.

#### 1. **Verify Running Containers and Ports**
   Run this to see all active containers, their status, and port mappings:
   ```
   docker ps
   ```
   - Look for an `api` container (it might be named `librechat_api` or similar). If it's missing or exited, that's the issue.
   - Confirm if port `3080` is mapped (e.g., `0.0.0.0:3080->3080/tcp`). If not, the service isn't exposing it.
   - If no containers show port 3080, proceed to the next steps.

#### 2. **Check Container Logs**
   Inspect logs for errors in startup, especially for the `api` and `LibreChat` services:
   ```
   docker logs LibreChat
   docker logs api  # Or docker logs librechat_api if named differently
   docker logs rag_api  # In case of dependency issues
   ```
   - Common errors: Permission denied (due to UID/GID), MongoDB/Meilisearch connection failures, or binding issues (e.g., not listening on 0.0.0.0).
   - If logs show the server starting but binding only to localhost inside the container, add `HOST=0.0.0.0` to your `.env` file.

#### 3. **Set UID and GID to Fix Permission Warnings**
   Your `.env` file (copied from `.env.example`) likely has these vars commented out. Unset vars can cause containers to fail silently due to file permission mismatches.
   - Edit `.env`:
     ```
     UID=1000  # Run `id -u` to get your user ID
     GID=1000  # Run `id -g` to get your group ID
     ```
   - Save, then restart:
     ```
     docker compose down
     docker compose up -d
     ```
   This ensures volumes (like config/logs) are owned by your user.

#### 4. **Test Connectivity**
   - Check if port 3080 is listening locally:
     ```
     curl -v http://localhost:3080
     ```
     - If it times out or refuses connection, the service isn't running/exposed.
   - If `docker ps` shows the port mapped but curl fails, check firewall (e.g., `sudo ufw status`) or try `http://127.0.0.1:3080`.

#### 5. **Additional Fixes if Needed**
   - **Image Pull Issues**: Your first attempt had a "denied" error for `ghcr.io/v2/librechat/librechat/manifests/latest`. If pulls fail again, authenticate with GitHub Container Registry:
     ```
     echo $YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
     ```
     (Create a personal access token at github.com/settings/tokens with `read:packages` scope.)
   - **Use the Recommended Compose File**: The default `docker-compose.yml` is for local builds, which can be finicky. Switch to `deploy-compose.yml` for stable remote images:
     - Rename or backup your current `docker-compose.yml`.
     - Use `deploy-compose.yml` instead: `docker compose -f deploy-compose.yml up -d`.
     - Ensure `.env` has `HOST=0.0.0.0` and `NODE_ENV=production`.
   - **Full Restart with Prune**: If stuck, clean up:
     ```
     docker compose down -v  # Removes volumes too
     docker system prune -f
     docker compose up -d
     ```
   - **Dependencies**: Confirm MongoDB and Meilisearch are healthy (`docker logs chat-mongodb`, etc.). The `api` depends on them.

After these steps, retry accessing http://localhost:3080. If logs show specific errors (e.g., Mongo connection), share them for more targeted help. This setup works for most users once UID/GID and dependencies are sorted.

[Local Docker Build Fails to Serve on localhost:3080](https://github.com/danny-avila/LibreChat/discussions/3425)
[LibreChat Docker Docs](https://www.librechat.ai/docs/local/docker)
[Env File Configuration (UID/GID)](https://www.librechat.ai/docs/configuration/dotenv)
