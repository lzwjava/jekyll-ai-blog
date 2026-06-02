---
audio: false
generated: true
lang: zh
layout: post
title: VS Code VSIX 下载
translated: true
type: note
---

要手动下载 Visual Studio Code（VS Code）扩展的 `.vsix` 文件，可以使用托管所有官方扩展的 Visual Studio Marketplace。`.vsix` 文件是 VS Code 扩展的打包格式，虽然 Marketplace 并不总是提供直接下载按钮，但你可以通过构造下载 URL 或使用替代方法来实现。以下是详细步骤：

### 手动下载 `.vsix` 文件的步骤

1. **在 Visual Studio Marketplace 上找到扩展**
   - 在网页浏览器中访问 [Visual Studio Marketplace](https://marketplace.visualstudio.com/vscode)。
   - 搜索你需要的扩展（例如，Microsoft 的 "Python"、"Prettier - Code formatter" 等）。
   - 打开扩展页面。例如，Python 扩展的 URL 可能类似于：
     `https://marketplace.visualstudio.com/items?itemName=ms-python.python`。

2. **识别发布者和扩展名称**
   - 在扩展页面上，记下**发布者**和**扩展标识符**。这些信息包含在 URL 中或显示在页面上。
   - 例如，在 `ms-python.python` 中，`ms-python` 是发布者，`python` 是扩展名称。

3. **构造下载 URL**
   - 可以使用 Marketplace 提供的特定 URL 模式直接下载 `.vsix` 文件。通用格式为：

     ```
     https://<publisher>.gallery.vsassets.io/_apis/public/gallery/publisher/<publisher>/extension/<extension-name>/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
     ```

   - 将 `<publisher>` 替换为发布者名称，`<extension-name>` 替换为扩展名称。
   - 对于 Python 扩展（`ms-python.python`），URL 为：

     ```
     https://ms-python.gallery.vsassets.io/_apis/public/gallery/publisher/ms-python/extension/python/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
     ```

   - 将此 URL 粘贴到浏览器中，将触发 `.vsix` 文件的下载。

4. **替代方法：使用 Marketplace 页面上的“下载扩展”链接（如果可用）**
   - 某些扩展页面在**资源**部分或其他位置包含“下载扩展”链接。如果存在，点击它可直接下载 `.vsix` 文件。但这不太常见，因此 URL 方法更可靠。

5. **验证下载**
   - 下载的文件将具有 `.vsix` 扩展名（例如 `ms-python.python-<version>.vsix`）。
   - 检查文件大小和名称，确保它与预期的扩展和版本匹配。

6. **在 VS Code 中安装 `.vsix` 文件（可选）**
   - 打开 VS Code。
   - 转到扩展视图（`Ctrl+Shift+X` 或 macOS 上的 `Cmd+Shift+X`）。
   - 点击扩展面板右上角的三个点菜单（`...`）。
   - 选择**从 VSIX 安装**，然后浏览并选择下载的 `.vsix` 文件。

### 示例演练

假设你需要 Dirk Baeumer 的 **ESLint** 扩展：

- Marketplace URL：`https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint`
- 发布者：`dbaeumer`
- 扩展名称：`vscode-eslint`
- 下载 URL：

  ```
  https://dbaeumer.gallery.vsassets.io/_apis/public/gallery/publisher/dbaeumer/extension/vscode-eslint/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
  ```

- 在浏览器中打开此 URL，`.vsix` 文件（例如 `dbaeumer.vscode-eslint-<version>.vsix`）将被下载。

### 注意事项

- **版本**：URL 中的 `/latest/` 部分确保你获得最新版本。如果你需要特定版本，通常需要访问版本号（在 Marketplace 的“版本历史”选项卡中可见），并可能需要调整 URL 或使用像 `ovsx` 这样的工具（见下文），尽管 Marketplace API 并不总是通过直接 URL 轻松公开旧版本。
- **下载被阻止**：如果 URL 不起作用，可能是发布者限制了直接访问，或者你的浏览器/网络阻止了它。在这种情况下，尝试使用不同的浏览器或下载管理器。
- **替代工具**：你可以使用像 `ovsx`（来自 Open VSX Registry）这样的命令行工具下载扩展。通过 npm 安装（`npm install -g ovsx`），然后运行：

  ```
  ovsx download ms-python.python
  ```

  这将通过编程方式下载 `.vsix` 文件。

### 最终步骤

要手动下载 VS Code 扩展的 `.vsix` 文件：

1. 访问 [Visual Studio Marketplace](https://marketplace.visualstudio.com/vscode) 上的扩展页面。
2. 识别发布者和扩展名称（例如 `ms-python.python`）。
3. 在浏览器中使用此 URL 格式：

   ```
   https://<publisher>.gallery.vsassets.io/_apis/public/gallery/publisher/<publisher>/extension/<extension-name>/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
   ```

4. 下载 `.vsix` 文件，并可选地在 VS Code 中安装它。
