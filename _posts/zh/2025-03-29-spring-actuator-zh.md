---
audio: false
generated: true
lang: zh
layout: post
title: Spring Actuator
translated: true
type: note
---

Spring Actuator 是 Spring Boot 中一项强大的功能，为应用程序监控和管理提供生产就绪工具。以下是详细使用指南：

### 1. **添加 Spring Actuator 依赖**
在项目中引入依赖。若使用 Maven，在 `pom.xml` 中添加：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

若使用 Gradle，在 `build.gradle` 中添加：

```gradle
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

### 2. **启动 Spring Boot 应用**
添加依赖后启动应用，Spring Actuator 将自动启用一系列用于监控和交互的端点。

### 3. **访问默认端点**
Spring Actuator 默认通过 HTTP 暴露多个端点，基础路径为 `/actuator`。常用端点示例（假设应用运行于 `localhost:8080`）：
- **健康检查**：`http://localhost:8080/actuator/health`
  - 返回应用状态（如 `{"status":"UP"}`）
- **应用信息**：`http://localhost:8080/actuator/info`
  - 显示可配置的任意应用信息
- **指标数据**：`http://localhost:8080/actuator/metrics`
  - 提供内存使用率、CPU 等详细指标

出于安全考虑，默认仅启用 `/health` 和 `/info` 端点，需手动配置暴露更多端点。

### 4. **配置 Actuator 端点**
通过 `application.properties` 或 `application.yml` 自定义暴露的端点：

#### `application.properties`
```properties
# 启用特定端点
management.endpoints.web.exposure.include=health,info,metrics,beans

# 修改基础路径（可选）
management.endpoints.web.base-path=/manage
```

#### `application.yml`
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, beans
      base-path: /manage
```

配置后可通过 `/manage/metrics` 或 `/manage/beans` 等路径访问端点。

### 5. **探索可用端点**
以下为可启用的常用端点：
- `/actuator/beans`：列出应用中所有 Spring bean
- `/actuator/env`：显示环境属性
- `/actuator/loggers`：查看和修改日志级别
- `/actuator/shutdown`：优雅停止应用（默认禁用）

测试时可启用所有端点：
```properties
management.endpoints.web.exposure.include=*
```

### 6. **保护 Actuator 端点**
由于端点可能暴露敏感信息，生产环境需加强安全：
- 添加 Spring Security：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```
- 在 `application.properties` 中配置安全：
```properties
spring.security.user.name=admin
spring.security.user.password=secret
management.endpoints.web.exposure.include=health,metrics
```
现在访问端点需进行身份验证（如使用 `admin:secret`）

### 7. **添加自定义健康检查（可选）**
通过实现 `HealthIndicator` 接口创建自定义健康指示器：

```java
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class CustomHealthCheck implements HealthIndicator {
    @Override
    public Health health() {
        boolean isHealthy = checkSomeCondition();
        if (isHealthy) {
            return Health.up().withDetail("customCheck", "运行正常").build();
        }
        return Health.down().withDetail("customCheck", "出现异常").build();
    }

    private boolean checkSomeCondition() {
        // 自定义检查逻辑
        return true;
    }
}
```

该检查结果将显示在 `/actuator/health` 端点中。

### 8. **监控指标数据**
启用 `/metrics` 端点后可查看具体指标：
- `http://localhost:8080/actuator/metrics/jvm.memory.used`
- `http://localhost:8080/actuator/metrics/http.server.requests`

可集成 Prometheus 或 Grafana 等工具进行高级监控。

### 9. **功能测试**
启动应用后通过浏览器、`curl` 或 Postman 测试端点：
```bash
curl http://localhost:8080/actuator/health
```

### 使用技巧
- 通过 `/actuator/info` 暴露自定义信息（如应用版本）：
```properties
info.app.name=MyApp
info.app.version=1.0.0
```
- 配置修改后需重启应用

以上是基础使用方法，如有特定使用场景或问题排查需求，欢迎进一步交流！
