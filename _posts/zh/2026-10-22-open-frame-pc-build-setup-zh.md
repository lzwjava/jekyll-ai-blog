---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开放式PC装机设置
translated: true
type: note
---

**问题：** 如何使用开放式机架（open rack / test bench）来固定 PC 组件（如主板）而不是传统机箱？

---

**答案：**

**开放式机架**（open-frame rack，也称为 open-frame chassis 或 test bench）的内部工作原理与普通机箱相同——只是去掉了外壳。以下是设置步骤：

---

### 1. 选择合适的开放式机架

确保它支持你的 **motherboard form factor**（主板规格）：

- ATX、Micro-ATX、Mini-ITX——大多数开放式机架会列出它们支持的类型
- 热门品牌：Thermaltake Core P 系列、Lian Li（垂直）、ASUS ROG Hyperion、TT A500

---

### 2. 安装主板

- 机架上有 **预钻孔的 standoff holes**（支撑柱孔），与 ATX/mATX/ITX 布局匹配
- 首先拧入 **brass standoffs**（铜支撑柱），然后将主板放在上面并拧紧螺丝
- 这与在普通机箱中安装完全相同——支撑柱可防止电气短路

---

### 3. 安装电源 (PSU)

- 大多数开放式机架都有 **专用的 PSU bracket**（电源支架，通常位于底部或背面）
- 用 4 颗螺丝固定，就像标准机箱一样

---

### 4. 安装 GPU

- 将 GPU 插入主板的 **PCIe x16 插槽**
- 许多开放式机架同时支持 **水平**（传统）和 **垂直**（展示）安装 GPU
- 垂直安装需要使用 riser cable（PCIe 延长线）

---

### 5. 安装存储设备 (SSD / HDD)

- 机架通常有 **drive trays 或 brackets**（硬盘托盘或支架），带有螺丝孔
- M.2 SSD 直接安装在主板上
- 2.5 英寸/3.5 英寸硬盘可以用 zip tie（扎带）固定或螺丝固定在机架的支架上

---

### 6. CPU 散热器

- 空气散热器或 AIO 液体散热器均可——开放式机架通常侧面或顶部有 **radiator mounting points**（散热器安装点）
- 气流通常优于封闭式机箱

---

### 7. 布线管理

- 使用 **zip ties**（扎带）或 Velcro straps（尼龙粘带）——电缆完全暴露，因此可以整洁布线
- 如果有 back channel（后端通道），可以将电缆绕到机架面板后面

---

### 关键提示与注意事项

| 主题 | 备注 |
| --- | --- |
| **灰尘** | 开放式机架更容易积尘——需要更频繁地清洁 |
| **接地** | 在接触组件前触摸金属部分（没有机箱接地） |
| **ESD** | 由于没有金属外壳，请使用 anti-static mat/wristband（静电防护垫/腕带） |
| **短路** | 不要让松动的螺丝或金属接触主板 |
| **宠物/儿童** | 旋转风扇和裸露的 PCB 容易接触到——请远离 |
| **气流** | 很好；适合超频或高功耗配置 |

---

### 常见用途

- **Test benches**（测试平台）——无需拆卸机箱面板即可轻松更换组件
- **Showcase builds**（展示性构建）——展示 RGB / 水冷
- **Enthusiast overclocking**（超频爱好者）——最大散热空间

---

**参考文献：**

- [Thermaltake Core P3 Open Frame Chassis Overview](https://www.thermaltake.com/core-p3-tempered-glass-edition.html)
- [How to Build a PC on an Open Test Bench — Linus Tech Tips](https://www.youtube.com/results?search_query=open+frame+pc+build+test+bench)
- [PC Part Picker: Open Air Cases](https://pcpartpicker.com/products/case/#t=10)
