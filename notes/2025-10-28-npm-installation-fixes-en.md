---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: npm Installation Error Fixes
translated: false
type: note
---

### Understanding the Error

This is an npm installation failure during a global update (or install) of the `@anthropic-ai/claude-code` package. The key issue is in the "reify" phase, where npm tries to "retire" (back up) the existing package directory before installing the new version. Specifically:

- npm is attempting to rename `/usr/lib/node_modules/@anthropic-ai/claude-code` to a temporary backup like `/usr/lib/node_modules/@anthropic-ai/.claude-code-ZjqcDZyQ`.
- This fails with `ENOTEMPTY: directory not empty` (errno -39), which typically occurs when:
  - The source directory contains files/subdirectories that are locked, in use, or have permission issues.
  - There are broken symlinks, open file handles (e.g., from a running `claude` process), or filesystem quirks on Linux.
  - Rarely, npm's internal move-file logic hits a race condition.

Your setup:

- Node: v22.18.0
- npm: v11.6.1
- OS: Linux 6.14.0-29-generic (likely Ubuntu/Debian)
- Running as root (based on log path `/root/.npm/_logs/`), so permissions aren't the root cause.
- Working directory: `/home/lzwjava/projects/blog-source` (but this is a global install, so irrelevant).

The package seems to be Anthropic's Claude Code tool (CLI for AI coding assistance), and line 73 shows a dependency mismatch warning for `@img/sharp-libvips-linux-x64`, but that's unrelated to the crash.

### Quick Fixes (Try in Order)

1. **Stop Any Running Processes**:
   - Kill any `claude` CLI or related processes: `pkill claude` (or `ps aux | grep claude` to find PIDs, then `kill <PID>`).
   - Close terminals/IDEs using the package.

2. **Manually Clean the Directory**:
   - Remove the existing package and binary:

     ```
     sudo rm -rf /usr/lib/node_modules/@anthropic-ai/claude-code
     sudo rm -f /usr/bin/claude
     ```

   - This bypasses npm's backup step. Then retry the install:

     ```
     sudo npm install -g @anthropic-ai/claude-code
     ```

3. **Clear npm Cache and Retry**:
   - Run:

     ```
     sudo npm cache clean --force
     sudo npm install -g @anthropic-ai/claude-code
     ```

   - If it persists, add `--no-optional` to skip optional deps like the Sharp image lib.

4. **Alternative: Use npx or Avoid Global**:
   - If you don't need it global, install locally in your project: `npm install @anthropic-ai/claude-code` (then run via `npx claude`).
   - Or use Yarn: `sudo yarn global add @anthropic-ai/claude-code` (Yarn handles moves differently sometimes).

5. **If Still Stuck**:
   - Check for filesystem issues: `ls -la /usr/lib/node_modules/@anthropic-ai/` (look for weird symlinks or locks).
   - Downgrade npm temporarily: `sudo npm install -g npm@10` (v11 has occasional reify bugs; revert after).
   - Full log: Check `/root/.npm/_logs/2025-10-27T16_10_10_534Z-debug-0.log` for more clues.

This should resolve it—npm globals on Linux can be finicky with renames. If you share the exact command you ran or more log context, I can refine this.
