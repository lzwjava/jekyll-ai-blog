---
audio: false
generated: true
lang: en
layout: post
title: 'PowerShell: Run Commands in Current Terminal'
translated: false
type: note
---

To run commands like `mvn` or WebSphere server commands directly in the current PowerShell terminal without opening a new command prompt, you can use the call operator (`&`) or directly invoke the command. This approach ensures the command executes within the existing PowerShell session, keeping output and errors in the same terminal.

Here’s how to do it:

1. **Directly Run the Command**:
   If the command (e.g., `mvn`) is in your system’s PATH or accessible in the current directory, simply type the command as you would in a terminal:

   ```powershell
   mvn clean install
   ```

   This runs `mvn` directly in the PowerShell session, and the output stays in the current terminal.

2. **Use the Call Operator (`&`)**:
   If you need to specify the path to the executable or the command is stored in a variable, use the call operator:

   ```powershell
   & "C:\path\to\maven\bin\mvn.cmd" clean install
   ```

   For WebSphere server commands, if you’re running something like `wsadmin` or `startServer`, you can do:

   ```powershell
   & "C:\path\to\WebSphere\AppServer\bin\startServer.bat" server1
   ```

   The `&` operator ensures the command runs in the current PowerShell session.

3. **Handle Commands with Spaces or Variables**:
   If the command path contains spaces or is stored in a variable, use `&` with the path quoted:

   ```powershell
   $mvnPath = "C:\Program Files\Apache Maven\bin\mvn.cmd"
   & $mvnPath clean install
   ```

4. **Set Environment Variables (if needed)**:
   Some commands like `mvn` or WebSphere scripts may require environment variables (e.g., `JAVA_HOME` or `WAS_HOME`). Set them in the script before running the command:

   ```powershell
   $env:JAVA_HOME = "C:\path\to\jdk"
   $env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
   mvn --version
   ```

   For WebSphere:

   ```powershell
   $env:WAS_HOME = "C:\path\to\WebSphere\AppServer"
   & "$env:WAS_HOME\bin\startServer.bat" server1
   ```

5. **Capture Output or Handle Errors**:
   To capture the command’s output or handle errors, use PowerShell’s standard mechanisms:

   ```powershell
   try {
       $output = & mvn clean install 2>&1
       Write-Output $output
   } catch {
       Write-Error "Failed to run Maven: $_"
   }
   ```

6. **Avoid `Start-Process`**:
   Unlike `Start-Process`, which launches a new process (often in a separate window), the above methods keep execution in the current session. Avoid using `Start-Process` like this:

   ```powershell
   # This will open a new command prompt window
   Start-Process -FilePath "mvn" -ArgumentList "clean install"
   ```

   Instead, stick with direct execution or `&`.

### Example Script
Here’s a sample PowerShell script to run `mvn` and a WebSphere command in the current terminal:

```powershell
# Set environment variables if needed
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
$env:WAS_HOME = "C:\IBM\WebSphere\AppServer"

# Run Maven command
Write-Output "Running Maven..."
& mvn clean install

# Run WebSphere server command
Write-Output "Starting WebSphere server..."
& "$env:WAS_HOME\bin\startServer.bat" server1
```

### Notes
- Ensure the command-line tools (`mvn`, `startServer.bat`, etc.) are in your PATH or provide the full path to the executable.
- If the command requires a specific working directory, use `Set-Location` (or `cd`) before running it:

   ```powershell
   Set-Location "C:\path\to\project"
   & mvn clean install
   ```

- For commands that rely on `.bat` or `.cmd` files (common with WebSphere), the `&` operator works well, but ensure the script runs in PowerShell, not `cmd.exe`.
- If you encounter issues with environment variables or PATH, verify them with `Get-ChildItem Env:`.

This approach keeps everything in the current PowerShell terminal, avoiding new windows and maintaining a clean workflow. If you have a specific command or setup causing issues, share more details, and I can tailor the solution further.
