---
audio: false
generated: true
lang: en
layout: post
title: Removing Custom Models in GitHub Copilot
translated: false
type: note
---

To remove a model in the GitHub Copilot extension for Visual Studio Code (VS Code), note that built-in models (like the default GitHub Copilot model) cannot be removed, as they are part of the extension. However, if you're referring to a custom model you've added via a third-party provider (e.g., Anthropic, OpenAI, Google Gemini, or others) using your own API key, you can effectively remove it by deleting the associated API key and provider details. This feature is in preview and may not be available for Copilot Business or Enterprise users yet.

Here are the steps based on the official documentation:

1. Open the Chat view in VS Code (if not already open, use the Command Palette with `Ctrl+Shift+P` or `Cmd+Shift+P` on macOS, then search for "Copilot: Open Chat").
2. In the Chat view, click the model picker dropdown (next to the input field) and select **Manage Models**. Alternatively, open the Command Palette and run the **GitHub Copilot: Manage Models** command.
3. In the Manage Models interface, hover over the provider for the model you want to remove and click the gear icon to edit its details.
4. Delete the API key (and any endpoint URL if applicable) from the fields, then save the changes. This should remove the model's availability from the picker.

If you encounter issues (e.g., the API key field doesn't update or clear properly, which has been reported as a bug in some cases), try this workaround first:
- Select a different model from the model picker in the Chat view to deselect the one you're trying to remove.
- Return to Manage Models, edit the provider, and then delete the API key.

Prerequisites and notes:
- This only applies to chat features; it doesn't affect code completions or other tools.
- Ensure your Copilot subscription allows access to multiple models (e.g., Individual, Pro, or preview features enabled for organizations).
- If the model persists or you face errors, restart VS Code or check for extension updates.

If this doesn't match what you meant by "remove a model" (e.g., if you're trying to disable the entire extension or hide Copilot features), clarify for more tailored steps.
