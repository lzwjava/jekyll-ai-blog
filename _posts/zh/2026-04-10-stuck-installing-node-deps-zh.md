---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装Node.js依赖包时卡住了
translated: true
type: note
---

问题：为什么 Hermes Agent 安装程序在 macOS 上完成先前步骤后卡在"安装 Node.js 依赖项（浏览器工具）"？

答案：

安装程序目前卡在 **Node.js 依赖项** 这一步，因为它正在克隆的仓库 `/Users/lzwjava/.hermes/hermes-agent` 中运行 `npm install`（用于浏览器自动化工具和 WhatsApp 桥接），而这个 `npm install` 命令正处于挂起状态。

这是 macOS（以及其他平台）上 `npm install` 非常常见的问题。脚本很可能执行类似 `cd /Users/lzwjava/.hermes/hermes-agent && npm install` 的操作（通常带有 `--silent` 或不显示详细输出），所以你看到没有进度，感觉像是卡住了。

### 最常见的原因：
- **网络 / npm 注册表超时或连接缓慢** — npm 正尝试从默认注册表 (`registry.npmjs.org`) 下载包，但遇到了停滞。
- **依赖项下载量过大** — Playwright（用于浏览器工具）会下载 Chromium 和其他二进制文件，在慢速或不稳定的连接上可能需要很长时间或出现挂起。
- **npm 缓存或锁定文件问题**。
- **代理、VPN 或防火墙干扰**了 npm 的网络请求。
- **Node.js/npm 版本在 macOS 上的特殊问题**（你的 Node.js 版本是 v25.3.0，这比较新；有时最新的版本会暂时出现兼容性问题）。

### 如何立即解决：

1. **取消当前安装**
   按 **Ctrl + C**（如果需要，多次按）来停止安装程序。

2. **进入项目文件夹**
   ```bash
   cd /Users/lzwjava/.hermes/hermes-agent
   ```

3. **按顺序尝试以下解决方案**（最有效的优先）：

   - **使用更快的镜像（对于中国或慢速连接强烈推荐）**：
     ```bash
     npm install --registry=https://registry.npmmirror.com
     ```

   - **清除 npm 缓存并重试**：
     ```bash
     npm cache clean --force
     npm install
     ```

   - **使用详细输出运行以查看实际卡在哪里**：
     ```bash
     npm install --verbose
     ```
     （观察输出 — 它会显示具体是哪个包导致了延迟。）

   - **删除 node_modules 和锁定文件然后重新安装**（全新开始）：
     ```bash
     rm -rf node_modules package-lock.json
     npm install
     ```

   - **在 npm install 之后显式安装 Playwright 浏览器**（如果它通过了主要安装步骤）：
     ```bash
     npx playwright install --with-deps chromium
     ```

4. **在 `npm install` 成功后**，重新运行 Hermes 安装程序或手动继续：
   ```bash
   # 如果安装程序已退出，通常可以再次运行它
   # 或继续执行：
   hermes doctor   # 检查一切是否正常
   ```

### 额外的 macOS 特定提示：
- 确保你有稳定的网络连接（尝试切换网络或暂时禁用 VPN）。
- 如果你在公司代理后面，用 `npm config set proxy http://your-proxy:port` 配置 npm。
- 更新 npm 本身：
  ```bash
  npm install -g npm@latest
  ```

一旦 Node.js 依赖项安装成功，Hermes 的其余设置应该会顺利完成。

如果仍然卡住，运行上面的详细命令，复制输出的最后几行，并在这里分享以获取更精确的帮助。如果这被证明是一个最近的 bug，你也可以查阅 Hermes Agent 官方的 GitHub issues。

参考：
- https://github.com/NousResearch/hermes-agent（项目仓库和已知的安装程序行为）
- https://hermes-agent.nousresearch.com/docs/reference/faq/（官方故障排除）
- 来自 Stack Overflow 和 npm 社区报告的常见 npm install 挂起解决方案。
