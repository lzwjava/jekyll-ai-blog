---
audio: false
generated: true
lang: zh
layout: post
title: 在Windows中实现代理检查
translated: true
type: note
---

要在 Windows 中使用 Git-Bash 和 PowerShell 实现代理检查，您需要在每个 shell 中设置机制，以检测何时执行与网络相关的命令，并在配置了代理设置时显示它们。以下是针对 Git-Bash 和 PowerShell 的步骤和代码。提到的"终端"很可能是指托管这些 shell 的 Windows 终端，因此我们将重点放在 Git-Bash 和 PowerShell 的实现上。

---

### **对于 Git-Bash**

Git-Bash 是 Windows 上的 Bash 模拟器，我们可以使用 `DEBUG` 陷阱在每次命令执行前运行一个函数。目标是检查命令是否与网络相关，以及是否设置了代理设置，然后显示它们。

#### **步骤：**

1. **定义网络相关命令列表。**
2. **创建一个函数来显示代理设置。**
3. **创建一个函数来检查命令和代理设置。**
4. **设置 `DEBUG` 陷阱，以便在每条命令之前运行检查。**
5. **定义一个手动的 `checkproxy` 函数，用于按需显示代理设置。**
6. **将所有配置添加到 `.bashrc` 文件中。**

#### **实现：**

将以下代码添加到您的 `~/.bashrc` 文件中（如果不存在则创建它）：

```bash
# 网络相关命令列表
network_commands=(
    "gpa"
    "git"
    "ssh"
    "scp"
    "sftp"
    "rsync"
    "curl"
    "wget"
    "apt"
    "yum"
    "dnf"
    "npm"
    "yarn"
    "pip"
    "pip3"
    "gem"
    "cargo"
    "docker"
    "kubectl"
    "ping"
    "traceroute"
    "netstat"
    "ss"
    "ip"
    "ifconfig"
    "dig"
    "nslookup"
    "nmap"
    "telnet"
    "ftp"
    "nc"
    "tcpdump"
    "adb"
    "bundle"
    "brew"
    "cpanm"
    "bundle exec jekyll"
    "make"
    "python"
    "glcoud"
)

# 显示代理设置的函数
display_proxy() {
    echo -e "🚀 **检测到代理设置:**"
    [ -n "$HTTP_PROXY" ] && echo "   - HTTP_PROXY: $HTTP_PROXY"
    [ -n "$http_proxy" ] && echo "   - http_proxy: $http_proxy"
    [ -n "$HTTPS_PROXY" ] && echo "   - HTTPS_PROXY: $HTTPS_PROXY"
    [ -n "$https_proxy" ] && echo "   - https_proxy: $https_proxy"
    [ -n "$ALL_PROXY" ] && echo "   - ALL_PROXY: $ALL_PROXY"
    [ -n "$all_proxy" ] && echo "   - all_proxy: $all_proxy"
    echo ""
}

# 检查命令是否为网络相关以及是否设置了代理的函数
proxy_check() {
    local cmd
    # 提取命令的第一个词
    cmd=$(echo "$BASH_COMMAND" | awk '{print $1}')

    for network_cmd in "${network_commands[@]}"; do
        if [[ "$cmd" == "$network_cmd" ]]; then
            # 检查是否设置了任何代理环境变量
            if [ -n "$HTTP_PROXY" ] || [ -n "$http_proxy" ] || \
               [ -n "$HTTPS_PROXY" ] || [ -n "$https_proxy" ] || \
               [ -n "$ALL_PROXY" ] || [ -n "$all_proxy" ]; then
                display_proxy
            fi
            break
        fi
    done
}

# 设置 DEBUG 陷阱，在每条命令之前运行 proxy_check
trap 'proxy_check' DEBUG

# 手动检查代理设置的函数
checkproxy() {
    echo "HTTP_PROXY: $HTTP_PROXY"
    echo "HTTPS_PROXY: $HTTPS_PROXY"
    echo "Git HTTP 代理:"
    git config --get http.proxy
    echo "Git HTTPS 代理:"
    git config --get https.proxy
}
```

