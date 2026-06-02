---
audio: false
generated: true
lang: en
layout: post
title: Instantiation Exception
translated: false
type: note
---

To fix the `java.lang.InstantiationException` occurring in `LazyDynaBean.java` at line 844 with the error message "Error instantiating property of type," follow these steps. This exception typically arises when the Apache Commons BeanUtils library's `LazyDynaBean` attempts to create an instance of a property’s type but fails because the type cannot be instantiated—most likely because it is an abstract class, an interface, or lacks a public no-argument constructor.

### Understanding the Problem

`LazyDynaBean` is a dynamic bean implementation from the Apache Commons BeanUtils library, designed to lazily initialize properties when they are accessed. The error suggests that at line 844 of `LazyDynaBean.java`, the code attempts to instantiate a property’s type (e.g., using `Class.newInstance()`), but the operation fails, throwing an `InstantiationException`. Common causes include:

- The property’s type is an abstract class or interface (e.g., `java.util.List` instead of `java.util.ArrayList`).
- The type is a concrete class but lacks a public no-arg constructor, which is required by `newInstance()`.

### Steps to Fix the Issue

#### 1. Identify the Problematic Property

- **Examine the Stack Trace**: The full stack trace or error logs should indicate which property `LazyDynaBean` is trying to instantiate when the exception occurs. For example, if the exception is thrown during a call like `dynaBean.get("someProperty")`, then "someProperty" is the culprit.
- **Check the Error Message**: If the complete error message specifies the type (e.g., "Error instantiating property of type java.util.List"), note the type involved.

#### 2. Determine the Property’s Type

- **Inspect the `DynaClass` Configuration**: `LazyDynaBean` relies on a `DynaClass` (often a `LazyDynaClass`) to define its properties and their types. Check how the properties are defined:
  - If you explicitly created a `LazyDynaClass`, look at the code where properties are added, such as `dynaClass.add("propertyName", PropertyType.class)`.
  - If `LazyDynaBean` is created without a predefined `DynaClass` (e.g., `new LazyDynaBean()`), properties are added dynamically, and the type may be inferred from the first value set or default to a problematic type.
- **Debugging Tip**: Add logging or use a debugger to print the type returned by `dynaClass.getDynaProperty("propertyName").getType()` for the offending property.

#### 3. Ensure the Property Type is Instantiable

- **Use a Concrete Class**: If the type is an abstract class or interface (e.g., `List`, `Map`, or a custom interface `MyInterface`), replace it with a concrete implementation that has a public no-arg constructor:
  - For `List`, use `ArrayList.class` instead of `List.class`.
  - For `Map`, use `HashMap.class` instead of `Map.class`.
  - For a custom interface or abstract class, select a concrete subclass (e.g., `MyConcreteClass` implementing `MyInterface`).
- **Example**:

  ```java
  LazyDynaClass dynaClass = new LazyDynaClass();
  dynaClass.add("myList", ArrayList.class); // Concrete class
  LazyDynaBean dynaBean = new LazyDynaBean(dynaClass);
  ```

#### 4. Adjust the Configuration

- **Predefine Properties**: If you control the `DynaClass`, explicitly define properties with concrete types before using the bean:

  ```java
  LazyDynaClass dynaClass = new LazyDynaClass();
  dynaClass.add("myProperty", MyConcreteClass.class);
  LazyDynaBean dynaBean = new LazyDynaBean(dynaClass);
  ```

- **Set Initial Values**: Alternatively, set an initial instance of a concrete class before accessing the property, preventing `LazyDynaBean` from attempting to instantiate it:

  ```java
  LazyDynaBean dynaBean = new LazyDynaBean();
  dynaBean.set("myProperty", new ArrayList<>()); // Set concrete instance
  Object value = dynaBean.get("myProperty"); // No instantiation needed
  ```

#### 5. Handle Dynamic Property Creation

- If properties are created dynamically (common with `LazyDynaBean`), ensure that the first value set for a property is an instance of a concrete class. This sets the type correctly:

  ```java
  LazyDynaBean dynaBean = new LazyDynaBean();
  dynaBean.set("myList", new ArrayList<>()); // Sets type to ArrayList
  ```

- Avoid accessing undefined properties without setting them first, as `LazyDynaBean` may attempt to instantiate a default type that could be problematic.

