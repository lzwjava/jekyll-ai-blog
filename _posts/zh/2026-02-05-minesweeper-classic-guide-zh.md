---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 扫雷经典游戏指南建议
translated: true
type: note
---

扫雷 (Minesweeper) 是一款经典的 Windows 益智游戏！以下是玩法说明：

**查找游戏：**
- 在旧版 Windows (XP/7) 上：它预装在 Games 中
- 在 Windows 10/11 上：你可以从 Microsoft Store 免费下载 "Microsoft Minesweeper"

**游戏玩法：**

目标是根据每个方块中关于邻近炸弹数量的线索，清除包含隐藏 mines 的网格。

**基本操作：**
- **左键点击**：揭开方块
- **右键点击**：放置 flag（旗帜）标记你认为有 mine 的地方
- **双击左右键**（在某些版本中）：如果你已经标记了正确数量的 mines，则揭开所有相邻方格

**游戏规则：**
1. 点击任意方块开始 —— 第一次点击总是安全的
2. 数字表示周围 8 个方格中共有多少个 mines
3. 使用逻辑推断出 mines 必须在的位置
4. 标记所有 mines 并揭开所有安全方块即可获胜
5. 点击到 mine 则游戏结束

**策略技巧：**
- 从可能性较少的角落和边缘开始
- 如果数字 "1" 只触碰一个未揭开的方块，那么该方块一定是 mine
- 如果一个方块的数字等于它周围未揭开的方块数，那么它们全都是 mines
- 如果你已经标记了某个数字周围所有的 mines，那么剩下的方块就是安全的

**难度级别：**

| 难度 | 网格大小 | Mines 数量 |
| :--- | :--- | :--- |
| Beginner | 9×9 | 10 |
| Intermediate | 16×16 | 40 |
| Expert | 30×16 | 99 |

想要了解任何特定策略的建议，或在理解特定 pattern 时遇到困难了吗？