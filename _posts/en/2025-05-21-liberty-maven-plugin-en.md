---
audio: false
generated: true
lang: en
layout: post
title: Liberty Maven Plugin
translated: false
type: note
---

To achieve your goal of running a script in IntelliJ IDEA on Windows that quickly manages your Liberty server and builds your program, while ensuring the server is stopped before replacing the EAR file, I recommend using the **Liberty Maven Plugin**. This approach is straightforward, integrates well with your Maven build process, and avoids the issues you’ve encountered with command formatting and batch files.

Here’s how to set it up:

---

### Solution: Using the Liberty Maven Plugin

#### Step 1: Add the Liberty Maven Plugin to Your `pom.xml`
The Liberty Maven Plugin allows you to control the Liberty server (start, stop, deploy, etc.) directly from Maven, which eliminates the need for complex scripts or batch files.

- Open your project’s `pom.xml` file.
- Add the following plugin configuration inside the `<build>` section:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>io.openliberty.tools</groupId>
            <artifactId>liberty-maven-plugin</artifactId>
            <version>3.3.4</version>
            <configuration>
                <serverName>default</serverName>
                <installDirectory>C:\path\to\liberty</installDirectory>
            </configuration>
        </plugin>
    </plugins>
</build>
```

- **Replace** `C:\path\to\liberty` with the actual path to your Liberty installation directory (e.g., `C:\Program Files\IBM\WebSphere\Liberty`).
- The `<serverName>default</serverName>` matches your use of `default` in the `server start default` and `server stop default` commands.

#### Step 2: Create a Maven Run Configuration in IntelliJ IDEA
Instead of using a script or batch file, you can configure IntelliJ IDEA to run a sequence of Maven goals that stop the server, build your project, and start the server again.

- In IntelliJ IDEA, go to **Run > Edit Configurations...**.
- Click the **+** button and select **Maven** from the list.
- Configure the run configuration:
  - **Name:** Give it a meaningful name, e.g., `Run Liberty`.
  - **Working directory:** Ensure it’s set to your project directory (usually auto-detected).
  - **Command line:** Enter the following sequence of Maven goals:
    ```
    liberty:stop package liberty:start
    ```
- Click **Apply** and then **OK**.

#### Step 3: Run the Configuration
- Use the **Run** button (green triangle) in IntelliJ IDEA to execute this configuration.
- This will:
  1. **Stop the Liberty server** (`liberty:stop`): Ensures the server is not running when the EAR file is replaced.
  2. **Build your project** (`package`): Runs `mvn package` to generate the EAR file.
  3. **Start the Liberty server** (`liberty:start`): Restarts the server with the updated EAR file.

---

### Why This Works for You
- **Fixes Command Format Issues:** You mentioned that using "Script text" in the run configuration splits `server start default` into separate arguments (`server`, `start`, `default`). The Maven approach avoids this entirely by using well-defined plugin goals.
- **Avoids Batch File Complexity:** You found it hard to make a `.bat` file work correctly (e.g., due to paths or environment settings). The Liberty Maven Plugin handles server management internally, so you don’t need to debug batch file commands or paths.
- **Meets Your Requirement:** You need the server stopped when replacing the EAR file to avoid startup problems. This solution explicitly stops the server before building and starts it afterward, ensuring a clean process.

---

### Alternative: Using a Batch File (If Preferred)
If you’d rather stick with a batch file, here’s a working example, though it’s less recommended due to the issues you’ve faced:

1. Create a file named `runLiberty.bat` in your project directory with the following content:

```bat
@echo off
set LIBERTY_BIN=C:\path\to\liberty\bin
set MAVEN_HOME=C:\path\to\maven
set PATH=%PATH%;%LIBERTY_BIN%;%MAVEN_HOME%\bin

"%LIBERTY_BIN%\server" stop default
mvn package
"%LIBERTY_BIN%\server" start default
```

- Replace `C:\path\to\liberty` and `C:\path\to\maven` with the actual paths to your Liberty and Maven installations.

2. In IntelliJ IDEA:
   - Go to **Run > Edit Configurations...**.
   - Click **+** and select **Batch file**.
   - Set the **Path to batch file** to the location of `runLiberty.bat`.
   - Set the **Working directory** to your project directory.
   - Click **Apply** and **OK**.

3. Run it using the **Run** button.

However, this method requires you to manually ensure paths and environment variables are correct, which you found difficult. The Maven plugin approach is simpler and more reliable.

---

### Recommendation
Use the **Liberty Maven Plugin** method outlined above. It’s:
- **Integrated:** Ties into your existing Maven build process.
- **Simple:** No need to wrestle with batch file syntax or paths.
- **Reliable:** Handles stopping and starting the server correctly, avoiding EAR replacement issues.

This setup will let you run your program quickly and consistently in IntelliJ IDEA on your Liberty server!
