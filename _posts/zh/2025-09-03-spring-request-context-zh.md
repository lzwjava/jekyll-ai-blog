---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Spring请求上下文实现方案
translated: true
type: note
---

Spring框架中微型"请求上下文"的绝佳应用场景。根据技术栈可选择以下几种简洁方案：

### 1) 请求作用域Bean（简单安全）

将测试用户ID存储在请求作用域的Bean中，由`TestUserFilter`设置，任何组件均可注入读取。

```java
// 在单个HTTP请求生命周期内保持值
@Component
@RequestScope
public class TestUserContext {
  private String userId;
  public String getUserId() { return userId; }
  public void setUserId(String userId) { this.userId = userId; }
}
```

```java
@Component
public class TestUserFilter extends OncePerRequestFilter {
  private final TestUserContext ctx;
  public TestUserFilter(TestUserContext ctx) { this.ctx = ctx; }

  @Override
  protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
      throws ServletException, IOException {
    String id = req.getHeader("X-Test-User-Id");
    if (id == null) id = req.getParameter("testUserId");
    if (id != null && !id.isBlank()) ctx.setUserId(id);
    chain.doFilter(req, res); // 请求结束后请求作用域Bean自动清理
  }
}
```

任意位置使用：

```java
@Service
public class SomeService {
  private final TestUserContext ctx;
  public SomeService(TestUserContext ctx) { this.ctx = ctx; }
  public void doWork() {
    String testUserId = ctx.getUserId(); // 未提供时返回null
  }
}
```

**优势：** 无需手动清理；同一请求内的控制器/服务/DAO层均可访问。

---

### 2) Spring Security上下文（若已使用Spring Security推荐此方案）

通过过滤器设置`Authentication`，所有组件可通过`SecurityContextHolder`或`@AuthenticationPrincipal`读取。

```java
@Component
public class TestUserFilter extends OncePerRequestFilter {
  @Override
  protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    String id = req.getHeader("X-Test-User-Id");
    if (id == null) id = req.getParameter("testUserId");

    if (id != null && !id.isBlank()) {
      var auth = new UsernamePasswordAuthenticationToken(
          id, "N/A", List.of(new SimpleGrantedAuthority("ROLE_TEST")));
      SecurityContextHolder.getContext().setAuthentication(auth);
    }
    try {
      chain.doFilter(req, res);
    } finally {
      SecurityContextHolder.clearContext();
    }
  }
}
```

任意位置使用：

```java
String testUserId = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
```

或在控制器中注入`Principal`/`Authentication`。

**优势：** 完美兼容方法级安全、审计、日志等功能。

---

### 3) ThreadLocal持有器（无Web/Security依赖时适用；务必记得清理）

未使用请求作用域或Security时的方案：

```java
public final class TestUserHolder {
  private static final ThreadLocal<String> USER_ID = new InheritableThreadLocal<>();
  public static void set(String id) { USER_ID.set(id); }
  public static String get() { return USER_ID.get(); }
  public static void clear() { USER_ID.remove(); }
}
```

```java
@Component
public class TestUserFilter extends OncePerRequestFilter {
  @Override
  protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    String id = req.getHeader("X-Test-User-Id");
    if (id == null) id = req.getParameter("testUserId");
    if (id != null && !id.isBlank()) TestUserHolder.set(id);
    try {
      chain.doFilter(req, res);
    } finally {
      TestUserHolder.clear(); // 对线程池环境至关重要
    }
  }
}
```

若需在异步任务中传递值，可通过`TaskDecorator`复制ThreadLocal。

---

### 实用技巧

* 通过`X-Test-User-Id`请求头（便于Postman/MockMvc传递）或查询参数传递测试ID
* MockMvc单元测试使用：`.header("X-Test-User-Id", "u123")`
* 需要简单"值容器"时优先选择**方案1**
* 已集成Spring Security或需要授权/审计时选择**方案2**
* 仅当不需要Spring作用域/安全功能时使用**方案3**，务必注意清理避免内存泄漏
