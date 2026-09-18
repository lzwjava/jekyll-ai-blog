---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 带宽效率：每赫兹比特
translated: true
type: note
---

**问题：什么是频带利用率（bandwidth efficiency）？**

**答案：**

**频带利用率 = 通信系统利用其可用带宽传输信息的效率。**

最常用的公式是：

$$
\boxed{\eta = \frac{R_b}{B}}
$$

其中：

* \\(R_b\\) = 比特率，单位为 **bit/s**
* \\(B\\) = 占用带宽，单位为 **Hz**
* \\(\eta\\) = 频带利用率，单位为 **bit/(s·Hz)**

### 示例

假设一个通信系统：

$$
R_b = 10\text{ Mbps}
$$

且占用带宽：

$$
B = 2\text{ MHz}
$$

则：

$$
\eta = \frac{10\times10^6}{2\times10^6}
=5\text{ bit/(s·Hz)}
$$

因此该系统每 1 Hz 带宽每秒传输 **5 比特**。

### 直观理解

将带宽想象成管道的宽度：

```text
带宽 B
<------------------------>

信息流
██████████████████████████  Rb
```

更高的 \\(\eta\\) 意味着 **每赫兹中挤入了更多比特**。

这就是为什么诸如 **QPSK、16-QAM、64-QAM、256-QAM** 等调制方式很重要：高阶调制可以在每个符号中传输更多比特，从而提高频谱效率。

对于理想的 \\(M\\)-ary 调制：

$$
\boxed{\eta \approx \log_2 M\quad \text{bit/(s·Hz)}}
$$

（在考虑脉冲成形滚降、编码开销、保护频带等因素之前）

例如：

$$
\text{QPSK}: \log_2 4=2
$$

$$
16\text{-QAM}: \log_2 16=4
$$

$$
64\text{-QAM}: \log_2 64=6
$$

因此 **频带利用率本质上就是“每秒每赫兹的比特数”。**