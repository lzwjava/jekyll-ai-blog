---
audio: false
generated: true
image: false
lang: en
layout: post
title: FluxReel rename complete everywhere
translated: false
type: note
---

Rename to **FluxReel** is complete everywhere. ✅

**What changed** (commit `e49cb31`, pushed to `origin/main`):

| Place | Before | After |
|---|---|---|
| Python package | `ahl/` | `fluxreel/` (git-tracked rename, all 20 files) |
| CLI command | `ahl` | `fluxreel` (`fluxreel img`, `fluxreel server`, `fluxreel tunnel`…) |
| pip package | `ahl 0.2.0` | `fluxreel 0.2.0` (old entry uninstalled) |
| All imports | `from ahl.…` | `from fluxreel.…` |
| Config path | `~/.config/ahl/.env` | `~/.config/fluxreel/.env` |
| pyproject.toml | name/description/script | `fluxreel` + new description |
| fabfile.py | `/root/ahl` deploy target | `/root/fluxreel` |
| Web UI | "🌸 AI Video Generator" | "🌸 FluxReel" + title tag |
| API title | "Gen Video API" | "FluxReel API" |
| localStorage key | `ahl_api_key` | `fluxreel_api_key` |
| Submission docs | `ahl` branding | **FluxReel** branding, commands `fluxreel` |
| PPT | `ahl_slides.pptx` | `fluxreel_slides.pptx` (re-rendered from Marp) |

**Verified working:**
- `python -m fluxreel` and the `fluxreel` console script both run
- All imports resolve (`SdCppProvider` loads fine)
- Server restarted as FluxReel on `:8000`, health OK, new UI branding served

One note: the running server was restarted under the new module (`-m fluxreel.gen_video.server`), and the old `ahl` pip entry was uninstalled — the environment is fully on FluxReel now.