---
audio: false
generated: true
lang: en
layout: post
title: Integrating YourKit Profiler with WebSphere Liberty on Windows
translated: false
type: note
---

Using YourKit Java Profiler with WebSphere Liberty Server on Windows involves integrating the YourKit agent into the WebSphere Liberty JVM and configuring it for profiling. Below are the steps to set this up, based on available information and best practices for YourKit and WebSphere Liberty integration:

### Prerequisites
- **YourKit Java Profiler**: Installed on your Windows machine. Download from [YourKit's official site](https://www.yourkit.com/) and ensure you have a valid license or trial key.
- **WebSphere Liberty**: Installed and running on your Windows system. Ensure you have administrative access to the server configuration files.
- **Java JDK**: WebSphere Liberty uses a Java runtime (IBM JDK or OpenJDK). Confirm the JDK version is compatible with YourKit (YourKit supports Java 5 and later, but verify compatibility with your specific version).
- **Administrative Privileges**: Required to modify WebSphere Liberty configuration files.

### Step-by-Step Guide

1. **Install YourKit Java Profiler**
   - Download and install the YourKit Java Profiler for Windows from [YourKit's website](https://www.yourkit.com/download).
   - Note the installation directory, as you'll need the path to the YourKit agent library (`yjpagent.dll`).

2. **Locate the YourKit Agent**
   - The YourKit agent for Windows is typically located at:
     ```
     C:\Program Files\YourKit-Java-Profiler-<version>\bin\win64\yjpagent.dll
     ```
     (Use `win32` instead of `win64` if running a 32-bit JVM.)
   - Ensure the agent matches the JVM architecture (32-bit or 64-bit) used by WebSphere Liberty.

3. **Configure WebSphere Liberty to Use the YourKit Agent**
   - **Locate the `jvm.options` File**:
     - Navigate to your WebSphere Liberty server’s configuration directory, typically:
       ```
       <LIBERTY_INSTALL_DIR>\usr\servers\<server_name>\jvm.options
       ```
       Replace `<LIBERTY_INSTALL_DIR>` with the path to your WebSphere Liberty installation (e.g., `C:\wlp`), and `<server_name>` with the name of your server (e.g., `defaultServer`).
     - If the `jvm.options` file doesn’t exist, create it in the server directory.
   - **Add the YourKit Agent Path**:
     - Open `jvm.options` in a text editor with administrative privileges.
     - Add the following line to include the YourKit agent:
       ```
       -agentpath:C:\Program Files\YourKit-Java-Profiler-<version>\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
       ```
       - Replace `<version>` with your YourKit version (e.g., `2023.9`).
       - The options (`disablestacktelemetry`, `disableexceptiontelemetry`, `probe_disable=*`) reduce overhead by disabling unnecessary telemetry. The `delay=10000` ensures the agent starts after the server initializes, and `sessionname=WebSphereLiberty` identifies the profiling session.
       - Example:
         ```
         -agentpath:C:\Program Files\YourKit-Java-Profiler-2023.9\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
         ```
   - **Save the File**: Ensure you have write permissions for the `jvm.options` file.

4. **Verify JVM Compatibility**
   - WebSphere Liberty often uses IBM JDK or OpenJDK. YourKit is compatible with both, but if you encounter issues (e.g., `NoSuchMethodError` as noted in some IBM JDK cases), add `probe_disable=*` to the agent path to disable probes that may cause conflicts with IBM JDK.[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=8042)
   - Check the Java version used by Liberty:
     ```
     <LIBERTY_INSTALL_DIR>\java\bin\java -version
     ```
     Ensure it’s supported by YourKit (Java 5 or later for older versions; modern versions support Java 8+).

5. **Start WebSphere Liberty**
   - Start your WebSphere Liberty server as usual:
     ```
     <LIBERTY_INSTALL_DIR>\bin\server start <server_name>
     ```
     Example:
     ```
     C:\wlp\bin\server start defaultServer
     ```
   - Check the server logs (`<LIBERTY_INSTALL_DIR>\usr\servers\<server_name>\logs\console.log` or `messages.log`) for any errors related to the YourKit agent.
   - Look for the YourKit agent log in:
     ```
     %USERPROFILE%\.yjp\log\<session_name>-<pid>.log
     ```
     Example:
     ```
     C:\Users\<YourUsername>\.yjp\log\WebSphereLiberty-<pid>.log
     ```
     The log should indicate the agent is loaded and listening on a port (default: 10001):
     ```
     Profiler agent is listening on port 10001
     ```

6. **Connect YourKit Profiler UI**
   - Launch the YourKit Java Profiler UI on your Windows machine.
   - In the YourKit UI, select **Profile | Profile Local Java Server or Application** or **Profile | Profile Remote Java Server or Application**.
     - For local profiling (since YourKit and Liberty are on the same machine), choose **Profile Local Java Server or Application**.
     - The UI should detect the WebSphere Liberty process (identified by `sessionname=WebSphereLiberty`).
   - If not detected automatically, use **Profile Remote Java Server or Application**, select **Direct Connect**, and enter:
     - **Host**: `localhost`
     - **Port**: `10001` (or the port specified in the agent log).
   - Connect to the server. The UI will display CPU, memory, and thread telemetry.

7. **Profile the Application**
   - Use the YourKit UI to:
     - **CPU Profiling**: Enable CPU sampling or tracing to identify performance bottlenecks. Avoid enabling “Profile J2EE” for high-load systems to minimize overhead.[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)
     - **Memory Profiling**: Analyze heap usage and detect memory leaks by grouping objects by web application (useful for Liberty-hosted apps).[](https://www.yourkit.com/docs/java-profiler/latest/help/webapps.jsp)
     - **Thread Analysis**: Check for deadlocks or frozen threads in the Threads tab.[](https://www.yourkit.com/changes/)
   - Take snapshots for offline analysis if needed (File | Save Snapshot).
   - Monitor memory usage, as profiling can increase memory consumption. Avoid long profiling sessions without monitoring.[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

8. **Troubleshooting**
   - **Server Fails to Start or Becomes Unreachable**:
     - Check logs (`console.log`, `messages.log`, and YourKit agent log) for errors like `OutOfMemoryError` or `NoSuchMethodError`.[](https://www.yourkit.com/forum/viewtopic.php?t=328)[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
     - Ensure the `-agentpath` is added to the correct `jvm.options` file and matches the script used to start Liberty.[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
     - If using IBM JDK, try adding `probe_disable=*` to the agent path to avoid conflicts.[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=8042)
   - **ClassNotFoundException**:
     - If you see errors like `java.lang.ClassNotFoundException` (e.g., for `java.util.ServiceLoader`), ensure the YourKit agent version is compatible with your JDK. For older IBM JDKs (e.g., Java 5), use YourKit 8.0 or earlier.[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=7149)
   - **No Profiling Data**:
     - Verify the YourKit agent and UI versions match. Mismatched versions can cause connection issues.[](https://www.yourkit.com/forum/viewtopic.php?t=328)
     - Ensure the server is accessible via the browser (e.g., `https://localhost:9443` if using SSL). If not, check firewall settings or SSL configuration.[](https://www.yourkit.com/forum/viewtopic.php?t=16205)
   - **Log File Issues**:
     - If no YourKit log is created in `~/.yjp/log/`, ensure the process has write permissions to the user’s home directory.[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=3219)
   - **Performance Impact**:
     - Profiling can impact performance. Use minimal settings (e.g., disable stack telemetry) for production-like environments.[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

9. **Optional: Use the YourKit Integration Wizard**
   - YourKit provides a Java Server Integration Wizard to simplify configuration:
     - Launch the YourKit UI and select **Profile | Profile Local Java Server or Application**.
     - Choose **WebSphere Liberty** from the list of supported servers (or “Other Java application” if Liberty isn’t listed).
     - Follow the wizard to generate the necessary `-agentpath` settings and update `jvm.options`. Ensure you have write permissions for the configuration files.[](https://www.yourkit.com/docs/java-profiler/latest/help/java-server-integration-wizard.jsp)
   - This is particularly useful for ensuring correct paths and settings.

10. **Stop Profiling**
    - To disable profiling, remove or comment out the `-agentpath` line in `jvm.options` and restart the server.
    - Alternatively, stop the server:
      ```
      <LIBERTY_INSTALL_DIR>\bin\server stop <server_name>
      ```

### Additional Notes
- **License**: No license key is required for the YourKit agent on the server; the license is applied in the YourKit UI. For remote profiling from another Windows machine, ensure the UI has a valid license.[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=11385)[](https://www.yourkit.com/forum/viewtopic.php?t=11385)
- **Remote Profiling**: If profiling from a different machine, ensure network connectivity to the agent port (default: 10001) and use the **Profile Remote Java Server or Application** option with the server’s hostname/IP.
- **Performance Considerations**: Profiling can increase memory and CPU usage. For production systems, start with minimal profiling options (e.g., CPU sampling) and monitor server health.[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)
- **Compatibility**: If using an older WebSphere Liberty version with IBM JDK 1.4.2 or 1.5, you may need an older YourKit version (e.g., 8.0 for Java 5).[](https://www.yourkit.com/forum/viewtopic.php?f=3&t=7149)[](https://stackoverflow.com/questions/61795/java-profiler-for-ibm-jvm-1-4-2-websphere-6-0-2)
- **Documentation**: Refer to YourKit’s official documentation for detailed profiling options: [YourKit Java Profiler Help](https://www.yourkit.com/docs/java/help/).[](https://www.jahia.com/blog/analyzing-system-performance-with-yourkit-java-profiler)

### Example Configuration
Here’s a sample `jvm.options` file:
```
-Xmx4G
-Xms4G
-agentpath:C:\Program Files\YourKit-Java-Profiler-2023.9\bin\win64\yjpagent.dll=disablestacktelemetry,disableexceptiontelemetry,delay=10000,probe_disable=*,sessionname=WebSphereLiberty
```

### Testing the Setup
- After starting the server, access your application (e.g., `https://localhost:9443`) to ensure it’s running.
- In the YourKit UI, verify that telemetry data (CPU, memory, threads) is displayed.
- If issues arise, check the YourKit agent log and Liberty logs for errors.

If you encounter specific errors or need help with a particular step, let me know, and I can provide further assistance!
