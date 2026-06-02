---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: WebSphere Development with Eclipse
translated: false
type: note
---

### Developing with IBM WebSphere Application Server (WAS) in Eclipse

IBM WebSphere Application Server (WAS) is a Java EE application server, and Eclipse serves as an excellent IDE for developing, assembling, and deploying applications to it. The primary tool for this integration is the **IBM WebSphere Application Server Developer Tools for Eclipse** (often abbreviated as WDT). This plugin provides server management, project creation, deployment, and debugging capabilities directly within Eclipse. It supports both traditional WAS (e.g., v8.5 and v9.x) and the lightweight Liberty profile.

#### Required Plugin
- **IBM WebSphere Application Server Developer Tools for Eclipse**: This is the essential plugin. Choose the version matching your WAS runtime (e.g., V8.5x or V9.x tools). It's available for free on the Eclipse Marketplace and supports recent Eclipse releases like 2024-06 or 2025-03.

No other plugins are strictly required, but for full Java EE development, ensure your Eclipse installation includes the Web Tools Platform (WTP), which is standard in the Eclipse IDE for Java EE Developers package.

#### Prerequisites
- Eclipse IDE for Java EE Developers (version 2023-09 or later recommended for compatibility).
- IBM WAS runtime installed locally (traditional or Liberty) for testing and deployment.
- Internet access for Marketplace installation (or download offline files).

#### Installation Steps
You can install WDT via the Eclipse Marketplace (easiest method), update site, or downloaded files. Restart Eclipse after installation.

1. **Via Eclipse Marketplace** (Recommended):
   - Open Eclipse and go to **Help > Eclipse Marketplace**.
   - Search for "IBM WebSphere Application Server Developer Tools".
   - Select the appropriate version (e.g., for V9.x or V8.5x).
   - Click **Install** and follow the prompts. Accept licenses and restart Eclipse when done.

2. **Via Update Site**:
   - Go to **Help > Install New Software**.
   - Click **Add** and enter the update site URL (e.g., `https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/wasdev/updates/wdt/2025-03_comp/` for recent versions—check IBM docs for the latest).
   - Select the WDT features (e.g., WebSphere Application Server V9.x Developer Tools) and install.

3. **From Downloaded Files** (Offline Option):
   - Download the ZIP archive from the [IBM Developer site](https://www.ibm.com/docs/en/wasdtfe?topic=installing-websphere-developer-tools) (e.g., `wdt-update-site_<version>.zip`).
   - Extract to a local folder.
   - In Eclipse, go to **Help > Install New Software > Add > Archive** and select the extracted site's `site.xml`.
   - Select and install the desired features, then restart.

After installation, verify by checking **Window > Show View > Servers**—WAS should appear as a server type option.

#### Basic Steps to Develop and Deploy WAS Applications
Once installed, you can create, build, and run Java EE applications targeted at WAS.

1. **Create a New Project**:
   - Go to **File > New > Project**.
   - Select **Web > Dynamic Web Project** (for web apps) or **Java EE > Enterprise Application Project** (for full EARs).
   - In the project wizard, set the target runtime to your local WAS installation (if not listed, add it via **Window > Preferences > Server > Runtime Environments > Add > WebSphere**).
   - Configure facets for Java EE version (e.g., 7 or 8) matching your WAS.

2. **Set Up the Server**:
   - Open the **Servers** view (**Window > Show View > Servers**).
   - Right-click in the view and select **New > Server**.
   - Choose **WebSphere Application Server** (traditional or Liberty) and point to your local WAS installation directory.
   - Finish and start the server (right-click > Start).

3. **Develop Your Application**:
   - Add Java classes, JSPs, servlets, EJBs, etc., in your project.
   - Use Eclipse's editors for XML configs (e.g., web.xml, ibm-web-bnd.xml for WAS-specific bindings).
   - Build the project (**Project > Build Project**).

4. **Deploy and Run**:
   - Right-click your project > **Run As > Run on Server** (select your WAS server).
   - Eclipse publishes the app (auto-publish for dev mode) and starts the server.
   - Debug by setting breakpoints and running in Debug mode.
   - For hot deployment (fast updates without restart), enable "Publish server changes immediately" in server config.

5. **Advanced Tips**:
   - Use Liberty profile for quicker local testing—it's included in WDT and mimics traditional WAS behavior.
   - For OSGi or microservices, create OSGi Bundle Projects via the plugin.
   - Monitor logs in the **Console** view during runtime.

If you encounter issues (e.g., compatibility errors), check IBM's known issues page or ensure your Eclipse and WAS versions align.

#### References
- [IBM WebSphere Application Server Developer Tools Overview](https://www.ibm.com/docs/en/wasdtfe?topic=websphere-developer-tools-overview)
- [Eclipse Marketplace: V9.x Tools](https://marketplace.eclipse.org/content/ibm-websphere-application-server-v9x-developer-tools)
- [Eclipse Marketplace: V8.5x Tools](https://marketplace.eclipse.org/content/ibm-websphere-application-server-v85x-developer-tools)
- [Installation Guide from IBM Docs](https://www.ibm.com/docs/en/wasdtfe?topic=installing-websphere-developer-tools)
