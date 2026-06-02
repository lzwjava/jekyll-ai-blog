---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Disable Claude Code Edit Confirmation Popup
translated: false
type: note
---

To disable the edit confirmation popup in Claude Code (so it just applies edits directly to files like `sync_githook.py` without asking), you need to configure the permissions in your `settings.json` file. This is the "Claude Code JSON" you're referring to—it's Claude Code's main settings file for user-level configs.

### Steps to Set It Up

1. **Locate or Create the File**:
   - The file is at `~/.claude/settings.json` (on macOS/Linux) or `%USERPROFILE%\.claude\settings.json` (on Windows). The `.claude` folder is hidden, so use your terminal/file explorer to navigate there.
   - If the file or folder doesn't exist, create them. You can do this by running Claude Code's `/config` command in its interactive REPL (it'll guide you to open the settings interface).

2. **Edit the JSON**:
   - Open `settings.json` in any text editor (e.g., VS Code).
   - Add or update the `permissions` section to auto-approve edits. Here's a simple config to disable prompts for all edit actions:

     ```json:disable-run
     {
       "permissions": {
         "defaultMode": "acceptEdits",
         "allow": [
           "Edit(*)",
           "Write(*)",
           "MultiEdit(*)"
         ],
         "ask": []
       }
     }
     ```

     - **What this does**:
       - `"defaultMode": "acceptEdits"`: Sets the global default to accept edits without prompting.
       - `"allow"`: Pre-approves specific tools like `Edit` (for single-file edits), `Write` (for writing content), and `MultiEdit` (for batch changes) for any files (`*` wildcard).
       - `"ask": []`: Ensures no actions trigger a prompt unless explicitly denied elsewhere.
     - Save the file. Changes apply immediately in your next Claude Code session.

3. **Test It**:
   - Restart Claude Code or reload the session.
   - Ask it to edit a file (e.g., "Edit sync_githook.py to add a comment"). It should apply the change without the popup.
   - If you want project-specific settings (e.g., only for this repo), create `.claude/settings.json` in your project's root folder instead.

4. **Optional Tweaks**:
   - For more granular control (e.g., only allow edits in certain directories): Change `"Edit(*)"` to `"Edit(./src/**)"`.
   - If prompts persist, run `/allowed-tools` in the REPL to check current rules, or use `/config` to tweak via the UI.
   - For security, avoid overly broad `allow` rules—start simple and expand.

This should make your workflow faster without interruptions. If you're in an enterprise setup, check with your admin, as managed policies might override user settings.

[Claude Code Settings Docs](https://docs.claude.com/en/docs/claude-code/settings)
[Disable Claude Code Permission Prompts Guide](https://www.arsturn.com/blog/how-to-disable-claude-code-permission-prompts)
```
