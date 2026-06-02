---
audio: false
generated: true
lang: en
layout: post
title: Visual Studio Code (VSCode) Copilot plugin
translated: false
type: note
---

No, the Visual Studio Code (VSCode) Copilot plugin cannot use a custom API key, such as your Gemini key. GitHub Copilot, developed by GitHub (owned by Microsoft), is an AI-powered code completion tool tightly integrated with GitHub’s infrastructure and specific AI models, originally based on OpenAI’s Codex. It relies on authentication through a GitHub account and a Copilot subscription, and it does not offer a built-in option to configure it with custom API keys from other providers, like Google’s Gemini.

However, since you have a Gemini key, there are alternative ways to leverage it within VSCode:

- **Gemini Code Assist**: Google provides an AI-powered coding assistant called Gemini Code Assist, which has an official extension for VSCode. This extension is designed to work with Google’s Gemini models and likely allows you to input your Gemini API key for authentication. You can install this extension from the VSCode Marketplace and configure it with your key to get code completion powered by Gemini.

- **Third-Party Plugins**: There may also be other third-party VSCode extensions available in the Marketplace that support multiple AI providers and allow you to use custom API keys, including one for Gemini. These plugins would let you connect to the Gemini API for code suggestions, though they might require additional setup.

### Why Copilot Doesn’t Support Custom Keys
GitHub Copilot is a proprietary tool optimized for its own ecosystem. While recent developments have seen GitHub partnering with Google to integrate Gemini models into Copilot, this integration is managed by GitHub and does not allow users to directly input their own Gemini API keys. Instead, access to any supported models (including Gemini, if available) is provided through the Copilot service itself, under GitHub’s control.

### Practical Recommendation
If your goal is to use your Gemini key in VSCode, installing the **Gemini Code Assist extension** is the most straightforward and officially supported option. Here’s how you can proceed:

1. Open VSCode.
2. Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
3. Search for “Gemini Code Assist” (or check Google’s official documentation for the exact name).
4. Install the extension and follow its setup instructions to input your Gemini API key.

This approach ensures you’re using the tool as intended, avoiding potential issues like violating terms of service or dealing with unsupported modifications to Copilot.

In summary, while the VSCode Copilot plugin itself cannot use your Gemini key, you can still achieve your goal of using Gemini in VSCode by opting for the Gemini Code Assist extension or a compatible third-party plugin.
