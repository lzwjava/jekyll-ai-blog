---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot in VS Code Partially Open Source
translated: false
type: note
---

Question: Is Copilot in VS Code open source?

Answer: **Partially.** The frontend and client-side integration of GitHub Copilot in VS Code are open source, but the actual AI models and backend services remain **closed source**.

Microsoft and GitHub transitioned the extension's codebase to an open-source model under the MIT license, migrating the code directly into the main open-source VS Code core repository.

Here is exactly what is open source versus what remains closed:

### What is Open Source

* **The UX and Client Extension:** The client-side code responsible for the user interface, chat windows, inline edit interfaces, and prompt management in VS Code is completely open source.
* **Prompt Engineering Logic:** You can inspect the repository to see how your context is gathered, how prompts are structured before being sent to the AI, and what telemetry data is being collected.

### What is Closed Source

* **The AI Models:** The actual underlying Large Language Models (LLMs) used by Copilot—such as those from OpenAI, Anthropic, and Google—are proprietary and closed source.
* **The Backend Services:** The cloud infrastructure and proprietary backend systems that process the AI requests and return data to your editor remain completely closed source.
* **Subscription Model:** Even though the client software is open source, using the official service still requires a GitHub Copilot account (though a limited "Copilot Free" tier is available).

References:

* [Visual Studio Code FAQ](https://code.visualstudio.com/docs/supporting/FAQ)
* [Open Source AI Editor: First Milestone - Visual Studio Code](https://code.visualstudio.com/blogs/2025/06/30/openSourceAIEditorFirstMilestone)
