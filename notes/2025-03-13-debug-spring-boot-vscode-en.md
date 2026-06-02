---
audio: false
generated: true
lang: en
layout: post
title: Debugging Spring Boot Applications in Visual Studio Code
translated: false
type: note
---

To debug a Maven Spring Boot project in Visual Studio Code (VSCode), you can follow these straightforward steps to set up and run your application in debug mode. This guide assumes you have a basic Maven Spring Boot project with a `pom.xml` file and a main class annotated with `@SpringBootApplication`. Here’s how to do it:

### Step 1: Install Necessary Extensions
Before you begin, ensure that VSCode is equipped with the required extensions for Java and Spring Boot development:
- **Java Extension Pack**: This includes essential tools like Language Support for Java by Red Hat, which provides debugging capabilities, along with other utilities for Java development.
- **Spring Boot Extension Pack**: This pack enhances Spring Boot development with features like the Spring Boot Dashboard, Spring Boot Tools, and more.

To install these:
1. Open VSCode.
2. Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
3. Search for "Java Extension Pack" and "Spring Boot Extension Pack," then click **Install** for each.

### Step 2: Open Your Maven Spring Boot Project
- Launch VSCode and open your project folder by selecting **File > Open Folder** and choosing the directory containing your `pom.xml` file.
- VSCode will detect the `pom.xml`, and the Java Extension Pack will automatically index the project and resolve dependencies. This may take a moment, so wait until the process completes (you’ll see progress in the bottom-right status bar).

### Step 3: Create or Edit the `launch.json` File
To configure debugging, you need to set up a `launch.json` file in VSCode:
1. Open the **Run and Debug** view by clicking the bug-and-play icon in the sidebar or pressing `Ctrl+Shift+D`.
2. If no debug configuration exists, click **"create a launch.json file"**. If one already exists, click the gear icon to edit it.
3. When prompted, select **Java** as the environment. VSCode will generate a default `launch.json` file in a `.vscode` folder within your project.
4. Add or modify a debug configuration for your Spring Boot application. Here’s an example configuration:

    ```json
    {
        "type": "java",
        "name": "Debug Spring Boot",
        "request": "launch",
        "mainClass": "com.example.demo.DemoApplication",
        "projectName": "demo"
    }
    ```

    - Replace `"com.example.demo.DemoApplication"` with the fully qualified name of your main class (e.g., `com.yourcompany.yourapp.YourApplication`).
    - Replace `"demo"` with your project’s name, typically the `<artifactId>` from your `pom.xml`.

5. Save the `launch.json` file.

#### Optional: Add Arguments
If your application requires specific arguments (e.g., Spring profiles), you can include them:
```json
{
    "type": "java",
    "name": "Debug Spring Boot",
    "request": "launch",
    "mainClass": "com.example.demo.DemoApplication",
    "projectName": "demo",
    "args": "--spring.profiles.active=dev"
}
```

### Step 4: Start Debugging
- In the **Run and Debug** view, select **"Debug Spring Boot"** from the dropdown menu at the top.
- Click the green play button (or press `F5`) to launch the application in debug mode.
- VSCode will compile the project using Maven, start the Spring Boot application, and attach the debugger automatically.

### Step 5: Set Breakpoints and Debug
- Open a Java file in your project (e.g., a controller or service class).
- Set breakpoints by clicking in the gutter to the left of the line numbers, where a red dot will appear.
- Interact with your application (e.g., via a browser or API client). When execution hits a breakpoint, VSCode will pause, allowing you to:
  - Inspect variables in the **Variables** panel.
  - Step through code using controls like **Step Over** (`F10`), **Step Into** (`F11`), or **Continue** (`F5`).
  - View the call stack and more in the debug sidebar.

### Alternative Methods
While the `launch.json` method is recommended for its flexibility, you can also debug using:
- **Maven View**:
  1. Open the Maven view in the sidebar (look for the "M" icon or enable it via Extensions).
  2. Expand your project, navigate to `spring-boot` under Plugins, right-click `spring-boot:run`, and select **Debug**.
  3. The application will start, and the debugger will attach.
- **Spring Boot Dashboard**:
  1. Open the Spring Boot Dashboard (usually in the Explorer view or via the command palette: `Spring Boot Dashboard`).
  2. Locate your application, right-click it, and select **Debug** (if available).

### Prerequisites and Notes
- Ensure **Maven** is installed on your system and accessible via the command line, or rely on VSCode’s embedded Maven (configured via settings if needed).
- Verify your project builds successfully (`mvn clean install`) to avoid runtime errors during debugging.
- Use a compatible Java version as specified in your `pom.xml` (e.g., via `<java.version>`).

By following these steps, you can effectively debug your Maven Spring Boot project in VSCode, leveraging its powerful debugging tools to identify and resolve issues in your code.
