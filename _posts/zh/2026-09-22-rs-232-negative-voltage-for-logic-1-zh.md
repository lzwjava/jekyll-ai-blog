---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'RS-232: 逻辑1的负电压'
translated: true
type: note
---

问题：**RS-232 逻辑 1 的电压范围是 −15 V 到 −5 V 吗？**

答案：**是的，大致如此——但正式 RS-232C 的限值更为精确。**

对于 RS-232 接收器：

| RS-232 信号电压 | 含义 |
| --------------: | ---- |
| **+3 V 到 +15 V** | 逻辑 **0**（SPACE） |
| **−3 V 到 −15 V** | 逻辑 **1**（MARK） |
| **−3 V 到 +3 V** | 未定义/过渡区域 |

因此：

```text
Voltage

 +15V ───────────── maximum
       │
       │  Logic 0
 +3V  ─────────────
       │
       │  UNDEFINED
  0V  ─────────────
       │
       │  UNDEFINED
 -3V  ─────────────
       │
       │  Logic 1
 -15V ───────────── minimum
```

关键点是：

```text
RS-232:

1  → negative voltage
0  → positive voltage
```

这与你可能从普通数字逻辑中得到的直觉**相反**，在普通数字逻辑中：

```text
CMOS:
1 → +3.3 V
0 → 0 V
```

### 一个细微的点

不要认为逻辑 1 必须严格等于 `-15 V`。

例如，发射器实际输出的可能是：

```text
Logic 1 → -8 V
Logic 0 → +8 V
```

这也是完全有效的。

标准规定的是**电压范围**，而不是每个设备都必须输出 ±15 V。

另外，区域：

```text
-3 V < V < +3 V
```

故意留作**无效/未定义区域**，为接收器提供噪声裕量。
