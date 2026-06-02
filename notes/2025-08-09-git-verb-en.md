---
audio: false
generated: true
image: false
lang: en
layout: post
title: Log Git Verbosely
translated: false
type: note
---

To enable verbose logging in Git, you can use specific flags or environment variables depending on the command and the level of detail you need. Here are the main approaches:

1. **Use the `--verbose` or `-v` flag**:
   Many Git commands support the `--verbose` (or `-v`) flag to provide more detailed output. For example:

   ```bash
   git commit --verbose
   ```

   This shows the diff of changes being committed in addition to the usual output.

2. **Enable verbose mode for specific commands**:
   - For `git push`:

     ```bash
     git push --verbose
     ```

     This provides details about the push process, including refs being pushed and server communication.
   - For `git fetch`:

     ```bash
     git fetch --verbose
     ```

     This shows detailed information about what’s being fetched.
   - For `git clone`:

     ```bash
     git clone --verbose <repository>
     ```

     This displays progress and additional details during cloning.

3. **Set the `GIT_TRACE` environment variable**:
   For deeper debugging, you can enable Git’s trace output to see low-level details of Git’s operations:

   ```bash
   GIT_TRACE=1 git <command>
   ```

   This outputs detailed logs about Git’s internal processes, such as command execution and system calls.

4. **Enable specific trace levels**:
   You can use more granular environment variables for specific aspects of Git:
   - `GIT_TRACE_CURL`: Enables verbose logging for HTTP operations (useful for remote interactions):

     ```bash
     GIT_TRACE_CURL=1 git <command>
     ```

   - `GIT_TRACE_PACKET`: Shows packet-level details for Git’s protocol:

     ```bash
     GIT_TRACE_PACKET=1 git <command>
     ```

   - `GIT_TRACE_PERFORMANCE`: Logs performance data:

     ```bash
     GIT_TRACE_PERFORMANCE=1 git <command>
     ```

5. **Increase verbosity for diff-related commands**:
   For commands like `git diff` or `git log`, you can use options to get more details:
   - `git diff --stat` shows a summary of changes.
   - `git log --verbose` or `git log -p` includes the full diff for each commit.

6. **Global configuration for verbose output**:
   You can configure Git to always be verbose for certain commands by setting aliases or using configuration options. For example:

   ```bash
   git config --global alias.logv "log --verbose"
   ```

   Then, running `git logv` will always include verbose output.

**Example**:
To see detailed output for a push operation with full tracing:

```bash
GIT_TRACE=1 git push --verbose
```

**Notes**:

- Verbose output can be overwhelming, especially with `GIT_TRACE`, so use it when debugging specific issues.
- Check the man pages for specific commands (e.g., `man git-push`) to see if they support `--verbose` or other debug flags.
- On Windows, use the same environment variable syntax in Command Prompt (`set GIT_TRACE=1`) or PowerShell (`$env:GIT_TRACE=1`).

If you need verbose logging for a specific Git command or scenario, let me know, and I can provide a tailored example!
