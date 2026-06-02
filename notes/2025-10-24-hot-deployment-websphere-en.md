---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Hot Deployment in WebSphere WAS
translated: false
type: note
---

### Understanding Hot Deployment and Hotswap in WebSphere Application Server (WAS)

Hot deployment (also known as hot reloading or hot swapping) is a development technique that allows you to update and deploy changes to your application—such as code, configuration, or resources—without requiring a full restart of the application server. This is particularly valuable during iterative development cycles, where frequent code changes (e.g., fixing bugs, tweaking logic, or updating UI elements) would otherwise be slowed down by lengthy server startup times, especially in enterprise environments like IBM WebSphere Application Server (WAS). Restarting a WAS instance can take minutes or even longer for large applications, disrupting workflows and testing.

The snippet you provided focuses on practical strategies for achieving faster iterations in WAS, emphasizing "exploded" WAR deployments and tools for enhanced hot swapping. I'll break this down step by step, explaining the concepts, how they work, their limitations, and implementation tips.

#### 1. Deploying as an "Exploded" WAR (Unpacked Deployment)
A WAR (Web Application Archive) file is essentially a zipped bundle containing your web application's resources: JSPs, servlets, Java classes, static files (HTML/CSS/JS), libraries (JARs), and configuration files (e.g., web.xml). By default, WARs are deployed as **packaged** (zipped) files, which WAS treats as immutable—any change requires repackaging and redeploying the entire archive.

An **exploded WAR** refers to unpacking (unzipping) the WAR file into a directory structure before deployment. This allows individual files or subdirectories to be modified directly on the server's filesystem without touching the entire archive.

**Why it enables faster iterations:**
- **File-level updates:** You can edit a single JSP or Java class file, and WAS can detect and reload just that component.
- **No repackaging:** Avoids the overhead of zipping/unzipping large WARs repeatedly.
- **Synergy with hot reloading:** Makes it easier for the server to monitor and refresh changed files.

