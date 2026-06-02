---
audio: false
generated: true
lang: en
layout: post
title: Spring Actuator
translated: false
type: note
---

Spring Actuator is a powerful feature in Spring Boot that provides production-ready tools for monitoring and managing your application. Here's a step-by-step guide on how to use it:

### 1. **Add Spring Actuator Dependency**
To use Spring Actuator, you need to include its dependency in your project. If you're using Maven, add this to your `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

For Gradle, add this to your `build.gradle`:

```gradle
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

### 2. **Start Your Spring Boot Application**
Once the dependency is added, start your Spring Boot application. Spring Actuator will automatically enable a set of endpoints that you can use to monitor and interact with your app.

### 3. **Access Default Endpoints**
Spring Actuator exposes several endpoints over HTTP by default. The base path is `/actuator`. Here are some commonly used ones (assuming your app runs on `localhost:8080`):
- **Health Check**: `http://localhost:8080/actuator/health`
  - Returns the status of your application (e.g., `{"status":"UP"}`).
- **Application Info**: `http://localhost:8080/actuator/info`
  - Displays arbitrary application info (configurable).
- **Metrics**: `http://localhost:8080/actuator/metrics`
  - Provides detailed metrics like memory usage, CPU, and more.

By default, only `/health` and `/info` are enabled for security reasons. To expose more endpoints, you need to configure them.

### 4. **Configure Actuator Endpoints**
You can customize which endpoints are exposed in your `application.properties` or `application.yml` file. For example:

#### `application.properties`
```properties
# Enable specific endpoints
management.endpoints.web.exposure.include=health,info,metrics,beans

# Change the base path (optional)
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

With this config, endpoints like `/manage/metrics` or `/manage/beans` will be available.

### 5. **Explore Available Endpoints**
Here are some useful Actuator endpoints you can enable:
- `/actuator/beans`: Lists all Spring beans in your application.
- `/actuator/env`: Shows environment properties.
- `/actuator/loggers`: Displays and modifies logger levels.
- `/actuator/shutdown`: Gracefully shuts down the app (disabled by default).

To enable all endpoints for testing, use:
```properties
management.endpoints.web.exposure.include=*
```

### 6. **Secure Actuator Endpoints**
Since Actuator exposes sensitive data, you should secure it in production:
- Add Spring Security:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```
- Configure security in `application.properties`:
```properties
spring.security.user.name=admin
spring.security.user.password=secret
management.endpoints.web.exposure.include=health,metrics
```
Now, accessing endpoints will require authentication (e.g., `admin:secret`).

### 7. **Add Custom Health Checks (Optional)**
You can create custom health indicators by implementing the `HealthIndicator` interface. Example:

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
            return Health.up().withDetail("customCheck", "All good!").build();
        }
        return Health.down().withDetail("customCheck", "Something's wrong").build();
    }

    private boolean checkSomeCondition() {
        // Your logic here
        return true;
    }
}
```

This will appear in the `/actuator/health` endpoint.

### 8. **Monitor Metrics**
To dive deeper into metrics, enable `/metrics` and explore specific ones like:
- `http://localhost:8080/actuator/metrics/jvm.memory.used`
- `http://localhost:8080/actuator/metrics/http.server.requests`

You can integrate with tools like Prometheus or Grafana for advanced monitoring.

### 9. **Test It Out**
Run your app and hit the endpoints using a browser, `curl`, or tools like Postman. For example:
```bash
curl http://localhost:8080/actuator/health
```

### Tips
- Use `/actuator/info` to expose custom info (e.g., app version) by adding:
```properties
info.app.name=MyApp
info.app.version=1.0.0
```
- Restart your app after making configuration changes.

That’s the basics! Let me know if you want help with a specific use case or troubleshooting.
