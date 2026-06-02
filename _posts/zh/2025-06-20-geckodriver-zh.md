---
audio: false
generated: true
lang: zh
layout: post
title: Selenium GeckoDriver Ubuntu 安装指南
translated: true
type: note
---

在 Ubuntu 系统上安装 Selenium Firefox 驱动（geckodriver）的步骤如下：

1. **安装 Firefox**（如未安装）：

   ```bash
   sudo apt update
   sudo apt install firefox
   ```

2. **下载 geckodriver**：
   - 访问 [geckodriver 发布页面](https://github.com/mozilla/geckodriver/releases)
   - 选择与你的 Firefox 版本兼容的最新版本。对于 Ubuntu，请下载 Linux 64 位版本（例如 `geckodriver-vX.XX.X-linux64.tar.gz`）
   - 下载命令示例（请将 `X.XX.X` 替换为最新版本号）：

     ```bash
     wget https://github.com/mozilla/geckodriver/releases/download/vX.XX.X/geckodriver-vX.XX.X-linux64.tar.gz
     ```

3. **解压下载的文件**：

   ```bash
   tar -xvzf geckodriver-vX.XX.X-linux64.tar.gz
   ```

4. **将 geckodriver 移动到系统路径**：
   - 将解压后的 `geckodriver` 移动到 `/usr/local/bin` 目录以实现全局访问：

     ```bash
     sudo mv geckodriver /usr/local/bin/
     ```

   - 赋予可执行权限：

     ```bash
     sudo chmod +x /usr/local/bin/geckodriver
     ```

5. **安装 Python 版 Selenium**（如使用 Python）：

   ```bash
   pip install selenium
   ```

6. **验证安装**：
   - 检查 geckodriver 版本：

     ```bash
     geckodriver --version
     ```

   - 使用简单 Python 脚本测试：

     ```python
     from selenium import webdriver

     driver = webdriver.Firefox()
     driver.get("https://www.example.com")
     print(driver.title)
     driver.quit()
     ```

**注意事项**：

- 请确保 Firefox 版本与 geckodriver 版本兼容（可查阅 geckodriver GitHub 页面的发布说明）
- 如遇问题，请确认已安装 `python3-pip`：

  ```bash
  sudo apt install python3-pip
  ```

- 如果系统找不到 geckodriver，请将 `/usr/local/bin` 添加到 `PATH` 环境变量：

  ```bash
  export PATH=$PATH:/usr/local/bin
  ```

按照以上步骤即可在 Ubuntu 上完成 Selenium Firefox 驱动的安装。如遇任何问题欢迎反馈！

---

`geckodriver-v0.36.0-linux-aarch64.tar.gz` 与 `geckodriver-v0.36.0-linux64.tar.gz` 的区别在于目标 CPU 架构：

- **linux-aarch64**：适用于 64 位 ARM 架构（如 ARMv8-A），常见于树莓派、某些服务器或基于 ARM 的现代 Linux 系统。"aarch64" 代表 64 位 ARM 架构

- **linux64**：适用于 64 位 x86 架构（也称为 x86_64 或 AMD64），这是大多数桌面电脑和服务器 PC 运行 Linux 的标准架构

**选择要点**：

- 若系统采用 64 位 ARM 处理器，请选择 `linux-aarch64`
- 若系统采用 64 位 x86 处理器，请选择 `linux64`
- 在 Linux 系统中可通过运行 `uname -m` 命令查看架构：若输出 `aarch64` 则使用 ARM 版本，若输出 `x86_64` 则使用 linux64 版本

`.asc` 文件是用于验证对应 `.tar.gz` 文件完整性和真实性的 GPG 签名文件。
