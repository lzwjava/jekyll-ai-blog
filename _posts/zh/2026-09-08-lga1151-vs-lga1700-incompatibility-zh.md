---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LGA1151 与 LGA1700 的不兼容性
translated: true
type: note
---

**问题：** Intel Core i5-7400 能否用于 MSI B760M-E DDR5 主板？

**答案：** **不能。❌**

**i5-7400** 是 **第7代 Kaby Lake** CPU，采用 **LGA1151** 接口。

您的 **MSI B760M-E DDR5** 主板采用 **LGA1700** 接口。

```text
i5-7400
  └── 第7代
      └── LGA1151 ❌

B760M-E DDR5
  └── 第12/13/14代
      └── LGA1700 ✅
```

因此，请勿为 B760 主板购买以下 CPU：

```text
i5-7400   ❌
i5-7500   ❌
i7-7700   ❌
i5-8400   ❌
i5-9400   ❌
```

尽管其中一些 CPU 物理外形相似，但 **LGA1151 ≠ LGA1700**。

针对 B760M-E 主板，请在闲鱼搜索以下型号：

```text
G6900
G7400
i3-12100
i3-12100F
i5-12400
i5-12400F
i5-13400
```

如果您想围绕这块 B760M-E 主板组装**最便宜的电脑**，建议目标为**二手 G6900/G7400**。若需要更强的性能，**i5-12400/F** 是性价比之选。
