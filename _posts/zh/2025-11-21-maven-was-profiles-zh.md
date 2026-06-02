---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: WAS环境配置中的Maven配置管理
translated: true
type: note
---

针对 IBM WebSphere Application Server（传统 WAS，非 Liberty），标准打包格式是 **EAR** 文件（即使是简单 Web 应用，WAS 也优先使用 EAR 而非独立 WAR）。处理不同环境（如本地开发环境使用固定/硬编码测试账号，服务器/生产环境使用 SSO 或正规安全域）的最佳实践是在单个 `pom.xml` 中使用 **Maven 构建配置档**。这能避免维护多个独立 POM 文件（如 `pom.xml` 和 `build_pom.xml`），既容易出错也不符合 Maven 惯例。

### 为何选择配置档而非多 POM？
- 单一可信源（单个 POM）
- 灵活激活：`mvn package -Plocal` 或 `mvn package -Pserver`
- 配置档可实现资源过滤、文件覆盖、插件配置调整或绑定修改（如 WAS 专用认证的 `ibm-web-bnd.xml`、`ibm-application-ext.xml`）
- 常用于开发/测试/生产环境差异配置，包括认证设置

### 推荐结构
使用 Maven 资源插件配合过滤功能 + 配置档专属资源目录，实现配置文件切换（如 `web.xml`、属性文件、Spring 安全配置或 WAS 绑定文件）

目录结构示例：
```
src/
├── main/
│   ├── resources/          (通用配置)
│   ├── webapp/
│   │   ├── WEB-INF/
│   │   │   ├── web.xml      (基础版本)
│   │   │   └── ibm-web-bnd.xml (可选，用于 JNDI/认证绑定)
│   └── ...
├── local/                   (本地环境专属资源)
│   └── webapp/
│       └── WEB-INF/
│           ├── web.xml      (含表单登录+硬编码用户/角色或无需安全配置的本地版本)
│           └── ...
└── server/                  (生产/SSO 环境专属资源)
    └── webapp/
        └── WEB-INF/
            ├── web.xml      (服务端版本配置 SSO：<login-config><auth-method>CLIENT-CERT</auth-method> 或 SPNEGO)
            └── ...
```

### pom.xml 配置示例
```xml
<project ...>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-was-app</artifactId>
    <version>1.0.0</version>
    <packaging>ear</packaging>   <!-- 若部署 WAR 可调整，但 WAS 优先推荐 EAR -->

    <properties>
        <maven.compiler.source>11</maven.compiler.source> <!-- 按需调整 Java 版本 -->
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- 应用依赖 -->
        <!-- WAS 编译期 API（provided 作用域） -->
        <dependency>
            <groupId>com.ibm.tools.target</groupId>
            <artifactId>was</artifactId>
            <version>9.0</version> <!-- 匹配 WAS 版本 -->
            <type>pom</type>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- EAR 打包插件（如需 WAR 请调整） -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-ear-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <!-- EAR 配置参数 -->
                </configuration>
            </plugin>

            <!-- 资源过滤与配置档覆盖 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.3.1</version>
                <configuration>
                    <useDefaultDelimiters>true</useDefaultDelimiters>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <!-- 配置档定义 -->
    <profiles>
        <!-- 本地开发配置档：固定用户/表单登录或免认证 -->
        <profile>
            <id>local</id>
            <activation>
                <activeByDefault>true</activeByDefault> <!-- 本地构建默认激活 -->
            </activation>
            <build>
                <resources>
                    <!-- 通用资源 -->
                    <resource>
                        <directory>src/main/resources</directory>
                        <filtering>true</filtering>
                    </resource>
                    <!-- 本地专属文件覆盖 -->
                    <resource>
                        <directory>src/local/webapp</directory>
                        <targetPath>${project.build.directory}/${project.artifactId}/WEB-INF</targetPath>
                    </resource>
                </resources>
            </build>
            <properties>
                <!-- 本地硬编码用户示例 -->
                <app.login.user>devuser</app.login.user>
                <app.login.password>devpass</app.login.password>
            </properties>
        </profile>

        <!-- 生产环境配置档：真实 SSO -->
        <profile>
            <id>server</id>
            <build>
                <resources>
                    <resource>
                        <directory>src/main/resources</directory>
                        <filtering>true</filtering>
                    </resource>
                    <resource>
                        <directory>src/server/webapp</directory>
                        <targetPath>${project.build.directory}/${project.artifactId}/WEB-INF</targetPath>
                    </resource>
                </resources>
            </build>
            <properties>
                <!-- 生产环境属性 -->
                <app.auth.method>SSO</app.auth.method>
            </properties>
        </profile>
    </profiles>
</project>
```

### 认证差异配置要点
- **本地环境**：在 `web.xml` 或属性文件中配置表单登录与简单用户/角色，或完全禁用安全约束（移除 `<security-constraint>`）
- **生产环境**：在 `web.xml` 中配置 WAS 专用 SSO（如结合 SPNEGO 的 `<auth-method>FORM</auth-method>`，或传统 WAS 常用的 LTPA + 全局安全域）。WAS 绑定文件（`ibm-web-bnd.xml`）也可按配置档覆盖用户/角色映射
- 若使用 Spring Security：通过相同方式切换 `applicationContext-security.xml` 或属性文件
- 本地硬编码用户：避免真实凭证，建议使用测试用户映射到本地 `users.properties` 或通过标志位禁用认证检查

### 构建命令
- 本地环境（默认）：`mvn clean package`
- 生产环境：`mvn clean package -Pserver`

通过此方案可从 **同一代码库** 生成适应不同环境的 EAR 文件。如需差异化产物命名（如 `myapp-local.ear` 与 `myapp.ear`），可在配置档的 `<build>` 章节添加 `<finalName>${project.artifactId}-${profile}</finalName>`

[Maven 配置档指南](https://maven.apache.org/guides/introduction/introduction-to-profiles.html)
[Maven EAR 插件文档](https://maven.apache.org/plugins/maven-ear-plugin/)
[IBM WAS Maven 集成指南](https://www.ibm.com/docs/en/wasdtfe/9.7.0?topic=suye-configuring-dependency-pom-files-that-emulate-classpath-specific-websphere-runtime-environments)
