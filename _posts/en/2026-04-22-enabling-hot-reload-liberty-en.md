---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling Hot Reload in Liberty
translated: false
type: note
---

**Question:**
How can I enable hot loading (live reload) of Java code and EAR changes in IBM WebSphere Liberty Profile when source files are modified?

---

**Answer:**

Hot reloading in IBM WebSphere Liberty (Liberty profile) is quite good compared to traditional app servers, but it depends on *how* you structure your deployment and development workflow. There are two levels to understand:

---

# 1. Basic Hot Reload (Class / Resource Changes)

Liberty supports automatic detection of changes in:

* `.class` files
* `.jsp`, `.html`, `.xml`
* some configuration files

### ✅ Enable it

In your `server.xml`, ensure:

```xml
<applicationMonitor updateTrigger="mbean" dropinsEnabled="true"/>
```

Or more commonly:

```xml
<applicationMonitor updateTrigger="polled" pollingRate="500ms"/>
```

### What happens?

* Liberty scans for file changes
* When `.class` changes → it reloads the classloader
* No full server restart needed

### ⚠️ Limitation

* Works best for **exploded applications**
* Does NOT always work well with packaged `.ear` or `.war` files

---

# 2. Best Practice: Use *Exploded EAR/WAR* (Critical)

Instead of deploying:

```
app.ear
```

Use:

```
app.ear/
  META-INF/
  lib/
  myapp.war/
    WEB-INF/classes/
```

### Why?

Liberty watches file system changes. If it's a packaged EAR:

* You must rebuild EAR → slow
* Liberty may redeploy entire app

With exploded EAR:

* Change `.class` → instant reload
* Change JSP → instant
* No packaging step

---

# 3. Development Mode (Recommended)

Liberty has a powerful dev mode:

### Use Maven

```bash
mvn liberty:dev
```

### Or Gradle

```bash
gradle libertyDev
```

### What it gives you

* Auto compile Java source
* Auto deploy changes
* Live reload browser
* Incremental updates

👉 This is the **closest to Spring Boot DevTools experience**

---

# 4. EAR Change / Full Application Reload

If you modify:

* `application.xml`
* dependencies in `lib/`
* structure of EAR

Then Liberty will:

* trigger full app restart (not full server restart)

### You can force reload via

```bash
touch server.xml
```

or using JMX (`updateTrigger="mbean"`)

---

# 5. IDE Integration (Very Important)

If you're using:

### IntelliJ IDEA

* Use **exploded artifact**
* Enable:

  * "Build project automatically"
  * Registry: `compiler.automake.allow.when.app.running=true`

### Eclipse

* Use **WebSphere Liberty Tools**
* Enable:

  * "Automatically publish when resources change"

---

# 6. Advanced: Classloader Behavior

Liberty uses **dynamic classloading**, but:

* Static fields are NOT reset
* Some frameworks cache aggressively

So sometimes you must:

```bash
mvn liberty:stop
mvn liberty:start
```

---

# 7. Common Pitfalls (Very Important)

### ❌ Packaging EAR every time

→ kills hot reload

### ❌ Using shared libraries incorrectly

→ changes not detected

### ❌ Framework interference

Examples:

* Hibernate caching
* Spring singleton beans

---

# 8. Practical Workflow (Recommended Setup)

For best developer experience:

1. Use exploded EAR/WAR
2. Run:

   ```bash
   mvn liberty:dev
   ```

3. Edit Java code
4. Let Maven auto-compile
5. Liberty reloads instantly

---

# 9. Summary

| Scenario             | Works? | Notes       |
| -------------------- | ------ | ----------- |
| Change `.class`      | ✅      | Fast reload |
| Change JSP/HTML      | ✅      | Instant     |
| Change EAR structure | ⚠️     | App restart |
| Packaged EAR         | ❌      | Avoid       |
| Exploded EAR         | ✅      | Best        |

---

If you want, I can show:

* a **full Maven project setup** for Liberty hot reload
* or compare this with **Tomcat / Spring Boot DevTools / JRebel** (big differences)
