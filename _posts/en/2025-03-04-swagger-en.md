---
audio: false
generated: true
lang: en
layout: post
title: Swagger Annotations
translated: false
type: note
---

To use the `swagger-annotations` package in your Java project, particularly for documenting a REST API built with Spring Boot, follow these steps. This guide assumes you are using Swagger 2.0, which is commonly integrated with the `springfox` library. The `swagger-annotations` package provides annotations to add metadata to your API endpoints, enabling automatic generation of API documentation.

---

### Step 1: Add the Required Dependencies

You need to include the `swagger-annotations` package and a Swagger integration library (e.g., `springfox`) in your project. If you're using Maven, add the following dependencies to your `pom.xml`:

```xml
<!-- Swagger Annotations -->
<dependency>
    <groupId>io.swagger</groupId>
    <artifactId>swagger-annotations</artifactId>
    <version>1.6.2</version>
</dependency>

<!-- Springfox Swagger 2 for Swagger Integration -->
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>

<!-- Springfox Swagger UI for Interactive Documentation -->
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>
```

- **`io.swagger:swagger-annotations`**: Provides the annotations for Swagger 2.0.
- **`springfox-swagger2`**: Integrates Swagger with Spring Boot and processes the annotations.
- **`springfox-swagger-ui`**: Adds a web interface to view the generated documentation.

> **Note**: Check for the latest versions on [Maven Repository](https://mvnrepository.com/) as these versions (1.6.2 for `swagger-annotations` and 2.9.2 for `springfox`) may have updates.

---

### Step 2: Configure Swagger in Your Application

To enable Swagger and allow it to scan your API for annotations, create a configuration class with a `Docket` bean. Add this to your Spring Boot application:

```java
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableSwagger2
public class SwaggerConfig {
    @Bean
    public Docket api() {
        return new Docket(DocumentationType.SWAGGER_2)
                .select()
                .apis(RequestHandlerSelectors.any()) // Scan all controllers
                .paths(PathSelectors.any())          // Include all paths
                .build();
    }
}
```

- **`@EnableSwagger2`**: Activates Swagger 2.0 support.
- **`Docket`**: Configures which endpoints to document. The above setup scans all controllers and paths, but you can customize it (e.g., `RequestHandlerSelectors.basePackage("com.example.controllers")`) to limit the scope.

---

### Step 3: Use Swagger Annotations in Your Code

The `swagger-annotations` package provides annotations to describe your API. Apply these to your controller classes, methods, parameters, and models. Below are common annotations with examples:

#### Annotating a Controller

Use `@Api` to describe the controller:

```java
import io.swagger.annotations.Api;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Api(value = "User Controller", description = "Operations pertaining to users")
@RestController
@RequestMapping("/users")
public class UserController {
    // Methods go here
}
```

- **`value`**: A short name for the API.
- **`description`**: A brief explanation of what the controller does.

#### Annotating API Operations

Use `@ApiOperation` to describe individual endpoints:

```java
import io.swagger.annotations.ApiOperation;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@ApiOperation(value = "Get a user by ID", response = User.class)
@GetMapping("/{id}")
public ResponseEntity<User> getUserById(@PathVariable Long id) {
    // Implementation
    return ResponseEntity.ok(new User(id, "John Doe"));
}
```

- **`value`**: A summary of the operation.
- **`response`**: The expected return type.

#### Describing Parameters

Use `@ApiParam` for method parameters:

```java
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@ApiOperation(value = "Create a new user")
@PostMapping
public ResponseEntity<User> createUser(
        @ApiParam(value = "User object to be created", required = true)
        @RequestBody User user) {
    // Implementation
    return ResponseEntity.ok(user);
}
```

- **`value`**: Describes the parameter.
- **`required`**: Indicates if the parameter is mandatory.

#### Specifying Responses

Use `@ApiResponses` and `@ApiResponse` to document possible HTTP responses:

```java
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiResponses;
import io.swagger.annotations.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;

@ApiOperation(value = "Delete a user")
@ApiResponses(value = {
    @ApiResponse(code = 200, message = "User deleted successfully"),
    @ApiResponse(code = 404, message = "User not found")
})
@DeleteMapping("/{id}")
public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
    // Implementation
    return ResponseEntity.ok().build();
}
```

- **`code`**: HTTP status code.
- **`message`**: Description of the response.

#### Describing Models

For data transfer objects (DTOs), use `@ApiModel` and `@ApiModelProperty`:

```java
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

@ApiModel(description = "User data transfer object")
public class User {
    @ApiModelProperty(notes = "The user's unique identifier", example = "1")
    private Long id;

    @ApiModelProperty(notes = "The user's name", example = "John Doe")
    private String name;

    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public User(Long id, String name) {
        this.id = id;
        this.name = name;
    }
}
```

- **`@ApiModel`**: Describes the model.
- **`@ApiModelProperty`**: Details each field, with optional examples.

---

### Step 4: Run and Access the Documentation

1. Start your Spring Boot application.
2. Open a browser and navigate to:
   **<http://localhost:8080/swagger-ui.html>**
   This URL displays the Swagger UI, an interactive interface showing your API documentation based on the annotations.

---

### Summary of How to Use `swagger-annotations`

1. **Add Dependencies**: Include `swagger-annotations` and `springfox` in your `pom.xml`.
2. **Configure Swagger**: Set up a `Docket` bean to enable Swagger scanning.
3. **Annotate Your Code**:
   - `@Api` for controllers.
   - `@ApiOperation` for methods.
   - `@ApiParam` for parameters.
   - `@ApiResponses` and `@ApiResponse` for response details.
   - `@ApiModel` and `@ApiModelProperty` for DTOs.
4. **View Documentation**: Access the Swagger UI at `/swagger-ui.html`.

---

### Additional Notes

- **Swagger 2.0 vs. OpenAPI 3.0**: This guide uses Swagger 2.0 with `io.swagger:swagger-annotations`. For OpenAPI 3.0, use `io.swagger.core.v3:swagger-annotations` and a library like `springdoc-openapi`, which changes some annotation names (e.g., `@Tag` instead of `@Api`).
- **Customization**: Adjust the `Docket` configuration to filter specific packages or paths for more focused documentation.
- **Quality**: Provide clear, detailed descriptions in annotations to improve the generated documentation’s usefulness.

By following these steps, you can effectively use the `swagger-annotations` package to document your REST API, making it easier for developers and consumers to understand and interact with your endpoints.
