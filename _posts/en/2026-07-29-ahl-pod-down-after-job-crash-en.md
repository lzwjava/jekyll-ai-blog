---
audio: false
generated: true
image: false
lang: en
layout: post
title: AHL Pod Down After Job Crash
translated: false
type: note
---

The pod has gone down and hasn't come back up. Here's the situation:

---

## 🚨 Server is Down

SSH port **31005** — Connection refused
Tunnel URL — **404 Not Found**

## 🔍 What Likely Happened

The **AHL video generation job** was submitted and went to `processing` state, but then errored out (went to "Not found"). This likely crashed the AHL server or caused an OOM kill, since the AHL process was using **~35GB of RAM**. The pod then restarted or was terminated.

## 🛠️ Possible Causes

1. **OOM (Out of Memory)** — The video generation model (FLUX) is very memory-hungry, and the pod may have been killed when it exceeded limits
2. **Pod restart** — If the Jupyter process (PID 1) exited, the pod restarts
3. **Job backend crash** — The gen-video processing encountered an error and crashed

## Next Steps

Try these once the pod comes back up:

1. **Check if the pod is still alive** from the platform console
2. If recreated, re-run the tunnel setup:

   ```bash
   ssh -p 31005 root@36.150.116.206
   export FRP_BROKER_URL=$(grep -z FRP_BROKER_URL /proc/1/environ | tr "\0" "\n" | cut -d= -f2-)
   export FRP_BROKER_TLS_SERVER_NAME=$(grep -z FRP_BROKER_TLS_SERVER_NAME /proc/1/environ | tr "\0" "\n" | cut -d= -f2-)
   export PATH="$HOME/.local/bin:$PATH"
   /var/run/secrets/frp-self-service/install
   rc-tunnel expose --port 8000
   ```

3. Check AHL server logs:

   ```bash
   curl http://127.0.0.1:8000/health  # if the server is up
   ```

Would you like me to keep trying to reconnect periodically?
