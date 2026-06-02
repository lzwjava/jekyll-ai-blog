---
audio: false
generated: true
lang: zh
layout: post
title: Bean的XML配置文件
translated: true
type: note
---

针对您关于 beans XML 工作原理的疑问，包括使用 props 和 keys 定义 bean 属性、哪些类会使用这些 XML 文件以及它们如何被加载，下面将进行清晰系统的说明。本解释假设是在 Spring 这类框架的语境下，"beans XML" 是配置 bean 的常用术语。

### Beans XML 如何工作？

在 Spring 这类框架中，**beans XML 文件**是用于定义和管理称为 *bean* 的对象的配置文件。这些 bean 通常是 Spring 框架实例化、配置和管理的 Java 对象。XML 文件指定了：

- **Bean**：每个 bean 使用 `<bean>` 标签定义，包含 `id`（唯一标识符）和 `class`（要实例化的 Java 类的全限定名）。
- **属性**：Bean 可以拥有属性，这些是设置到 bean 中用于配置其行为的值或引用。属性使用 `<property>` 标签定义。
- **Props 和 Keys**：在 `<property>` 标签内，可以使用 `<props>` 元素定义一组键值对。这在 bean 期望一个 `java.util.Properties` 对象或类似结构（如 `Map`）时非常有用。`<props>` 元素包含多个 `<prop>` 标签，每个标签都有一个 `key` 属性和对应的值。

以下是一个在 beans XML 文件中的示例：

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

在这个例子中：

- 一个 ID 为 `myBean` 的 bean 由 `com.example.MyBean` 类创建。
- 该 bean 有一个名为 `someProperty` 的属性。
- `<props>` 元素定义了一组键值对（`key1=value1` 和 `key2=value2`），Spring 会将其转换为 `Properties` 对象，并通过像 `setSomeProperty(Properties props)` 这样的 setter 方法注入到 `myBean` 中。

您查询中提到的 "it puts in resources" 表述有些模糊，但它很可能指的是 XML 文件本身作为一种*资源*（应用程序类路径或文件系统中的文件）被应用程序使用，或者也可能指 XML 中定义的 bean（如数据源）代表了应用程序使用的资源。目前，我们先假设它指的是 XML 文件本身作为被应用程序加载的资源。

### 哪些类会使用这些 XML 文件？

在 Spring 中，负责使用（即加载和处理）beans XML 文件的类是 **`ApplicationContext`**。更准确地说，是 `ApplicationContext` 接口的一个实现，例如：

- **`ClassPathXmlApplicationContext`**：从类路径加载 XML 文件。
- **`FileSystemXmlApplicationContext`**：从文件系统加载 XML 文件。

`ApplicationContext` 是 Spring 用于向应用程序提供配置信息的核心接口。它读取 beans XML 文件，解析它，并使用其中的定义来创建和管理 bean。虽然 bean 本身（例如 `com.example.MyBean`）会使用 XML 中定义的属性，但 `ApplicationContext` 是直接处理 XML 文件以实现这一点的类。

### 它将如何被加载？

beans XML 文件通过创建一个 `ApplicationContext` 实现的实例并指定 XML 文件的位置来加载到应用程序中。以下是其工作步骤：

1. **指定 XML 文件位置**：当您实例化 `ApplicationContext` 时，需要提供 XML 文件的名称或路径。例如：

   ```java
   ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
   ```

   这里，假设 `"beans.xml"` 位于类路径中（例如，在典型的 Java 项目的 `src/main/resources` 目录下）。

2. **作为资源加载**：`ApplicationContext` 使用 `ResourceLoader` 来定位并作为 `Resource` 加载 XML 文件。在这种情况下，`ClassPathXmlApplicationContext` 会在类路径中查找该文件。

3. **解析 XML**：在内部，Spring 使用 `XmlBeanDefinitionReader` 来解析 XML 文件。该读取器解释 `<bean>` 标签、属性和 `<props>` 元素，创建描述每个 bean 应如何构建的 `BeanDefinition` 对象。

4. **Bean 创建**：`ApplicationContext`（它扩展了 Spring 的 `BeanFactory`）使用这些 bean 定义来实例化 bean，设置它们的属性（包括注入来自 `<props>` 的 `Properties` 对象），并管理它们的生命周期。

加载完成后，您可以像这样从 `ApplicationContext` 中获取 bean：

```java
MyBean myBean = context.getBean("myBean", MyBean.class);
```

### 整体流程总结

- **Beans XML 如何工作**：XML 定义了 bean 及其属性，包括通过 `<props>` 定义的键值对。Spring 解析此 XML 来配置和实例化 bean。
- **使用 XML 的类**：`ApplicationContext`（例如 `ClassPathXmlApplicationContext`）使用 XML 文件来设置应用程序。
- **如何加载**：当您创建 `ApplicationContext` 实例并指定文件位置时，XML 作为资源从类路径或文件系统加载。

例如，如果您的 `beans.xml` 在类路径中，您可以使用以下代码加载它：

```java
ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
```

然后 Spring 会处理其余工作，使配置好的 bean 可供您的应用程序使用。

这种机制强大而灵活，允许您在 XML 中定义复杂的配置，Spring 在运行时将这些配置变为现实。
