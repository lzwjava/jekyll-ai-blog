---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restart RunPod After Crash
translated: false
type: note
---

The RunPod instance is down — SSH connection refused. The server likely crashed or was terminated (possibly the OOM from the client build processes or the Node process hitting a resource limit).

To recover, recreate the RunPod pod, then run:

```bash
bash runpod/start_services.sh
```

If the pod's filesystem is persisted, this will pick up the existing `/workspace/LibreChat` with everything already built. If it's a fresh pod, run `build_librechat.sh` first to rebuild the client, then `start_services.sh`.

Let me know when you've restarted the pod and I'll verify and fix anything that needs attention.
