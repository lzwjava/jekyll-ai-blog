---
audio: false
generated: true
lang: en
layout: post
title: OpenJDK 21 Tools Overview
translated: false
type: note
---

The directory `/usr/lib/jvm/java-21-openjdk-amd64/bin/` contains tools provided by the OpenJDK 21 Java Development Kit (JDK). These tools are used for various tasks related to Java development, debugging, monitoring, and packaging. Below is a concise explanation of each tool and its common usage. For detailed usage, you can run `tool_name --help` or `man tool_name` in the terminal for most of these tools.

---

### 1. **jar** - Create and manage Java ARchive (JAR) files
- **Purpose**: Package Java classes and resources into a JAR file or extract contents from a JAR.
- **Common Usage**:
  ```bash
  jar cf myapp.jar *.class  # Create a JAR file
  jar xf myapp.jar          # Extract contents of a JAR
  jar tf myapp.jar          # List contents of a JAR
  ```
- **Example**: `jar cvfm myapp.jar manifest.txt *.class` (creates a JAR with a manifest file).

---

### 2. **java** - Launch a Java application
- **Purpose**: Run a Java program by executing a class file or JAR.
- **Common Usage**:
  ```bash
  java MyClass              # Run a class file
  java -jar myapp.jar       # Run a JAR file
  java -cp . MyClass        # Run with a specific classpath
  ```
- **Example**: `java -Xmx512m -jar myapp.jar` (runs a JAR with 512MB max heap).

---

### 3. **javadoc** - Generate API documentation
- **Purpose**: Create HTML documentation from Java source code comments.
- **Common Usage**:
  ```bash
  javadoc -d docs MyClass.java  # Generate docs in 'docs' folder
  ```
- **Example**: `javadoc -d docs -sourcepath src -subpackages com.example` (generate docs for a package).

---

### 4. **jcmd** - Send diagnostic commands to a running JVM
- **Purpose**: Interact with a running Java process for diagnostics (e.g., thread dumps, heap info).
- **Common Usage**:
  ```bash
  jcmd <pid> help           # List available commands for a JVM process
  jcmd <pid> Thread.print   # Print thread dump
  ```
- **Example**: `jcmd 1234 GC.run` (trigger garbage collection for process ID 1234).

---

### 5. **jdb** - Java Debugger
- **Purpose**: Debug Java applications interactively.
- **Common Usage**:
  ```bash
  jdb MyClass               # Start debugging a class
  java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005 MyClass  # Run with debug agent
  jdb -attach localhost:5005  # Attach to running JVM
  ```
- **Example**: `jdb -sourcepath src MyClass` (debug with source code).

---

### 6. **jdeps** - Analyze class and JAR dependencies
- **Purpose**: Identify dependencies of a Java application or library.
- **Common Usage**:
  ```bash
  jdeps myapp.jar           # Analyze dependencies in a JAR
  jdeps -s MyClass.class    # Summary of dependencies
  ```
- **Example**: `jdeps -v myapp.jar` (verbose dependency analysis).

---

### 7. **jhsdb** - Java HotSpot Debugger
- **Purpose**: Advanced debugging and analysis of JVM processes (e.g., core dumps).
- **Common Usage**:
  ```bash
  jhsdb jmap --heap --pid <pid>  # Analyze heap of a running process
  jhsdb hsdb                     # Launch HotSpot debugger GUI
  ```
- **Example**: `jhsdb jmap --heap --pid 1234` (dump heap info for process 1234).

---

### 8. **jinfo** - View or modify JVM configuration
- **Purpose**: Inspect or change JVM options for a running process.
- **Common Usage**:
  ```bash
  jinfo <pid>               # View JVM flags and properties
  jinfo -flag +PrintGC <pid>  # Enable a JVM flag
  ```
- **Example**: `jinfo -sysprops 1234` (display system properties for process 1234).

---

### 9. **jmap** - Dump JVM memory or heap information
- **Purpose**: Generate heap dumps or memory statistics.
- **Common Usage**:
  ```bash
  jmap -heap <pid>          # Print heap summary
  jmap -dump:file=dump.hprof <pid>  # Create a heap dump
  ```
