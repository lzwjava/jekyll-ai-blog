---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jackson默认类型机制详解与禁用方法
translated: true
type: note
---

在Jackson（`com.fasterxml.jackson.databind`库）中，**默认类型识别**是`ObjectMapper`的一项功能，它会在序列化的JSON中自动包含类型元数据（如`@class`或`@type`），以便对象能够反序列化回其原始的多态类型。

例如，如果你序列化一个包含`Dog`和`Cat`的`List<Animal>`，默认类型识别会添加额外的JSON字段，让Jackson知道之后要重新实例化哪个子类。

---

### 禁用机制解析

当你**禁用默认类型识别**时，Jackson将停止注入这些额外的类型元数据字段。这意味着：

* JSON输出将更"简洁"，不包含`@class`/`@type`提示
* 反序列化时，Jackson只能使用声明的静态类型（传入的目标类型）重建对象，无法识别原始运行时类型
* 除非显式配置`@JsonTypeInfo`、`@JsonSubTypes`或自定义模块，否则所有多态使用场景都会失效

---

### 相关配置方法

* **启用方法**（2.10之前版本）：
  ```java
  objectMapper.enableDefaultTyping();
  ```
  （已弃用，因其过于宽松会引入安全风险）

* **禁用方法**：
  ```java
  objectMapper.disableDefaultTyping();
  ```
  或在新版本（2.10+）中调用：
  ```java
  objectMapper.activateDefaultTyping(PolymorphicTypeValidator, ObjectMapper.DefaultTyping.NON_FINAL);
  ```
  若要*禁用*，只需**不调用**此方法（不启用则无默认类型识别），也可调用：
  ```java
  objectMapper.deactivateDefaultTyping();
  ```

---

### 安全机制与设计原理

* 现代Jackson版本中**默认禁用类型识别**，因其可能被恶意利用（攻击者可构造实例化危险类的JSON）
* 禁用后Jackson将处于"安全模式"，反序列化仅适用于显式绑定的类型，而非任意运行时类型
* 若需多态支持，应使用`@JsonTypeInfo`注解类，而非依赖全局默认类型识别

---

✅ **核心结论：**
禁用默认类型识别后，Jackson将**不会**在JSON中包含类型元数据，这意味着反序列化时无法自动重建多态子类型。虽然会降低灵活性，但能提升安全性并保持JSON结构简洁。

需要展示启用与禁用默认类型识别的**JSON示例对比**吗？
