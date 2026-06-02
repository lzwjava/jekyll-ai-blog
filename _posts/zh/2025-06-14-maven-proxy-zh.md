---
audio: false
generated: true
lang: zh
layout: post
title: Maven代理设置
translated: true
type: note
---

根据 `checkproxy` 命令的输出结果，您的 HTTP 和 HTTPS 代理均设置为 `http://127.0.0.1:7890`。以下是更新后的 Maven `settings.xml` 配置片段，用于配置 Maven 使用这些代理设置。

### 更新后的 `settings.xml` 代理配置片段

在 Maven `settings.xml` 文件（位于 `~/.m2/settings.xml` 或 `/usr/share/maven/conf/settings.xml`）中添加或更新 `<proxies>` 部分，内容如下：

```xml
<settings>
  <proxies>
    <proxy>
      <id>http-proxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>127.0.0.1</host>
      <port>7890</port>
      <nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>
    </proxy>
    <proxy>
      <id>https-proxy</id>
      <active>true</active>
      <protocol>https</protocol>
      <host>127.0.0.1</host>
      <port>7890</port>
      <nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>
    </proxy>
  </proxies>
</settings>
```

### 配置片段说明

- **`<id>`**：每个代理配置的唯一标识符（`http-proxy` 和 `https-proxy`）
- **`<active>true</active>`**：启用代理
- **`<protocol>`**：HTTP 代理设置为 `http`，HTTPS 代理设置为 `https`，与 `checkproxy` 输出匹配
- **`<host>127.0.0.1</host>`**：代理服务器 IP 地址，与代理设置一致
- **`<port>7890</port>`**：两个代理的端口号，如设定所示
- **`<nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>`**：排除 `localhost` 和 `127.0.0.1` 不走代理，这是避免本地服务问题的标准做法
- **无 `<username>` 或 `<password>`**：由于代理输出未显示需要认证，故省略这些字段。如需认证，请添加凭据信息

### 应用步骤

1. **打开 `settings.xml`**：
   - 若存在 `~/.m2/settings.xml`，直接编辑（如 `nano ~/.m2/settings.xml`）
   - 若不存在，可创建该文件或编辑全局文件 `/usr/share/maven/conf/settings.xml`（需要 `sudo` 权限）

2. **插入或更新 `<proxies>` 部分**：
   - 若已存在 `<proxies>` 部分，替换或合并其中的 `<proxy>` 条目
   - 若 `<settings>` 内容为空或较少，可将整个片段作为文件内容

3. **保存并关闭**文件

### 验证配置

运行需要网络访问的 Maven 命令来确认代理生效：

```bash
cd ~/Projects/blog-server
mvn -X clean checkstyle:check
```

在调试输出（`-X`）中查找表明 Maven 正在使用代理的日志行（如连接到 `127.0.0.1:7890`）。如果命令能正常下载依赖或完成且无网络错误，则代理配置成功。

### 故障排除

- **代理未生效**：
  - 确保 `127.0.0.1:7890` 的代理服务正在运行（可用 `curl -x http://127.0.0.1:7890 https://repo.maven.apache.org` 测试）
  - 检查 `settings.xml` 文件是否存在拼写错误
- **配置文件被忽略**：
  - 通过调试输出确认 Maven 是否读取了 `~/.m2/settings.xml`
  - 若使用全局文件，请确认正确编辑了 `/usr/share/maven/conf/settings.xml`
- **需要认证**：
  - 若代理需要用户名和密码，请在每个 `<proxy>` 块中添加：

    ```xml
    <username>用户名</username>
    <password>密码</password>
    ```

### 关于先前问题的说明

您在 `blog-server` 项目中遇到的 `checkstyle:check` 问题（涉及 `checks.xml` 和 `SuppressWithNearbyTextFilter`）应通过单独更新 `pom.xml` 来解决（如先前建议：使用 `maven-checkstyle-plugin:3.3.1` 配合 Checkstyle `10.17.0` 和 `<configLocation>${project.basedir}/checks.xml</configLocation>`）。上述代理设置将确保 Maven 能够下载该修复所需的所有构件。

如遇问题或需要有关更新 `pom.xml` 及代理调试的进一步帮助，请随时告知！
