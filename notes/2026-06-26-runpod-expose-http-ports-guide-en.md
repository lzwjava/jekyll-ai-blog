---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Expose HTTP Ports Guide
translated: false
type: note
---

Question: How do I configure "Expose HTTP ports (max 10)" in RunPod?

Answer:

The "Expose HTTP ports" field tells RunPod which ports inside your container should be reachable over HTTP through its proxy. You enter a comma-separated list of port numbers (max 10).

How it works:

- Enter the port(s) your app listens on, e.g. `8888,7860,8000`.
- RunPod's proxy maps each to a public URL: `https://<​POD_ID>-<​PORT>.proxy.runpod.net`
- The proxy terminates TLS and forwards to your container over HTTP, so your app just needs to bind plain HTTP on that port.

Critical requirement — bind to `0.0.0.0`, not `localhost`:

```bash
# Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Common app servers
python -m http.server 8000 --bind 0.0.0.0
# FastAPI / uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
# Gradio
demo.launch(server_name="0.0.0.0", server_port=7860)
```

If you bind to `127.0.0.1`, the proxy can't reach it and you'll get a 502.

Typical setup:

| Field | Value |
|-------|-------|
| Expose HTTP Ports | `8888,7860,8000` |
| Expose TCP Ports | `22` (SSH — uses direct TCP, not the HTTP proxy) |

Notes:

- HTTP ports go through the `*.proxy.runpod.net` reverse proxy (good for web UIs, APIs, notebooks).
- TCP ports (like SSH `22`) get a direct `<​IP_ADDRESS>:<​PORT>` mapping instead — use that field for SSH or anything non-HTTP.
- The proxy only speaks HTTP/WebSocket on the container side. For raw TCP services (Redis, Postgres, custom protocols), use Expose TCP Ports.
- You set this either in the template config or when deploying the pod; on a running pod you generally need to edit the template and redeploy to change exposed ports.
- The proxy has an idle/timeout behavior (~100s) that can cut long-lived requests — for streaming or long jobs, prefer a TCP port or keep connections active.

References:

- [RunPod Docs — Expose Ports](https://docs.runpod.io/pods/configuration/expose-ports)
- [RunPod Docs — Connect to a Pod](https://docs.runpod.io/pods/connect-to-a-pod)
