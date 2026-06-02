---
audio: false
generated: true
lang: zh
layout: post
title: Javax JSON 处理
translated: true
type: note
---

我将解释如何使用 `javax.json` 包（Java API for JSON Processing 的一部分）来处理 Java 中的 JSON 数据。以下是详细指南：

1. 首先，在项目中添加依赖（如果使用 Maven）：
```xml
<dependency>
    <groupId>javax.json</groupId>
    <artifactId>javax.json-api</artifactId>
    <version>1.1.4</version>
</dependency>
<!-- 实现（如 GlassFish） -->
<dependency>
    <groupId>org.glassfish</groupId>
    <artifactId>javax.json</artifactId>
    <version>1.1.4</version>
</dependency>
```

2. 使用 `javax.json` 的基础示例：

a) 创建 JSON 对象：
```java
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonArray;

public class JsonExample {
    public static void main(String[] args) {
        // 创建 JSON 对象
        JsonObject jsonObject = Json.createObjectBuilder()
            .add("name", "John Doe")
            .add("age", 30)
            .add("isStudent", false)
            .add("address", Json.createObjectBuilder()
                .add("street", "123 Main St")
                .add("city", "New York"))
            .build();

        System.out.println(jsonObject.toString());
    }
}
```

b) 创建 JSON 数组：
```java
JsonArray jsonArray = Json.createArrayBuilder()
    .add("Apple")
    .add("Banana")
    .add(Json.createObjectBuilder()
        .add("name", "Orange")
        .add("price", 0.99))
    .build();
```

c) 从字符串解析 JSON：
```java
import javax.json.JsonReader;
import java.io.StringReader;

String jsonString = "{\"name\":\"Jane\",\"age\":25}";
JsonReader jsonReader = Json.createReader(new StringReader(jsonString));
JsonObject parsedObject = jsonReader.readObject();
jsonReader.close();

// 访问值
String name = parsedObject.getString("name");
int age = parsedObject.getInt("age");
```

d) 将 JSON 写入字符串：
```java
import javax.json.JsonWriter;
import java.io.StringWriter;

JsonObject jsonObject = Json.createObjectBuilder()
    .add("title", "Example")
    .build();

StringWriter stringWriter = new StringWriter();
JsonWriter jsonWriter = Json.createWriter(stringWriter);
jsonWriter.writeObject(jsonObject);
jsonWriter.close();

String result = stringWriter.toString();
```

3. 关键类和接口：
- `Json`：创建 JSON 构建器和读取器的工厂类
- `JsonObject`：表示 JSON 对象
- `JsonArray`：表示 JSON 数组
- `JsonObjectBuilder`：构建 JSON 对象
- `JsonArrayBuilder`：构建 JSON 数组
- `JsonReader`：从输入源读取 JSON
- `JsonWriter`：将 JSON 写入输出源

4. 处理不同的 JSON 值类型：
```java
JsonObject obj = // ... 某个 JSON 对象
String stringValue = obj.getString("key");
int intValue = obj.getInt("key");
boolean boolValue = obj.getBoolean("key");
JsonObject nestedObj = obj.getJsonObject("key");
JsonArray arrayValue = obj.getJsonArray("key");

// 检查键是否存在并处理 null
if (obj.containsKey("key") && !obj.isNull("key")) {
    String value = obj.getString("key");
}
```

5. 流式 API 示例（用于大型 JSON）：
```java
import javax.json.stream.JsonParser;
import java.io.StringReader;

String json = "{\"name\":\"John\",\"scores\":[1,2,3]}";
JsonParser parser = Json.createParser(new StringReader(json));
while (parser.hasNext()) {
    JsonParser.Event event = parser.next();
    switch (event) {
        case KEY_NAME:
            System.out.println("键: " + parser.getString());
            break;
        case VALUE_STRING:
            System.out.println("字符串: " + parser.getString());
            break;
        case VALUE_NUMBER:
            System.out.println("数字: " + parser.getBigDecimal());
            break;
    }
}
parser.close();
```

提示：
- 使用完毕后始终关闭 `JsonReader`、`JsonWriter` 和 `JsonParser`
- 处理 `javax.json.JsonException` 以应对可能的解析错误
- 对于大型 JSON 文档使用流式 API（`JsonParser`）
- 该 API 是不可变的 - 构建器会创建新实例

这涵盖了使用 `javax.json` 的基础知识。如果您需要更具体的示例或有特定用例，请告诉我！
