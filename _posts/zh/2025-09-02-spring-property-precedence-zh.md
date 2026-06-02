---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Spring属性优先级规则详解
translated: true
type: note
---

在 Spring 中，当配置源（如 `application.properties`、`application.yml`、环境变量、命令行参数等）中出现**重复的属性键**时，**优先级最高的最后一个配置将生效**。

以下是详细说明：

### 1. 属性源顺序

Spring Boot 采用明确定义的**属性源顺序**。例如：

* 命令行参数
* `application.properties` / `application.yml`（特定配置文件的优先，然后是默认配置）
* 环境变量
* 系统属性
* 代码中的默认值（`@Value("${...:default}")`）

如果同一属性键出现在多个源中，Spring 会选择**最高优先级源**中的值。

### 2. 同一文件内

如果在**单个文件**（如 `application.properties`）中重复出现同一属性键，Spring 将使用**最后声明的配置项**。
示例（`application.properties`）：

```properties
server.port=8080
server.port=9090
```

此时 `server.port=9090` 将生效。

### 3. 跨多个文件

如果在 `application.properties` 和 `application-dev.properties` 中定义了相同属性，并且激活了 `dev` 配置文件，那么 `application-dev.properties` 中的值将覆盖默认文件中的值。

### 4. 使用 `@PropertySource`

如果通过 `@PropertySource` 加载多个属性文件，声明顺序至关重要。除非标记 `ignoreResourceNotFound` 或显式控制优先级，否则后加载的文件将覆盖先前的值。

---

✅ **总结：**

* Spring 通过**属性源优先级**来解析属性
* 在**同一文件**中，**最后的键定义**生效
* 跨文件/配置文件时，**激活配置文件的属性**或**后加载文件的属性**将覆盖先前的值

是否需要为您展示 **Spring Boot 属性优先级层次结构（从高到低）**？这将更清晰地展示属性覆盖的发生位置。
