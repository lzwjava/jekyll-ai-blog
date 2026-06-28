---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux触控板与macOS不同
translated: true
type: note
---

问题：在运行 Fedora 的 2017 款 MacBook Pro 上，触控板表现真的还不错吗？它使用的驱动程序和 macOS 上一样吗？

答案：

不——这是一个常见误解。2017 款 MacBook Pro 在 Fedora（或任何 Linux 系统）下，触控板并**不**使用与 macOS 相同的驱动程序，且开箱即用的体验明显更差。

根据具体型号的不同，存在两种截然不同的硬件路径：

**1. 非触控栏 13 英寸机型（"MacBookPro14,1"）** —— 使用更传统的 Apple 触控板，通过 Linux 内核中的标准 `bcm5974` USB 驱动访问。此型号表现尚可：多点触控、轻点点击、双指滚动都能正常工作。虽未达到 macOS 水平，但可用。

**2. 触控栏机型（MacBookPro14,2 / 14,3）** —— 触控板和键盘位于 Apple T1 芯片之后，通过 SPI 接口（而非标准 USB）通信。这类机型需要内核树外的 `applespi` 驱动。在其部分代码进入主线内核（5.x 版本左右的 `apple-ibridge` / `applespi`）之前，历史上必须通过 `macbook12-spi-driver` DKMS 模块加载。缺少该驱动时，全新安装的 Fedora 可能完全无法使用触控板和键盘。

为何驱动原理与 macOS 存在根本性差异：

- macOS 使用苹果专有的手势识别引擎，即闭源用户态堆栈（`AppleMultitouchTrackpad`）。内核仅提供原始多点触控接触数据；所有“手感”——动量滚动、手掌误触抑制调校、手势加速度曲线——均存在于该闭源堆栈中。
- Linux 通过 `bcm5974`/`applespi` 获取原始接触数据，并将其传递给 **libinput**。libinput 自行处理手势、手掌误触和滚动，效果虽好但方式不同。所以硬件相同，但其上的整个处理层是完全独立的开源重新实现。

总结：滚动和基本手势表现尚可，但你会发现手掌误触抑制效果缺失或更粗糙，缺乏触觉 Force Touch 反馈（Taptic Engine 未被驱动），三指/四指手势需要手动配置（例如 `libinput-gestures` 或 `fusuma`）。对非触控栏机型而言，“还不错”的说法是合理的；但对任何机型来说，“和 macOS 一样好”都不准确。

如果你想检查具体设备绑定的情况：

```bash
# 查看当前输入设备和驱动
sudo libinput list-devices | grep -A6 -i trackpad

# 识别型号
cat /sys/devices/virtual/dmi/id/product_name   # 例如 MacBookPro14,3

# 检查 applespi/bcm5974 是否已加载
lsmod | grep -E 'applespi|bcm5974|apple_ib'

# 实时调整 libinput 行为（轻点点击、自然滚动）
gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true
gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll true
```

因此：驱动不同，质量也不同——但在 2017 款非触控栏 13 英寸机型上，日常使用确实足够好用。
