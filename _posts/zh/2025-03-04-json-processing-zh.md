---
audio: false
generated: true
lang: zh
layout: post
title: Java中的JSON数据处理
translated: true
type: note
---

要在 Java 项目中使用 `com.fasterxml.jackson` 包进行 JSON 处理，您可以利用 Jackson 库，该库广泛用于 Java 对象与 JSON 之间的相互转换。以下是一个分步指南，假设您正在使用基于 Maven 的项目。本指南重点介绍提供 JSON 数据绑定高级功能的 `jackson-databind` 模块。

---

### 1. 将 Jackson 依赖项添加到项目

要使用 `com.fasterxml.jackson` 包，您需要在项目中包含 Jackson 库。如果使用 Maven，请将以下依赖项添加到 `pom.xml` 文件中：

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.12.5</version> <!-- 请替换为最新版本 -->
</dependency>
```

- **注意**：请查看 [Maven 中央仓库](https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind)获取最新版本，可能比 2.12.5 更新。
- `jackson-databind` 模块依赖于 `jackson-core` 和 `jackson-annotations`，因此除非有特定要求，否则无需单独添加这些依赖项。

添加依赖项后，运行 `mvn install` 或在 IDE 中刷新项目以下载库。

---

### 2. 创建 `ObjectMapper` 实例

`com.fasterxml.jackson.databind` 包中的 `ObjectMapper` 类是进行 JSON 操作的主要工具。它是线程安全的，且实例化资源消耗较大，因此最好创建单个可重用的实例：

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonExample {
    private static final ObjectMapper mapper = new ObjectMapper();
}
```

将此代码放在执行 JSON 操作的类中。

---

### 3. 将 Java 对象转换为 JSON（序列化）

要将 Java 对象转换为 JSON 字符串，请使用 `writeValueAsString` 方法。以下是一个示例：

#### 定义 Java 类

创建一个包含要序列化字段的类。确保它具有 getter 和 setter 方法，因为 Jackson 默认使用这些方法来访问私有字段：

```java
public class MyClass {
    private String field1;
    private int field2;

    public MyClass(String field1, int field2) {
        this.field1 = field1;
        this.field2 = field2;
    }

    public String getField1() {
        return field1;
    }

    public void setField1(String field1) {
        this.field1 = field1;
    }

    public int getField2() {
        return field2;
    }

    public void setField2(int field2) {
        this.field2 = field2;
    }
}
```

#### 序列化为 JSON

使用 `ObjectMapper` 将对象转换为 JSON：

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonExample {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        MyClass obj = new MyClass("value1", 123);
        String json = mapper.writeValueAsString(obj);
        System.out.println(json);
    }
}
```

**输出**：

```json
{"field1":"value1","field2":123}
```

---

### 4. 将 JSON 转换为 Java 对象（反序列化）

要将 JSON 字符串转换回 Java 对象，请使用 `readValue` 方法：

```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonExample {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        String json = "{\"field1\":\"value1\",\"field2\":123}";
        MyClass obj = mapper.readValue(json, MyClass.class);
        System.out.println(obj.getField1()); // 输出 "value1"
    }
}
```

- **错误处理**：如果 JSON 格式错误或与类结构不匹配，`readValue` 方法会抛出 `JsonProcessingException`（受检异常）。使用 try-catch 块处理或在方法签名中声明：

```java
try {
    MyClass obj = mapper.readValue(json, MyClass.class);
} catch (JsonProcessingException e) {
    e.printStackTrace();
}
```

---

### 5. 使用注解自定义 JSON 处理

Jackson 提供注解来自定义字段的序列化或反序列化方式。将 `com.fasterxml.jackson.annotation` 中的这些注解添加到您的类中：

#### 重命名字段

使用 `@JsonProperty` 将 Java 字段映射到不同的 JSON 字段名称：

```java
import com.fasterxml.jackson.annotation.JsonProperty;

public class MyClass {
    @JsonProperty("name")
    private String field1;
    private int field2;
    // 构造函数、getter、setter
}
```

**输出**：

```json
{"name":"value1","field2":123}
```

#### 忽略字段

使用 `@JsonIgnore` 在序列化中排除字段：

```java
import com.fasterxml.jackson.annotation.JsonIgnore;

public class MyClass {
    private String field1;
    @JsonIgnore
    private int field2;
    // 构造函数、getter、setter
}
```

**输出**：

```json
{"field1":"value1"}
```

#### 格式化日期

使用 `@JsonFormat` 指定日期的序列化方式：

```java
import com.fasterxml.jackson.annotation.JsonFormat;
import java.util.Date;

public class MyClass {
    private String field1;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    private Date date;
    // 构造函数、getter、setter
}
```

**输出**（示例）：

```json
{"field1":"value1","date":"2023-10-25"}
```

---

### 6. 处理高级场景

以下是一些您可能觉得有用的附加功能：

#### 美化 JSON 输出

为了可读的 JSON 输出，使用 `writerWithDefaultPrettyPrinter`：

```java
String prettyJson = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(obj);
```

**输出**：

```json
{
  "field1" : "value1",
  "field2" : 123
}
```

#### 忽略未知属性

如果 JSON 包含 Java 类中不存在的字段，配置 `ObjectMapper` 忽略它们：

```java
mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
```

#### 处理文件

从文件读取或写入文件：

```java
// 写入文件
mapper.writeValue(new File("output.json"), obj);

// 从文件读取
MyClass obj = mapper.readValue(new File("input.json"), MyClass.class);
```

#### 处理列表或泛型

对于集合，使用 `TypeReference` 保留泛型类型信息：

```java
import com.fasterxml.jackson.core.type.TypeReference;
import java.util.List;

List<MyClass> list = mapper.readValue(json, new TypeReference<List<MyClass>>() {});
```

---

### 7. 使用 `JsonNode` 进行动态 JSON 操作

如果不想将 JSON 映射到特定类，可以使用 `JsonNode` 进行基于树的操作：

```java
import com.fasterxml.jackson.databind.JsonNode;

JsonNode node = mapper.readTree("{\"field1\":\"value1\",\"field2\":123}");
String value = node.get("field1").asText(); // 返回 "value1"
```

您还可以动态构建 JSON：

```java
import com.fasterxml.jackson.databind.node.ObjectNode;

ObjectNode node = mapper.createObjectNode();
node.put("field1", "value1");
node.put("field2", 123);
String json = mapper.writeValueAsString(node);
```

---

### 总结

要使用 `com.fasterxml.jackson` 包：

1. 将 `jackson-databind` 依赖项添加到 `pom.xml`。
2. 创建单个 `ObjectMapper` 实例以供重用。
3. 使用 `writeValueAsString` 将 Java 对象转换为 JSON，使用 `readValue` 将 JSON 转换为 Java 对象。
4. 使用注解如 `@JsonProperty`、`@JsonIgnore` 和 `@JsonFormat` 自定义行为。
5. 处理异常（例如 `JsonProcessingException`）并根据特定需求配置 `ObjectMapper`（例如忽略未知属性）。
6. 探索高级功能，如美化输出、文件 I/O 或使用 `JsonNode` 进行动态 JSON 处理。

通过以上步骤，您可以使用 Jackson 库在 Java 应用程序中有效地处理 JSON。
