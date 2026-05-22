---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 类似Python的Verilog CLI工作流
translated: true
type: note
---

鉴于您的背景——终端优先、Python 原生、CLI 工具构建者——答案显而易见：

---

## **Icarus Verilog (`iverilog`)**

```bash
brew install icarus-verilog
```

就这样。一个工具，用起来和 GCC 一模一样。

```bash
iverilog -o sim counter.v counter_tb.v
./sim
```

- 无图形界面
- 无需许可证
- 无项目文件
- 输出在终端
- 错误信息像您已经熟悉的编译器错误
- 与 VSCode + Claude 完美搭配，用于 AI 辅助 Verilog 开发

---

**您将进入的工作循环：**

```
写 .v → iverilog → 读错误 → 问 Claude → 修复 → 重复
```

与您的 Python REPL 工作流相同。卡住时以 `picorv32` 作为参考代码开始。