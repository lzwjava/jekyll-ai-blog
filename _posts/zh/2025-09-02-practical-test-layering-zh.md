---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实用测试分层指南
translated: true
type: note
---

很好的问题。合理的测试策略主要关乎**风险与反馈速度**。以下是一个实用的方法，用于决定**在哪个层级测试什么**——不用表格，只有清晰的规则和示例。

---

# 核心原则

* **测试行为，而非实现。** 优先使用公共 API 而非私有细节。
* **将大多数检查下推到能捕获错误的最快层级。**
* **仅在风险值得时才使用真实依赖**（数据库、队列、浏览器）。
* **端到端覆盖关键路径，但要节制。** UI 测试最脆弱且最慢；留待真正重要的场景。

---

# 测试内容与层级（快速启发法）

## 1) 单元测试（快速、隔离）

**使用时机：** 纯/领域逻辑无需 I/O（数据库、HTTP、文件系统）即可测试。

* 业务规则、定价/费用计算、验证器、映射器、工具类。
* 服务方法（其仓储/客户端被**模拟**）。
* 目标：大量小测试；在毫秒级内失败。

**Java/Spring 示例**

```java
@ExtendWith(MockitoExtension.class)
class FeeServiceTest {
  @Mock AccountRepo repo;
  @InjectMocks FeeService svc;

  @Test void vipGetsDiscount() {
    when(repo.tier("u1")).thenReturn("VIP");
    assertEquals(Money.of(90), svc.charge("u1", Money.of(100)));
    verify(repo).tier("u1");
  }
}
```

## 2) 集成 / 组件测试（真实装配，最少模拟）

**使用时机：** 需要验证 Spring 装配、序列化、过滤器、数据库查询、事务。

* **无网络的 HTTP 层**：`@WebMvcTest`（控制器 + JSON），或 `@SpringBootTest(webEnvironment=RANDOM_PORT)` 用于完整技术栈。
* **数据库正确性**：使用 **Testcontainers** 运行真实数据库；检查 SQL、索引、迁移。
* **消息传递**：使用真实代理容器（Kafka/RabbitMQ）测试消费者/生产者。

**HTTP 切片示例**

```java
@WebMvcTest(controllers = OrderController.class)
class OrderControllerTest {
  @Autowired MockMvc mvc;
  @MockBean OrderService svc;

  @Test void createsOrder() throws Exception {
    when(svc.create(any())).thenReturn(new Order("id1", 100));
    mvc.perform(post("/orders").contentType("application/json")
        .content("{\"amount\":100}"))
      .andExpect(status().isCreated())
      .andExpect(jsonPath("$.id").value("id1"));
  }
}
```

**使用 Testcontainers 的数据库测试**

```java
@Testcontainers
@SpringBootTest
class RepoIT {
  @Container static PostgreSQLContainer<?> db = new PostgreSQLContainer<>("postgres:16");
  @Autowired OrderRepo repo;

  @Test void persistsAndQueries() {
    var saved = repo.save(new OrderEntity(null, 100));
    assertTrue(repo.findById(saved.getId()).isPresent());
  }
}
```

## 3) API 契约 & 端到端 API 测试

**使用时机：** 必须保证**向后兼容的契约**或完整的系统工作流。

* **契约测试**（例如，OpenAPI 模式验证或 Pact）无需 UI 即可捕获破坏性变更。
* **端到端 API 流程**：使用真实数据库启动应用并通过 HTTP 访问（使用 RestAssured）。专注于快乐路径 + 少量关键边缘情况。

**API E2E 示例**

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class ApiFlowIT {
  @LocalServerPort int port;
  @Test void happyPath() {
    given().port(port).contentType("application/json")
      .body("{\"amount\":100}")
      .when().post("/orders")
      .then().statusCode(201)
      .body("amount", equalTo(100));
  }
}
```

## 4) UI 端到端测试（浏览器）

**使用时机：** 仅有**少量**关键用户旅程必须在真实浏览器中得到验证：

* 认证 + 结账；资金流动；PII 流程；文件上传。
* 限制在 **3–10 个关键场景**。其他所有内容：在单元/集成/API 层进行覆盖。

**Selenium 还是 Playwright/Cypress？**

* **对于现代 Angular 应用，优先选择 Playwright**（或 Cypress）：自动等待、更易用的选择器、并行化、内置的跟踪查看器、在 Chromium/Firefox/WebKit 上稳定的无头运行。
* **如果必须驱动自定义网格中的真实供应商浏览器**，与**遗留/企业**设置交互，或者您已有成熟的 Selenium 基础设施，则**使用 Selenium**。它需要更多配置工作；您将需要显式等待和一个用于提速的网格。

**Playwright (TypeScript) 示例**

```ts
import { test, expect } from '@playwright/test';

