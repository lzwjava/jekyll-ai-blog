---
audio: false
generated: true
lang: en
layout: post
title: Troubleshooting VSCode Extension Installation with Proxy Issues
translated: false
type: note
---

To check the extension installation log in Visual Studio Code (VSCode) or use the command line to install an extension with `code --install-extension` and view the log—especially if you suspect a proxy issue—here’s how you can proceed:

---

### Using the Command Line with `code --install-extension`
You can install extensions via the command line and get some visibility into the process, which might help diagnose proxy issues.

1. **Install with Verbose Output**
   Run the following command to install an extension and see more detailed output:
   ```bash
   code --install-extension <extension-id> --verbose
   ```
   - Replace `<extension-id>` with the ID of the extension (e.g., `vscodevim.vim`).
   - The `--verbose` flag increases the output detail, showing progress and potential errors, such as proxy or network issues.

2. **Handle Proxy Issues**
   If you’re behind a proxy, it might interfere with the installation. Try these approaches:
   - **Set Proxy Environment Variables**:
     Before running the command, configure the proxy settings:
     ```bash
     export HTTP_PROXY=http://your-proxy-server:port
     export HTTPS_PROXY=http://your-proxy-server:port
     code --install-extension <extension-id>
     ```
     - On Windows, use `set` instead of `export`:
       ```cmd
       set HTTP_PROXY=http://your-proxy-server:port
       set HTTPS_PROXY=http://your-proxy-server:port
       code --install-extension <extension-id>
       ```
   - **Specify Proxy Directly**:
     Use the `--proxy-server` flag:
     ```bash
     code --install-extension <extension-id> --proxy-server=http://your-proxy-server:port
     ```

3. **Check the Output**
   - The console output from the `--verbose` flag will show the installation progress and any errors (e.g., connection timeouts or proxy authentication failures).
   - Note: The command-line interface (`code`) has limited proxy support compared to the VSCode GUI, so logs might not be as detailed as expected.

---

### Checking Logs in VSCode
For more detailed logs—especially after an installation attempt—use VSCode’s built-in logging features:

1. **Open the Logs Folder**
   - Open VSCode and access the Command Palette:
     - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
     - Type and select **Developer: Open Logs Folder**.
   - This opens a folder containing various log files. Look for:
     - **`exthost.log`**: Logs related to extension host processes, including installation attempts.
     - **`sharedprocess.log`**: Logs for shared processes that might include extension-related events.
   - Open these files in a text editor and search for errors mentioning the extension ID, network issues, or proxy problems.

2. **View the Output Panel**
   - In VSCode, go to `View > Output` to open the **Output** panel.
   - In the dropdown menu on the right, select **Extensions**.
   - This shows real-time logs for extension activities when installing from within VSCode (not directly via CLI). If you retry the installation through the VSCode UI, you might see proxy-related errors here.

---

### Additional Steps for Proxy Troubleshooting
Since you suspect a proxy issue, here are extra tips to ensure proper configuration:

- **Configure Proxy in VSCode**
  - Open VSCode settings (`File > Preferences > Settings` or `Ctrl+,`).
  - Search for `proxy` and set:
    ```json
    "http.proxy": "http://your-proxy-server:port"
    ```
  - Optionally, adjust `"http.proxyStrictSSL"` (set to `false` if needed) or `"http.proxyAuthorization"` (for authenticated proxies).
  - These settings apply to installations within VSCode, not necessarily the CLI.

- **Test Network Access**
  - Manually test if the proxy allows access to the VSCode Marketplace:
    - Find the extension’s VSIX file URL (e.g., from the Marketplace website).
    - Use a tool like `curl`:
      ```bash
      curl -x http://your-proxy-server:port <vsix-url>
      ```
    - If this fails, your proxy might be blocking the connection.

---

### Recommended Approach
- **For CLI Installation**: Use `code --install-extension <extension-id> --verbose` with proxy environment variables or `--proxy-server` to see immediate output. Check for errors in the terminal.
- **For Detailed Logs**: Install the extension via the VSCode UI (Marketplace) and check the **Output > Extensions** panel or the logs folder (`exthost.log`).
- **Proxy Check**: Ensure proxy settings are correct in both your system and VSCode.

This combination lets you monitor progress and diagnose proxy issues effectively. If the CLI output isn’t sufficient, the VSCode logs will provide deeper insight into what’s going wrong.
