---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: PowerShell 脚本的点源导入
translated: true
type: note
---

### 在 .ps1 文件中使用点源加载 PowerShell 函数

点源加载（使用 `.` 操作符）可将 PowerShell 脚本（.ps1 文件）载入当前会话内存，使其函数和变量无需执行脚本顶层代码即可直接使用。该功能适用于导入模块或可复用代码。

#### 基础语法

在 PowerShell 会话中运行以下命令：

```
. 路径\你的脚本.ps1
```

- 将 `路径\你的脚本.ps1` 替换为实际文件路径（建议使用绝对路径确保可靠性）
- 示例：`. C:\脚本\我的函数.ps1` —— 这将把该文件中的函数加载到当前会话

#### 运行机制

- 脚本中定义的函数可在当前会话中直接调用
- 变量也会被导入（除非被限定为局部作用域）
- 生产环境中建议避免使用点源加载，改用模块以获得更好组织性
- 提示：若路径包含空格，需用引号包裹：`. "C:\我的脚本\函数集.ps1"`

常见问题：若脚本存在语法错误，点源加载会报错失败。可通过命令提示符运行 `PowerShell -Command ". .\你的脚本.ps1"` 进行测试。

### 配置 PowerShell 执行策略

执行策略是用于限制 PowerShell 脚本运行的安全设置，可防止恶意代码执行。该策略支持作用域分级（如计算机全局、用户特定）。

#### 查看当前策略

在 PowerShell 中运行：

```
Get-ExecutionPolicy
```

- 输出示例：`Restricted`（禁止所有脚本）、`AllSigned`（仅允许签名脚本）、`RemoteSigned`（远程脚本需签名，本地脚本直接允许）或 `Unrestricted`

#### 设置或修改策略

使用 `Set-ExecutionPolicy`（计算机级修改需要管理员权限）：

- 允许本地编写脚本的示例：`Set-ExecutionPolicy RemoteSigned`
- 强制应用不提示：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force`
- 作用域限定：`Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser`（仅影响当前用户）

#### 常用策略说明

- `Restricted`：默认策略，禁止运行任何脚本
- `AllSigned`：要求数字签名（安全但不便）
- `RemoteSigned`：平衡安全性与便利性——允许本地脚本，远程脚本需签名
- `Unrestricted`：运行所有脚本（存在风险，需谨慎使用）
- `Bypass`：完全无限制，适用于自动化场景

提示：策略仅作用于控制台会话，除非单独设置，否则不影响 ISE 或 VS Code。可通过运行 `Write-Host "Hello"` 等示例脚本测试策略变更。更多信息请参阅微软文档：`help about_Execution_Policies`。企业环境中组策略可能会覆盖本地设置。
