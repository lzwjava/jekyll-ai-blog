---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Video Generator with Providers
translated: false
type: note
---

Done! Here's a summary of everything created:

---

## What was built

### Provider System (`ahl/gen_video/providers/`)

| File | Description |
| --- | --- |
| `base.py` | `ImageProvider` abstract base class |
| `factory.py` | `create_provider()` — creates providers by name: `openrouter`, `local`, `auto` |
| `openrouter_provider.py` | Uses OpenRouter API (`black-forest-labs/flux.2-pro`) — existing behavior, extracted to provider |
| `local_provider.py` | **New** — runs FLUX inference on the local AMD GPU using diffusers (`FLUX.1-schnell`, `FLUX.1-dev`, `FLUX.2-dev`) |

### Frontend UI (embedded in `server.py`)

- Beautiful dark theme single-page app
- **Step 1**: Topic input box → generates AI markdown content via `POST /api/generate-content`
- **Step 2**: Content preview with edit/regenerate
- **Step 3**: Provider selector with 3 options:
  - ☁️ **OpenRouter** — `black-forest-labs/flux.2-pro`
  - 🖥️ **Local GPU** — FLUX on AMD GPU (with variant selector: schnell/dev/2-dev)
  - ⚡ **Auto** — tries local first, falls back to OpenRouter
- Real-time job polling with logs
- Video preview + download
- Recent jobs list with quick download

### API Endpoints

| Endpoint | Description |
| --- | --- |
| `GET /` | Frontend UI |
| `POST /api/generate-content` | Generate markdown from a topic via LLM |
| `POST /api/generate-video` | Submit video job (accepts `provider`, `local_variant`) |
| `GET /api/jobs/{id}` | Job status |
| `GET /api/jobs/{id}/download` | Download completed video |

### Start the server

```bash
ahl server
# or on remote:
ahl gen-video server
```
