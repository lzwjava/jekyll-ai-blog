---
audio: false
generated: true
lang: en
layout: post
title: Spring Data REST Module
translated: false
type: note
---

To use **spring-data-rest-core**, you can leverage the Spring Data REST module to expose your Spring Data repositories as RESTful endpoints in your application. Below is a complete, step-by-step guide to get you started:

---

### 1. Add the Spring Data REST Dependency
To use Spring Data REST, you need to include its dependency in your project. If you're using **Spring Boot** (a common scenario), add the following dependency to your build file:

- **Maven**:
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-rest</artifactId>
  </dependency>
  ```

- **Gradle**:
  ```gradle
  implementation 'org.springframework.boot:spring-boot-starter-data-rest'
  ```

This starter brings in `spring-data-rest-core` along with other necessary components. For non-Spring Boot projects, you can include `spring-data-rest-core` directly, but the Spring Boot starter is recommended for simplicity.

---

### 2. Define Your Entities
Create your domain model by defining entity classes using a persistence technology like JPA (Java Persistence API). For example:

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

    // Constructors
    public User() {}
    public User(String name) {
        this.name = name;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

This `User` entity represents a simple table in your database with an `id` and `name`.

---

### 3. Create Repository Interfaces
Define a repository interface for your entity by extending one of Spring Data’s repository interfaces, such as `JpaRepository`. For example:

```java
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
```

By extending `JpaRepository`, you get basic CRUD (Create, Read, Update, Delete) operations for free. Spring Data REST will automatically expose this repository as a RESTful endpoint.

---

### 4. Run Your Application
With the dependency added and your entities and repositories defined, start your Spring Boot application. Spring Data REST will automatically generate REST endpoints based on your repository. For the `UserRepository` above, you can access:

- **GET /users**: Retrieve a list of all users.
- **GET /users/{id}**: Retrieve a specific user by ID.
- **POST /users**: Create a new user (with a JSON payload, e.g., `{"name": "Alice"}`).
- **PUT /users/{id}**: Update an existing user.
- **DELETE /users/{id}**: Delete a user.

For example, if your application runs on `localhost:8080`, you can use a tool like `curl` or a browser to test:

```bash
curl http://localhost:8080/users
```

The response will include HATEOAS links, allowing clients to navigate related resources dynamically.

---

### 5. (Optional) Customize the REST Endpoints
You can customize how your repositories are exposed using annotations or configuration:

- **Change the Endpoint Path**:
  Use the `@RepositoryRestResource` annotation to specify a custom path:
  ```java
  import org.springframework.data.rest.core.annotation.RepositoryRestResource;

  @RepositoryRestResource(path = "people")
  public interface UserRepository extends JpaRepository<User, Long> {
  }
  ```
  Now, the endpoint will be `/people` instead of `/users`.

- **Configure Global Settings**:
  Customize the base path or other settings by implementing `RepositoryRestConfigurer`:
  ```java
  import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.data.rest.core.config.RepositoryRestConfiguration;

  @Configuration
  public class RestConfig implements RepositoryRestConfigurer {
      @Override
      public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config) {
          config.setBasePath("/api"); // All endpoints will start with /api
      }
  }
  ```
  With this, your users would be accessible at `/api/users`.

---

### Key Features of Spring Data REST
- **HATEOAS Support**: Responses include hypermedia links to related resources.
- **Pagination and Sorting**: Use query parameters like `?page=0&size=10&sort=name,asc` to paginate and sort results.
- **Filtering**: Add custom query methods to your repository (e.g., `findByName(String name)`) to expose additional endpoints.

---

### Summary
To use `spring-data-rest-core`:
1. Include the Spring Data REST dependency (e.g., `spring-boot-starter-data-rest` for Spring Boot).
2. Define your entities with appropriate annotations (e.g., `@Entity` for JPA).
3. Create repository interfaces extending Spring Data interfaces (e.g., `JpaRepository`).
4. Run your application to access automatically generated REST endpoints.
5. Optionally, customize endpoint paths or behavior as needed.

This approach allows you to quickly build a RESTful API with minimal code, leveraging the core functionality of Spring Data REST.
