---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 进入MSI BIOS并禁用安全启动
translated: true
type: note
---

## MSI MAG B760M Mortar — Enter BIOS

**按键：DEL (Delete)**

具体操作步骤如下：

1. **完全关闭**电脑（或重新启动）
2. **按下电源按钮**
3. **立即开始反复敲击 DEL 键** — 每秒一次，不要长按
4. 你将看到 MSI Click BIOS 界面

> 注意：在 MSI 主板上，POST 期间通常会在屏幕底部显示 "Press DEL to enter BIOS Setup"。如果错过了，只需重新启动并重试——提早一点开始敲击。

---

## 进入 BIOS 后 → Disable Secure Boot

在 B760M Mortar 上的菜单路径：

1. **Settings**（或者如果可见，**Security** 选项卡——旧版 MSI BIOS 在此处；在 Click BIOS 5 中位于 **Settings** 下）
2. → **Security**
3. → **Secure Boot**
4. → 设置为 **Disabled**
5. 按 **F10** → **Yes** 以 Save & Exit

某些 MSI BIOS 版本上的替代路径：

- **Boot** → **Secure Boot** → **Disabled**

---

## 如果你使用的是新版 MSI Click BIOS（UEFI/GUI 风格）

寻找 **Settings** 图标（顶部或侧面的齿轮图标），然后：

- **Security** → **Secure Boot** → **Disabled**

---

重启一次后，`nvidia-smi` 即可正常工作。如果进入 BIOS 后找不到 Secure Boot 选项，请告诉我——我可以查找这块主板的精确菜单截图。
