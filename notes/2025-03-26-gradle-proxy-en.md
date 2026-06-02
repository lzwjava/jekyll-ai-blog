---
audio: false
generated: true
lang: en
layout: post
title: Configure Proxy for Gradle in VSCode
translated: false
type: note
---

To configure a proxy for Gradle in Visual Studio Code (VSCode) so it can download dependencies through a proxy, you need to set up the proxy settings in Gradle's configuration. Gradle uses a properties file to manage such settings, and VSCode relies on Gradle's build system for Gradle projects. Here's how you can do it:

### Steps to Configure Proxy for Gradle in VSCode

1. **Locate or Create the Gradle Properties File**
   - Gradle uses a file called `gradle.properties` to store global configuration settings.
   - This file is typically located in the Gradle user home directory:
     - On Windows: `C:\Users\<YourUsername>\.gradle\gradle.properties`
     - On macOS/Linux: `~/.gradle/gradle.properties`
   - If the file doesn’t exist, create it in the above location.

2. **Add Proxy Settings to `gradle.properties`**
   - Open the `gradle.properties` file in a text editor.
   - Add the following lines, replacing the placeholders (`<proxyHost>`, `<proxyPort>`, `<username>`, `<password>`) with your actual proxy details:
     ```
     systemProp.http.proxyHost=<proxyHost>
     systemProp.http.proxyPort=<proxyPort>
     systemProp.http.proxyUser=<username>
     systemProp.http.proxyPassword=<password>
     systemProp.https.proxyHost=<proxyHost>
     systemProp.https.proxyPort=<proxyPort>
     systemProp.https.proxyUser=<username>
     systemProp.https.proxyPassword=<password>
     ```
   - Example with real values:
     ```
     systemProp.http.proxyHost=proxy.example.com
     systemProp.http.proxyPort=8080
     systemProp.http.proxyUser=myuser
     systemProp.http.proxyPassword=mypassword
     systemProp.https.proxyHost=proxy.example.com
     systemProp.https.proxyPort=8080
     systemProp.https.proxyUser=myuser
     systemProp.https.proxyPassword=mypassword
     ```
   - If your proxy doesn’t require authentication (username/password), you can omit the `proxyUser` and `proxyPassword` lines.

3. **Optional: Configure Proxy per Project**
   - If you want the proxy settings to apply only to a specific project (instead of globally), you can add the `gradle.properties` file to your project’s root directory (e.g., `<project-root>/gradle.properties`) with the same content as above.

4. **Verify Gradle Uses the Proxy**
   - Open your Gradle project in VSCode.
   - Run a build task (e.g., `gradle build`) via the VSCode terminal or the Gradle extension.
   - Gradle should now route its downloads (like dependencies from the official site) through the specified proxy.

5. **VSCode-Specific Notes**
   - Ensure the **Java Extension Pack** and **Gradle for Java** extensions are installed in VSCode, as they enhance Gradle project support.
   - If VSCode still has issues, check that your Java runtime (used by Gradle) also respects the proxy. You might need to set JVM proxy arguments:
     - In VSCode, go to `File > Preferences > Settings`.
     - Search for `java.gradle.build.jvmArguments`.
     - Add something like:
       ```
       -Dhttp.proxyHost=<proxyHost> -Dhttp.proxyPort=<proxyPort> -Dhttps.proxyHost=<proxyHost> -Dhttps.proxyPort=<proxyPort>
       ```

6. **Test the Configuration**
   - Reload your project in VSCode (e.g., close and reopen it or use the “Refresh” button in the Gradle sidebar).
   - Run a Gradle task (e.g., `gradle build` or `gradle dependencies`) to confirm it downloads files through the proxy.

### Troubleshooting
- **Check Proxy Details**: Ensure your proxy host, port, and credentials are correct.
- **Firewall or Network**: If it still fails, your proxy or network might block specific Gradle URLs (e.g., `https://services.gradle.org`). Test with a command like `curl` or consult your network admin.
- **Verbose Output**: Run Gradle with `--debug` or `--info` (e.g., `gradle build --debug`) in the VSCode terminal to see detailed logs about network requests.

This setup should allow Gradle in VSCode to download dependencies via your proxy successfully. Let me know if you run into any issues!