#### 6. Verify Constructor Accessibility

- Confirm that the concrete class has a public no-arg constructor. For example:

  ```java
  public class MyConcreteClass {
      public MyConcreteClass() {
          // Public no-arg constructor
      }
  }
  ```

- If the class lacks this, either add the constructor or use a different class that meets this requirement.

### Example Fix

Suppose the error occurs because a property `"items"` is typed as `java.util.List`, an interface:

- **Problematic Code**:

  ```java
  LazyDynaClass dynaClass = new LazyDynaClass();
  dynaClass.add("items", List.class); // Interface, cannot be instantiated
  LazyDynaBean dynaBean = new LazyDynaBean(dynaClass);
  dynaBean.get("items"); // Throws InstantiationException
  ```

- **Fixed Code**:

  ```java
  LazyDynaClass dynaClass = new LazyDynaClass();
  dynaClass.add("items", ArrayList.class); // Concrete class
  LazyDynaBean dynaBean = new LazyDynaBean(dynaClass);
  dynaBean.get("items"); // Returns a new ArrayList
  ```

### Additional Considerations

- **Custom Types**: If the property type is a custom abstract class or interface, provide a concrete subclass tailored to your application.
- **Library Version**: Ensure you’re using a compatible version of Apache Commons BeanUtils, though this issue is generally usage-related rather than a bug.
- **Alternative Approach**: If adjusting types is impractical, consider initializing all properties with concrete instances before use, or explore `WrapDynaBean` for wrapping existing beans without instantiation attempts.

### Final Solution

To resolve the `java.lang.InstantiationException` at `LazyDynaBean.java` line 844:

1. Locate the property causing the error via the stack trace or logs.
2. Check its defined type in the `DynaClass` or its inferred type from usage.
3. Replace any abstract class or interface with a concrete class (e.g., `ArrayList` for `List`) that has a public no-arg constructor.
4. Update the `DynaClass` definition or set an initial concrete instance to avoid automatic instantiation.

Without the specific property name or type from the error message, ensure all property types in your `LazyDynaBean` usage are concrete and instantiable. This should eliminate the exception.

---

I understand that you're encountering a `java.lang.InstantiationException` in your filter class during the `init(FilterConfig filterConfig)` method, and you're looking for a way to fix it. This error typically occurs when the code tries to create an instance of a class that cannot be instantiated, such as an abstract class or interface, often linked to the use of `LazyDynaBean` from Apache Commons BeanUtils at line 844. Since you’ve mentioned that you only have a filter class with an `init` method, let’s address this step-by-step to resolve the issue.

### Understanding the Problem

In a Java web application, a filter’s `init` method is called by the servlet container to initialize the filter using a `FilterConfig` object. The error suggests that during this initialization, something (likely `LazyDynaBean`) is trying to instantiate a property type that isn’t a concrete class or lacks a public no-argument constructor. Since you’re using `LazyDynaBean` (implied by the error message), it’s probably being used to dynamically handle properties, perhaps from the `FilterConfig` parameters, and one of those properties is causing the exception.

### Steps to Fix the Issue

1. **Examine Your `init` Method**
   Start by looking at the code inside your `init(FilterConfig filterConfig)` method. You might be creating a `LazyDynaBean` to store configuration data or process initialization parameters. Here’s an example of what your code might look like:

   ```java
   import org.apache.commons.beanutils.LazyDynaBean;
   import javax.servlet.*;

   public class MyFilter implements Filter {
       private LazyDynaBean configBean;

       @Override
       public void init(FilterConfig filterConfig) throws ServletException {
           configBean = new LazyDynaBean();
           Enumeration<String> initParams = filterConfig.getInitParameterNames();
           while (initParams.hasMoreElements()) {
               String paramName = initParams.nextElement();
               String paramValue = filterConfig.getInitParameter(paramName);
               configBean.set(paramName, paramValue);
           }
           // Accessing a property that might trigger instantiation
           Object someProperty = configBean.get("someProperty");
       }

       @Override
       public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
               throws IOException, ServletException {
           chain.doFilter(request, response);
       }

       @Override
       public void destroy() {}
   }
   ```

   In this example, if `"someProperty"` isn’t set with a value beforehand and its type is abstract (e.g., `List` instead of `ArrayList`), `LazyDynaBean` will try to instantiate it and fail, causing the `InstantiationException`.

