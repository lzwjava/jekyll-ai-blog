---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 功能标志实现示例
translated: true
type: note
---

问题：如何在代码中实际使用 feature flag，能否用几种流行语言展示具体的例子？

回答：

Feature flag 让你可以将代码合并到 `main` 并部署到生产环境，同时让功能完全隐藏（或部分可见），直到你准备好为止。你可以通过外部方式（仪表盘、CLI 或配置文件）控制开关——无需新的部署即可开启/关闭。

### 编写带有 feature flag 的代码的核心原则

1. 默认情况下始终安全（flag 关闭 = 旧的、经过验证的行为）。
2. 在启动时或请求时，保持 flag 检查快速且同步。
3. 在 30-90 天内清理 flag 和废弃代码。
4. 明确命名 flag：`new-checkout-flow-2025q1`、`ai-search-backend-v2` 等。

### 实际案例

#### 1. JavaScript / TypeScript (React + LaunchDarkly 示例)

```tsx
import { useFlags, useLDClient } from 'launchdarkly-react-client-sdk';

function CheckoutButton() {
  const { newCheckoutFlow2025q1 } = useFlags();

  if (newCheckoutFlow2025q1) {
    return <NewFancyCheckout />;
  }

  return <OldCheckout />;
}
```

按百分比灰度发布示例：

```ts
const variant = ldClient.variation('new-checkout-flow-2025q1', { key: user.id }, 'control');
if (variant === 'new') { /* ... */ }
```

#### 2. Python (Flask/Django + Unleash 或简单的 Redis)

```python
from flask import Flask
import requests

app = Flask(__name__)

def is_feature_enabled(feature_name, user_id=None):
    # Simple Unleash example
    response = requests.get(f"https://unleash/api/features/{feature_name}")
    data = response.json()
    return data['enabled']

@app.route("/dashboard")
def dashboard():
    if is_feature_enabled("new-dashboard-v2", user_id=current_user.id):
        return render_template("new_dashboard.html")
    return render_template("old_dashboard.html")
```

使用本地配置服务更简单：

```python
if settings.FEATURE_FLAGS.get('ai-search-enabled', False):
    results = call_openai_search(query)
else:
    results = call_legacy_search(query)
```

#### 3. Go (使用 Unleash Go 客户端)

```go
if client.IsEnabled("payment-retry-logic-v3", unleash.WithContext(ctx)) {
    doNewRetryLogic()
} else {
    doOldRetryLogic()
}

// Percentage rollout to 10% of users
if client.IsEnabled("new-onboarding", unleash.WithFallback(false), unleash.WithContext(userContext)) {
    showNewOnboarding()
}
```

#### 4. Ruby on Rails (使用 Flipflop 或 Rollout)

```ruby
# config/features.yml or dashboard toggle
if Flipflop.new_checkout_flow?
  render "checkouts/new_flow"
else
  render "checkouts/legacy"
end

# Gradual rollout to 5% of users + all staff
Flipflop.new_checkout_flow? do |user|
  actor.staff? || Random.rand(100) < 5
end
```

#### 5. 带有 feature flag 的数据库迁移模式

这通常需要用于 schema 更改：

```python
# Step 1: Add column with flag off (no code uses it yet)
add_column :users, :preferred_language, :string

# Step 2: Deploy code that writes to both old and new places when flag is on
if feature_enabled?(:new-language-storage)
  user.update(preferred_language: lang)           # new column
end
user.update(language: lang)                         # old column (still used)

# Step 3: Back-fill data when 100% rolled out
# Step 4: Flip flag permanently on, remove old code/column
```

### 常见灰度发布策略（在 feature flag 仪表盘中完成，无需更改代码）

| 策略                    | 用例                                       |
|--------------------------|---------------------------------------------|
| 布尔开关                | 内部工具、管理功能                          |
| 按用户百分比            | 金丝雀发布 (0.1% → 100%)                    |
| 特定用户/邮箱           | Beta 测试人员、内部测试                      |
| 环境 (prod/staging)    | 如果需要，可以在 staging 环境中关闭          |
| 国家/租户               | 首先只在欧盟发布                            |

### 大公司的真实案例

- Netflix：每一个 UI 更改都位于 feature flag 之后；他们同时运行数百个 A/B 测试。
- Facebook：臭名昭著的“暗发布”——他们将整个 Timeline 功能提前数月部署到生产环境，隐藏在 flag 之后。
- Shopify：几乎完全依靠 feature flag 和 trunk-based development，将部署频率从每周 1 次提高到每天 50+ 次。
- GitHub：使用 Scientist gem + feature flag 进行有风险的重构（并行运行新旧代码，比较结果）。

一旦你习惯了，你就会开始将 feature flag 视为发布任何非平凡内容的主要方式——部署真正变得枯燥。

参考资料：

- [LaunchDarkly Docs – Code examples in 12 languages](https://docs.launchdarkly.com)
- [Martin Fowler – Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html)
- [Unleash open-source feature flag server](https://www.getunleash.io)
- [Feature Flagging Guide by Split.io](https://www.split.io/product/feature-flags)
