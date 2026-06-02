---
audio: false
generated: true
image: false
lang: zh
layout: post
title: npm安装后脚本卡顿修复
translated: true
type: note
---

问题：为什么我的 npm install 在运行完 fsevents、better-sqlite3、@askjo/camoufox-browser、agent-browser 和 geckodriver 等包的 postinstall 脚本后会卡住？

回答：

你的 npm 安装似乎在多个 postinstall 脚本执行完成后出现了卡顿（显示旋转器 ⠇ ⠋ ⠧）。这是一个常见问题，尤其是在 macOS 上，以下是最可能的原因和解决方法：

### 卡顿的最常见原因：
1. **@askjo/camoufox-browser 的 postinstall 脚本**
   命令 `npx camoufox-js fetch || true` 很可能是问题的根源。
   - 此脚本可能会下载一个较大的浏览器二进制文件（Camoufox 是一款基于 Firefox 的自动化/测试浏览器）。
   - 下载过程可能非常缓慢、静默失败，或因网络问题、防火墙、VPN 或速率限制而卡住。
   - 即使包含 `|| true`，底层进程可能仍在后台运行或挂起。

2. **网络相关问题**
   - 获取大文件（浏览器二进制文件、驱动等）时网络连接缓慢或不稳定。
   - 公司或学校防火墙或代理阻止了下载。
   - npm 注册表或 GitHub 发布镜像速度较慢。

3. **其他 postinstall 脚本**
   - `fsevents` 失败（在非 macOS 系统或有时在 macOS 上因 node-gyp 问题出现）是预期情况，但因其标记为可选，通常不会阻塞安装。
   - `better-sqlite3`、`agent-browser` 和 `geckodriver` 已成功完成（代码：0）。
   - 但某些脚本可能会生成后台进程，导致 npm 持续等待。

4. **npm 本身运行缓慢或状态异常**
   - node_modules 文件夹过大或依赖过多。
   - npm 缓存损坏。
   - 解压或安装过程中磁盘空间或内存不足。

### 解决方法：

**立即操作（按顺序尝试）：**

1. **再多等一会儿**
   Camoufox 的下载可能只是较慢。在终止之前，可让其再运行 5–10 分钟。

2. **取消并重新运行以获得更详细信息**
   按 `Ctrl + C` 停止，然后运行：
   ```bash
   npm install --loglevel=verbose
   ```
   这将显示更详细的输出，从而准确查看哪个环节卡住了。

3. **跳过或修复有问题的 postinstall 脚本**
   尝试在安装时跳过可选依赖或脚本：
   ```bash
   npm install --ignore-scripts
   ```
   然后根据需要手动运行重要脚本：
   ```bash
   npx camoufox-js fetch
   ```

   或者强制暂时跳过 Camoufox 的下载：
   ```bash
   npm install --ignore-scripts
   ```

4. **清除缓存并全新安装**（如果持续失败，推荐此方法）：
   ```bash
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```

5. **检查网络和系统资源**
   - 确保网络连接稳定且速度快。
   - 检查可用磁盘空间：`df -h`
   - 监控网络活动或尝试使用不同的网络/VPN。

6. **更新 npm 和 Node.js**
   ```bash
   npm install -g npm@latest
   ```
   如果 Node 版本非常旧，也考虑更新它。

7. **针对 camoufox-browser 的特定修复**
   如果下载持续卡住，可尝试手动运行并获取更详细的输出：
   ```bash
   npx camoufox-js fetch --verbose
   ```
   （请查阅包的文档以确认确切参数。）

### 补充提示：
- 这类卡顿问题常发生在浏览器自动化包（puppeteer、playwright、geckodriver、camoufox 等）中，因为它们需要下载较大的二进制文件（约 100MB 以上）。
- 如果你使用的是 macOS（路径显示为 `/Users/lzwjava/...`），若不在真实的 Mac 上或缺少 Xcode 命令行工具，fsevents 失败属于正常现象。
- 对于 `better-sqlite3`，如果将来安装失败，请确保已安装 Python 和构建工具。

建议首先尝试 `--loglevel=verbose` 版本，这样就能看到当前实际发生的情况。

如果你在再次卡住后提供完整的详细输出，我可以更精确地帮你定位具体原因。

参考：
- 无
