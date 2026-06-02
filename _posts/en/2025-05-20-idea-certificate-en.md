---
audio: false
generated: true
lang: en
layout: post
title: Handling Non-Trusted Certificates in IntelliJ IDEA
translated: false
type: note
---

The "Untrusted Server's Certificate" dialog in IntelliJ IDEA often appears when the IDE encounters SSL certificates that aren't trusted by its keystore, such as self-signed or custom corporate certificates. Since you've already imported your corporation's keystore into `/lib/cacerts` but still see the prompt, the issue might stem from IntelliJ not using that keystore or additional certificates causing the dialog. Here's how to address it and potentially stop the prompts:

### Option 1: Configure IntelliJ to Accept Non-Trusted Certificates Automatically
Enabling this option tells IntelliJ to bypass the dialog for untrusted certificates, but be cautious as it reduces security by accepting all certificates, potentially exposing you to man-in-the-middle attacks.

- **Windows/Linux**:
  1. Go to `File > Settings > Tools > Server Certificates`.
  2. Check the box for **"Accept non-trusted certificates automatically"**.
  3. Click **Apply** and **OK**.
- **macOS**:
  1. Go to `IntelliJ IDEA > Preferences > Tools > Server Certificates`.
  2. Check **"Accept non-trusted certificates automatically"**.
  3. Click **Apply** and **OK**.[](https://stackoverflow.com/questions/60092405/untrusted-server-certificate-in-intellij)[](https://www.javahelps.com/2020/12/things-to-do-after-installing-intellij.html)

**Note**: This is not recommended unless you're in a trusted, isolated network (e.g., air-gapped corporate environment), as it can make your IDE vulnerable to unverified connections.[](https://stackoverflow.com/questions/60092405/untrusted-server-certificate-in-intellij)

### Option 2: Verify and Correct the Keystore Configuration
Since you've imported the corporate keystore into `/lib/cacerts`, ensure IntelliJ is using it correctly. The issue might be that IntelliJ is still referencing its own truststore or the wrong cacerts file.

1. **Check the Keystore Path**:
   - IntelliJ often uses its own truststore at `~/.IntelliJIdea<version>/system/tasks/cacerts` or the JetBrains Runtime (JBR) truststore at `<IntelliJ Installation>/jbr/lib/security/cacerts`.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004301319-Adding-root-CA-to-intellij-on-Windows-10)
   - If you modified `/lib/cacerts` in the IntelliJ directory, confirm it’s the correct path for your IDE version. For JetBrains Toolbox installations, the path might differ (e.g., `~/AppData/Local/JetBrains/Toolbox/apps/IDEA-U/ch-0/<version>/jbr/lib/security/cacerts` on Windows).[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004301319-Adding-root-CA-to-intellij-on-Windows-10)
   - Use the `keytool` command to verify the certificate is in the cacerts file:
     ```bash
     keytool -list -keystore <path-to-cacerts> -storepass changeit
     ```
     Ensure your corporate CA certificate is listed.

2. **Point IntelliJ to the Custom Keystore**:
   - If the certificate is correctly imported but IntelliJ still prompts, it might not be using the modified cacerts. Add a custom VM option to specify the truststore:
     1. Go to `Help > Edit Custom VM Options`.
     2. Add:
        ```
        -Djavax.net.ssl.trustStore=<path-to-cacerts>
        -Djavax.net.ssl.trustStorePassword=changeit
        ```
        Replace `<path-to-cacerts>` with the full path to your modified `cacerts` file.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000080810-Setting-Truststore-)
     3. Restart IntelliJ IDEA.

3. **Re-import the Certificate**:
   - If the certificate import was incomplete or incorrect, re-import it:
     ```bash
     keytool -import -trustcacerts -file <certificate-file>.cer -alias <alias> -keystore <path-to-cacerts> -storepass changeit
     ```
     Replace `<certificate-file>.cer` with your corporate CA certificate and `<path-to-cacerts>` with the correct cacerts file path.[](https://www.baeldung.com/jvm-certificate-store-errors)

### Option 3: Add Certificates via IntelliJ’s Server Certificates Settings
Instead of modifying the cacerts file manually, you can add certificates through IntelliJ’s UI, which stores them in its internal truststore:

1. Go to `File > Settings > Tools > Server Certificates` (or `IntelliJ IDEA > Preferences` on macOS).
2. Click the **"+"** button to add a new certificate.
3. Browse to your corporate CA certificate file (in `.cer` or `.pem` format) and import it.
4. Restart IntelliJ to ensure the certificate is recognized.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004301319-Adding-root-CA-to-intellij-on-Windows-10)

