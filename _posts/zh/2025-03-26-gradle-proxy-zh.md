---
audio: false
generated: true
lang: zh
layout: post
title: 在VSCode中配置Gradle代理
translated: true
type: note
---

为在 Visual Studio Code (VSCode) 中配置 Gradle 代理，使其能够通过代理下载依赖项，您需要在 Gradle 配置中设置代理参数。Gradle 使用属性文件管理此类设置，而 VSCode 的 Gradle 项目依赖于 Gradle 构建系统。具体操作如下：

### 配置 Gradle 代理的步骤

1. **定位或创建 Gradle 属性文件**
   - Gradle 使用名为 `gradle.properties` 的文件存储全局配置
   - 该文件通常位于 Gradle 用户主目录：
     - Windows：`C:\Users\<用户名>\.gradle\gradle.properties`
     - macOS/Linux：`~/.gradle/gradle.properties`
   - 若文件不存在，请在上述路径创建

2. **添加代理设置至 `gradle.properties`**
   - 用文本编辑器打开 `gradle.properties` 文件
   - 添加以下内容（将占位符替换为实际代理参数）：

     ```
     systemProp.http.proxyHost=<代理主机>
     systemProp.http.proxyPort=<代理端口>
     systemProp.http.proxyUser=<用户名>
     systemProp.http.proxyPassword=<密码>
     systemProp.https.proxyHost=<代理主机>
     systemProp.https.proxyPort=<代理端口>
     systemProp.https.proxyUser=<用户名>
     systemProp.https.proxyPassword=<密码>
     ```

   - 实际参数示例：

     ```
     systemProp.http.proxyHost=proxy.example.com
     systemProp.http.proxyPort=8080
     systemProp.http.proxyUser=myuser
     systemProp.http.proxyPassword=mypassword
     systemProp.https.proxyHost=proxy.example.com
     systemProp.https.proxyPort=8080
     systemProp.https.proxyUser=myuser
     systemProp.https.proxyPassword=mypassword
     ```

   - 若代理无需认证，可省略 `proxyUser` 和 `proxyPassword` 行

3. **可选：按项目配置代理**
   - 若需代理设置仅对特定项目生效（而非全局），可在项目根目录创建 `gradle.properties` 文件（例如 `<项目根目录>/gradle.properties`），内容与全局配置相同

4. **验证 Gradle 代理状态**
   - 在 VSCode 中打开 Gradle 项目
   - 通过 VSCode 终端或 Gradle 扩展运行构建任务（如 `gradle build`）
   - 此时 Gradle 应通过指定代理下载依赖项（如来自官方站点的组件）

5. **VSCode 特别说明**
   - 请确保已安装 **Java Extension Pack** 和 **Gradle for Java** 扩展以增强 Gradle 项目支持
   - 若问题仍存，请检查 Java 运行时（Gradle 使用）是否遵循代理设置。可能需要设置 JVM 代理参数：
     - 在 VSCode 中进入 `文件 > 首选项 > 设置`
     - 搜索 `java.gradle.build.jvmArguments`
     - 添加如下参数：

       ```
       -Dhttp.proxyHost=<代理主机> -Dhttp.proxyPort=<代理端口> -Dhttps.proxyHost=<代理主机> -Dhttps.proxyPort=<代理端口>
       ```

6. **测试配置**
   - 在 VSCode 中重新加载项目（如关闭后重新打开，或点击 Gradle 侧边栏的“刷新”按钮）
   - 运行 Gradle 任务（如 `gradle build` 或 `gradle dependencies`）确认文件通过代理下载

### 故障排除

- **核对代理信息**：确保代理主机、端口及认证信息准确
- **网络环境检查**：若仍失败，可能是代理或网络屏蔽了特定 Gradle URL（如 `https://services.gradle.org`）。可通过 `curl` 命令测试，或联系网络管理员
- **查看详细日志**：在 VSCode 终端中运行 `gradle build --debug` 或 `gradle build --info` 查看网络请求详情

完成以上配置后，VSCode 中的 Gradle 即可通过代理成功下载依赖项。若遇到问题欢迎随时反馈！
