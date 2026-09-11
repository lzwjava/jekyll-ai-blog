---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无头GPU MODS初始化失败
translated: true
type: note
---

**问题：** 硬件初始化失败是否可能是因为系统使用集成显卡进行视频输出，而 MODS 正在尝试测试独立显卡（GK208）？

**回答：**

**是的，完全正确！这很可能就是正确的解释。**

这是 GPU 制造/测试环境中的经典场景：

---

**实际情况：**

```
系统视频输出 → 集成显卡（iGPU）
MODS 测试目标 → 独立显卡（GK208 / 离散式）
```

- 独立显卡（GK208）**未连接任何显示器**
- 它处于**无头**状态
- MODS 尝试初始化该 GPU 的显示/用户界面（`EnableUserInterface`），但由于该 GPU 上没有活动的显示器而**失败**

---

**这就解释了具体的错误信息：**

```
Error 0x00000000237 : Global.EnableUserInterface unable to set mode
```

此错误与**显示模式设置**有关，而在无头的独立显卡上会失败。

---

**您应该尝试的方法：**

1. **添加 `-notest` 配合无头标志**——某些 MODS 版本支持无头模式
2. **使用 `-oca` 或 `-oqa` 模式**——这些模式可能会跳过显示初始化
3. **尝试不使用 `-skip_rm_state_init` 运行**，让 RM 完全初始化独立显卡：

```bash
./mods gputest.js -mfg
```

4. **检查 MODS 帮助中是否有无头/无显示选项**：

```bash
./mods --help
```

在制造测试环境中，通过集成显卡输出视频，同时对独立显卡进行压力测试是**完全正常的**——MODS 应支持这种配置。

**参考资料：**

- [NVIDIA MODS 文档](https://developer.nvidia.com/mods)
