---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing npm postinstall script hang
translated: false
type: note
---

Question: Why is my npm install getting stuck at the @askjo/camoufox-browser postinstall script, and what does the SIGINT message mean after I press Ctrl+C?

Answer:

The output you shared confirms the exact cause of the hang.

### What happened:
- npm was running the **postinstall** script for `@askjo/camoufox-browser@1.0.12`.
- That script executes: `npx camoufox-js fetch || true`
- This command was **still running** (and probably downloading a large browser binary) when you pressed Ctrl + C.
- Because you interrupted it, npm reported:
  ```
  npm info run @askjo/camoufox-browser@1.0.12 postinstall { code: null, signal: 'SIGINT' }
  ```
  SIGINT simply means “the process was interrupted by the user” (Ctrl+C).

The spinner (`⠇ ⠋ ⠙ ⠸`) staying visible means the `camoufox-js fetch` process did **not** exit cleanly or quickly, so npm was waiting for it.

### Why it gets stuck:
`camoufox-js fetch` downloads a full browser (Camoufox, a Firefox-based browser used for automation). These downloads are often:
- Very large (100 MB – 300 MB+)
- Slow on certain networks
- Prone to hanging if the connection is unstable, behind a firewall/proxy, or if the download server is slow

Even the `|| true` part doesn’t always help if the child process itself freezes.

### How to fix it properly:

1. **Clean up and try again with better control**  
   First, remove the partially installed package:
   ```bash
   rm -rf node_modules/@askjo/camoufox-browser
   ```

2. **Install while skipping scripts temporarily** (fastest workaround)
   ```bash
   npm install --ignore-scripts
   ```

3. **Manually run the fetch with more visibility** (recommended)
   After the install finishes with `--ignore-scripts`, run the fetch manually so you can see progress:
   ```bash
   npx camoufox-js fetch
   ```
   - Watch the output carefully. If it still hangs, you’ll see exactly where.
   - You can also try adding any verbose flags if the tool supports them (e.g. `npx camoufox-js fetch --verbose`).

4. **Full clean reinstall (if problems continue)**
   ```bash
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install --ignore-scripts
   npx camoufox-js fetch
   ```

5. **Network-related solutions**
   - Use a faster or different internet connection (mobile hotspot sometimes helps).
   - Disable VPN/proxy temporarily if you’re using one.
   - Try running the fetch during off-peak hours if the server is busy.

6. **Alternative: Skip this dependency entirely if you don’t need it**
   If this project doesn’t actually require Camoufox (it seems related to browser automation/hermes-agent), you could remove or replace the dependency. But only do this if you understand the project’s requirements.

### Quick test:
After doing `npm install --ignore-scripts`, run this to check if the fetch works:
```bash
npx camoufox-js fetch
```

If the manual fetch also hangs or fails, the issue is definitely with the download itself (network, firewall, or the camoufox download server).

Would you like me to give you commands to check your network speed or see what files camoufox is trying to download? Just let me know the result after trying the manual `npx camoufox-js fetch`.

References:  
- None