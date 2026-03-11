---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot 基础扩展最终版本
translated: true
type: note
---

搜索结果显示有足够的信息来回答这个问题。现在让我看看关键数据点。`GitHub.copilot`（基础版，非聊天版）扩展使用非常低的 VS Code 引擎最低要求（如 1.103.0），因此在 VS Code 1.106.3 时间段（2025 年 11 月 25 日）发布的任何版本都会兼容。VsixHub 搜索显示 `GitHub Copilot v1.388.0` 于 2025 年 10 月 25 日更新（要求 VS Code 1.103.0+）。我需要找到在 VS Code 1.106.3 时间左右发布的版本。现在我有了全面的了解。让我把这一切整理成一个清晰的答案。

**收集的关键事实：**

1. VSCode 1.106.3 于 2025 年 11 月 25 日发布。

2. 在 VS Code 1.106 左右的时间，Microsoft 宣布 `GitHub.copilot` 扩展（用于内联/幽灵文本建议）将被弃用，其功能移入 Copilot Chat 扩展。帖子中说道："The GitHub Copilot extension will be deprecated by early 2026, which means it will be removed from the VS Code Marketplace."

3. VsixHub 跟踪的基础 `GitHub.copilot` VSIX 的最后一个已知版本是 **v1.388.0**，更新于 2025 年 10 月 25 日，要求 VS Code 1.103.0 及以上。基础 `GitHub.copilot` 扩展在 2025 年 10 月 25 日后没有发布更新的版本——这使得 v1.388.0 成为 VS Code 1.106.3 发布时可用的最后一个版本。

4. VsixHub 上的版本历史确认 v1.388.0 是最新的，前一个条目是 v1.387.0 更新于 2025 年 10 月 22 日。2025 年 11 月没有为基础 `GitHub.copilot` 扩展发布版本。

---

问题：当 VS Code 1.106.3 发布时，最新兼容的 `GitHub.copilot`（非 `github.copilot-chat`）VSIX 扩展版本是什么？

答案：

## VS Code 1.106.3 和 GitHub Copilot（基础）扩展

VS Code 1.106.3 于 **2025 年 11 月 25 日** 发布，作为 2025 年 10 月（v1.106）周期的第三个恢复/补丁发布。

### 重要背景：GitHub Copilot 扩展弃用

就在 VS Code 1.106 发布窗口前后，Microsoft 宣布 `GitHub.copilot`（基础）扩展将被 **弃用，并将于 2026 年初从 VS Code Marketplace 中移除**。内联建议功能已被开源并合并到 `GitHub.copilot-chat` 扩展中，这意味着所有 Copilot 功能将被统一到一个扩展中。

### 最新兼容的 `github.copilot.vsix` 版本

基础 `GitHub.copilot` 扩展的最后一个发布版本是 **v1.388.0**，更新于 2025 年 10 月 25 日。它要求 VS Code **1.103.0 及以上**，这意味着它与 VS Code 1.106.3 完全兼容。

版本历史确认，在 v1.388.0（2025 年 10 月 25 日）之后，没有发布基础 `GitHub.copilot` 扩展的新版本。前一个发布是 2025 年 10 月 22 日的 v1.387.0。这意味着当 VS Code 1.106.3 于 2025 年 11 月 25 日发布时，**v1.388.0 已经是基础扩展的最后一个版本**。

### 总结

| 项目 | 详情 |
|---|---|
| 扩展 | `GitHub.copilot`（基础、内联建议） |
| VSCode 1.106.3 时最新版本 | **v1.388.0** |
| 发布 | 2025 年 10 月 25 日 |
| VS Code 引擎要求 | 1.103.0 及以上 |
| 与 1.106.3 兼容？ | ✅ 是 |
| 状态 | 已弃用（最后一个发布） |

您可以直接通过 Marketplace API 下载：
```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot/1.388.0/vspackage
```

参考：

- [VSCode 1.106.3 发布 (GitClear)](https://www.gitclear.com/open_repos/Microsoft/vscode/release/1.106.3)
- [GitHub Copilot v1.388.0 VSIX – VsixHub](https://www.vsixhub.com/vsix/63883/)
- [开源 AI 编辑器：第二个里程碑（内联建议开源）](https://code.visualstudio.com/blogs/2025/11/04/openSourceAIEditorSecondMilestone)