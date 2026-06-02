---
audio: false
generated: true
lang: zh
layout: post
title: RESTful Web服务Java API
translated: true
type: note
---

要使用 `javax.ws.rs`（即 RESTful Web 服务的 Java API，通常称为 JAX-RS），您需要按照一系列步骤来设置项目、定义 RESTful 资源、配置应用程序并部署它。JAX-RS 允许您创建符合 REST 架构风格的 Web 服务，使用注解来定义端点和处理 HTTP 请求。以下是一个全面的入门指南：

---

### **1. 设置项目**
要使用 `javax.ws.rs`，您需要包含 JAX-RS API 和一个实现（因为 `javax.ws.rs` 是一个规范，而非运行时）。一个流行的实现是 Jersey。如果您使用 Maven，请将必要的依赖项添加到您的 `pom.xml` 中：

#### **依赖项**
```xml
<!-- JAX-RS API -->
<dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>2.1.1</version>
</dependency>

<!-- Jersey 实现（包含核心依赖项） -->
<dependency>
    <groupId>org.glassfish.jersey.bundles</groupId>
    <artifactId>jaxrs-ri</artifactId>
    <version>2.34</version>
</dependency>

<!-- 可选：使用 Jackson 的 JSON 支持 -->
<dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
    <version>2.34</version>
</dependency>
```

- `javax.ws.rs-api` 提供了核心的 JAX-RS 注解和类。
- `jaxrs-ri` 包包含了 Jersey 实现及其依赖项。
- `jersey-media-json-jackson` 模块（可选）添加了对 JSON 序列化/反序列化的支持。

确保您的项目已设置为使用 servlet 容器（例如 Tomcat）或 Java EE 服务器，因为 JAX-RS 应用程序通常在此类环境中运行。或者，您可以使用轻量级服务器（如 Grizzly）独立运行（稍后会详细介绍）。

---

### **2. 创建 RESTful 资源**
JAX-RS 中的 RESTful 服务是使用带有 `@Path` 注解的资源类以及 HTTP 方法注解（如 `@GET`、`@POST` 等）来定义的。以下是一个简单资源的示例：

#### **示例：HelloResource.java**
```java
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/hello")
public class HelloResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String sayHello() {
        return "Hello, World!";
    }
}
```

- **`@Path("/hello")`**：指定此资源的 URI 路径（例如 `http://localhost:8080/api/hello`）。
- **`@GET`**：表示此方法处理 HTTP GET 请求。
- **`@Produces(MediaType.TEXT_PLAIN)`**：指定响应将为纯文本。

当向 `/hello` 发出 GET 请求时，此方法返回 `"Hello, World!"`。

---

### **3. 配置 JAX-RS 应用程序**
您需要告诉 JAX-RS 运行时包含哪些资源。这可以通过创建一个扩展 `javax.ws.rs.core.Application` 的应用程序配置类来完成。

#### **示例：MyApplication.java**
```java
import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;
import java.util.HashSet;
import java.util.Set;

@ApplicationPath("/api")
public class MyApplication extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> classes = new HashSet<>();
        classes.add(HelloResource.class);
        return classes;
    }
}
```

- **`@ApplicationPath("/api")`**：定义所有资源的基础 URI 路径（例如 `/api/hello`）。
- **`getClasses()`**：返回要包含在应用程序中的资源类的集合。

对于现代的 servlet 容器（Servlet 3.0+），这种基于注解的配置通常就足够了，您可能不需要 `web.xml` 文件。

---

### **4. 处理不同的 HTTP 方法和参数**
JAX-RS 提供了注解来处理各种 HTTP 方法、媒体类型和参数。

#### **示例：处理 POST 请求**
```java
import javax.ws.rs.POST;
import javax.ws.rs.Consumes;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@POST
@Consumes(MediaType.APPLICATION_JSON)
public Response createItem(MyItem item) {
    // 处理项目的逻辑
    return Response.status(Response.Status.CREATED).build();
}
```

- **`@POST`**：处理 HTTP POST 请求。
- **`@Consumes(MediaType.APPLICATION_JSON)`**：期望 JSON 输入，该输入将被反序列化为 `MyItem` 对象。
- **`Response`**：返回 201 Created 状态。

#### **示例：路径参数**
```java
import javax.ws.rs.PathParam;
import javax.ws.rs.Path;

@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)
public MyItem getItem(@PathParam("id") String id) {
    // 通过 ID 检索项目的逻辑
    return new MyItem(id);
}
```

- **`@Path("/{id}")`**：定义一个路径参数（例如 `/hello/123`）。
- **`@PathParam("id")`**：从 URI 中注入 `id` 值。

#### **示例：查询参数**
```java
import javax.ws.rs.QueryParam;

@GET
@Produces(MediaType.APPLICATION_JSON)
public List<MyItem> getItems(@QueryParam("category") String category) {
    // 按类别筛选项目的逻辑
    return itemList;
}
```

- **`@QueryParam("category")`**：从查询字符串中检索 `category` 值（例如 `/hello?category=books`）。

---

### **5. 部署应用程序**
您可以将 JAX-RS 应用程序部署到像 Tomcat 这样的 servlet 容器中：

1. 将您的项目打包为 WAR 文件（例如使用 `mvn package`）。
2. 将 WAR 文件部署到您的容器中。
3. 在配置的 URI（例如 `http://localhost:8080/your-app/api/hello`）访问您的服务。

或者，为了开发或独立使用，您可以使用 Jersey 和 Grizzly 以编程方式运行应用程序：

#### **示例：独立主类**
```java
import org.glassfish.jersey.grizzly2.httpserver.GrizzlyHttpServerFactory;
import org.glassfish.jersey.server.ResourceConfig;
import java.net.URI;

public class Main {
    public static void main(String[] args) {
        URI baseUri = URI.create("http://localhost:8080/api/");
        ResourceConfig config = new ResourceConfig(HelloResource.class);
        GrizzlyHttpServerFactory.createHttpServer(baseUri, config);
        System.out.println("Server running at " + baseUri);
    }
}
```

这将启动一个 HTTP 服务器，而无需完整的 servlet 容器。

---

### **6. 附加功能**
- **异常处理**：使用 `ExceptionMapper` 优雅地处理异常。
  ```java
  import javax.ws.rs.NotFoundException;
  import javax.ws.rs.core.Response;
  import javax.ws.rs.ext.ExceptionMapper;
  import javax.ws.rs.ext.Provider;

  @Provider
  public class NotFoundExceptionMapper implements ExceptionMapper<NotFoundException> {
      @Override
      public Response toResponse(NotFoundException exception) {
          return Response.status(Response.Status.NOT_FOUND).build();
      }
  }
  ```
- **依赖注入**：使用 `@Context` 注入对象（如 `UriInfo`），或依赖实现的 DI 框架（例如 Jersey 中的 HK2）。
- **测试**：使用 Postman 或 Jersey 测试框架等工具来测试您的端点。

---

### **总结**
要使用 `javax.ws.rs`，请在项目中包含 JAX-RS API 和一个实现（如 Jersey），使用注解定义路径和 HTTP 方法的资源类，配置应用程序（通过 `Application` 子类或 `web.xml`），并将其部署到 servlet 容器中或独立运行。这使您能够使用 Java 高效地构建 RESTful Web 服务。
