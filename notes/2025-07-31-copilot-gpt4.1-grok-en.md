---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring Copilot for Custom Models
translated: false
type: note
---

When you select "managed models" in GitHub Copilot and still see GPT-4.1 as the default, or can't use Grok or Kimi models from OpenRouter as expected, there are a few potential reasons and steps to address this. Here's a breakdown of the issue and how to configure Copilot to use Grok or Kimi models via OpenRouter:

### Why GPT-4.1 Is Still Used
1. **Default Model Setting**: GitHub Copilot defaults to GPT-4.1 for Copilot Chat, Edits, and Agent Mode unless explicitly changed. Even when you select "managed models," the default model may persist if you haven't fully configured OpenRouter integration or selected a specific model.[](https://github.blog/changelog/2025-05-08-openai-gpt-4-1-is-now-generally-available-in-github-copilot-as-the-new-default-model/)
2. **Context-Specific Model Usage**: The "fix box" (inline chat or code completion) in Copilot might not support switching to custom models like Grok or Kimi in certain contexts. For example, the Copilot Chat panel or inline suggestions might use the default model (GPT-4.1) unless you explicitly switch to a custom model in the immersive view or Agent Mode.[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
3. **OpenRouter Integration Limitations**: OpenRouter allows access to models like Grok (created by xAI) and Kimi (from Moonshot AI), but Copilot's integration with OpenRouter requires a specific setup, and not all models may be immediately available due to API limitations or configuration issues. For instance, OpenRouter’s API may not announce tool support for all models, which can prevent Agent Mode or certain features from working with Grok or Kimi.[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
4. **Subscription or Configuration Restrictions**: If you're using a free tier or a non-Pro/Business Copilot subscription, you might be limited to default models like GPT-4.1. Additionally, some models (e.g., Grok or Kimi) may require specific configurations or premium access through OpenRouter.[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

### How to Use Grok or Kimi Models in Copilot via OpenRouter
To use Grok or Kimi models from OpenRouter in Copilot, particularly for the "fix box" (inline chat or code completion), follow these steps:

1. **Set Up OpenRouter with Copilot**:
   - **Get an OpenRouter API Key**: Sign up at [openrouter.ai](https://openrouter.ai) and obtain an API key. Ensure you have credits or a plan that supports access to Grok (xAI) and Kimi (Moonshot AI K2) models.[](https://openrouter.ai/models)[](https://openrouter.ai)
   - **Configure OpenRouter in VS Code**:
     - Open Visual Studio Code (VS Code) and ensure the latest GitHub Copilot extension is installed (v1.100.2 or later).[](https://github.com/microsoft/vscode-copilot-release/issues/10193)
     - Go to the Copilot dashboard in the Status Bar, or open the Command Palette (`Ctrl+Shift+P` or `Command+Shift+P` on Mac) and type `GitHub Copilot: Manage Models`.
     - Add your OpenRouter API key and configure the endpoint to include OpenRouter models. You may need to follow OpenRouter’s documentation for integrating with VS Code’s Copilot extension.[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
   - **Verify Model Availability**: After adding the OpenRouter endpoint, check the "Manage Models" section in Copilot. Models like `openrouter/xai/grok` or `openrouter/moonshotai/kimi-k2` should appear in the model picker. If they don’t, ensure your OpenRouter account has access to these models and that there are no restrictions (e.g., free tier limitations).[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

2. **Switch Models for the Fix Box**:
   - **For Inline Chat (Fix Box)**: The "fix box" likely refers to Copilot’s inline chat or code completion feature. To change the model for inline chat:
     - Open the Copilot Chat interface in VS Code (via the icon in the title bar or sidebar).
     - In the chat view, select the `CURRENT-MODEL` dropdown menu (usually in the bottom right) and choose `openrouter/xai/grok` or `openrouter/moonshotai/kimi-k2` if available.[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
     - If the dropdown doesn’t show Grok or Kimi, it might be due to OpenRouter’s API not announcing tool support for these models, which can limit their use in certain Copilot features like Agent Mode or inline fixes.[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
   - **For Code Completion**: To change the model for code completions (not just chat):
     - Open the Command Palette (`Ctrl+Shift+P` or `Command+Shift+P`) and type `GitHub Copilot: Change Completions Model`.
     - Select the desired OpenRouter model (e.g., Grok or Kimi) from the list. Note that not all OpenRouter models may support code completion due to VS Code’s current limitation of supporting only Ollama endpoints for custom models, though OpenRouter can work with a proxy workaround.[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-completion-model)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)

3. **Workaround for OpenRouter Models**:
   - **Proxy Solution**: Since OpenRouter’s API doesn’t always announce tool support (required for Agent Mode or advanced features), you can use a proxy like `litellm` to enable Grok or Kimi in Copilot. Edit the `config.yaml` file to include:
     ```yaml
     model_list:
       - model_name: grok
         litellm_params:
           model: openrouter/xai/grok
       - model_name: kimi-k2
         litellm_params:
           model: openrouter/moonshotai/kimi-k2
     ```
     - Follow the setup instructions from sources like [Bas codes](https://bas.codes) or [DEV Community](https://dev.to) for detailed steps on configuring the proxy.[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
   - **Restart VS Code**: After configuring the proxy, restart VS Code to ensure the new models are available in the model picker.

4. **Check Subscription and Permissions**:
   - **Copilot Subscription**: Ensure you have a Copilot Pro or Business subscription, as free-tier users may not have the option to add custom models.[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
   - **Business Restrictions**: If you’re using a Copilot Business subscription, your organization must enable model switching. Check with your admin or refer to GitHub’s documentation on managing Copilot policies.[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
   - **OpenRouter Credits**: Verify that your OpenRouter account has sufficient credits to access premium models like Grok or Kimi, as these may consume more credits than others.[](https://www.reddit.com/r/GithubCopilot/comments/1la87wr/why_are_gh_copilot_pro_models_so_much_worse_than/)

5. **Troubleshooting the Fix Box**:
   - If the fix box still uses GPT-4.1, it could be because the inline chat feature is locked to the default model in certain contexts (e.g., non-immersive view). Try switching to the immersive view of Copilot Chat (`https://github.com/copilot`) to select Grok or Kimi explicitly.[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
   - If Grok or Kimi don’t appear in the model picker, double-check the OpenRouter integration in `Manage Models`. You may need to refresh the model list or re-add the OpenRouter API key.[](https://github.com/microsoft/vscode-copilot-release/issues/10193)
   - If the issue persists, test the models in Copilot’s Agent Mode or chat interface first to confirm they’re working, then try applying them to inline fixes.

6. **Alternative Tools**:
   - If OpenRouter integration with Copilot remains problematic, consider using Grok directly via [grok.com](https://grok.com) or the Grok iOS/Android apps, which offer free access with usage quotas. Kimi models can also be tested via OpenRouter’s chat interface to ensure they’re accessible.[](https://openrouter.ai)
   - For a more seamless experience, you might explore other IDEs or tools like Cursor, which has been noted to work well with OpenRouter’s Kimi K2 model.[](https://openrouter.ai)

### Additional Notes
- **Model Performance**: Grok is optimized for reasoning and truth-seeking, making it suitable for complex debugging or architectural tasks, while Kimi (K2) may excel in specific coding scenarios. Test both to see which performs better for your use case.[](https://github.blog/ai-and-ml/github-copilot/which-ai-model-should-i-use-with-github-copilot/)
- **Community Feedback**: Some users report issues with OpenRouter models not appearing in Copilot’s model picker, especially with free-tier accounts. This might require a paid OpenRouter plan or Copilot Pro subscription to resolve.[](https://github.com/microsoft/vscode-copilot-release/issues/10193)[](https://www.reddit.com/r/GithubCopilot/comments/1la87wr/why_are_gh_copilot_pro_models_so_much_worse_than/)
- **Ongoing Limitations**: There’s an open discussion about enabling custom API endpoints directly in Copilot (see [microsoft/vscode-copilot-release#7518](https://github.com/microsoft/vscode-copilot-release/issues/7518)). Until this is implemented, the proxy workaround is the most reliable method for using Grok or Kimi.[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)

### Citations
- [Changing the AI model for Copilot Chat - GitHub Docs](https://docs.github.com/en/copilot/managing-copilot/changing-the-ai-model-for-copilot-chat)[](https://docs.github.com/en/copilot/how-tos/use-ai-models/change-the-chat-model)
- [How to Use Third Party Models in GitHub Copilot Agent Mode - Bas codes](https://bas.codes)[](https://bas.codes/posts/how-to-use-third-party-models-in-copilot-agent-mode/)
- [Openrouter - openrouter.ai](https://openrouter.ai)[](https://openrouter.ai/models)
- [Agent Mode With Third-Party Models in Copilot - DEV Community](https://dev.to)[](https://dev.to/bascodes/agent-mode-with-third-party-models-in-copilot-317k)
- [Openrouter - openrouter.ai](https://openrouter.ai)[](https://openrouter.ai)
- [r/LocalLLaMA on Reddit: Github Copilot now supports Ollama and OpenRouter Models](https://www.reddit.com)[](https://www.reddit.com/r/LocalLLaMA/comments/1jslnxb/github_copilot_now_supports_ollama_and_openrouter/)
- [Which AI model should I use with GitHub Copilot? - The GitHub Blog](https://github.blog)[](https://github.blog/ai-and-ml/github-copilot/which-ai-model-should-i-use-with-github-copilot/)
- [OpenAI GPT-4.1 is now generally available in GitHub Copilot - GitHub Changelog](https://github.blog)[](https://github.blog/changelog/2025-05-08-openai-gpt-4-1-is-now-generally-available-in-github-copilot-as-the-new-default-model/)
- [OpenRouter (free) Models Missing from Manage Models - GitHub Issues](https://github.com/microsoft/vscode-copilot-release/issues/10193)[](https://github.com/microsoft/vscode-copilot-release/issues/10193)

If you encounter specific errors or need further assistance with the setup, please provide more details (e.g., error messages, VS Code version, or subscription type), and I can tailor the solution further!
