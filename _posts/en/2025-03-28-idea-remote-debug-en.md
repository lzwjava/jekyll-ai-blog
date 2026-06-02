---
audio: false
generated: true
lang: en
layout: post
title: IntelliJ IDEA's Built-in Remote Debugging
translated: false
type: note
---

To connect IntelliJ IDEA to the debug port of a WebSphere Liberty Server that you've started with `server debug default`, without using the WebSphere Liberty plugin, you can leverage IntelliJ IDEA's built-in remote debugging feature. This approach works because WebSphere Liberty, when started in debug mode, exposes a debug port (typically 7777 by default) that any JVM debugger, including IntelliJ IDEA, can attach to. Below are the detailed steps to achieve this:

---

### Step 1: Start the WebSphere Liberty Server in Debug Mode

When you run `server debug default` (assuming "default" is the name of your server; replace it with your actual server name if different), WebSphere Liberty starts with debugging enabled. By default, this command configures the server to listen for debug connections on port **7777**.

- **Command**:

  ```bash
  server debug default
  ```

- **What it does**: This starts the "default" server in debug mode, automatically enabling JVM debugging options (e.g., `-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=7777`).
- **Verification**: After running the command, check the server console output or logs (e.g., `messages.log`) to confirm that the server is listening on the debug port. Look for a message indicating the debug port (usually 7777 unless it’s overridden or unavailable).

---

### Step 2: Confirm the Debug Port

The default debug port for WebSphere Liberty is **7777**. However, if this port is in use or has been customized:

- Check the console output after starting the server. It might say something like "Listening for debugger connections on port 7777."
- If the port differs (e.g., a random port is assigned due to a conflict), note the actual port number for use in IntelliJ IDEA.

For this guide, we’ll assume the default port **7777** unless your setup indicates otherwise.

---

### Step 3: Configure Remote Debugging in IntelliJ IDEA

IntelliJ IDEA’s remote debugging feature allows you to connect to the server’s JVM without needing a specific WebSphere plugin. Here’s how to set it up:

1. **Open Run/Debug Configurations**:
   - In IntelliJ IDEA, go to the top menu and select **Run > Edit Configurations**.

2. **Add a New Remote Debug Configuration**:
   - Click the **+** button (or "Add New Configuration") in the top-left corner.
   - From the list, select **Remote JVM Debug** (it might just say "Remote" depending on your IntelliJ version).

3. **Set Configuration Details**:
   - **Name**: Give it a meaningful name, e.g., "WebSphere Liberty Debug."
   - **Host**: Set to `localhost` (assuming the server runs on the same machine as IntelliJ IDEA; use the server’s IP address if it’s remote).
   - **Port**: Set to `7777` (or the actual debug port if different).
   - **Transport**: Ensure it’s set to **Socket**.
   - **Debugger Mode**: Select **Attach** (this tells IntelliJ to connect to an already-running JVM).
   - Leave other settings (like "Command line arguments for remote JVM") as default unless you need specific JVM options.

4. **Save the Configuration**:
   - Click **Apply** and then **OK** to save.

---

### Step 4: Start Debugging

With the server running in debug mode and the configuration set up:

- Go to **Run > Debug** (or click the bug icon) and select your new configuration (e.g., "WebSphere Liberty Debug").
- IntelliJ IDEA will attempt to attach to the server’s JVM on the specified host and port.
- If successful, you’ll see a message in the Debug window like "Connected to the target VM, address: 'localhost:7777'."

---

### Step 5: Debug Your Application

- **Set Breakpoints**: In your source code, click in the gutter next to the line numbers to add breakpoints where you want execution to pause.
- **Trigger Execution**: Interact with your application (e.g., send a request to the server) to hit the breakpoints.
- **Debug**: Once a breakpoint is hit, use IntelliJ’s debugging tools (step over, step into, resume, etc.) to inspect variables and control execution.

---

### Additional Notes

- **Local vs. Remote Server**: If WebSphere Liberty is running on a different machine, replace `localhost` with the server’s IP address in the remote debug configuration. Ensure the debug port (e.g., 7777) is open and not blocked by a firewall.
- **Port Conflicts**: If port 7777 is unavailable when the server starts, WebSphere Liberty might pick a random port. Check the server output to confirm the port and update the IntelliJ configuration accordingly.
- **No Plugin Needed**: This method uses IntelliJ IDEA’s standard remote debugging feature, so no WebSphere Liberty plugin is required.

---

### Summary

By starting your WebSphere Liberty Server with `server debug default` (which enables debugging on port 7777 by default) and configuring a remote debug setup in IntelliJ IDEA, you can connect to the server’s debug port without the WebSphere Liberty plugin. This gives you full debugging capabilities—breakpoints, variable inspection, and step-through execution—directly within IntelliJ IDEA.

