---
audio: false
generated: true
image: false
lang: en
layout: post
title: Launch Extension Host in VSCode
translated: false
type: note
---

To press **F5** in Visual Studio Code (VSCode) to launch the **Extension Development Host** for developing a VSCode extension, follow these steps:

1. **Open Your Extension Project in VSCode**:
   - Ensure you have a VSCode extension project set up. This typically includes a `package.json` file with the necessary extension configurations (e.g., `contributes`, `activationEvents`).
   - Open the folder containing your extension project in VSCode by selecting `File > Open Folder` or using `Ctrl+K, Ctrl+O` (Windows/Linux) or `Cmd+K, Cmd+O` (Mac).

2. **Verify Your Extension Setup**:
   - Make sure you have a valid `package.json` file in your project root with at least the following fields:
     ```json
     {
       "name": "your-extension-name",
       "displayName": "Your Extension Name",
       "description": "Description of your extension",
       "version": "0.0.1",
       "engines": {
         "vscode": "^1.60.0"
       },
       "categories": ["Other"],
       "activationEvents": ["*"],
       "main": "./extension.js",
       "contributes": {}
     }
     ```
   - Ensure you have an `extension.js` (or equivalent) file as the entry point for your extension code.
   - Install dependencies by running `npm install` in the integrated terminal (`Ctrl+``) if your extension uses Node.js modules.

3. **Press F5 to Launch the Extension Development Host**:
   - Press **F5** on your keyboard while your extension project is open in VSCode.
   - This starts the **Extension Development Host**, a separate VSCode window where your extension is loaded for testing.
   - VSCode will automatically:
     - Build your extension (if using TypeScript, it compiles `.ts` files to `.js`).
     - Launch a new VSCode instance with your extension activated.
     - Open a debugger attached to the Extension Host process.

4. **Debugging Configuration**:
   - VSCode uses a `launch.json` file in the `.vscode` folder to configure debugging. If it doesn’t exist, VSCode will create one automatically when you press F5 for the first time.
   - A typical `launch.json` for an extension looks like this:
     ```json
     {
       "version": "0.2.0",
       "configurations": [
         {
           "name": "Run Extension",
           "type": "extensionHost",
           "request": "launch",
           "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
           "outFiles": ["${workspaceFolder}/out/**/*.js"],
           "preLaunchTask": "npm: watch"
         }
       ]
     }
     ```
   - Ensure the `preLaunchTask` (if present) matches a task in your `tasks.json` (e.g., for compiling TypeScript).

5. **Test Your Extension**:
   - In the Extension Development Host window, your extension should be active. Test its functionality (e.g., commands, UI contributions) as defined in your `package.json` and code.
   - Use the **Debug Console** in the main VSCode window to view logs or errors from your extension.

6. **Troubleshooting**:
   - If F5 doesn’t work:
     - Ensure Node.js and npm are installed, as they’re required for extension development.
     - Check that you have the VSCode Extension API dependencies installed (`npm install @types/vscode`).
     - Verify the `launch.json` configuration points to the correct paths.
     - If you see errors, check the **Output** panel (select "Extension" in the dropdown) in the Extension Development Host window.
   - If the Extension Host doesn’t launch, ensure your project has no syntax errors in `package.json` or your main extension file.

**Additional Notes**:
- You can also start the Extension Development Host by opening the **Run and Debug** panel (`Ctrl+Shift+D` or `Cmd+Shift+D` on Mac) and selecting “Run Extension” from the dropdown, then clicking the green play button.
- To reload the Extension Host after making changes, use `Ctrl+R` (Windows/Linux) or `Cmd+R` (Mac) in the Extension Development Host window, or restart it with F5.

For more details, see the official VSCode extension development guide:
[VS Code Extension Development](https://code.visualstudio.com/api/get-started/your-first-extension)
