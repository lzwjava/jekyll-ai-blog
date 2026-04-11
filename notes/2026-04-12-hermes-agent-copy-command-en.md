---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Copy Command Explained
translated: false
type: note
---

**Question:** What is the copy command in Hermes Agent?

**Answer:**

Hermes Agent (by Nous Research) does not have a traditional "copy" command in the conventional sense of copying files. However, there are several clipboard and file-related operations available:

## Clipboard Operations

### Pasting Images from Clipboard
Hermes supports pasting images directly from your clipboard into the CLI for vision analysis using Ctrl+V or the /paste command. The methods include:

1. **`/paste` command** - Type /paste and press Enter to check your clipboard for an image and attach it. This is the most reliable method that works in every environment.

2. **Ctrl+V** - When your clipboard contains both text and an image, Ctrl+V automatically checks for the image too (requires bracketed paste support in your terminal).

3. **Alt+V** - Press Alt+V to check the clipboard for an image, though this does not work in VSCode's integrated terminal.

### Image Storage
Images pasted from the clipboard are automatically saved to ~/.hermes/images/ as PNG files with timestamped filenames.

## File System Copy Operations

While not explicitly documented as a dedicated "copy" command in Hermes Agent's CLI, the agent has access to terminal tools and can execute standard Unix commands like `cp` for file copying through its terminal tool.

## Configuration Export
For copying configuration data, such as Browser Use API keys, Hermes uses commands like `hermes config set BROWSER_USE_API_KEY $(browser-use config get api_key)` to copy keys between systems.

**References:**

- [https://hermes-agent.nousresearch.com/docs/guides/tips/](https://hermes-agent.nousresearch.com/docs/guides/tips/)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/vision/](https://hermes-agent.nousresearch.com/docs/user-guide/features/vision/)
- [https://docs.browser-use.com/cloud/tutorials/integrations/hermes-agent](https://docs.browser-use.com/cloud/tutorials/integrations/hermes-agent)