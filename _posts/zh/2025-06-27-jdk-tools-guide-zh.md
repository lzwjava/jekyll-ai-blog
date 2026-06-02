---
audio: false
generated: true
lang: zh
layout: post
title: OpenJDK 21工具概览
translated: true
type: note
---

目录 `/usr/lib/jvm/java-21-openjdk-amd64/bin/` 包含 OpenJDK 21 开发工具包（JDK）提供的工具。这些工具用于 Java 开发、调试、监控和打包等相关任务。以下是各工具及其常见用途的简明说明。要获取详细用法，可在终端中运行 `tool_name --help` 或 `man tool_name` 查看大多数工具的帮助信息。

---

### 1. **jar** - 创建和管理 Java 归档文件
- **用途**：将 Java 类和资源打包成 JAR 文件，或从 JAR 中提取内容。
- **常用命令**：
  ```bash
  jar cf myapp.jar *.class  # 创建 JAR 文件
  jar xf myapp.jar          # 解压 JAR 文件内容
  jar tf myapp.jar          # 列出 JAR 文件内容
  ```
- **示例**：`jar cvfm myapp.jar manifest.txt *.class`（创建包含清单文件的 JAR）。

---

### 2. **java** - 启动 Java 应用程序
- **用途**：通过执行类文件或 JAR 来运行 Java 程序。
- **常用命令**：
  ```bash
  java MyClass              # 运行类文件
  java -jar myapp.jar       # 运行 JAR 文件
  java -cp . MyClass        # 使用指定类路径运行
  ```
- **示例**：`java -Xmx512m -jar myapp.jar`（以 512MB 最大堆内存运行 JAR）。

---

### 3. **javadoc** - 生成 API 文档
- **用途**：根据 Java 源代码注释生成 HTML 文档。
- **常用命令**：
  ```bash
  javadoc -d docs MyClass.java  # 在 'docs' 目录生成文档
  ```
- **示例**：`javadoc -d docs -sourcepath src -subpackages com.example`（为包生成文档）。

---

### 4. **jcmd** - 向运行中的 JVM 发送诊断命令
- **用途**：与运行中的 Java 进程交互进行诊断（如线程转储、堆信息）。
- **常用命令**：
  ```bash
  jcmd <pid> help           # 列出 JVM 进程可用命令
  jcmd <pid> Thread.print   # 打印线程转储
  ```
- **示例**：`jcmd 1234 GC.run`（为进程 ID 1234 触发垃圾回收）。

---

### 5. **jdb** - Java 调试器
- **用途**：交互式调试 Java 应用程序。
- **常用命令**：
  ```bash
  jdb MyClass               # 开始调试类文件
  java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005 MyClass  # 使用调试代理运行
  jdb -attach localhost:5005  # 连接到运行中的 JVM
  ```
- **示例**：`jdb -sourcepath src MyClass`（带源代码调试）。

---

### 6. **jdeps** - 分析类和 JAR 依赖关系
- **用途**：识别 Java 应用程序或库的依赖项。
- **常用命令**：
  ```bash
  jdeps myapp.jar           # 分析 JAR 中的依赖关系
  jdeps -s MyClass.class    # 依赖关系摘要
  ```
- **示例**：`jdeps -v myapp.jar`（详细依赖关系分析）。

---

### 7. **jhsdb** - Java HotSpot 调试器
- **用途**：对 JVM 进程进行高级调试和分析（如核心转储）。
- **常用命令**：
  ```bash
  jhsdb jmap --heap --pid <pid>  # 分析运行中进程的堆内存
  jhsdb hsdb                     # 启动 HotSpot 调试器图形界面
  ```
- **示例**：`jhsdb jmap --heap --pid 1234`（转储进程 1234 的堆信息）。

---

### 8. **jinfo** - 查看或修改 JVM 配置
- **用途**：检查或更改运行中进程的 JVM 选项。
- **常用命令**：
  ```bash
  jinfo <pid>               # 查看 JVM 标志和属性
  jinfo -flag +PrintGC <pid>  # 启用 JVM 标志
  ```
- **示例**：`jinfo -sysprops 1234`（显示进程 1234 的系统属性）。

---

