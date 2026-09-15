---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FR03D热成像相机评测
translated: true
type: note
---

Question: **FeelElec FR03D 热像仪怎么样？**

Answer: **对于电子/PCB 调试来说挺有意思，但具体买哪个版本需要斟酌。**

FR03D 是一款手持热像仪，**热分辨率 240×240**，配备 2.8 英寸显示屏，标称测温范围为 **−20°C 至 550°C**。制造商/卖家将其定位为适用于电气检测、HVAC/泄漏检测和 PCB 维修。([FeelElec][1])

### 用于 PCB 调试

关键选项是：

**FR03D + 微距镜头 → 有意思得多。**

商品页面明确销售用于电路板检测的微距镜头版本。([京东][2])

对于这类需要定位以下问题的场景：

* 短路的电容 / IC
* 异常发热的稳压器
* 电源轨漏电流
* MOSFET 发热
* USB/充电电路故障
* PCB 上的热梯度

热像仪确实很实用。你基本上是在寻找：

```text
正常板卡：
────────────────────────
████████████████████████
        ↑
     大致均匀

故障：
────────────────────────
███████████▓▓▓█████████
             ████
             ████  ← 局部热点
```

关键的是**热分辨率和光学性能**，而不是标称的显示分辨率。240×240 的显示屏并不代表你能远距离分辨出微小的 PCB 元件。

### 一个我持保留态度的方面

根据一个 FR03D 商品页面，其标称测量精度约为 **±2% 或 ±2°C**。([MOLANLM][3])

用于**发现异常**没问题，但不应将其视为实验室级温度测量。

例如，调试 PCB 时看到：

```text
PMIC：       43°C
MOSFET：     47°C
电容：       82°C  ← 可疑
```

这非常有用。

但不要过度解读：

```text
“这个元件刚好是 73.4°C”
```

因为发射率、距离、反射、对焦、气流和测量光斑都会影响结果。

### 价格方面需要谨慎

我找到一个 FR03D 的售价大约在 **$150**，而当前 256×192 传感器的替代品也多在 $200–400 区间。([MOLANLM][3])

例如：

### [Elitech TIC-210 256×192](https://www.elitecheu.com/products/elitech-tic-210-handheld-thermal-imaging-camera?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=55727850324355&utm_source=chatgpt.com)

*$351.71*

### [Teslong M2 Pro 256×192](https://www.bestbuy.com/product/teslong-m2-pro-256x192-infrared-therrmal-handheld-camera-black-dark-grey-orange/J3Q5Q9HLT5/sku/12836658?fs=tl923b&utm_medium=feed&utm_source=chatgpt.com)

*$479.99*

### [Thermal Master P3 PCB 热像仪](https://dryitcenter.com/products/thermal-master-p3-pcb-thermal-camera?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=52935824506991&utm_source=chatgpt.com)

*$299.99*

### [Foxwell RT280 PRO](https://www.foxwelldiag.com/products/foxwell-rt280-pro?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=51680873742618&utm_source=chatgpt.com)

*$312.00*

如果你的主要用途是 **PCB 维修**，我实际上更关注**微距镜头 / 最近对焦距离 / IFOV**，而不是标称分辨率。

**我的看法：**

| 用途               | FR03D                           |
| ------------------ | ------------------------------- |
| 查找发热的 IC      | ✅ 不错                          |
| 电源电子           | ✅ 不错                          |
| HVAC / 管道泄漏    | ✅ 不错                          |
| 一般家庭检测       | ✅ 不错                          |
| PCB 维修           | **✅ + 微距镜头**                |
| 手机 PCB 微小元件  | ⚠️ 需仔细检查微距光学性能        |
| 精确绝对温度测量   | ⚠️ 不是强项                     |
| 专业计量           | ❌ 我会升级选择                  |

如果你是专门为**电子调试**购买，我会选择 **FR03D + 微距镜头**，而不是普通版 FR03D。

我还可以专门对比 **FR03D vs FR03E vs FE20 vs Thermal Master P3** 在 PCB/手机主板调试方面的表现，并告诉你我会买哪一款。

[1]: https://feelelec.cn/index.php?a=index&aid=129&c=View&m=home&utm_source=chatgpt.com "FR03D高精度手持测温漏水维修探测器电路检测热像仪_郑州丰易智能科技有限公司"
[2]: https://www.jd.com/jiage/1318acd383dc60cb3192.html?utm_source=chatgpt.com "红外热像仪探测器价格报价行情 - 京东"
[3]: https://www.molanlm.com/products/high-definition-lcd-screen-with-240-240-resolution-feelelec-fr03d-handheld-infrared-thermal-imager?utm_source=chatgpt.com "(High-definition LCD screen with 240*240 resolution) FeelElec FR03D Handheld Infrared Thermal Imager"