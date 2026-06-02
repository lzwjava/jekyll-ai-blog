---
audio: false
generated: true
lang: en
layout: post
title: VS Code VSIX Download
translated: false
type: note
---

To manually download a `.vsix` file for a Visual Studio Code (VS Code) extension, you can use the Visual Studio Marketplace, which hosts all official extensions. The `.vsix` file is the packaged format for VS Code extensions, and while the Marketplace doesn’t always provide a direct download button, you can construct the download URL or use alternative methods. Here’s how to do it step-by-step:

### Steps to Manually Download a `.vsix` File

1. **Find the Extension on the Visual Studio Marketplace**
   - Go to the [Visual Studio Marketplace](https://marketplace.visualstudio.com/vscode) in your web browser.
   - Search for the extension you want (e.g., "Python" by Microsoft, "Prettier - Code formatter", etc.).
   - Open the extension’s page. For example, the Python extension’s URL might look like:
     `https://marketplace.visualstudio.com/items?itemName=ms-python.python`.

2. **Identify the Publisher and Extension Name**
   - On the extension’s page, note the **publisher** and **extension identifier**. These are part of the URL or displayed on the page.
   - For example, in `ms-python.python`, `ms-python` is the publisher, and `python` is the extension name.

3. **Construct the Download URL**
   - The `.vsix` file can be downloaded directly using a specific URL pattern provided by the Marketplace. The general format is:

     ```
     https://<publisher>.gallery.vsassets.io/_apis/public/gallery/publisher/<publisher>/extension/<extension-name>/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
     ```

   - Replace `<publisher>` with the publisher’s name and `<extension-name>` with the extension name.
   - For the Python extension (`ms-python.python`), the URL would be:

     ```
     https://ms-python.gallery.vsassets.io/_apis/public/gallery/publisher/ms-python/extension/python/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
     ```

   - Paste this URL into your browser, and it will trigger the download of the `.vsix` file.

4. **Alternative: Use the Marketplace Page “Download Extension” Link (if available)**
   - Some extension pages include a “Download Extension” link under the **Resources** section or elsewhere. If present, click it to download the `.vsix` file directly. However, this is less common, so the URL method is more reliable.

5. **Verify the Download**
   - The downloaded file will have a `.vsix` extension (e.g., `ms-python.python-<version>.vsix`).
   - Check the file size and name to ensure it matches the extension and version you expect.

6. **Install the `.vsix` File in VS Code (Optional)**
   - Open VS Code.
   - Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
   - Click the three-dot menu (`...`) at the top-right of the Extensions pane.
   - Select **Install from VSIX**, then browse to and select the downloaded `.vsix` file.

### Example Walkthrough

Let’s say you want the **ESLint** extension by Dirk Baeumer:

- Marketplace URL: `https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint`
- Publisher: `dbaeumer`
- Extension name: `vscode-eslint`
- Download URL:

  ```
  https://dbaeumer.gallery.vsassets.io/_apis/public/gallery/publisher/dbaeumer/extension/vscode-eslint/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
  ```

- Open this URL in your browser, and the `.vsix` file (e.g., `dbaeumer.vscode-eslint-<version>.vsix`) will download.

### Notes

- **Version**: The `/latest/` part of the URL ensures you get the most recent version. If you need a specific version, you’d typically need access to the version number (visible on the Marketplace’s “Version History” tab) and might need to adjust the URL or use a tool like `ovsx` (see below), though the Marketplace API doesn’t always expose older versions easily via direct URL.
- **Blocked Downloads**: If the URL doesn’t work, the publisher might restrict direct access, or your browser/network might block it. In such cases, try a different browser or a download manager.
- **Alternative Tools**: You can use a command-line tool like `ovsx` (from the Open VSX Registry) to download extensions. Install it via npm (`npm install -g ovsx`), then run:

  ```
  ovsx download ms-python.python
  ```

  This downloads the `.vsix` file programmatically.

### Final Answer

To manually download a `.vsix` file for a VS Code extension:

1. Go to the extension’s page on the [Visual Studio Marketplace](https://marketplace.visualstudio.com/vscode).
2. Identify the publisher and extension name (e.g., `ms-python.python`).
3. Use this URL format in your browser:

   ```
   https://<publisher>.gallery.vsassets.io/_apis/public/gallery/publisher/<publisher>/extension/<extension-name>/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
   ```

4. Download the `.vsix` file and optionally install it in VS Code.
