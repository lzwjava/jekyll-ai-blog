---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jackson Default Typing Explained and Disabled
translated: false
type: note
---

In Jackson (the `com.fasterxml.jackson.databind` library), **default typing** is a feature of `ObjectMapper` that automatically includes type metadata (like `@class` or `@type`) in serialized JSON so that objects can be deserialized back into their original polymorphic types.

For example, if you serialize a `List<Animal>` containing both `Dog` and `Cat`, default typing adds extra JSON fields so Jackson knows which subclass to re-instantiate later.

---

### How Disabling Works

When you **disable default typing**, Jackson stops injecting those extra type metadata fields. That means:

* JSON output will be “cleaner,” without `@class`/`@type` hints.
* On deserialization, Jackson can only reconstruct objects using declared static types (the target type you pass in), not the original runtime types.
* Any polymorphic use cases will break unless you explicitly configure `@JsonTypeInfo`, `@JsonSubTypes`, or custom modules.

---

### Relevant Methods

* **Enabling** (pre-2.10 style):

  ```java
  objectMapper.enableDefaultTyping();
  ```

  (deprecated, because it was too permissive and introduced security risks.)

* **Disabling**:

  ```java
  objectMapper.disableDefaultTyping();
  ```

  or in newer versions (2.10+), you call:

  ```java
  objectMapper.activateDefaultTyping(PolymorphicTypeValidator, ObjectMapper.DefaultTyping.NON_FINAL);
  ```

  To *disable*, you simply **do not call** this method at all (there’s no default typing unless you enable it), or you can call:

  ```java
  objectMapper.deactivateDefaultTyping();
  ```

---

### Security and Rationale

* **Default typing is disabled by default** in modern Jackson versions because it can be exploited (attackers could craft JSON that instantiates dangerous classes).
* If you disable it, Jackson behaves in a “safer” mode, where deserialization only works for types you explicitly bind, not arbitrary runtime types.
* If you need polymorphic support, you should annotate your classes with `@JsonTypeInfo` instead of relying on global default typing.

---

✅ **In short:**
Disabling default typing tells Jackson **not** to include type metadata in JSON, meaning it won’t auto-reconstruct polymorphic subtypes on deserialization. This reduces flexibility but is safer and keeps the JSON clean.

Do you want me to show you a **before/after JSON example** with default typing enabled vs disabled?
