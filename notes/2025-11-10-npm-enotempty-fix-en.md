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

The error `ENOTEMPTY` during `npm i -g` occurs because npm is attempting to replace the existing `@anthropic-ai/claude-code` package directory but can't rename it to a temporary location—likely due to a partial/failed prior install leaving the directory in a locked or inconsistent state.

### Quick Fix

1. **Manually remove the problematic directory** (requires sudo):

   ```
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai/claude-code
   ```

2. **Clear npm cache** (optional but helps with corruption):

   ```
   sudo npm cache clean --force
   ```

3. **Reinstall the package**:

   ```
   sudo npm i -g @anthropic-ai/claude-code
   ```

### If Removal Fails (Permission/Occupied)

- Check for running processes using the directory:

  ```
  sudo lsof /usr/lib/node_modules/@anthropic-ai/claude-code
  ```

  Kill any PIDs if safe (e.g., `sudo kill <PID>`).

- As a last resort, reboot the system to release locks, then retry the `rm -rf`.

Note: There is no official `@anthropic-ai/claude-code` package on npm (Anthropic does not publish CLI tools this way). This may be a third-party or unofficial package—verify the source before installing globally.
