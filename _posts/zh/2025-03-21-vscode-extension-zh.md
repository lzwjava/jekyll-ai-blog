---
audio: false
generated: true
lang: zh
layout: post
title: 代理环境下VSCode扩展安装故障排查
translated: true
type: note
---

要检查 Visual Studio Code (VSCode) 中的扩展安装日志，或使用命令行通过 `code --install-extension` 安装扩展并查看日志——特别是当您怀疑存在代理问题时——可以按以下步骤操作：

---

### 使用命令行 `code --install-extension`

您可以通过命令行安装扩展，并查看安装过程的相关信息，这有助于诊断代理问题。

1. **使用详细输出安装**
   运行以下命令安装扩展并查看更详细的输出：

   ```bash
   code --install-extension <扩展ID> --verbose
   ```

   - 将 `<扩展ID>` 替换为扩展的实际 ID（例如 `vscodevim.vim`）。
   - `--verbose` 标志会增加输出的详细程度，显示进度和可能的错误，例如代理或网络问题。

2. **处理代理问题**
   如果您位于代理之后，可能会干扰安装。尝试以下方法：
   - **设置代理环境变量**：
     在运行命令之前，配置代理设置：

     ```bash
     export HTTP_PROXY=http://您的代理服务器:端口
     export HTTPS_PROXY=http://您的代理服务器:端口
     code --install-extension <扩展ID>
     ```

     - 在 Windows 上，使用 `set` 而不是 `export`：

       ```cmd
       set HTTP_PROXY=http://您的代理服务器:端口
       set HTTPS_PROXY=http://您的代理服务器:端口
       code --install-extension <扩展ID>
       ```

   - **直接指定代理**：
     使用 `--proxy-server` 标志：

     ```bash
     code --install-extension <扩展ID> --proxy-server=http://您的代理服务器:端口
     ```

3. **检查输出**
   - `--verbose` 标志的控制台输出将显示安装进度和任何错误（例如连接超时或代理认证失败）。
   - 注意：命令行界面（`code`）的代理支持有限，不如 VSCode 图形界面详细，因此日志可能不如预期详细。

---

### 在 VSCode 中检查日志

如需更详细的日志——特别是在安装尝试之后——可以使用 VSCode 的内置日志功能：

1. **打开日志文件夹**
   - 打开 VSCode 并访问命令面板：
     - 按下 `Ctrl+Shift+P`（或在 macOS 上按下 `Cmd+Shift+P`）。
     - 输入并选择 **Developer: Open Logs Folder**。
   - 这将打开一个包含多个日志文件的文件夹。请查找：
     - **`exthost.log`**：与扩展主机进程相关的日志，包括安装尝试。
     - **`sharedprocess.log`**：共享进程的日志，可能包含与扩展相关的事件。
   - 在文本编辑器中打开这些文件，并搜索提及扩展 ID、网络问题或代理问题的错误。

2. **查看输出面板**
   - 在 VSCode 中，转到 `查看 > 输出` 以打开 **输出** 面板。
   - 在右侧的下拉菜单中，选择 **Extensions**。
   - 这将显示扩展活动的实时日志，适用于在 VSCode 内部安装扩展（不适用于直接通过 CLI 安装）。如果您通过 VSCode 界面重试安装，可能会在此处看到与代理相关的错误。

---

### 代理故障排除的额外步骤

由于您怀疑是代理问题，以下是一些额外提示以确保配置正确：

- **在 VSCode 中配置代理**
  - 打开 VSCode 设置（`文件 > 首选项 > 设置` 或 `Ctrl+,`）。
  - 搜索 `proxy` 并设置：

    ```json
    "http.proxy": "http://您的代理服务器:端口"
    ```

  - 可选调整 `"http.proxyStrictSSL"`（如果需要，设置为 `false`）或 `"http.proxyAuthorization"`（用于需要认证的代理）。
  - 这些设置适用于 VSCode 内部的安装，不一定适用于 CLI。

- **测试网络访问**
  - 手动测试代理是否允许访问 VSCode 市场：
    - 从市场网站找到扩展的 VSIX 文件 URL。
    - 使用 `curl` 等工具：

      ```bash
      curl -x http://您的代理服务器:端口 <vsix-url>
      ```

    - 如果失败，可能是代理阻止了连接。

---

### 推荐方法

- **对于 CLI 安装**：使用 `code --install-extension <扩展ID> --verbose` 并配合代理环境变量或 `--proxy-server` 以查看即时输出。检查终端中的错误。
- **对于详细日志**：通过 VSCode 界面（市场）安装扩展，并检查 **输出 > Extensions** 面板或日志文件夹（`exthost.log`）。
- **代理检查**：确保系统和 VSCode 中的代理设置正确。

这种组合方法可以让您监控进度并有效诊断代理问题。如果 CLI 输出不够详细，VSCode 日志将提供更深入的错误信息。