2. **Identify the Problematic Property**
   Since the error occurs in `LazyDynaBean.java` at line 844, it’s likely tied to a `get` or `set` operation on the `LazyDynaBean`. To find the culprit:
   - Add logging or print statements before each `configBean.get()` or `configBean.set()` call to see which property triggers the exception.
   - Example:

     ```java
     System.out.println("Getting property: someProperty");
     Object someProperty = configBean.get("someProperty");
     ```

3. **Ensure Concrete Types or Initial Values**
   `LazyDynaBean` creates properties lazily, but if you access a property without setting it first, it tries to instantiate its type. If that type is abstract or an interface (e.g., `List`, `Map`), it throws an `InstantiationException`. To fix this:
   - **Set an Initial Value**: Provide a concrete instance before accessing the property.

     ```java
     configBean.set("someProperty", new ArrayList<String>()); // Concrete class
     Object someProperty = configBean.get("someProperty");    // Safe now
     ```

   - **Specify a Concrete Type**: If you define property types, use concrete classes.

     ```java
     configBean.setType("someProperty", ArrayList.class); // Not List.class
     ```

4. **Verify Constructors**
   If you’re setting a property with a custom class (e.g., `MyCustomClass`), ensure it has a public no-arg constructor:

   ```java
   public class MyCustomClass {
       public MyCustomClass() {} // Required by LazyDynaBean
   }
   ```

   Then use it:

   ```java
   configBean.set("someProperty", new MyCustomClass());
   ```

5. **Simplify If Possible**
   If you’re only using `LazyDynaBean` to store `FilterConfig` parameters, consider avoiding it altogether and using a `Map` or direct `FilterConfig` access:

   ```java
   public class MyFilter implements Filter {
       private Map<String, String> configMap;

       @Override
       public void init(FilterConfig filterConfig) throws ServletException {
           configMap = new HashMap<>();
           Enumeration<String> initParams = filterConfig.getInitParameterNames();
           while (initParams.hasMoreElements()) {
               String paramName = initParams.nextElement();
               configMap.put(paramName, filterConfig.getInitParameter(paramName));
           }
       }
       // Other methods...
   }
   ```

   This avoids the `LazyDynaBean` complexities entirely.

### Final Solution

Here’s a corrected version of the filter assuming `LazyDynaBean` is necessary:

```java
import org.apache.commons.beanutils.LazyDynaBean;
import javax.servlet.*;
import java.util.ArrayList;
import java.util.Enumeration;

public class MyFilter implements Filter {
    private LazyDynaBean configBean;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        configBean = new LazyDynaBean();
        Enumeration<String> initParams = filterConfig.getInitParameterNames();
        while (initParams.hasMoreElements()) {
            String paramName = initParams.nextElement();
            String paramValue = filterConfig.getInitParameter(paramName);
            configBean.set(paramName, paramValue); // Set string values safely
        }
        // Pre-set any properties that will be accessed later with concrete types
        if (configBean.get("someProperty") == null) {
            configBean.set("someProperty", new ArrayList<String>());
        }
        Object someProperty = configBean.get("someProperty"); // Now safe
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {}
}
```

### Testing the Fix

- Deploy the updated filter to your servlet container (e.g., Tomcat).
- Check the logs to ensure the `InstantiationException` no longer occurs.
- If it persists, share the full stack trace or more code details for further assistance.

This approach ensures that all properties accessed via `LazyDynaBean` are either set with concrete instances or avoided, resolving the `InstantiationException` in your filter’s `init` method.

---

I understand that you're encountering an issue where `LazyDynaBean` appears in an error message (specifically a `java.lang.InstantiationException` at `LazyDynaBean.java:844`), even though you never explicitly mention or use `LazyDynaBean` in your code. This situation typically arises when a library or framework you're using indirectly relies on `LazyDynaBean`. Let’s break this down and resolve it step-by-step.

### Why Is `LazyDynaBean` Involved?

Since you’re not directly referencing `LazyDynaBean`, it’s likely being invoked by a dependency in your project, such as:

