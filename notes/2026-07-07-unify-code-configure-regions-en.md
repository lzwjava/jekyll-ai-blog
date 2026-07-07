---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unify Code, Configure Regions
translated: false
type: note
---

Question: For a multi-region app, is creating three separate branches for three regions a mistake? Should we use variables/configuration or conditional bean loading instead and maximize code sharing?

Answer:

Yes, in most cases **three long-lived branches for three regions is a bad architecture choice**. The usual better design is:

```
one codebase
        |
        +-- configuration
        |
        +-- feature flags
        |
        +-- environment variables
        |
        +-- conditional modules / beans
        |
        +-- region-specific adapters
```

The core principle is:

> **Business logic should be shared; differences should be injected.**

A common mistake:

```
main
 |
 +-- china-region
 |     +-- change payment
 |     +-- change user flow
 |     +-- change API
 |
 +-- us-region
 |     +-- change payment
 |     +-- change user flow
 |
 +-- eu-region
       +-- change payment
       +-- change user flow
```

After 1 year:

```
china-region   ---- 200 commits different
us-region      ---- 150 commits different
eu-region      ---- 180 commits different
```

Now every bug fix needs:

```
fix bug
  |
  +--> cherry-pick china
  +--> cherry-pick us
  +--> cherry-pick eu
```

Eventually branches become different products.

---

Better:

### 1. Configuration-driven behavior

Example:

```yaml
region: us

payment:
  provider: stripe

storage:
  provider: s3
```

China:

```yaml
region: cn

payment:
  provider: alipay

storage:
  provider: oss
```

Same code:

```java
interface PaymentService {
    void pay(Order order);
}
```

Different implementations:

```java
@Component
@ConditionalOnProperty(
    name="payment.provider",
    havingValue="stripe"
)
class StripePaymentService implements PaymentService {
}
```

```java
@Component
@ConditionalOnProperty(
    name="payment.provider",
    havingValue="alipay"
)
class AlipayPaymentService implements PaymentService {
}
```

Spring loads the correct bean.

---

### 2. Strategy pattern for regional differences

Example:

```java
interface TaxCalculator {
    BigDecimal calculate(Order order);
}
```

Implement:

```
TaxCalculator
      |
      +-- ChinaTaxCalculator
      |
      +-- USTaxCalculator
      |
      +-- EUTaxCalculator
```

Selection:

```java
TaxCalculator calculator =
    factory.get(region);
```

---

### 3. Feature flags

For temporary differences:

```java
if (featureFlags.newCheckoutEnabled(region)) {
    newCheckout();
} else {
    oldCheckout();
}
```

Useful for:

* A/B tests
* gradual rollout
* regulatory changes

---

### 4. Separate deployment, not separate code

A common enterprise setup:

```
Git repository

app/
 ├── common/
 │     ├── user
 │     ├── order
 │     ├── payment interface
 │
 ├── region/
 │     ├── cn
 │     ├── us
 │     └── eu
 │
config/
 ├── cn.yaml
 ├── us.yaml
 └── eu.yaml
```

Deploy:

```
CN production
    |
    +-- same binary
    +-- cn config


US production
    |
    +-- same binary
    +-- us config
```

---

There are exceptions where separate branches make sense:

* legally different products
* completely different customer workflows
* different release schedules
* different teams owning products
* impossible-to-merge dependencies

For example:

```
Android app China version
vs
Android app government-regulated version
```

might justify separation.

But for:

* different payment providers
* different cloud providers
* different languages
* different compliance rules
* different UI options

→ usually configuration + dependency injection is better.

Large systems generally optimize for:

```
maximum shared code
+
minimum regional customization
```

because every duplicated line becomes future maintenance cost. The goal is not "one branch at all costs"; the goal is **one source of truth for the common system**.
