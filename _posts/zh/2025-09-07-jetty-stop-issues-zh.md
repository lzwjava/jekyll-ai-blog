---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 修复Jetty分叉项目停止问题
translated: true
type: note
---

你实际上大部分操作都是正确的——出现卡顿几乎总是因为**停止目标无法连接到分叉的Jetty**（错误的stopHost/端口/密钥作用域）或者因为**`run-forked`意外保持Maven连接**。以下是两个可靠的解决方案，任选其一。

### 方案A —— 可靠模式：`jetty:start`（守护进程）+ `jetty:stop`

这种方式完全避免使用`run-forked`，是集成测试生命周期中最稳定的方案。

**需要调整的内容**

1. 在`pre-integration-test`阶段固定插件版本并使用带`daemon=true`的`start`目标
2. 将Python集成测试保留在`integration-test`阶段
3. 在`post-integration-test`阶段使用`stop`目标
4. 在**两个**执行块中提供*相同*的`stopHost/stopPort/stopKey`配置

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <version>9.4.54.v20240208</version>

  <configuration>
    <httpConnector>
      <port>8080</port>
      <host>127.0.0.1</host>
    </httpConnector>
  </configuration>

  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals>
        <goal>start</goal>
      </goals>
      <configuration>
        <daemon>true</daemon>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec},append=true
        </jvmArgs>
        <webApp>
          <contextPath>/</contextPath>
        </webApp>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals>
        <goal>stop</goal>
      </goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>
      </configuration>
    </execution>
  </executions>
</plugin>
```

**此方案解决"卡住"问题的原理**

* `daemon=true`使`start`目标立即将控制权交还给Maven，以便集成测试可以运行
* 匹配的`stopHost/stopPort/stopKey`确保`stop`目标能够访问到同一个Jetty实例
* 不依赖`run-forked`的监控线程行为

---

### 方案B —— 保留`run-forked`，但确保停止功能实际生效

如果仍想使用`run-forked`，常见陷阱包括：

* `stopHost`默认值可能与子进程绑定方式不一致（IPv6 vs IPv4）
* `stopPort/stopKey`仅在启动执行中设置但**未**在停止执行中镜像配置
* 如果配置错位，子进程可能不会暴露停止处理器

**按以下方式收紧配置：**

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <version>9.4.54.v20240208</version>

  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals>
        <goal>run-forked</goal>
      </goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>

        <httpConnector>
          <host>127.0.0.1</host>
          <port>8080</port>
        </httpConnector>

        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec},append=true
        </jvmArgs>
        <webApp>
          <contextPath>/</contextPath>
        </webApp>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals>
        <goal>stop</goal>
      </goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>
      </configuration>
    </execution>
  </executions>
</plugin>
```

**额外保护措施**

* 如果您的macOS/Java选择IPv6而停止目标使用IPv4，请在子进程`jvmArgs`中添加：

  ```
  <jvmArgs>
    -Djava.net.preferIPv4Stack=true
    -javaagent:...
  </jvmArgs>
  ```

* 确保`8081`端口没有被其他进程占用，如有占用请将启动和停止配置改为其他空闲端口
* 如果集成测试崩溃或卡住，`post-integration-test`可能永远不会执行；这种情况下可添加`verify`阶段的终止回退方案（见下文）

---

### 可选安全网 —— 如果`stop`失败则强制终止子进程

通过写入文件的PID强制终止分叉的Jetty：

1. 在`run-forked`/`start`配置中添加：

```
<pidFile>${project.build.directory}/jetty.pid</pidFile>
```

2. 在`post-integration-test`之后，在`verify`阶段添加`exec-maven-plugin`，检查pid文件并在进程仍存活时强制终止

---

### 从日志中发现的几个小问题

* `No Spring WebApplicationInitializer types detected`在使用`web.xml`+DispatcherServlet时是正常现象，与停止卡住无关
* 建议将集成测试移至**maven-failsafe-plugin**（绑定到`integration-test`/`verify`阶段），单元测试继续使用surefire。当前使用的`exec-maven-plugin`方案可行，但failsafe与集成测试生命周期结合更佳

---

如果需要，请提供完整的Jetty插件配置块及任何`settings.xml`镜像配置（用于本地仓库路径），我会为您的代码库量身定制最精确的最小修改方案。
