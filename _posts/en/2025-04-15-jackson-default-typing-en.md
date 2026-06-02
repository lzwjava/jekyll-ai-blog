---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Jackson Default Typing Explained
translated: false
type: note
---

### What is Default Typing in Jackson's ObjectMapper?

Jackson's `ObjectMapper` is a core class in the Jackson JSON library for Java, responsible for serializing Java objects to JSON and deserializing JSON back to objects. "Default typing" is a feature that enhances the handling of polymorphic types (e.g., when a field can hold different subclasses). It works by embedding type information in the JSON output during serialization, which the mapper uses during deserialization to instantiate the correct concrete class.

Without default typing, Jackson relies on the declared type (e.g., an abstract base class or interface), and you might need custom configuration like `@JsonTypeInfo` annotations to specify subtypes. Enabling default typing provides a global or semi-global fallback for polymorphism, particularly useful for collections or maps with mixed types.

### How Does It Work?

Enabling default typing modifies the serialization process:
1. **Serialization**: When serializing an object graph, Jackson adds a special `@class` field or similar metadata to the JSON to indicate the runtime type of polymorphic objects. This happens only for types where the declared type doesn't fully specify the concrete class (e.g., `List` containing `String` and `Integer` objects, or abstract class fields).

2. **Deserialization**: During deserialization, the mapper uses this embedded type info to look up and instantiate the exact class. It leverages Jackson's `TypeFactory` to resolve types dynamically.

To enable it, you call one of these methods on an `ObjectMapper` instance:
- `mapper.enableDefaultTyping()`: A deprecated method that enables constant-time polymorphic typing inclusion (susceptible to security issues).
- `mapper.activateDefaultTyping(ObjectMapper.DefaultTyping policy)`: A safer, recommended alternative introduced in Jackson 2.10. It allows specifying a `DefaultTyping` enum value, such as:
  - `JAVA_LANG_OBJECT`: Includes typing for all `Object` references.
  - `NON_CONCRETE_AND_ARRAYS`: Includes typing for abstract/non-concrete types and arrays.
  - `NON_FINAL`: Includes typing for non-final classes.

Example usage:
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import static com.fasterxml.jackson.databind.ObjectMapper.DefaultTyping;

ObjectMapper mapper = new ObjectMapper();
mapper.activateDefaultTyping(DefaultTyping.NON_CONCRETE_AND_ARRAYS);
```

Without enabling, if you serialize a `List<Object>` with mixed types, the JSON might omit type details, leading to deserialization errors. With it enabled, the JSON includes type hints, e.g., `[{"@class": "java.lang.String", "value": "hello"}, {"@class": "java.lang.Integer", "value": 42}]`.

### Security Considerations and Limitations

- **Vulnerabilities**: Blindly enabling default typing (especially the old `enableDefaultTyping()`) can expose systems to attacks like data extraction, as it allows deserializing arbitrary classes via crafted JSON. Jackson limits this by default in newer versions, only allowing common types unless customized.
- **Use Case Fit**: It's best for trusted environments with polymorphic data (e.g., internal APIs). For public APIs, prefer explicit type annotations or custom serializers/deserializers for better security.
- **Performance**: Adds minor overhead due to embedded type info, increasing JSON size.

If this relates to a different "object mapper" (e.g., Elasticsearch's or another library), provide more context for a tailored explanation. For full details, refer to Jackson's official documentation.
