---
audio: false
generated: true
lang: en
layout: post
title: Using FastJson
translated: false
type: note
---

FastJSON is a high-performance JSON processing library for Java, developed by Alibaba. It’s widely used for parsing JSON strings into Java objects, serializing Java objects into JSON, and handling JSON data efficiently. Below is a guide on how to use FastJSON based on its core features.

### Step 1: Add FastJSON to Your Project
To use FastJSON, you need to include it in your project. If you're using Maven, add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>2.0.51</version> <!-- Use the latest version available -->
</dependency>
```

For Gradle, add this to your `build.gradle`:

```gradle
implementation 'com.alibaba:fastjson:2.0.51'
```

Check the [Maven Central Repository](https://mvnrepository.com/artifact/com.alibaba/fastjson) for the latest version.

### Step 2: Basic Usage
Here’s how to use FastJSON for common tasks like serialization and deserialization.

#### 1. **Serializing Java Objects to JSON**
You can convert a Java object to a JSON string using `JSON.toJSONString()`.

```java
import com.alibaba.fastjson.JSON;

public class Main {
    public static void main(String[] args) {
        // Create a sample object
        User user = new User("Alice", 25);

        // Serialize to JSON string
        String jsonString = JSON.toJSONString(user);
        System.out.println(jsonString);
    }
}

// Sample User class
class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Getters and setters (required for FastJSON to work properly)
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}
```

**Output:**
```json
{"age":25,"name":"Alice"}
```

#### 2. **Deserializing JSON to Java Objects**
You can parse a JSON string back into a Java object using `JSON.parseObject()`.

```java
import com.alibaba.fastjson.JSON;

public class Main {
    public static void main(String[] args) {
        String jsonString = "{\"age\":25,\"name\":\"Alice\"}";

        // Deserialize to User object
        User user = JSON.parseObject(jsonString, User.class);
        System.out.println("Name: " + user.getName() + ", Age: " + user.getAge());
    }
}
```

**Output:**
```
Name: Alice, Age: 25
```

#### 3. **Parsing JSON into a List**
If your JSON represents a list of objects, use `JSON.parseArray()`.

```java
import com.alibaba.fastjson.JSON;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        String jsonArray = "[{\"name\":\"Alice\",\"age\":25},{\"name\":\"Bob\",\"age\":30}]";

        // Deserialize to List<User>
        List<User> users = JSON.parseArray(jsonArray, User.class);
        for (User user : users) {
            System.out.println("Name: " + user.getName() + ", Age: " + user.getAge());
        }
    }
}
```

**Output:**
```
Name: Alice, Age: 25
Name: Bob, Age: 30
```

### Step 3: Advanced Features
FastJSON offers additional customization options:

#### 1. **Customizing Serialization**
You can control how fields are serialized using `SerializerFeature` options.

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;

public class Main {
    public static void main(String[] args) {
        User user = new User("Alice", 25);

        // Use PrettyFormat for readable output
        String jsonString = JSON.toJSONString(user, SerializerFeature.PrettyFormat);
        System.out.println(jsonString);
    }
}
```

**Output:**
```json
{
	"age":25,
	"name":"Alice"
}
```

Common `SerializerFeature` options:
- `WriteNullListAsEmpty`: Empty lists are written as `[]` instead of `null`.
- `WriteMapNullValue`: Include fields with `null` values in the output.

#### 2. **Handling Complex Objects**
For nested objects, ensure the inner classes have proper getters/setters.

```java
import com.alibaba.fastjson.JSON;

public class Main {
    public static void main(String[] args) {
        Address address = new Address("123 Main St", "NY");
        User user = new User("Alice", 25, address);

        String jsonString = JSON.toJSONString(user);
        System.out.println(jsonString);

        User parsedUser = JSON.parseObject(jsonString, User.class);
        System.out.println(parsedUser.getAddress().getCity());
    }
}

class User {
    private String name;
    private int age;
    private Address address;

    public User(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public Address getAddress() { return address; }
    public void setAddress(Address address) { this.address = address; }
}

class Address {
    private String street;
    private String city;

    public Address(String street, String city) {
        this.street = street;
        this.city = city;
    }

    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = street; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
}
```

**Output:**
```json
{"address":{"city":"NY","street":"123 Main St"},"age":25,"name":"Alice"}
NY
```

### Step 4: Notes and Best Practices
- **Security**: FastJSON has had vulnerabilities in older versions (e.g., remote code execution). Always use the latest version and avoid enabling `Feature.SupportAutoType` unless necessary.
- **Performance**: FastJSON is optimized for speed, but test it with your specific use case for large datasets.
- **Documentation**: Refer to the official [FastJSON GitHub page](https://github.com/alibaba/fastjson) for more details.

Let me know if you need help with a specific use case or troubleshooting!
