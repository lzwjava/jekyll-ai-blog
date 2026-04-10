---
audio: false
generated: true
image: false
lang: en
layout: post
title: Camoufox-js fetch verbose option absence
translated: false
type: note
---

Question: What is the verbose option for the command "npx camoufox-js fetch"?

Answer:

The `npx camoufox-js fetch` command does **not** have an official `--verbose` or `-v` flag.

The JavaScript version (`camoufox-js`) is a lightweight wrapper/port and its fetch command is very simple. It only shows basic progress like:

```
Fetching Camoufox binaries...
Downloading Camoufox... [----------------------------------------] 0% 1523.2s
```

There is no built-in verbose mode to show more detailed logs (such as exact download URL, HTTP headers, or chunk-by-chunk speed).

### Best Ways to Get More Information While Downloading:

1. **Combine with proxy (as you asked before)** – this is still the most useful:
   ```bash
   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
   ```

2. **Force re-download** (useful if the previous download was corrupted):
   ```bash
   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch --force
   ```
   (Note: `--force` may or may not be supported; if it shows an error, just delete the cache folder manually and retry.)

3. **See more output using npm/npx verbose mode** (helps a little):
   ```bash
   npm_config_loglevel=verbose HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
   ```

4. **Manual download workaround (most transparent)**:
   - First, find the real download URL by looking inside the package.
   - Run this to locate the cache and source:
     ```bash
     find ~/.cache -name "*camoufox*" 2>/dev/null || echo "No cache found yet"
     ```
   - Many users in China end up downloading the large binary manually via browser + VPN/proxy and placing it in the correct cache folder.

### Quick Tip for Your Situation (China + slow download):
The best practical command right now is:
```bash
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
npx camoufox-js fetch
```

Make sure your proxy (Clash, V2Ray, etc.) is running and set to **Global** or **Proxy Mode** before running it.

If you want, run this first to test if the proxy works for downloads:
```bash
HTTP_PROXY=http://127.0.0.1:7890 curl -I https://www.google.com
```

Would you like commands to manually find and clear the Camoufox download cache so you can start fresh?

References:  
- https://github.com/apify/camoufox-js  
- https://www.npmjs.com/package/@askjo/camoufox-browser  
- https://www.mintlify.com/jo-inc/camofox-browser/installation