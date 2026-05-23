---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越原始硬件的iPhone流畅度
translated: true
type: note
---

**问题：** 为什么 iPhone X 用起来比 Google Pixel 7 更流畅，尽管 Pixel 7 搭载了更新、更快的芯片？

**回答：**

这是一个经典的“感知流畅度”问题。答案涉及多个叠加因素，而不仅仅是原始硬件性能。

## 1. VSYNC 与帧率节奏

iPhone X 运行在 **60Hz**，但 Apple 的渲染管线极其严格地以一致的帧时间达到 60fps 目标。一个节奏完美的 60fps *感觉上* 比一个节奏不统一的 90/120fps 更流畅，因为你的眼睛真正感知到的卡顿是**帧时间波动**。

Pixel 7 的屏幕运行在 **90Hz**，但 Android 的帧调度器历来较为松散。即使是在 90Hz 下，一帧耗时 15ms 而非 11.1ms 也会导致明显的卡顿。Google 已有所改进，但 Apple 的管线在端到端上更为紧凑。

## 2. 触控延迟——真正的杀手

Apple 的秘密武器是**触控采样与输入延迟**：

- iPhone X 的**触控采样率为 120Hz**（是屏幕刷新率的两倍）
- 触控控制器与 SoC 协同设计——没有第三方触控 IC 带来的延迟
- Apple 在**专用的低延迟路径**上处理触控输入，与主渲染管线解耦

Pixel 7（Tensor G2）：触控采样率为屏幕刷新率（90Hz），输入经过 Android 的 `InputDispatcher` → `ViewRootImpl` → `Choreographer` 管线，每一步都增加延迟。

结果：iPhone X 的触控到像素延迟约为 **~30-40ms**，而 Android 通常为 **~60-80ms**。这种差异是*可以感受到的*，不仅仅是测量数据。

## 3. Core Animation 与 Android 的渲染线程

iOS 使用 **Core Animation**，它运行在独立的**渲染服务器**（`backboardd`/`SpringBoard`）上，与应用进程分离：

```
应用进程 → 提交 CA 事务 → 渲染服务器合成 → GPU → 屏幕
```

即使你的应用主线程繁忙，动画仍能在渲染服务器上以完整帧率运行。滚动动画、弹簧物理、转场效果——从应用角度来看都是“发射后不理”。

Android 的对应物是 **RenderThread**（Android 5 中添加），但在进程内运行，且与应用生命周期耦合更紧密。一个层的卡顿可能传播到其他层。

## 4. ProMotion 与固定刷新率——但这里情况相反

讽刺的是，iPhone X 没有 ProMotion（iPhone 13 Pro 才引入）。所以理论上 Pixel 7 的 90Hz 应该更胜一筹。但帧率节奏糟糕的 90Hz 在感知上输给了帧率节奏完美的 60Hz。

## 5. 滚动物理与弹簧动画

Apple 的滚动减速曲线和弹簧动画（`UIScrollView`）经过了严苛的调校。**橡皮筋效果**、动量曲线和手势识别器优先级系统都是第一方自研，并经过了 15 年以上的实战检验。

Android 的 `RecyclerView` + `OverScroller` 物理机制不同，第三方应用经常不一致地覆盖它们。结果就是 Android 上不同应用的滚动行为各不相同。

## 6. GPU 驱动成熟度

Apple 的 GPU 驱动是**用户空间 + 编译进 iOS** 的。没有内核驱动往返，没有为 UIKit 渲染采用通用的 Vulkan/OpenGL 开销。Metal 堆栈与 GPU 协同设计。

Pixel 7 的 Tensor G2 使用 **ARM Mali GPU**，搭配通用驱动堆栈。Tensor 芯片在 Android 上与高通骁龙相比历来存在 GPU 性能问题，这使得 Pixel 7 的情况比其他 Android 旗舰机更糟。

## 总结表

| 因素 | iPhone X | Pixel 7 |
|---|---|---|
| 屏幕刷新率 | 60 | 90 |
| 触控采样率 | 120Hz | 90Hz |
| 触控延迟 | ~35ms | ~65ms |
| 动画管线 | 渲染服务器（进程外） | RenderThread（进程内） |
| GPU 驱动 | Metal，协同设计 | Mali，通用堆栈 |
| 帧率节奏一致性 | 优秀 | 良好但存在波动 |

**核心洞察：** 流畅度主要取决于*输入延迟*和*帧率一致性*，而非时钟速度或刷新率。Apple 掌控全栈——芯片、操作系统、框架、应用——并且针对这条路径优化了 15 年。Google 正在追赶，但其软件+硬件堆栈仍有更多可动部件，且垂直整合程度较低。