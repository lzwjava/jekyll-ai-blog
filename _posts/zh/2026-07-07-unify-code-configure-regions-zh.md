---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 统一代码，配置区域
translated: true
type: note
---

问题：对于一个多区域应用，为三个区域分别创建三个独立分支是否是一个错误？我们是否应该使用变量/配置或条件 bean 加载来最大化代码共享？

回答：

是的，在大多数情况下，**为三个区域维护三个长期分支是一个糟糕的架构选择**。通常更好的设计是：

```
一个代码库
        |
        +-- 配置
        |
        +-- 特性开关
        |
        +-- 环境变量
        |
        +-- 条件模块/bean
        |
        +-- 区域专属适配器
```

核心原则是：

> **业务逻辑应当共享；差异应当注入。**

常见的错误做法：

```
main
 |
 +-- china-region
 |     +-- 修改支付
 |     +-- 修改用户流程
 |     +-- 修改 API
 |
 +-- us-region
 |     +-- 修改支付
 |     +-- 修改用户流程
 |
 +-- eu-region
       +-- 修改支付
       +-- 修改用户流程
```

一年后：

```
china-region   ---- 200 次提交差异
us-region      ---- 150 次提交差异
eu-region      ---- 180 次提交差异
```

此时每个 bug 修复都需要：

```
修复 bug
  |
  +--> cherry-pick 到 china
  +--> cherry-pick 到 us
  +--> cherry-pick 到 eu
```

最终各个分支会演变成不同的产品。

---

更好的做法：

### 1. 配置驱动行为

示例：

```yaml
region: us

payment:
  provider: stripe

storage:
  provider: s3
```

中国区：

```yaml
region: cn

payment:
  provider: alipay

storage:
  provider: oss
```

相同代码：

```java
interface PaymentService {
    void pay(Order order);
}
```

不同实现：

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

Spring 会加载正确的 bean。

---

### 2. 策略模式处理区域差异

示例：

```java
interface TaxCalculator {
    BigDecimal calculate(Order order);
}
```

实现：

```
TaxCalculator
      |
      +-- ChinaTaxCalculator
      |
      +-- USTaxCalculator
      |
      +-- EUTaxCalculator
```

选择方式：

```java
TaxCalculator calculator =
    factory.get(region);
```

---

### 3. 特性开关

针对临时差异：

```java
if (featureFlags.newCheckoutEnabled(region)) {
    newCheckout();
} else {
    oldCheckout();
}
```

适用于：

* A/B 测试
* 逐步 rollout
* 法规变更

---

### 4. 分开部署，而非分开代码

常见的企业架构：

```
Git 仓库

app/
 ├── common/
 │     ├── user
 │     ├── order
 │     ├── payment 接口
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

部署：

```
中国区生产环境
    |
    +-- 同一份二进制文件
    +-- cn 配置

美国区生产环境
    |
    +-- 同一份二进制文件
    +-- us 配置
```

---

有些例外情况，此时独立分支是合理的：

* 法律上不同的产品
* 完全不同的用户工作流
* 不同的发布计划
* 不同团队拥有产品
* 无法合并的依赖

例如：

```
Android 中国版
vs
Android 政府监管版
```

可能值得分离。

但对于：

* 不同的支付提供商
* 不同的云服务商
* 不同的语言
* 不同的合规要求
* 不同的 UI 选项

→ 通常是配置 + 依赖注入更优。

大型系统通常优化目标为：

```
最大化共享代码
+
最小化区域定制
```

因为每一行重复的代码都会成为未来的维护成本。目标不是“不惜一切代价维护一个分支”，目标应该是 **为公共系统维护单一事实来源**。
