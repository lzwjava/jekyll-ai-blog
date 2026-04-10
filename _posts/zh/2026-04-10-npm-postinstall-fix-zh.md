---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复npm安装后脚本卡住问题
translated: true
type: note
---

问：为什么我的 npm install 会卡在 @askjo/camoufox-browser 的 postinstall 脚本上，按下 Ctrl+C 后出现的 SIGINT 消息是什么意思？

答：

你分享的输出信息已确认了卡住的确切原因。

### 发生了什么：
- npm 正在运行 `@askjo/camoufox-browser@1.0.12` 的 **postinstall** 脚本。
- 该脚本执行：`npx camoufox-js fetch || true`
- 当你按下 Ctrl + C 时，该命令**仍在运行**（很可能正在下载一个大型的浏览器二进制文件）。
- 因为你中断了它，npm 报告：
  ```
  npm info run @askjo/camoufox-browser@1.0.12 postinstall { code: null, signal: 'SIGINT' }
  ```
  SIGINT 仅表示“进程被用户中断”（Ctrl+C）。

旋转图标（`⠇ ⠋ ⠙ ⠸`）持续显示意味着 `camoufox-js fetch` 进程**没有**顺利或快速退出，因此 npm 仍在等待它。

### 为什么会卡住：
`camoufox-js fetch` 会下载一个完整的浏览器（Camoufox，一个基于 Firefox 用于自动化的浏览器）。这类下载通常具有以下特点：
- 体积非常大（100 MB – 300 MB 以上）
- 在某些网络上速度缓慢
- 如果连接不稳定、处于防火墙/代理之后，或下载服务器较慢，容易卡住

即使有 `|| true` 部分，如果子进程本身冻结了，它也未必能起作用。

### 如何正确修复：

1. **清理并尝试在更好的控制下重新安装**  
   首先，删除部分已安装的包：
   ```bash
   rm -rf node_modules/@askjo/camoufox-browser
   ```

2. **安装时暂时跳过脚本**（最快的解决方法）
   ```bash
   npm install --ignore-scripts
   ```

3. **手动运行 fetch 以获得更清晰的进度显示**（推荐）
   在使用 `--ignore-scripts` 完成安装后，手动运行 fetch 以便查看进度：
   ```bash
   npx camoufox-js fetch
   ```
   - 仔细查看输出。如果仍然卡住，你会看到具体的卡住位置。
   - 你也可以尝试添加任何该工具支持的详细输出标志（例如 `npx camoufox-js fetch --verbose`）。

4. **完整清理并重新安装**（如果问题持续）
   ```bash
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install --ignore-scripts
   npx camoufox-js fetch
   ```

5. **网络相关解决方案**
   - 使用更快或不同的互联网连接（有时移动热点会有帮助）。
   - 如果正在使用 VPN/代理，请暂时禁用它。
   - 如果服务器繁忙，尝试在非高峰时段运行 fetch。

6. **替代方案：如果不需要此依赖，完全跳过它**
   如果此项目实际上不需要 Camoufox（它似乎与浏览器自动化/hermes-agent 相关），你可以删除或替换此依赖。但请仅在理解项目需求的情况下进行此操作。

### 快速测试：
在完成 `npm install --ignore-scripts` 后，运行以下命令检查 fetch 是否正常工作：
```bash
npx camoufox-js fetch
```

如果手动 fetch 也卡住或失败，那么问题肯定出在下载本身（网络、防火墙或 camoufox 下载服务器）。

是否需要我提供命令来检查你的网络速度或查看 camoufox 正在尝试下载哪些文件？只需告诉我尝试手动 `npx camoufox-js fetch` 后的结果。

参考文献：  
- 无