---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu系统上安装YourKit Java性能分析工具
translated: true
type: note
---

在 Ubuntu 系统上安装 YourKit Java Profiler，请根据 YourKit 官网提供的指引按以下步骤操作：

1. **下载分析器**：
   - 访问 YourKit Java Profiler 下载页面：[https://www.yourkit.com/java/profiler/download/](https://www.yourkit.com/java/profiler/download/)
   - 选择支持 Java 8 至 Java 24 的 YourKit Java Profiler 2025.3 Linux 版本，该版本兼容包括 Ubuntu 在内的 Linux 系统，支持 arm32、arm64、ppc64le、x64 和 x86 架构。请确保系统满足[系统要求](https://www.yourkit.com/docs/java/system-requirements/)以保障兼容性

2. **下载压缩包**：
   - 下载适用于 Linux 的 `.zip` 压缩包（例如 `YourKit-JavaProfiler-2025.3-<构建版本>.zip`）。下载链接可在 YourKit 下载页面获取

3. **解压压缩包**：
   - 打开终端并进入下载文件所在目录（如 `~/Downloads`）
   - 使用以下命令解压：
     ```bash
     unzip YourKit-JavaProfiler-2025.3-<构建版本>.zip -d /opt/yourkit
     ```
     请将 `<构建版本>` 替换为实际下载文件的构建编号。此命令会将分析器解压至 `/opt/yourkit` 目录，也可选择其他目标目录

4. **运行分析器**：
   - 进入解压目录：
     ```bash
     cd /opt/yourkit
     ```
   - 运行启动脚本：
     ```bash
     ./bin/profiler.sh
     ```
     此时将启动 YourKit Java Profiler 图形界面

5. **可选：通过许可证密钥实现无人值守安装**：
   - 若已获取许可证密钥，可通过命令行参数自动接受最终用户许可协议并激活许可证：
     ```bash
     ./bin/profiler.sh -accept-eula -license-key=<许可证密钥>
     ```
     将 `<许可证密钥>` 替换为实际密钥。此方式适用于自动化部署场景

6. **集成开发环境（可选）**：
   - 若使用 Eclipse、IntelliJ IDEA 或 NetBeans 等 IDE，YourKit 提供专用插件：
     - Eclipse 用户可通过 **帮助 > 安装新软件**，添加插件仓库地址：`https://www.yourkit.com/download/yjp2025_3_for_eclipse/`
     - 选择 YourKit Java Profiler 插件并按指引完成安装，必要时重启 Eclipse
     - 也可使用离线安装包：`<分析器安装目录>/lib/eclipse-plugin/yjp2025_3_for_eclipse.zip`
   - 安装完成后，Eclipse 工具栏、主菜单及上下文菜单中将出现"Profile"操作项

7. **验证安装**：
   - 启动分析器后，欢迎界面可监控本地 Java 应用、连接远程应用或打开现有快照。可通过演示程序体验分析器功能

8. **补充说明**：
   - 若运行异常，请确保系统已安装 Java 8 或更高版本（可通过 `java -version` 验证），YourKit 需兼容的 JVM 环境
   - 远程分析时需确保已配置 SSH 访问权限
   - YourKit 提供 15 天免费试用期，初期无需许可证。非商业开源项目可联系销售获取免费许可
   - 若因安装路径含空格导致启动失败，请将解压目录移至无空格路径（如 `/opt/yourkit`）

如需进一步协助，请参阅 [YourKit 官方文档](https://www.yourkit.com/docs/java/)或通过[支持页面](https://www.yourkit.com/support/)联系技术团队。

若具体步骤遇到问题，可随时获取帮助！
