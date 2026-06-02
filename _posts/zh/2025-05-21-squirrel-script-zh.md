---
audio: false
generated: true
lang: zh
layout: post
title: SQuirreL启动脚本
translated: true
type: note
---

此批处理脚本用于启动 SQuirreL SQL Client（一款基于 Java 的数据库管理工具）。以下是对该脚本的详细解析，逐步说明其用途、结构和功能。

---

### **概述**

该脚本设计用于：

1. 配置运行 SQuirreL SQL Client 所需的 Java 环境
2. 验证 Java 版本兼容性（需要 Java 1.6 或 1.7）
3. 检查软件更新并在可用时应用
4. 构建 SQuirreL 及其库的类路径
5. 使用适当参数启动 SQuirreL SQL Client 应用程序

该脚本专为 Windows 系统编写（使用 `.bat` 扩展名），采用 Windows 命令提示符的批处理脚本语言。

---

### **逐行详解**

#### **1. `@echo off`**

- **用途**：禁用命令在控制台的回显，通过仅显示预期输出（如错误信息或特定的 `echo` 语句）使脚本输出更清晰
- **效果**：除非使用 `echo` 显式打印，否则脚本中执行的命令不会显示

---

#### **2. `@rem IZPACK_JAVA is filtered in by the IzPack installer when this script is installed`**

- **用途**：注释（`@rem`）说明 `IZPACK_JAVA` 变量由 IzPack 安装程序在安装过程中设置
- **背景**：IzPack 是用于创建 Java 应用程序安装程序的工具，它在脚本中动态设置 `JAVA_HOME` 环境变量以指向安装期间使用的 Java 安装路径

#### **3. `set IZPACK_JAVA=%JAVA_HOME`**

- **用途**：将 `JAVA_HOME` 环境变量（由 IzPack 设置）的值赋给 `IZPACK_JAVA` 变量
- **说明**：这确保脚本知道 Java 安装位置。`JAVA_HOME` 通常指向 Java 开发工具包（JDK）或 Java 运行时环境（JRE）的根目录

---

#### **4. Java 检测逻辑**

```bat
@rem 我们根据以下算法检测要使用的 java 可执行文件：
@rem 1. 如果 IzPack 安装程序使用的 java 可用，则使用该版本；否则
@rem 2. 使用命令路径中的 java
if exist "%IZPACK_JAVA%\bin\javaw.exe" (
  set LOCAL_JAVA=%IZPACK_JAVA%\bin\javaw.exe
) else (
  set LOCAL_JAVA=javaw.exe
)
```

- **用途**：确定用于运行 SQuirreL SQL 的 Java 可执行文件
- **逻辑**：
  1. **检查 IzPack Java**：脚本检查 `javaw.exe` 是否存在于 `IZPACK_JAVA` 指定的 Java 安装目录的 `bin` 子目录中（即 `%IZPACK_JAVA%\bin\javaw.exe`）
     - `javaw.exe` 是 Windows 特有的 Java 可执行文件，它运行 Java 应用程序时不打开控制台窗口（与 `java.exe` 不同）
     - 如果找到，`LOCAL_JAVA` 设置为 `javaw.exe` 的完整路径
  2. **回退到 PATH**：如果在 `IZPACK_JAVA` 目录中未找到 `javaw.exe`，脚本将回退使用系统 `PATH` 环境变量中的 `javaw.exe`
- **为何使用 `javaw.exe`？**：使用 `javaw.exe` 可确保应用程序在没有持久命令窗口的情况下运行，提供更简洁的用户体验

#### **5. `echo Using java: %LOCAL_JAVA%`**

- **用途**：将正在使用的 Java 可执行文件路径打印到控制台，用于调试或信息目的
- **示例输出**：如果 `LOCAL_JAVA` 为 `C:\Program Files\Java\jre1.6.0_45\bin\javaw.exe`，将显示：

  ```
  Using java: C:\Program Files\Java\jre1.6.0_45\bin\javaw.exe
  ```

---

#### **6. 确定 SQuirreL SQL 主目录**