### 9. **jmap** - 转储 JVM 内存或堆信息
- **用途**：生成堆转储或内存统计信息。
- **常用命令**：
  ```bash
  jmap -heap <pid>          # 打印堆摘要
  jmap -dump:file=dump.hprof <pid>  # 创建堆转储文件
  ```
- **示例**：`jmap -dump:live,format=b,file=dump.hprof 1234`（转储存活对象）。

---

### 10. **jpackage** - 打包 Java 应用程序
- **用途**：为 Java 应用程序创建原生安装包或可执行文件（如 .deb、.rpm、.exe）。
- **常用命令**：
  ```bash
  jpackage --input target --name MyApp --main-jar myapp.jar --main-class MyClass
  ```
- **示例**：`jpackage --type deb --input target --name MyApp --main-jar myapp.jar`（创建 Debian 包）。

---

### 11. **jps** - 列出运行中的 JVM 进程
- **用途**：显示 Java 进程及其进程 ID。
- **常用命令**：
  ```bash
  jps                       # 列出所有 Java 进程
  jps -l                    # 包含完整类名
  ```
- **示例**：`jps -m`（显示主类及参数）。

---

### 12. **jrunscript** - 在 Java 中运行脚本
- **用途**：使用 Java 脚本引擎执行脚本（如 JavaScript）。
- **常用命令**：
  ```bash
  jrunscript -e "print('Hello')"  # 运行单行脚本命令
  jrunscript script.js            # 运行脚本文件
  ```
- **示例**：`jrunscript -l js -e "print(2+2)"`（运行 JavaScript 代码）。

---

### 13. **jshell** - 交互式 Java REPL
- **用途**：交互式运行 Java 代码片段以进行测试或学习。
- **常用命令**：
  ```bash
  jshell                    # 启动交互式解释器
  jshell script.jsh         # 运行 JShell 脚本
  ```
- **示例**：`jshell -q`（以静默模式启动 JShell）。

---

### 14. **jstack** - 生成线程转储
- **用途**：捕获运行中 JVM 的线程堆栈轨迹。
- **常用命令**：
  ```bash
  jstack <pid>              # 打印线程转储
  jstack -l <pid>           # 包含锁信息
  ```
- **示例**：`jstack 1234 > threads.txt`（将线程转储保存至文件）。

---

### 15. **jstat** - 监控 JVM 统计信息
- **用途**：显示性能统计信息（如垃圾回收、内存使用情况）。
- **常用命令**：
  ```bash
  jstat -gc <pid>           # 显示垃圾回收统计
  jstat -class <pid> 1000   # 每秒显示类加载统计
  ```
- **示例**：`jstat -gcutil 1234 1000 5`（每秒显示 GC 统计，共 5 次）。

---

### 16. **jstatd** - JVM 监控守护进程
- **用途**：运行远程监控服务器，允许 `jstat` 等工具远程连接。
- **常用命令**：
  ```bash
  jstatd -J-Djava.security.policy=jstatd.policy
  ```
- **示例**：`jstatd -p 1099`（在 1099 端口启动守护进程）。

---

### 17. **keytool** - 管理加密密钥和证书
- **用途**：为安全的 Java 应用程序创建和管理密钥库。
- **常用命令**：
  ```bash
  keytool -genkeypair -alias mykey -keystore keystore.jks  # 生成密钥对
  keytool -list -keystore keystore.jks                     # 列出密钥库内容
  ```
- **示例**：`keytool -importcert -file cert.pem -keystore keystore.jks`（导入证书）。

---

### 18. **rmiregistry** - 启动 RMI 注册表
- **用途**：为 Java 远程方法调用对象运行注册表。
- **常用命令**：
  ```bash
  rmiregistry               # 在默认端口启动 RMI 注册表
  rmiregistry 1234          # 在指定端口启动
  ```
- **示例**：`rmiregistry -J-Djava.rmi.server.codebase=file:./classes/`（指定代码库启动）。

---

### 19. **serialver** - 为类生成 serialVersionUID
- **用途**：计算实现 `Serializable` 接口的 Java 类的 `serialVersionUID`。
- **常用命令**：
  ```bash
  serialver MyClass         # 打印类的 serialVersionUID
  ```
- **示例**：`serialver -classpath . com.example.MyClass`（计算指定类的序列化版本）。

---

