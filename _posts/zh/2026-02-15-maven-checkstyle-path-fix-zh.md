---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Maven Checkstyle 文件路径错误
translated: true
type: note
---

**Question:** 为什么我的 Google Cloud Build 在 Maven checkstyle 阶段报错 "Unable to find configuration file at location: /app/checks.xml: Could not find resource '/app/checks.xml'"？

**Answer:**

构建失败的原因是 `maven-checkstyle-plugin`（版本 3.6.0）被配置为使用位于 `/app/checks.xml` 的 Checkstyle 配置文件，但在构建时，该文件在 Docker container 内部并不存在。

这是在容器化 Maven 构建中非常常见的问题（特别是在 Google Cloud Build、Cloud Run 基于源码的构建或类似的 CI 环境中）。

### 最可能的原因

1. **代码库中缺少 checks.xml 文件**
   你的 `pom.xml` 中可能包含类似以下的代码：

   ```xml
   <plugin>
       <groupId>org.apache.maven.plugins</groupId>
       <artifactId>maven-checkstyle-plugin</artifactId>
       <version>3.6.0</version>
       <configuration>
           <configLocation>/app/checks.xml</configLocation>
           <!-- 或 <configLocation>checks.xml</configLocation> -->
       </configuration>
       <executions>
           <execution>
               <id>checkstyle-check</id>
               <phase>verify</phase>
               <goals>
                   <goal>check</goal>
               </goals>
           </execution>
       </executions>
   </plugin>
   ```

   但是 `checks.xml` 文件（或你使用的任何名称）并未出现在项目的根目录（或路径所预期的位置）。

2. **使用了绝对路径 (/app/checks.xml) 而不是相对路径**
   `/app/checks.xml` 是 container 内部的绝对路径。
   除非你的 Dockerfile 明确将文件复制到 `/app/checks.xml`，否则 Maven 将无法找到它。
   Cloud Build 通常将你的代码库 checkout 到 `/workspace`，而不是 `/app`。

3. **文件在 .gitignore 中或未提交**
   如果 `checks.xml` 仅存在于你的本地机器上，但被忽略或未 push，它在 Cloud Build 中将不可用。

### 推荐的修复方案（选择其一）

#### 方案 1：使用相对路径（最常见且最简洁）

将 `pom.xml` 中的配置更改为**相对路径**：

```xml
<configLocation>checks.xml</configLocation>
<!-- 或者如果它在子文件夹中 -->
<configLocation>config/checkstyle/checks.xml</configLocation>
```

然后确保该文件存在于 Git repository 的对应位置（commit 并 push 它）。

#### 方案 2：保持当前路径但在 Dockerfile 中复制文件

如果你确实需要使用 `/app/checks.xml`，请在 Dockerfile 的 `mvn package` 步骤**之前**添加以下内容：

```dockerfile
COPY checks.xml /app/checks.xml
```

（假设 `checks.xml` 位于代码库的根目录）

#### 方案 3：临时跳过 checkstyle（用于调试/解锁）

在 `cloudbuild.yaml` 或 Dockerfile 的 Maven 命令中添加此 flag：

```yaml
- name: 'gcr.io/cloud-builders/mvn'
  args: ['-B', '--no-transfer-progress', 'package', '-Dcheckstyle.skip=true']
```

或者在 Dockerfile 中：

```dockerfile
RUN mvn -B --no-transfer-progress package -Dcheckstyle.skip=true
```

#### 方案 4：使用标准发布的 ruleset 而非自定义文件

将你的配置替换为知名的 ruleset（无需本地文件）：

```xml
<configLocation>google_checks.xml</configLocation>
<!-- 或 sun_checks.xml，或通过 dependency 引入 -->
```

许多团队使用 Google 的风格：

```xml
<dependency>
    <groupId>com.puppycrawl.tools</groupId>
    <artifactId>checkstyle</artifactId>
    <version>10.18.0</version> <!-- 需匹配你的 plugin 版本范围 -->
</dependency>
...
<configLocation>google_checks.xml</configLocation>
```

### 快速诊断步骤

1. 在 Dockerfile 或 `cloudbuild.yaml` 的 `mvn` 命令之前添加以下命令：

   ```bash
   ls -la /workspace || ls -la .
   find / -name checks.xml 2>/dev/null || true
   ```

2. 重新运行构建并查看 log —— 这将显示文件是否真的存在。

一旦文件出现在 plugin 预期的位置，"Could not find resource" 错误就会消失，构建应该可以继续进行（除非存在实际的代码风格违规）。

**References:**

- [https://maven.apache.org/plugins/maven-checkstyle-plugin/examples/custom-checker.html](https://maven.apache.org/plugins/maven-checkstyle-plugin/examples/custom-checker.html)
- [https://cloud.google.com/build/docs/optimize-builds/speed-up-builds#use_m2_cache](https://cloud.google.com/build/docs/optimize-builds/speed-up-builds#use_m2_cache) (相关的 Cloud Build 上的 Maven 技巧)
- [https://github.com/checkstyle/checkstyle/issues?q=is%3Aissue+configLocation+not+found](https://github.com/checkstyle/checkstyle/issues?q=is%3Aissue+configLocation+not+found) (报告的类似问题)
