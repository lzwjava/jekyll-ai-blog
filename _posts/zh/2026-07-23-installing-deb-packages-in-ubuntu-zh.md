---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu中安装.deb软件包
translated: true
type: note
---

在 Ubuntu 中安装 `.deb` 包有几种方法。

### 方法一：使用 `apt`（推荐）

打开终端，导航到包含 `.deb` 文件的文件夹，然后运行：

```bash
sudo apt install ./package_name.deb
```

示例：

```bash
sudo apt install ./google-chrome-stable_current_amd64.deb
```

推荐使用 `apt`，因为它会自动安装所需的依赖项。

---

### 方法二：使用 `dpkg`

使用以下命令安装包：

```bash
sudo dpkg -i package_name.deb
```

如果缺少依赖项，请使用以下命令修复：

```bash
sudo apt --fix-broken install
```

---

### 方法三：使用图形界面

1. 双击 `.deb` 文件。
2. 它将在 Ubuntu 的软件中心（或其他包安装器）中打开。
3. 点击 **安装**。
4. 在提示时输入密码。

---

### 验证安装

要检查包是否已安装，请运行：

```bash
dpkg -l | grep package_name
```

或者，如果它是一个命令行应用程序：

```bash
package_name --version
```

如果你在安装特定 `.deb` 文件时遇到问题，请告诉我：

* 你的 Ubuntu 版本（`lsb_release -a`）
* `.deb` 文件的名称
* 你收到的任何错误消息