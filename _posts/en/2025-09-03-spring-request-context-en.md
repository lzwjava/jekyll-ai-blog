---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spring Request Context Implementation Options
translated: false
type: note
---

Great use-case for a tiny “request context” in Spring. You’ve got a few clean options—pick one based on your stack:

### 1) Request-scoped bean (simple & safe)

Store the test user id in a request-scoped bean that your `TestUserFilter` sets, and any component can inject/read.

```java
// holds the value for the lifetime of a single HTTP request
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
    chain.doFilter(req, res); // request-scope bean is auto-cleaned after request ends
  }
}
```

Use anywhere:

```java
@Service
public class SomeService {
  private final TestUserContext ctx;
  public SomeService(TestUserContext ctx) { this.ctx = ctx; }
  public void doWork() {
    String testUserId = ctx.getUserId(); // null if not provided
  }
}
```

**Why:** No manual cleanup; works across controllers/services/DAOs within the same request.

---

### 2) Spring Security context (recommended if you already use Spring Security)

Let the filter set an `Authentication` so all components can read it via `SecurityContextHolder` or `@AuthenticationPrincipal`.

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

Use anywhere:

```java
String testUserId = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
```

or inject `Principal`/`Authentication` in controllers.

**Why:** Plays nicely with method security, auditing, logs, etc.

---

### 3) ThreadLocal holder (works without web/security deps; remember to clear)

If you’re not using request scope or Security:

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
      TestUserHolder.clear(); // CRITICAL for pooled threads
    }
  }
}
```

If you run async tasks and need propagation, add a `TaskDecorator` to copy the ThreadLocal.

---

### Quick tips

* Put the id in a header like `X-Test-User-Id` (easy to pass from Postman/MockMvc) or a query param for local testing.
* For unit tests with MockMvc: `.header("X-Test-User-Id", "u123")`.
* Prefer **Option 1** if you want a simple “bag” visible to any bean in the same HTTP request.
* Prefer **Option 2** if you already use Spring Security or want authorization/auditing integration.
* Use **Option 3** only when you don’t want Spring scopes/security; be meticulous about clearing to avoid leaks.
