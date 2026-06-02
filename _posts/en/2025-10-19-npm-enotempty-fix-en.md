---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing npm ENOTEMPTY Installation Error
translated: false
type: note
---

### Understanding the Error

Your `sudo npm i -g @anthropic-ai/claude-code --verbose` command is failing with an `ENOTEMPTY` error during the installation process. This is a common npm issue that occurs when npm tries to rename (or move) an existing directory as part of updating or reinstalling a package, but the directory isn't empty. In this case, it's specifically failing to rename `/usr/lib/node_modules/@anthropic-ai/claude-code` to a temporary backup location (`/usr/lib/node_modules/@anthropic-ai/.claude-code-ZjqcDZyQ`).

This typically happens due to:

- A previous partial or interrupted installation leaving behind files or subdirectories.
- File locks from another process (e.g., if the package was partially loaded or another npm command is running).
- Rarely, permission quirks with global installs under `sudo`.

The package itself (`@anthropic-ai/claude-code`) is legitimate—it's Anthropic's official CLI tool for "Claude Code," an agentic coding assistant that integrates with your terminal and codebase.

### Quick Fixes

Try these steps in order. Run them as root or with `sudo` where noted, since this is a global install.

1. **Manually Remove the Existing Directory**
   This clears out the problematic partial install:

   ```
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai/claude-code
   ```

   - If the parent scoped directory (`@anthropic-ai`) is now empty, you can remove it too:

     ```
     sudo rm -rf /usr/lib/node_modules/@anthropic-ai
     ```

   Then retry your original command:

   ```
   sudo npm i -g @anthropic-ai/claude-code --verbose
   ```

2. **Clear npm Cache**
   If the above doesn't work, corrupted cache entries might be involved:

   ```
   sudo npm cache clean --force
   sudo npm cache verify
   ```

   Retry the install after this.

3. **Check for Running Processes**
   Ensure no other npm/Node processes are using the directory:

   ```
   ps aux | grep npm
   ```

   Kill any lingering ones if needed (e.g., `sudo kill <PID>`), then retry.

4. **Alternative: Use npx for Testing**
   If you just want to test the tool without a full global install, try:

   ```
   npx @anthropic-ai/claude-code --help
   ```

   This downloads and runs it temporarily without modifying your global modules.

### Additional Tips

- **Permissions Best Practice**: Global installs with `sudo` can lead to ownership issues later. Consider using a node version manager like `nvm` to avoid `sudo` entirely, or set a custom global prefix:

  ```
  mkdir ~/.npm-global
  npm config set prefix '~/.npm-global'
  export PATH=~/.npm-global/bin:$PATH
  ```

  Then install without `sudo`.
- **Verify After Install**: Once installed, check with `claude-code --version` (assuming that's the binary name—confirm in the docs).
- If issues persist, share the output of `npm ls -g @anthropic-ai/claude-code` for more diagnostics.

This should get you up and running quickly. If you hit another snag, paste the new log!

[Claude Code on npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)
[Anthropic Docs: Set up Claude Code](https://docs.claude.com/en/docs/claude-code/setup)