```bat
set basedir=%~f0
:strip
set removed=%basedir:~-1%
set basedir=%basedir:~0,-1%
if NOT "%removed%"=="\" goto strip
set SQUIRREL_SQL_HOME=%basedir%
```

- **用途**：确定 SQuirreL SQL 的安装目录（`SQUIRREL_SQL_HOME`）
- **说明**：
  - `%~f0`：扩展为批处理脚本本身的完整路径（例如 `C:\Program Files\SQuirreL\squirrel-sql.bat`）
  - **`:strip` 循环**：脚本迭代地从 `basedir` 移除最后一个字符，直到遇到反斜杠（`\`），从而去除脚本文件名得到目录路径
  - **结果**：`SQUIRREL_SQL_HOME` 设置为包含脚本的目录（例如 `C:\Program Files\SQuirreL`）
- **为何采用此方法？**：这确保脚本可以动态确定自身的安装目录，使其在不同系统间具有可移植性

---

#### **7. Java 版本检查**

```bat
"%LOCAL_JAVA%" -cp "%SQUIRREL_SQL_HOME%\lib\versioncheck.jar" JavaVersionChecker 1.6 1.7
if ErrorLevel 1 goto ExitForWrongJavaVersion
```

- **用途**：验证 Java 版本与 SQuirreL SQL 兼容（需要 Java 1.6 或 1.7）
- **说明**：
  - 脚本运行 `JavaVersionChecker` 类，该类来自 SQuirreL SQL 的 `lib` 目录中的 `versioncheck.jar`
  - **`-cp`**：指定类路径，指向 `versioncheck.jar`
  - **参数**：`1.6 1.7` 表示 Java 版本必须为 1.6 或 1.7
  - **注意**：`versioncheck.jar` 编译时兼容 Java 1.2.2，确保其可以在较旧的 JVM 上运行以执行版本检查
  - **错误处理**：如果 Java 版本不兼容，`ErrorLevel` 设置为 1，脚本跳转到 `:ExitForWrongJavaVersion` 标签，终止执行
- **为何进行此检查？**：SQuirreL SQL 需要特定 Java 版本才能正常运行，这防止应用程序在不支持的 JVM 上运行

---

#### **8. 软件更新检查**

```bat
if not exist "%SQUIRREL_SQL_HOME%\update\changeList.xml" goto launchsquirrel
SET TMP_CP="%SQUIRREL_SQL_HOME%\update\downloads\core\squirrel-sql.jar"
if not exist %TMP_CP% goto launchsquirrel
dir /b "%SQUIRREL_SQL_HOME%\update\downloads\core\*.*" > %TEMP%\update-lib.tmp
FOR /F %%I IN (%TEMP%\update-lib.tmp) DO CALL "%SQUIRREL_SQL_HOME%\addpath.bat" "%SQUIRREL_SQL_HOME%\update\downloads\core\%%I"
SET UPDATE_CP=%TMP_CP%
SET UPDATE_PARMS=--log-config-file "%SQUIRREL_SQL_HOME%\update-log4j.properties" --squirrel-home "%SQUIRREL_SQL_HOME%" %1 %2 %3 %4 %5 %6 %7 %8 %9
"%LOCAL_JAVA%" -cp %UPDATE_CP% -Dlog4j.defaultInitOverride=true -Dprompt=true net.sourceforge.squirrel_sql.client.update.gui.installer.PreLaunchUpdateApplication %UPDATE_PARAMS%
```

- **用途**：在启动主应用程序前检查并应用软件更新
- **说明**：
  1. **检查更新文件**：
     - 脚本检查 `update` 目录中是否存在 `changeList.xml`。该文件由 SQuirreL 的软件更新功能创建，用于跟踪更新
     - 如果 `changeList.xml` 不存在，脚本跳过更新过程并跳转到 `:launchsquirrel`
     - 它还检查 `update\downloads\core` 目录中是否存在更新的 `squirrel-sql.jar`。如果不存在，脚本跳转到 `:launchsquirrel`
  2. **构建更新类路径**：
     - `dir /b` 命令列出 `update\downloads\core` 目录中的所有文件，并将其写入临时文件（`%TEMP%\update-lib.tmp`）
     - `FOR /F` 循环遍历 `update-lib.tmp` 中的文件，并调用 `addpath.bat` 将每个文件追加到存储在 `TMP_CP` 中的类路径
     - `UPDATE_CP` 设置为类路径，起始于更新目录中的 `squirrel-sql.jar`
  3. **设置更新参数**：
     - `UPDATE_PARMS` 包括：
       - `--log-config-file`：指定更新过程中日志记录的 Log4j 配置文件
       - `--squirrel-home`：传递 SQuirreL 安装目录
       - `%1 %2 %3 ... %9`：传递提供给脚本的任何命令行参数
  4. **运行更新应用程序**：
     - 脚本启动 `PreLaunchUpdateApplication`（`squirrel-sql.jar` 中的一个 Java 类）以应用更新
     - **`-Dlog4j.defaultInitOverride=true`**：覆盖默认的 Log4j 配置
     - **`-Dprompt=true`**：可能在更新过程中启用交互式提示
- **为何有此步骤？**：SQuirreL SQL 支持自动更新，此部分确保在启动主应用程序前应用任何已下载的更新

---

#### **9. 启动 SQuirreL SQL**

```bat
:launchsquirrel
@rem 构建 SQuirreL 的类路径
set TMP_CP="%SQUIRREL_SQL_HOME%\squirrel-sql.jar"
dir /b "%SQUIRREL_SQL_HOME%\lib\*.*" > %TEMP%\squirrel-lib.tmp
FOR /F %%I IN (%TEMP%\squirrel-lib.tmp) DO CALL "%SQUIRREL_SQL_HOME%\addpath.bat" "%SQUIRREL_SQL_HOME%\lib\%%I"
SET SQUIRREL_CP=%TMP_CP%
echo "SQUIRREL_CP=%SQUIRREL_CP%"
```

- **用途**：构建主 SQuirreL SQL 应用程序的类路径并准备启动
- **说明**：
  1. **初始化类路径**：
     - `TMP_CP` 使用 SQuirreL 安装目录中 `squirrel-sql.jar` 的路径进行初始化
  2. **添加库 Jar 文件**：
     - `dir /b` 命令列出 `lib` 目录中的所有文件，并将其写入 `squirrel-lib.tmp`
     - `FOR /F` 循环遍历文件，并调用 `addpath.bat` 将每个库文件（如 `.jar` 文件）追加到 `TMP_CP` 类路径
  3. **设置最终类路径**：
     - `SQUIRREL_CP` 设置为完成的类路径
  4. **调试输出**：
     - 脚本打印最终类路径（`SQUIRREL_CP`）用于调试目的

---

#### **10. 设置启动参数**

```bat
SET TMP_PARMS=--log-config-file "%SQUIRREL_SQL_HOME%\log4j.properties" --squirrel-home "%SQUIRREL_SQL_HOME%" %1 %2 %3 %4 %5 %6 %7 %8 %9
```

- **用途**：定义传递给 SQuirreL SQL 应用程序的参数
- **说明**：
  - `--log-config-file`：指定主应用程序的 Log4j 配置文件
  - `--squirrel-home`：传递 SQuirreL 安装目录
  - `%1 %2 ... %9`：传递提供给脚本的任何命令行参数

---

#### **11. 启动应用程序**

```bat
@rem -Dsun.java2d.noddraw=true 防止在 Win32 系统上出现性能问题
start "SQuirreL SQL Client" /B "%LOCAL_JAVA%" -Xmx256m -Dsun.java2d.noddraw=true -cp %SQUIRREL_CP% -splash:"%SQUIRREL_SQL_HOME%/icons/splash.jpg" net.sourceforge.squirrel_sql.client.Main %TMP_PARMS%
```

- **用途**：启动 SQuirreL SQL Client 应用程序
- **说明**：
  - **`start "SQuirreL SQL Client" /B`**：在新进程中运行命令，不打开新的控制台窗口（`/B` 抑制窗口）
  - **`%LOCAL_JAVA%`**：指定要使用的 Java 可执行文件
  - **`-Xmx256m`**：设置 Java 堆最大大小为 256 MB 以限制内存使用
  - **`-Dsun.java2d.noddraw=true`**：禁用 Java 2D 图形的 DirectDraw，以避免 Windows 系统上的性能问题
  - **`-cp %SQUIRREL_CP%`**：指定应用程序的类路径
  - **`-splash:"%SQUIRREL_SQL_HOME%/icons/splash.jpg"`**：在应用程序启动时显示启动画面（图像）
  - **`net.sourceforge.squirrel_sql.client.Main`**：要执行的主 Java 类
  - **`%TMP_PARMS%`**：传递先前定义的参数

---

#### **12. 错误 Java 版本退出**

```bat
:ExitForWrongJavaVersion
```

- **用途**：如果 Java 版本检查失败，用作退出点的标签
- **说明**：如果 Java 版本不是 1.6 或 1.7，脚本跳转至此并终止，不启动应用程序

---

### **关键组件和概念**

1. **类路径构建**：
   - 脚本通过包含 `squirrel-sql.jar` 和 `lib` 或 `update\downloads\core` 目录中的所有 `.jar` 文件，动态构建更新过程（`UPDATE_CP`）和主应用程序（`SQUIRREL_CP`）的类路径
   - 假定 `addpath.bat` 脚本（未显示）将每个文件追加到类路径变量

2. **Log4j 配置**：
   - Log4j 是 SQuirreL SQL 使用的日志记录框架。脚本为更新过程（`update-log4j.properties`）和主应用程序（`log4j.properties`）指定了单独的 Log4j 配置文件

3. **软件更新机制**：
   - SQuirreL SQL 支持自动更新，由 `PreLaunchUpdateApplication` 类管理。脚本检查更新文件并在必要时运行更新过程

4. **Java 版本兼容性**：
   - 脚本强制要求与 Java 1.6 或 1.7 严格兼容，可能是由于这些版本特定的依赖项或功能

5. **可移植性**：
   - 脚本通过动态确定安装目录和 Java 可执行文件位置，设计为可移植

---

### **潜在问题和注意事项**

1. **Java 版本限制**：
   - 脚本仅允许 Java 1.6 或 1.7，这些版本已过时（分别于 2006 年和 2011 年发布）。现代系统可能装有更新的 Java 版本，导致脚本失败，除非安装了兼容的 JRE
   - **解决方法**：用户可能需要安装兼容的 JRE，或修改脚本以支持更新的版本（如果 SQuirreL SQL 兼容）

2. **硬编码路径**：
   - 脚本假定某些文件（如 `squirrel-sql.jar`、`versioncheck.jar`、`addpath.bat`）存在于相对于 `SQUIRREL_SQL_HOME` 的特定目录中。如果这些文件缺失或移动，脚本将失败

3. **Windows 特定**：
   - 脚本使用 Windows 特定命令（`dir /b`、`FOR /F`、`start /B`）和 `javaw.exe`，使其在不修改的情况下与非 Windows 系统不兼容

4. **错误处理**：
   - 脚本处理 Java 版本错误，但未为其他故障（如缺失 `squirrel-sql.jar` 或无效类路径）提供详细的错误消息

5. **内存限制**：
   - `-Xmx256m` 标志将 JVM 内存限制为 256 MB，对于大型数据库或复杂查询可能不足，可能导致 `OutOfMemoryError`

---

### **总结**

此批处理脚本是 SQuirreL SQL Client 的启动器，执行以下任务：

- 检测并配置 Java 可执行文件
- 验证 Java 版本兼容性（1.6 或 1.7）
- 检查并在可用时应用软件更新
- 构建应用程序的类路径
- 使用适当参数（包括启动画面和内存设置）启动 SQuirreL SQL

该脚本结构良好，适合其用途，但针对特定环境（Windows、Java 1.6/1.7）定制，可能需要更新以支持现代系统或更新的 Java 版本。

如果您有进一步的问题或需要协助修改脚本（例如支持更新的 Java 版本），请告知！
