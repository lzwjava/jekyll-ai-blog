---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Templates Explained
translated: false
type: note
---

Question: In RunPod, what does "Your templates" mean when it says "Pre-configure your Docker images once, then reuse them across Pods and Serverless"?

Answer:

A RunPod **Template** is just a saved spec for a container — it's the metadata layer sitting on top of a Docker image, not the image itself. You define it once, then reference it whenever you spin up compute, instead of re-typing the same config every time.

**What a Template actually stores:**

```
Template = {
  container_image: "docker.io/you/your-image:tag",  # from Docker Hub / GHCR / private registry
  container_disk_size_gb: 20,
  volume_disk_size_gb: 50,          # persistent volume, if any
  volume_mount_path: "/workspace",
  docker_start_command: "python3 rp_handler.py",  # or entrypoint override
  env_vars: {"HF_TOKEN": "<SECRET>", "MODEL_NAME": "..."},
  ports: "8888/http,22/tcp",        # exposed ports for Pods (Jupyter, SSH)
  is_serverless: false,             # affects which surfaces can use it
}
```

**Pods vs Serverless — same Template, different runtime semantics:**

| | Pods | Serverless |
|---|---|---|
| Lifecycle | Long-running, you start/stop manually | Ephemeral workers, spun up per-request, scale to zero |
| Entry point | Usually SSH/Jupyter into a running container | Must call `runpod.serverless.start({"handler": handler})` |
| Billing | Per-hour while running | Per-second of actual compute during request handling |
| Networking | Exposed ports (8888, 22, etc.) | No exposed ports — request/response via RunPod's queue |

The reason the same Docker image *usually* doesn't just drop into both: a Pod image expects to run indefinitely and serve interactive access (SSH, Jupyter), while a Serverless image must implement the `runpod` Python SDK's handler pattern and exit gracefully after each job — a GPU Cloud template will not work in Serverless without the Serverless handler, so it's not recommended to use images designed for Pods within Serverless.

So "pre-configure once, reuse across Pods and Serverless" really means: you can point *multiple* endpoint/pod configs at the *same underlying image* (if you build it generically enough — e.g., an image with both an interactive entrypoint and a `rp_handler.py` guarded by an env var), and you don't have to redefine disk size, env vars, exposed ports, etc. every time you deploy. It's a DRY mechanism for deployment config, not a magic compatibility layer between the two runtimes.

**Practical build pattern if you actually want one image serving both:**

```dockerfile
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04
COPY . /workspace
WORKDIR /workspace
RUN pip install runpod torch transformers

# entrypoint.sh decides mode at container start
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/bash
# entrypoint.sh
if [ "$RUNPOD_SERVERLESS" = "1" ]; then
    exec python3 rp_handler.py   # runpod.serverless.start(...)
else
    exec /start.sh               # jupyter lab / sshd for interactive Pod use
fi
```

Then one Template, two deploy targets: set `RUNPOD_SERVERLESS=1` as an env var override when creating the Serverless endpoint, leave it unset for a Pod.

**Where you manage these:** `console.runpod.io/serverless/user/templates` for Serverless-scoped templates, and the equivalent Pods templates page for GPU Cloud — templates can also be created programmatically via `runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")` using the Python SDK, useful if you want to script template creation as part of your CI/CD instead of clicking through the UI.

References:

- [Runpod Serverless Overview](https://docs.runpod.io/serverless/overview)
- [Getting Started with Runpod Serverless](https://trapdoor.cloud/getting-started-with-runpod-serverless/)
- [runpod-python GitHub](https://github.com/runpod/runpod-python)
- [Runpod Quick Deploy](https://docs.runpod.io/serverless/quick-deploys)