- **Apache Commons BeanUtils**: This library uses `LazyDynaBean` internally for dynamic property access or bean manipulation.
- **Spring Framework**: If your code integrates with Spring (e.g., in a filter or bean configuration), it might use BeanUtils or similar utilities that involve `LazyDynaBean`.
- **Other Frameworks**: Any tool dealing with dynamic properties, configurations, or bean instantiation could be the culprit.

The `InstantiationException` suggests that `LazyDynaBean` is trying to create an instance of a class but failing, possibly because it’s encountering an abstract class, interface, or a type without a public no-argument constructor.

### How to Fix the Issue

Here’s a structured approach to identify and resolve the problem:

#### 1. Examine the Stack Trace

- Look at the full stack trace of the `InstantiationException`. It will show the sequence of calls leading to `LazyDynaBean.java:844`.
- Identify the library or framework in your code that triggers this call. For example, you might see references to `org.apache.commons.beanutils` or `org.springframework.beans`.

#### 2. Review Your Code and Dependencies

- Check your filter (or the class where the error occurs) for dependencies. If it’s a servlet filter, look at:
  - The `init` method.
  - Any properties or beans it uses.
  - Libraries imported in your project (e.g., via Maven/Gradle).
- Common libraries to suspect:
  - `commons-beanutils` (used for dynamic property handling).
  - Spring or other frameworks that manage beans.

#### 3. Inspect Configuration

- If your filter is configured via XML (e.g., in a `web.xml` or Spring context file), ensure all referenced objects are properly defined.
- For example, if a property is set dynamically:

  ```xml
  <bean id="myFilter" class="com.example.MyFilter">
      <property name="someProperty" ref="someBean"/>
  </bean>
  ```

  Verify that `someBean` is a concrete class, like:

  ```xml
  <bean id="someBean" class="com.example.ConcreteClass"/>
  ```

#### 4. Ensure Concrete Types

- The exception often occurs when a library expects to instantiate a type but gets an interface or abstract class (e.g., `List` instead of `ArrayList`).
- If you’re defining properties, make sure they use concrete implementations with public no-arg constructors:

  ```java
  private List<String> myList = new ArrayList<>(); // Good
  private List<String> myList; // Risky if set dynamically
  ```

#### 5. Debug the Problem

- Add logging or use a debugger in your filter’s `init` method (or wherever the error occurs) to pinpoint the exact line causing the exception.
- Example:

  ```java
  public class MyFilter implements Filter {
      private List<String> myList;

      public void setMyList(List<String> myList) {
          this.myList = myList;
      }

      @Override
      public void init(FilterConfig config) throws ServletException {
          System.out.println("Initializing filter...");
          if (myList == null) {
              myList = new ArrayList<>(); // Initialize manually if needed
          }
      }
  }
  ```

#### 6. Manual Initialization (if Needed)

- If the library is dynamically setting properties and failing, consider initializing them yourself to bypass the issue:

  ```java
  public class MyFilter implements Filter {
      private SomeClass myObject = new SomeClass(); // Concrete instance

      @Override
      public void init(FilterConfig config) throws ServletException {
          // Filter initialization logic
      }
  }
  ```

### Example Scenario

Suppose you’re using Spring’s `GenericFilterBean` and have:

```xml
<bean id="myFilter" class="com.example.MyFilter">
    <property name="myList" ref="listBean"/>
</bean>
<bean id="listBean" class="java.util.List"/> <!-- Problem: Interface -->
```

The fix would be:

```xml
<bean id="listBean" class="java.util.ArrayList"/> <!-- Concrete class -->
```

Or in code:

```java
public class MyFilter extends GenericFilterBean {
    private List<String> myList = new ArrayList<>(); // Default concrete instance

    public void setMyList(List<String> myList) {
        this.myList = myList;
    }
}
```

### Final Steps

- **Identify the Source**: Pinpoint the library or configuration causing `LazyDynaBean` to be invoked.
- **Fix Configurations**: Ensure all types are concrete and instantiable.
- **Test**: Redeploy and verify the exception is resolved.

If the problem persists, share more details (e.g., the stack trace, your filter code, or dependencies), and I can provide a more specific solution. This approach should help you eliminate the `InstantiationException` without needing to directly handle `LazyDynaBean`.
