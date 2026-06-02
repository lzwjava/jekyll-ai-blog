---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 自托管本地Copilot替代方案
translated: true
type: note
---

你在寻找开源工具来实现本地的“类Copilot”体验——能够自己运行（使用自己的token或模型），或许还能集成到VS Code或其他IDE中。不需要表格，只需清晰简洁的说明。以下是知名度较高的选择：

---

### **Tabby**

一个用Rust编写的自托管AI编程助手。它开源、无需外部服务，并提供OpenAPI风格的接口——使得与本地IDE和基础设施的集成变得简单直接。它甚至支持消费级GPU和编辑器集成，包括Vim/Neovim。（[GitHub][1], [Software Recommendations Stack Exchange][2]）

---

### **FauxPilot**

一个开源项目，旨在作为GitHub Copilot的本地托管替代方案。它利用Salesforce的CodeGen模型，通过NVIDIA的Triton Inference Server（和FasterTransformer）运行。可通过Docker部署，兼容类Copilot客户端，在拥有性能足够的GPU时表现最佳。（[GitHub][3]）

---

### **Privy**

另一个MIT许可的、在本地运行的开源工具。它提供类似GitHub Copilot的实时代码补全和聊天功能。它可以与Ollama、llama.cpp或llamafile等LLM运行时集成，并根据你的硬件支持流行的编程模型（如CodeLlama变体）。（[GitHub][4]）

---

### **GPT4All, Continue, LocalPilot** *（及类似工具）*

与Tabby和FauxPilot一同被提及的几个自托管工具；它们提供注重本地隐私的编程辅助。虽然通常不那么完善，但在硬件限制或特定工作流程需要时，它们是可行的选择。（[Virtualization Howto][5]）

---

### **Ollama (配合 Docker)**

本身并非完整的Copilot替代品，而是一个强大的用于本地运行LLM的开源工具。你可以通过Docker使用Ollama托管像Phi-2这样的模型，然后通过LLM扩展（例如Hugging Face的 `llm-vscode`）连接到VS Code。这使你基本上可以与本地模型聊天或获得代码辅助。（[Tommaso Colella][6], [Reddit][7]）

---

### **社区热议**

来自Reddit的讨论：

* “使用Ollama AI在Docker服务器上免费自托管你自己的‘Copilot’”——强调了Ollama的有效性及其与VS Code的集成。（[Reddit][7]）
* “Tabby（现在）是最受欢迎的‘开源且本地’工具”——指出其日益增长的应用。（[Reddit][8]）

---

### **总结建议**

* **如果你想要一个成熟完善的开源Copilot替代品：** 从 **Tabby** 开始。
* **如果你想要更接近Copilot基础设施的东西（并且拥有不错的GPU）：** 试试 **FauxPilot**。
* **如果你想要代码补全+聊天功能，并且在模型/运行时选择上更灵活：** 尝试 **Privy**。
* **想要完全控制端点和模型？** 将 **Ollama** 与你自己的LLM配对，然后使用标准的LLM接口进行连接。

---

### **你的后续步骤**

1. **评估硬件：** FauxPilot和Privy可能需要不错的GPU；Tabby更轻量。
2. **选择一个运行时/框架：**
    * **Tabby**：具有编辑器支持的全面选择。
    * **FauxPilot**：类似Copilot，使用Docker和Triton。
    * **Privy**：灵活、模型无关的设置。
    * **Ollama + LLM**：纯粹的DIY——如果你习惯自己构建端点，这是个好选择。
3. **连接到你的IDE：** VS Code（或其他IDE）支持通过本地端点使用这些工具，就像Copilot一样。

如果你需要针对任何特定工具的入门帮助或设置步骤指导，请告诉我！

[1]: https://github.com/TabbyML/tabby?utm_source=chatgpt.com "TabbyML/tabby: 自托管AI编程助手"
[2]: https://softwarerecs.stackexchange.com/questions/90507/foss-alternative-to-github-copilot?utm_source=chatgpt.com "FOSS替代GitHub Copilot的方案？"
[3]: https://github.com/fauxpilot/fauxpilot?utm_source=chatgpt.com "FauxPilot - 一个开源的...替代方案"
[4]: https://github.com/srikanth235/privy?utm_source=chatgpt.com "srikanth235/privy: 一个开源的...替代方案"
[5]: https://www.virtualizationhowto.com/2025/05/best-self-hosted-github-copilot-ai-coding-alternatives/?utm_source=chatgpt.com "最佳自托管GitHub Copilot AI编程替代方案"
[6]: https://gioleppe.github.io/posts/diy-copilot-phi/?utm_source=chatgpt.com "使用Phi-2和Ollama DIY自托管Copilot"
[7]: https://www.reddit.com/r/vscode/comments/1by7njo/self_host_your_own_copilot_for_free_with_ollama/?utm_source=chatgpt.com "使用Ollama AI在...上免费自托管你自己的\"Copilot\""
[8]: https://www.reddit.com/r/LocalLLaMA/comments/12m8fnm/best_local_equivalent_of_github_copilot/?utm_source=chatgpt.com "最佳的本地GitHub Copilot等效方案？: r/LocalLLaMA"
