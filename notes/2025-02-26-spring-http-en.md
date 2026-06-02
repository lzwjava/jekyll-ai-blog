---
audio: false
generated: true
lang: en
layout: post
title: Spring HTTP Clients
translated: false
type: note
---

To answer the query "how to use FeignClient, or Spring RestClient, or Spring WebClient," I'll explain how each of these Spring tools can be used to make HTTP requests, focusing on their setup and basic usage. These are all part of the Spring ecosystem for interacting with RESTful services, but they serve different purposes depending on your application's needs. Below, I’ll provide a clear, step-by-step guide for each, along with simple examples.

---

### **1. Using FeignClient**
FeignClient is a declarative REST client provided by Spring Cloud. It allows you to define HTTP clients as interfaces with annotations, making it particularly useful in microservices architectures where you need to call other services.

#### **Steps to Use FeignClient**
1. **Add Dependencies**: Include Spring Cloud dependencies in your project. If you're using Maven, add the Spring Cloud starter for Feign to your `pom.xml`:
   ```xml
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-openfeign</artifactId>
   </dependency>
   ```
   Ensure you also have a dependency management block for Spring Cloud, specifying a compatible version.

2. **Enable Feign Clients**: Annotate your main application class or a configuration class with `@EnableFeignClients` to activate Feign support:
   ```java
   import org.springframework.boot.SpringApplication;
   import org.springframework.boot.autoconfigure.SpringBootApplication;
   import org.springframework.cloud.openfeign.EnableFeignClients;

   @SpringBootApplication
   @EnableFeignClients
   public class MyApplication {
       public static void main(String[] args) {
           SpringApplication.run(MyApplication.class, args);
       }
   }
   ```

3. **Define the FeignClient Interface**: Create an interface annotated with `@FeignClient`, specifying the service name or URL, and define methods corresponding to the REST endpoints:
   ```java
   import org.springframework.cloud.openfeign.FeignClient;
   import org.springframework.web.bind.annotation.GetMapping;
   import java.util.List;

   @FeignClient(name = "user-service", url = "http://localhost:8080")
   public interface UserClient {
       @GetMapping("/users")
       List<User> getUsers();
   }
   ```
   Here, `name` is a logical name for the client, and `url` is the base URL of the target service. The `@GetMapping` annotation maps to the `/users` endpoint.

4. **Inject and Use the Client**: Autowire the interface in your service or controller and call its methods as if they were local:
   ```java
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;
   import java.util.List;

   @Service
   public class UserService {
       @Autowired
       private UserClient userClient;

       public List<User> fetchUsers() {
           return userClient.getUsers();
       }
   }
   ```

#### **Key Points**
- FeignClient is synchronous by default.
- It’s ideal for microservices with service discovery (e.g., Eureka) when you omit the `url` and let Spring Cloud resolve it.
- Error handling can be added with fallbacks or circuit breakers (e.g., Hystrix or Resilience4j).

---

### **2. Using Spring RestClient**
Spring RestClient is a synchronous HTTP client introduced in Spring Framework 6.1 as a modern alternative to the deprecated `RestTemplate`. It provides a fluent API for building and executing requests.

#### **Steps to Use RestClient**
1. **Dependencies**: RestClient is included in `spring-web`, which is part of Spring Boot’s `spring-boot-starter-web`. No additional dependencies are typically needed:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-web</artifactId>
   </dependency>
   ```

2. **Create a RestClient Instance**: Instantiate `RestClient` using its static `create()` method or customize it with a builder:
   ```java
   import org.springframework.web.client.RestClient;

   RestClient restClient = RestClient.create();
   ```
   For custom configurations (e.g., timeouts), use `RestClient.builder()`.

3. **Build and Execute a Request**: Use the fluent API to specify the HTTP method, URI, headers, and body, then retrieve the response:
   ```java
   import org.springframework.http.MediaType;
   import org.springframework.web.client.RestClient;
   import java.util.List;

   public class UserService {
       private final RestClient restClient;

       public UserService() {
           this.restClient = RestClient.create();
       }

       public List<User> fetchUsers() {
           return restClient.get()
               .uri("http://localhost:8080/users")
               .accept(MediaType.APPLICATION_JSON)
               .retrieve()
               .body(new ParameterizedTypeReference<List<User>>() {});
       }
   }
   ```
   - `get()` specifies the HTTP method.
   - `uri()` sets the endpoint.
   - `accept()` sets the expected content type.
   - `retrieve()` executes the request, and `body()` extracts the response, using `ParameterizedTypeReference` for generic types like lists.

4. **Handle the Response**: The response is returned directly since RestClient is synchronous. For more control (e.g., status codes), use `toEntity()`:
   ```java
   import org.springframework.http.ResponseEntity;

   ResponseEntity<List<User>> response = restClient.get()
       .uri("http://localhost:8080/users")
       .accept(MediaType.APPLICATION_JSON)
       .retrieve()
       .toEntity(new ParameterizedTypeReference<List<User>>() {});
   List<User> users = response.getBody();
   ```

#### **Key Points**
- RestClient is synchronous, making it suitable for traditional, blocking applications.
- It throws exceptions (e.g., `RestClientException`) on HTTP errors, which you can catch and handle.
- It’s a replacement for `RestTemplate` with a more intuitive API.

---

### **3. Using Spring WebClient**
Spring WebClient is a reactive, non-blocking HTTP client introduced in Spring WebFlux. It’s designed for asynchronous operations and integrates with reactive streams (Mono and Flux).

#### **Steps to Use WebClient**
1. **Add Dependencies**: Include the WebFlux dependency in your project:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-webflux</artifactId>
   </dependency>
   ```

