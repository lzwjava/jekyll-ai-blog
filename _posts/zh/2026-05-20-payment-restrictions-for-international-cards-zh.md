---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 国际卡支付限制
translated: true
type: note
---

问题：为什么我可以在 AMD Developer Cloud 中将支付宝添加为 GPU 虚拟机的支付方式，但我的汇丰香港万事达借记卡（地址为中国）却无法使用？

回答：

这很可能是因为地区及银行限制，而非 AMD Developer Cloud 本身的问题：

1. **发卡机构限制：** 部分银行（尤其是境外银行）可能会阻止向云服务进行的跨境交易。如果 AMD 的计费系统检测到您的账户位于中国，您的汇丰香港卡可能会被视为国际交易。

2. **账单地址不匹配：** 许多支付网关要求卡的账单地址与账户所在国家一致。由于您的卡是基于香港的，而您的 AMD 账户显示的是中国地址，系统可能会拒绝该卡。

3. **支付网关限制：** 某些服务使用 Stripe 或其他处理器，这些处理器对于接受哪些国家发行的卡有规定。支付宝在中国国内使用，因此易于通过，而国际卡则可能受到限制。

4. **卡类型：** 借记卡在网上国际支付中有时比信用卡受到更多限制，尤其是涉及定期或预付费订阅时。

**解决方法：**

* 使用完全受支持的支付宝。
* 使用中国境内发行的卡（建议信用卡），并确保账单地址匹配。
* 如果您希望使用香港卡，可能需要联系 AMD 支持，了解是否允许跨境计费的例外情况。

参考链接：

* [AMD Developer Cloud 支付方式](https://developer.amd.com/amd-developer-cloud/)
* [Stripe 卡限制](https://stripe.com/docs/payments/cards/payment-methods)
* [支付宝国际接受情况](https://intl.alipay.com/)
