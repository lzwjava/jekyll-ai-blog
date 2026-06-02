---
audio: false
generated: true
lang: en
layout: post
title: Spring Boot Exceptions
translated: false
type: note
---

When working with Spring Boot or the broader Spring Framework, developers frequently encounter exceptions due to configuration issues, runtime errors, or improper use of APIs. Below is a list of common exceptions you might face, along with their typical causes and potential resolutions. These exceptions are grouped by category for clarity.

---

### **1. Configuration-Related Exceptions**

- **`org.springframework.beans.factory.BeanCreationException`**:
  - **Cause**: A bean failed to be created due to missing dependencies, misconfiguration, or instantiation errors.
  - **Example**: Missing `@Component`, `@Service`, or `@Autowired` dependency not found.
  - **Resolution**: Check bean definitions, ensure dependencies are available, and verify annotations.

- **`org.springframework.beans.factory.NoSuchBeanDefinitionException`**:
  - **Cause**: Spring cannot find a bean of the requested type or name in the application context.
  - **Example**: Attempting to `@Autowired` a bean that isn’t defined or scanned.
  - **Resolution**: Ensure the bean is annotated (e.g., `@Component`) and within the component scan path.

- **`org.springframework.context.ApplicationContextException`**:
  - **Cause**: General failure to initialize the Spring application context.
  - **Example**: Invalid configuration in `application.properties` or a syntax error in a `@Configuration` class.
  - **Resolution**: Review stack trace for root cause (e.g., invalid property or missing resource).

- **`org.springframework.beans.factory.UnsatisfiedDependencyException`**:
  - **Cause**: A dependency required by a bean cannot be satisfied.
  - **Example**: Circular dependency or missing implementation for an interface.
  - **Resolution**: Break circular dependencies (e.g., use `@Lazy`) or provide the missing dependency.

---

### **2. Web and REST-Related Exceptions**

- **`org.springframework.web.bind.MissingServletRequestParameterException`**:
  - **Cause**: A required request parameter is missing in an HTTP request.
  - **Example**: `@RequestParam("id")` is specified, but the client didn’t send `id`.
  - **Resolution**: Make the parameter optional (`required = false`) or ensure the client includes it.

- **`org.springframework.http.converter.HttpMessageNotReadableException`**:
  - **Cause**: The request body cannot be deserialized (e.g., malformed JSON).
  - **Example**: Sending invalid JSON to a `@RequestBody` endpoint.
  - **Resolution**: Validate the request payload and ensure it matches the target object structure.

- **`org.springframework.web.method.annotation.MethodArgumentTypeMismatchException`**:
  - **Cause**: A method argument cannot be converted to the expected type.
  - **Example**: Passing a string like `"abc"` to a parameter expecting an `int`.
  - **Resolution**: Validate input or use custom converters.

- **`org.springframework.web.servlet.NoHandlerFoundException`**:
  - **Cause**: No controller mapping exists for the requested URL.
  - **Example**: A typo in `@RequestMapping` or missing controller.
  - **Resolution**: Verify endpoint mappings and ensure controllers are scanned.

---

### **3. Data Access (Spring Data/JPA/Hibernate) Exceptions**

- **`org.springframework.dao.DataIntegrityViolationException`**:
  - **Cause**: A database operation violates a constraint (e.g., unique key or foreign key).
  - **Example**: Inserting a duplicate primary key value.
  - **Resolution**: Check data for uniqueness or handle the exception gracefully.

- **`org.springframework.orm.jpa.JpaSystemException`**:
  - **Cause**: General JPA-related runtime error, often wrapping a Hibernate exception.
  - **Example**: Constraint violation or connection issue.
  - **Resolution**: Inspect the nested exception (e.g., `SQLException`) for details.

- **`org.hibernate.LazyInitializationException`**:
  - **Cause**: Attempting to access a lazily-loaded entity outside an active session.
  - **Example**: Accessing a `@OneToMany` relationship after the transaction ends.
  - **Resolution**: Use eager fetching, fetch in the query (e.g., `JOIN FETCH`), or ensure an open session.

- **`org.springframework.dao.InvalidDataAccessApiUsageException`**:
  - **Cause**: Incorrect usage of Spring Data or JDBC APIs.
  - **Example**: Passing a null parameter to a query expecting a value.
  - **Resolution**: Validate query parameters and API usage.