- **Example**: `jmap -dump:live,format=b,file=dump.hprof 1234` (dump live objects).

---

### 10. **jpackage** - Package Java applications
- **Purpose**: Create native installers or executables for Java applications (e.g., .deb, .rpm, .exe).
- **Common Usage**:
  ```bash
  jpackage --input target --name MyApp --main-jar myapp.jar --main-class MyClass
  ```
- **Example**: `jpackage --type deb --input target --name MyApp --main-jar myapp.jar` (create a Debian package).

---

### 11. **jps** - List running JVM processes
- **Purpose**: Display Java processes with their process IDs (PIDs).
- **Common Usage**:
  ```bash
  jps                       # List all Java processes
  jps -l                    # Include full class names
  ```
- **Example**: `jps -m` (show main class and arguments).

---

### 12. **jrunscript** - Run scripts in Java
- **Purpose**: Execute scripts (e.g., JavaScript) using the Java scripting engine.
- **Common Usage**:
  ```bash
  jrunscript -e "print('Hello')"  # Run a single script command
  jrunscript script.js            # Run a script file
  ```
- **Example**: `jrunscript -l js -e "print(2+2)"` (run JavaScript code).

---

### 13. **jshell** - Interactive Java REPL
- **Purpose**: Run Java code snippets interactively for testing or learning.
- **Common Usage**:
  ```bash
  jshell                    # Start interactive shell
  jshell script.jsh         # Run a JShell script
  ```
- **Example**: `jshell -q` (start JShell in quiet mode).

---

### 14. **jstack** - Generate thread dumps
- **Purpose**: Capture the stack traces of threads in a running JVM.
- **Common Usage**:
  ```bash
  jstack <pid>              # Print thread dump
  jstack -l <pid>           # Include lock information
  ```
- **Example**: `jstack 1234 > threads.txt` (save thread dump to a file).

---

### 15. **jstat** - Monitor JVM statistics
- **Purpose**: Display performance statistics (e.g., garbage collection, memory usage).
- **Common Usage**:
  ```bash
  jstat -gc <pid>           # Show garbage collection stats
  jstat -class <pid> 1000   # Show class loading stats every 1 second
  ```
- **Example**: `jstat -gcutil 1234 1000 5` (show GC stats 5 times, every 1 second).

---

### 16. **jstatd** - JVM monitoring daemon
- **Purpose**: Run a remote monitoring server to allow tools like `jstat` to connect remotely.
- **Common Usage**:
  ```bash
  jstatd -J-Djava.security.policy=jstatd.policy
  ```
- **Example**: `jstatd -p 1099` (start daemon on port 1099).

---

### 17. **keytool** - Manage cryptographic keys and certificates
- **Purpose**: Create and manage keystores for secure Java applications.
- **Common Usage**:
  ```bash
  keytool -genkeypair -alias mykey -keystore keystore.jks  # Generate a key pair
  keytool -list -keystore keystore.jks                     # List keystore contents
  ```
- **Example**: `keytool -importcert -file cert.pem -keystore keystore.jks` (import a certificate).

---

### 18. **rmiregistry** - Start RMI registry
- **Purpose**: Run a registry for Java Remote Method Invocation (RMI) objects.
- **Common Usage**:
  ```bash
  rmiregistry               # Start RMI registry on default port (1099)
  rmiregistry 1234          # Start on a specific port
  ```
- **Example**: `rmiregistry -J-Djava.rmi.server.codebase=file:./classes/` (start with a codebase).

---

### 19. **serialver** - Generate serialVersionUID for classes
- **Purpose**: Compute the `serialVersionUID` for Java classes implementing `Serializable`.
- **Common Usage**:
  ```bash
  serialver MyClass         # Print serialVersionUID for a class
  ```
- **Example**: `serialver -classpath . com.example.MyClass` (compute for a specific class).

---

