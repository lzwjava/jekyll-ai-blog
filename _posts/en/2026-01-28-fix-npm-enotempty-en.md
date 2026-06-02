---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix npm ENOTEMPTY Error Quickly
translated: false
type: note
---

**Question:** How to fix the npm error "ENOTEMPTY: directory not empty" when trying to globally install @anthropic-ai/claude-code?

**Answer:**

This is a very common npm bug / race condition that happens during global package installation or update when npm tries to rename the old folder but the target temporary folder already exists (or has permission issues, or leftover files).

Here are the most reliable ways to fix it, ordered from safest/quickest to more aggressive:

### Quick & Recommended Fixes (try in this order)

1. **Force remove the temporary folder npm created**

   ```bash
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai/.claude-code-*
   ```

   Then retry:

   ```bash
   sudo npm install -g @anthropic-ai/claude-code
   ```

2. **Completely remove the existing package folder first**

   ```bash
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai
   sudo npm install -g @anthropic-ai/claude-code
   ```

3. **Use --force flag (often works when the folder is partially corrupted)**

   ```bash
   sudo npm install -g @anthropic-ai/claude-code --force
   ```

4. **Clean npm cache + force install (good when you suspect cache issues too)**

   ```bash
   sudo npm cache clean --force
   sudo npm install -g @anthropic-ai/claude-code --force
   ```

### If the above still fails (rare)

5. **Manually rename the folder yourself (bypasses npm's rename logic)**

   ```bash
   sudo mv /usr/lib/node_modules/@anthropic-ai/claude-code \
           /usr/lib/node_modules/@anthropic-ai/claude-code-old-$(date +%s)
   sudo npm install -g @anthropic-ai/claude-code
   ```

   Then later you can delete the -old- folder if everything works.

6. **Use npm@latest (sometimes older npm versions have worse rename handling)**

   ```bash
   sudo npm install -g npm@latest
   sudo npm install -g @anthropic-ai/claude-code
   ```

### Most Reliable One-liner Combo (what I usually do)

```bash
sudo rm -rf /usr/lib/node_modules/@anthropic-ai \
           /usr/lib/node_modules/@anthropic-ai/.claude-code-* \
&& sudo npm cache clean --force \
&& sudo npm install -g @anthropic-ai/claude-code --force
```

After any of these succeed, verify with:

```bash
claude-code --version
# or just
claude-code
```

**Note:** The package name `@anthropic-ai/claude-code` does not appear to be an official Anthropic package (as of late 2025 / early 2026). Make sure you're installing the tool you actually intend to use.

**References:**

- None (common npm error, well documented across Stack Overflow, GitHub issues, and npm bug tracker)