#### **工作原理：**

- `network_commands` 数组列出了与网络相关的命令。
- `display_proxy` 显示所有相关的代理环境变量（如果已设置）。
- `proxy_check` 使用 `BASH_COMMAND`（在 `DEBUG` 陷阱中可用）获取正在执行的命令，提取第一个词，并检查它是否与任何网络命令匹配。如果设置了代理变量，则显示它们。
- `trap 'proxy_check' DEBUG` 行确保 `proxy_check` 在每条命令之前运行。
- `checkproxy` 允许您手动查看代理设置，包括 Git 特定的代理配置。
- 将此添加到 `.bashrc` 后，重新启动 Git-Bash 或运行 `source ~/.bashrc` 以应用更改。

#### **用法：**

- 当您运行网络命令（例如 `git clone`、`curl`）时，如果配置了代理设置，它们将在命令执行前显示。
- 运行 `checkproxy` 以手动查看代理设置。

---

### **对于 PowerShell**

PowerShell 没有与 Bash 的 `DEBUG` 陷阱直接等效的功能，但我们可以使用 `PSReadLine` 模块的 `CommandValidationHandler` 来实现类似的功能。此处理程序在每条命令之前运行，允许我们检查网络命令和代理设置。

#### **步骤：**

1. **定义网络相关命令列表。**
2. **创建一个函数来显示代理设置。**
3. **设置 `CommandValidationHandler` 来检查命令和代理设置。**
4. **定义一个手动的 `checkproxy` 函数，用于按需显示代理设置。**
5. **将所有配置添加到您的 PowerShell 配置文件中。**

#### **实现：**

首先，通过在 PowerShell 中运行 `$PROFILE` 来定位您的 PowerShell 配置文件。如果它不存在，请创建它：

```powershell
New-Item -Type File -Force $PROFILE
```

将以下代码添加到您的 PowerShell 配置文件（例如 `Microsoft.PowerShell_profile.ps1`）：

```powershell
# 网络相关命令列表
$networkCommands = @(
    "gpa",
    "git",
    "ssh",
    "scp",
    "sftp",
    "rsync",
    "curl",
    "wget",
    "apt",
    "yum",
    "dnf",
    "npm",
    "yarn",
    "pip",
    "pip3",
    "gem",
    "cargo",
    "docker",
    "kubectl",
    "ping",
    "traceroute",
    "netstat",
    "ss",
    "ip",
    "ifconfig",
    "dig",
    "nslookup",
    "nmap",
    "telnet",
    "ftp",
    "nc",
    "tcpdump",
    "adb",
    "bundle",
    "brew",
    "cpanm",
    "bundle exec jekyll",
    "make",
    "python",
    "glcoud"
)

# 显示代理设置的函数
function Display-Proxy {
    Write-Host "🚀 **检测到代理设置:**"
    if ($env:HTTP_PROXY) { Write-Host "   - HTTP_PROXY: $env:HTTP_PROXY" }
    if ($env:http_proxy) { Write-Host "   - http_proxy: $env:http_proxy" }
    if ($env:HTTPS_PROXY) { Write-Host "   - HTTPS_PROXY: $env:HTTPS_PROXY" }
    if ($env:https_proxy) { Write-Host "   - https_proxy: $env:https_proxy" }
    if ($env:ALL_PROXY) { Write-Host "   - ALL_PROXY: $env:ALL_PROXY" }
    if ($env:all_proxy) { Write-Host "   - all_proxy: $env:all_proxy" }
    Write-Host ""
}

# 设置 CommandValidationHandler 在执行前检查命令
Set-PSReadLineOption -CommandValidationHandler {
    param($command)
    # 提取命令的第一个词
    $cmd = ($command -split ' ')[0]

    if ($networkCommands -contains $cmd) {
        # 检查是否设置了任何代理环境变量
        if ($env:HTTP_PROXY -or $env:http_proxy -or $env:HTTPS_PROXY -or $env:https_proxy -or $env:ALL_PROXY -or $env:all_proxy) {
            Display-Proxy
        }
    }
    # 始终返回 true 以允许命令执行
    return $true
}

# 手动检查代理设置的函数
function checkproxy {
    Write-Host "HTTP_PROXY: $env:HTTP_PROXY"
    Write-Host "HTTPS_PROXY: $env:HTTPS_PROXY"
    Write-Host "Git HTTP 代理:"
    git config --get http.proxy
    Write-Host "Git HTTPS 代理:"
    git config --get https.proxy
}
```

