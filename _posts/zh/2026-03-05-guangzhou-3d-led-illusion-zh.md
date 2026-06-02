---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 广州3D LED幻影秘密
translated: true
type: note
---

**问题**：中国天河仁丰大厦上的大型3D效果屏幕是如何实现的，广告有时显示像大象这样的动物从大楼中走出来？播放这些广告使用什么软件？是OBS吗？

**回答**：

中国广州天河区仁丰大厦（Renfeng Building，仁丰大厦）上的大型屏幕是一个覆盖约1,403平方米的巨型户外**naked-eye 3D LED display**。它于2022年左右升级支持惊人的naked-eye 3D效果，成为天河路商圈的标志性“屏王”之一。

这些引人入胜的3D效果——动物（如大象）、飞船、熊猫、龙、机械手或其他物体似乎从大楼中爆出或跃出的场景——**并非真正的全息投影**，而是通过以下方式创建的光学错觉：

- **屏幕结构**：显示屏通常采用L形、弯曲或直角（90°）配置，包裹大楼的转角或立面。这种物理曲面是深度错觉的关键。
- **内容设计**：视频使用3D动画软件（如Blender、Cinema 4D、Maya或带插件的After Effects）专门制作。创作者应用变形映射和透视技巧，使物体在特定角度（通常为主行人/观赏方向）观看时似乎延伸到屏幕平面之外。
- **Naked-eye 3D原理**：它依赖**binocular disparity**和motion parallax。由于屏幕布局的角度/曲面，每个眼睛看到略微不同的透视，脑部将它们组合成强烈的深度和凸出感——无需眼镜。高分辨率LED模块（如P6或更精细）和精确对齐提升真实感。

这种技术从2020–2022年起在中国非常流行，著名案例包括成都（如太古里IFS屏幕上的巨型熊猫或老虎跃出）、上海和广州（包括仁丰大厦以及附近的广州设计城或新大新百货）。

对于播放，使用专业的**media server systems**和专用播放软件，而不是像OBS Studio这样的消费级工具（OBS主要用于直播流，且缺乏对巨型不规则LED墙的扭曲/映射3D内容的稳健支持）。

中国这些大型naked-eye 3D设置常见的专业解决方案包括：

- NovaStar（LED控制中非常广泛使用；其Taurus/VX系列媒体播放器 + V-Can或NovaLCT软件处理调度、扭曲和高比特率4K/8K播放）。
- Colorlight、Linsn或Huidu系统的发送卡和接收卡。
- 专用的3D播放软件，如：
  - Disguise (d3)
  - Notch
  - TouchDesigner
  - 来自Resolume等公司的自定义媒体服务器（巨型户外屏幕较少见）
  - 中国平台如LEDshowT、ViPlex，或集成商的专有系统（如Yaham、Unit LED或RAVLED）

这些系统支持内容映射到非矩形/曲面、多个部分的同步、亮度/颜色校准以及定时广告轮播。3D内容预渲染为常规2D视频文件，但针对确切的观赏透视设计，因此从街上的指定位置“弹出”正确。

简而言之：魔力主要来自巧妙的内容创作 + 倾斜屏幕几何，通过专业的LED媒体服务器和控制软件播放——远比OBS更先进和可靠。

**参考资料**：

- [https://www.yaham.com/guangzhou-led-display-king-was-born-naked-eye-3d-big-screen-debut.html](https://www.yaham.com/guangzhou-led-display-king-was-born-naked-eye-3d-big-screen-debut.html)
- [https://www.unit-led.com/3d-billboard-china](https://www.unit-led.com/3d-billboard-china)
- [https://www.doitvision.com/outdoor-naked-eye-3d-screens](https://www.doitvision.com/outdoor-naked-eye-3d-screens)
- [https://ledscreenfactory.com/3d-led-display-complete-guide](https://ledscreenfactory.com/3d-led-display-complete-guide)
