---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RAYTHINK CX200S与EX100在PCB应用中的对比
translated: true
type: note
---

问题：**我应该购买RAYTHINK睿创燧石热像仪而不是FeelElec FR03D吗？**

答案：**是的——但前提是你看的RAYTHINK型号是CX200S / CX200S Ultra。** 如果商品实际上是最便宜的**EX100**，我会选择**FR03D + 微距镜头**用于PCB检测工作。

你粘贴的标题太笼统，无法确定具体的RAYTHINK型号。RAYTHINK有多款手持热像仪，传感器差异很大。

### 针对你的使用场景，我的排名

假设你的主要用途是**电子/PCB故障排查**：

|                    | FeelElec FR03D | RAYTHINK EX100 | RAYTHINK CX200S |
| ------------------ | -------------: | -------------: | --------------: |
| 原生红外分辨率     |       240×240* |    **160×120** |     **256×192** |
| NETD               |          ~40mK |           40mK |    更优等级     |
| 对焦               |  固定/可变     |          固定  |   更优光学系统  |
| PCB检测            |            ⭐⭐⭐ |             ⭐⭐ |        **⭐⭐⭐⭐** |
| 常规巡检           |           ⭐⭐⭐⭐ |            ⭐⭐⭐ |       **⭐⭐⭐⭐⭐** |
| 做工/生态         |       预算级    |          良好  | **更好**        |

*注意电商平台上的商品信息：“240×240”有时可能指的是显示屏或超分辨率，而非原生探测器分辨率。

RAYTHINK官方EX100的规格实际上是**160×120原生分辨率**、40mK、4.62 mrad IFOV（瞬时视场角），最小成像距离为11厘米。（[Raythink Tech][1]）

其较新的**CX200S**使用**256×192探测器**，AI超分辨率可达512×384。RAYTHINK明确将电子维修列为使用场景。（[Raythink Tech][2]）

### 我为什么更倾向于CX200S

对于PCB故障排查，这一点非常重要：

```text
原生像素
      ↓
空间分辨率
      ↓
我能否区分元器件A和元器件B？
      ↓
我能否定位到实际失效的元器件？
```

256×192传感器拥有**49,152个原生热成像像素**。

160×120只有：

```text
19,200
```

也就是少了约**2.56倍的热成像像素**。

AI超分辨率并不能创造缺失的热成像信息。所以：

```text
160×120 → AI → 320×240
```

并不会等同于真正的320×240探测器。

这就是为什么我会优先考虑**原生探测器分辨率 + IFOV + 光学系统**。

### 但还有一个更重要的点

对于你的特定使用场景，**一旦你面对的是微小的贴片元件（SMD），微距能力几乎比其他任何因素都重要**。

RAYTHINK高端型号RT630就是一个很好的例子：其官方文档明确标注了专用微距光学系统，可达到**每像素30–60 µm**，最小成像距离为19–39毫米。（[Raythink Tech][3]）

正是这种光学系统让热成像变得真正有价值，适用于：

```text
手机PCB
    ↓
电源管理IC（PMIC）
    ↓
0.5毫米电容
    ↓
找到精确的发热元件
```

一台没有良好近焦光学系统的普通256×192热像仪在这里仍然会令人失望。

## 我会买什么

**如果RAYTHINK商品是CX200S：**
→ **购买RAYTHINK CX200S。**

### [Raythink CX200S 手持式红外热像测温仪](https://openelab.io/products/raythink-cx200s-handheld-thermal-imaging?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45715511181510&utm_source=chatgpt.com)

*$464.00美元*

**如果是EX100：**
→ **我会选择FR03D + 微距镜头**，假设价格相近。

**如果你的预算在400–700美元左右：**
→ 我会跳过这两款，寻找一款**原生256×192或384×288分辨率、带手动对焦 + 微距/近焦能力**的设备。这才是板级维修体验明显提升的起点。

如果你把**RAYTHINK的商品截图或确切型号 + 价格**发给我，我可以直接告诉你**“买这个/别买这个”**，而不是猜测商品是哪一个RAYTHINK型号。

参考链接：

* [RAYTHINK官方EX100规格](https://raythink-tech.cn/index.php?c=show&id=448&utm_source=chatgpt.com)
* [RAYTHINK官方CX200S信息](https://www.raythink-tech.cn/index.php?c=show&id=527&utm_source=chatgpt.com)
* [RAYTHINK官方RT630规格](https://www.raythink-tech.cn/index.php?c=show&id=48&utm_source=chatgpt.com)

[1]: https://raythink-tech.cn/index.php?c=show&id=448&utm_source=chatgpt.com "EX100_手持测温热像仪_温度检测_工业监测_产品中心_燧石技术（烟台）有限公司"
[2]: https://www.raythink-tech.cn/index.php?c=show&id=527&utm_source=chatgpt.com "Raythink睿创燧石CX200S系列手持红外热像仪荣获2026国际CMF最佳CMF设计奖！_资讯中心_关于我们_燧石技术（烟台）有限公司"
[3]: https://www.raythink-tech.cn/index.php?c=show&id=48&utm_source=chatgpt.com "RT630_手持测温热像仪_温度检测_工业监测_产品中心_燧石技术（烟台）有限公司"