### 20. **javac** - Java 编译器
- **用途**：将 Java 源文件编译为字节码。
- **常用命令**：
  ```bash
  javac MyClass.java        # 编译单个文件
  javac -d bin *.java       # 编译到指定目录
  ```
- **示例**：`javac -cp lib/* -sourcepath src -d bin src/MyClass.java`（带依赖编译）。

---

### 21. **javap** - 反汇编类文件
- **用途**：查看已编译类的字节码或方法签名。
- **常用命令**：
  ```bash
  javap -c MyClass          # 反汇编字节码
  javap -s MyClass          # 显示方法签名
  ```
- **示例**：`javap -c -private MyClass`（显示私有方法和字节码）。

---

### 22. **jconsole** - 图形化 JVM 监控工具
- **用途**：通过图形界面监控 JVM 性能（内存、线程、CPU）。
- **常用命令**：
  ```bash
  jconsole                  # 启动 JConsole 并连接本地 JVM
  jconsole <pid>            # 连接指定进程
  ```
- **示例**：`jconsole localhost:1234`（连接远程 JVM）。

---

### 23. **jdeprscan** - 扫描已弃用 API
- **用途**：识别 JAR 或类文件中已弃用 API 的使用情况。
- **常用命令**：
  ```bash
  jdeprscan myapp.jar       # 扫描 JAR 中的已弃用 API
  ```
- **示例**：`jdeprscan --release 11 myapp.jar`（基于 Java 11 API 检查）。

---

### 24. **jfr** - Java Flight Recorder
- **用途**：管理和分析 Java Flight Recorder 性能分析数据。
- **常用命令**：
  ```bash
  jfr print recording.jfr   # 打印 JFR 文件内容
  jfr summary recording.jfr # 汇总 JFR 文件信息
  ```
- **示例**：`jfr print --events GC recording.jfr`（显示 GC 事件）。

---

### 25. **jimage** - 检查或提取 JIMAGE 文件
- **用途**：处理 JDK 模块使用的 JIMAGE 文件。
- **常用命令**：
  ```bash
  jimage extract image.jimage  # 提取 JIMAGE 文件内容
  ```
- **示例**：`jimage list image.jimage`（列出 JIMAGE 文件内容）。

---

### 26. **jlink** - 创建自定义 Java 运行时镜像
- **用途**：构建仅包含所需模块的最小化 JRE。
- **常用命令**：
  ```bash
  jlink --module-path mods --add-modules java.base --output myjre
  ```
- **示例**：`jlink --add-modules java.base,java.sql --output custom-jre`（创建含指定模块的 JRE）。

---

### 27. **jmod** - 管理 JMOD 文件
- **用途**：创建或管理 JDK 模块使用的 JMOD 文件。
- **常用命令**：
  ```bash
  jmod create --class-path classes mymod.jmod  # 创建 JMOD 文件
  jmod list mymod.jmod                        # 列出文件内容
  ```
- **示例**：`jmod extract mymod.jmod`（解压 JMOD 文件内容）。

---

### 28. **jwebserver** - 简易 HTTP 服务器
- **用途**：运行基础 Web 服务器以提供静态文件服务。
- **常用命令**：
  ```bash
  jwebserver -d /path/to/dir  # 为指定目录启动服务器
  jwebserver -p 8080          # 在指定端口启动
  ```
- **示例**：`jwebserver -d ./html -p 8000`（在 8000 端口提供 ./html 目录文件服务）。

---

### 进阶学习建议
- **文档查阅**：运行 `tool_name --help` 或查阅 Oracle JDK 文档（如 https://docs.oracle.com/en/java/javase/21/docs/specs/man/）
- **手册页**：对带手册页的工具使用 `man tool_name` 命令
- **实践操作**：在测试项目中实验以理解工具行为
- **监控工具**：使用 `jps` 查找 Java 进程 PID 后配合 `jcmd`、`jmap`、`jstack` 等工具
- **调试技巧**：组合使用 `jdb`、`jhsdb` 或 `jconsole` 进行高级调试

如果您正在开发交易项目（根据目录名称推测），`javac`、`java`、`jar` 和 `jpackage` 等工具可能最适用于编译、运行和打包应用程序。性能调优时可使用 `jstat`、`jmap` 或 `jfr`。如需深入了解特定工具或获取交易项目相关帮助，请随时告知！
