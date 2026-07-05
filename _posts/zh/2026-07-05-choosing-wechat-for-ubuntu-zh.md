---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 选择Ubuntu版微信
translated: true
type: note
---

**问题：** 在Ubuntu上应该选择哪个Linux版微信安装包？

**回答：**

如果你使用的是运行Ubuntu的普通PC（Intel或AMD CPU），请选择：

* ✅ **X86 → `.deb`**（`WeChatLinux_x86_64.deb`）

这是Ubuntu及其他基于Debian的发行版的原生安装包格式。

### 你应该选择哪个？

| 你的系统                                                                           | 选择             |
| ---------------------------------------------------------------------------------- | ---------------- |
| Intel/AMD架构的Ubuntu（大多数笔记本电脑/台式机，例如Core i9、Ryzen）               | ✅ **X86 `.deb`** |
| ARM架构的Ubuntu（例如树莓派、运行Linux的Apple M系列、骁龙X Elite）                 | ✅ **ARM `.deb`** |
| Fedora、RHEL、Rocky、CentOS、openSUSE                                              | `.rpm`           |
| 任何Linux发行版（便携版，无需安装）                                                | `AppImage`       |
| 龙芯CPU                                                                            | `LoongArch .deb` |

### 针对你的电脑

根据我们之前的对话，你的机器配备的是**Intel Core i9-13900KF**和**RTX 4070**，因此你应该下载：

> **X86 → `WeChatLinux_x86_64.deb`**

### 安装方法

下载后：

```bash
cd ~/Downloads
sudo apt install ./WeChatLinux_x86_64.deb
```

或

```bash
sudo dpkg -i WeChatLinux_x86_64.deb
sudo apt --fix-broken install
```

第一个命令（`apt install ./...`）通常更推荐，因为它会自动安装所需的依赖包。

### 是否应该使用AppImage版本？

对于Ubuntu，我推荐使用**`.deb`**，因为：

* ✅ 与系统菜单集成
* ✅ 更易于更新和卸载
* ✅ 更好的桌面集成
* ✅ Ubuntu的标准安装方式

仅在以下情况下使用**AppImage**：

* 你没有管理员（`sudo`）权限，
* 你需要一个完全便携的副本，
* 或者你使用的Linux发行版不支持`.deb`或`.rpm`。

因此，对于你搭载i9-13900KF的Ubuntu桌面，**请下载X86架构的`.deb`安装包**。