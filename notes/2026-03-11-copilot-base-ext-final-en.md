---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot Base Extension Final Version
translated: false
type: note
---

The search results show enough information to answer this question. Let me now look at the key data points. The `GitHub.copilot` (base, not chat) extension uses a very low VS Code engine minimum (like 1.103.0), so any version released around VS Code 1.106.3's timeframe (November 25, 2025) would work. The VsixHub search showed `GitHub Copilot v1.388.0` was updated October 25, 2025 (requiring VS Code 1.103.0+). I need to find what version was released around the time of VS Code 1.106.3.Now I have a comprehensive picture. Let me put this all together into a clear answer.

**Key facts gathered:**

1. VSCode 1.106.3 was released on November 25, 2025.

2. Around the time of VS Code 1.106, Microsoft announced that the `GitHub.copilot` extension (for inline/ghost text suggestions) was being deprecated, with its functionality moved into the Copilot Chat extension. The post stated: "The GitHub Copilot extension will be deprecated by early 2026, which means it will be removed from the VS Code Marketplace."

3. The last known version of the base `GitHub.copilot` VSIX tracked by VsixHub was **v1.388.0**, updated October 25, 2025, requiring VS Code 1.103.0 and up. No newer version of the base `GitHub.copilot` extension was released after October 25, 2025 — making v1.388.0 the last version available when VS Code 1.106.3 was released.

4. The version history on VsixHub confirms v1.388.0 is the latest, and the previous entry was v1.387.0 updated October 22, 2025. No versions were released in November 2025 for the base `GitHub.copilot` extension.

---

Question: When VS Code 1.106.3 was released, what was the latest compatible `GitHub.copilot` (not `github.copilot-chat`) VSIX extension version?

Answer:

## VS Code 1.106.3 and GitHub Copilot (Base) Extension

VS Code 1.106.3 was released on **November 25, 2025** as the third recovery/patch release of the October 2025 (v1.106) cycle.

### Important Context: GitHub Copilot Extension Deprecation

Right around the VS Code 1.106 release window, Microsoft announced that the `GitHub.copilot` (base) extension was being **deprecated and would be removed from the VS Code Marketplace by early 2026**. The inline suggestion functionality was open-sourced and merged into the `GitHub.copilot-chat` extension, meaning all Copilot functionality was being unified into a single extension.

### Latest Compatible `github.copilot.vsix` Version

The last released version of the base `GitHub.copilot` extension is **v1.388.0**, which was updated on October 25, 2025. It requires VS Code **1.103.0 and up**, meaning it is fully compatible with VS Code 1.106.3.

The version history confirms that no new releases of the base `GitHub.copilot` extension were published after v1.388.0 (October 25, 2025). The preceding release was v1.387.0 on October 22, 2025. This means when VS Code 1.106.3 shipped on November 25, 2025, **v1.388.0 was already the last-ever version** of the base extension.

### Summary

| Item | Detail |
| --- | --- |
| Extension | `GitHub.copilot` (base, inline suggestions) |
| Latest version at time of VSCode 1.106.3 | **v1.388.0** |
| Released | October 25, 2025 |
| VS Code engine requirement | 1.103.0 and up |
| Compatible with 1.106.3? | ✅ Yes |
| Status | Deprecated (last ever release) |

You can download it directly via the Marketplace API:

```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot/1.388.0/vspackage
```

References:

- [VSCode 1.106.3 Release (GitClear)](https://www.gitclear.com/open_repos/Microsoft/vscode/release/1.106.3)
- [GitHub Copilot v1.388.0 VSIX – VsixHub](https://www.vsixhub.com/vsix/63883/)
- [Open Source AI Editor: Second Milestone (Inline suggestions open-sourced)](https://code.visualstudio.com/blogs/2025/11/04/openSourceAIEditorSecondMilestone)
