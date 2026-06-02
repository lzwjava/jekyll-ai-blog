---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Skip Camosfox Setup
translated: false
type: note
---

Question: In the Hermes Agent install.sh script for Linux, how to set up Camosfox (Camofox) browser, and can we skip installing it when running install.sh?

Answer:

Yes, you can safely skip or delay **Camosfox** (also called **Camofox**) during the initial `./install.sh` run. It is **not** installed automatically by the main script.

### Quick Summary

- The `install.sh` script installs:
  - Python dependencies (including browser tools via Playwright)
  - Node.js + npm dependencies
  - **Local Chromium** via `npx playwright install chromium --with-deps`
- **Camosfox / Camofox** is an **optional advanced stealth browser** (a self-hosted Node.js wrapper around **Camoufox**, a Firefox fork with strong fingerprint spoofing/anti-detection). It is **not** part of the default install.

You mentioned you filled a fake location and some browser settings can be skipped — this matches the setup for stealth browsing in Hermes Agent.

### Can We Skip It During install.sh?

**Yes, completely.**
The script has no flag to force Camosfox. You can run the installer normally (or with `--skip-setup` if you want to skip the wizard):

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Or with options:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --skip-setup
```

After installation finishes, you can decide whether to set up Camosfox later.

### How to Set Up Camosfox (Camofox) Manually (Recommended for Stealth Use)

1. **Install Camosfox** (after Hermes is installed):

   ```bash
   git clone https://github.com/jo-inc/camofox-browser.git
   cd camofox-browser
   npm install
   npm start
   ```

   - First run will download **Camoufox** (~300MB).
   - It runs a local server (default port 9377).

   Alternative (easier, using Docker):

   ```bash
   docker run -d --network host -e CAMOFOX_PORT=9377 jo-inc/camofox-browser
   ```

2. **Configure Hermes to use it**:
   Edit your config file:

   ```bash
   nano ~/.hermes/.env
   ```

   Add or modify these lines:

   ```
   BROWSER_BACKEND=camofox
   CAMOFOX_URL=http://localhost:9377
   # Or if using Docker/remote: http://127.0.0.1:9377
   ```

   You can also set fake location, user-agent spoofing, etc., inside the Camosfox/Camoufox settings if needed (or let Hermes handle it).

3. **Test it**:
   Run Hermes and ask it to browse a site that usually blocks bots:

   ```
   hermes
   ```

   Then say something like: "Go to example.com and tell me the main content" or use browser tools.

### Alternatives if You Don't Want Camosfox

- **Default**: Hermes uses **local Chromium** (via Playwright) — already installed by the script. Good for most tasks but easier to detect.
- **Cloud options**: You can configure external services like Browser Use for even better stealth (no local install needed).

### Tips for Your Fresh Linux Setup

- You already filled a fake location — that's useful for privacy/stealth. Camosfox makes this much stronger with C++-level fingerprint spoofing.
- If you want to avoid Node.js/browser stuff entirely during install, the script still works fine (browser features just won't be available until you set them up).
- After install, run `hermes setup` to configure API keys and other settings.
- To update later: `hermes update`

If you run into any errors during install (e.g., missing dependencies or Node issues), paste the exact error here and I'll help debug.

The script you shared looks correct and up-to-date for the official Hermes Agent from Nous Research. No major issues in the provided code for skipping the optional stealth browser.

References:

- <https://github.com/NousResearch/hermes-agent>
- <https://hermes-agent.nousresearch.com/docs/user-guide/features/browser> (Camofox setup guide)
- <https://github.com/jo-inc/camofox-browser>
