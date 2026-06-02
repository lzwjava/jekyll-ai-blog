---
audio: false
generated: true
lang: en
layout: post
title: Java API for RESTful Web Services
translated: false
type: note
---

To use `javax.ws.rs`, the Java API for RESTful web services (commonly referred to as JAX-RS), you need to follow a series of steps to set up your project, define RESTful resources, configure your application, and deploy it. JAX-RS allows you to create web services that adhere to the REST architectural style, using annotations to define endpoints and handle HTTP requests. Below is a comprehensive guide to get you started:

---

### **1. Set Up Your Project**
To use `javax.ws.rs`, you need to include the JAX-RS API and an implementation (since `javax.ws.rs` is a specification, not a runtime). A popular implementation is Jersey. If you're using Maven, add the necessary dependencies to your `pom.xml`:

#### **Dependencies**
```xml
<!-- JAX-RS API -->
<dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>2.1.1</version>
</dependency>

<!-- Jersey Implementation (includes core dependencies) -->
<dependency>
    <groupId>org.glassfish.jersey.bundles</groupId>
    <artifactId>jaxrs-ri</artifactId>
    <version>2.34</version>
</dependency>

<!-- Optional: JSON support with Jackson -->
<dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
    <version>2.34</version>
</dependency>
```

- The `javax.ws.rs-api` provides the core JAX-RS annotations and classes.
- The `jaxrs-ri` bundle includes the Jersey implementation and its dependencies.
- The `jersey-media-json-jackson` module (optional) adds support for JSON serialization/deserialization.

Ensure your project is set up with a servlet container (e.g., Tomcat) or a Java EE server, as JAX-RS applications typically run in such environments. Alternatively, you can run standalone with a lightweight server like Grizzly (more on that later).

---

### **2. Create a RESTful Resource**
RESTful services in JAX-RS are defined using resource classes annotated with `@Path` and HTTP method annotations like `@GET`, `@POST`, etc. Here’s an example of a simple resource:

#### **Example: HelloResource.java**
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

- **`@Path("/hello")`**: Specifies the URI path for this resource (e.g., `http://localhost:8080/api/hello`).
- **`@GET`**: Indicates this method handles HTTP GET requests.
- **`@Produces(MediaType.TEXT_PLAIN)`**: Specifies that the response will be plain text.

When a GET request is made to `/hello`, this method returns `"Hello, World!"`.

---

### **3. Configure the JAX-RS Application**
You need to tell the JAX-RS runtime which resources to include. This can be done by creating an application configuration class that extends `javax.ws.rs.core.Application`.

#### **Example: MyApplication.java**
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

- **`@ApplicationPath("/api")`**: Defines the base URI path for all resources (e.g., `/api/hello`).
- **`getClasses()`**: Returns the set of resource classes to be included in the application.

With modern servlet containers (Servlet 3.0+), this annotation-based configuration is often sufficient, and you may not need a `web.xml` file.

---

### **4. Handle Different HTTP Methods and Parameters**
JAX-RS provides annotations to handle various HTTP methods, media types, and parameters.

#### **Example: Handling POST Requests**
```java
import javax.ws.rs.POST;
import javax.ws.rs.Consumes;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@POST
@Consumes(MediaType.APPLICATION_JSON)
public Response createItem(MyItem item) {
    // Logic to process the item
    return Response.status(Response.Status.CREATED).build();
}
```

- **`@POST`**: Handles HTTP POST requests.
- **`@Consumes(MediaType.APPLICATION_JSON)`**: Expects JSON input, which is deserialized into a `MyItem` object.
- **`Response`**: Returns a 201 Created status.

#### **Example: Path Parameters**
```java
import javax.ws.rs.PathParam;
import javax.ws.rs.Path;

@GET
@Path("/{id}")
@Produces(MediaType.APPLICATION_JSON)
public MyItem getItem(@PathParam("id") String id) {
    // Logic to retrieve item by ID
    return new MyItem(id);
}
```

- **`@Path("/{id}")`**: Defines a path parameter (e.g., `/hello/123`).
- **`@PathParam("id")`**: Injects the `id` value from the URI.

#### **Example: Query Parameters**
```java
import javax.ws.rs.QueryParam;

@GET
@Produces(MediaType.APPLICATION_JSON)
public List<MyItem> getItems(@QueryParam("category") String category) {
    // Logic to filter items by category
    return itemList;
}
```

- **`@QueryParam("category")`**: Retrieves the `category` value from the query string (e.g., `/hello?category=books`).

---

### **5. Deploy the Application**
You can deploy your JAX-RS application in a servlet container like Tomcat:

1. Package your project as a WAR file (e.g., using `mvn package`).
2. Deploy the WAR file to your container.
3. Access your service at the configured URI (e.g., `http://localhost:8080/your-app/api/hello`).

Alternatively, for development or standalone use, you can run the application programmatically using Jersey with Grizzly:

#### **Example: Standalone Main**
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

This starts an HTTP server without a full servlet container.

---

### **6. Additional Features**
- **Exception Handling**: Use `ExceptionMapper` to handle exceptions gracefully.
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
- **Dependency Injection**: Use `@Context` to inject objects like `UriInfo` or rely on the implementation’s DI framework (e.g., HK2 in Jersey).
- **Testing**: Use tools like Postman or the Jersey Test Framework to test your endpoints.

---

### **Summary**
To use `javax.ws.rs`, include the JAX-RS API and an implementation like Jersey in your project, define resource classes with annotations for paths and HTTP methods, configure the application (via an `Application` subclass or `web.xml`), and deploy it to a servlet container or run it standalone. This enables you to build RESTful web services efficiently with Java.
