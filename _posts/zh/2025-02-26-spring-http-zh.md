---
audio: false
generated: true
lang: zh
layout: post
title: Spring HTTP客户端
translated: true
type: note
---

针对“如何使用FeignClient、Spring RestClient或Spring WebClient”的问题，我将分别解释这些Spring生态中用于HTTP请求调用的工具，重点说明它们的配置方法和基础使用。这些组件虽然都用于与RESTful服务交互，但各自适用于不同的应用场景。下面我将逐步说明每种工具的使用方式，并附上简单示例。

---

### **1. 使用FeignClient**
FeignClient是Spring Cloud提供的声明式REST客户端。它允许通过注解定义HTTP客户端接口，特别适用于微服务架构中需要调用其他服务的场景。

#### **使用步骤**
1. **添加依赖**：在项目中引入Spring Cloud依赖。若使用Maven，请在`pom.xml`中添加Feign启动器：
   ```xml
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-openfeign</artifactId>
   </dependency>
   ```
   请确保在依赖管理模块中指定了兼容的Spring Cloud版本。

2. **启用Feign客户端**：在主应用类或配置类上添加`@EnableFeignClients`注解以激活Feign功能：
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

3. **定义FeignClient接口**：创建带有`@FeignClient`注解的接口，指定服务名称或URL，并定义与REST端点对应的方法：
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
   其中`name`为客户端逻辑名称，`url`为目标服务的基础地址。`@GetMapping`注解映射到`/users`端点。

4. **注入并使用客户端**：在服务类或控制器中自动注入接口，像调用本地方法一样使用：
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

#### **核心特点**
- FeignClient默认采用同步调用
- 适用于结合服务发现（如Eureka）的微服务架构（可省略`url`由Spring Cloud自动解析）
- 可通过fallback或熔断器（如Hystrix、Resilience4j）实现错误处理

---

### **2. 使用Spring RestClient**
Spring RestClient是Spring Framework 6.1引入的同步HTTP客户端，作为已弃用的`RestTemplate`的现代替代方案，提供流畅的API用于构建和执行请求。

#### **使用步骤**
1. **依赖配置**：RestClient包含在`spring-web`模块中，Spring Boot项目通过`spring-boot-starter-web`依赖即可引入：
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-web</artifactId>
   </dependency>
   ```

2. **创建RestClient实例**：通过静态方法`create()`创建实例，或使用构建器进行定制：
   ```java
   import org.springframework.web.client.RestClient;

   RestClient restClient = RestClient.create();
   ```
   如需自定义配置（如超时设置），可使用`RestClient.builder()`

3. **构建并执行请求**：通过流式API指定HTTP方法、URI、请求头和请求体，然后获取响应：
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
   - `get()`指定HTTP方法
   - `uri()`设置端点地址
   - `accept()`设置期望的内容类型
   - `retrieve()`执行请求，`body()`提取响应，使用`ParameterizedTypeReference`处理泛型类型（如列表）

4. **处理响应**：由于RestClient是同步的，响应会直接返回。如需更精细控制（如状态码），可使用`toEntity()`：
   ```java
   import org.springframework.http.ResponseEntity;

   ResponseEntity<List<User>> response = restClient.get()
       .uri("http://localhost:8080/users")
       .accept(MediaType.APPLICATION_JSON)
       .retrieve()
       .toEntity(new ParameterizedTypeReference<List<User>>() {});
   List<User> users = response.getBody();
   ```

#### **核心特点**
- 适用于传统的阻塞式同步应用
- 遇到HTTP错误时会抛出异常（如`RestClientException`），需捕获处理
- 作为`RestTemplate`的替代方案，提供更直观的API

---

### **3. 使用Spring WebClient**
Spring WebClient是Spring WebFlux提供的响应式非阻塞HTTP客户端，专为异步操作设计，可与响应式流（Mono和Flux）无缝集成。

#### **使用步骤**
1. **添加依赖**：在项目中引入WebFlux依赖：
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-webflux</artifactId>
   </dependency>
   ```

2. **创建WebClient实例**：通过基础URL或默认配置创建实例：
   ```java
   import org.springframework.web.reactive.function.client.WebClient;

   WebClient webClient = WebClient.create("http://localhost:8080");
   ```
   使用`WebClient.builder()`可进行自定义配置（如编解码器、过滤器）

3. **构建并执行请求**：通过流式API构建请求并获取响应式返回：
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
   - `bodyToFlux(User.class)`处理`User`对象流
   - `collectList()`将`Flux<User>`转换为`Mono<List<User>>`

4. **订阅响应**：由于WebClient是响应式的，必须订阅`Mono`或`Flux`才能触发请求：
   ```java
   Mono<List<User>> usersMono = fetchUsers();
   usersMono.subscribe(users -> System.out.println(users));
   ```
   也可在响应式管道中链式处理，或使用阻塞调用（不推荐在响应式上下文中使用）：
   ```java
   List<User> users = fetchUsers().block();
   ```

#### **核心特点**
- 非阻塞设计，适用于基于Spring WebFlux的响应式应用
- 使用`Mono`处理单值响应，`Flux`处理多值响应
- 可通过`onErrorResume()`、`retry()`等操作符实现错误处理

---

### **对比与选用场景**
- **FeignClient**：适用于微服务架构中的声明式接口客户端，同步调用，简化服务间调用
- **RestClient**：适用于传统阻塞式Spring应用的同步HTTP请求，是现代版`RestTemplate`
- **WebClient**：适用于响应式非阻塞HTTP请求，用于WebFlux应用或高并发场景

---

### **示例：调用POST接口**
假设需要通过调用`POST /users`接口创建用户，并传递`User`对象

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

### **总结**
- **FeignClient**：通过接口定义，启用后即可像本地Bean一样使用
- **RestClient**：通过流式API构建请求，同步获取响应
- **WebClient**：通过流式API构建请求，获取响应式流并进行异步处理

请根据应用架构选择：微服务场景用FeignClient，阻塞式应用用RestClient，响应式应用用WebClient。每种工具都遵循上文展示的简明配置和使用模式。
