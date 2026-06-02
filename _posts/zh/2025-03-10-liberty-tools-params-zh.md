---
audio: false
generated: true
lang: zh
layout: post
title: 在Liberty Tools插件中传递自定义JVM参数
translated: true
type: note
---

您可以通过在 VS Code 的 Liberty 开发模式启动配置中添加自定义 JVM 参数（例如 `-Dversion=5.1`）。通常，您需要编辑（或创建）项目中的 `.vscode/launch.json` 文件，并将参数包含在 `"vmArgs"` 属性下（如果配置需要 Maven 目标参数，则使用 `"args"`）。

例如，如果您使用 Liberty Tools 扩展进行开发模式，配置可能如下所示：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "liberty",
      "request": "launch",
      "name": "Liberty Dev Mode",
      "goal": "dev",
      "vmArgs": "-Dversion=5.1"
    }
  ]
}
```

### 操作步骤：
1. **打开或创建启动配置：**
   - 在 VS Code 中打开您的项目
   - 进入 `.vscode` 文件夹并打开（或创建）`launch.json` 文件

2. **添加开发模式配置：**
   - 按上述示例添加配置条目。关键属性 `"vmArgs"` 允许您指定在开发模式启动时传递给服务器的 JVM 选项

3. **保存并启动：**
   - 保存文件
   - 使用“运行和调试”视图启动 "Liberty Dev Mode" 配置

如果您直接使用 Maven，也可以通过命令行启动开发模式：

```bash
mvn liberty:dev -Dversion=5.1
```

这会在启动服务器时将自定义属性传递给 JVM。

通过这种方式配置，Liberty Tools 扩展将在每次启动开发模式时包含您的自定义参数（`-Dversion=5.1`）。
