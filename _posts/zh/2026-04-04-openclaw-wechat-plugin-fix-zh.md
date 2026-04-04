---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw微信插件修复
translated: true
type: note
---

好问题。让我详细分解整个过程——从“损坏的插件”到“微信成功连接”的完整链条。

---

## 🔍 微信如何被连接——完整解析

### 第一阶段：诊断

1. **你要求**检查微信插件
2. **运行 `openclaw status`**——获得清晰的错误：
   ```
   TypeError: (0, _pluginSdk.resolvePreferredOpenClawTmpDir) is not a function
   ```
3. **检查插件版本**：`v1.0.3`（3月29日安装）
4. **在 npm 上搜索**最新版本：`v2.1.6` 存在
5. **根本原因**：v1.0.3 调用了一个来自 OpenClaw Plugin SDK 的函数，该函数在新版 OpenClaw（2026.4.2）中被移除/重命名

### 第二阶段：失败的尝试

1. 在扩展目录内运行 `npm install @tencent-weixin/openclaw-weixin@2.1.6`
2. **为何不成功**：OpenClaw 扩展采用**源码优先**模式——它直接从扩展目录加载 `index.ts` 和 `src/`，而不是从 `node_modules` 加载。npm 仅更新了 `package.json` + `node_modules/`，旧的 `.ts` 源码文件未被触及

### 第三阶段：修复

1. **备份**旧扩展目录：`mv openclaw-weixin openclaw-weixin.bak`
2. **使用 npm 将 v2.1.6 源码安装到临时目录**：
   ```
   npm install @tencent-weixin/openclaw-weixin@2.1.6 --prefix weixin-tmp
   ```
3. **复制源码**从 `weixin-tmp/node_modules/@tencent-weixin/openclaw-weixin/` → 新的 `openclaw-weixin/` 目录（这次真正获取了 v2.1.6 的源码文件）
4. **在新目录内运行 `npm install`** 以安装依赖项（557个包）
5. **清理**临时目录
6. **验证**：`package.json` 现在显示 `"version": "2.1.6"`，且 `openclaw status` 不再抛出 SDK 错误

### 第四阶段：二维码登录

1. **阅读插件源码**以找到登录命令——发现它通过 `openclaw channels login --channel openclaw-weixin` 注册
2. **登录流程**：
   - 插件调用 `https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3` 获取二维码
   - 在终端中以 ASCII 艺术形式渲染并提供直接 URL
   - 每1秒长轮询 `get_qrcode_status`，最长持续8分钟
   - 状态：`wait` → `scaned` → `confirmed`
   - 当状态为 `confirmed` 时，将 `bot_token` + `ilink_bot_id` + `baseurl` 保存至 `openclaw.json`
3. **你用微信扫描了二维码**并在应用中确认
4. 插件接收到 `bot_token`，将配置写入磁盘
5. 运行 `openclaw gateway restart` 以用新账户重新加载

### 各工具的作用

| 工具 | 用途 |
|------|---------|
| `exec` | 运行所有 shell 命令——npm install、openclaw status、grep、文件读取 |
| `process` | 监控长时间运行命令（mtr、npm、登录过程） |
| `read` | 阅读插件源码以理解登录 API |
| `web_search` / `memory_search` | 上下文收集（本次无需网络搜索） |
| `cron` | 审查现有的 cron 任务，用于生成综合性报告 |

### 为何能成功

关键洞察在于：OpenClaw 扩展**不是标准的 npm 包**——它们是从扩展目录以源码形式加载的。简单的 `npm install` 不会替换 `.ts` 文件。我不得不通过 npm 在临时位置获取新源码，然后整体复制过来。🦞