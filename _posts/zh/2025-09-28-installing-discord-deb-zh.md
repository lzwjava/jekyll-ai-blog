---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: Discord DEB文件安装方法
translated: true
type: note
---

要安装 `discord-0.0.111.deb` 文件，您可以使用以下几种方法：

**方法一：使用 dpkg（命令行）**
```bash
sudo dpkg -i discord-0.0.111.deb
```

若遇到依赖性问题，请运行：
```bash
sudo apt-get install -f
```

**方法二：使用 apt（推荐）**
```bash
sudo apt install ./discord-0.0.111.deb
```

此方法比 dpkg 能更好地自动处理依赖关系。

**方法三：使用 gdebi（如已安装）**
```bash
sudo gdebi discord-0.0.111.deb
```

**方法四：图形界面方式**
若使用桌面环境，通常可直接双击 .deb 文件，系统会通过软件包管理器（如软件中心）打开并完成安装。

**前提条件：**
- 请确保当前位于包含 .deb 文件的目录
- 需要拥有 sudo 权限
- 若尚未获取该文件，可从 Discord 官网下载

**安装完成后：**
您可通过应用程序菜单启动 Discord，或在终端中运行 `discord` 命令启动。

您更倾向于使用哪种方法？是否需要某个具体步骤的协助？
