---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot Java 编码规范
translated: true
type: note
---

## 1. 核心原则

- 遵循标准的 Java 代码规范
- 优先考虑可读性和可维护性
- 保持 Spring 生态系统内的一致性
- 符合 Java 核心最佳实践

## 2. 代码格式化

### 通用指南

- 使用 IntelliJ IDEA 默认格式化设置
- 4 空格缩进（不使用制表符）
- 最大行长度为 120 个字符
- 使用标准 Java 大括号风格

### 具体格式化规则

- 方法之间用空行分隔
- 不留尾随空格
- 使用 Unix 风格的行结束符（LF）

## 3. 命名规范

### 类命名

- 使用描述性、有意义的名称
- 使用大驼峰命名法
- 示例：
  - `ConfigurationProperties`
  - `AutoConfigurationImportSelector`
  - `SpringApplication`

### 方法命名

- 使用小驼峰命名法
- 动词或动词短语
- 示例：
  - `configure()`
  - `registerBeanDefinitions()`
  - `isEnabledByDefault()`

## 4. 注解实践

### 注解顺序

- 标准注解顺序：
  1. 重写注解（`@Override`）
  2. 作用域注解（`@Component`、`@Service`）
  3. 依赖注入注解
  4. 事务注解
  5. 自定义项目注解

### 注解位置

```java
@Component
@Transactional
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

## 5. 依赖注入

### 首选注入方式

- 构造函数注入
- 避免字段注入
- 在构造函数上使用 `@Autowired`

```java
@Service
public class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}
```

## 6. 日志记录

- 使用 SLF4J 进行日志记录
- 使用 `private static final Logger` 或 Lombok 的 `@Slf4j`

```java
@Slf4j
@Service
public class UserService {
    public void processUser(User user) {
        log.info("正在处理用户：{}", user.getUsername());
    }
}
```

## 7. 错误处理

- 使用特定异常类型
- 提供有意义的错误信息
- 使用 `@ControllerAdvice` 进行全局异常处理

## 8. 配置

- 优先使用 `application.yml` 而非 `application.properties`
- 使用特定环境的配置文件
- 外部化配置值

## 9. 测试

- 使用 JUnit 5
- 利用 Spring Boot 测试工具
- 遵循 Arrange-Act-Assert 模式

## 10. 附加资源

- [Spring Boot GitHub 编码风格](https://github.com/spring-projects/spring-boot/blob/main/CONTRIBUTING.md)
- [Spring Framework 指南](https://github.com/spring-projects/spring-framework/wiki/Code-Style)
