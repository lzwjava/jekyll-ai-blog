---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pip 依赖版本冲突
translated: true
type: note
---

因为 `torch 2.11.0` 或 `sglang` 可能声明了类似 `triton>=3.5` 的依赖约束。当你正常执行 `pip install triton==3.4.0` 时，pip 会检查所有已安装包的约束，然后要么：

1. **拒绝**降级（出现冲突错误）
2. **接受**降级，但随后在 pip 解析依赖时又被升级回去（这正是实际发生的情况——它又被升级回了 3.6.0）

`--no-deps` 告诉 pip：“只安装这个精确版本，不要检查或安装任何依赖。”它强制固定了版本。

但老实说，即使使用 `--no-deps` 也可能无法持久——torch 可能在运行时加载 triton 并进行版本检查。使用 vLLM 是这里更干净的解决路径。