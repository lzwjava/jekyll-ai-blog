---
audio: false
generated: true
lang: en
layout: post
title: Spring Boot DevTools for Auto-Restart
translated: false
type: note
---

When you run a Spring Boot application using `mvn spring-boot:run`, file watchers and auto-restart or hot-reload capabilities are not enabled by default. However, you can enable them by adding the `spring-boot-devtools` dependency to your project. This module provides features like automatic restarts and LiveReload for faster development.

### Details

1. **Default Behavior Without DevTools**:
   - Running `mvn spring-boot:run` without `spring-boot-devtools` does not include file watchers or auto-restart. You need to manually stop and restart the application to apply changes to Java classes, static resources, or templates.
   - Static resources (e.g., HTML, CSS, JS) may require a full rebuild or restart unless configured otherwise.

2. **With `spring-boot-devtools`**:
   - **File Watchers**: DevTools monitors the classpath for changes to Java files, properties, and certain resources (e.g., `/resources`, `/static`, `/templates`).
   - **Auto-Restart**: When a file on the classpath changes (e.g., a Java class or properties file), DevTools triggers an automatic restart of the application. This is faster than a cold start because it uses two classloaders: one for unchanged third-party libraries (base classloader) and another for your application code (restart classloader).[](https://docs.spring.io/spring-boot/reference/using/devtools.html)[](https://docs.spring.io/spring-boot/docs/1.5.16.RELEASE/reference/html/using-boot-devtools.html)
   - **LiveReload**: Changes to static resources (e.g., HTML, CSS, JS in `/static`, `/public`, or `/templates`) or templates (e.g., Thymeleaf) trigger a browser refresh instead of aBelow is an example of how to configure `spring-boot-devtools` for file watching, auto-restart, and hot-reloading in your Spring Boot application using a `application.yml` file. This configuration is tailored to your `blog-server` project, based on the logs you provided, which show DevTools is active and monitoring `target/classes`.

### `application.yml` Configuration

```yaml
spring:
  devtools:
    restart:
      # Enable auto-restart (default: true)
      enabled: true
      # Additional directories to monitor for restarts (e.g., custom config folder)
      additional-paths:
        - /home/lzw/Projects/blog-server/config
      # Files/directories to exclude from triggering restarts (default exclusions kept)
      exclude: static/**,public/**,templates/**,logs/**,generated/**
      # Poll interval for file changes (in milliseconds, default: 1000)
      poll-interval: 1000
      # Quiet period after file changes before restarting (in milliseconds, default: 400)
      quiet-period: 400
      # Optional: File to manually trigger restarts
      trigger-file: .restart
    livereload:
      # Enable LiveReload for browser refresh on static resource changes (default: true)
      enabled: true
```

### Explanation of Settings

- **`spring.devtools.restart.enabled`**: Enables auto-restart when classpath files change (e.g., `target/classes`, as seen in your log: `file:/home/lzw/Projects/blog-server/target/classes/`).
- **`spring.devtools.restart.additional-paths`**: Monitors extra directories (e.g., `/home/lzw/Projects/blog-server/config`) for changes to trigger restarts.
- **`spring.devtools.restart.exclude`**: Prevents restarts for changes in `static/`, `public/`, `templates/`, `logs/`, or `generated/` directories, while allowing LiveReload for static resources (e.g., HTML, CSS, JS).
- **`spring.devtools.restart.poll-interval`**: Sets how often DevTools checks for file changes (1000ms = 1 second).
- **`spring.devtools.restart.quiet-period`**: Waits 400ms after detecting a change to ensure no further changes are pending before restarting.
- **`spring.devtools.restart.trigger-file`**: Allows manual restarts by updating `.restart` (e.g., `touch /home/lzw/Projects/blog-server/.restart`).
- **`spring.devtools.livereload.enabled`**: Enables the LiveReload server, which triggers browser refreshes for changes in `static/` or `templates/` (requires a LiveReload browser extension).

### Steps to Apply

1. Create or update `src/main/resources/application.yml` with the above configuration.
2. Ensure `spring-boot-devtools` is in your `pom.xml`:

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-devtools</artifactId>
       <scope>runtime</scope>
       <optional>true</optional>
   </dependency>
   ```

3. Run `mvn spring-boot:run`. DevTools will monitor `target/classes` and `/home/lzw/Projects/blog-server/config` (if added), restarting the app on Java or properties file changes and refreshing the browser on static resource changes.
4. For LiveReload, install a browser extension (e.g., from <http://livereload.com/extensions/>) or integrate a LiveReload client in your front-end.

### Notes

- Your logs show a fast startup (0.8 seconds), so the default `poll-interval` and `quiet-period` should be fine. Adjust them (e.g., `poll-interval: 500`) if restarts feel sluggish in a larger project.
- If you don’t need LiveReload (e.g., using a separate front-end dev server), set `livereload.enabled: false`.
- For manual restarts, create `.restart` in your project root and update it when needed.

This YAML configuration should work seamlessly with your setup, enhancing the file-watching and auto-restart features you’re already seeing. full restart, provided you have a LiveReload browser extension installed (supported for Chrome, Firefox, Safari).[](https://www.concretepage.com/spring-boot/spring-boot-automatic-restart-using-developer-tools-with-maven)[](https://www.codejava.net/frameworks/spring-boot/spring-boot-auto-reload-changes-using-livereload-and-devtools)            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append(System.lineSeparator());
                }
            }

            // Capture error output
            try (BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()))) {
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append(System.lineSeparator());
                }
            }

- **Exclusions**: By default, resources in `/META-INF/maven`, `/META-INF/resources`, `/resources`, `/static`, `/public`, and `/templates` don’t trigger a restart but do trigger a LiveReload. You can customize this with `spring.devtools.restart.exclude`.[](https://docs.spring.io/spring-boot/reference/using/devtools.html)

3. **Setup for DevTools**:
   Add the following dependency to your `pom.xml`:

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-devtools</artifactId>
       <scope>runtime</scope>
       <optional>true</optional>
   </dependency>
   ```

   - The `<optional>true</optional>` ensures DevTools is not included in production builds.[](https://www.concretepage.com/spring-boot/spring-boot-automatic-restart-using-developer-tools-with-maven)
   - Run the application with `mvn spring-boot:run`. DevTools will automatically enable file watching and auto-restart.

4. **Behavior in IDEs**:
   - **Eclipse**: Saving changes (Ctrl+S) automatically triggers a build, which DevTools detects and restarts the application.[](https://docs.spring.io/spring-boot/docs/1.5.7.RELEASE/reference/html/howto-hotswapping.html)
   - **IntelliJ IDEA**: You need to manually trigger a build (Ctrl+F9 or "Make Project") for DevTools to detect changes, unless you configure auto-build. Alternatively, enable "Build project automatically" in IntelliJ settings for seamless restarts.[](https://www.codejava.net/frameworks/spring-boot/spring-boot-auto-restart-and-live-reload-in-intellij-idea)
   - For LiveReload, install the browser extension from <http://livereload.com/extensions/> and enable it.[](https://www.codejava.net/frameworks/spring-boot/spring-boot-auto-reload-changes-using-livereload-and-devtools)

5. **Alternative: Spring Loaded**:
   - Instead of DevTools, you can use Spring Loaded for more advanced hot-swapping (e.g., method signature changes). Add it to the `spring-boot-maven-plugin`:

     ```xml
     <plugin>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-maven-plugin</artifactId>
         <dependencies>
             <dependency>
                 <groupId>org.springframework</groupId>
                 <artifactId>springloaded</artifactId>
                 <version>1.2.8.RELEASE</version>
             </dependency>
         </dependencies>
     </plugin>
     ```

   - Spring Loaded is less recommended than DevTools, as it’s not as actively maintained and may not support all frameworks.[](https://docs.spring.io/spring-boot/docs/1.5.7.RELEASE/reference/html/howto-hotswapping.html)[](https://docs.spring.io/spring-boot/docs/1.5.16.RELEASE/reference/html/howto-hotswapping.html)

6. **Hot-Reloading Static Resources**:
   - Without DevTools, you can enable hot-reloading of static resources by setting `spring-boot-maven-plugin`’s `addResources` property:

     ```xml
     <plugin>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-maven-plugin</artifactId>
         <configuration>
             <addResources>true</addResources>
         </configuration>
     </plugin>
     ```

   - This adds `src/main/resources` to the classpath, allowing in-place editing of static files, but it’s less comprehensive than DevTools.[](https://docs.spring.io/spring-boot/maven-plugin/run.html)

7. **Caveats**:
   - DevTools may cause classloading issues in multi-module projects. If this happens, try disabling restart with `spring.devtools.restart.enabled=false` or use JRebel for advanced reloading.[](https://docs.spring.io/spring-boot/reference/using/devtools.html)
   - For non-classpath files, use `spring.devtools.restart.additional-paths` to monitor additional directories.[](https://docs.spring.io/spring-boot/docs/1.5.16.RELEASE/reference/html/using-boot-devtools.html)
   - LiveReload requires a browser extension and may not work for all front-end setups (e.g., React with Webpack).[](https://stackoverflow.com/questions/49888724/hot-reload-for-spring-boot-backend-frontend)
   - If restarts are slow, adjust `spring.devtools.restart.poll-interval` and `spring.devtools.restart.quiet-period` to optimize file watching.[](https://docs.spring.io/spring-boot/reference/using/devtools.html)

### Steps for a Simple App

1. Create a basic Spring Boot app (e.g., using Spring Initializr with `spring-boot-starter-web`).
2. Add the `spring-boot-devtools` dependency to `pom.xml`.
3. Run `mvn spring-boot:run`.
4. Modify a Java file, properties file, or static resource (e.g., HTML in `src/main/resources/static`).
5. Observe the auto-restart (for Java/properties) or browser refresh (for static resources with LiveReload enabled).

### Example

For a simple app with a REST controller:

```java
@RestController
public class HelloController {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}
```

- Add DevTools, run `mvn spring-boot:run`, and change the `hello()` method’s return value. The app will restart automatically.
- Add an `index.html` in `src/main/resources/static`, install the LiveReload extension, and modify the HTML. The browser will refresh without a restart.

### Conclusion

For a simple Spring Boot app, adding `spring-boot-devtools` is the easiest way to enable file watchers, auto-restart, and hot-reloading. Use `mvn spring-boot:run` with DevTools for a seamless development experience. If you need more advanced hot-swapping, consider Spring Loaded or JRebel, but DevTools is sufficient for most cases.[](https://www.geeksforgeeks.org/hot-reload-with-spring-boot-devtools/)[](https://docs.spring.io/spring-boot/how-to/hotswapping.html)

---

Below is an example of how to configure `spring-boot-devtools` for file watching, auto-restart, and hot-reloading in your Spring Boot application using a `application.yml` file. This configuration is tailored to your `blog-server` project, based on the logs you provided, which show DevTools is active and monitoring `target/classes`.

### `application.yml` Configuration

```yaml
spring:
  devtools:
    restart:
      # Enable auto-restart (default: true)
      enabled: true
      # Additional directories to monitor for restarts (e.g., custom config folder)
      additional-paths:
        - /home/lzw/Projects/blog-server/config
      # Files/directories to exclude from triggering restarts (default exclusions kept)
      exclude: static/**,public/**,templates/**,logs/**,generated/**
      # Poll interval for file changes (in milliseconds, default: 1000)
      poll-interval: 1000
      # Quiet period after file changes before restarting (in milliseconds, default: 400)
      quiet-period: 400
      # Optional: File to manually trigger restarts
      trigger-file: .restart
    livereload:
      # Enable LiveReload for browser refresh on static resource changes (default: true)
      enabled: true
```

### Explanation of Settings

- **`spring.devtools.restart.enabled`**: Enables auto-restart when classpath files change (e.g., `target/classes`, as seen in your log: `file:/home/lzw/Projects/blog-server/target/classes/`).
- **`spring.devtools.restart.additional-paths`**: Monitors extra directories (e.g., `/home/lzw/Projects/blog-server/config`) for changes to trigger restarts.
- **`spring.devtools.restart.exclude`**: Prevents restarts for changes in `static/`, `public/`, `templates/`, `logs/`, or `generated/` directories, while allowing LiveReload for static resources (e.g., HTML, CSS, JS).
- **`spring.devtools.restart.poll-interval`**: Sets how often DevTools checks for file changes (1000ms = 1 second).
- **`spring.devtools.restart.quiet-period`**: Waits 400ms after detecting a change to ensure no further changes are pending before restarting.
- **`spring.devtools.restart.trigger-file`**: Allows manual restarts by updating `.restart` (e.g., `touch /home/lzw/Projects/blog-server/.restart`).
- **`spring.devtools.livereload.enabled`**: Enables the LiveReload server, which triggers browser refreshes for changes in `static/` or `templates/` (requires a LiveReload browser extension).

### Steps to Apply

1. Create or update `src/main/resources/application.yml` with the above configuration.
2. Ensure `spring-boot-devtools` is in your `pom.xml`:

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-devtools</artifactId>
       <scope>runtime</scope>
       <optional>true</optional>
   </dependency>
   ```

3. Run `mvn spring-boot:run`. DevTools will monitor `target/classes` and `/home/lzw/Projects/blog-server/config` (if added), restarting the app on Java or properties file changes and refreshing the browser on static resource changes.
4. For LiveReload, install a browser extension (e.g., from <http://livereload.com/extensions/>) or integrate a LiveReload client in your front-end.

### Notes

- Your logs show a fast startup (0.8 seconds), so the default `poll-interval` and `quiet-period` should be fine. Adjust them (e.g., `poll-interval: 500`) if restarts feel sluggish in a larger project.
- If you don’t need LiveReload (e.g., using a separate front-end dev server), set `livereload.enabled: false`.
- For manual restarts, create `.restart` in your project root and update it when needed.

This YAML configuration should work seamlessly with your setup, enhancing the file-watching and auto-restart features you’re already seeing.
