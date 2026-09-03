---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 纸巾保护CPU插座针脚
translated: true
type: note
---

问题：为什么闲鱼上卖主板的人经常在CPU插槽上放纸巾/纸？

答案：通常是为了**在存储和运输过程中保护LGA CPU插槽引脚**。

在Intel LGA主板上，插槽内有数百/数千个极细的弹簧触点。如果有东西碰到它们，很容易弯曲。

卖家可能在插槽上放纸巾/纸，原因是：

* **保护引脚免受物理接触**——尤其是当CPU被取下时。
* **防止灰尘和碎屑**进入插槽。
* **防止插槽被包装刮伤/损坏**。
* 运输二手主板时，卖家可能没有原来的**塑料LGA插槽保护盖**，所以纸巾是一种廉价的替代品。

然而，**纸巾并不理想**。正确的保护是原装的**CPU插槽保护盖**：

![Image](https://images.openai.com/static-rsc-4/UfyIQmzD0MrhKGDWjt5OpEjf7qeu2mX030i0RdIGf2YlWJIVGn6fVYo-zqOfWoSbroFQMTOVQOno9wdWUtHbU3yHIKnp-km9OAnqwZVn_LyL25bPw_xc5a6M2T3cfmST6fu4_tY8XReRjf2KW5-BoRpkP43EZP2LIcDn1XCA2ASQAE4uyhzNt9QMgh7cZTGc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Q8YOXKzGmFMgq5I2mk-_XN6_ZZZIDIddb2W7os31y4DmF9pVUXpngdSdzfU9t2qcRBvEnETKwgVb66yURIW9--oM6lTR4Prn1EdPrX02boumIQ5yzeGQpZrSEYZd0goDKSN_giECxMh7405ulZiLfEd55G4eV12Xf91ILaYaIuKCxkOPlmZR7ec0B59CU_En?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Ok_eSX9mbsb0s3Teu9arMNXFG5LYRT0CzfrTkVdsJcgX9ZhbcK2JoYQ1sMEZ4ssV_tuXv_TDB2sJajoW4S3_nO6kO4s05W7VrOFlGi4zyKSoUm5TwLyLxE5EJQVENE9KPrxkE5j8LsNNkS_gfpQM4156Chgvuo021blcuWgAccvZlMV3lwO_d_1YOwbErZuZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/jUAyVZ8eO8WCTniIci4UL6h83wKgQV8i6kURC7TmzcC5ZwP4G_ImjVCXz0RHGrS5M1wzDW_3Ux3b2TCu4VJxyJ0oFKYv9EP4fJ7SKNjVenQpcn40tmNf7UgcquYO7XhNeNIcEDD6e_od68m0n2bsmca_H6_5HXanweF_zAno1nuXOlJGW8mi57EKh39syZwJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WnI3xZZs-PPnL-3Q7X8aIpPfqfHkY8XRXduwQG6XF1pOpEWQQHVaXrcNbjUQP83VDDbI3E-rGzpJMV_zZk7_ct7XTPQP3dlpvsKcCo1SqWMZ0DeXJjhdfvIUMucgtapO_H9H53CclZ2pkJJBNYpEOWqalWuNv6Zg4ffkR0_Q8tSrP7VIuZX5Yalnfg_ai01_?purpose=fullsize)

### 为什么这在购买二手主板时很重要

如果你收到一块插槽上盖着纸巾的主板，**不要立即横向拉扯纸巾**。

危险在于引脚：

```text
        CPU插槽
   ┌─────────────────┐
   │  \ \ \ \ \ \ \  │
   │   \ \ \ \ \ \   │  ← 极其脆弱的引脚
   │  \ \ \ \ \ \ \  │
   └─────────────────┘
          ↑
       纸巾
```

如果纸巾的纤维卡在引脚中，拉扯它可能会导致引脚弯曲。

正确做法：

1. 将主板从包装中取出。
2. 水平放置主板。
3. 在强光/放大镜下检查插槽。
4. 如果纸巾只是松散地放在上面，则非常轻柔地**垂直向上**提起它。
5. 检查是否有任何插槽引脚弯曲。

**重要的是，装有CPU的主板不需要在插槽上盖纸巾**——CPU本身就能保护触点。纸巾主要出现在卖家运输**没有CPU且没有原装插槽保护盖**的主板时。

如果你购买这些便宜的闲鱼板子专门用于你的GPU测试平台，我建议你特别关注**LGA引脚是否弯曲、插槽保护盖是否缺失、是否有腐蚀、以及主板能否正常POST**，而不是把纸巾本身视为可疑点。
