---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 根节点状态详解
translated: true
type: note
---

现在我对整体情况有了完整的了解。实际情况是这样的：

**根节点确实处于`ACTIVE`+`PASS`状态** —— 这意味着它已通过评估并准备展开。那个"PASS"标识是`result_state`，而非整体状态。节点本身是健康的。

**为何只有一个节点：** 根节点被添加到前沿集合后，展开循环开始执行。它会调用`_extract_child_contexts(root_problem_context)`，根据`route_options`生成子上下文。在`step_index=0`且没有`selected_route_family`的情况下，会**为每个路径选项创建一个子节点**，数量上限受`route_surface_budget`（=`max_children_per_expansion`，默认值为4）限制。

**真正的症结在于资源预算。** 构建根节点后，`expansions_used = 0`。但随后运行循环时，**构建根节点本身就被计入了一次展开**。在`expansion_budget = 8`且根节点需要大量模型调用的情况下，前沿展开虽然启动——但由于kimi-k2速度较慢，可能刚构建完根节点和少量节点，这8个资源槽位就已耗尽。

**解决方案：** 在预算输入框中填入更大数值（例如`4`），然后点击"运行下一步"。每次点击都会进一步展开前沿集合。路线分支（依赖关系、约束条件、不变性、扩展性）应该会在下次运行后作为根节点的子节点出现。只有当您在`run_on_create`完成后明确增加预算，决策树才会继续生长。