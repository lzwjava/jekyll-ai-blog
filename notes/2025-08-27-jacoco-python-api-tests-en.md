---
audio: false
generated: true
image: false
lang: en
layout: post
title: JaCoCo for Python API Tests Guide
translated: false
type: note
---

Good question — this is a classic integration problem between **Java code coverage tools** (JaCoCo) and **non-Java test harnesses** (like Python `unittest` hitting your REST endpoints).

---

### Why JaCoCo works with JUnit but not directly with Python tests

* JaCoCo works by attaching a **Java agent** (`-javaagent:jacocoagent.jar`) to the JVM.
* When your tests run **inside the same JVM** (JUnit, TestNG, etc.), JaCoCo can see which classes and methods are loaded/executed and generate detailed coverage reports.
* If you use Python `unittest` + `requests` to hit your API endpoints, you’re exercising the **running server** from outside the JVM.
  That means JaCoCo doesn’t automatically see coverage, unless the server process itself has the agent attached.

---

### How you can get accurate coverage with JaCoCo and Python tests

You don’t need to switch to JUnit. You can still use JaCoCo, but you must **attach the agent to the JVM where your big Java project (the server) runs**, not to the test runner.

1. **Run your Java application with the JaCoCo agent**
   Add the agent to your Java server startup:

   ```bash
   java -javaagent:/path/to/jacocoagent.jar=destfile=jacoco-it.exec,output=file,append=false \
        -jar myserver.jar
   ```

   This will collect execution data (`jacoco-it.exec`) while your Python tests hit the endpoints.

2. **Run your Python tests normally**

   ```bash
   python -m unittest discover tests/
   ```

   Since the server is already running with the agent, all classes and methods hit by HTTP requests will be recorded.

3. **Shut down the server**
   The `.exec` file will be flushed.

4. **Generate a coverage report**
   Use the Maven plugin or CLI to convert the `.exec` file into HTML/XML reports:

   ```bash
   mvn jacoco:report -Djacoco.dataFile=jacoco-it.exec
   ```

   or with CLI:

   ```bash
   java -jar jacococli.jar report jacoco-it.exec \
        --classfiles target/classes \
        --sourcefiles src/main/java \
        --html report
   ```

---

### Two modes of testing with JaCoCo

* **Unit tests (in-JVM with JUnit):** works out-of-the-box with the Maven plugin (`prepare-agent` + `report`).
* **Integration tests (external clients like Python):** requires starting the JVM with the agent, then merging the `.exec` data back into reports.

---

### About your log4j idea

Counting log statements per file is extremely coarse:

* Not every method logs.
* Logs don’t cover conditionals or branches.
* Coverage is not reliable.

JaCoCo, in contrast, measures **class, method, line, and branch coverage** — much finer granularity.

---

✅ **Answer:** Yes, you can absolutely use the JaCoCo approach even if your tests are in Python. The trick is to **attach JaCoCo to the Java process under test** (your server), not the test runner. Then generate the report afterward. This way you’ll get the same method-level and branch-level coverage as with JUnit.

---

Do you want me to draft a **Maven config example** that sets up a special profile for “integration tests” with JaCoCo, so you can run your server, hit it with Python tests, and then generate coverage in one command?
