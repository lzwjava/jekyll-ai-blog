---
audio: false
generated: true
lang: zh
layout: post
title: Spring Data REST模块
translated: true
type: note
---

要使用 **spring-data-rest-core**，你可以借助 Spring Data REST 模块将 Spring Data 仓库暴露为应用程序中的 RESTful 端点。以下是完整的入门指南：

---

### 1. 添加 Spring Data REST 依赖
要使用 Spring Data REST，你需要在项目中添加其依赖。如果使用 **Spring Boot**（常见场景），请在构建文件中添加以下依赖：

- **Maven**：
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-rest</artifactId>
  </dependency>
  ```

- **Gradle**：
  ```gradle
  implementation 'org.springframework.boot:spring-boot-starter-data-rest'
  ```

该 starter 会引入 `spring-data-rest-core` 及其他必要组件。对于非 Spring Boot 项目，可直接引入 `spring-data-rest-core`，但推荐使用 Spring Boot starter 以简化配置。

---

### 2. 定义实体类
使用 JPA（Java Persistence API）等持久化技术定义实体类来创建领域模型。例如：

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;

@Entity
public class User {
    @Id
    @GeneratedValue
    private Long id;
    private String name;

    // 构造器
    public User() {}
    public User(String name) {
        this.name = name;
    }

    // Getter 和 Setter
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

该 `User` 实体对应数据库中的简单表结构，包含 `id` 和 `name` 字段。

---

### 3. 创建仓库接口
通过扩展 Spring Data 的仓库接口（如 `JpaRepository`）为实体定义仓库接口。例如：

```java
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
```

扩展 `JpaRepository` 即可免费获得基础 CRUD（增删改查）操作。Spring Data REST 会自动将该仓库暴露为 RESTful 端点。

---

### 4. 运行应用程序
添加依赖并定义实体和仓库后，启动 Spring Boot 应用程序。Spring Data REST 将基于仓库自动生成 REST 端点。针对上述 `UserRepository`，可访问：

- **GET /users**：获取所有用户列表
- **GET /users/{id}**：根据 ID 获取特定用户
- **POST /users**：创建新用户（需 JSON 载荷，如 `{"name": "Alice"}`）
- **PUT /users/{id}**：更新现有用户
- **DELETE /users/{id}**：删除用户

例如，若应用程序运行在 `localhost:8080`，可使用 `curl` 或浏览器进行测试：

```bash
curl http://localhost:8080/users
```

响应将包含 HATEOAS 链接，允许客户端动态导航相关资源。

---

### 5. （可选）自定义 REST 端点
可通过注解或配置自定义仓库的暴露方式：

- **修改端点路径**：
  使用 `@RepositoryRestResource` 注解指定自定义路径：
  ```java
  import org.springframework.data.rest.core.annotation.RepositoryRestResource;

  @RepositoryRestResource(path = "people")
  public interface UserRepository extends JpaRepository<User, Long> {
  }
  ```
  此时端点将变为 `/people` 而非 `/users`

- **全局配置**：
  通过实现 `RepositoryRestConfigurer` 自定义基础路径等设置：
  ```java
  import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.data.rest.core.config.RepositoryRestConfiguration;

  @Configuration
  public class RestConfig implements RepositoryRestConfigurer {
      @Override
      public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config) {
          config.setBasePath("/api"); // 所有端点将以 /api 开头
      }
  }
  ```
  配置后，用户数据将可通过 `/api/users` 访问

---

### Spring Data REST 核心特性
- **HATEOAS 支持**：响应包含超媒体链接指向相关资源
- **分页与排序**：使用 `?page=0&size=10&sort=name,asc` 等查询参数进行分页和排序
- **过滤功能**：在仓库中添加自定义查询方法（如 `findByName(String name)`）可暴露额外端点

---

### 总结
使用 `spring-data-rest-core` 的步骤：
1. 引入 Spring Data REST 依赖（如 Spring Boot 项目使用 `spring-boot-starter-data-rest`）
2. 使用相应注解（如 JPA 的 `@Entity`）定义实体
3. 创建扩展 Spring Data 接口（如 `JpaRepository`）的仓库接口
4. 运行应用程序即可访问自动生成的 REST 端点
5. 按需自定义端点路径或行为

该方法能通过最简代码快速构建 RESTful API，充分发挥 Spring Data REST 的核心功能。