**How to deploy an exploded WAR in WAS:**
- **Using the Admin Console:**
  1. Log into the WAS Integrated Solutions Console (typically at `http://localhost:9060/ibm/console`).
  2. Navigate to **Applications > New Application > New Enterprise Application**.
  3. Instead of selecting a packaged WAR file, point to the root directory of your unpacked WAR (e.g., `/path/to/myapp.war/`—note the trailing slash to indicate it's a directory).
  4. Complete the deployment wizard, ensuring "Deploy Web services" and other options match your app.
- **Using wsadmin (scripting tool):**
  ```bash
  wsadmin.sh -c "AdminApp.install('/path/to/myapp', '[ -MapWebModToVH [[myapp .* default_host.* virtual_host ]]]')"
  ```
  Replace `/path/to/myapp` with your exploded directory.
- **Development servers (e.g., Liberty Profile):** For lighter testing, use Open Liberty (a WAS variant) with `server start` and place your exploded app in the `dropins` folder for automatic deployment.

**Best practices:**
- Use a source control tool (e.g., Git) to sync changes from your IDE to the exploded directory.
- Monitor disk space, as exploded deployments consume more storage.
- In production, stick to packaged WARs for security and consistency—hot deployment is mainly for dev/test.

Once deployed exploded, WAS's built-in mechanisms can kick in for partial hot reloading.

#### 2. WAS's Built-in Hot-Reload Support
WAS provides native support for hot reloading certain components without a full restart, but it's limited. This relies on the server's **file polling** mechanism, where WAS periodically scans the exploded deployment directory for changes (configurable via JVM args like `-DwasStatusCheckInterval=5` for 5-second checks).

**What WAS supports out-of-the-box:**
- **JSPs (JavaServer Pages):**
  - JSPs are dynamically compiled into servlets on first access. If you modify a JSP file in an exploded WAR, WAS can detect the change, recompile it, and reload the servlet.
  - **How it works:** Set `reloadInterval` in `ibm-web-ext.xmi` (under WEB-INF) to a low value (e.g., 1 second) for frequent checks. Or use the global setting in **Servers > Server Types > WebSphere application servers > [your_server] > Java and Process Management > Process definition > Java Virtual Machine > Custom properties** with `com.ibm.ws.webcontainer.invokefilterscompatibility=true`.
  - **Limitations:** Only works for JSPs that haven't been cached aggressively. Complex JSPs with includes or tags might require a module restart.
- **Some Java classes (servlets and EJBs):**
  - For exploded deployments, WAS can reload individual class files if they're in the WEB-INF/classes or lib directories.
  - **How it works:** Enable "Application reload" in the deployment descriptor or via console: **Applications > [your_app] > Manage Modules > [module] > Reload behavior > Reload enabled**.
  - This triggers a **module-level reload**, which is faster than a full app restart but still unloads/reloads the entire module (e.g., your web app).

**Limitations of built-in support:**
- **Not true hotswap:** Changes to core application logic (e.g., modifying a method in a running servlet class) won't take effect without unloading the old classloader. You might see `ClassNotFoundException` or stale code.
- **State loss:** Sessions, singletons, or database connections may reset.
- **IBM JDK specifics:** WAS often uses IBM's JDK, which has quirks with class reloading compared to OpenJDK/HotSpot.
- **No support for structural changes:** Adding new classes, changing method signatures, or updating annotations requires a restart.
- **Performance overhead:** Frequent polling can strain resources in dev.

For basic UI tweaks (JSP edits) or simple class updates, this is sufficient and free. But for "full hotswap"—where you can edit running code mid-execution without any reload—you need third-party tools.

#### 3. Full Hotswap Solutions
To achieve seamless code changes (e.g., editing a method body in a debugger-attached IDE like Eclipse or IntelliJ, and seeing it apply instantly), use plugins that patch the JVM's class loading and instrumentation.

**Option 1: JRebel (Paid Plugin)**
- **What it is:** A commercial tool from Perforce (formerly ZeroTurnaround) that provides comprehensive hotswap for Java apps. It instruments your bytecode at startup, allowing reloads of classes, resources, and even framework-specific changes (e.g., Spring beans, Hibernate entities).
- **Why use it with WAS:**
  - Deep integration with WAS, including support for exploded WARs, OSGi bundles, and IBM JDK.
  - Handles complex scenarios like changing method signatures or adding fields (beyond standard JVMTI hotswap limits).
  - **Features:** Automatic detection of changes from your IDE; no manual redeploys; preserves app state.
- **How to set it up:**
  1. Download JRebel from the official site and install as an Eclipse/IntelliJ plugin.
  2. Generate a `rebel.xml` config file for your project (auto-generated or manual).
  3. Add JVM args to your WAS server: `-javaagent:/path/to/jrebel.jar` (full path to the agent JAR).
  4. Start WAS in debug mode (`-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8000`).
  5. Attach your IDE debugger and edit code—JRebel syncs changes live.
- **Cost:** Subscription-based (~$400/user/year for individuals; enterprise licensing varies). Free trial available.
- **Pros:** Reliable, user-friendly, excellent WAS support.
- **Cons:** Paid; requires setup per project.

**Option 2: DCEVM + HotSwapAgent (Free Alternative)**
- **What it is:** An open-source combo for advanced hotswapping.
  - **DCEVM (Dynamic Code Evolution VM):** A modified JVM that extends HotSpot's JVMTI (Java Virtual Machine Tool Interface) to allow more aggressive class redefinitions (e.g., adding/removing methods, changing hierarchies).
  - **HotSwapAgent:** An agent that builds on DCEVM, providing IDE integration for automatic class reloading.
- **Why use it with WAS:**
  - Free and powerful for dev, mimicking JRebel's capabilities.
  - Supports method body changes, resource updates, and even some framework reloads (via plugins).
- **Compatibility note with WAS's IBM JDK:**
  - WAS typically ships with IBM's J9 JDK, which **does not support DCEVM** natively (DCEVM is HotSpot-specific).
  - **Workaround:** Switch to OpenJDK/HotSpot for development (e.g., via `JAVA_HOME` override in `setInitial.sh` or Liberty's `jvm.options`). Test thoroughly—IBM JDK's garbage collection and security features might differ.
  - In production, revert to IBM JDK; this is dev-only.
- **How to set it up:**
  1. **Install DCEVM:**
     - Download the DCEVM patcher JAR from GitHub (e.g., `dcevm-11.0.0+7-full.jar` for JDK 11+).
     - Run: `java -jar dcevm.jar /path/to/your/jdk/jre/lib/server/jvm.dll server` (Windows) or equivalent for Linux (`libjvm.so`).
     - This patches your JDK's JVM binary—backup first!
  2. **Install HotSwapAgent:**
     - Download `hotswap-agent.jar` from GitHub.
     - Add to WAS JVM args: `-XXaltjvm=dcevm -XX:+TraceClassLoading -javaagent:/path/to/hotswap-agent.jar=DCEVM` (plus any plugins, e.g., `=hotswap-spring` for Spring).
  3. **IDE integration:**
     - Install the HotSwapAgent plugin for IntelliJ/Eclipse.
     - Start WAS with debug args as above.
     - Edit and save code in IDE—agent reloads automatically.
  4. **Testing compatibility:**
     - Run a smoke test: Deploy a simple servlet, edit a method (e.g., add a log line), hit the endpoint, and verify the change without restart.
     - Check logs for errors like `HotSwap failed: method limit reached` (DCEVM has limits on changes per class).
- **Pros:** Free, customizable (via plugins for Spring, CDI, etc.), community-supported.
- **Cons:** Setup is fiddly; potential instability with non-standard JVMs; limited to HotSpot (test IBM JDK switch carefully); not as polished as JRebel.

#### When to Use What
- **Exploded WAR + Built-in reload:** For quick JSP/static file tweaks in early dev.
- **JRebel:** If budget allows and you need enterprise-grade reliability.
- **DCEVM + HotSwapAgent:** For cost-free full hotswap, but allocate time for JVM compatibility testing.

In summary, these techniques transform WAS from a heavyweight server into a more agile dev environment, cutting iteration times from minutes to seconds. Start with exploded WARs for immediate gains, then layer on tools as needed. If you're hitting specific errors, share more details for troubleshooting.

**References:**
[JRebel Documentation for WebSphere](https://www.jrebel.com/products/jrebel/tutorials/deploy-jrebel-websphere)
[DCEVM GitHub Repo](https://github.com/dcevm/dcevm)
[HotSwapAgent GitHub Repo](https://github.com/HotswapProjects/HotswapAgent)
[IBM Knowledge Center: WebSphere Hot Deployment](https://www.ibm.com/docs/en/was/9.0.5?topic=applications-hot-deployment)
