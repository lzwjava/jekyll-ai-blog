---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试航嘉电源
translated: true
type: note
---

**问题：** 我有一个 Huntkey 航嘉 睿智 300S PSU，并且我有电源连接器（24-pin ATX）。如何测试这个 PSU 是否正常工作？

**回答：**

睿智 300S 是一款入门级 ATX PSU（额定功率约 200W）。既然你已经有了连接器，可以使用经典的 **Paperclip / Jumper 测试** 来进行检测。方法如下：

---

### ⚠️ 安全第一

- 通电时切勿触碰任何裸露的引脚。
- 不要无人看管已短接的 PSU。
- 在插入或取出回形针之前，务必先拔掉交流电源线。

---

### 方法 1 — Paperclip 测试（基础、免费）

这是检查 PSU 是否能够正常启动的最简单方法。---

### 方法 2 — PSU 测试仪（更全面，约 $12–20 美元）

专用 PSU 测试仪可以自动完成 Paperclip 测试，并在 LCD 屏幕上快速显示各电压轨的读数。入门级 LCD 型号价格约为 $12–20 美元。只需将 24-pin 连接器插入测试仪并通电——它会一次性检查所有电压轨（+12V、+5V、+3.3V）。

---

### 方法 3 — 万用表（最准确）

如果风扇转动但你仍想验证电压输出，请使用设置为直流电压档的万用表。测量输出连接器（例如 Molex 或 SATA 电源插头）与地线（黑色线）之间的电压。预期值如下：

| 电压轨 | 线色    | 预期电压          |
|--------|---------|-------------------|
| +12V   | 黄色    | 11.4V – 12.6V     |
| +5V    | 红色    | 4.75V – 5.25V     |
| +3.3V  | 橙色    | 3.14V – 3.47V     |

---

### 快速总结

| 测试方式      | 成本        | 能告诉你什么                     |
|---------------|-------------|----------------------------------|
| Paperclip     | 免费        | 能否正常启动？                   |
| PSU 测试仪    | 约 $15 美元 | 所有电压轨是否都存在？           |
| 万用表        | 约 $15–30 美元 | 电压是否在规格范围内？         |

如果 Paperclip 测试后没有任何风扇启动，则 PSU 有故障。如果风扇转动，PSU 仍有可能损坏，但更有可能是系统中的其他组件出现了问题。

---

**参考来源：**

- [NZXT：测试你的 PSU（Paperclip 测试）](https://support.nzxt.com/hc/en-us/articles/1260802863490-Testing-your-Power-Supply-Unit-Paperclip-Test)
- [Corsair：如何测试 PSU](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/how-to-test-a-psu-power-supply-unit/)
- [Tech-Insider：如何测试电源（2026）](https://tech-insider.org/how-to-test-a-power-supply-2026/)
- [Huntkey 睿智 300S 产品页面](https://www.huntkey.cn/product/product_id=452.html)
