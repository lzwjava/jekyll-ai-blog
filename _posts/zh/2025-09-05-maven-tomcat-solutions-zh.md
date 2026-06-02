---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Maven Tomcat插件问题解决方案
translated: true
type: note
---

你在自己的日志中已经找到了关键线索：

> `[INFO] Skipping non-war project`

没有任何启动过程，因为 **tomcat7-maven-plugin 只运行打包为 WAR 的 webapp**（采用经典的 `src/main/webapp` 目录结构）。你的项目目前几乎肯定是打包为 JAR 格式，所以该插件在构建完成后就直接退出了。

还有第二个陷阱：你正在运行 **Tomcat 11**（使用 Jakarta `jakarta.*` API），但你的依赖是 **Spring 5.2.x**（使用 `javax.*`）。这种不匹配意味着即使 Tomcat 启动了，直接部署到 Tomcat 11 也会在没有迁移的情况下失败。对于 Spring 5 请使用 Tomcat 9（javax），或者将应用升级到 Spring 6/Jakarta 以适配 Tomcat 10/11。

以下是几条清晰的路径供你选择——选择其中一条即可正常工作：

### 路径 1 — 保持 Spring 5，使用 Jetty 插件本地运行（最快）

无需 WAR 打包；适合快速开发。

1. 添加插件：

   ```xml
   <plugin>
     <groupId>org.eclipse.jetty</groupId>
     <artifactId>jetty-maven-plugin</artifactId>
     <version>9.4.54.v20240208</version>
   </plugin>
   ```
2. 运行：

   ```bash
   mvn jetty:run -Djetty.port=8080
   ```

这种方式使用 `javax.*`，与 Spring 5 匹配。

### 路径 2 — 保持 Spring 5，构建 WAR 并使用 Tomcat7 插件

1. 在 `pom.xml` 中设置 WAR 打包：

   ```xml
   <packaging>war</packaging>
   ```
2. 确保 webapp 目录结构存在：

   ```
   src/main/webapp/
   src/main/webapp/WEB-INF/web.xml   # 可选（如果你有 Servlet 3 初始化器）
   ```
3. （可选）添加插件配置：

   ```xml
   <plugin>
     <groupId>org.apache.tomcat.maven</groupId>
     <artifactId>tomcat7-maven-plugin</artifactId>
     <version>2.2</version>
     <configuration>
       <path>/</path>
       <port>8080</port>
     </configuration>
   </plugin>
   ```
4. 运行：

   ```bash
   mvn tomcat7:run            # 用于展开式 webapp
   # 或者
   mvn package && mvn tomcat7:run-war
   ```

### 路径 3 — 保持 Spring 5，部署到独立的 Tomcat 9

这种方式无需修改代码即可匹配 `javax.*`。

```bash
brew install tomcat@9
/opt/homebrew/opt/tomcat@9/bin/catalina start
```

构建并将你的 WAR 文件放入 `.../tomcat@9/libexec/webapps/`。

### 路径 4 — 将应用升级到 Spring 6/Jakarta，继续使用 Tomcat 11

如果你希望使用现代版本的 Tomcat：

* 升级到 Spring Framework 6.x / Spring Boot 3.x。
* 将导入语句从 `javax.*` 改为 `jakarta.*`。
* 然后 Tomcat 10/11 就可以正常工作了。

---

#### 为什么 `mvn tomcat7:run` 显示成功但“没有任何反应”

* Maven 阶段成功完成，但插件检测到**非 WAR 打包**，因此它**没有启动**嵌入式 Tomcat。这正是 “Skipping non-war project” 的含义。

---

如果你告诉我你倾向于哪条路径，我可以为你提供确切的 `pom.xml` 和该设置所需的最简文件（包括一个简单的控制器以及如何通过 `http://localhost:8080/hello` 访问它）。