test('checkout happy path', async ({ page }) => {
  await page.goto('http://localhost:4200');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.getByLabel('Email').fill('u@example.com');
  await page.getByLabel('Password').fill('secret');
  await page.getByRole('button', { name: 'Login' }).click();

  await page.getByText('Add to cart', { exact: true }).first().click();
  await page.getByRole('button', { name: 'Checkout' }).click();
  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

**如果必须使用 Selenium (Java)**

```java
WebDriver d = new ChromeDriver();
d.get("http://localhost:4200");
new WebDriverWait(d, Duration.ofSeconds(10))
  .until(ExpectedConditions.elementToBeClickable(By.id("loginBtn"))).click();
```

---

# 逐层决策（快速流程）

1. **能否在没有 I/O 的情况下测试？**
    → 能：进行**单元测试**。

2. **是否依赖框架装配/序列化或数据库查询？**
    → 是：进行**集成/组件**测试（Spring 切片，Testcontainers）。

3. **是否是跨服务/公共 API 契约？**
    → 是：进行**契约测试**（模式/Pact）加上几个 **API E2E** 流程。

4. **其价值是否仅在 UI 中可见或是关键 UX？**
    → 是：进行 **UI E2E** 测试，但仅限于核心旅程。

---

# 合理的比例与预算

* 大致目标为 **70–80% 单元测试**，**15–25% 集成/API 测试**，**5–10% UI E2E 测试**。
* 保持每次提交的 CI 快速：单元测试 <2–3 分钟，集成测试并行化；在 PR 上运行**少量 UI 冒烟测试**，**更广泛的 UI 测试包**在夜间运行。

---

# 优先事项（基于风险的检查清单）

* 资金流动、认证、权限、合规性 → **API 和一个 UI 快乐路径**。
* 复杂计算、定价规则 → **单元测试**（多种情况）+ 几个使用真实数据库处理舍入/时区的**集成测试**。
* 持久化逻辑、迁移、复杂连接 → **使用 Testcontainers 的仓储测试**。
* 跨团队契约 → CI 中的**契约测试**以阻止破坏性变更。
* 可访问性、国际化 → **组件测试**用于 ARIA/区域设置 + 关键页面的**定期 UI 扫描**（axe）。

---

# CI 流水线形态（实用主义）

* **每次推送时：** 单元测试 + 切片测试；少量 API E2E 测试；极少量 UI 冒烟测试（1–3 个）。
* **夜间：** 完整的 API E2E 测试，更广泛的 UI 测试包，性能冒烟测试（k6），基本安全扫描（ZAP）。
* **快速隔离不稳定的测试**；修复或删除——不要忽略。

---

# 测试数据与不稳定性提示

* 使用**工厂方法/构建器**；避免共享的可变固件。
* 在启动时使用 SQL/数据**种子化 Testcontainers**；保持测试**幂等**。
* 在 UI 中，优先使用**角色/标签选择器**而非 CSS/XPath；避免休眠，使用与用户可见条件绑定的等待。
* **记录跟踪信息**（Playwright trace, Selenium logs）以便调试 CI 失败。

---

# 简明经验法则

* 如果一个错误本可以被**更快**的层级捕获，**就将测试下移**。
* 仅保留**少量、关键**的 UI 旅程测试。
* 使用 **Testcontainers** 使集成测试有意义。
* 除非 Selenium 是硬性要求，否则优先选择 **Playwright**。

如果你愿意，告诉我你的**前 3–5 个业务关键流程**，我可以为你勾勒出每个层级的具体测试清单（包括工具选择和 CI 门控）。
