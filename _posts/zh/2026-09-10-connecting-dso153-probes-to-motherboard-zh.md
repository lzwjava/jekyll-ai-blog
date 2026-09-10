---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将DSO153探头连接到主板
translated: true
type: note
---

问题：在测量通电主板时，**DSO153 的红色和黑色 probe leads** 到底应该接在哪里？

回答：对于简单的电压测量：

```text
黑色 probe → GND
红色 probe → 你要测量的电压
```

### 最简单的首次测试：ATX +5VSB

将 PSU 连接到主板后：

```text
ATX 24-pin:

黑色线  ────── 黑色 probe
                 │
                 └── GND

紫色线 ───── 红色 probe
                 │
                 └── +5VSB
```

你应该会读到大约：

```text
+5 V
```

不要交换它们。

然后你可以测量：

| ATX 线 | 红色 probe | 黑色 probe | 预期值 |
| ------- | ----------- | ----------- | -------: |
| 紫色    | 紫色线      | 黑色线      |     ~5 V |
| 红色    | 红色线      | 黑色线      |     ~5 V |
| 橙色    | 橙色线      | 黑色线      |   ~3.3 V |
| 黄色    | 黄色线      | 黑色线      |    ~12 V |

对于你的**第一次测量**，我强烈建议**紫色 → 红色 probe，黑色 → 黑色线**。这是确认 DSO153 是否正常工作的最简单、最安全的方法。

如果你上传一张实际 ATX 连接器的照片，我可以为你识别出具体的孔/线。