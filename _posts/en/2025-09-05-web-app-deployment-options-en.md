---
audio: false
generated: true
image: false
lang: en
layout: post
title: Web Application Deployment Options Explained
translated: false
type: note
---

Got it — let me explain those options clearly for you.

### Option 1: Quick Development Setup (Recommended)

This is the easiest way to start the project during development.
If your `pom.xml` includes a Tomcat or Jetty plugin, you can run the app directly with:

```bash
mvn tomcat7:run
```

or

```bash
mvn jetty:run
```

This launches the web app in an embedded Tomcat/Jetty without building a WAR or deploying manually. If you don’t already have the plugin, you’d need to add it to `pom.xml` first.

---

### Option 2: Build and Deploy WAR

This is the more “traditional” approach. You package the application into a WAR file:

```bash
mvn clean package
```

This produces something like `target/playground-server-1.0.war`.
You then copy that WAR into a standalone Tomcat/Jetty server’s `webapps/` folder, restart the server, and access the deployed app in the browser.

---

### Option 3: Use Embedded Server (Manual Setup)

Currently your `Application.main()` just starts the Spring context — it doesn’t actually start a web server.
If you want the app itself to launch Tomcat (without relying on an external one), you’d need to modify your main class to set up and start an embedded Tomcat instance programmatically.

This gives you a self-contained runnable JAR, but it requires extra setup code.

---

### Option 4: Spring Boot Migration

This project has **some Spring Boot test setup**, but isn’t a real Spring Boot app yet. That’s why running:

```bash
mvn spring-boot:run
```

doesn’t work.

If you want, you can migrate:

* Add the proper Spring Boot starter dependencies.
* Change your main class to `@SpringBootApplication`.
* Then you’d be able to just run with `mvn spring-boot:run` or even `java -jar target/app.jar`.

This is the most modern approach, but requires some changes to your code and `pom.xml`.

---

✅ **In short**:

* If you just want to test quickly → use **Option 1**.
* If you’re deploying to an existing server → use **Option 2**.
* If you want a self-contained app without external Tomcat → use **Option 3**.
* If you want to modernize and simplify long-term → use **Option 4**.

---

Do you want me to show you the **exact `pom.xml` snippet** for Option 1 (Tomcat/Jetty plugin) so you can just run `mvn tomcat7:run` right away?
