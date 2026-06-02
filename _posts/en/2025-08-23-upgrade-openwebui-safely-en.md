---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade Open WebUI Safely Now
translated: false
type: note
---

Got you. Here are the safe, no-nonsense ways to upgrade Open WebUI.

## If you installed with `pip` (your case)

```bash
# 1) (Recommended) activate the env you use for Open WebUI
#    e.g. conda:
conda activate open-webui
#    or venv:
# source ~/open-webui-venv/bin/activate

# 2) Upgrade to latest
python3.11 -m pip install -U open-webui

# 3) (Optional) if pip caching causes trouble
python3.11 -m pip cache purge
python3.11 -m pip install --no-cache-dir -U open-webui

# 4) Verify what you got
python3.11 -m pip show open-webui
```

Official docs say just `pip install -U open-webui` upgrades to the latest release. ([Open WebUI][1])

### Keep your data/settings persistent

When you run the server, you can pin a data directory so upgrades don’t touch it:

```bash
# macOS/Linux
DATA_DIR="$HOME/.open-webui" open-webui serve
# Windows (PowerShell)
$env:DATA_DIR="C:\open-webui\data"; open-webui serve
```

This mirrors the docs’ guidance to set `DATA_DIR` (or use `uvx … @latest serve` with the same variable) so your chats/config live outside the package install. ([Open WebUI][2])

> Tip: If you previously ran without `DATA_DIR`, start using it now; Open WebUI will use that folder going forward.

## If you used Docker (for completeness)

```bash
# stop & remove old container (data is in the named volume)
docker rm -f open-webui

# pull the latest image
docker pull ghcr.io/open-webui/open-webui:main

# start again with your existing volume
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

This is the project’s recommended manual update flow; your data persists in the `open-webui` Docker volume. ([Open WebUI][3])

## Check what “latest” is

You can confirm the newest tag from GitHub Releases before/after you upgrade. ([GitHub][4])

If anything errors (e.g., Python version mismatch), ensure you’re on Python 3.11 for the pip method, which the project explicitly recommends. ([GitHub][5])

Want me to spot-check your current env or interpret any upgrade error output? Paste it here and I’ll troubleshoot.

[1]: https://docs.openwebui.com/getting-started/quick-start/?utm_source=chatgpt.com "️ Quick Start"
[2]: https://docs.openwebui.com/?utm_source=chatgpt.com "Open WebUI: Home"
[3]: https://docs.openwebui.com/getting-started/updating/?utm_source=chatgpt.com "Updating Open WebUI"
[4]: https://github.com/open-webui/open-webui/releases?utm_source=chatgpt.com "Releases · open-webui/open-webui"
[5]: https://github.com/open-webui/open-webui?utm_source=chatgpt.com "open-webui/open-webui: User-friendly AI Interface ..."
