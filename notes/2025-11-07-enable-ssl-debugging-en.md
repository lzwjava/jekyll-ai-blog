---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Enable Java SSL TLS Debugging
translated: false
type: note
---

### Enabling SSL/TLS Debugging in Java

To enable detailed logging for SSL/TLS-related activities in Java (e.g., handshakes, certificate validation, key exchanges), you use the JVM system property `-Djavax.net.debug`. This outputs debug information to the console (stdout/stderr) when your Java application runs.

#### Step-by-Step Instructions

1. **Choose the Debug Level**:
   - Use `ssl` for basic SSL/TLS handshake details.
   - Use `ssl:handshake` for verbose handshake messages (including cipher suites and certificates).
   - Use `all` for comprehensive debugging (includes SSL plus other network protocols—use sparingly as it's very verbose).
   - Common recommendation: Start with `ssl:handshake:verbose,keymanager:trustmanager` for targeted SSL insights.

2. **Set the Property When Running Your Java Application**:
   - **Command-Line Execution** (e.g., via `java` command):

     ```
     java -Djavax.net.debug=ssl:handshake -jar your-app.jar
     ```

     Replace `your-app.jar` with your actual application or class (e.g., `com.example.Main`).

   - **In an IDE (e.g., IntelliJ IDEA, Eclipse)**:
     - Go to Run/Debug Configurations.
     - Add `-Djavax.net.debug=ssl:handshake` to the **VM options** field.
     - Run or debug the configuration.

   - **In a Build Tool (e.g., Maven or Gradle)**:
     - **Maven** (in `pom.xml` under `<build><plugins><plugin>` for surefire):

       ```xml
       <configuration>
         <argLine>-Djavax.net.debug=ssl:handshake</argLine>
       </configuration>
       ```

     - **Gradle** (in `build.gradle`):

       ```groovy
       test {
         jvmArgs '-Djavax.net.debug=ssl:handshake'
       }
       ```

3. **Capture the Logs**:
   - The output appears in your console/terminal.
   - Redirect to a file for easier review:

     ```
     java -Djavax.net.debug=ssl:handshake -jar your-app.jar > ssl-debug.log 2>&1
     ```

   - Look for lines starting with `***` (e.g., `*** ClientHello` for handshake starts) or `javax.net.ssl` prefixes.

4. **Disable It**:
   - Simply remove the `-D` flag when done—it's not set by default to avoid performance overhead.

#### Example Output Snippet

When enabled, you'll see something like:

```
*** ServerHello, TLSv1.2
RandomCookie:  GMT: 1731000000 bytes = { ... }
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
Compression Method: 0
***
```

#### Tips

- This works for Java 8+ (including 11, 17, 21). In newer versions, you might also enable `-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3` for protocol-specific logs.
- High verbosity can slow down your app and flood logs—test in a dev environment.
- If using a framework like Spring Boot, add it to `application.properties`: `debug=true` (for general) or via command-line args.

For more details, see the official Oracle docs: [Java Secure Socket Extension (JSSE) Reference Guide](https://docs.oracle.com/en/java/javase/17/docs/specs/security/standard-names.html#jsse-cipher-suite-names).
