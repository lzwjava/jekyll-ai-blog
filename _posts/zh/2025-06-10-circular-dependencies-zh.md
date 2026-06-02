---
audio: false
generated: true
lang: zh
layout: post
title: Spring循环依赖解析
translated: true
type: note
---

Spring或Spring Boot中的循环依赖是指两个或多个Bean在初始化过程中直接或间接相互依赖的情况。这会形成一个循环链，导致Spring的依赖注入机制无法解析依赖关系——因为每个Bean都要求对方先完成初始化。该问题通常出现在Spring应用上下文的Bean创建过程中，并引发`BeanCurrentlyInCreationException`异常。

### 循环依赖的成因
Spring通过依赖注入容器管理Bean，通常根据依赖关系按特定顺序创建Bean。当Bean以循环方式相互引用时（例如Bean A依赖Bean B，Bean B又依赖Bean A），Spring会在初始化过程中陷入无限循环而无法完成实例化。这种情况在组件高度耦合的复杂应用中尤为常见。

以下场景更容易出现循环依赖：
1. **构造器注入**：通过构造器装配Bean时，Spring必须在实例化阶段解析依赖，若Bean相互引用则会引发循环问题
2. **字段/Setter注入与立即初始化**：当单例Bean采用立即初始化（默认行为）时，Spring会立即解析依赖关系，从而暴露循环依赖
3. **配置错误或过度复杂的Bean关系**：糟糕的设计或关注点分离不足可能导致意外循环
4. **注解使用**：在紧密耦合的组件中使用`@Autowired`或`@Component`等自动注入注解可能无意间形成循环

### 典型循环依赖场景

#### 场景1：构造器注入循环
```java
@Component
public class BeanA {
    private final BeanB beanB;

    @Autowired
    public BeanA(BeanB beanB) {
        this.beanB = beanB;
    }
}

@Component
public class BeanB {
    private final BeanA beanA;

    @Autowired
    public BeanB(BeanA beanA) {
        this.beanA = beanA;
    }
}
```
**问题**：`BeanA`的构造器需要`BeanB`，而`BeanB`的构造器又需要`BeanA`。由于双方都要求对方先完成初始化，Spring无法创建任一Bean。

**报错**：`BeanCurrentlyInCreationException: 创建名为'beanA'的Bean时出错：请求的Bean正在创建中：是否存在无法解析的循环引用？`

#### 场景2：字段注入循环
```java
@Component
public class BeanA {
    @Autowired
    private BeanB beanB;
}

@Component
public class BeanB {
    @Autowired
    private BeanA beanA;
}
```
**问题**：虽然字段注入比构造器注入更灵活，但当两个Bean都是单例（默认作用域）时，Spring在初始化过程中仍会检测到循环依赖。

#### 场景3：间接循环依赖
```java
@Component
public class BeanA {
    @Autowired
    private BeanB beanB;
}

@Component
public class BeanB {
    @Autowired
    private BeanC beanC;
}

@Component
public class BeanC {
    @Autowired
    private BeanA beanA;
}
```
**问题**：`BeanA`→`BeanB`→`BeanC`→`BeanA`形成依赖循环。这种间接依赖更隐蔽，但会导致相同问题。

#### 场景4：配置类循环引用
```java
@Configuration
public class ConfigA {
    @Autowired
    private ConfigB configB;

    @Bean
    public ServiceA serviceA() {
        return new ServiceA(configB);
    }
}

@Configuration
public class ConfigB {
    @Autowired
    private ConfigA configA;

    @Bean
    public ServiceB serviceB() {
        return new ServiceB(configA);
    }
}
```
**问题**：配置类`ConfigA`和`ConfigB`相互依赖，在Spring初始化这些类中定义的Bean时会产生循环。

### Spring Boot中的常见诱因
- **自动配置**：当自定义Bean与自动配置的Bean交互时，可能引发依赖循环
- **组件扫描**：过度使用`@ComponentScan`或配置不当可能引入意外Bean导致循环
- **紧耦合设计**：业务逻辑中服务层、仓储层或控制层的紧耦合易产生循环
- **原型作用域误用**：虽然原型作用域Bean有时可避免循环依赖，但与单例Bean混合使用仍可能出问题

### 解决方案
1. **使用`@Lazy`注解**：
   - 在某个依赖上添加`@Lazy`延迟初始化
   ```java
   @Component
   public class BeanA {
       @Autowired
       @Lazy
       private BeanB beanB;
   }
   ```
   通过允许`BeanA`在`BeanB`解析前部分初始化来打破循环

2. **改用Setter/字段注入**：
   - 将构造器注入改为Setter注入，允许Spring先初始化Bean再注入依赖
   ```java
   @Component
   public class BeanA {
       private BeanB beanB;

       @Autowired
       public void setBeanB(BeanB beanB) {
           this.beanB = beanB;
       }
   }
   ```

3. **代码重构解耦**：
   - 引入接口或中间组件解耦Bean
   ```java
   public interface Service {
       void performAction();
   }

   @Component
   public class BeanA implements Service {
       @Autowired
       private BeanB beanB;

       public void performAction() {
           // 业务逻辑
       }
   }

   @Component
   public class BeanB {
       @Autowired
       private Service service; // 依赖接口而非直接依赖BeanA
   }
   ```

4. **使用`@DependsOn`注解**：
   - 显式控制Bean初始化顺序
   ```java
   @Component
   @DependsOn("beanB")
   public class BeanA {
       @Autowired
       private BeanB beanB;
   }
   ```

5. **启用代理机制**：
   - 通过`@EnableAspectJAutoProxy`确保Spring使用代理（CGLIB或JDK动态代理）处理依赖

6. **重新评估设计**：
   - 循环依赖常暗示设计缺陷，可考虑遵循单一职责原则或依赖倒置原则重构

### 调试技巧
- **查看堆栈跟踪**：`BeanCurrentlyInCreationException`的堆栈会显示参与循环的Bean
- **启用调试日志**：设置`spring.main.lazy-initialization=true`或启用`org.springframework`包的调试日志
- **使用工具**：Spring Boot Actuator或IDE插件（如Spring Tools Suite）可可视化Bean依赖关系

### 预防措施
- **遵循最佳实践**：通过接口或抽象减少紧耦合
- **模块化设计**：将大型应用拆分为松散耦合的小模块
- **早期测试**：通过集成测试在开发阶段发现循环依赖
- **限制组件扫描**：精确配置`@ComponentScan`范围避免引入不必要Bean

### 不易出现循环依赖的场景
- **原型作用域**：按需创建的原型作用域Bean可降低循环概率（但非完全避免）
- **延迟初始化**：全局延迟初始化（`spring.main.lazy-initialization=true`）可延缓Bean创建，但可能掩盖问题本质

### 总结
Spring/Spring Boot中的循环依赖源于Bean间的紧耦合，常由构造器注入或复杂配置加剧。常用解决方案包括使用`@Lazy`注解、改用Setter/字段注入或通过重构打破循环。理解根本原因并应用最佳实践能有效预防和解决此类问题。如果您遇到具体循环依赖案例，欢迎分享相关代码或错误详情，我将协助进一步分析！