### Option 4: Check for Proxy or Antivirus Interference
Corporate environments often use proxies or antivirus software (e.g., Zscaler, Forcepoint) that perform man-in-the-middle SSL inspection, generating new certificates dynamically. This can cause repeated prompts if the certificates change frequently (e.g., daily, as with McAfee Endpoint Security).[](https://stackoverflow.com/questions/60092405/untrusted-server-certificate-in-intellij)[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004301319-Adding-root-CA-to-intellij-on-Windows-10)

- **Import Proxy/Antivirus CA Certificate**:
  - Obtain the root CA certificate from your proxy or antivirus software (ask your IT team).
  - Import it into IntelliJ’s truststore via `Settings > Tools > Server Certificates` or into the cacerts file using the `keytool` command above.
- **Disable SSL Inspection (if possible)**:
  - If your proxy allows, configure it to bypass SSL inspection for IntelliJ-related domains (e.g., `plugins.jetbrains.com`, `repo.maven.apache.org`).

### Option 5: Debug and Identify Problematic Certificates
If the issue persists, identify which server or certificate is causing the prompt:

1. Enable verbose SSL logging:
   - Go to `Help > Edit Custom VM Options` and add:
     ```
     -Djavax.net.debug=ssl:handshake:verbose
     ```
   - Restart IntelliJ and check the `idea.log` file (located in `~/.IntelliJIdea<version>/system/log/`) for SSL errors, such as `PKIX path building failed`. This will show the problematic server or certificate.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360010576419-Adding-trusted-certs)

2. Check for specific plugins or integrations:
   - Plugins like Maven, Gradle, or version control systems (e.g., Git, SVN) may connect to servers with different certificates. Disable plugins temporarily to isolate the issue.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000131364-Server-s-Certificate-is-not-trusted-pop-up)
   - For Maven, ensure the JDK configured in `File > Settings > Build, Execution, Deployment > Build Tools > Maven > Runner` uses the updated cacerts.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360010576419-Adding-trusted-certs)

### Additional Notes
- **Security Warning**: Accepting non-trusted certificates automatically is convenient but risky in non-isolated networks. Only use this in trusted environments.[](https://stackoverflow.com/questions/60092405/untrusted-server-certificate-in-intellij)[](https://stackoverflow.com/questions/26192713/android-studio-servers-certificate-is-not-trusted)
- **System Time Sync**: Ensure your system clock is synchronized, as a mismatch can cause certificate validation issues.[](https://stackoverflow.com/questions/60092405/untrusted-server-certificate-in-intellij)
- **JetBrains Runtime (JBR)**: IntelliJ runs on its own JBR, which may not use the system’s Java truststore. Changes to the system’s `$JAVA_HOME/lib/security/cacerts` won’t affect IntelliJ unless explicitly configured.[](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360010576419-Adding-trusted-certs)
- **Persistent Prompts**: If prompts persist after importing the certificate, it could be due to a plugin or service (e.g., JFrog, SonarQube) using a different truststore. Check plugin settings or contact your IT team for the full certificate chain.[](https://community.sonarsource.com/t/sonarlint-does-not-respect-the-certificates-added-in-the-intellijs-keystore/22897)[](https://github.com/jfrog/jfrog-idea-plugin/issues/34)

### Recommended Approach
1. Try **Option 3** (add certificates via IntelliJ’s UI) first, as it’s the safest and most straightforward.
2. If that fails, verify the keystore path and configuration with **Option 2**.
3. Use **Option 1** (auto-accept) only as a last resort in a trusted environment.
4. If the issue involves a proxy or antivirus, work with your IT team to obtain and import the correct CA certificates.

If you still face issues, share details about the certificate (e.g., issuer, domain) or any error messages from the `idea.log` file, and I can help narrow it down further.
