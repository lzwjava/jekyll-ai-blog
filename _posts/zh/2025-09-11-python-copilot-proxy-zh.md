---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: Python Copilot 代理服务器实现
translated: true
type: note
---

这个 Python 脚本是一个与 GitHub Copilot 交互以生成代码补全的本地代理服务器。它通过处理身份验证并将请求转发到 Copilot 的 API，模拟了官方 GitHub Copilot 插件（例如 Neovim 插件）的行为。

---

### **核心组件与工作流程**
1. **身份验证（`setup()` 和 `get_token()`）**
   - 使用 OAuth 设备流程与 GitHub 进行身份验证
   - 向 GitHub 请求设备代码和用户代码
   - 要求用户访问验证网址并输入用户代码
   - 轮询 GitHub 直到获取访问令牌
   - 将令牌保存至 `.copilot_token` 供后续使用
   - 将访问令牌交换为 Copilot 会话令牌（API 调用必需）

2. **令牌刷新（`token_thread()`）**
   - 在后台线程中运行
   - 每 25 分钟刷新一次 Copilot 令牌（因令牌会过期）

3. **Copilot API 交互（`copilot()`）**
   - 向 Copilot API 发送提示（代码片段）
   - 以流式传输模式逐行返回生成的补全内容
   - 处理错误（如无效/过期的令牌）

4. **HTTP 服务器（`HTTPRequestHandler`）**
   - 监听 POST 请求（例如来自本地编辑器）
   - 从请求中提取提示内容和编程语言
   - 调用 `copilot()` 并以纯文本形式返回补全结果

5. **主函数（`main()`）**
   - 启动令牌刷新线程
   - 在指定端口（默认：8080）启动 HTTP 服务器

---

### **运行机制详解**
1. **首次运行（无令牌）**
   - 脚本调用 `setup()` 通过 OAuth 进行身份验证
   - 用户访问 GitHub，输入代码并授权访问
   - 脚本将访问令牌保存至 `.copilot_token`

2. **后续运行（令牌已存在）**
   - 脚本读取 `.copilot_token` 并获取 Copilot 会话令牌
   - 若令牌过期，会自动刷新

3. **处理请求**
   - 本地编辑器（如 Neovim）发送包含代码片段的 POST 请求
   - 脚本将提示内容转发至 Copilot API
   - 补全结果返回给编辑器

4. **令牌管理**
   - 后台线程每 25 分钟刷新一次令牌，避免过期

---

### **开发背景**
- **绕过官方插件**：部分编辑器（如 Neovim）缺乏官方 Copilot 支持，此脚本可作为桥梁
- **本地代理**：通过本地管理令牌避免频率限制
- **自定义扩展**：可修改以适配不同编辑器或 API

---

### **安全与伦理考量**
- **硬编码客户端 ID**：脚本使用 GitHub Copilot 官方客户端 ID（Iv1.b507a08c87ecfe98），在非官方插件中使用可能违反 GitHub 服务条款
- **令牌存储**：访问令牌以明文形式存储（.copilot_token），存在安全风险
- **频率限制**：频繁请求可能触发 GitHub 滥用检测机制

---
### **使用方法**
1. 运行脚本：
   ```sh
   python copilot_proxy.py [端口号]
   ```
   （默认端口：8080）

2. 配置编辑器向 http://localhost:8080 发送 JSON 格式请求：
   ```json
   {
     "prompt": "def hello_world():",
     "language": "python"
   }
   ```

3. 脚本将返回 Copilot 的补全内容

---
### **优化方向**
- **增强错误处理**：重试失败请求，处理网络问题
- **安全令牌存储**：使用加密存储或环境变量
- **配置文件**：支持自定义客户端 ID、端口等参数
- **日志记录**：添加调试日志便于故障排查

---
### **替代方案**
- 使用官方 Copilot 插件（VS Code、JetBrains 等）
- 尝试开源替代方案如 Codeium 或 Tabby

该脚本是巧妙的解决方案，但因可能违反服务条款，使用时需谨慎。
