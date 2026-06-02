---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Jackson默认类型机制解析
translated: true
type: note
---

### Jackson ObjectMapper 中的默认类型机制是什么？

Jackson 的 `ObjectMapper` 是 Jackson JSON 库中用于 Java 对象与 JSON 相互转换的核心类。"默认类型机制"是一项增强多态类型处理的功能（例如当某个字段可容纳不同子类时）。其工作原理是在序列化过程中将类型信息嵌入 JSON 输出，反序列化时映射器利用这些信息实例化正确的具体类。

若不启用默认类型机制，Jackson 将依赖声明类型（如抽象基类或接口），可能需要通过 `@JsonTypeInfo` 注解等自定义配置来指定子类型。启用该功能可为多态场景提供全局或半全局的备用方案，特别适用于包含混合类型的集合或映射结构。

### 工作机制解析

启用默认类型机制会改变序列化过程：
1. **序列化**：当序列化对象图时，Jackson 会在 JSON 中添加特殊的 `@class` 字段或类似元数据，用于标识多态对象的运行时类型。这仅发生在声明类型未完全指定具体类的场景（例如包含 `String` 和 `Integer` 的 `List`，或抽象类字段）。

2. **反序列化**：在反序列化过程中，映射器利用嵌入的类型信息查找并实例化精确的类。通过 Jackson 的 `TypeFactory` 实现动态类型解析。

启用方式（调用 `ObjectMapper` 实例的方法）：
- `mapper.enableDefaultTyping()`：已弃用方法，启用恒定时间多态类型包含（存在安全风险）
- `mapper.activateDefaultTyping(ObjectMapper.DefaultTyping policy)`：Jackson 2.10 引入的更安全方案，需指定枚举值：
  - `JAVA_LANG_OBJECT`：为所有 `Object` 引用添加类型信息
  - `NON_CONCRETE_AND_ARRAYS`：为抽象/非具体类型及数组添加类型信息
  - `NON_FINAL`：为非 final 类添加类型信息

使用示例：
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import static com.fasterxml.jackson.databind.ObjectMapper.DefaultTyping;

ObjectMapper mapper = new ObjectMapper();
mapper.activateDefaultTyping(DefaultTyping.NON_CONCRETE_AND_ARRAYS);
```

若不启用该功能，序列化包含混合类型的 `List<Object>` 时，JSON 可能缺失类型细节导致反序列化错误。启用后，JSON 将包含类型提示，例如：`[{"@class": "java.lang.String", "value": "hello"}, {"@class": "java.lang.Integer", "value": 42}]`。

### 安全考量与限制

- **漏洞风险**：盲目启用默认类型机制（尤其是旧版 `enableDefaultTyping()`）可能使系统面临数据提取等攻击，因为恶意构造的 JSON 可触发任意类反序列化。新版 Jackson 默认仅允许常见类型以降低风险。
- **适用场景**：最适用于需要处理多态数据的可信环境（如内部 API）。对于公开 API，建议使用显式类型注解或自定义序列化/反序列化器以提升安全性。
- **性能影响**：嵌入类型信息会增加 JSON 体积，带来轻微性能开销。

若此内容涉及其他"对象映射器"（如 Elasticsearch 或其他库），请提供更多背景信息以获取针对性说明。完整细节请参阅 Jackson 官方文档。
