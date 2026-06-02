---
audio: false
generated: true
lang: en
layout: post
title: Javax Json Processing
translated: false
type: note
---

I'll explain how to use the `javax.json` package, which is part of the Java API for JSON Processing (JSON-P) to work with JSON data in Java. Here's a comprehensive guide:

1. First, add the dependency to your project (if using Maven):
```xml
<dependency>
    <groupId>javax.json</groupId>
    <artifactId>javax.json-api</artifactId>
    <version>1.1.4</version>
</dependency>
<!-- Implementation (like GlassFish) -->
<dependency>
    <groupId>org.glassfish</groupId>
    <artifactId>javax.json</artifactId>
    <version>1.1.4</version>
</dependency>
```

2. Basic examples of using `javax.json`:

a) Creating a JSON Object:
```java
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonArray;

public class JsonExample {
    public static void main(String[] args) {
        // Create a JSON object
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

b) Creating a JSON Array:
```java
JsonArray jsonArray = Json.createArrayBuilder()
    .add("Apple")
    .add("Banana")
    .add(Json.createObjectBuilder()
        .add("name", "Orange")
        .add("price", 0.99))
    .build();
```

c) Parsing JSON from String:
```java
import javax.json.JsonReader;
import java.io.StringReader;

String jsonString = "{\"name\":\"Jane\",\"age\":25}";
JsonReader jsonReader = Json.createReader(new StringReader(jsonString));
JsonObject parsedObject = jsonReader.readObject();
jsonReader.close();

// Access values
String name = parsedObject.getString("name");
int age = parsedObject.getInt("age");
```

d) Writing JSON to String:
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

3. Key Classes and Interfaces:
- `Json`: Factory class for creating JSON builders and readers
- `JsonObject`: Represents a JSON object
- `JsonArray`: Represents a JSON array
- `JsonObjectBuilder`: Builds JSON objects
- `JsonArrayBuilder`: Builds JSON arrays
- `JsonReader`: Reads JSON from input source
- `JsonWriter`: Writes JSON to output source

4. Handling different JSON value types:
```java
JsonObject obj = // ... some JSON object
String stringValue = obj.getString("key");
int intValue = obj.getInt("key");
boolean boolValue = obj.getBoolean("key");
JsonObject nestedObj = obj.getJsonObject("key");
JsonArray arrayValue = obj.getJsonArray("key");

// Check if key exists and handle null
if (obj.containsKey("key") && !obj.isNull("key")) {
    String value = obj.getString("key");
}
```

5. Streaming API example (for large JSON):
```java
import javax.json.stream.JsonParser;
import java.io.StringReader;

String json = "{\"name\":\"John\",\"scores\":[1,2,3]}";
JsonParser parser = Json.createParser(new StringReader(json));
while (parser.hasNext()) {
    JsonParser.Event event = parser.next();
    switch (event) {
        case KEY_NAME:
            System.out.println("Key: " + parser.getString());
            break;
        case VALUE_STRING:
            System.out.println("String: " + parser.getString());
            break;
        case VALUE_NUMBER:
            System.out.println("Number: " + parser.getBigDecimal());
            break;
    }
}
parser.close();
```

Tips:
- Always close `JsonReader`, `JsonWriter`, and `JsonParser` when done
- Handle `javax.json.JsonException` for potential parsing errors
- Use the streaming API (`JsonParser`) for large JSON documents
- The API is immutable - builders create new instances

This covers the basics of using `javax.json`. Let me know if you need more specific examples or have a particular use case in mind!
