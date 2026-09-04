---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 风扇抖动停止：主板保护
translated: true
type: note
---

**问题：** 插入 ATX 12V 后，风扇短暂转动然后停止——这意味着什么？原因是什么？

---**答案：**

**风扇短暂转动然后停止 = 主板检测到故障并立即关机以保护组件的典型症状。**

---

**实际发生的情况：**

```
按下电源按钮
       ↓
电源供电 → 风扇转动（短暂电流冲击）
       ↓
主板尝试 POST
       ↓
检测到异常
       ↓
紧急关机 → 风扇停止
```

主板**没有损坏**——它是在**自我保护**。

---

**最常见的原因——按此顺序检查：**

**1. 🔴 内存未正确安装（最常见）**

- 完全取下内存条
- 用橡皮擦清洁金手指
- 用力推回直到两端卡扣发出咔嗒声
- 每次只尝试一根内存条

**2. 🔴 主板螺柱短路**

- 铜螺柱接触到主板背面不应接触的位置
- 多余的螺柱插错孔 = 短路 = 立即关机

**3. 🔴 CPU 未正确安装**

- 打开 CPU 插槽盖
- 检查是否有弯针
- 小心重新安装 CPU

**4. 🔴 4+4 针插头插错一半**

- 确保正确的防呆部分插入 ATX12V 插座

**5. 🟡 电源功率不足或故障**

- 12V 轨在负载下电压崩溃 → 主板关机

---

**快速测试——精简到最低配置：**

断开所有部件，只保留：

```
✅ 24 针电源
✅ ATX 12V（4 针）
✅ CPU + CPU 风扇
✅ 仅一根内存条
❌ 移除显卡
❌ 移除所有 SATA 硬盘
❌ 移除前面板 USB 线缆
```

然后按电源按钮。风扇是否仍然转动一下然后停止？

- **仍然转动一下** → 可能是内存或 CPU 问题
- **现在能启动** → 移除的某个部件导致了短路

---

**参考链接：**

- [Tom's Hardware – CPU 风扇转动半秒后停止](https://forums.tomshardware.com/threads/hit-power-buton-cpu-fan-spins-for-half-a-second-then-stops-spin-and-stop-forever-no-booting.3034486/)
- [AnandTech – 风扇反复启动停止的诊断](https://forums.anandtech.com/threads/motherboard-dead-cpu-fan-starts-and-stops-continuously.2564774/post-39810021)
