---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Control M环境变量设置方法
translated: true
type: note
---

在BMC Control-M（包括Control-M/Enterprise Manager和Control-M Automation API/Agent）中，有几种常见且推荐的方法可将环境变量传递或提供给作业。以下是最常用的方法（按推荐程度从高到低排列）：

### 1. **使用Control-M作业定义中的「环境变量」功能**（推荐 - Control-M 9.0.20+版本）
在Control-M Web界面（或Automation API JSON）中，可直接定义在作业执行前设置到作业进程环境中的变量。

**Control-M Web界面操作：**
- 打开作业属性
- 进入**Execution**标签页 → **Environment Variables**
- 添加名称/值对（例如 MY_VAR = my_value）

**Automation API（JSON）示例：**
```json
{
  "MyJob": {
    "Type": "Job:OS",
    "Command": "echo $MY_VAR",
    "Environment Variables": [
      {"MY_VAR": "HelloFromControlM"},
      {"ANOTHER_VAR": "12345"}
    ]
  }
}
```
这些变量会在Windows和Unix/Linux代理上自动导出到作业环境中。

### 2. **使用 %%PARM语法（AutoEdit变量）** – 传统环境中极为常见
在文件夹或作业级别定义变量，这些变量在排序/运行时进行解析。

**作业定义示例（cmm或JSON）：**
```text
%%MY_VAR = some_value
```
或动态设置：
```text
%%MY_VAR = %%$DATE
```
在脚本/命令中通过代理原生语法引用：
- Unix/Linux：`$MY_VAR` 或 `${MY_VAR}`
- Windows：`%MY_VAR%`
还可通过告警、循环作业或Automation API设置这些变量。

### 3. **在脚本/命令行中显式设置**
```text
# Unix示例
export MY_VAR=value && /path/to/script.sh

:: Windows示例
set MY_VAR=value && script.bat
```

### 4. **使用Control-M代理的「agentenv」或配置文件脚本**（对该代理上所有作业全局生效）
非作业专用方法，但有时会使用：
- Unix：编辑Control-M源化的`$HOME/.bashrc`或`$HOME/.profile`
- 或使用Control-M代理工具`agt_profile`添加永久环境设置

### 5. **通过「参数」传递（本地或SMART文件夹参数）并转换为环境变量**
定义文件夹参数后以%%PARAM_NAME形式引用，然后在作业中执行：
```text
export MY_VAR=%%MY_PARAM
```

### 6. **使用Control-M Automation API的「deploy」或「run」时传递变量**
通过API触发作业时，可在运行时传递变量：
```json
"variables": [
  {"MY_VAR": "runtime_value"},
  {"DEBUG": "true"}
]
```
这些变量在作业中作为%%MY_VAR可用，若使用现代「环境变量」功能则会自动导出为环境变量。

### 最佳实践总结（2024–2025）
- Control-M 9.0.21+版本：使用作业定义中的原生**环境变量**功能（GUI或JSON）。此方式清晰直观，在Windows和Unix系统上表现一致。
- 旧版本或传统定义：使用%%AutoEdit变量结合脚本中的export/set命令。

通过这种方式，所有配置都可在Control-M内部可见，无需依赖外部配置文件或封装脚本。
