---
audio: false
generated: true
lang: zh
layout: post
title: PowerShell：在当前终端中运行命令
translated: true
type: note
---

要在当前 PowerShell 终端中直接运行 `mvn` 或 WebSphere 服务器命令（无需打开新的命令提示符窗口），您可以使用调用运算符 (`&`) 或直接执行命令。这种方法能确保命令在现有的 PowerShell 会话中执行，使输出和错误信息都保留在同一终端中。

具体操作如下：

1. **直接运行命令**：
   如果命令（如 `mvn`）位于系统 PATH 环境变量或当前目录可访问路径中，只需像在终端中一样输入命令：

   ```powershell
   mvn clean install
   ```

   这将在当前 PowerShell 会话中直接运行 `mvn`，输出内容会保留在当前终端。

2. **使用调用运算符 (`&`)**：
   如果需要指定可执行文件路径，或命令存储在变量中，请使用调用运算符：

   ```powershell
   & "C:\maven\bin\mvn.cmd" clean install
   ```

   对于 WebSphere 服务器命令（如 `wsadmin` 或 `startServer`）：

   ```powershell
   & "C:\WebSphere\AppServer\bin\startServer.bat" server1
   ```

   `&` 运算符能确保命令在当前 PowerShell 会话中运行。

3. **处理含空格或变量的命令**：
   当命令路径包含空格或存储在变量中时，结合引号使用 `&`：

   ```powershell
   $mvnPath = "C:\Program Files\Apache Maven\bin\mvn.cmd"
   & $mvnPath clean install
   ```

4. **设置环境变量（如需要）**：
   某些命令（如 `mvn` 或 WebSphere 脚本）可能需要环境变量（例如 `JAVA_HOME` 或 `WAS_HOME`）。在运行命令前于脚本中设置：

   ```powershell
   $env:JAVA_HOME = "C:\jdk"
   $env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
   mvn --version
   ```

   对于 WebSphere：

   ```powershell
   $env:WAS_HOME = "C:\WebSphere\AppServer"
   & "$env:WAS_HOME\bin\startServer.bat" server1
   ```

5. **捕获输出或处理错误**：
   使用 PowerShell 的标准机制捕获命令输出或处理错误：

   ```powershell
   try {
       $output = & mvn clean install 2>&1
       Write-Output $output
   } catch {
       Write-Error "Maven 执行失败: $_"
   }
   ```

6. **避免使用 `Start-Process`**：
   `Start-Process` 会启动新进程（通常在新窗口中运行），而上述方法能保持执行在当前会话中。请避免如下用法：

   ```powershell
   # 此命令会打开新的命令提示符窗口
   Start-Process -FilePath "mvn" -ArgumentList "clean install"
   ```

   应坚持使用直接执行或 `&` 运算符。

### 示例脚本
以下是在当前终端中运行 `mvn` 和 WebSphere 命令的 PowerShell 示例脚本：

```powershell
# 按需设置环境变量
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
$env:WAS_HOME = "C:\IBM\WebSphere\AppServer"

# 运行 Maven 命令
Write-Output "正在运行 Maven..."
& mvn clean install

# 运行 WebSphere 服务器命令
Write-Output "正在启动 WebSphere 服务器..."
& "$env:WAS_HOME\bin\startServer.bat" server1
```

### 注意事项
- 确保命令行工具（`mvn`、`startServer.bat` 等）位于 PATH 中，或提供可执行文件的完整路径
- 若命令需要特定工作目录，请先使用 `Set-Location`（或 `cd`）切换目录：

   ```powershell
   Set-Location "C:\project"
   & mvn clean install
   ```

- 对于依赖 `.bat` 或 `.cmd` 文件的命令（常见于 WebSphere），`&` 运算符能良好兼容，但需确保脚本在 PowerShell 中而非 `cmd.exe` 中运行
- 若遇到环境变量或 PATH 相关问题，可用 `Get-ChildItem Env:` 进行验证

这种方法能将所有操作保留在当前 PowerShell 终端中，避免新窗口弹窗，保持工作流整洁。如果您遇到特定命令或配置问题，请提供更多细节，我将为您定制解决方案。
