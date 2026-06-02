---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: IntelliJ IDEA for WebSphere Development
translated: false
type: note
---

### Using IntelliJ IDEA for IBM WebSphere Application Server (WAS) Development

IntelliJ IDEA is a solid choice for developing Java EE applications targeted at IBM WebSphere Application Server (WAS). It supports Java EE standards, which WAS adheres to, and offers excellent tooling for building, deploying, and debugging enterprise apps. While Eclipse has more native WAS integration via IBM's tools, IntelliJ works well with some setup. Below, I'll cover the basics, remote debugging (yes, you can attach to the WAS JVM), and additional tips.

#### 1. Initial Setup for WAS Development in IntelliJ
- **Install Required Plugins**:
  - Go to **File > Settings > Plugins** and search for "WebSphere Server" in the JetBrains Marketplace. Install it for better local server management (e.g., starting/stopping WAS from IntelliJ). This plugin isn't bundled, so it's optional but recommended for local dev.
  - Ensure you have the Java EE and Jakarta EE plugins enabled (they're usually pre-installed).

- **Create a Project**:
  - Start a new **Java Enterprise** project (or import an existing one).
  - Select **Web Application** archetype and configure for Java EE (e.g., version 8 or 9, depending on your WAS version like 9.x).
  - Add dependencies for WAS-specific libs if needed (e.g., via Maven/Gradle: `com.ibm.websphere.appserver.api:jsp-2.3` for JSP support).

- **Configure Local WAS Server (Optional for Local Runs)**:
  - Go to **Run > Edit Configurations > + > WebSphere Server > Local**.
  - Point to your local WAS installation directory (e.g., `/opt/IBM/WebSphere/AppServer`).
  - Set the server name, JRE (use IBM's JDK if bundled with WAS), and deployment options (e.g., exploded WAR for hot-reload).
  - For deployment: In the **Deployment** tab, add your artifact (e.g., WAR file) and set context path.

This setup lets you run/deploy directly from IntelliJ for local testing.

#### 2. Remote Debugging: Attaching IntelliJ to the WAS JVM
Yes, you can absolutely attach the IntelliJ debugger to a remote WAS JVM. This is standard Java remote debugging via JDWP (Java Debug Wire Protocol). It works for both local and remote WAS instances—treat the server as a "remote JVM."

**Step 1: Enable Debugging on the WAS Server**
- **Via Admin Console (Recommended for Production-Like Setups)**:
  - Log into the WAS Admin Console (e.g., `https://your-host:9043/ibm/console`).
  - Navigate to **Servers > Server Types > WebSphere Application Servers > [Your Server] > Debugging Service**.
  - Check **Enable service at server startup**.
  - Set **JVM debug port** (default is 7777; choose an unused port like 8000 to avoid conflicts).
  - Save and restart the server.

- **Via server.xml (For Standalone or Quick Edits)**:
  - Edit `$WAS_HOME/profiles/[Profile]/config/cells/[Cell]/nodes/[Node]/servers/[Server]/server.xml`.
  - In the `<jvmEntries>` section under `<processDefinitions>`, add or update:
    ```
    <jvmEntries xmi:id="..." debugMode="true">
      <debugArgs>-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000</debugArgs>
    </jvmEntries>
    ```
    - `suspend=n` starts the server normally (use `suspend=y` to pause on startup).
    - Replace `8000` with your port.
  - Save, then restart the server: `./startServer.sh [ServerName]` (or via console).

- Verify: Check server logs for "JDWP: transport=dt_socket, address=*:8000" or similar.

**Step 2: Configure Remote Debug in IntelliJ**
- Go to **Run > Edit Configurations > + > Remote JVM Debug**.
- Name it (e.g., "WAS Remote Debug").
- Set **Debugger mode** to "Attach to remote JVM".
- **Host**: Your WAS server IP/hostname (e.g., `localhost` for local, `192.168.1.100` for remote).
- **Port**: The JVM debug port (e.g., 8000).
- Optionally, set **Use module classpath** if your project has specific libs.
- Apply and close.

**Step 3: Attach and Debug**
- Set breakpoints in your code (e.g., in a servlet or EJB).
- Deploy your app to WAS (manually via Admin Console or wsadmin scripts).
- Run the debug configuration (**Run > Debug 'WAS Remote Debug'**).
- Trigger your app (e.g., via HTTP request). IntelliJ will attach, and execution will pause at breakpoints.
- Common issues: Firewall blocking the port, mismatched JDK versions (use WAS's IBM JDK in IntelliJ), or server not restarted after config changes.

This works for WAS 7+ (including Liberty profile). For remote servers, ensure network access to the debug port.

#### 3. Other Tips for Efficient WAS Development
- **Hot Deployment/Hotswap**: For faster iterations, deploy as an "exploded" WAR (unpacked). WAS supports hot-reload for JSPs and some classes, but for full hotswap (code changes without restart), use JRebel plugin (paid) or DCEVM + HotSwapAgent (free, but test compatibility with WAS's IBM JDK).

- **Build Tools**: Use Maven or Gradle for dependencies. Add WAS runtime libs as provided scope to avoid classpath bloat:
  ```
  <dependency>
    <groupId>com.ibm.websphere.appserver.runtime</groupId>
    <artifactId>shared</artifactId>
    <version>9.0.5</version>
    <scope>provided</scope>
  </dependency>
  ```
  Run `mvn clean package` and deploy the WAR via Admin Console.

- **Logging and Profiling**: Integrate SLF4J/Logback for app logs. For performance, use VisualVM or YourKit (attach remotely like debugging). WAS's PMI (Performance Monitoring Infrastructure) is great—enable it in Admin Console for metrics.

- **Testing**: Use Arquillian for integration tests against a remote WAS. Or embed Open Liberty (WAS-compatible) for local unit tests without full WAS.

- **Version-Specific Notes**: For WAS 9.x+, leverage Jakarta EE migration tools in IntelliJ. If using WAS Liberty (microprofile-focused), the Liberty Tools plugin adds dev mode with auto-reload.

- **Common Pitfalls**:
  - Classpath issues: Ensure IntelliJ's project SDK matches WAS's JDK.
  - Security: Remote debug exposes the port—use only in dev/trusted networks.
  - Plugin Limitations: The WebSphere plugin is basic; for advanced features, consider IBM's Rational Application Developer (but stick to IntelliJ for its UX).

This should get you up and running. If you're on a specific WAS version, share details for more tailored advice.

#### References
- [Run/Debug Configuration: WebSphere Server | IntelliJ IDEA](https://www.jetbrains.com/help/idea/run-debug-configuration-websphere-server.html)
- [WebSphere remote server debug configuration in IntelliJ Idea](https://stackoverflow.com/questions/33013860/websphere-remote-server-debug-configuration-in-intellij-idea)
- [Debug code running on IBM Websphere using Eclipse / Intellij IDEA](https://davanum.wordpress.com/2009/11/20/debug-code-running-on-ibm-websphere-using-eclipse-intellij-idea/)
- [Debugging applications - IBM](https://www.ibm.com/docs/en/was/9.0.5?topic=applications-debugging)
- [Remote Debugging with IntelliJ IDEA | Baeldung](https://www.baeldung.com/intellij-remote-debugging)
