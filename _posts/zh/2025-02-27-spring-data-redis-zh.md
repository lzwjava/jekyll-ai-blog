---
audio: false
generated: true
lang: zh
layout: post
title: Spring Data Redis
translated: true
type: note
---

Spring Data Redis 是将高性能内存数据库 Redis 集成到 Spring 应用中的绝佳工具。它通过提供熟悉的存储库风格接口和对底层 Redis 操作的抽象，简化了 Redis 的使用流程。下面我们来逐步讲解如何配置和使用它。

### 1. **项目配置**
首先在项目中添加 Spring Data Redis 依赖。如果使用 Maven，请在 `pom.xml` 中添加：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

如果使用 Gradle，请添加：

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
```

这会包含 Redis 客户端（默认使用 Lettuce）。若需使用 Jedis，可显式添加并排除 Lettuce：

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
    <exclusions>
        <exclusion>
            <groupId>io.lettuce</groupId>
            <artifactId>lettuce-core</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

### 2. **Redis 配置**
在 `application.properties` 或 `application.yml` 中配置 Redis 连接。对于运行在默认端口（6379）的本地 Redis 实例：

```properties
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password= # 可选，如果 Redis 服务器设置了密码
spring.redis.database=0 # 默认数据库索引
```

如果使用远程 Redis 服务器或 AWS ElastiCache 等服务，请相应更新主机地址和认证信息。

### 3. **使用 RedisTemplate 基础操作**
Spring Data Redis 提供 `RedisTemplate` 进行底层操作。可将其自动注入服务或组件：

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

@Service
public class RedisService {
    private final RedisTemplate<String, String> redisTemplate;

    @Autowired
    public RedisService(RedisTemplate<String, String> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public void saveData(String key, String value) {
        redisTemplate.opsForValue().set(key, value);
    }

    public String getData(String key) {
        return redisTemplate.opsForValue().get(key);
    }
}
```

- `RedisTemplate` 支持泛型：`<String, String>` 表示键值均为字符串类型，也可使用其他类型（如 `<String, Object>`）
- `opsForValue()` 用于基础键值操作，还提供 `opsForList()`、`opsForSet()`、`opsForHash()` 等方法操作不同 Redis 数据结构

### 4. **对象存储操作**
如需存储 Java 对象，需为 `RedisTemplate` 配置序列化器。Spring Boot 会自动配置，也可按需自定义：

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new Jackson2JsonRedisSerializer<>(Object.class));
        template.afterPropertiesSet();
        return template;
    }
}
```

现在即可进行对象存储：

```java
public class Person {
    private String firstName;
    private String lastName;

    // 默认构造函数（用于反序列化）
    public Person() {}

    public Person(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    // Getter 和 Setter
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
}
```

```java
@Service
public class PersonRedisService {
    private final RedisTemplate<String, Object> redisTemplate;

    @Autowired
    public PersonRedisService(RedisTemplate<String, Object> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public void savePerson(String key, Person person) {
        redisTemplate.opsForValue().set(key, person);
    }

    public Person getPerson(String key) {
        return (Person) redisTemplate.opsForValue().get(key);
    }
}
```

### 5. **存储库模式**
如需更高级的抽象，可使用 Spring Data Redis 存储库。定义实体和存储库：

```java
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@RedisHash("Person") // 映射到前缀为 "Person" 的 Redis 哈希
public class Person {
    @Id
    private String id; // Redis 键格式为 "Person:<id>"
    private String firstName;
    private String lastName;

    // 构造函数、getter、setter（同上）
}
```

```java
import org.springframework.data.repository.CrudRepository;

public interface PersonRepository extends CrudRepository<Person, String> {
}
```

使用示例：

```java
@Service
public class PersonService {
    private final PersonRepository repository;

    @Autowired
    public PersonService(PersonRepository repository) {
        this.repository = repository;
    }

    public void savePerson() {
        Person person = new Person("John", "Doe");
        repository.save(person);
        System.out.println("已保存人员 ID: " + person.getId());
    }

    public void findPerson(String id) {
        Person person = repository.findById(id).orElse(null);
        if (person != null) {
            System.out.println(person.getFirstName() + " " + person.getLastName());
        }
    }
}
```

- `@RedisHash` 将实体映射到 Redis 哈希结构
- 存储库提供开箱即用的 CRUD 操作

### 6. **运行应用**
确保 Redis 在本地运行（例如通过 Docker：`docker run -d -p 6379:6379 redis`）或连接到远程实例。然后启动 Spring Boot 应用：

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 7. **高级功能**
- **TTL（生存时间）：** 通过 `redisTemplate.expire(key, 10, TimeUnit.MINUTES)` 设置键过期
- **哈希操作：** 使用 `opsForHash()` 直接操作 Redis 哈希
- **发布/订阅：** 使用 `RedisMessageListenerContainer` 实现消息功能

### 操作示例
1. 使用 `repository.save()` 或 `redisTemplate.opsForValue().set()` 保存 `Person` 对象
2. 通过 `repository.findById()` 或 `redisTemplate.opsForValue().get()` 检索数据
3. 使用 `redis-cli` 检查 Redis 实例中的数据

以上涵盖了核心功能！如果您需要了解缓存、发布/订阅等特定功能，请告诉我您的具体需求，我将深入讲解。这些内容是否符合您的预期？
