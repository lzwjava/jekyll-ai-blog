---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing WebSphere Large EAR Upload Errors
translated: false
type: note
---

### Understanding the Issue
The "multipart file upload error" (often something like `org.apache.commons.fileupload.FileUploadException: Processing of multipart/form-data request failed. File too large (errno:27)`) typically occurs when updating an EAR file in IBM WebSphere Application Server (WAS) via the Administrative Console. This is common for larger EAR files (e.g., >20MB) due to limits on file uploads, temporary storage, heap memory, or OS resource constraints. It's not an issue with the EAR itself but with how the console handles the HTTP multipart upload.

### Quick Fixes to Try First
1. **Copy the EAR to the Server and Deploy Locally**:
   - Use FTP/SCP to transfer the new EAR file to a directory on the WAS server (e.g., `/opt/IBM/WebSphere/AppServer/installableApps/`).
   - In the Admin Console: Go to **Applications > Application Types > WebSphere enterprise applications**.
   - Select your existing application > **Update**.
   - Choose **Replace or add a single module** or **Replace the entire application**, then select **Local file system** and point to the copied EAR path.
   - This bypasses the multipart upload over HTTP.

2. **Increase OS File Size Limits (UNIX/Linux Servers)**:
   - The error `errno:27` often means the file exceeds the ulimit for the process.
   - Run `ulimit -f` as the WAS user (e.g., `webadmin`) to check the current limit.
   - Set it to unlimited: Add `ulimit -f unlimited` to the user's shell profile (e.g., `~/.bash_profile`) or the server's startup script.
   - Restart the Deployment Manager (dmgr) and retry the upload.

### Configuration Changes in WAS
1. **Increase Heap Size for Deployment Manager**:
   - Large EARs can cause OutOfMemory during processing.
   - In Admin Console: **Servers > Server Types > Administrative servers > Deployment Manager**.
   - Under **Java and Process Management > Process definition > Java Virtual Machine**:
     - Set **Initial heap size** to 1024 (or higher, e.g., 2048 for very large EARs).
     - Set **Maximum heap size** to 2048 (or higher).
   - Save, restart the dmgr, and retry.

2. **Adjust HTTP Session or Post Size Limits (If Applicable)**:
   - For web container limits: **Servers > Server Types > WebSphere application servers > [Your Server] > Web Container > HTTP transports**.
   - Increase **Maximum post size** (in bytes) if it's set low.
   - Note: This affects the admin console's web app indirectly.

### Recommended Long-Term Solution: Use wsadmin for Updates
For large or frequent updates, avoid the console entirely—it's unreliable for big files. Use the wsadmin scripting tool (Jython or JACL) to update the application.

#### Steps:
1. Copy the new EAR to a server-accessible path (e.g., `/tmp/myapp.ear`).
2. Launch wsadmin:
   ```
   /opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -user admin -password pass
   ```
3. Run this Jython script to update:
   ```python
   AdminApp.update('MyAppName', 'app', [-Map ModulesToApps, '[-MapWebModToVH [[default_host MyContext virtual_host]] ]'], [-Operation update], [-appname MyAppName], [-MapModulesToServers [[MyModule MyServer]]], [-nodefaultoptions], [-preCompileJSPs false], [-contextroot MyContext], [-noTxImport], [-connType SERVER], [ -contenturi /tmp/myapp.ear ])
   AdminConfig.save()
   ```
   - Replace `MyAppName` with your app's name, `MyContext` with the context root, `MyServer` with the target server/cluster, and `/tmp/myapp.ear` with the EAR path.
4. Sync nodes if in a clustered environment: `AdminControl.invoke(AdminControl.completeServers(), 'sync')`.
5. Restart the app: **Applications > [App] > Restart**.

This method is faster, avoids upload limits, and is scriptable for automation (e.g., via Jenkins).

### Additional Tips
- **Check Logs**: Review `SystemOut.log` and `SystemErr.log` in the dmgr profile for details (e.g., `/opt/IBM/WebSphere/AppServer/profiles/Dmgr01/logs/dmgr/`).
- **Test with Smaller EAR**: Verify if the issue is size-related by zipping a minimal version.
- **WAS Version**: Ensure you're on a supported version (e.g., 8.5, 9.0). Apply latest fixes if needed.
- If the error persists (e.g., timeout), increase the HTTP timeout in **Environment > Web Application Servers > [Server] > Container Settings > Web Container Settings > Web container > Session management > Configuration > Timeout**.

If none of these resolve it, share the exact error message and WAS version for more tailored advice.

### References
- [Error during deploy of war file on Websphere Application Server 7.0](https://coderanch.com/t/459530/application-servers/Error-deploy-war-file-Websphere)
- [OutOfMemory errors while deploying applications in WebSphere Application Server](https://www.ibm.com/support/pages/outofmemory-errors-while-deploying-applications-websphere-application-server)
- [Maximum size limit of an Ear that can be deployed in WAS](https://stackoverflow.com/questions/58748076/maximum-size-limit-of-an-ear-that-can-be-deployed-in-was)
- [Deploying the enterprise archive (EAR) using the WebSphere Administrative Console](https://www.ibm.com/docs/en/configurepricequote/9.5.0?topic=cwaso-deploying-enterprise-archive-ear-using-websphere-admin-console)
