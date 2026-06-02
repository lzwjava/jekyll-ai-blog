---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何跳过Camosfox安装
translated: true
type: note
---

是的，你可以在首次运行 `./install.sh` 时安全地跳过或延迟安装 **Camosfox**（也称为 **Camofox**）。主脚本**不会**自动安装它。

### 快速摘要
- `install.sh` 脚本会安装：
  - Python 依赖（包括通过 Playwright 安装的浏览器工具）
  - Node.js + npm 依赖
  - **本地 Chromium**（通过 `npx playwright install chromium --with-deps`）
- **Camosfox / Camofox** 是一个**可选的高级隐身浏览器**（一个自托管的 Node.js 包装器，封装了 **Camoufox** —— 一个具有强大指纹欺骗/反检测功能的 Firefox 分支）。它**不属于**默认安装内容。

你提到填写了虚假位置，并且可以跳过一些浏览器设置 —— 这与 Hermes Agent 中隐身浏览的设置相符。

### 能否在运行 install.sh 时跳过它？
**是的，完全可以。**
脚本没有强制安装 Camosfox 的选项。你可以正常运行安装程序（或使用 `--skip-setup` 来跳过向导）：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

或者带选项运行：
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --skip-setup
```

安装完成后，你可以稍后再决定是否设置 Camosfox。

### 如何手动设置 Camosfox (Camofox)（建议用于隐身用途）

1. **安装 Camosfox**（在 Hermes 安装完成后）：
   ```bash
   git clone https://github.com/jo-inc/camofox-browser.git
   cd camofox-browser
   npm install
   npm start
   ```
   - 首次运行将下载 **Camoufox**（约 300MB）。
   - 它将运行一个本地服务器（默认端口 9377）。

   替代方案（更简单，使用 Docker）：
   ```bash
   docker run -d --network host -e CAMOFOX_PORT=9377 jo-inc/camofox-browser
   ```

2. **配置 Hermes 以使用它**：
   编辑你的配置文件：
   ```bash
   nano ~/.hermes/.env
   ```

   添加或修改以下行：
   ```
   BROWSER_BACKEND=camofox
   CAMOFOX_URL=http://localhost:9377
   # 如果使用 Docker/远程：http://127.0.0.1:9377
   ```

   你还可以根据需要（或让 Hermes 处理）在 Camosfox/Camoufox 设置中配置虚假位置、用户代理欺骗等。

3. **测试它**：
   运行 Hermes 并让它访问一个通常屏蔽机器人的网站：
   ```
   hermes
   ```
   然后输入类似：“访问 example.com 并告诉我主要内容”，或者使用浏览器工具。

### 如果你不想使用 Camosfox 的替代方案
- **默认方案**：Hermes 使用**本地 Chromium**（通过 Playwright）—— 脚本已安装。适用于大多数任务，但更容易被检测到。
- **云选项**：你可以配置外部服务，如 Browser Use，以获得更好的隐身效果（无需本地安装）。

### 针对全新 Linux 设置的提示
- 你已经填写了虚假位置 —— 这对隐私/隐身很有用。Camosfox 通过 C++ 级别的指纹欺骗使其更加强大。
- 如果你在安装期间想完全避免 Node.js/浏览器相关组件，脚本仍然可以正常工作（只是在你完成设置之前，浏览器功能将不可用）。
- 安装后，运行 `hermes setup` 来配置 API 密钥和其他设置。
- 后续更新请运行：`hermes update`

如果你在安装过程中遇到任何错误（例如缺少依赖项或 Node 问题），请将确切的错误信息粘贴到这里，我会帮助你调试。

你分享的脚本看起来是正确的，并且与 Nous Research 官方的 Hermes Agent 保持同步。所提供的代码中，在跳过可选隐身浏览器方面没有重大问题。

参考：
- https://github.com/NousResearch/hermes-agent
- https://hermes-agent.nousresearch.com/docs/user-guide/features/browser (Camofox 设置指南)
- https://github.com/jo-inc/camofox-browser
