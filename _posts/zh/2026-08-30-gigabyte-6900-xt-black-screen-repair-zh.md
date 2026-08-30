---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 技嘉6900 XT黑屏修复
translated: true
type: note
---

问题：YouTube视频《Gigabyte 6900 XT Graphics Card Repair - Black Screen》中讲解的内容和修复过程是什么？

答案：
本视频来自**NorthridgeFix**，演示了对一块**Gigabyte Radeon RX 6900 XT**显卡的诊断与修复过程，该显卡能够开机但无法显示图像（黑屏问题）。

### 修复过程的关键步骤

1. **初始电源轨与短路检查：**
* 技术人员使用二极管模式（电压降测试）测量12V电源输入线和3.3V线是否存在短路 [[01:08](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D68)]。
* 所有电源线的电压降读数约为0.45V - 0.47V，确认主电源轨上没有短路 [[01:32](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D92)]。

2. **显微镜下目视检查：**
* 对PCB两面进行彻底目视检查，查看是否有烧毁元件、液体损坏或物理损伤 [[02:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D135)]。
* 使用异丙醇和防静电钢丝刷清理微小的表面腐蚀 [[05:08](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D308)]。

3. **确定根本原因：**
* 检查PCIe接口边缘靠近底部插槽处，发现一个位于PCIe数据线上的小型表面贴装耦合电容物理损坏，从焊盘上脱落 [[09:00](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D540)]。
* 数据线电容缺失或断裂会阻止与主板的正常通信，导致黑屏输出 [[09:23](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D563)]。

4. **元件修复与PCB掩膜：**
* 涂抹助焊剂并施加新焊锡，将松脱的电容重新焊接到其铜迹焊盘上 [[10:06](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D606)]。
* 使用万用表确认电容到PCIe插槽触点的连通性 [[11:04](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D664)]。
* 在元件周围涂抹UV焊料掩膜（用UV灯固化），以加固脆弱/薄弱的焊盘，防止未来再次脱落 [[13:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D795)]。

5. **测试与验证：**
* 将显卡安装到测试平台系统中，连接12V PCIe电源和HDMI [[15:02](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D902)]。
* 开机后，显卡成功自检并向显示器输出有效的显示信号 [[15:52](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvzsPSHN6uCo%26t%3D952)]。

参考资料：

* [Gigabyte 6900 XT Graphics Card Repair - Black Screen](http://www.youtube.com/watch?v=vzsPSHN6uCo)