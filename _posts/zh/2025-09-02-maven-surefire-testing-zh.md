---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Maven Surefire插件单元测试指南
translated: true
type: note
---

**Maven Surefire Plugin** 是在 Maven 构建生命周期的 **test** 阶段运行单元测试的插件。由于几乎所有项目都需要将自动化测试集成到构建过程中，它成为了最常用的 Maven 插件之一。

---

## 插件简介

* **名称**：`maven-surefire-plugin`
* **用途**：执行基于 JUnit（3、4、5）、TestNG 等测试框架编写的测试用例
* **绑定阶段**：Maven 默认生命周期的 `test` 阶段
* **输出**：生成测试报告（默认保存在 `target/surefire-reports` 目录）

---

## 工作原理

1. 当执行 `mvn test` 或 `mvn package` 命令时，Maven 会调用 Surefire 插件
2. 插件会扫描 `src/test/java` 目录中的测试类
3. 默认匹配以下命名模式的测试文件：

   * `*Test.java`
   * `Test*.java`
   * `*Tests.java`
   * `*TestCase.java`
4. 在独立的类加载器中执行测试用例
5. 将测试结果输出到 `target/surefire-reports` 目录（支持纯文本、XML 格式，通过报告插件还可生成 HTML）

---

## 基础用法

在 `pom.xml` 中进行配置：

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>3.2.5</version> <!-- 建议使用最新稳定版 -->
    </plugin>
  </plugins>
</build>
```

配置完成后执行：

```bash
mvn test
```

---

## 常用配置

* **包含/排除模式**：

```xml
<configuration>
  <includes>
    <include>**/*MyTest.java</include>
  </includes>
  <excludes>
    <exclude>**/IntegrationTest.java</exclude>
  </excludes>
</configuration>
```

* **系统属性配置**：

```xml
<configuration>
  <systemPropertyVariables>
    <env>dev</env>
  </systemPropertyVariables>
</configuration>
```

* **并行测试执行**：

```xml
<configuration>
  <forkCount>2</forkCount>
  <reuseForks>true</reuseForks>
  <parallel>classes</parallel>
</configuration>
```

此配置可在多个 JVM 进程或线程中并行运行测试。

---

## 适用场景

* 需要将**单元测试**集成到 Maven 生命周期时
* 实现**单元测试（Surefire）**与**集成测试（Failsafe 插件）**的分离：

  * Surefire → 单元测试（`mvn test`）
  * Failsafe → 集成测试（`mvn verify`）

---

✅ **总结**：`maven-surefire-plugin` 是 Maven 项目中执行单元测试的核心插件。通过在 `pom.xml` 中配置，使用 `mvn test` 命令运行测试，并在 `target/surefire-reports` 目录中查看测试报告。

---

需要我进一步解释 **Surefire 和 Failsafe 插件的区别**吗？（这两个插件经常被混淆）