2. **Create a WebClient Instance**: Instantiate `WebClient` with a base URL or default settings:
   ```java
   import org.springframework.web.reactive.function.client.WebClient;

   WebClient webClient = WebClient.create("http://localhost:8080");
   ```
   Use `WebClient.builder()` for custom configurations (e.g., codecs, filters).

3. **Build and Execute a Request**: Use the fluent API to construct the request and retrieve a reactive response:
   ```java
   import org.springframework.http.MediaType;
   import org.springframework.web.reactive.function.client.WebClient;
   import reactor.core.publisher.Mono;
   import java.util.List;

   public class UserService {
       private final WebClient webClient;

       public UserService(WebClient webClient) {
           this.webClient = webClient;
       }

       public Mono<List<User>> fetchUsers() {
           return webClient.get()
               .uri("/users")
               .accept(MediaType.APPLICATION_JSON)
               .retrieve()
               .bodyToFlux(User.class)
               .collectList();
       }
   }
   ```
   - `bodyToFlux(User.class)` handles a stream of `User` objects.
   - `collectList()` converts the `Flux<User>` to a `Mono<List<User>>`.

4. **Subscribe to the Response**: Since WebClient is reactive, you must subscribe to the `Mono` or `Flux` to trigger the request:
   ```java
   Mono<List<User>> usersMono = fetchUsers();
   usersMono.subscribe(users -> System.out.println(users));
   ```
   Alternatively, chain it in a reactive pipeline or block (not recommended in reactive contexts):
   ```java
   List<User> users = fetchUsers().block();
   ```

#### **Key Points**
- WebClient is non-blocking and ideal for reactive applications built with Spring WebFlux.
- Use `Mono` for single-valued responses and `Flux` for multi-valued responses.
- Error handling can be done with operators like `onErrorResume()` or `retry()`.

---

### **Comparison and When to Use Each**
- **FeignClient**: Use for declarative, interface-based clients in microservices setups. It’s synchronous and simplifies service-to-service calls.
- **RestClient**: Use for synchronous HTTP requests in traditional, blocking Spring applications. It’s a modern alternative to `RestTemplate`.
- **WebClient**: Use for reactive, non-blocking HTTP requests in WebFlux-based applications or when handling high concurrency.

---

### **Example: Calling a POST Endpoint**
Suppose you need to create a user by calling `POST /users` with a `User` object.

#### **FeignClient**
```java
@FeignClient(name = "user-service", url = "http://localhost:8080")
public interface UserClient {
    @PostMapping("/users")
    User createUser(@RequestBody User user);
}

@Service
public class UserService {
    @Autowired
    private UserClient userClient;

    public User createUser(User user) {
        return userClient.createUser(user);
    }
}
```

#### **RestClient**
```java
@Service
public class UserService {
    private final RestClient restClient = RestClient.create();

    public User createUser(User user) {
        return restClient.post()
            .uri("http://localhost:8080/users")
            .contentType(MediaType.APPLICATION_JSON)
            .body(user)
            .retrieve()
            .body(User.class);
    }
}
```

#### **WebClient**
```java
@Service
public class UserService {
    private final WebClient webClient;

    public UserService(WebClient webClient) {
        this.webClient = WebClient.create("http://localhost:8080");
    }

    public Mono<User> createUser(User user) {
        return webClient.post()
            .uri("/users")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(user)
            .retrieve()
            .bodyToMono(User.class);
    }
}
```

---

### **Conclusion**
- **FeignClient**: Define an interface, enable it, and use it like a local bean.
- **RestClient**: Build requests fluently and get responses synchronously.
- **WebClient**: Build requests fluently, retrieve reactive streams, and process them asynchronously.

Choose based on your application’s architecture: FeignClient for microservices, RestClient for blocking apps, and WebClient for reactive apps. Each follows a straightforward setup and usage pattern as shown above.