---

### **4. Security-Related Exceptions**

- **`org.springframework.security.access.AccessDeniedException`**:
  - **Cause**: The authenticated user lacks permission for a resource.
  - **Example**: Accessing a secured endpoint without the required role.
  - **Resolution**: Check `@PreAuthorize` or security configuration and adjust roles/authorities.

- **`org.springframework.security.authentication.BadCredentialsException`**:
  - **Cause**: Authentication failed due to incorrect username or password.
  - **Example**: User enters wrong credentials in a login form.
  - **Resolution**: Ensure credentials are correct; customize error handling for user feedback.

- **`org.springframework.security.authentication.DisabledException`**:
  - **Cause**: The user account is disabled.
  - **Example**: A `UserDetails` implementation returns `isEnabled() == false`.
  - **Resolution**: Enable the account or update the user status.

---

### **5. Miscellaneous Runtime Exceptions**

- **`java.lang.IllegalStateException`**:
  - **Cause**: Spring encounters an invalid state during execution.
  - **Example**: Calling a method on a bean that hasn’t been fully initialized.
  - **Resolution**: Check lifecycle methods or bean initialization order.

- **`org.springframework.transaction.TransactionException`**:
  - **Cause**: An issue occurred during transaction management.
  - **Example**: Transaction rollback due to an unhandled exception.
  - **Resolution**: Ensure proper `@Transactional` usage and handle exceptions within the transaction.

- **`java.lang.NullPointerException`**:
  - **Cause**: Attempting to access a null object reference.
  - **Example**: An `@Autowired` dependency wasn’t injected due to misconfiguration.
  - **Resolution**: Add null checks or debug why the dependency is missing.

---

### **6. Spring Boot-Specific Exceptions**

- **`org.springframework.boot.context.embedded.EmbeddedServletContainerException`** (older versions) or **`org.springframework.boot.web.server.WebServerException`** (newer versions):
  - **Cause**: Failure to start the embedded web server (e.g., Tomcat, Jetty).
  - **Example**: Port already in use (e.g., `8080`).
  - **Resolution**: Change the port in `application.properties` (`server.port=8081`) or free the occupied port.

- **`org.springframework.boot.autoconfigure.jdbc.DataSourceProperties$DataSourceBeanCreationException`**:
  - **Cause**: Failure to configure the datasource.
  - **Example**: Missing or incorrect `spring.datasource.url/username/password`.
  - **Resolution**: Verify datasource properties in `application.properties` or `application.yml`.

- **`org.springframework.boot.SpringApplication - Application run failed`**:
  - **Cause**: Generic failure during Spring Boot startup.
  - **Example**: Misconfiguration, missing beans, or dependency conflicts.
  - **Resolution**: Check the full stack trace for the root cause.

---

### **Best Practices to Handle Exceptions**

1. **Global Exception Handling**:
   - Use `@ControllerAdvice` with `@ExceptionHandler` to catch and handle exceptions consistently across your application.
   - Example:
     ```java
     @ControllerAdvice
     public class GlobalExceptionHandler {
         @ExceptionHandler(DataIntegrityViolationException.class)
         public ResponseEntity<String> handleDataIntegrityViolation() {
             return ResponseEntity.status(HttpStatus.CONFLICT).body("Data integrity violation occurred.");
         }
     }
     ```

2. **Logging**:
   - Log exceptions with a framework like SLF4J/Logback to aid debugging.

3. **Custom Exceptions**:
   - Define application-specific exceptions and map them to appropriate HTTP statuses.

4. **Validation**:
   - Use `@Valid` and Bean Validation (e.g., `@NotNull`) to catch errors early and avoid runtime exceptions.

5. **Debugging**:
   - Enable detailed logging (`logging.level.org.springframework=DEBUG`) in `application.properties` to trace issues.

---

### **Conclusion**

These exceptions are among the most common you’ll encounter when using Spring Boot or the Spring Framework. Understanding their causes and resolutions can significantly speed up development and debugging. If you’re facing a specific exception and need a deeper dive, feel free to share the details, and I’ll provide a tailored explanation!
