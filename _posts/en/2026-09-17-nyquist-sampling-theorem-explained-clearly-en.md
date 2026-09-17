---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nyquist Sampling Theorem Explained Clearly
translated: false
type: note
---

Question: What is the **Nyquist theorem (奈奎斯特定理)** in communication systems?

Answer:

The key idea is:

> **A band-limited signal can be perfectly reconstructed from its samples if the sampling frequency is at least twice the highest frequency contained in the signal.**

Mathematically:

$$
\boxed{f_s \ge 2f_{\max}}
$$

where:

* \\(f_s\\) = sampling frequency
* \\(f_{\max}\\) = highest frequency component in the signal

### 1. Intuition

Suppose your analog signal looks like:

$$
x(t)=\sin(2\pi 10\,000t)
$$

Its highest frequency is:

$$
f_{\max}=10\,\text{kHz}
$$

Therefore you need:

$$
f_s \ge 2\times10\text{kHz}=20\,\text{kHz}
$$

So sampling at **20 kHz or higher** allows ideal reconstruction.

This is why CD audio uses:

$$
44.1\text{ kHz} > 2\times20\text{ kHz}
$$

because human-audible frequencies are approximately up to 20 kHz.

---

### 2. Why "twice"?

Think about a sinusoid.

If you sample too slowly, different analog frequencies can produce exactly the same sampled points.

For example, sampling a 10-kHz sinusoid at 15 kHz can make it appear as a **5-kHz sinusoid**.

This phenomenon is called **aliasing**.

![Image](https://images.openai.com/static-rsc-4/22WVjWn_qazMYn_jYImv4gHIRaTqjdMpGf72Z1wFB5Zi5ZKj3H_E0nOxLwBYNTsM8qSw7wNciUQEKXid6KJhSZL2Mou11CklH7LwL21Esr5TsVXxRnq4ljhGnAwVbbMAH_2XHxZB3P4BB2xtGuM7GRe3-4GidOL6B9tsykCmIeU0jm6Ut6g8QQiAL9shsUUH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UugvvRPQiUYiNSdO1oK8M7O2ZapfDX_1MMxcR6V-fQ4eYIIbHVYRX8kW4MEs5pYkixxE8j8myWO_8D6Qvrn-Bn4Ec-wwbuT1BT1wkkFu33v0woDP5aLpne8ZpSEa7kFecKU5UlpqJt8p3nyx2IcsSSCA-csJyeunep_rZWqveJUVsgvKIboCnUJnG3dR3Ae9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/X0PSHK45ShtBfvClVG3rY_7rIZEDBLnWlRarK2jfDNic84in3WOpAfvEAs80yc1gLvjkWmJuok84vWMDnYGmu65ca11cSs0ojpan_AqfhQBD6ml5CbLK66J3835jLyg4si_k4IGccqaPtNF01f6NqJAJJTeZL30Ed_xgsURre2MxPnHsrRwC2jik2NWf5zSO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yDyjJVIz3KbuqcDooga6g3g6GF_6qrJtmSt2XMOWKp9LHhurfBy0LqDsvXeriMucbFYlJC6iB_XM1vbdpTNGQ8BkZlyGaUKw3YBuOteiPLwwB0S3v1211CsRHkI_s0sNRVjz3ZdZeWpyGZcTV8htU6ezv4KE1KV9THYDu8pTwYBZRe1JpdmgJGAsCqWDKO9f?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/V4fEhEWtwFxEeNOJEYowYC-2Uoz6pvYodytx5mgEy2-PCc_7l6ijr31IUwFvoOr1OHzJXy5wuJGt70mQejFeaUPnQpjkTabytY-wEDYAx0aBqRwrIErxqbkemRE-E4_pQlvB-5M3mL9b42oMy3gKUdO4A6G8xMA4e6vERuMJJE-F7UC485HoET4MdDn9kbYE?purpose=fullsize)

The frequency relationship is roughly:

$$
f_{\text{alias}}
=
|f-kf_s|
$$

for some integer \\(k\\).

For example:

$$
10\text{ kHz}
\quad\text{sampled at}\quad
15\text{ kHz}
$$

gives:

$$
|10-15|=5\text{ kHz}
$$

So after sampling, you can't distinguish the original 10-kHz signal from a 5-kHz signal.

---

### 3. In communication systems

There's an important distinction between **Nyquist sampling theorem** and **Nyquist's no-ISI criterion**.

The one above is usually called:

**Nyquist sampling theorem**

$$
\boxed{f_s\ge2B}
$$

where \\(B\\) is the signal bandwidth when the signal is baseband-limited.

But in digital communication, you may also encounter the **Nyquist bit-rate formula**:

$$
\boxed{R_{\max}=2B\log_2 L}
$$

where:

* \\(R_{\max}\\) = maximum theoretical symbol/bit rate for a noiseless channel
* \\(B\\) = bandwidth in Hz
* \\(L\\) = number of signal levels

For binary signaling, \\(L=2\\):

$$
R_{\max}=2B
$$

This is **a different Nyquist theorem**.

### Easy way to remember

| Concept                      | Formula             | Meaning                                         |
| ---------------------------- | ------------------- | ----------------------------------------------- |
| **Nyquist sampling theorem** | \\(f_s\ge2f_{\max}\\) | How fast to sample an analog signal             |
| **Nyquist bit-rate theorem** | \\(R=2B\log_2L\\)     | Maximum data rate of an ideal noiseless channel |

And don't confuse either with **Shannon capacity**:

$$
\boxed{C=B\log_2(1+\mathrm{SNR})}
$$

Shannon deals with **noise**; Nyquist's bit-rate formula assumes an **ideal noiseless channel**.

I can also walk through **why the factor \\(2B\\) mathematically appears using Fourier transforms/sinc reconstruction**, which makes the theorem much easier to remember.