### 20. **javac** - Java compiler
- **Purpose**: Compile Java source files into bytecode.
- **Common Usage**:
  ```bash
  javac MyClass.java        # Compile a single file
  javac -d bin *.java       # Compile to a specific directory
  ```
- **Example**: `javac -cp lib/* -sourcepath src -d bin src/MyClass.java` (compile with dependencies).

---

### 21. **javap** - Disassemble class files
- **Purpose**: View the bytecode or method signatures of a compiled class.
- **Common Usage**:
  ```bash
  javap -c MyClass          # Disassemble bytecode
  javap -s MyClass          # Show method signatures
  ```
- **Example**: `javap -c -private MyClass` (show private methods and bytecode).

---

### 22. **jconsole** - Graphical JVM monitoring tool
- **Purpose**: Monitor JVM performance (memory, threads, CPU) via a GUI.
- **Common Usage**:
  ```bash
  jconsole                  # Start JConsole and connect to a local JVM
  jconsole <pid>            # Connect to a specific process
  ```
- **Example**: `jconsole localhost:1234` (connect to a remote JVM).

---

### 23. **jdeprscan** - Scan for deprecated APIs
- **Purpose**: Identify usage of deprecated APIs in a JAR or class file.
- **Common Usage**:
  ```bash
  jdeprscan myapp.jar       # Scan a JAR for deprecated APIs
  ```
- **Example**: `jdeprscan --release 11 myapp.jar` (check against Java 11 APIs).

---

### 24. **jfr** - Java Flight Recorder
- **Purpose**: Manage and analyze Java Flight Recorder profiling data.
- **Common Usage**:
  ```bash
  jfr print recording.jfr   # Print contents of a JFR file
  jfr summary recording.jfr # Summarize a JFR file
  ```
- **Example**: `jfr print --events GC recording.jfr` (show GC events).

---

### 25. **jimage** - Inspect or extract JIMAGE files
- **Purpose**: Work with JIMAGE files (used in JDK modules).
- **Common Usage**:
  ```bash
  jimage extract image.jimage  # Extract contents of a JIMAGE file
  ```
- **Example**: `jimage list image.jimage` (list contents of a JIMAGE).

---

### 26. **jlink** - Create custom Java runtime images
- **Purpose**: Build a minimal JRE with only required modules.
- **Common Usage**:
  ```bash
  jlink --module-path mods --add-modules java.base --output myjre
  ```
- **Example**: `jlink --add-modules java.base,java.sql --output custom-jre` (create JRE with specific modules).

---

### 27. **jmod** - Manage JMOD files
- **Purpose**: Create or manage JMOD files (used for JDK modules).
- **Common Usage**:
  ```bash
  jmod create --class-path classes mymod.jmod  # Create a JMOD file
  jmod list mymod.jmod                        # List contents
  ```
- **Example**: `jmod extract mymod.jmod` (extract JMOD contents).

---

### 28. **jwebserver** - Simple HTTP server
- **Purpose**: Run a basic web server for serving static files.
- **Common Usage**:
  ```bash
  jwebserver -d /path/to/dir  # Start server for a directory
  jwebserver -p 8080          # Start on a specific port
  ```
- **Example**: `jwebserver -d ./html -p 8000` (serve files from ./html on port 8000).

---

### Tips for Further Learning
- **Documentation**: Run `tool_name --help` or check Oracle’s JDK documentation (e.g., https://docs.oracle.com/en/java/javase/21/docs/specs/man/).
- **Man Pages**: Use `man tool_name` for tools with manual pages.
- **Practice**: Experiment in a test project to understand tool behavior.
- **Monitoring Tools**: For `jcmd`, `jmap`, `jstack`, etc., use `jps` to find the PID of your Java process.
- **Debugging**: Combine `jdb`, `jhsdb`, or `jconsole` for advanced debugging.

If you’re working on a trading project (as suggested by your directory), tools like `javac`, `java`, `jar`, and `jpackage` are likely most relevant for compiling, running, and packaging your application. For performance tuning, use `jstat`, `jmap`, or `jfr`. Let me know if you need a deeper dive into any specific tool or help with your trading project!
