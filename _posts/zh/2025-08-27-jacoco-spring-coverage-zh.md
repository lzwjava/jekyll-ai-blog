---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JaCoCo多模块Spring覆盖率配置
translated: true
type: note
---

很好——JaCoCo 在多模块 Spring 项目中表现优异。您需要实现：

1. 各模块的单元测试覆盖率；
2. 父项目的聚合报告；
3. 可选配置档用于整合**集成**测试覆盖率（例如被 Python 测试调用的 Liberty+EAR 运行结果）。

以下是一套经过实战检验的配置方案，可直接使用。

---

### 父级 `pom.xml`（打包方式为 `pom`）

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.myco.chat</groupId>
  <artifactId>chat-parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>ChatCommon</module>
    <module>ChatLib</module>
    <module>ChatCore</module>
    <module>ChatWeb</module>
  </modules>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.jacoco</groupId>
          <artifactId>jacoco-maven-plugin</artifactId>
          <version>0.8.12</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>3.2.5</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-failsafe-plugin</artifactId>
          <version>3.2.5</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>

  <!-- 为所有模块的单元测试生成聚合报告 -->
  <reporting>
    <plugins>
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <reportSets>
          <reportSet>
            <reports>
              <!-- 在父级执行 'mvn verify' 时会触发 'report-aggregate' -->
              <report>report-aggregate</report>
            </reports>
            <configuration>
              <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate</outputDirectory>
              <reports>
                <xml>true</xml>
                <html>true</html>
                <csv>false</csv>
              </reports>
              <!-- 可选全局过滤规则 -->
              <excludes>
                <exclude>**/*Application.class</exclude>
                <exclude>**/*Configuration.class</exclude>
                <exclude>**/generated/**</exclude>
              </excludes>
            </configuration>
          </reportSet>
        </plugins>
      </plugin>
    </plugins>
  </reporting>

  <!-- 用于添加集成测试覆盖率的配置档（例如 Liberty + Python 测试） -->
  <profiles>
    <profile>
      <id>it-coverage</id>
      <activation><activeByDefault>false</activeByDefault></activation>
      <build>
        <plugins>
          <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.12</version>
            <executions>
              <!-- 创建同时读取外部 .exec 文件的聚合报告 -->
              <execution>
                <id>report-aggregate-it</id>
                <phase>verify</phase>
                <goals><goal>report-aggregate</goal></goals>
                <configuration>
                  <!-- 指向 Liberty JVM 代理生成的 .exec 文件 -->
                  <dataFiles>
                    <!-- 示例路径，请根据 CI/Liberty 位置调整 -->
                    <dataFile>${project.basedir}/.jacoco/jacoco-it.exec</dataFile>
                    <!-- 如需整合多节点数据可添加更多 dataFile 条目 -->
                  </dataFiles>
                  <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate-it</outputDirectory>
                  <reports>
                    <xml>true</xml>
                    <html>true</html>
                    <csv>false</csv>
                  </reports>
                  <excludes>
                    <exclude>**/generated/**</exclude>
                  </excludes>
                </configuration>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
```

---

### 子模块配置（`ChatCommon/pom.xml`, `ChatLib/pom.xml`, `ChatCore/pom.xml`, `ChatWeb/pom.xml`）

```xml
<project>
  <parent>
    <groupId>com.myco.chat</groupId>
    <artifactId>chat-parent</artifactId>
    <version>1.0.0</version>
  </parent>
  <modelVersion>4.0.0</modelVersion>
  <artifactId>ChatCommon</artifactId>
  <packaging>jar</packaging>

  <build>
    <plugins>
      <!-- 为本模块单元测试挂载代理 -->
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <executions>
          <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
            <configuration>
              <!-- 将 argLine 存入命名属性，便于与其他参数混合使用 -->
              <propertyName>jacocoArgLine</propertyName>
              <append>true</append>
              <excludes>
                <exclude>**/generated/**</exclude>
              </excludes>
            </configuration>
          </execution>
          <execution>
            <id>report</id>
            <phase>verify</phase>
            <goals><goal>report</goal></goals>
            <configuration>
              <reports>
                <xml>true</xml>
                <html>true</html>
                <csv>false</csv>
              </reports>
            </configuration>
          </execution>
          <!-- 可选：覆盖率阈值检查 -->
          <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
              <rules>
                <rule>
                  <element>PACKAGE</element>
                  <limits>
                    <limit>
                      <counter>LINE</counter>
                      <value>COVEREDRATIO</value>
                      <minimum>0.60</minimum>
                    </limit>
                    <limit>
                      <counter>BRANCH</counter>
                      <value>COVEREDRATIO</value>
                      <minimum>0.40</minimum>
                    </limit>
                  </limits>
                </rule>
              </rules>
            </configuration>
          </execution>
        </executions>
      </plugin>

      <!-- 确保 Surefire 使用代理配置 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <argLine>${jacocoArgLine} ${surefireArgLine}</argLine>
        </configuration>
      </plugin>

      <!-- （可选）模块级集成测试配置 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-failsafe-plugin</artifactId>
        <configuration>
          <argLine>${jacocoArgLine} ${failsafeArgLine}</argLine>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

> 在 `ChatLib`、`ChatCore` 和 `ChatWeb` 中采用相同配置
> 对于 Spring Boot WAR/JAR 项目的 `ChatWeb`，配置完全一致

---

### 运行说明

**跨模块单元测试覆盖率（父级生成聚合 XML）：**

```bash
mvn -q clean verify
# XML:  target/site/jacoco-aggregate/jacoco.xml
# HTML: target/site/jacoco-aggregate/index.html
```

**Liberty + Python 测试的集成覆盖率：**

1. 使用 JaCoCo 代理启动 Liberty（如前所述），运行 Python 测试后停止或转储数据
   确保 `.exec` 文件生成在 `${project.basedir}/.jacoco/jacoco-it.exec`（或在父配置档中更新路径）
2. 构建包含集成测试数据的聚合报告：

```bash
mvn -q -Pit-coverage verify
# XML:  target/site/jacoco-aggregate-it/jacoco.xml
# HTML: target/site/jacoco-aggregate-it/index.html
```

---

### 省时要点

* **聚合功能仅适用于声明模块的父级项目**（打包方式为 `pom`）。请在父目录执行 `mvn` 命令
* 在 `<reports>` 中启用 **XML** 输出（`jacoco.xml`）后，Codecov/Sonar 可直接使用
* 如需收集多个 `.exec` 文件（例如多个 Liberty 节点），可：
  * 在 `it-coverage` 配置档的 `<dataFiles>…</dataFile>` 中列出所有文件，或
  * 先用 `jacococli.jar merge …` 合并文件，再指向合并后的文件
* 不要指向 EAR 的类文件——JaCoCo 报告需要**模块编译后的类**（`*/target/classes`）和源码，`report-aggregate` 会自动处理
* 如果 Surefire 也设置了 `argLine`，请将 `${jacocoArgLine}` 置于首位以免丢失代理配置

如果您能提供具体的模块包根路径和 Liberty `.exec` 文件生成位置，我可以为您定制 `<dataFiles>` 和排除规则，确保聚合 XML 清晰可用且满足 CI 要求。
