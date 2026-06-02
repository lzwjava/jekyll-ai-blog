---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Updating WebSphere Context Root
translated: false
type: note
---

### Updating the Web Context Root in IBM WebSphere Application Server (WAS)

The web context root defines the base URL path for your web application (e.g., `/myapp`). In IBM WebSphere Application Server, you can update it either during initial deployment or for an existing application via the Administrative Console. Below are the steps for an existing application. Ensure you have administrative access to the WAS console.

#### Prerequisites
- Access to the WebSphere Administrative Console (typically at `https://your-server:9043/ibm/console`).
- The application must be installed and stopped (recommended) before making changes to avoid conflicts.

#### Steps to Update Context Root
1. **Log in to the Administrative Console**:
   - Open a web browser and navigate to the WAS console URL.
   - Enter your admin credentials.

2. **Navigate to the Application**:
   - In the left navigation pane, expand **Applications** > **Application Types** > **WebSphere enterprise applications**.
   - Locate and select your deployed application from the list.

3. **Access Context Root Settings**:
   - On the application details page, scroll down to the **Web Module Properties** section.
   - Click **Context root for web modules**.

4. **Edit the Context Root**:
   - In the table that appears, find the web module (e.g., your WAR file name).
   - Update the **Context root** field with the new value (e.g., change from `/oldapp` to `/newapp`). Avoid leading slashes if not needed, but include them for paths like `/myapp`.
   - Click **OK** to save changes.

5. **Save and Synchronize Configuration**:
   - Click **Save** in the console (or **Save directly to the master configuration** if prompted).
   - If in a clustered or network deployment environment:
     - Go to **System administration** > **Nodes**.
     - Select all relevant nodes and click **Full Resynchronize**.

6. **Restart the Application**:
   - Return to **Applications** > **WebSphere enterprise applications**.
   - Select your application and click **Stop**, then **Start**.
   - Alternatively, restart the entire server via **Servers** > **Server Types** > **WebSphere application servers** > select server > **Restart**.

7. **Verify the Change**:
   - Access the application URL in a browser (e.g., `http://your-server:9080/newapp`).
   - Check server logs (e.g., `SystemOut.log`) for any errors related to the deployment.

#### Additional Notes
- **During Initial Deployment**: If deploying a new app, specify the context root in the **Select installation options** step under **Context root** for each web module.
- **EAR Files**: For applications bundled in an EAR, ensure the `application.xml` doesn't hardcode the context root; overrides in the console take precedence.
- **Common Issues**:
  - Changes may not apply if the app is running—always stop it first.
  - In WebSphere Liberty or Open Liberty, use `server.xml` configurations instead.
  - For virtual hosts or plugins, update the web server plugin configuration after changes.
- If the application uses security or shared libraries, test thoroughly post-update.

For more details, refer to the official IBM documentation or community guides.

#### References
- [Context root for web modules settings](https://www.ibm.com/docs/SSEQTP_9.0.5/com.ibm.websphere.base.doc/ae/uweb_contextroot.html)
- [IBM WebSphere - Context root of an application](https://www.freekb.net/Article?id=1647)
- [WebSphere 8.5 context root change not applying to WAR file](https://stackoverflow.com/questions/24472790/websphere-8-5-context-root-change-not-applying-to-war-file)
