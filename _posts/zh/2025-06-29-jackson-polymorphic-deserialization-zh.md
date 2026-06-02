---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Jackson多态反序列化概述
translated: true
type: note
---

### Jackson 多态反序列化概述

Jackson 是一个用于 JSON 序列化与反序列化的 Java 库。多态反序列化功能允许 Jackson 在反序列化过程中，根据 JSON 中嵌入的类型信息自动实例化基类的正确子类。这在处理继承层次结构时非常有用，能确保从 JSON 数据创建正确的对象类型。

核心组件：
- **@JsonTypeInfo**：控制类型信息在 JSON 中存储位置和方式的注解
- **@JsonSubTypes**：列出子类及其标识符的注解
- Jackson 的子类型解析机制负责处理映射关系

若未配置这些注解，Jackson 会默认将所有对象反序列化为基类类型，可能导致子类特有数据丢失。

### 运作机制详解

1. **基类注解配置**：
   - 使用 `@JsonTypeInfo` 指定类型信息嵌入位置（例如作为 JSON 对象的属性）
   - 示例：
     ```java
     @JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "@type")
     @JsonSubTypes({
         @JsonSubType(value = Cat.class, name = "cat"),
         @JsonSubType(value = Dog.class, name = "dog")
     })
     public abstract class Animal {
         public String name;
     }
     ```
     - `use = JsonTypeInfo.Id.NAME`：使用名称（字符串标识符）表示类型
     - `include = JsonTypeInfo.As.PROPERTY`：将类型信息以属性形式（"@type"）添加到 JSON 对象
     - `@JsonSubTypes`：将子类名称映射到对应的 Java 类（如 "cat" → Cat.class）

2. **序列化过程**：
   - 当序列化 Cat 或 Dog 对象时，Jackson 会将类型标识符添加到 JSON
   - 示例输出：`{"@type": "cat", "name": "Whiskers", "purr": true}`（如果 Cat 类包含 "purr" 字段）

3. **反序列化过程**：
   - Jackson 读取 JSON 并检查类型信息（如 "@type" 属性）
   - 通过 `@JsonSubTypes` 将标识符（"cat"）映射回注册的子类（Cat.class）
   - 实例化正确的子类并填充其字段
   - 若未匹配到类型信息或信息缺失，可配置为默认使用基类或抛出异常（通过 `defaultImpl` 配置）

4. **支持的类型信息格式**：
   - `@JsonTypeInfo.As.PROPERTY`：类型作为字段（如 `{"@type": "cat", ...}`）
   - `@JsonTypeInfo.As.WRAPPER_OBJECT`：用类型作为键的包装器包裹对象（如 `{"cat": {...}}`）
   - `@JsonTypeInfo.As.WRAPPER_ARRAY`：使用数组格式
   - `@JsonTypeInfo.As.EXTERNAL_PROPERTY`：类型信息存储于独立字段（适用于 XML 类结构）

### 高级配置与边界情况

- **自定义名称映射**：使用 `@JsonTypeInfo(use = JsonTypeInfo.Id.CLASS)` 将完整类名直接嵌入 JSON（如 `{"@class": "com.example.Cat", ...}`），但重构时可能产生问题
- **默认实现**：通过 `defaultImpl = Animal.class` 配置类型信息缺失时的回退方案
- **可见性与混入机制**：若无法修改源类，可通过混入类应用注解
- **错误处理**：当类型信息不匹配已注册子类型时，Jackson 会抛出 `JsonMappingException`，可通过自定义反序列化器处理
- **性能影响**：反序列化时因高效查找产生的开销很小，但嵌入类型信息会增加 JSON 载荷大小

完整文档请参阅 Jackson 官方指南：[多态类型处理](https://github.com/FasterXML/jackson-docs/wiki/JacksonPolymorphicDeserialization)。此功能自 Jackson 2.x 版本起保持稳定，其他 JSON 库（如 Gson）也具备类似概念。如需进一步定制，可扩展 `PolymorphicTypeValidator` 来保障不可信输入场景下的安全性。
