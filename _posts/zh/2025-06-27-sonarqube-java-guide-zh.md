---
audio: false
generated: true
lang: zh
layout: post
title: 精通SonarQube在Java与Spring项目中的应用
translated: true
type: note
---

# SonarQube 与 Java 和 Spring 项目使用全面指南

## 简介
SonarQube 是一个用于持续检查代码质量的开源平台。它通过静态代码分析来检测错误、代码异味、安全漏洞，并计算代码覆盖率。本指南全面介绍了如何在 Java Spring 项目中设置和使用 SonarQube，包括安装、配置、集成和最佳实践。

## 目录
1. [什么是 SonarQube？](#什么是-sonarqube)
2. [前置条件](#前置条件)
3. [安装 SonarQube](#安装-sonarqube)
4. [设置 Java Spring 项目](#设置-java-spring-项目)
5. [为项目配置 SonarQube](#为项目配置-sonarqube)
6. [运行 SonarQube 分析](#运行-sonarqube-分析)
7. [解读 SonarQube 结果](#解读-sonarqube-结果)
8. [最佳实践](#最佳实践)
9. [常见问题排查](#常见问题排查)
10. [结论](#结论)

## 什么是 SonarQube？
SonarQube 是一个通过分析源代码提供持续代码质量检查的工具，主要检测：
- **错误**：代码中的潜在错误
- **代码异味**：可能导致技术债务的可维护性问题
- **安全漏洞**：可能被利用的安全问题
- **代码覆盖率**：单元测试覆盖的代码百分比
- **重复代码**：可被重构的重复代码块

它支持多种语言，包括 Java，并能与 Maven、Gradle 等构建工具以及 CI/CD 流水线无缝集成。

## 前置条件
在设置 SonarQube 之前，请确保具备：
- **Java 开发工具包 (JDK)**：11 或更高版本（SonarQube 需要 Java 11 或 17）
- **Maven 或 Gradle**：Java Spring 项目的构建工具
- **SonarQube 服务器**：9.9 LTS 或更高版本（社区版足以满足大多数使用场景）
- **SonarScanner**：用于运行分析的 CLI 工具
- **数据库**：SonarQube 需要数据库（如 PostgreSQL、MySQL 或用于测试的嵌入式 H2）
- **Spring 项目**：可正常工作的 Spring Boot 或 Spring Framework 项目
- **IDE**：用于开发的 IntelliJ IDEA、Eclipse 或 VS Code

## 安装 SonarQube

### 步骤 1：下载并安装 SonarQube
1. **下载 SonarQube**：
   - 访问 [SonarQube 下载页面](https://www.sonarqube.org/downloads/)
   - 根据需求选择社区版（免费）或其他版本
   - 下载 ZIP 文件（例如 `sonarqube-9.9.0.zip`）

2. **解压 ZIP**：
   - 将下载的文件解压到目录，如 `/opt/sonarqube` 或 `C:\sonarqube`

3. **配置数据库**：
   - SonarQube 需要数据库。生产环境建议使用 PostgreSQL 或 MySQL，测试环境使用嵌入式 H2 数据库即可
   - PostgreSQL 配置示例：
     - 安装 PostgreSQL 并创建数据库（如 `sonarqube`）
     - 更新 SonarQube 配置文件（`conf/sonar.properties`）：
       ```properties
       sonar.jdbc.url=jdbc:postgresql://localhost:5432/sonarqube
       sonar.jdbc.username=sonarqube_user
       sonar.jdbc.password=sonarqube_pass
       ```

4. **启动 SonarQube**：
   - 进入 SonarQube 目录（`bin/<平台>`）
   - 运行启动脚本：
     - Linux/Mac：`./sonar.sh start`
     - Windows：`StartSonar.bat`
   - 通过 `http://localhost:9000`（默认端口）访问 SonarQube

5. **登录**：
   - 默认凭证：`admin/admin`
   - 首次登录后修改密码

### 步骤 2：安装 SonarScanner
1. **下载 SonarScanner**：
   - 从 [SonarQube Scanner 页面](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner/)下载
   - 解压到目录，如 `/opt/sonar-scanner`

2. **配置环境变量**：
   - 将 SonarScanner 添加到 PATH：
     - Linux/Mac：`export PATH=$PATH:/opt/sonar-scanner/bin`
     - Windows：将 `C:\sonar-scanner\bin` 添加到系统 PATH

3. **验证安装**：
   - 运行 `sonar-scanner --version` 确认安装

## 设置 Java Spring 项目
本指南使用基于 Maven 的 Spring Boot 项目。Gradle 或非 Boot Spring 项目的步骤类似。

1. **创建 Spring Boot 项目**：
   - 使用 [Spring Initializer](https://start.spring.io/) 创建包含以下配置的项目：
     - 依赖项：Spring Web、Spring Data JPA、H2 Database、Spring Boot Starter Test
     - 构建工具：Maven
   - 下载并解压项目

2. **添加单元测试**：
   - 确保项目包含用于测量代码覆盖率的单元测试
   - 测试类示例：
     ```java
     import org.junit.jupiter.api.Test;
     import org.springframework.boot.test.context.SpringBootTest;

     @SpringBootTest
     public class ApplicationTests {
         @Test
         void contextLoads() {
         }
     }
     ```

3. **添加 JaCoCo 以获取代码覆盖率**：
   - 在 `pom.xml` 中添加 JaCoCo Maven 插件以生成代码覆盖率报告：
     ```xml
     <plugin>
         <groupId>org.jacoco</groupId>
         <artifactId>jacoco-maven-plugin</artifactId>
         <version>0.8.8</version>
         <executions>
             <execution>
                 <goals>
                     <goal>prepare-agent</goal>
                 </goals>
             </execution>
             <execution>
                 <id>report</id>
                 <phase>test</phase>
                 <goals>
                     <goal>report</goal>
                 </goals>
             </execution>
         </executions>
     </plugin>
     ```

## 为项目配置 SonarQube

1. **创建 SonarQube 项目**：
   - 登录 SonarQube（`http://localhost:9000`）
   - 点击 **Create Project** > **Manually**
   - 提供 **Project Key**（如 `my-spring-project`）和 **Display Name**
   - 生成用于身份验证的令牌（如 `my-token`）

2. **配置 `sonar-project.properties`**：
   - 在 Spring 项目根目录创建 `sonar-project.properties` 文件：
     ```properties
     sonar.projectKey=my-spring-project
     sonar.projectName=My Spring Project
     sonar.host.url=http://localhost:9000
     sonar.token=my-token
     sonar.java.binaries=target/classes
     sonar.sources=src/main/java
     sonar.tests=src/test/java
     sonar.junit.reportPaths=target/surefire-reports
     sonar.jacoco.reportPaths=target/jacoco.exec
     sonar.sourceEncoding=UTF-8
     ```

3. **Maven 集成（替代方案）**：
   - 除了 `sonar-project.properties`，也可以在 `pom.xml` 中配置 SonarQube：
     ```xml
     <properties>
         <sonar.host.url>http://localhost:9000</sonar.host.url>
         <sonar.token>my-token</sonar.token>
         <sonar.projectKey>my-spring-project</sonar.projectKey>
         <sonar.projectName>My Spring Project</sonar.projectName>
     </properties>
     <build>
         <plugins>
             <plugin>
                 <groupId>org.sonarsource.scanner.maven</groupId>
                 <artifactId>sonar-maven-plugin</artifactId>
                 <version>3.9.1.2184</version>
             </plugin>
         </plugins>
     </build>
     ```

## 运行 SonarQube 分析

1. **使用 SonarScanner**：
   - 进入项目根目录
   - 运行：
     ```bash
     sonar-scanner
     ```
   - 确保在分析前执行测试（Maven 项目使用 `mvn test`）

2. **使用 Maven**：
   - 运行：
     ```bash
     mvn clean verify sonar:sonar
     ```
   - 此命令会编译代码、运行测试、生成覆盖率报告并将结果发送到 SonarQube

3. **验证结果**：
   - 打开 SonarQube（`http://localhost:9000`）并导航到项目
   - 检查仪表板上的分析结果

## 解读 SonarQube 结果
SonarQube 仪表板提供：
- **概览**：问题、覆盖率和重复代码的摘要
- **问题**：按严重程度（阻塞、严重、主要等）列出的错误、安全漏洞和代码异味
- **代码覆盖率**：测试覆盖的代码百分比（通过 JaCoCo）
- **重复代码**：重复的代码块
- **质量阈**：基于预定义阈值（如覆盖率 > 80%）的通过/失败状态

### 示例操作：
- **修复错误**：处理关键问题，如空指针解引用
- **重构代码异味**：简化复杂方法或移除未使用的代码
- **提高覆盖率**：为未覆盖的代码编写额外的单元测试

## 最佳实践
1. **与 CI/CD 集成**：
   - 将 SonarQube 分析添加到 CI/CD 流水线（如 Jenkins、GitHub Actions）
   - GitHub Actions 工作流示例：
{% raw %}
     ```yaml
     name: CI with SonarQube
     on: [push]
     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v3
           - name: Set up JDK 11
             uses: actions/setup-java@v3
             with:
               java-version: '11'
           - name: Build and Analyze
             run: mvn clean verify sonar:sonar -Dsonar.host.url=http://localhost:9000 -Dsonar.token=${{ secrets.SONAR_TOKEN }}
     ```
{% endraw %}

2. **定义质量阈**：
   - 在 SonarQube 中设置代码覆盖率、错误和安全漏洞的阈值
   - 示例：如果覆盖率 < 80% 或存在严重问题，则构建失败

3. **使用 SonarLint**：
   - 在 IDE（如 IntelliJ IDEA）中安装 SonarLint 插件，在开发过程中发现问题

4. **定期分析**：
   - 每次提交或每天运行 SonarQube 分析，及早发现问题

5. **自定义规则**：
   - 根据项目需求定制 SonarQube 规则（如禁用不相关的规则或添加自定义规则）

## 常见问题排查
1. **分析结果上传失败**：
   - 检查配置中的 `sonar.host.url` 和 `sonar.token`
   - 确保 SonarQube 服务器正在运行（`http://localhost:9000`）

2. **无代码覆盖率数据**：
   - 验证 `pom.xml` 中的 JaCoCo 插件配置是否正确
   - 在分析前运行 `mvn test` 以生成 `jacoco.exec`

3. **数据库连接错误**：
   - 确认 `sonar.properties` 中的数据库凭证
   - 确保数据库服务器正在运行

4. **内存不足**：
   - 在 `sonar.properties` 中增加 JVM 内存：
     ```properties
     sonar.web.javaOpts=-Xmx2g -Xms1g
     ```

## 结论
SonarQube 是维护 Java Spring 项目代码质量的强大工具。通过将其集成到开发工作流中，您可以及早发现问题、提高代码可维护性并确保稳健的安全性。定期分析，结合 CI/CD 集成和 SonarLint 等最佳实践，将帮助您维护高质量的代码库。
