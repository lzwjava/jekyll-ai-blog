---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI作为嵌入式计算层
translated: true
type: note
---

**问题：未来的 AI 设备会是什么样子？**

**回答：**

我认为重要的转变是：

> **AI 不再是打开的应用，而成为嵌入物理 objects 的计算层。**

可能的演变过程大致如下：

| 时代      | AI 设备                   | 核心理念                           |
| --------- | ------------------------- | ---------------------------------- |
| 2020–25年 | 手机 + 云端大语言模型        | 你与一个 app 对话                   |
| 2025–30年 | AI PC / AI 手机            | 本地推理 + 云端                     |
| 2026–32年 | AI 眼镜                  | AI 持续看/听                        |
| 2028–35年 | AI 耳机 / 可穿戴设备        | 始终在线的个人助手                     |
| 2030年代    | 机器人                    | AI 在物理空间中行动                   |
| 更后期     | 环境计算                  | 环境本身成为交互界面                   |

### 1. AI 眼镜很可能是近期最大的外形规格

![Image](https://images.openai.com/static-rsc-4/6NNa5X2ILtmX5CTnPcm6B4ySZrjjEiMi5t4bz0v5-IKeWcaKiS7sN62MbGb4GiYieSzwNi1wbEzjz-qcnKXs-pzvxtbHSwC2bPZTBjcmFVdYGo6gZfwuSBDCvvqrYtq0kP0qrIvOt_-AlhM9AJqZeXjXXszMz4UsF9b0BWaN6xNZUO1abMlI1VjQ9AY0wJvG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Kbrr10DxpJ87ne8aEJaa-3IpaExvTwhq1dGaelH5hFNjE0-0eaTBVOknv4gDTHKeaCQnqcGoSXBqHn1UUPRW0wCXMAB84thLhOf41RVnhL2FTsX_adMzniWo1uBgzyIvf9UODGViRUss0fQx3rU9ZoCyXieW9_xmWD4tIk2MtbgMKqWhcnUL2QCIlb2QR8l0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CKessij0HhVxLeSQCgwpU-wIGhTF1VKJsytJGCxfI_zNGCBkdgsI37V3mAZF9jQXcV1klQmExos1SGAr0qyO6yYHQ13eyaixdGbMhMtL7_xSjDSM11iIAf-SfZ1SEpaCf4zAcAsAFO5RgWxSo6emV7EXZnFivfgvb2Y2HZeJdnMXZR7F5DXfMvb6go99RYNa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_Ih44136qCVxpKqlEiB4Xf2OTxDEo2ihBiHocxcjQt_IQ7ljm5wEm5ZOnnT7P4o1zYl6SPBmaM4nz2Om2R3KVMfLoRrJG04k5sWLEz3onKGU3VpNJuhpCTDvJrlHf1QySLS5UaiCPmN0qLB4mVQCSnbBAzxoGS2Rd-i-RkHLizIq5tBcWAsYlqBGA7t0U_sR?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xe6eOFj6wMl07nWTIbJoSUMa4Ex0-mrsydC8bZ7Ts3CB6Fxni6qKLXmFfMPGF-Cyzov2YTuiOfuXn4RbKpNQ-RzCctBP4GuK6U1wfBizlumPp8NIe1LmR82S6YHQw5xQcXs_69SRGleAiFc1FonQFpHYYXRoJ8RyGUs19oKTh7R4uvRXJCEHeNmu1aX74n94?purpose=fullsize)

设想你可以随身带着这样的系统：

```text
摄像头 ─────┐
麦克风 ─────┤
             ↓
        本地 AI
             ↓
       云端模型
             ↓
      ┌──────┴──────┐
      ↓             ↓
   音频输出        显示
```

你不需要问：

> "这是什么建筑？"

眼镜已经看到了。

你不需要打字：

> "翻译这个菜单。"

它们看到菜单并悄悄告诉你翻译。

交互变成了 **上下文 → 推理 → 行动**，而不是 **键盘 → 提示 → 回答**。

---

### 2. AI 耳机可能变得比眼镜更重要

耳机有一个巨大的优势：

**它们已经整日戴在你的耳朵里。**

它们可以提供：

* 语音翻译
* 会议记忆
* 个人提醒
* 导航
* 上下文问答
* 实时对话辅助
* 环境感知

对于许多任务，你并不需要屏幕。

```text
世界
  ↓
麦克风
  ↓
语音/音频编码器
  ↓
大语言模型
  ↓
TTS
  ↓
你的耳朵
```

这本质上是一个 **始终可用的语音助手**。

---

### 3. 手机可能成为"计算枢纽"

眼镜/耳机不会立即取代手机，而是作为轻客户端：

```text
             ┌── 眼镜
             │
传感器 ──────┼── 耳机
             │
             └── 手表
                  │
                  ↓
             智能手机
                  │
             ├── NPU/GPU
             ├── 存储
             └── 网络
                  │
                  ↓
              云端 AI
```

手机的重点逐渐从 *触摸屏幕* 转向提供：

**计算 + 电池 + 连接 + 存储**。

---

### 4. AI 机器人是最有趣的终点

当前的大语言模型拥有：

```text
眼睛 → 视觉模型
耳朵 → 语音模型
大脑 → 大语言模型
手   → ????
```

机器人学旨在闭合这最后一个循环：

```text
观察
   ↓
理解
   ↓
推理
   ↓
规划
   ↓
行动
   ↓
再次观察
```

这与 ChatGPT 有本质区别。

机器人可以接收：

> "整理书桌。"

并将其转化为数百个底层操作。

这就是 **AI + 硬件 + 强化学习 + 视觉 + 仿真** 交汇之处。

---

### 5. 终极设备可能是一种我们现在不称之为"设备"的东西

最终：

```text
              ┌───────────────┐
              │ 个人 AI        │
              │   智能助手     │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     眼镜          手机          机器人
        ↓             ↓             ↓
     摄像头        传感器         执行器
        └─────────────┼─────────────┘
                      ↓
                 个人模型
```

这个 **智能助手** 成为了产品。

物理设备则成为它的：

* 眼睛
* 耳朵
* 嘴巴
* 手
* 轮子
* 网络接口。

这就是为什么我认为"AI 设备"最终与其说是发明一个新 gadget，不如说是赋予 AI **持续的感知 + 记忆 + 自主能力 + 执行器**。

### 我的预测

如果让我对重要的硬件方向进行排序：

**2026–28年：** AI 眼镜 / 耳机
**2027–30年：** 本地 AI PC 和手机
**2028–35年：** 人形 / 专用机器人
**2030年之后：** 环境 AI + 机器人生态系统

而对于既喜欢 **大语言模型** 又喜欢 **硬件维修** 的人来说，最有趣的交汇点可能是 **边缘 AI 计算**：NPU/GPU 模块、摄像头、传感器、电源电子、嵌入式 Linux 以及小型多模态模型。这比仅仅运行另一个聊天机器人更接近 AI 的物理未来。

我还可以具体描绘一下 **2030 年左右一台 1000 美元的个人 AI 设备堆栈** 可能实际包含的内容——计算、摄像头、内存、电池、模型大小以及带宽。
