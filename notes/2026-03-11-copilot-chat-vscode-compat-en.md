---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot Chat Compatibility for VS Code
translated: false
type: note
---

Now I have enough data. Let me consolidate the findings.

---

Question: Which `GitHub.copilot-chat` VSIX extension version is compatible with VS Code 1.106.3?

Answer:

## GitHub Copilot Chat Compatible with VS Code 1.106.3

### Important Compatibility Warning First

Copilot Chat releases **in lockstep with VS Code** due to its deep UI integration. This means every new version of Copilot Chat is only compatible with the latest and newest release of VS Code — if you are using an older version of VS Code, you will not be able to use the latest Copilot Chat.

Because VS Code 1.106.3 was released November 25, 2025, you need a version of `github.copilot-chat` that was designed to work with the `1.106.x` engine.

### Versions Compatible with VS Code 1.106.x

Based on VsixHub's version history, these are the `github.copilot-chat` releases that declared **VS Code 1.106.0** (or `1.106.0-20251103`) as their engine requirement:

| Version | Updated | Requires VS Code |
|---|---|---|
| **0.33.2025101606** | October 16, 2025 | 1.106.0 and up |
| **0.33.2025103102** | October 31, 2025 | 1.106.0-20251103 and up |
| **0.33.2025110601** | November 6, 2025 | 1.106.0-20251103 and up |
| **0.33.2025110703** | November 8, 2025 | 1.106.0-20251103 and up |
| **0.33.2025111103** | November 12, 2025 | 1.106.0-20251103 and up |
| **0.34.2025111403** | November 15, 2025 | 1.106.0-20251103 and up |

The last version released before VS Code 1.106.3's release date (November 25, 2025) was **`0.34.2025111403`**, updated November 15, 2025.

### Recommended Version

**`0.34.2025111403`** is the latest `github.copilot-chat` VSIX that is compatible with VS Code 1.106.3. You can download it directly:

```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot-chat/0.34.2025111403/vspackage
```

### ⚠️ Note on v0.33 vs v0.34

Some users reported that the `0.34` release appeared flagged as a pre-release version of Copilot Chat in some environments, causing issues. If you experience this, the `0.33.2025111103` release (November 12, 2025) is the safest stable fallback for VS Code 1.106.x.

Fallback download:
```
https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GitHub/vsextensions/copilot-chat/0.33.2025111103/vspackage
```

References:

- [GitHub Copilot Chat 0.34.2025111403 – VsixHub](https://www.vsixhub.com/vsix/179478/)
- [GitHub Copilot Chat 0.33.2025111103 – VsixHub](https://www.vsixhub.com/vsix/178702/)
- [GitHub Copilot Chat 0.33.2025101606 – VsixHub](https://www.vsixhub.com/vsix/176559/)
- [vscode-copilot-chat GitHub repo – compatibility note](https://github.com/microsoft/vscode-copilot-chat)
- [VSCodium Copilot guide – pre-release version issue discussion](https://github.com/VSCodium/vscodium/discussions/1487)
