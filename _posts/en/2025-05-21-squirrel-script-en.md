---
audio: false
generated: true
lang: en
layout: post
title: SQuirreL Launch Script
translated: false
type: note
---

This batch script is used to launch the SQuirreL SQL Client, a Java-based database administration tool. Below is a comprehensive explanation of the script, breaking down its purpose, structure, and functionality step by step.

---

### **Overview**
The script is designed to:
1. Configure the Java environment to run SQuirreL SQL Client.
2. Verify the Java version compatibility (requires Java 1.6 or 1.7).
3. Check for software updates and apply them if available.
4. Build the classpath for SQuirreL and its libraries.
5. Launch the SQuirreL SQL Client application with appropriate parameters.

The script is written for Windows (using the `.bat` extension) and uses the Windows Command Prompt's batch scripting language.

---

### **Line-by-Line Explanation**

#### **1. `@echo off`**
- **Purpose**: Disables the echoing of commands to the console, making the script's output cleaner by showing only the intended output (e.g., error messages or specific `echo` statements).
- **Effect**: Commands executed in the script are not displayed unless explicitly printed using `echo`.

---

#### **2. `@rem IZPACK_JAVA is filtered in by the IzPack installer when this script is installed`**
- **Purpose**: A comment (`@rem`) indicating that the `IZPACK_JAVA` variable is set by the IzPack installer during installation.
- **Context**: IzPack is a tool used to create installers for Java applications. It dynamically sets the `JAVA_HOME` environment variable in the script to point to the Java installation used during setup.

#### **3. `set IZPACK_JAVA=%JAVA_HOME`**
- **Purpose**: Assigns the value of the `JAVA_HOME` environment variable (set by IzPack) to the `IZPACK_JAVA` variable.
- **Explanation**: This ensures the script knows where the Java installation is located. `JAVA_HOME` typically points to the root directory of a Java Development Kit (JDK) or Java Runtime Environment (JRE).

---

#### **4. Java Detection Logic**
```bat
@rem We detect the java executable to use according to the following algorithm:
@rem 1. If the one used by the IzPack installer is available then use that; otherwise
@rem 2. Use the java that is in the command path.
if exist "%IZPACK_JAVA%\bin\javaw.exe" (
  set LOCAL_JAVA=%IZPACK_JAVA%\bin\javaw.exe
) else (
  set LOCAL_JAVA=javaw.exe
)
```
- **Purpose**: Determines which Java executable to use for running SQuirreL SQL.
- **Logic**:
  1. **Check for IzPack Java**: The script checks if `javaw.exe` exists in the `bin` directory of the Java installation specified by `IZPACK_JAVA` (i.e., `%IZPACK_JAVA%\bin\javaw.exe`).
     - `javaw.exe` is a Windows-specific Java executable that runs Java applications without opening a console window (unlike `java.exe`).
     - If found, `LOCAL_JAVA` is set to the full path of `javaw.exe`.
  2. **Fallback to PATH**: If `javaw.exe` is not found in the `IZPACK_JAVA` directory, the script falls back to using `javaw.exe` from the system's `PATH` environment variable.
- **Why `javaw.exe`?**: Using `javaw.exe` ensures the application runs without a persistent command window, providing a cleaner user experience.

#### **5. `echo Using java: %LOCAL_JAVA%`**
- **Purpose**: Prints the path of the Java executable being used to the console for debugging or informational purposes.
- **Example Output**: If `LOCAL_JAVA` is `C:\Program Files\Java\jre1.6.0_45\bin\javaw.exe`, it will display:
  ```
  Using java: C:\Program Files\Java\jre1.6.0_45\bin\javaw.exe
  ```

---