---

Running and debugging WebSphere Liberty applications in IntelliJ IDEA without the dedicated Liberty Tools plugin is achievable by manually setting up the Liberty runtime and configuring IntelliJ IDEA for remote debugging and external tool execution. This approach requires a few manual steps compared to using the integrated plugin, but it provides the necessary functionality to develop and troubleshoot your Liberty applications.

Here's a breakdown of the process:

**1. Obtain and Install WebSphere Liberty Runtime:**

Since you don't have the plugin to manage the runtime for you, you'll need to download and install the WebSphere Liberty runtime manually. You can obtain the runtime from the official IBM website or through other distribution methods like Maven or Gradle if you're managing your project with those tools.

Typically, the manual installation involves downloading a ZIP or JAR file and extracting it to a directory on your system. This directory will be your Liberty installation home (`<LIBERTY_HOME>`).

**2. Configure Liberty Server for Debugging:**

To debug your application, you need to start the Liberty server with debugging enabled. This is done by adding specific JVM options when the server starts. These options tell the Java Virtual Machine (JVM) to listen for a debugger connection on a specific port.

Locate the `jvm.options` file in your Liberty server configuration directory (`<LIBERTY_HOME>/usr/servers/<your_server_name>/`). If this file doesn't exist, you can create it. Add the following line to the `jvm.options` file:

```
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
```

- `-agentlib:jdwp`: Loads the Java Debug Wire Protocol (JDWP) library.
- `transport=dt_socket`: Specifies that the debugger will connect using a socket.
- `server=y`: Indicates that the JVM will act as the server, listening for a debugger connection.
- `suspend=n`: Specifies that the JVM should not wait for the debugger to connect before starting. You can change this to `suspend=y` if you need to debug code that runs during server startup.
- `address=5005`: Sets the port number the debugger will connect to. You can change this to any available port.

**3. Configure IntelliJ IDEA to Run Liberty:**

You can use IntelliJ IDEA's "External Tools" configuration to start your Liberty server from within the IDE.

- Go to `File` \> `Settings` (or `IntelliJ IDEA` \> `Preferences` on macOS).
- Navigate to `Tools` \> `External Tools`.
- Click the `+` icon to add a new external tool.
- Configure the tool with the following details:
  - **Name:** Give it a descriptive name, e.g., "Start Liberty Server".
  - **Program:** Browse to the Liberty server script. This will typically be `<LIBERTY_HOME>/bin/server` for Linux/macOS or `<LIBERTY_HOME>\bin\server.bat` for Windows.
  - **Arguments:** Add the arguments to start your specific server instance. This is usually `start <your_server_name>`, where `<your_server_name>` is the name of your server directory in `<LIBERTY_HOME>/usr/servers/`.
  - **Working directory:** Set this to `<LIBERTY_HOME>/bin`.

Now you can start your Liberty server by going to `Tools` \> `External Tools` and selecting the tool you just configured.

**4. Configure IntelliJ IDEA for Remote Debugging:**

To debug your application running on the manually started Liberty server, you'll use IntelliJ IDEA's "Remote JVM Debug" configuration.

- Go to `Run` \> `Edit Configurations`.
- Click the `+` icon and select `Remote JVM Debug`.
- Configure the settings:
  - **Name:** Give it a descriptive name, e.g., "Debug Liberty Server".
  - **Debugger mode:** Select `Attach to remote JVM`.
  - **Host:** Enter `localhost` (or the IP address of the machine running Liberty if it's not on your local machine).
  - **Port:** Enter the port number you configured in the `jvm.options` file (e.g., `5005`).
  - **Use module classpath of:** Select the module in your IntelliJ IDEA project that contains your Liberty application code. This helps IntelliJ IDEA map the running code to your source files for debugging.

**5. Run and Debug:**

1. Start the Liberty server using the "External Tools" configuration you created in IntelliJ IDEA.
2. Wait for the server to start and indicate that it's listening for the debugger on the configured port (you should see a message in the server console output).
3. Set breakpoints in your application code within IntelliJ IDEA.
4. Go to `Run` \> `Debug` and select the "Debug Liberty Server" configuration you created.

IntelliJ IDEA will attempt to connect to the running Liberty server on the specified port. Once connected, you can use all of IntelliJ IDEA's debugging features, such as stepping through code, inspecting variables, and evaluating expressions.

By following these steps, you can effectively run and debug your WebSphere Liberty applications in IntelliJ IDEA without relying on the dedicated Liberty Tools plugin, giving you direct control over the server lifecycle and debugging process.
