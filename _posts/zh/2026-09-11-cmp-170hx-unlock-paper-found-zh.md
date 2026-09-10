---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 发现 CMP 170HX 解锁论文
translated: true
type: note
---

问题：**你指的是最近的CMP 170HX解锁论文，而不是GitHub上的实现。**

答案：**是的——你说得对。我找到了。**

这篇论文是：

**《加密矿中的金丝雀：击败GPU安全协处理器中的堆栈保护》——Jon Pry，2026年6月。** 该论文于**2026年6月26日**上传，明确针对CMP 170HX。([ResearchGate][1])

[论文——加密矿中的金丝雀](https://www.researchgate.net/publication/408132536_A_Canary_in_the_Crypto_Mine_Defeating_Stack_Protection_in_a_GPU_Secure_Coprocessor?utm_source=chatgpt.com)

该论文的核心成果远比单纯的“解锁VRAM”更有趣：

```text
CMP 170HX
   │
   ├── GA100 / A100 芯片
   │
   ├── SM速率：1/32
   ├── VRAM：暴露8/10 GB
   └── PCIe：Gen1
          │
          ▼
   SEC2 / 高度安全Falcon
          │
          ▼
   堆栈保护绕过
          │
          ▼
   任意代码执行
          │
          ▼
   修改GPU特权状态
          │
          ├── 恢复SM吞吐量
          ├── 恢复内存布局
          └── 解除PCIe限制
```

论文声称，这三项商业限制可以通过**已获取root权限的主机在软件层面破解**，无需NVIDIA签名密钥、调试熔丝或物理访问。关键漏洞在于GPU安全协处理器的堆栈保护机制。([ResearchGate][1])

而时间线现在非常清晰：

* **6月26日：**《加密矿中的金丝雀》作为预印本流传。
* **7月1日：**原始的`booter_load`反汇编出现。
* **7月3日：**带注释的反汇编。
* **7月10日：**寄存器/小工具研究。
* **7月14日：**`cmpunlocker`初始提交。
* **7月16日：**论文以`main.pdf`形式发布到研究服务器。
* **7月18日：**工作内存解锁提交。([GitHub][2])

因此，**你记得的论文几乎可以肯定是Jon Pry的论文**。后来的`cmpunlocker`项目是围绕这项研究构建的实现/复现层。([GitHub][3])

我还可以追溯**论文 → 确切漏洞 → 确切寄存器写入 → 8 GB → 64 GB 的转变**，并从技术层面完整映射整个过程。

[1]: https://www.researchgate.net/publication/408132536_A_Canary_in_the_Crypto_Mine_Defeating_Stack_Protection_in_a_GPU_Secure_Coprocessor?utm_source=chatgpt.com "(PDF) 加密矿中的金丝雀：击败GPU安全协处理器中的堆栈保护"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/history/clean-room-and-provenance.md?utm_source=chatgpt.com "cmp170hx/docs/history/clean-room-and-provenance.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://github.com/WebForks/cmpunlocker/blob/main/README.md?utm_source=chatgpt.com "cmpunlocker/README.md at main · WebForks/cmpunlocker · GitHub"
