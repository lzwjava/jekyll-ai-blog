---
audio: false
generated: true
lang: en
layout: post
title: XML Configuration Files For Beans
translated: false
type: note
---

To address your query about how beans XML works, including bean properties with props and keys, what class uses these XML files, and how they are loaded, let’s break it down clearly and systematically. This explanation assumes a context like Spring, where "beans XML" is a common term for configuring beans.

### How Does Beans XML Work?

In frameworks like Spring, a **beans XML file** is a configuration file used to define and manage objects called *beans*. These beans are typically Java objects that the Spring framework instantiates, configures, and manages. The XML file specifies:

- **Beans**: Each bean is defined using a `<bean>` tag, which includes an `id` (a unique identifier) and a `class` (the fully qualified name of the Java class to instantiate).
- **Properties**: Beans can have properties, which are values or references set into the bean to configure its behavior. Properties are defined using the `<property>` tag.
- **Props and Keys**: Within a `<property>` tag, you can use a `<props>` element to define a set of key-value pairs. This is useful when a bean expects a `java.util.Properties` object or a similar structure like a `Map`. The `<props>` element contains multiple `<prop>` tags, each with a `key` attribute and a corresponding value.

Here’s an example of how this looks in a beans XML file:

```xml
<bean id="myBean" class="com.example.MyBean">
    <property name="someProperty">
        <props>
            <prop key="key1">value1</prop>
            <prop key="key2">value2</prop>
        </props>
    </property>
</bean>
```

In this example:

- A bean with the ID `myBean` is created from the class `com.example.MyBean`.
- The bean has a property named `someProperty`.
- The `<props>` element defines a set of key-value pairs (`key1=value1` and `key2=value2`), which Spring converts into a `Properties` object and injects into `myBean` via a setter method like `setSomeProperty(Properties props)`.

The phrase "it puts in resources" in your query is a bit unclear, but it likely refers to the XML file being a *resource* (a file in the application’s classpath or filesystem) that the application uses, or it could mean that the beans defined in the XML (like a data source) represent resources used by the application. For now, let’s assume it’s about the XML file itself being a resource loaded by the application.

### What Class Will Use These XML Files?

In Spring, the class responsible for using (i.e., loading and processing) the beans XML file is the **`ApplicationContext`**. More precisely, it’s an implementation of the `ApplicationContext` interface, such as:

- **`ClassPathXmlApplicationContext`**: Loads the XML file from the classpath.
- **`FileSystemXmlApplicationContext`**: Loads the XML file from the filesystem.

The `ApplicationContext` is Spring’s central interface for providing configuration information to an application. It reads the beans XML file, parses it, and uses the definitions to create and manage the beans. While the beans themselves (e.g., `com.example.MyBean`) use the properties defined in the XML, the `ApplicationContext` is the class that directly processes the XML file to make this happen.

### How Will It Be Loaded?

The beans XML file is loaded into the application by creating an instance of an `ApplicationContext` implementation and specifying the location of the XML file. Here’s how it works step-by-step:

1. **Specify the XML File Location**: When you instantiate the `ApplicationContext`, you provide the name or path of the XML file. For example:

   ```java
   ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
   ```

   Here, `"beans.xml"` is assumed to be in the classpath (e.g., in the `src/main/resources` directory in a typical Java project).

2. **Loading as a Resource**: The `ApplicationContext` uses a `ResourceLoader` to locate and load the XML file as a `Resource`. In this case, `ClassPathXmlApplicationContext` looks for the file in the classpath.

3. **Parsing the XML**: Internally, Spring uses an `XmlBeanDefinitionReader` to parse the XML file. This reader interprets the `<bean>` tags, properties, and `<props>` elements, creating `BeanDefinition` objects that describe how each bean should be constructed.

4. **Bean Creation**: The `ApplicationContext` (which extends Spring’s `BeanFactory`) uses these bean definitions to instantiate the beans, set their properties (including injecting the `Properties` object from `<props>`), and manage their lifecycle.

Once loaded, you can retrieve beans from the `ApplicationContext` like this:

```java
MyBean myBean = context.getBean("myBean", MyBean.class);
```

### Putting It All Together

- **How Beans XML Works**: The XML defines beans and their properties, including key-value pairs via `<props>`. Spring parses this XML to configure and instantiate the beans.
- **Class That Uses the XML**: The `ApplicationContext` (e.g., `ClassPathXmlApplicationContext`) uses the XML file to set up the application.
- **How It’s Loaded**: The XML is loaded as a resource from the classpath or filesystem when you create an `ApplicationContext` instance, specifying the file’s location.

For example, if your `beans.xml` is in the classpath, you’d load it with:

```java
ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
```

Spring then handles the rest, making the configured beans available to your application.

This mechanism is powerful and flexible, allowing you to define complex configurations in XML that Spring brings to life at runtime.
