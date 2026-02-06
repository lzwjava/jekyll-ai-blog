---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Azure CLI 全局选项指南
translated: true
type: note
---

Question: 请提供 Azure CLI 命令行选项的全面介绍。

Answer: 

**Azure CLI** (`az`) 是一个用于管理 Azure 资源的跨平台命令行工具。几乎每个命令都支持一组**全局参数**（也称为全局选项），这些参数在几乎所有命令中都是通用的。

当讨论 Azure CLI 使用模式时，这些全局选项是最常用的“命令行选项”。

### 最重要的全局参数 (2026)

这些参数可以附加到几乎任何 `az` 命令之后：

| 参数                  | 缩写 | 常用值 / 描述                                                                 | 典型使用场景                              |
|-----------------------|-------|-----------------------------------------------------------------------------|-----------------------------------------------|
| `--help`              | `-h`  | 显示命令或组的帮助信息                                                           | 学习任何命令：`az vm create -h`          |
| `--output`            | `-o`  | `json` (默认), `jsonc`, `table`, `tsv`, `yaml`, `yamlc`, `none`                    | 人类可读：`--output table`<br>机器处理：`--output json` |
| `--query`             |       | JMESPath 表达式                                                                 | 过滤输出：`--query "[].{name:name, id:id}"` |
| `--subscription`      |       | Subscription 名称或 ID                                                       | 覆盖默认值：`--subscription "Prod Sub"` |
| `--verbose`           |       | 增加日志详细程度                                                               | 在执行期间查看更多详细信息             |
| `--debug`             |       | 显示所有调试日志和底层的 REST API 调用                                              | 故障排除 / 深度调试              |
| `--only-show-errors`  |       | 抑制警告，只显示错误                                                           | 保持 CI/CD 输出整洁                            |

**快速示例**：

```bash
# 人类友好的表格输出
az resource list --output table

# 过滤仅显示名称和位置
az vm list --query "[].{Name:name, Location:location}" --output table

# 在特定的 subscription 中运行命令
az group list --subscription "My-Dev-Sub" -o table

# 调试一个失败的命令
az storage account create ... --debug
```

### 其他常用全局 / 频繁遇到的选项

- `--resource-group` / `-g`  
  非常常见的参数（严格来说不是全局的，但出现在数百个命令中）

- `--name` / `-n`  
  资源名称（非常常见）

- `--ids`  
  接受一个或多个 Azure Resource ID，而不需要提供 `--resource-group --name ...`

- `--yes` / `-y`  
  自动回答确认提示为“是”（非常适合自动化）

- `--no-wait`  
  不等待长时间运行的操作完成（即发即弃）

- `--wait` (部分命令支持)  
  等待操作完成并显示最终状态

### 影响命令行行为的配置

许多行为可以设置一次（而不需要每次重复使用 flag），使用：

```bash
# 交互式向导（推荐初学者使用）
az init

# 或设置具体值
az config set core.output=table
az config set core.default_subscription="My-Sub-Name"
az config set logging.enable_log_file=true
```

影响命令行体验的常见配置键：

- `core.output` → 默认输出格式
- `core.only_show_errors` → 类似永久启用 `--only-show-errors`
- `core.no_color` → 禁用 ANSI 颜色
- `core.collect_telemetry` → 选择不加入遥测
- `core.default_subscription` / `core.default_resource_group` / `core.default_location`

### Positional vs Named Arguments

Azure CLI 使用两种样式：

- **Named**（最常用）：`--resource-group myRg --name myVm`
- **Positional**（较少见，但存在）：一些非常旧的命令或扩展

为了清晰度和脚本的健壮性，始终首选 Named Arguments。

### 最佳实践总结 (2026 风格)

- 交互式操作时使用 `--output table`
- 在脚本 / CI/CD 中使用 `--output json` + `--query`
- 使用资源 ID 编写脚本时首选 `--ids`
- 在流水线中串联使用 `--only-show-errors`
- 使用 `az config` 或 `az init` 来减少重复输入
- 始终通过帮助查看：`az <group> <command> -h`

运行 `az --help` 或任何带 `--help` 的命令时，都会显示全局参数的完整列表。

参考资料：

- [Get started with Azure CLI - Global arguments](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest)
- [Azure CLI global parameters](https://learn.microsoft.com/en-us/cli/azure/azure-cli-global-parameters?view=azure-cli-latest)
- [Azure CLI configuration options](https://learn.microsoft.com/en-us/cli/azure/azure-cli-configuration?view=azure-cli-latest)
- [Azure CLI reference index](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest)