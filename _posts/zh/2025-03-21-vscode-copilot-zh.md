---
audio: false
generated: true
lang: zh
layout: post
title: 在VS Code中开始使用GitHub Copilot
translated: true
type: note
---

在 Visual Studio Code (VS Code) 中使用 GitHub Copilot 设置完成后非常简单。以下是截至 2025 年 3 月 20 日的分步指南：

---

### 步骤 1：安装 VS Code
- 确保已安装 Visual Studio Code。如果尚未安装，请从 [code.visualstudio.com](https://code.visualstudio.com/) 下载。
- 将 VS Code 更新至最新版本以获得最佳兼容性（前往 `帮助 > 检查更新`）。

---

### 步骤 2：安装 GitHub Copilot 扩展
1. **打开 VS Code**。
2. **前往扩展市场**：
   - 点击左侧活动栏中的扩展图标（或按 `Ctrl+Shift+X` / Mac 上按 `Cmd+Shift+X`）。
3. **搜索 "GitHub Copilot"**：
   - 在搜索栏中输入 "GitHub Copilot"。
   - 查找 GitHub 官方的扩展（带有已验证徽章）。
4. **安装扩展**：
   - 点击 "GitHub Copilot" 旁边的 `安装` 按钮。
5. **可选：安装 Copilot Chat（推荐）**：
   - 搜索 "GitHub Copilot Chat" 并安装。这将添加对话式 AI 功能，例如通过聊天提问或生成代码。

---

### 步骤 3：登录 GitHub Copilot
1. **通过 GitHub 认证**：
   - 安装后，会弹出提示要求登录。
   - 点击弹出窗口中的 `Sign in to GitHub`，或前往 Copilot 状态图标（VS Code 右下角）并选择 "Sign in"。
2. **在浏览器中授权**：
   - 浏览器窗口将打开，要求登录 GitHub 账户。
   - 点击 `Authorize Git hypoxia` 批准授权请求。
3. **复制代码**：
   - GitHub 将提供一个一次性代码。复制并在 VS Code 提示时粘贴回去。
4. **验证激活**：
   - 登录后，状态栏中的 Copilot 图标应变为绿色，表示已激活。您还会看到确认访问的通知。

---

### 步骤 4：配置 Copilot（可选）
- **启用/禁用建议**：
  - 前往 `文件 > 首选项 > 设置`（或按 `Ctrl+,` / `Cmd+,`）。
  - 搜索 "Copilot" 以调整设置，例如启用内联建议或针对特定语言禁用它。
- **检查订阅**：
  - Copilot 在 30 天试用期后需要订阅（$10/月或 $100/年）。学生、教师和开源维护者可以通过 [GitHub Education](https://education.github.com/) 或 Copilot 设置申请免费访问。

---

### 步骤 5：开始使用 Copilot
以下是在编码工作流中利用 Copilot 的方法：

#### 1. **代码建议**
- **内联自动完成**：
  - 在文件中开始输入（例如，在 Python 中输入 `def calculate_sum(`），Copilot 将以灰色文本显示建议。
  - 按 `Tab` 接受建议，或继续输入以忽略。
- **多行建议**：
  - 编写注释如 `// Function to sort an array` 并按 Enter。Copilot 可能会建议整个实现（例如排序算法）。
  - 使用 `Alt+]`（或 Mac 上 `Option+]`）循环查看多个建议。

#### 2. **从注释生成代码**
- 输入描述性注释如：
  ```javascript
  // Fetch data from an API and handle errors
  ```
  按 Enter，Copilot 可能会生成：
  ```javascript
  async function fetchData(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
    }
  }
  ```
- 按 `Tab` 接受或根据需要调整。

#### 3. **Copilot Chat（如果已安装）**
- **打开聊天**：
  - 点击侧边栏中的聊天图标或使用 `Ctrl+Alt+C`（可自定义）。
- **提问**：
  - 输入如“解释 JavaScript 中 Promise 的工作原理”或“编写读取 CSV 文件的 Python 脚本”。
  - Copilot 将在聊天面板中回复，并可直接将代码插入编辑器。
- **上下文帮助**：
  - 高亮代码，右键点击并选择“Ask Copilot”以解释或重构它。

#### 4. **调试和测试**
- 编写注释如 `// Write unit tests for this function`，Copilot 可以使用 Jest 或 PyTest 等框架生成测试用例。

---

### 有效使用技巧
- **具体明确**：提供的上下文越多（例如注释、变量名），Copilot 的建议越好。
- **检查建议**：Copilot 并非完美—始终检查其代码的准确性和安全性。
- **语言支持**：它最适用于流行语言（Python、JavaScript、Java 等），但也支持数十种其他语言。
- **键盘快捷键**：
  - `Alt+\`（或 Mac 上 `Option+\`）：手动显示所有建议。
  - `Ctrl+Enter`：打开建议面板。

---

### 故障排除
- **无法工作？**：
  - 确保已登录（检查状态栏）。
  - 在 GitHub 账户设置中验证订阅是否有效。
  - 如果问题持续，重启 VS Code 或重新安装扩展。
- **没有建议？**：
  - 检查当前语言是否启用了 Copilot（设置中 `editor.inlineSuggest.enabled` 应为 true）。

---

就是这样！您现在已准备好在 VS Code 中使用 GitHub Copilot。开始打开文件，输入一些代码或注释，让 Copilot 协助您。祝您编码更高效！
