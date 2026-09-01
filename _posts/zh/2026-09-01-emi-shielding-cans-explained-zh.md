---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EMI屏蔽罩详解
translated: true
type: note
---

**问题：** GPU显卡和便利店冰箱控制板上的电路板中，那些钢/金属材质的盾形物体是什么？它们与锂有关吗？

**回答：**

PCB上那些金属"盾牌"形状的物体叫做**EMI屏蔽罩**（也称射频屏蔽罩或屏蔽笼）——它们与锂毫无关系。以下是其作用：

**它们是什么：**
这些金属罩是一种法拉第笼，用于封闭PCB上的电子电路。它们既能限制外部电磁干扰（EMI）辐射影响元件，也能防止内部产生的EMI向外泄露。

**材质构成：**
它们由黄铜、镍银或不锈钢等材料制成的封闭金属罩，与PCB的地线连接。能有效减小环形天线尺寸，并吸收/反射电磁辐射。

**外观设计原因：**
这些极薄的金属板通过焊接固定在PCB上——可在SMT（表面贴装技术）生产线上快速可靠地安装。它们采用标准外形规格，具有特定的焊盘尺寸、高度和形状。

**为何用于冰箱和GPU：**
现代电子设备充满EMI隐患——时钟频率达到千兆赫级，开关稳压器工作在兆赫兹频段，无线射频模块无处不在。PCB内部及周围的电磁噪声极其复杂。若无屏蔽，设备可能无法通过法规测试（FCC、CE、CISPR），出现自干扰，或干扰周围设备。

简而言之：它们是**电磁屏蔽罩**，而非电池或任何锂相关部件。它们保护敏感电路免受无线电/电磁噪声影响——这是现代家电或电脑元件中不可或缺的设计。

**参考来源：**
- [PCB电磁屏蔽最佳实践 – JLCPCB](https://jlcpcb.com/blog/emi-shielding-pcb)
- [屏蔽：在PCB上使用金属屏蔽罩进行EMI屏蔽 – MADPCB](https://madpcb.com/glossary/shield/)
- [EMI基础与板级屏蔽设计 – Interference Technology](https://interferencetechnology.com/emi-basics-and-board-level-shielding-design/)