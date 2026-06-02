---
audio: false
generated: true
lang: en
layout: post
title: Configuring launch.json for Spring Boot in VSCode
translated: false
type: note
---

To configure the `launch.json` file for a Maven Spring Boot project in Visual Studio Code (VSCode), you need to set up a launch configuration that allows VSCode to run and debug your application using its Java extensions. Below is a step-by-step guide to help you achieve this.

### Prerequisites

Before proceeding, ensure the following:

- You have the **Java Extension Pack** installed in VSCode. This pack includes essential extensions like "Debugger for Java" and "Language Support for Java" by Red Hat, which provide support for running and debugging Java applications, including Spring Boot projects.
- Your Spring Boot project is a Maven project with a valid `pom.xml` file.
- The project has a main class annotated with `@SpringBootApplication`, which contains the `main` method to start the application.

### Steps to Configure `launch.json`

1. **Locate the Main Class**
   - In a typical Spring Boot project, the main class is located in the `src/main/java` directory and is annotated with `@SpringBootApplication`. For example, it might be named `com.example.demo.DemoApplication`.
   - Open your project in VSCode and identify the fully qualified name of this class (e.g., `com.example.demo.DemoApplication`).

2. **Determine the Project Name**
   - The project name in a Maven project corresponds to the `artifactId` defined in your `pom.xml` file.
   - Open your `pom.xml` file and look for the `<artifactId>` tag. For example:

     ```xml
     <artifactId>demo</artifactId>
     ```

     Here, the project name would be `demo`.

3. **Open the Debug View**
   - In VSCode, click on the **Debug** icon in the left sidebar (or press `Ctrl+Shift+D` / `Cmd+Shift+D` on Mac).
   - Click on the gear icon ⚙️ next to the "Run and Debug" dropdown to configure launch settings. If no `launch.json` exists, VSCode will prompt you to create one.

4. **Create or Edit `launch.json`**
   - If prompted to select an environment, choose **Java**. This will generate a basic `launch.json` file in the `.vscode` folder of your project.
   - Open the `launch.json` file. If it already exists, you can edit it directly.

5. **Add a Launch Configuration**
   - Add the following configuration inside the `"configurations"` array in `launch.json`. Replace the placeholders with your project's details:

     ```json
     {
         "type": "java",
         "name": "Launch Spring Boot App",
         "request": "launch",
         "mainClass": "com.example.demo.DemoApplication",
         "projectName": "demo"
     }
     ```

     - **Explanation of Fields:**
       - `"type": "java"`: Specifies that this is a Java launch configuration.
       - `"name": "Launch Spring Boot App"`: A descriptive name for this configuration, which will appear in the debug dropdown.
       - `"request": "launch"`: Indicates that VSCode should launch the application (as opposed to attaching to an existing process).
       - `"mainClass"`: The fully qualified name of your Spring Boot main class (e.g., `com.example.demo.DemoApplication`).
       - `"projectName"`: The `artifactId` from your `pom.xml` (e.g., `demo`), which helps VSCode locate the project in a multi-module setup.

   - Here’s an example of a complete `launch.json` file with this configuration:

     ```json
     {
         "version": "0.2.0",
         "configurations": [
             {
                 "type": "java",
                 "name": "Launch Spring Boot App",
                 "request": "launch",
                 "mainClass": "com.example.demo.DemoApplication",
                 "projectName": "demo"
             }
         ]
     }
     ```

6. **Optional: Add VM Arguments or Program Arguments**
   - If your application requires additional settings (e.g., activating a Spring profile), you can add them using `"vmArgs"` or `"args"`:
     - Example with a Spring profile:

       ```json
       {
           "type": "java",
           "name": "Launch Spring Boot App with Profile",
           "request": "launch",
           "mainClass": "com.example.demo.DemoApplication",
           "projectName": "demo",
           "vmArgs": "-Dspring.profiles.active=dev"
       }
       ```

       This sets the `spring.profiles.active` property to `dev`.
     - Example with program arguments:

       ```json
       "args": ["arg1", "arg2"]
       ```

7. **Save and Run**
   - Save the `launch.json` file.
   - Go back to the Debug view, select **"Launch Spring Boot App"** from the dropdown, and click the green play button (or press `F5`).
   - VSCode will build and run your Spring Boot application using Maven and the Java extension. You should see the Spring Boot startup logs in the Debug Console.

### Verifying the Configuration

- If your Spring Boot application is a web application, open a browser and navigate to `http://localhost:8080` (or the port specified in your `application.properties` or `application.yml` file) to confirm it’s running.
- You can also set breakpoints in your code and use the debug controls (pause, step over, etc.) to debug your application.

### Notes

- The Java extensions in VSCode automatically handle the classpath and build process based on your `pom.xml`, so you typically don’t need to manually run `mvn clean install` beforehand.
- If your project is part of a multi-module Maven setup, ensure the `projectName` matches the correct module’s `artifactId`.
- For advanced configurations (e.g., custom working directories or pre-launch tasks), refer to the [VSCode Java Debugging documentation](https://code.visualstudio.com/docs/java/java-debugging).

With this setup, your `launch.json` should be correctly configured to run and debug your Maven Spring Boot project in VSCode!
