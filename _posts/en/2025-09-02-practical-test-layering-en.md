---
audio: false
generated: true
image: false
lang: en
layout: post
title: Practical Test Layering Guide
translated: false
type: note
---

Great question. A sane test strategy is mainly about **risk and feedback speed**. Here’s a practical way to decide **what to test at which layer**—no tables, just clear rules and examples.

---

# Core principles

* **Test behavior, not implementation.** Favor public APIs over private details.
* **Push most checks down to the fastest layer** that can catch the bug.
* **Use real dependencies only when the risk warrants it** (DB, queues, browser).
* **Cover critical paths end-to-end, but sparingly.** UI tests are the most fragile and slow; save them for what truly matters.

---

# What goes where (quick heuristics)

## 1) Unit tests (fast, isolated)

**Use when:** Pure/domain logic can be tested without I/O (DB, HTTP, filesystem).

* Business rules, pricing/fee calcs, validators, mappers, utilities.
* Service methods with repos/clients **mocked**.
* Goal: lots of small tests; fail in milliseconds.

**Java/Spring example**

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

## 2) Integration / component tests (real wiring, minimal mocks)

**Use when:** You need to verify Spring wiring, serialization, filters, DB queries, transactions.

* **HTTP layer without network**: `@WebMvcTest` (controllers + json), or `@SpringBootTest(webEnvironment=RANDOM_PORT)` for full stack.
* **DB correctness**: Use **Testcontainers** to run a real DB; check SQL, indexes, migrations.
* **Messaging**: Test consumers/producers with a real broker container (Kafka/RabbitMQ).

**HTTP slice example**

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

**DB with Testcontainers**

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

## 3) API contract & end-to-end API tests

**Use when:** You must guarantee **backward-compatible contracts** or full system workflows.

* **Contract tests** (e.g., OpenAPI schema validation or Pact) catch breaking changes without UI.
* **End-to-end API flows**: Spin the app with real DB and hit it via HTTP (RestAssured). Focus on happy paths + a few critical edge cases.

**API E2E example**

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

## 4) UI end-to-end tests (browser)

**Use when:** Only a **few** critical user journeys must be proven in a real browser:

* Auth + checkout; money moves; PII flows; file upload.
* Keep to **3–10 key scenarios**. Everything else: cover at unit/integration/API layers.

**Selenium vs. Playwright/Cypress?**

* **Prefer Playwright** (or Cypress) for modern Angular apps: auto-waiting, easier selectors, parallelism, built-in trace viewer, stable headless runs across Chromium/Firefox/WebKit.
* **Use Selenium** if you must drive **real vendor browsers in a custom grid**, interact with **legacy/enterprise** setups, or you already have mature Selenium infra. It’s more plumbing; you’ll need explicit waits and a grid for speed.

**Playwright (TypeScript) example**

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

**If you must use Selenium (Java)**

```java
WebDriver d = new ChromeDriver();
d.get("http://localhost:4200");
new WebDriverWait(d, Duration.ofSeconds(10))
  .until(ExpectedConditions.elementToBeClickable(By.id("loginBtn"))).click();
```

---

# Deciding layer-by-layer (quick flow)

1. **Can it be tested without I/O?**
   → Yes: **Unit test** it.

2. **Does it depend on framework wiring/serialization or DB queries?**
   → Yes: **Integration/component** test (Spring slices, Testcontainers).

3. **Is it a cross-service/public API contract?**
   → Yes: **Contract tests** (schema/Pact) + a couple **API E2E** flows.

4. **Is the value only visible in the UI or critical UX?**
   → Yes: **UI E2E**, but only core journeys.

---

# Sensible proportions & budgets

* Aim roughly for **70–80% unit**, **15–25% integration/API**, **5–10% UI E2E**.
* Keep per-commit CI fast: unit in <2–3 min, integration parallelized; run a **small UI smoke** on PRs, a **broader UI pack nightly**.

---

# What to prioritize (risk-based checklist)

* Money movement, auth, permissions, compliance → **API & a UI happy path**.
* Complex calculations, pricing rules → **Unit** (many cases) + a **couple integration** with real DB rounding/timezones.
* Persistence logic, migrations, tricky joins → **Repo tests with Testcontainers**.
* Cross-team contracts → **Contract tests** in CI to block breaking changes.
* Accessibility, i18n → **Component tests** for ARIA/locale + **periodic UI scan** (axe) on key pages.

---

# CI pipeline shape (pragmatic)

* **On every push:** unit + slice tests; a handful of API E2E; tiny UI smoke (1–3).
* **Nightly:** full API E2E, broader UI pack, performance smoke (k6), basic security scan (ZAP).
* **Quarantine flakies** fast; fix or delete—don’t ignore.

---

# Test data & flakiness tips

* Use **factory methods/builders**; avoid shared mutable fixtures.
* **Seed Testcontainers** with SQL/data on startup; keep tests **idempotent**.
* In UI, prefer **role/label selectors** over CSS/XPath; avoid sleeps, use waits tied to user-visible conditions.
* **Record traces** (Playwright trace, Selenium logs) for debugging CI failures.

---

# TL;DR rules of thumb

* If a bug would have been caught by a **faster** layer, **move the test down**.
* Keep only **few, critical** UI journeys.
* Use **Testcontainers** to make integration meaningful.
* Prefer **Playwright** unless Selenium is a hard requirement.

If you want, tell me your **top 3–5 business-critical flows** and I’ll sketch the exact test list per layer (with tool choices and CI gating).
