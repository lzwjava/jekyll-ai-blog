---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Chatbot Setup Summary
translated: false
type: note
---

Here's the full summary of what was done this session.

---

## RunPod LibreChat + SGLang Setup — Complete Summary

### Server
- **Host:** `213.173.110.200:23634` (key: `~/.ssh/id_ed25519`)
- **Chatbot URL:** `http://213.173.110.200:8888` (LibreChat UI)

### Services Running

| Service | Internal Port | Status | Details |
|---------|-------------|--------|---------|
| **SGLang** | 30000 | ✅ | Qwen 2.5 14B AWQ, warmed up with CUDA graphs |
| **MongoDB** | 27017 | ✅ | Data at `/workspace/mongodb` |
| **LibreChat** | 8889 | ✅ | Serves through nginx proxy on 8888 |
| **nginx** | 8888 | ✅ | Proxies 8888 → 8889 with 300s timeout |

### What Was Done

1. **Inspected the server** — found SGLang running on 30000 with Qwen 14B AWQ, LibreChat cloned at `/workspace/LibreChat` with `.env` and `librechat.yaml` already configured to use SGLang.

2. **Freed port 8888** — killed Jupyter Lab that was occupying it.

3. **Started MongoDB** — `mongod --dbpath /workspace/mongodb --logpath /workspace/mongodb/mongod.log --fork` (wasn't running).

4. **Fixed empty `actions.ts`** — `packages/data-provider/src/actions.ts` was 0 bytes from the shallow git clone. Restored via `git checkout`. This had a knock-on effect: the client Vite build failed with missing exports (`validateAndParseOpenAPISpec`, `openapiToFunction`).

5. **Rebuilt Node native modules** — MongoDB driver v6.20.0's native BSON addon was incompatible with Node v22.23.1. `npm rebuild mongodb` fixed the ABI mismatch.

6. **Built the client** — `npm run build:packages` then `vite build` succeeded. The client dist is at `/workspace/LibreChat/client/dist/`.

7. **Changed port** — `.env`: `PORT=8888` → `PORT=8889`. Added nginx reverse proxy on port 8888 (`/etc/nginx/conf.d/librechat.conf`) forwarding to 8889. This ensures:
   - External requests hit nginx on 8888
   - nginx adds proper proxy headers and a 300s timeout
   - LibreChat backend runs on 8889 internally

8. **Started LibreChat** — Running on port 8889, served externally via nginx on 8888.

### Files Saved to `runpod/`

| File | Purpose |
|------|---------|
| `start_services.sh` | One-command restart: MongoDB → check SGLang → rebuild native modules → start LibreChat → verify |
| `build_librechat.sh` | Full rebuild: restore git files → build packages → Vite client build |
| `start_librechat.md` | Runbook with current state, service table, verification commands |
| `setup_librechat.sh` | *(pre-existing)* Older script, port 3080-based, still there for reference |

### Key Pitfalls Encountered

1. **Shallow git clone** → empty `actions.ts` → client build fails with missing OpenAPI exports
2. **Node v22 vs mongodb v6** → native addon ABI mismatch → process hangs silently on `require("mongodb")` with no error message
3. **SSH disconnect kills children** → `nohup`/`&` from SSH don't survive disconnection, must use `setsid` + background terminal
4. **LibreChat DOMAIN_SERVER = 0.0.0.0** → wrong for external access, switched to `127.0.0.1` for nginx backend

### Access

Open `http://213.173.110.200:8888` in your browser. Register an account, then select **Qwen 2.5 14B AWQ** in the model picker to chat.
