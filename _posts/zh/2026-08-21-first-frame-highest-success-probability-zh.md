---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 首帧最高成功概率
translated: true
type: note
---

问题：在二进制指数退避算法中，哪个帧的传输成功概率最高？

答案：是的，你的回答正确，解释也很准确。

在**二进制指数退避算法**（用于CSMA/CD，例如以太网）中：

- 当发生碰撞时，站点在重传前会等待一个随机时隙数。
- 随机退避的范围随每次碰撞呈指数增长：
  - 第1次碰撞：从{0, 1}中随机选取 → 范围 = 2
  - 第2次碰撞：从{0, 1, 2, 3}中随机选取 → 范围 = 4
  - 第k次碰撞：从{0, 1, ..., 2^k − 1}中随机选取 → 范围 = 2^k

**为什么A（首次发送）的成功概率最高：**

| 帧 | 碰撞次数 | 退避范围 | 网络状态 | 成功概率 |
|---|---|---|---|---|
| A | 0 | 无（无需等待） | 最不拥挤 | **最高** |
| B | 2 | {0–3} | 中等 | 较低 |
| C | 4 | {0–15} | 更拥挤 | 更低 |
| D | 8 | {0–255} | 非常拥挤 | 最低 |

两个叠加的原因使A成为最佳：
1. **更小的退避范围** → 随机延迟更小，重试更快
2. **更少的先前碰撞** → 当时网络拥堵程度更低

你的记忆技巧很实用：
> "首发送，成功率高；冲突多，概率跑。"

---

参考资料：
- [Binary Exponential Backoff - Wikipedia](https://en.wikipedia.org/wiki/Exponential_backoff)
- [CSMA/CD and Backoff Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/collision-detection-csmacd/)