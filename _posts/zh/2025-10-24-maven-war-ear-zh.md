---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Maven WAR与EAR模块配置
translated: true
type: note
---

### Maven多模块项目实现WAR到EAR的打包配置

在Maven中，要实现一个模块生成WAR文件（例如Web应用），另一个模块将其组装成EAR（企业级归档包），需要使用多模块项目结构。EAR模块通过`maven-ear-plugin`依赖WAR模块，确保在构建过程中将WAR包含在EAR中。

#### 第一步：创建父级POM
父级POM定义模块并管理共享配置，需将其打包类型设置为`pom`。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>web-module</module>  <!-- 优先构建此模块 -->
        <module>ear-module</module>
    </modules>

    <!-- 可选：共享依赖和插件版本管理 -->
    <dependencyManagement>
        <dependencies>
            <!-- 在此定义子模块版本 -->
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <!-- 管理插件版本 -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-ear-plugin</artifactId>
                    <version>3.3.0</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

#### 第二步：配置WAR模块
该模块将Web应用打包为WAR，需设置打包类型为`war`。此处无需特殊EAR配置，只需确保优先构建。

目录结构：`web-module/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>web-module</artifactId>
    <packaging>war</packaging>

    <dependencies>
        <!-- 添加Web依赖，例如servlet-api -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.3.2</version>
            </plugin>
        </plugins>
    </build>
</project>
```

#### 第三步：配置EAR模块
该模块负责组装EAR，需设置打包类型为`ear`，并通过`maven-ear-plugin`引用WAR模块。该插件将拉取WAR构件并打包进EAR。

目录结构：`ear-module/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>ear-module</artifactId>
    <packaging>ear</packaging>

    <dependencies>
        <!-- 依赖WAR模块以包含到构建中 -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>web-module</artifactId>
            <version>${project.version}</version>
            <type>war</type>
        </dependency>
        <!-- 可选：添加EJB或其他模块 -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-ear-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <!-- EAR版本（例如Java EE） -->
                    <version>8</version>

                    <!-- EAR中的库目录 -->
                    <defaultLibBundleDir>lib</defaultLibBundleDir>

                    <!-- 瘦身WAR（排除已存在于EAR库的依赖） -->
                    <skinnyWars>true</skinnyWars>

                    <!-- 定义要包含的模块 -->
                    <modules>
                        <webModule>
                            <groupId>com.example</groupId>
                            <artifactId>web-module</artifactId>
                            <bundleDir>/</bundleDir>  <!-- EAR根目录 -->
                            <contextRoot>/mywebapp</contextRoot>  <!-- 部署上下文路径 -->
                        </webModule>
                        <!-- 如需添加<ejbModule>或<jarModule> -->
                    </modules>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### 第四步：构建项目
- 在**父目录**执行：`mvn clean install`
  - 此命令按顺序构建模块（先WAR后EAR）
- EAR将生成在`ear-module/target/ear-module-1.0-SNAPSHOT.ear`
- 若仅构建EAR（假设WAR已构建）：`cd ear-module && mvn clean package`

#### 关键要点
- **构建顺序**：在父POM的`<modules>`中WAR模块需列在EAR之前，确保Maven优先构建WAR
- **依赖关系**：EAR模块通过`<dependency>`依赖WAR，确保在打包时解析依赖
- **自定义配置**：通过`<contextRoot>`调整Web应用URL路径，在`<modules>`中添加更多模块（如EJB JAR）
- **故障排查**：若WAR未包含，检查构件坐标是否完全匹配，可在EAR模块使用`mvn dependency:tree`验证

更多细节请参考官方Maven EAR插件文档。

[Apache Maven EAR Plugin](https://maven.apache.org/plugins/maven-ear-plugin/)
[Maven多模块项目指南](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Multi-module_Projects)
