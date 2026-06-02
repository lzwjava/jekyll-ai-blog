---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring RubyGems Proxy Settings
translated: false
type: note
---

To ensure that `gem` (RubyGems) is using your proxy (e.g., at `http://127.0.0.1:7890`) during installation, follow these steps. Based on the verbose output you shared, it *already appears to be using the proxy*—the "Connecting to 127.0.0.1:7890... connected" line is a strong indicator from the underlying HTTP client (likely `net/http` or `curl`-like behavior in verbose mode).

### 1. **Configure the Proxy (if not already set)**

- **Option A: Use environment variables (recommended for one-off or sudo commands)**
     These tell `gem` to route traffic through the proxy. Run this before your install:

     ```
     export http_proxy=http://127.0.0.1:7890
     export https_proxy=http://127.0.0.1:7890
     sudo -E gem install jekyll bundler --verbose
     ```

  - The `-E` flag preserves your environment variables when using `sudo`.
  - For persistent setup, add the `export` lines to your `~/.bashrc` or `~/.profile`.

- **Option B: Configure in `~/.gemrc` (user-level, no sudo needed for future installs)**
     Create or edit `~/.gemrc`:

     ```
     echo 'http_proxy: http://127.0.0.1:7890' >> ~/.gemrc
     echo 'https_proxy: http://127.0.0.1:7890' >> ~/.gemrc
     ```

     Then run `gem install jekyll bundler --verbose` (without `sudo` if possible—`sudo` can ignore user configs). If using `sudo`, stick with Option A.

### 2. **Verify It's Using the Proxy**

- **Run with `--verbose` (as you did)**: Look for lines like:
  - `HEAD https://index.rubygems.org/` followed by proxy connection details.
  - `Connecting to 127.0.0.1:7890... connected.` (this confirms proxy usage).
  - If it shows direct connections to `rubygems.org` (e.g., IP addresses without proxy mention), it's bypassing the proxy.

- **Test with a dry-run or info fetch**:

     ```
     gem fetch jekyll --verbose --platform=ruby
     ```

     Or just query the index:

     ```
     gem search jekyll --verbose
     ```

     Check the output for proxy connections.

- **Check environment variables**:

     ```
     echo $http_proxy $https_proxy
     ```

     If they're set correctly, `gem` should inherit them.

- **Debug with `gem env`**:

     ```
     gem env
     ```

     Look under "HTTP Proxy" or "HTTPS Proxy" sections for your proxy URL.

### Troubleshooting

- **If sudo ignores the proxy**: Use `sudo -E` or run without `sudo` (install to user dir: `gem install --user-install jekyll bundler`).
- **No connection lines?** Your proxy might not be verbose-enabled, or env vars aren't set. Test the proxy separately: `curl -v https://rubygems.org/` (should show proxy hops).
- **Corporate/strict proxy?** If it requires auth, use `http://user:pass@127.0.0.1:7890`.
- **Still failing?** Temporarily disable the proxy (`unset http_proxy https_proxy`) and retry—if it works without, the issue is config; if not, check your proxy server (e.g., Clash/V2Ray logs).

Your install succeeded (200 OK responses), so you're likely good—just confirm the next run shows the proxy connection for peace of mind. If you share more output, I can debug further!
