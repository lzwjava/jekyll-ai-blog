---
audio: false
generated: true
image: false
lang: en
layout: post
title: npm postinstall script hang fix
translated: false
type: note
---

Question: Why is my npm install getting stuck after running postinstall scripts for packages like fsevents, better-sqlite3, @askjo/camoufox-browser, agent-browser, and geckodriver?

Answer:

Your npm installation appears to be hanging (stuck with the spinner ⠇ ⠋ ⠧) right after several postinstall scripts have finished. This is a common issue, especially on macOS, and here are the most likely causes and fixes:

### Most Common Reasons for the Hang:
1. **@askjo/camoufox-browser postinstall script**  
   The command `npx camoufox-js fetch || true` is likely the culprit.  
   - This script probably downloads a large browser binary (Camoufox is a Firefox-based browser for automation/testing).  
   - Downloads can be very slow, fail silently, or get stuck due to network issues, firewall, VPN, or rate limiting.  
   - Even though it has `|| true`, the underlying process may still be running in the background or hanging.

2. **Network-related problems**  
   - Slow or unstable internet connection while fetching large files (browser binaries, drivers, etc.).
   - Corporate/school firewall or proxy blocking the download.
   - npm registry or GitHub release mirrors being slow.

3. **Other postinstall scripts**  
   - `fsevents` failed (expected on non-macOS or sometimes on macOS with node-gyp issues), but it’s marked as optional so it usually doesn’t block.
   - `better-sqlite3`, `agent-browser`, and `geckodriver` completed successfully (code: 0).
   - However, some scripts can spawn background processes that keep npm waiting.

4. **npm itself being slow or in a bad state**  
   - Large node_modules folder or many dependencies.
   - npm cache corruption.
   - Running out of disk space or memory during extraction/install.

### How to Fix It:

**Immediate actions (try in order):**

1. **Wait a bit longer**  
   The download for camoufox might just be slow. Let it run for 5–10 more minutes before killing it.

2. **Cancel and retry with more visibility**  
   Press `Ctrl + C` to stop, then run:
   ```bash
   npm install --loglevel=verbose
   ```
   This will show more detailed output so you can see exactly which part is hanging.

3. **Skip or fix the problematic postinstall**  
   Try installing while skipping optional dependencies or scripts:
   ```bash
   npm install --ignore-scripts
   ```
   Then manually run the important scripts if needed:
   ```bash
   npx camoufox-js fetch
   ```

   Or force skip the camoufox fetch temporarily:
   ```bash
   npm install --ignore-scripts
   ```

4. **Clear cache and clean install** (recommended if it keeps failing):
   ```bash
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```

5. **Check network and resources**
   - Make sure you have a stable, fast internet connection.
   - Check available disk space: `df -h`
   - Monitor network activity or use a different network/VPN.

6. **Update npm and Node.js**
   ```bash
   npm install -g npm@latest
   ```
   Also consider updating your Node version if it’s very old.

7. **Specific fix for camoufox-browser**  
   If the fetch keeps hanging, you can try running it manually with more output:
   ```bash
   npx camoufox-js fetch --verbose
   ```
   (Check the package documentation for exact flags.)

### Additional Tips:
- This kind of hanging often happens with browser automation packages (puppeteer, playwright, geckodriver, camoufox, etc.) because they download large binaries (~100MB+).
- If you're on macOS (as the path suggests `/Users/lzwjava/...`), fsevents failing is normal if you're not on a real Mac or if Xcode command line tools are missing.
- For `better-sqlite3`, make sure you have Python and build tools installed if it ever fails in the future.

Try the `--loglevel=verbose` version first so you can see what’s actually happening right now.

If you share the full verbose output after it gets stuck again, I can help pinpoint the exact cause more accurately.

References:  
- None