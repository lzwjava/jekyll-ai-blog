---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run FLUX.2-dev in tmux via SSH
translated: false
type: note
---

All set up. Now SSH in and run in a **tmux session** (so it persists even if you disconnect):

```bash
ssh -p 31145 root@36.150.116.206

# Start tmux
tmux new -s flux

# Activate env and run
source /root/flux_env/bin/activate
python3 /root/run_flux.py
```

The download is **~35GB** and will take some time (~15-30 mins depending on mirror speed). The script will:
1. ✅ Download FLUX.2-dev from the HuggingFace mirror
2. ✅ Load the model onto your AMD GPU (48GB VRAM)
3. ✅ Generate a test image (`test_flux.png`)

To **detach** from tmux and leave it running: `Ctrl+B, then D`
To **re-attach** later: `tmux attach -t flux`
