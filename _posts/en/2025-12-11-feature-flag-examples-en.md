---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Feature Flag Implementation Examples
translated: false
type: note
---

Question: How do you actually use feature flags in code, and can you show concrete examples in a few popular languages?

Answer:

Feature flags let you merge code to `main` and deploy it to production while keeping the feature completely hidden (or partially visible) until you’re ready. You control the toggle externally (dashboard, CLI, or config file) — no new deploy needed to turn it on/off.

### Core principles when writing flagged code
1. Always safe by default (flag OFF = old, proven behavior).
2. Keep flag checks cheap and synchronous at startup or request time.
3. Clean up the flag + dead code within 30–90 days.
4. Name flags clearly: `new-checkout-flow-2025q1`, `ai-search-backend-v2`, etc.

### Real-world examples

#### 1. JavaScript / TypeScript (React + LaunchDarkly example)
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

Percentage rollout example:
```ts
const variant = ldClient.variation('new-checkout-flow-2025q1', { key: user.id }, 'control');
if (variant === 'new') { /* ... */ }
```

#### 2. Python (Flask/Django + Unleash or simple Redis)
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

Even simpler with a local config service:
```python
if settings.FEATURE_FLAGS.get('ai-search-enabled', False):
    results = call_openai_search(query)
else:
    results = call_legacy_search(query)
```

#### 3. Go (with Unleash Go client)
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

#### 4. Ruby on Rails (with Flipflop or Rollout)
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

#### 5. Feature-flagged database migration pattern
You often need this for schema changes:
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

### Common rollout strategies (done in the flag dashboard, no code change)

| Strategy               | Use case                                   |
|-----------------------|---------------------------------------------|
| Boolean on/off        | Internal tools, admin features              |
| % of users            | Canary releases (0.1% → 100%)               |
| Specific users/emails | Beta testers, dogfooding                    |
| Environment (prod/staging) | Keep it off in staging if you want        |
| Country / tenant      | Launch only in EU first                     |

### Real examples from big companies
- Netflix: Every single UI change is behind a flag; they run hundreds of A/B tests simultaneously.
- Facebook: The infamous “dark launch” — they deployed the entire Timeline feature to production months early, hidden behind flags.
- Shopify: Went from 1 deploy/week to 50+/day almost entirely thanks to feature flags + trunk-based dev.
- GitHub: Uses Scientist gem + feature flags for risky refactors (runs new and old code in parallel, compares results).

Once you get comfortable, you’ll start treating feature flags as the primary way you release anything non-trivial — and deployments truly become boring.

References:
- [LaunchDarkly Docs – Code examples in 12 languages](https://docs.launchdarkly.com)
- [Martin Fowler – Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html)
- [Unleash open-source feature flag server](https://www.getunleash.io)
- [Feature Flagging Guide by Split.io](https://www.split.io/product/feature-flags)
