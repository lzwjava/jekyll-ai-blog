---
audio: false
generated: true
lang: en
layout: post
title: Liberty Tools Extension in Visual Studio Code
translated: false
type: note
---

Below is an overview of how you can use the Liberty Tools extension in Visual Studio Code to work with a WebSphere Liberty server:

---

### 1. Install the Liberty Tools Extension

- **Find and Install:**
  Open VS Code’s Extensions view, search for **"IBM WebSphere Liberty Tools"**, and install it.
- **Extension Benefits:**
  This extension integrates server management, application deployment, and debugging into VS Code.

---

### 2. Prepare Your WebSphere Liberty Server

- **Install or Point to a Liberty Runtime:**
  If you don’t already have a Liberty server installed, download and install one from IBM. If it’s already installed, note its installation directory.
- **Ensure Compatibility:**
  Verify that your Liberty runtime version is compatible with the extension.

---

### 3. Configure Your Liberty Server in VS Code

- **Creating a New Server Instance:**
  Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and run the command:
  `Liberty: Create Server`
  Follow the prompts to:
  - Select the runtime installation folder.
  - Specify the server configuration file (typically the `server.xml`).
- **Existing Projects:**
  If you already have a Liberty-based application, open the workspace so the extension can detect and help manage your server settings.

---

### 4. Adding Your Application

- **Deploying the App:**
  You can add your application to the server by either:
  - Editing the `server.xml` to include your application’s context and deployment details, or
  - Using the extension’s UI options (often available in the Liberty view) to “Add Application” or “Deploy Application.”
- **Build Integration:**
  If you’re using Maven or Gradle, the extension may also offer tasks that build your application before deployment.

---

### 5. Starting, Stopping, and Debugging the Server

- **Starting the Server:**
  In the Liberty view (often available as a dedicated panel or tree view in VS Code), right-click your configured server and select **"Start Server"**.
  The output pane will display startup logs and any configuration messages.
- **Stopping the Server:**
  Similarly, right-click and choose **"Stop Server"** to shut down your instance.
- **Debugging:**
  If you need to debug your application:
  - Set breakpoints in your code.
  - Use the command palette to run **"Liberty: Debug Server"** (or use the debug options provided in the Liberty view) to attach the VS Code debugger to your running server.
  - Your breakpoints should now be hit as your application processes requests.

---

### 6. Additional Features and Tips

- **Live Log Monitoring:**
  The extension provides a way to view Liberty server logs in real time, making it easier to diagnose issues.
- **Editing Server Configuration:**
  Benefit from IntelliSense and suggestions when editing your `server.xml` directly within VS Code.
- **Task Integration:**
  Utilize VS Code’s tasks if you’re running automated builds or deployments as part of your development workflow.
- **Container and Remote Support:**
  Depending on your setup, you might also be able to configure Liberty to run within containers or remote environments, with additional commands available in the extension.

---

### Final Notes

Using the Liberty Tools extension streamlines the process of developing, deploying, and debugging your WebSphere Liberty applications directly within VS Code. This integration helps reduce context switching and speeds up your development cycle.

Feel free to refer to the official IBM documentation on the Liberty Tools extension for any advanced configurations or troubleshooting steps.
