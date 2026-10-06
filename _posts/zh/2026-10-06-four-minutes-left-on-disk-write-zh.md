---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘写入剩余四分钟
translated: true
type: note
---

你已完成 **77%**。以下是计算过程：

- ISO 总量：**6,518,974,464 字节**（6.07 GiB）
- 已写入：5,041,553,408 字节（4.7 GiB）
- **剩余：约 1.4 GiB**（1,477,421,056 字节）

按当前约 5.85 MB/s 的速度：

```
1,477,421,056 字节 ÷ 5,847,161 B/s ≈ 253 秒
```

**大约还剩 4 分钟**（约 4.2 分钟）。注意速度已降至约 5.8 MB/s，因此很可能是 USB 2.0——不要期望它会加速。让它完成即可；结束后会显示一行 `2948850+1 records in / out` 并返回提示符，然后运行 `sync`，并用 `diskutil list disk12` 进行验证。