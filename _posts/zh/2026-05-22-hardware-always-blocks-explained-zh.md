---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 硬件always块详解
translated: true
type: note
---

**问题：** Verilog 中的 `always` 是什么意思？它像 for 循环吗？`posedge` 又是什么意思？

**回答：**

好问题——这些正是核心思维模式的转变。

---

## `always` —— 不是 for 循环

for 循环执行一次就退出。`always` **永不退出。永远不。** 它更像是：

```python
# 软件类比
while True:
    if condition_changed:
        recompute_output()
```

但即使这样也不对，因为它隐含了顺序检查。在硬件中，`always` 的意思是：

> **“这个电路是物理连接好的，只要输入发生变化，它会立即响应。”**

没有循环。没有迭代。硬件只是……存在。并做出响应。

```verilog
always @(*) begin
    out = a & b;   // 每当 a 或 b 变化时，out 立即更新
end
```

这综合成一个与门。没有循环。没有时钟。只是一根导线和一个门始终活跃在那里。

---

## `always` 的两种风格

### 风格 1：`always @(*)` —— 组合逻辑

```verilog
always @(*) begin
    out = a & b;
end
```

```
a ──┐
    ├─[AND]── out
b ──┘
```

`@(*)` 表示“当任何输入变化时触发”。这纯粹是物理过程——电流流动，输出在纳秒内更新。不涉及时钟。

### 风格 2：`always @(posedge clk)` —— 时序逻辑

```verilog
always @(posedge clk) begin
    q <= d;
end
```

这仅在时钟沿上更新。这就是 **触发器** —— 所有数字芯片中最基本的存储单元。

---

## `posedge` —— 上升沿

时钟信号看起来像这样：

```
clk:  0──┐  ┌──┐  ┌──┐  ┌──
         │  │  │  │  │  │
         └──┘  └──┘  └──┘

         ↑     ↑     ↑
       posedge posedge posedge   ← 在此触发
```

`posedge clk` = 时钟从 0 → 1 的 **确切时刻**。

`negedge clk` = 时钟从 1 → 0 的确切时刻。

所以：

```verilog
always @(posedge clk) begin
    count <= count + 1;
end
```

意思是：**“每个时钟节拍恰好一次，递增计数。”** 节拍之间——什么也不发生。数值被冻结。

---

## 并排对比

```verilog
// 组合逻辑 —— 类似纯函数，无记忆
always @(*) begin
    sum = a + b;    // 当 a 或 b 变化时立即更新
end

// 时序逻辑 —— 类似只在节拍上更新的变量
always @(posedge clk) begin
    sum <= a + b;   // 仅在时钟上升沿更新
end
```

硬件上的区别：

```
组合逻辑：                    时序逻辑：

a ──┐                        a ──┐
    ├─[ADDER]── sum              ├─[ADDER]──[D flip-flop]── sum
b ──┘                        b ──┘              ↑
                                              clk
```

触发器就是在每个时钟沿“捕获”数值并保持到下一个沿的盒子。

---

## 时钟就是一切

在实际运行于 3 GHz 的芯片中：

```
posedge 每秒触发 3,000,000,000 次
         ↑
         每次触发时，整个芯片中所有时序 always 块同时更新
```

MI300X 的计算单元运行在约 2.1 GHz。每个 posedge，芯片上数千个 `always @(posedge clk)` 块并行触发。这就是机器的运作方式。

---

## 给你一个具体类比

把它想象成一个事件循环，不过是物理的：

```
always @(*)        →  反应式：类似于 Vue/React 在状态变化时重新渲染
always @(posedge)  →  时钟驱动：类似于 setInterval(fn, 0.33ns) —— 每秒触发 30 亿次
```

只不过没有 JS 引擎。没有调度器。只有晶体管在切换。
