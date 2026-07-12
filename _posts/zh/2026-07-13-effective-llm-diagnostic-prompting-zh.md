---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 有效的LLM诊断提示
translated: true
type: note
---

问题：除了特定的PSU/主板问题——在向LLM询问此类诊断之前，充分描述发生的事情并写出好的prompt实际上是否重要？

回答：是的，这里是有具体机制原因的，而不仅仅是“良好实践”的空谈。

**为什么这对hardware diagnosis特别重要：**

LLM diagnostic output是对你输入的pattern completion，而不是针对你实际设备的lookup。当prompt薄弱时，两种failure mode叠加在一起：

1. **Under-specified prompt → 跨多种可能原因的interpolation。** “连接GPU后主板嗡嗡声”匹配training data中的：coil whine（正常）、PSU overcurrent、错误电缆插入、capacitor failure、ground loop、PSU sag under load。没有确切的事件顺序（插了什么，按什么顺序，噪音何时开始，是否完全开机），模型会选择所有这些案例中最*statistically likely*的narrative——这就是为什么你得到了一些“听起来合理”（分析出来一篇看起来有道理的）而非根据实际wiring *verified*的东西。

2. **没有与ground truth交叉验证 → 听起来自信的hallucination。** Corsair CPU/PCIe 8-pin pinout不匹配是真实且有记载的——相同的母头连接器形状，不同的pin接线，PSU制造商特定。但是否*that specific failure*就是你的主板所发生的事情是一个单独的说法，模型仅凭text description无法验证。是plausible，但未confirmed。

**真正解决这个问题的是——一个更好的prompt模板：**

```
上下文：
- Hardware: [exact PSU model, exact GPU model, exact motherboard model]
- Sequence: [what you plugged, in exact order, with timestamps if possible]
- Symptom: [buzzing/no post/etc — exact sound, exact timing relative to power-on]
- What you already ruled out: [reseated cable? multimeter tested? swapped PSU cable?]

询问：
1. 列出可能的root causes，根据症状按可能性排序
2. 对于每个，命名可以证伪它的specific test（不是“检查电缆”——“用multimeter测量pin X与pin Y之间的continuity，期望Y，如果Z则排除”）
3. 不要得出结论——仅提供下一步诊断步骤
```

这将LLM转变为checklist generator，而不是生成听起来合理但你无法依据其行动的故事的narrator。

**关于你朋友的怀疑**——值得认真对待，不要忽视：“如果合适就不应该有问题”对Corsair modular PSUs来说是错误的，因为连接器键位相同但CPU和PCIe轨道的接线不同——这是Corsair自己记录的警告，不是LLM猜测。如果错误接线的12V rail反馈到期望不同pinout的header，GPU*can*影响主板，尤其是在非ATX规范的适配器上。但“PSU兼容性这么差”也是一个合理的反驳——不是ATX坏了，而是*modular cables是PSU-model-specific的*，而且Corsair明确表示不要在同一品牌的不同PSU型号/世代之间混用电缆。这是一个真正的设计footgun，并非不可信。

底线：当主板在维修时，向维修店询问实际root cause（他们会有scope/multimeter），不要让LLM的“看起来合理”的narrative成为你接受的诊断，直到通过实际测量确认。

参考：

- [Corsair Cable Compatibility Guide](https://www.corsair.com/us/en/explorer/diy/psus/why-you-should-only-use-corsair-modular-cables-with-corsair-power-supplies/)
- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)