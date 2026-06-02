---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 联想 BIOS 与 USB 启动指南
translated: true
type: note
---

Question: In a Lenovo 2011 laptop, what is the typical command/key to enter BIOS, and how to choose a bootable USB disk with Linux Mint?

Answer:

对于 2011 年左右的 Lenovo 笔记本，按键取决于它是 **ThinkPad** 系列还是 **IdeaPad** / 消费级系列模型。以下是最常见的选项：

### 1. 进入 BIOS Setup

- **ThinkPad 模型最常用**（非常典型于 2010–2012 年的商务笔记本，如 T410, T420, X220, L420 等）：
  完全关闭笔记本电源。
  按下电源键 → 立即并重复点击 **F1**（或有时是 Fn + F1）。
  → 这几乎总能进入 2011 时代 ThinkPad 的 BIOS Setup Utility。

- **IdeaPad / 消费级模型最常用**（G560, Z570, Y560 等）：
  断电 → 按下电源键 → 立即并重复点击 **F2**（或 Fn + F2）。
  一些较旧的 IdeaPad 模型可能会在屏幕上短暂显示 "Press F2 to Setup"。

- **备选 / 替代方法**（如果上述方法失败，请尝试）：
  - 开机过程中重复点击 **Enter**（某些 ThinkPad 会显示 "Startup Interrupt Menu" → 然后按 F1 进入 BIOS）。
  - 开机后立即重复点击 **Esc**（少数情况下有效）。

提示：在启动过程中仔细观察屏幕 —— 许多 Lenovo 笔记本会短暂显示 "Press [key] to enter Setup"（通常是 F1 或 F2）。

### 2. 从 USB 启动 (Linux Mint)

主要有两种方法：

**方法 A — 使用一次性 Boot Menu（推荐且最简单）**

- 插入你的 Linux Mint USB（确已正确创建，例如使用 Rufus 或 dd）。
- 开启笔记本并立即开始点击以下按键之一：
  - **F12** — 2011 年左右 Lenovo 笔记本（包括 ThinkPad 和 IdeaPad）最常用的 Boot Menu 按键
  - **F10** 或 **Fn + F10** — 在某些模型上有效
  - **Esc** — 偶尔的替代方案
- 当 **Boot Menu** 出现时，选择 USB 设备（可能显示为 "USB HDD", "UEFI: USB", "Kingston" 等）。
  按 Enter → 它应该开始启动 Linux Mint。

**方法 B — 在 BIOS 中永久更改启动顺序**

- 进入 BIOS（如上所述使用 F1 或 F2）。
- 转到 **Startup** 或 **Boot** 选项卡（使用方向键）。
- 找到启动优先级 / 启动顺序列表。
- 使用 + / – 键或 F5 / F6 将 USB 设备（通常列为 "USB HDD", "Removable Device" 或品牌名称）移动到顶部。
- 如果你看到 **UEFI/Legacy Boot** 或 **Boot Mode**，将其设置为 **Legacy**（或 "Both"/"CSM"）—— 大多数 2011 年的 Lenovo 笔记本在 Legacy/CSM 模式下运行 Linux Mint USB 效果更好。
- 按 **F10** → 选择 Yes 以 **Save and Exit**。

保存后，笔记本应在下次重启时自动从 USB 启动。

**2011 年 Lenovo 笔记本快速总结**

- BIOS → 先尝试 **F1**（ThinkPad 风格），然后是 **F2**
- 从 USB 启动 → 启动时点击 **F12** 进入 Boot Menu（最快的方法）

References:

- https://support.lenovo.com/us/en/solutions/ht500222-recommended-ways-to-enter-bios-boot-menu-thinkpad-thinkcentre-thinkstation
- https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad
- https://www.wikihow.com/Enter-the-BIOS-on-a-Lenovo-Laptop
