---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Jackson Polymorphic Deserialization Overview
translated: false
type: note
---

### Overview of Jackson Polymorphic Deserialization

Jackson is a Java library for JSON serialization and deserialization. Polymorphic deserialization allows Jackson to automatically instantiate the correct subclass of a base class during deserialization, based on type information embedded in the JSON. This is useful when dealing with inheritance hierarchies, ensuring the right object type is created from JSON data.

Key components:
- **@JsonTypeInfo**: Annotations that control where and how type information is stored in the JSON.
- **@JsonSubTypes**: Annotations that list subclasses (subtypes) and their identifiers.
- Jackson's subtype resolution handles the mapping.

Without these, Jackson would default to deserializing all objects as the base class, potentially losing subclass-specific data.

### How It Works Step-by-Step

1. **Annotations on the Base Class**:
   - Use `@JsonTypeInfo` to specify where type info is embedded (e.g., as a property in the JSON object).
   - Example:
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
     - `use = JsonTypeInfo.Id.NAME`: Uses a name (string identifier) for the type.
     - `include = JsonTypeInfo.As.PROPERTY`: Adds the type info as a property ("@type") in the JSON object.
     - `@JsonSubTypes`: Maps subclass names to their Java classes (e.g., "cat" → Cat.class).

2. **Serialization Process**:
   - When serializing a Cat or Dog object, Jackson adds the type identifier to the JSON.
   - Example output: `{"@type": "cat", "name": "Whiskers", "purr": true}` (if Cat has a "purr" field).

3. **Deserialization Process**:
   - Jackson reads the JSON and checks the type info (e.g., "@type" property).
   - It maps the identifier ("cat") back to the registered subclass (Cat.class) using `@JsonSubTypes`.
   - Instantiates the correct subclass and populates its fields.
   - If no match or missing type info, it defaults to the base class or throws exceptions (configurable via `defaultImpl`).

4. **Supported Type Info Formats**:
   - `@JsonTypeInfo.As.PROPERTY`: Type as a field (e.g., `{"@type": "cat", ...}`).
   - `@JsonTypeInfo.As.WRAPPER_OBJECT`: Wraps the object in a wrapper with the type as the key (e.g., `{"cat": {...}}`).
   - `@JsonTypeInfo.As.WRAPPER_ARRAY`: Uses an array format.
   - `@JsonTypeInfo.As.EXTERNAL_PROPERTY`: Type info in a separate field (advanced, for XML-like structures).

### Advanced Configuration and Edge Cases

- **Custom Name Mappers**: Use `@JsonTypeInfo(use = JsonTypeInfo.Id.CLASS)` to embed the fully qualified class name directly in JSON (e.g., `{"@class": "com.example.Cat", ...}`), which can be brittle across refactoring.
- **Default Implementation**: Add `defaultImpl = Animal.class` to fall back if type info is missing.
- **Visibility and Mix-Ins**: Apply annotations via mix-in classes if you can't modify the source classes.
- **Error Handling**: If type info doesn't match a registered subtype, Jackson throws a `JsonMappingException`. This can be handled with custom deserializers.
- **Performance**: Minimal overhead during deserialization due to efficient lookups, but embedding type info increases JSON payload size.

For full docs, see Jackson's official guide: [Polymorphic Type Handling](https://github.com/FasterXML/jackson-docs/wiki/JacksonPolymorphicDeserialization). This feature has been stable since Jackson 2.x, with similar concepts in other JSON libraries like Gson. If customizing further, extend `PolymorphicTypeValidator` for security in untrusted inputs.
