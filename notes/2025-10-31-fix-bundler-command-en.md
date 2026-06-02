---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix Bundler Command Not Found
translated: false
type: note
---

### Understanding the Issue
Your `gem install jekyll bundler` succeeded (it installed 30 gems, including Bundler 2.7.2), but the `bundle` command isn't found. This is a common PATH/environment issue on Ubuntu/Debian systems after a system-wide `sudo gem install`. Gems install binaries to `/usr/local/bin` (or similar), but your shell's `$PATH` might not include it, or the change hasn't propagated (e.g., need to reload your profile).

The system's suggestion to `apt install ruby-bundler` would install an older version (2.4.20) via apt, which could conflict with your gem-installed Bundler 2.7.2—avoid that for now. Same for snap; it might isolate Ruby in a way that breaks gem paths.

### Quick Fix: Verify and Use the Installed Bundler
1. **Check where `bundle` is installed**:
   ```
   gem environment
   ```
   - Look for "EXECUTABLE DIRECTORY" (likely `/usr/local/bin`). Note that path.

2. **Locate and test `bundle` directly**:
   ```
   which bundle  # If nothing, try: find /usr/local -name bundle 2>/dev/null
   /usr/local/bin/bundle --version  # Should output "Bundler version 2.7.2"
   ```
   - If it works, great! Use the full path for now: `/usr/local/bin/bundle install`

3. **Run your Jekyll setup with the full path**:
   - In `~/projects/blog-source` (assuming it has a `Gemfile`):
     ```
     /usr/local/bin/bundle install
     /usr/local/bin/bundle exec jekyll serve
     ```
   - This should install Jekyll dependencies and start the server (usually at http://127.0.0.1:4000).

### Permanent Fix: Update Your PATH
If `/usr/local/bin` isn't in your `$PATH`, add it:
1. Edit `~/.bashrc` (or `~/.profile` for login shells):
   ```
   nano ~/.bashrc
   ```
   Add this line at the end:
   ```
   export PATH="/usr/local/bin:$PATH"
   ```

2. Reload your shell:
   ```
   source ~/.bashrc
   ```

3. Verify:
   ```
   echo $PATH  # Should now include /usr/local/bin
   bundle --version  # Should work without full path
   ```

Now retry:
```
bundle install
bundle exec jekyll serve
```

### If That Doesn't Work
- **Permission issues?** (Rare, but sudo can cause them.) Reinstall without sudo (user-local install):
  ```
  gem install --user-install bundler jekyll
  ```
  Then add `export PATH="$HOME/.local/share/gem/ruby/*/bin:$PATH"` to `~/.bashrc` (adjust path from `gem environment`).

- **Ruby version mismatch?** Check with `ruby --version`. If it's system Ruby (e.g., 2.7.x), consider Ruby version managers like `rbenv` (install via `curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash`, then follow setup). This avoids system conflicts long-term.

- **Proxy still in play?** If your env vars (`http_proxy`, etc.) are set, Bundler should inherit them—just ensure they're exported before running.

Your setup should be running smoothly after the PATH tweak. If you hit errors (e.g., share `gem environment` output), paste them for more targeted help!
