---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stuck Installing Node.js Dependencies
translated: false
type: note
---

Question: Why is the Hermes Agent Installer stuck at "Installing Node.js dependencies (browser tools)" on macOS after previous steps succeeded?

Answer:

The installer is now stuck at the **Node.js dependencies** step because it is running `npm install` (for browser automation tools and the WhatsApp bridge) inside the cloned repository at `/Users/lzwjava/.hermes/hermes-agent`, and this `npm install` command is hanging.

This is a very common issue with `npm install` on macOS (and other platforms). The script likely does something like `cd /Users/lzwjava/.hermes/hermes-agent && npm install` (often with `--silent` or without verbose output), so you see no progress and it appears frozen.

### Most likely causes:
- **Network / npm registry timeout or slow connection** — npm is trying to download packages from the default registry (`registry.npmjs.org`) and is stalling.
- **Large dependency downloads** — Playwright (used for browser tools) downloads Chromium and other binaries, which can take a long time or hang on slow/unstable connections.
- **npm cache or lockfile issues**.
- **Proxy, VPN, or firewall interfering** with npm's network requests.
- **Node.js/npm version quirks** on macOS (your Node.js is v25.3.0, which is quite new; sometimes very recent versions have temporary compatibility hiccups).

### How to fix it right now:

1. **Cancel the current install**
   Press **Ctrl + C** (multiple times if needed) to stop the installer.

2. **Go to the project folder**
   ```bash
   cd /Users/lzwjava/.hermes/hermes-agent
   ```

3. **Try these fixes one by one** (most effective first):

   - **Use a faster mirror (highly recommended for China or slow connections)**:
     ```bash
     npm install --registry=https://registry.npmmirror.com
     ```

   - **Clear npm cache and retry**:
     ```bash
     npm cache clean --force
     npm install
     ```

   - **Run with verbose output to see where it is actually stuck**:
     ```bash
     npm install --verbose
     ```
     (Watch the output — it will show exactly which package is causing the delay.)

   - **Delete node_modules and lockfile then reinstall** (clean start):
     ```bash
     rm -rf node_modules package-lock.json
     npm install
     ```

   - **Install Playwright browsers explicitly after npm install** (if it gets past the main install):
     ```bash
     npx playwright install --with-deps chromium
     ```

4. **After successful `npm install`**, rerun the Hermes installer or continue manually:
   ```bash
   # If the installer exited, you can usually just run it again
   # Or continue with:
   hermes doctor   # to check everything
   ```

### Extra macOS-specific tips:
- Make sure you have a stable internet connection (try switching networks or disabling VPN temporarily).
- If you are behind a corporate proxy, configure npm with `npm config set proxy http://your-proxy:port`.
- Update npm itself:
  ```bash
  npm install -g npm@latest
  ```

Once the Node.js dependencies install successfully, the rest of the Hermes setup should complete without issues.

If it still hangs, run the verbose command above, copy the last few lines of output, and share them here for more precise help. You can also check the official GitHub issues for Hermes Agent if this turns out to be a recent bug.

References:
- https://github.com/NousResearch/hermes-agent (project repository and known installer behavior)
- https://hermes-agent.nousresearch.com/docs/reference/faq/ (official troubleshooting)
- Common npm install hanging solutions from Stack Overflow and npm community reports.
