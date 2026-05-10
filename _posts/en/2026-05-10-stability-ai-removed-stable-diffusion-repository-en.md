---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stability AI Removed Stable Diffusion Repository
translated: false
type: note
---

**Question:** Why did the GitHub repository `git@github.com:Stability-AI/stablediffusion.git` (shown in the `.git/config` file) stop working / get shut down?

**Answer:**

## The `Stability-AI/stablediffusion` Repository Has Been Removed

Your local project at `~/projects/stablediffusion` has its Git remote configured to point to `git@github.com:Stability-AI/stablediffusion.git`. This remote is now **dead** — the repository no longer exists on GitHub.

### What Happened?

The `https://github.com/Stability-AI/stablediffusion` repository is no longer available, as it was either removed or made private by Stability AI.

The official reason, as stated by Stability AI, is related to **model deprecation and regulatory compliance**. Stability AI officially deprecated Stable Diffusion 2.0 and 2.1 as part of their effort to clean up and consolidate their model offerings and to get ahead of upcoming compliance requirements for the EU AI Act in 2026. These models have been outpaced by newer architectures that offer stronger performance, safety, and alignment, and continuing to maintain them does not fit their long-term roadmap.

### Impact

This removal only affects **new installations** that try to clone the repository. Existing installations that had already cloned the repo are unaffected.

### What Can You Do?

Since your `.git/config` still points to the now-deleted repo, any `git fetch`, `git pull`, or `git push` to `origin` will fail with:

```
remote: Repository not found.
fatal: repository 'https://github.com/Stability-AI/stablediffusion.git/' not found
```

**Your options:**

1. **Use a community mirror** — The AUTOMATIC1111 WebUI project has already patched their installer to use a community fork. They switched the stable diffusion repo URL from `https://github.com/Stability-AI/stablediffusion.git` to the fork at `https://github.com/w-e-w/stablediffusion.git`. You can update your own remote similarly:

   ```bash
   git remote set-url origin https://github.com/w-e-w/stablediffusion.git
   ```

2. **Keep your local copy as-is** — If you already have a full local clone, you don't need the remote for day-to-day work. You just won't be able to pull upstream updates (since upstream is gone anyway).

3. **Switch to a maintained alternative** — Consider migrating to actively maintained SD repositories such as:
   - [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion) (the original SD 1.x codebase)
   - [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
   - [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

**References:**

- [AUTOMATIC1111 WebUI Issue #17204 – Repository not found](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/17204)
- [AUTOMATIC1111 WebUI Discussion #17212 – Fix for the clone failure](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/17212)
- [HuggingFace Discussion – SD 2.1 deprecation statement](https://huggingface.co/spaces/stabilityai/stable-diffusion-3.5-large/discussions/648)