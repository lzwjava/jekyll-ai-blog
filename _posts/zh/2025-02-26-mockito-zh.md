---
audio: false
generated: true
lang: zh
layout: post
title: Java测试中Mockito的使用
translated: true
type: note
---

在 Java 测试中使用 Mockito 时，请按照以下步骤创建模拟对象、桩方法及验证交互：

### 1. **添加依赖**

在 `pom.xml` (Maven) 中包含 Mockito 和 JUnit：

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>5.3.1</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.2</version>
    <scope>test</scope>
</dependency>
```

### 2. **设置测试类**

结合 JUnit 5 使用 Mockito 扩展：

```java
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class UserServiceTest {
    // ...
}
```

### 3. **创建模拟对象并注入依赖**

- 使用 `@Mock` 标注需要模拟的依赖项
- 使用 `@InjectMocks` 将模拟对象注入被测试类

```java
@Mock
private UserRepository userRepository;

@InjectMocks
private UserService userService; // UserService 依赖 UserRepository
```

### 4. **桩方法调用**

使用 `when().thenReturn()` 定义模拟行为：

```java
@Test
void getUserById_ReturnsUser_WhenUserExists() {
    User mockUser = new User(1L, "Alice");
    // 对仓库方法进行桩设置
    when(userRepository.findById(1L)).thenReturn(mockUser);

    User result = userService.getUserById(1L);

    assertEquals("Alice", result.getName());
}
```

### 5. **验证交互**

检查模拟方法是否按预期被调用：

```java
@Test
void getUserById_CallsRepository() {
    userService.getUserById(1L);
    // 验证仓库方法被调用一次且参数为 ID 1
    verify(userRepository, times(1)).findById(1L);
}
```

---

### **常见使用场景**

#### **桩异常抛出**

```java
@Test
void getUserById_ThrowsException_WhenRepositoryFails() {
    when(userRepository.findById(anyLong())).thenThrow(new RuntimeException("数据库错误"));

    assertThrows(RuntimeException.class, () -> userService.getUserById(1L));
}
```

#### **参数匹配器**

使用 `any()`, `eq()` 等实现灵活参数匹配：

```java
when(userRepository.findById(anyLong())).thenReturn(new User(1L, "Bob"));
```

#### **BDD（行为驱动开发）风格**

使用 `given().willReturn()` 提升可读性：

```java
import static org.mockito.BDDMockito.*;

@Test
void bddStyleExample() {
    given(userRepository.findById(1L)).willReturn(new User(1L, "Alice"));

    User result = userService.getUserById(1L);

    then(userRepository).should().findById(1L);
    assertEquals("Alice", result.getName());
}
```

#### **参数捕获器**

捕获参数以执行详细断言：

```java
@Test
void saveUser_CapturesArgument() {
    ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);

    userService.saveUser("Charlie");

    verify(userRepository).save(userCaptor.capture());
    assertEquals("Charlie", userCaptor.getValue().getName());
}
```

---

### **关键要点**

- **初始化**：使用 `@ExtendWith(MockitoExtension.class)`（JUnit 5）或在 `@BeforeEach` 中使用 `MockitoAnnotations.openMocks(this)`
- **静态模拟**：使用 `mockito-inline` 依赖项来模拟静态方法/构造器
- **监视对象**：使用 `@Spy` 包装真实对象（部分模拟）

### **故障排除**

- **空模拟对象**：确保模拟对象已完成初始化（使用 `@ExtendWith` 或 `openMocks()`）
- **桩设置错误**：在测试调用方法前完成桩设置

进阶用法请参阅 [Mockito 官方文档](https://site.mockito.org/)。
