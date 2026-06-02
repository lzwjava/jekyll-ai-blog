---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot Chat 对 VS Code 的兼容性
translated: true
type: note
---

现在我有足够的数据。让我整合这些发现。

---

问题：哪个 `GitHub.copilot-chat` VSIX 扩展版本与 VS Code 1.106.3 兼容？

答案：

## 与 VS Code 1.106.3 兼容的 GitHub Copilot Chat

### 首先重要的兼容性警告

Copilot Chat 发布**与 VS Code 严格同步**，因为其深度 UI 集成。这意味着每个新版本的 Copilot Chat 仅与最新的 VS Code 版本兼容——如果您使用的是较旧的 VS Code 版本，则无法使用最新的 Copilot Chat。

由于 VS Code 1.106.3 于 2025 年 11 月 25 日发布，您需要一个专为 `1.106.x` 引擎设计的 `github.copilot-chat` 版本。

### 与 VS Code 1.106.x 兼容的版本

根据 VsixHub 的版本历史，这些 `github.copilot-chat` 发布版本声明了 **VS Code 1.106.0**（或 `1.106.0-20251103`）作为其引擎要求：

| 版本 | 更新日期 | 所需 VS Code |
|---|---|---|
| **0.33.2025101606** | 2025 年 10 月 16 日 | 1.106.0 及更高版本 |
| **0.33.2025103102** | 2025 年 10 月 31 日 | 1.106.0-20251103 及更高版本 |
| **0.33.2025110601** | 2025 年 11 月 6 日 | 1.106.0-20251103 及更高版本 |
| **0.33.2025110703** | 2025 年 11 月 8 日 | 1.106.0-20251103 及更高版本 |
| **0.33.2025111103** | 2025 年 11 月 12 日 | 1.106.0-20251103 及更高版本 |
| **0.34.2025111403** | 2025 年 11 月 15 日 | 1.106.0-20251103 及更高版本 |

在 VS Code 1.106.3 发布日期（2025 年 11 月 25 日）之前发布的最后一个版本是 **`0.34.2025111403`**，更新于 2025 年 11 月 15 日。

### 推荐版本

**`0.34.2025111403`** 是与 VS Code 1.106.3 兼容的最新 `github.copilot-chat` VSIX。您可以直接下载：

```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot-chat/0.34.2025111403/vspackage
```

### ⚠️ v0.33 与 v0.34 的注意事项

一些用户报告称，`0.34` 版本在某些环境中被标记为 Copilot Chat 的预发布版本，导致问题。如果您遇到此问题，则 `0.33.2025111103` 版本（2025 年 11 月 12 日）是 VS Code 1.106.x 的最安全稳定备用版本。

备用下载：

```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot-chat/0.33.2025111103/vspackage
```

参考资料：

- [GitHub Copilot Chat 0.34.2025111403 – VsixHub](https://www.vsixhub.com/vsix/179478/)
- [GitHub Copilot Chat 0.33.2025111103 – VsixHub](https://www.vsixhub.com/vsix/178702/)
- [GitHub Copilot Chat 0.33.2025101606 – VsixHub](https://www.vsixhub.com/vsix/176559/)
- [vscode-copilot-chat GitHub repo – compatibility note](https://github.com/microsoft/vscode-copilot-chat)
- [VSCodium Copilot guide – pre-release version issue discussion](https://github.com/VSCodium/vscodium/discussions/1487)