#### **6. Determining the SQuirreL SQL Home Directory**
```bat
set basedir=%~f0
:strip
set removed=%basedir:~-1%
set basedir=%basedir:~0,-1%
if NOT "%removed%"=="\" goto strip
set SQUIRREL_SQL_HOME=%basedir%
```
- **Purpose**: Determines the directory where SQuirreL SQL is installed (`SQUIRREL_SQL_HOME`).
- **Explanation**:
  - `%~f0`: This expands to the full path of the batch script itself (e.g., `C:\Program Files\SQuirreL\squirrel-sql.bat`).
  - **`:strip` Loop**: The script iteratively removes the last character from `basedir` until it encounters a backslash (`\`), effectively stripping the script's filename to get the directory path.
  - **Result**: `SQUIRREL_SQL_HOME` is set to the directory containing the script (e.g., `C:\Program Files\SQuirreL`).
- **Why this approach?**: This ensures the script can dynamically determine its own installation directory, making it portable across different systems.

---

#### **7. Java Version Check**
```bat
"%LOCAL_JAVA%" -cp "%SQUIRREL_SQL_HOME%\lib\versioncheck.jar" JavaVersionChecker 1.6 1.7
if ErrorLevel 1 goto ExitForWrongJavaVersion
```
- **Purpose**: Verifies that the Java version is compatible with SQuirreL SQL (requires Java 1.6 or 1.7).
- **Explanation**:
  - The script runs the `JavaVersionChecker` class from `versioncheck.jar`, located in the `lib` directory of SQuirreL SQL.
  - **`-cp`**: Specifies the classpath, pointing to `versioncheck.jar`.
  - **Arguments**: `1.6 1.7` indicates that the Java version must be 1.6 or 1.7.
  - **Note**: `versioncheck.jar` is compiled with Java 1.2.2 compatibility, ensuring it can run on older JVMs to perform the version check.
  - **Error Handling**: If the Java version is incompatible, the `ErrorLevel` is set to 1, and the script jumps to the `:ExitForWrongJavaVersion` label, terminating execution.
- **Why this check?**: SQuirreL SQL requires specific Java versions to function correctly, and this prevents the application from running on unsupported JVMs.

---

#### **8. Software Update Check**
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
- **Purpose**: Checks for and applies software updates before launching the main application.
- **Explanation**:
  1. **Check for Update Files**:
     - The script checks if `changeList.xml` exists in the `update` directory. This file is created by SQuirreL's software update feature to track updates.
     - If `changeList.xml` does not exist, the script skips the update process and jumps to `:launchsquirrel`.
     - It also checks for the updated `squirrel-sql.jar` in the `update\downloads\core` directory. If it doesn’t exist, the script skips to `:launchsquirrel`.
  2. **Build Update Classpath**:
     - The `dir /b` command lists all files in the `update\downloads\core` directory and writes them to a temporary file (`%TEMP%\update-lib.tmp`).
     - The `FOR /F` loop iterates over the files in `update-lib.tmp` and calls `addpath.bat` to append each file to the classpath stored in `TMP_CP`.
     - `UPDATE_CP` is set to the classpath, starting with `squirrel-sql.jar` from the update directory.
  3. **Set Update Parameters**:
     - `UPDATE_PARMS` includes:
       - `--log-config-file`: Specifies the Log4j configuration file for logging during the update process.
       - `--squirrel-home`: Passes the SQuirreL installation directory.
       - `%1 %2 %3 ... %9`: Passes any command-line arguments provided to the script.
  4. **Run Update Application**:
     - The script launches `PreLaunchUpdateApplication` (a Java class in `squirrel-sql.jar`) to apply updates.
     - **`-Dlog4j.defaultInitOverride=true`**: Overrides the default Log4j configuration.
     - **`-Dprompt=true`**: Likely enables interactive prompts during the update process.
- **Why this step?**: SQuirreL SQL supports automatic updates, and this section ensures any downloaded updates are applied before launching the main application.

---

#### **9. Launch SQuirreL SQL**
```bat
:launchsquirrel
@rem build SQuirreL's classpath
set TMP_CP="%SQUIRREL_SQL_HOME%\squirrel-sql.jar"
dir /b "%SQUIRREL_SQL_HOME%\lib\*.*" > %TEMP%\squirrel-lib.tmp
FOR /F %%I IN (%TEMP%\squirrel-lib.tmp) DO CALL "%SQUIRREL_SQL_HOME%\addpath.bat" "%SQUIRREL_SQL_HOME%\lib\%%I"
SET SQUIRREL_CP=%TMP_CP%
echo "SQUIRREL_CP=%SQUIRREL_CP%"
```
- **Purpose**: Builds the classpath for the main SQuirreL SQL application and prepares to launch it.
- **Explanation**:
  1. **Initialize Classpath**:
     - `TMP_CP` is initialized with the path to `squirrel-sql.jar` in the SQuirreL installation directory.
  2. **Add Library Jars**:
     - The `dir /b` command lists all files in the `lib` directory and writes them to `squirrel-lib.tmp`.
     - The `FOR /F` loop iterates over the files and calls `addpath.bat` to append each library file (e.g., `.jar` files) to the `TMP_CP` classpath.
  3. **Set Final Classpath**:
     - `SQUIRREL_CP` is set to the completed classpath.
  4. **Debug Output**:
     - The script prints the final classpath (`SQUIRREL_CP`) for debugging purposes.

---

#### **10. Set Launch Parameters**
```bat
SET TMP_PARMS=--log-config-file "%SQUIRREL_SQL_HOME%\log4j.properties" --squirrel-home "%SQUIRREL_SQL_HOME%" %1 %2 %3 %4 %5 %6 %7 %8 %9
```
- **Purpose**: Defines the parameters to pass to the SQuirreL SQL application.
- **Explanation**:
  - `--log-config-file`: Specifies the Log4j configuration file for the main application.
  - `--squirrel-home`: Passes the SQuirreL installation directory.
  - `%1 %2 ... %9`: Passes any command-line arguments provided to the script.

---

#### **11. Launch the Application**
```bat
@rem -Dsun.java2d.noddraw=true prevents performance problems on Win32 systems.
start "SQuirreL SQL Client" /B "%LOCAL_JAVA%" -Xmx256m -Dsun.java2d.noddraw=true -cp %SQUIRREL_CP% -splash:"%SQUIRREL_SQL_HOME%/icons/splash.jpg" net.sourceforge.squirrel_sql.client.Main %TMP_PARMS%
```
- **Purpose**: Launches the SQuirreL SQL Client application.
- **Explanation**:
  - **`start "SQuirreL SQL Client" /B`**: Runs the command in a new process without opening a new console window (`/B` suppresses the window).
  - **`%LOCAL_JAVA%`**: Specifies the Java executable to use.
  - **`-Xmx256m`**: Sets the maximum Java heap size to 256 MB to limit memory usage.
  - **`-Dsun.java2d.noddraw=true`**: Disables DirectDraw for Java 2D graphics to avoid performance issues on Windows systems.
  - **`-cp %SQUIRREL_CP%`**: Specifies the classpath for the application.
  - **`-splash:"%SQUIRREL_SQL_HOME%/icons/splash.jpg"`**: Displays a splash screen (an image) when the application starts.
  - **`net.sourceforge.squirrel_sql.client.Main`**: The main Java class to execute.
  - **`%TMP_PARMS%`**: Passes the parameters defined earlier.

---

#### **12. Exit for Wrong Java Version**
```bat
:ExitForWrongJavaVersion
```
- **Purpose**: A label used as an exit point if the Java version check fails.
- **Explanation**: If the Java version is not 1.6 or 1.7, the script jumps here and terminates without launching the application.

---

### **Key Components and Concepts**
1. **Classpath Construction**:
   - The script dynamically builds the classpath for both the update process (`UPDATE_CP`) and the main application (`SQUIRREL_CP`) by including `squirrel-sql.jar` and all `.jar` files in the `lib` or `update\downloads\core` directories.
   - The `addpath.bat` script (not shown) is assumed to append each file to the classpath variable.

2. **Log4j Configuration**:
   - Log4j is a logging framework used by SQuirreL SQL. The script specifies separate Log4j configuration files for the update process (`update-log4j.properties`) and the main application (`log4j.properties`).

3. **Software Update Mechanism**:
   - SQuirreL SQL supports automatic updates, managed by the `PreLaunchUpdateApplication` class. The script checks for update files and runs the update process if necessary.

4. **Java Version Compatibility**:
   - The script enforces strict compatibility with Java 1.6 or 1.7, likely due to dependencies or features specific to these versions.

5. **Portability**:
   - The script is designed to be portable by dynamically determining the installation directory and Java executable location.

---

### **Potential Issues and Considerations**
1. **Java Version Restriction**:
   - The script only allows Java 1.6 or 1.7, which are outdated (released in 2006 and 2011, respectively). Modern systems may have newer Java versions, causing the script to fail unless an older JRE is installed.
   - **Workaround**: Users may need to install a compatible JRE or modify the script to support newer versions (if SQuirreL SQL is compatible).

2. **Hardcoded Paths**:
   - The script assumes certain files (e.g., `squirrel-sql.jar`, `versioncheck.jar`, `addpath.bat`) exist in specific directories relative to `SQUIRREL_SQL_HOME`. If these are missing or moved, the script will fail.

3. **Windows-Specific**:
   - The script uses Windows-specific commands (`dir /b`, `FOR /F`, `start /B`) and `javaw.exe`, making it incompatible with non-Windows systems without modification.

4. **Error Handling**:
   - The script handles Java version errors but does not provide detailed error messages for other failures (e.g., missing `squirrel-sql.jar` or invalid classpath).

5. **Memory Limit**:
   - The `-Xmx256m` flag limits the JVM to 256 MB of memory, which may be insufficient for large databases or complex queries, potentially causing `OutOfMemoryError`.

---

### **Summary**
This batch script is a launcher for the SQuirreL SQL Client, performing the following tasks:
- Detects and configures the Java executable.
- Verifies Java version compatibility (1.6 or 1.7).
- Checks for and applies software updates if available.
- Builds the classpath for the application.
- Launches SQuirreL SQL with appropriate parameters, including a splash screen and memory settings.

The script is well-structured for its purpose but is tailored to a specific environment (Windows, Java 1.6/1.7) and may require updates to support modern systems or newer Java versions.

If you have further questions or need assistance modifying the script (e.g., to support newer Java versions), let me know!
