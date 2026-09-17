---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 奈奎斯特采样定理清晰解释
translated: true
type: note
---

问题：什么是通信系统中的**奈奎斯特定理**？

答案：

关键思想是：

> **如果一个带限信号的采样频率至少是其最高频率的两倍，则该信号可以从其采样中完美重构。**

数学上表示为：

$$
\boxed{f_s \ge 2f_{\max}}
$$

其中：

* \\(f_s\\) = 采样频率
* \\(f_{\max}\\) = 信号中的最高频率分量

### 1. 直观理解

假设你的模拟信号如下：

$$
x(t)=\sin(2\pi 10\,000t)
$$

其最高频率为：

$$
f_{\max}=10\,\text{kHz}
$$

因此你需要：

$$
f_s \ge 2\times10\text{kHz}=20\,\text{kHz}
$$

因此以 **20 kHz 或更高** 频率采样可实现理想重构。

这就是 CD 音频使用以下频率的原因：

$$
44.1\text{ kHz} > 2\times20\text{ kHz}
$$

因为人耳可听频率大约上限为 20 kHz。

---

### 2. 为什么是“两倍”？

考虑一个正弦波。

如果采样过慢，不同的模拟频率可能产生完全相同的采样点。

例如，以 15 kHz 采样一个 10 kHz 的正弦波，它会表现为一个 **5 kHz 的正弦波**。

这种现象称为**混叠**。

![Image](https://images.openai.com/static-rsc-4/22WVjWn_qazMYn_jYImv4gHIRaTqjdMpGf72Z1wFB5Zi5ZKj3H_E0nOxLwBYNTsM8qSw7wNciUQEKXid6KJhSZL2Mou11CklH7LwL21Esr5TsVXxRnq4ljhGnAwVbbMAH_2XHxZB3P4BB2xtGuM7GRe3-4GidOL6B9tsykCmIeU0jm6Ut6g8QQiAL9shsUUH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UugvvRPQiUYiNSdO1oK8M7O2ZapfDX_1MMxcR6V-fQ4eYIIbHVYRX8kW4MEs5pYkixxE8j8myWO_8D6Qvrn-Bn4Ec-wwbuT1BT1wkkFu33v0woDP5aLpne8ZpSEa7kFecKU5UlpqJt8p3nyx2IcsSSCA-csJyeunep_rZWqveJUVsgvKIboCnUJnG3dR3Ae9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/X0PSHK45ShtBfvClVG3rY_7rIZEDBLnWlRarK2jfDNic84in3WOpAfvEAs80yc1gLvjkWmJuok84vWMDnYGmu65ca11cSs0ojpan_AqfhQBD6ml5CbLK66J3835jLyg4si_k4IGccqaPtNF01f6NqJAJJTeZL30Ed_xgsURre2MxPnHsrRwC2jik2NWf5zSO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yDyjJVIz3KbuqcDooga6g3g6GF_6qrJtmSt2XMOWKp9LHhurfBy0LqDsvXeriMucbFYlJC6iB_XM1vbdpTNGQ8BkZlyGaUKw3YBuOteiPLwwB0S3v1211CsRHkI_s0sNRVjz3ZdZeWpyGZcTV8htU6ezv4KE1KV9THYDu8pTwYBZRe1JpdmgJGAsCqWDKO9f?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/V4fEhEWtwFxEeNOJEYowYC-2Uoz6pvYodytx5mgEy2-PCc_7l6ijr31IUwFvoOr1OHzJXy5wuJGt70mQejFeaUPnQpjkTabytY-wEDYAx0aBqRwrIErxqbkemRE-E4_pQlvB-5M3mL9b42oMy3gKUdO4A6G8xMA4e6vERuMJJE-F7UC485HoET4MdDn9kbYE?purpose=fullsize)

频率关系大致为：

$$
f_{\text{混叠}} = |f - k f_s|
$$

对于某个整数 \\(k\\)。

例如：

$$
10\text{ kHz} \quad\text{以}\quad 15\text{ kHz}\quad\text{采样}
$$

得到：

$$
|10-15|=5\text{ kHz}
$$

因此采样后，你无法区分原始的 10 kHz 信号和 5 kHz 信号。

---

### 3. 在通信系统中

在**奈奎斯特采样定理**和**奈奎斯特无码间干扰准则**之间存在重要区别。

上面介绍的那个通常称为：

**奈奎斯特采样定理**

$$
\boxed{f_s \ge 2B}
$$

其中 \\(B\\) 是信号为基带限时的带宽。

但在数字通信中，你可能还会遇到**奈奎斯特比特率公式**：

$$
\boxed{R_{\max}=2B\log_2 L}
$$

其中：

* \\(R_{\max}\\) = 无噪声信道的最大理论符号/比特率
* \\(B\\) = 带宽（Hz）
* \\(L\\) = 信号电平数

对于二进制信号，\\(L=2\\)：

$$
R_{\max}=2B
$$

这是**一个不同的奈奎斯特定理**。

### 快速记忆方法

| 概念                         | 公式                | 含义                            |
| ---------------------------- | ------------------- | ----------------------------------------------- |
| **奈奎斯特采样定理**         | \\(f_s\ge2f_{\max}\\) | 模拟信号的采样速度要求                          |
| **奈奎斯特比特率定理**       | \\(R=2B\log_2L\\)     | 理想无噪声信道的最大数据速率                     |

并且不要将两者与**香农容量**混淆：

$$
\boxed{C=B\log_2(1+\mathrm{SNR})}
$$

香农处理**噪声**；奈奎斯特比特率公式假设**理想无噪声信道**。

我还可以详细解释**为什么因子 \\(2B\\) 在数学上通过傅里叶变换/sinc 重构出现**，这使该定理更容易记忆。
