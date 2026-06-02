---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot 日志自动收集
translated: true
type: note
---

你说得完全正确！手动复制粘贴日志确实繁琐且容易出错。让我来展示如何在 Spring Boot 项目中配置使用 Logback 实现自动化日志收集。

现在让我展示如何在 Spring Boot 应用属性中配置这个功能：

如果你更喜欢编程式配置，这里也提供 Java 配置方式：

以下是这种自动化设置的主要优势：

**这个配置能为你带来：**

1. **自动创建日志目录** - 在项目中创建 `logs/` 文件夹
2. **多日志文件** - 分离常规日志、错误日志和启动日志
3. **滚动文件** - 按日期和大小自动轮转日志
4. **基于会话的日志记录** - 每次运行都会生成带时间戳的日志文件
5. **无需手动复制** - 所有内容自动保存

**你将获得的文件结构：**

```
logs/
├── myapp.log                    # 当前常规日志
├── myapp-error.log             # 仅错误日志
├── myapp-startup.log           # 启动日志
├── myapp-session-20250710_143022.log  # 特定会话日志
└── archived/                   # 旧的轮转日志
```

**使用方法：**

1. 将 `logback-spring.xml` 放入 `src/main/resources/` 文件夹
2. 在 `application.yml` 中更新日志配置
3. 运行你的 Spring Boot 应用
4. 日志将自动收集在 `logs/` 目录中

这完全消除了手动复制日志的需要 - 你的应用每次运行都会自动生成有组织、可搜索的日志文件，方便后续查阅！

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- 定义日志目录和文件模式 -->
    <property name="LOG_DIR" value="logs"/>
    <property name="APP_NAME" value="myapp"/>

    <!-- 控制台输出器用于开发 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- 文件输出器用于所有日志 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_DIR}/${APP_NAME}.log</file>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_DIR}/${APP_NAME}.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>300MB</totalSizeCap>
        </rollingPolicy>
    </appender>

    <!-- 单独输出器仅用于错误日志 -->
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_DIR}/${APP_NAME}-error.log</file>
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n%ex</pattern>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_DIR}/${APP_NAME}-error.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>100MB</totalSizeCap>
        </rollingPolicy>
    </appender>

    <!-- 单独输出器用于启动日志 -->
    <appender name="STARTUP_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_DIR}/${APP_NAME}-startup.log</file>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_DIR}/${APP_NAME}-startup.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>7</maxHistory>
        </rollingPolicy>
    </appender>

    <!-- 应用特定日志记录器用于启动事件 -->
    <logger name="org.springframework.boot" level="INFO" additivity="false">
        <appender-ref ref="STARTUP_FILE"/>
        <appender-ref ref="FILE"/>
        <appender-ref ref="CONSOLE"/>
    </logger>

    <!-- 捕获 SQL 日志（如果使用 JPA） -->
    <logger name="org.hibernate.SQL" level="DEBUG" additivity="false">
        <appender-ref ref="FILE"/>
    </logger>

    <!-- 根日志记录器配置 -->
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
        <appender-ref ref="ERROR_FILE"/>
    </root>

    <!-- 环境特定配置 -->
    <springProfile name="prod">
        <root level="WARN">
            <appender-ref ref="FILE"/>
            <appender-ref ref="ERROR_FILE"/>
        </root>
    </springProfile>

    <springProfile name="dev">
        <root level="DEBUG">
            <appender-ref ref="CONSOLE"/>
            <appender-ref ref="FILE"/>
            <appender-ref ref="ERROR_FILE"/>
        </root>
    </springProfile>
</configuration>
```

```yaml
spring:
  application:
    name: myapp

logging:
  config: classpath:logback-spring.xml
  level:
    root: INFO
    com.yourpackage: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG

# 替代方案：直接在 application.yml 中配置（更简单的方法）
  file:
    name: logs/${spring.application.name}.log
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
  logback:
    rollingpolicy:
      max-file-size: 10MB
      max-history: 30
      total-size-cap: 300MB

# 用于监控日志的管理端点
management:
  endpoints:
    web:
      exposure:
        include: health,info,loggers,logfile
  endpoint:
    loggers:
      enabled: true
```

```java
package com.yourpackage.config;

import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.encoder.PatternLayoutEncoder;
import ch.qos.logback.classic.filter.LevelFilter;
import ch.qos.logback.core.rolling.RollingFileAppender;
import ch.qos.logback.core.rolling.TimeBasedRollingPolicy;
import ch.qos.logback.core.util.FileSize;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

import javax.annotation.PostConstruct;
import java.io.File;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Configuration
public class LoggingConfiguration {

    @Value("${spring.application.name:myapp}")
    private String appName;

    @Value("${logging.path:logs}")
    private String logPath;

    @PostConstruct
    public void initLogging() {
        setupLogDirectory();
        setupSessionLogger();
    }

    private void setupLogDirectory() {
        File logDir = new File(logPath);
        if (!logDir.exists()) {
            logDir.mkdirs();
        }
    }

    private void setupSessionLogger() {
        LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();

        // 创建会话特定的日志文件
        String sessionId = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String sessionLogFile = logPath + "/" + appName + "-session-" + sessionId + ".log";

        // 设置会话输出器
        RollingFileAppender sessionAppender = new RollingFileAppender();
        sessionAppender.setContext(context);
        sessionAppender.setFile(sessionLogFile);

        // 模式编码器
        PatternLayoutEncoder encoder = new PatternLayoutEncoder();
        encoder.setContext(context);
        encoder.setPattern("%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n");
        encoder.start();
        sessionAppender.setEncoder(encoder);

        // 滚动策略
        TimeBasedRollingPolicy rollingPolicy = new TimeBasedRollingPolicy();
        rollingPolicy.setContext(context);
        rollingPolicy.setParent(sessionAppender);
        rollingPolicy.setFileNamePattern(logPath + "/" + appName + "-session-%d{yyyy-MM-dd}.%i.log");
        rollingPolicy.setMaxHistory(7);
        rollingPolicy.setTotalSizeCap(FileSize.valueOf("100MB"));
        rollingPolicy.start();

        sessionAppender.setRollingPolicy(rollingPolicy);
        sessionAppender.start();

        // 添加到根日志记录器
        Logger rootLogger = context.getLogger(Logger.ROOT_LOGGER_NAME);
        rootLogger.addAppender(sessionAppender);
    }
}

// 用于自定义日志收集的工具类
@Component
public class LogCollector {

    private static final Logger logger = LoggerFactory.getLogger(LogCollector.class);

    @Value("${logging.path:logs}")
    private String logPath;

    @EventListener(ApplicationReadyEvent.class)
    public void onApplicationReady() {
        logger.info("应用成功启动于 {}", LocalDateTime.now());
        logger.info("日志文件收集在: {}", new File(logPath).getAbsolutePath());
    }

    @EventListener(ContextClosedEvent.class)
    public void onApplicationShutdown() {
        logger.info("应用关闭于 {}", LocalDateTime.now());
        collectFinalLogs();
    }

    private void collectFinalLogs() {
        // 可选：在关闭时压缩或归档日志
        try {
            File logDir = new File(logPath);
            if (logDir.exists()) {
                logger.info("日志收集完成。总文件数: {}", logDir.listFiles().length);
            }
        } catch (Exception e) {
            logger.error("日志收集过程中出错", e);
        }
    }
}
```