#### **工作原理：**

- `$networkCommands` 是一个包含网络相关命令的数组。
- `Display-Proxy` 显示所有相关的代理环境变量（如果已设置）。
- `Set-PSReadLineOption -CommandValidationHandler` 定义了一个脚本块，在每条命令之前运行：
  - 它提取命令的第一个词。
  - 检查它是否在 `$networkCommands` 中。
  - 如果设置了代理变量，则调用 `Display-Proxy`。
  - 返回 `$true` 以确保命令执行。
- `checkproxy` 允许手动查看代理设置，包括 Git 特定的代理。
- 添加到配置文件后，重新启动 PowerShell 或运行 `. $PROFILE` 以应用更改。

#### **要求：**

- 需要 `PSReadLine` 模块，该模块默认包含在 PowerShell 5.1 及更高版本中。
- 如果使用旧版本，您可能需要升级 PowerShell 或寻找替代方法（此处不涉及，因为大多数系统使用较新版本）。

#### **用法：**

- 当您运行网络命令（例如 `git pull`、`curl`）时，如果配置了代理设置，它们将在命令执行前显示。
- 运行 `checkproxy` 以手动查看代理设置。

---

### **关于"终端"的说明**

- 如果"终端"指的是 Windows 终端，它只是 Git-Bash、PowerShell 或命令提示符 (cmd.exe) 等 shell 的宿主。
- 上述实现在 Windows 终端内的 Git-Bash 或 PowerShell 会话中工作。
- 在命令提示符 (cmd.exe) 中实现类似功能是不切实际的，因为其脚本功能有限。建议改用 Git-Bash 或 PowerShell。

---

### **其他注意事项**

- **命令解析：**
  - 两种实现都只检查命令的第一个词是否在网络的命令列表中。例如，`git clone` 会触发，因为 `git` 在列表中。
  - 像 `bundle exec jekyll` 这样的多词命令，如果 `bundle` 在列表中，则会触发，这在大多数情况下已经足够。
  - 如果需要，您可以修改代码以检查命令中的所有词，但这可能导致误报，并且通常没有必要。

- **代理变量：**
  - 两种实现都检查 `HTTP_PROXY`、`http_proxy`、`HTTPS_PROXY`、`https_proxy`、`ALL_PROXY` 和 `all_proxy`，以涵盖常见的变体。
  - 在 Windows 中，环境变量不区分大小写，但为了与类 Unix 行为（尤其是在 Git-Bash 中）保持一致，我们检查了两种大小写形式。

- **Git 代理设置：**
  - 两个 shell 中的 `checkproxy` 函数都使用 `git config --get` 显示 Git 特定的代理设置。

---

### **测试**

- **设置代理变量：**
  - 在 Git-Bash 中：`export HTTP_PROXY=http://proxy.example.com:8080`
  - 在 PowerShell 中：`$env:HTTP_PROXY = "http://proxy.example.com:8080"`
- **运行网络命令：**
  - 尝试诸如 `git --version`、`curl -V` 等命令。
  - 代理设置应在命令输出之前显示。
- **使用 `checkproxy`：**
  - 在任一 shell 中运行 `checkproxy` 以手动查看代理设置。

---

此实现在 Git-Bash 和 PowerShell 中都提供了强大的代理检查功能，适用于在 Windows 终端内或独立使用。
