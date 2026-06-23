---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Miu2D：从零开始的2D ARPG引擎
translated: true
type: note
---

Miu2D 是一个从零构建的 2D ARPG 引擎，采用 TypeScript + Rust 编写，通过原生 WebGL 渲染，不依赖任何游戏框架。

关键事实：

- 17.6 万行代码
- TypeScript + Rust（寻路编译为 WASM）
- 原生 WebGL —— 无 PixiJS、Phaser、Unity、Godot
- 自研精灵批处理、A* 寻路、二进制格式解码器、脚本虚拟机、天气粒子、屏幕特效 —— 全部从底层实现
- 自定义 DSL 包含 218 条命令 + Lua 5.4 运行时（通过 wasmoon）
- Rust A* 寻路通过 WASM 运行约 0.2ms，采用零拷贝共享内存
- SpriteBatcher 将约 4800 个图块绘制合并为 1-5 次 WebGL 绘制调用

作为概念验证，它复刻了三款经典金山（西山居）武侠 RPG，可在浏览器中完整游玩：

1. 《剑侠情缘外传：月影传说》—— 2001 年，7 个以上结局
2. 《剑侠情缘贰》—— 1998 年，暗黑破坏神风格实时战斗
3. 《新剑侠情缘》—— 2001 年，110 张以上地图

这是一个单体仓库（pnpm workspace），包含一个 Web 包、用于数据转换/分析的脚本以及一个 Vercel 部署。项目从第一天起就采用 AI 辅助编码（"vibe coding"）。

在线演示：<https://miu2d.com>
