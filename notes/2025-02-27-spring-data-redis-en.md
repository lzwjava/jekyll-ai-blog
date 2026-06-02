---
audio: false
generated: true
lang: en
layout: post
title: Spring Data Redis
translated: false
type: note
---

Spring Data Redis is a fantastic tool for integrating Redis—a high-performance, in-memory data store—into your Spring application. It simplifies working with Redis by providing a familiar repository-style interface and abstractions over low-level Redis operations. Let’s walk through how to set it up and use it step-by-step.

### 1. **Set Up Your Project**

First, include the Spring Data Redis dependency in your project. If you’re using Maven, add this to your `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

For Gradle, use:

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
```

This includes the Redis client (Jedis or Lettuce—Lettuce is the default). If you prefer Jedis, you can add it explicitly and exclude Lettuce:

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

### 2. **Configure Redis**

Configure your Redis connection in `application.properties` or `application.yml`. For a local Redis instance running on the default port (6379):

```properties
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password= # Optional, if your Redis server has a password
spring.redis.database=0 # Default database index
```

If you’re using a remote Redis server or a service like AWS ElastiCache, update the host and credentials accordingly.

### 3. **Basic Usage with RedisTemplate**

Spring Data Redis provides `RedisTemplate` for low-level operations. You can autowire it into your service or component:

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

- `RedisTemplate` is generic: `<String, String>` means keys and values are strings. You can use other types (e.g., `<String, Object>`).
- `opsForValue()` is for simple key-value operations. Other methods include `opsForList()`, `opsForSet()`, `opsForHash()`, etc., for different Redis data structures.

### 4. **Using with Objects**

To store and retrieve Java objects, configure `RedisTemplate` with serializers. Spring Boot auto-configures it, but you can customize it if needed:

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

Now you can store and retrieve objects:

```java
public class Person {
    private String firstName;
    private String lastName;

    // Default constructor (for deserialization)
    public Person() {}

    public Person(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    // Getters and setters
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

### 5. **Repository Approach**

For a higher-level abstraction, use Spring Data Redis repositories. Define an entity and a repository:

```java
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@RedisHash("Person") // Maps to a Redis hash with prefix "Person"
public class Person {
    @Id
    private String id; // Redis key will be "Person:<id>"
    private String firstName;
    private String lastName;

    // Constructors, getters, setters (as above)
}
```

```java
import org.springframework.data.repository.CrudRepository;

public interface PersonRepository extends CrudRepository<Person, String> {
}
```

Use it like this:

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
        System.out.println("Saved person with ID: " + person.getId());
    }

    public void findPerson(String id) {
        Person person = repository.findById(id).orElse(null);
        if (person != null) {
            System.out.println(person.getFirstName() + " " + person.getLastName());
        }
    }
}
```

- `@RedisHash` maps the entity to a Redis hash.
- The repository provides CRUD operations out of the box.

### 6. **Run Your Application**

Ensure Redis is running locally (e.g., via Docker: `docker run -d -p 6379:6379 redis`) or connect to a remote instance. Then start your Spring Boot app:

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

### 7. **Advanced Features**

- **TTL (Time-to-Live):** Set expiration on keys with `redisTemplate.expire(key, 10, TimeUnit.MINUTES)`.
- **Hashes:** Use `opsForHash()` to work with Redis hashes directly.
- **Pub/Sub:** Use `RedisMessageListenerContainer` for messaging.

### Example Workflow

1. Save a `Person` object with `repository.save()` or `redisTemplate.opsForValue().set()`.
2. Retrieve it with `repository.findById()` or `redisTemplate.opsForValue().get()`.
3. Check your Redis instance (e.g., with `redis-cli`) to see the data.

This covers the essentials! If you want to explore caching, pub/sub, or something specific, let me know what you’re aiming for, and I’ll dive deeper. How does this fit with what you’re trying to do?
