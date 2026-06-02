---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Jython in WebSphere Application Server
translated: false
type: note
---

### Using Jython in IBM WebSphere Application Server

Note: "jPython" refers to Jython, an implementation of Python that runs on the Java Virtual Machine (JVM). It's commonly used in WebSphere for administrative scripting and can also be integrated into deployed applications. WebSphere Application Server (WAS) bundles Jython (typically version 2.1 or later, depending on the WAS version) under `<WAS_HOME>/optionalLibraries/jython`, so no separate installation is usually needed. Below, I'll cover the two primary use cases: administrative tasks and runtime use in applications.

#### 1. Administrative Scripting with wsadmin
The most common way to use Jython in WebSphere is for server management tasks like deploying applications, starting/stopping servers, configuring resources, and listing installed apps. This is done via the `wsadmin` tool, which supports Jython as the preferred scripting language (over the deprecated Jacl).

**Prerequisites:**
- Ensure the WebSphere server is running.
- Locate `wsadmin` in `<WAS_HOME>/bin/wsadmin.sh` (Linux/Unix) or `wsadmin.bat` (Windows).
- Jython is pre-bundled; for newer features (e.g., Python 2.5+ syntax), you may need to upgrade via a custom classpath (see advanced notes below).

**Basic Steps to Run a Jython Script:**
1. Create a Jython script file (e.g., `example.py`) with your code. Use AdminConfig, AdminControl, and AdminApp objects for WebSphere-specific operations.

   Example script to list all installed applications (`listApps.py`):
   ```
   # List all applications
   apps = AdminApp.list()
   print("Installed Applications:")
   for app in apps.splitlines():
       if app.strip():
           print(app.strip())
   AdminConfig.save()  # Optional: Save config changes
   ```

2. Run the script using `wsadmin`:
   - Connect via SOAP (default for remote):
     ```
     wsadmin.sh -lang jython -f listApps.py -host <hostname> -port <soap_port> -user <admin_user> -password <admin_pass>
     ```
   - For local (no host/port):
     ```
     wsadmin.sh -lang jython -f listApps.py
     ```
   - Example output: Lists apps like `DefaultApplication`.

3. For interactive mode (REPL):
   ```
   wsadmin.sh -lang jython
   ```
   Then type Jython commands directly, e.g., `print AdminApp.list()`.

**Common Examples:**
- **Deploy an EAR/WAR:** Create `deployApp.py`:
  ```
  appName = 'MyApp'
  earPath = '/path/to/MyApp.ear'
  AdminApp.install(earPath, '[-appname ' + appName + ' -server server1]')
  AdminConfig.save()
  print('Deployed ' + appName)
  ```
  Run: `wsadmin.sh -lang jython -f deployApp.py`.

- **Start/Stop Server:**
  ```
  server = AdminControl.completeObjectName('type=Server,process=server1,*')
  AdminControl.invoke(server, 'start')  # Or 'stop'
  ```

- **Specify Jython Version (if needed):** For Jython 2.1 explicitly:
  `wsadmin.sh -usejython21 true -f script.py`. For custom versions, add to classpath: `-wsadmin_classpath /path/to/jython.jar`.

**Tips:**
- Use `AdminConfig.help('object_type')` for command help.
- Scripts can be automated in CI/CD (e.g., Jenkins) by calling `wsadmin` in batch files.
- For thin client (no full WAS install): Download client jars from IBM and set classpath.

#### 2. Using Jython in Deployed Applications
To execute Jython code within a Java application (e.g., servlet or EJB) running on WebSphere, include the Jython runtime (jython.jar) in the application's classpath. This allows embedding Python scripts or using Jython as a scripting engine. Download the latest jython.jar from the official Jython site if the bundled version is outdated.

There are two main methods: **Classpath** (server-wide) or **Shared Library** (reusable across apps).

**Method 1: Classpath (Direct Addition to JVM)**
1. Save `jython.jar` to an accessible path on the WebSphere host (e.g., `/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/mylibs/jython.jar`).
2. Log in to the WebSphere Admin Console.
3. Navigate to **Servers > Server Types > WebSphere application servers > [Your Server]**.
4. Go to **Java and Process Management > Process definition > Java Virtual Machine > Classpath**.
5. Add the full path to `jython.jar` (e.g., `/opt/.../jython.jar`).
6. In **Generic JVM arguments**, add the Python path:
   `-Dpython.path=/opt/.../jython.jar/Lib` (points to Jython's standard library).
7. Click **OK**, save the configuration, and restart the server.
8. Synchronize nodes if in a clustered environment (via **System administration > Nodes > Synchronize**).
9. In your Java code, use `org.python.util.PythonInterpreter` to run Jython scripts:
   ```
   import org.python.util.PythonInterpreter;
   PythonInterpreter interpreter = new PythonInterpreter();
   interpreter.exec("print('Hello from Jython in WebSphere!')");
   ```

**Method 2: Shared Library (Recommended for Multiple Apps)**
1. Place `jython.jar` in a shared directory (e.g., `/shared/libs/jython.jar`).
2. In Admin Console: **Environment > Shared libraries > [Scope: Server or Cell] > New**.
3. Enter a name (e.g., `JythonLib`), check **Use a native library directory**, and set **Classpath** to `/shared/libs/jython.jar`.
4. Save.
5. For a specific application: **Applications > Application Types > WebSphere enterprise applications > [Your App] > Reference shared libraries**.
6. Under **Shared library references**, click **Add**, select `JythonLib`, and set **Classpath** to match.
7. Save, update the app (restart if needed), and synchronize nodes.
8. Reference in code as in the Classpath method.

**Tips for Apps:**
- For servlet-based Jython apps, use PyServlet (included in Jython) for Python handlers.
- Test in a dev environment; monitor logs for classpath issues.
- If using newer Jython (e.g., 2.7), ensure Java 8+ compatibility.

#### Advanced Notes
- **Version Compatibility:** WAS 9.x uses Jython 2.7+. For upgrades, replace the bundled jar but test thoroughly.
- **Error Handling:** In scripts, use `try: ... except Exception as e: print(e)`.
- **IDE Support:** Use IBM Rational Application Developer (RAD) or Eclipse with WebSphere plugins for debugging Jython/wsadmin scripts.
- **Resources:** For full tutorials, see the book *WebSphere Application Server Administration Using Jython* or IBM's wsadmin docs.

If this doesn't match your exact scenario (e.g., specific WAS version or use case), provide more details for tailored advice.

**References:**
- [Using wsadmin scripting with Jython (IBM Docs)](https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-using-wsadmin-jython)
- [Deploying Jython on WebSphere (Oracle Guide)](https://docs.oracle.com/en/applications/jd-edwards/cross-product/9.2/eotos/deploying-jython-on-ais-server-on-ibm-websphere-application.html)
- [WebSphere Jython Integration (Stack Overflow)](https://stackoverflow.com/questions/25187577/will-the-ibm-websphere-application-server-run-the-python-jython-script-without-p)
- [Jython Wiki on WebSphere](https://wiki.python.org/jython/WebSphere)
- [Deploy App with Jython Example](https://jobhunterssite.wordpress.com/2016/05/12/deploy-an-application-in-websphere-using-jython-automation/)
