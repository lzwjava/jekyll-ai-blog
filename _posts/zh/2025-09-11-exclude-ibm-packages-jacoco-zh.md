---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 在JaCoCo中排除com.ibm包
translated: true
type: note
---

若要在 **WebSphere Liberty Profile** 环境中从 JaCoCo 覆盖率中排除 **`com.ibm`** 包（或其他任何包），您可以在 **`pom.xml`** 文件中配置排除项。这通常在 **JaCoCo Maven 插件** 配置中完成。

---

### **如何在 `pom.xml` 中排除 `com.ibm` 包**

您可以在 JaCoCo 插件配置中使用 `<excludes>` 标签来指定应从覆盖率报告中排除的类或包。

#### **配置示例：**

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version> <!-- 请使用最新版本 -->
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
                    <configuration>
                        <outputDirectory>${project.reporting.outputDirectory}/jacoco</outputDirectory>
                        <excludes>
                            <!-- 排除所有 com.ibm 包 -->
                            <exclude>com/ibm/**</exclude>
                        </excludes>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

---

### **说明：**
- **`<excludes>`**：此部分指定应从覆盖率报告中排除的类或包。
- **`<exclude>com/ibm/**</exclude>`**：这会排除 `com.ibm` 包及其所有子包下的所有类。

---

### **补充说明：**
- 如需排除多个包，可添加更多 `<exclude>` 条目：
  ```xml
  <excludes>
      <exclude>com/ibm/**</exclude>
      <exclude>org/apache/**</exclude>
  </excludes>
  ```
- 如果在 **WebSphere Liberty** 中使用 **JaCoCo**，请确保 JaCoCo 代理已在 `server.env` 或 `jvm.options` 文件中正确配置，并且 `pom.xml` 中的排除项符合您的要求。

---

### **最佳实践：**
- 始终通过运行覆盖率报告并检查排除的包是否未包含在结果中来验证排除项。
- 如果需要在运行时（例如在 JaCoCo 代理参数中）排除包，可以在代理参数中使用 `excludes` 参数：
  ```plaintext
  -javaagent:/path/to/jacocoagent.jar=destfile=/path/to/jacoco.exec,excludes=com.ibm.*
  ```
