---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 选择 CI4 而非 CI3 的迁移
translated: true
type: note
---

问题：基于当前的 CI4 迁移状态以及描述的两种修复方案，应该选择哪个方案——方案 A（完成 CI4 重构）还是方案 B（降级到 PHP 8.3 + 保留 CI3）？

答案：

## 决策框架：方案 A vs 方案 B

这并非纯粹的技术决策——这是一个**业务风险 + 时间跨度**的决策。以下是结构化分析：

---

### 🔴 为何方案 B（停留在 CI3 + PHP 8.3）是一个陷阱

方案 B 感觉安全，因为它快速，但 2026 年的环境已发生重大变化：

**CI3 没有官方的 PHP 8.2+ 支持。** CI3 处于维护模式，仅接收有限的安全修复，并且官方不保证在没有社区应用补丁的情况下支持 PHP 8.2 或更高版本。

**PHP 8.3 + CI3 是一个已知问题。** 在 PHP 8.3 上运行 CI 3.1.13 会在核心文件中产生诸如 "Creation of dynamic property is deprecated" 的错误。您将需要手动为框架打补丁——这是一个持续性的负担，而非一次性修复。

**PHP 版本有 EOL 时间线。** 当前受支持的 PHP 版本包括 8.2（支持至 2026 年 12 月）、8.3（支持至 2027 年 12 月）和 8.4（支持至 2028 年 12 月）。CI3 并未官方支持其中任何一个版本——因此每次 PHP 版本升级都会带来新的风险。

**开发人员的可用性只会进一步缩减。** 在 2026 年找到愿意在 CodeIgniter 3 上工作的开发人员越来越难——现代工程师倾向于使用当前框架，并积极回避遗留技术栈。

---

### 🟢 为何方案 A（完成 CI4 重构）是正确的选择

您已经完成了大部分繁重工作。评估显示：

- 25 个控制器已迁移 ✅
- 32 个模型已迁移 ✅
- 框架启动、路由解析、数据库/Redis 连接正常 ✅
- 基础设施（Docker、Nginx、PHP 8.5 FPM）稳固 ✅

**仅剩的阻碍是 3 个遗留库：** `JSSDK`、`REST_Controller` 和 `WeChat SDK`。这些库使用了 `get_instance()`——即 CI3 的全局单例。CI4 是对框架的重写，不向后兼容——更合适的思路是转换您的应用，而不是升级它。您已经转换了应用 90% 的部分。剩下的 10% 现在集中在这几个库中。

PHP 8.5 要求 CodeIgniter 4.7.0 或更高版本——您的技术栈（PHP 8.5.4 + CI4 v4.7.2）完全匹配并且得到官方支持。

---

### 🛠️ 方案 A 的具体修复计划

**在 JSSDK 中替换 `get_instance()`：**

在 CI4 中，没有全局的 `get_instance()`。正确的模式是依赖注入或使用服务容器：

```php
// CI3（已失效）
$CI =& get_instance();
$CI->load->library('session');

// CI4 替代方案
$session = \Config\Services::session();
// 或者通过构造函数注入
```

**替换 `REST_Controller`：**

CI4 有原生的 API 资源控制器。替换为：
```php
// CI3 模式（已失效）
class Api extends REST_Controller { ... }

// CI4 模式
use CodeIgniter\RESTful\ResourceController;
class Api extends ResourceController { ... }
```

**替换 `$this->load->*` 模式：**

```php
// CI3（已失效）
$this->load->model('UserModel');

// CI4
$userModel = new \App\Models\UserModel();
// 或者
$userModel = model('UserModel');
```

**WeChat/WeChatPlatform SDK：**
这些库很可能仅使用 `get_instance()` 来访问配置或数据库。提取这些依赖项，并通过构造函数注入的方式传递。

---

### 📊 决策矩阵

| 因素 | 方案 A（CI4 重构） | 方案 B（CI3 + PHP 8.3） |
|---|---|---|
| 修复所需时间 | ~2 小时（估算） | 5 分钟 |
| 长期可行性 | ✅ 官方支持 | ❌ 不受支持且日渐衰退 |
| PHP 兼容性 | ✅ 官方支持 PHP 8.5 | ⚠️ 需要手动打补丁 |
| 安全状况 | ✅ 积极开发 | ❌ 仅限维护 |
| 性能 | ✅ JIT + PHP 8.5 优势 | ❌ 无 JIT，旧版运行时 |
| 未来开发招聘 | ✅ 现代技术栈 | ❌ 人才池不断缩小 |
| 已完成的工作 | 如果放弃，将前功尽弃 | - |
| 技术债务 | 消除 | 增加 |

---

### ✅ 最终裁决

**选择方案 A。** 您距离一个完全现代化、官方支持的技术栈只差一次专注的编码会话。方案 B 是一个 5 分钟的修复，可能为您争取 12-18 个月的时间，然后您将再次面临完全相同的决策——届时选择更少，技术债务更多。

阻碍您的三个库（`JSSDK`、`REST_Controller`、`WeChat SDK`）是易于理解的 CI3 模式，并且有直接的 CI4 对应方案。这是最后一公里——不要现在回头。

> **如果今天时间压力非常紧迫：** 使用一个临时适配层——用一个返回服务定位器对象的兼容性函数来包装 `get_instance()`，解除应用阻塞，部署，然后进行正确的重构。这能让您在 30 分钟内启动并运行，而无需放弃 CI4。

参考资料：

- [还在运行 CodeIgniter 3？2026 年您的迁移选择](https://pegotec.net/still-running-codeigniter-3-your-options-in-2026/)
- [CodeIgniter 4 服务器要求](https://codeigniter.com/user_guide/intro/requirements.html)
- [从 CI3 升级到 CI4 — 官方文档](https://codeigniter4.github.io/userguide/installation/upgrade_4xx.html)
- [升级 CodeIgniter — Zend 指南](https://www.zend.com/blog/upgrading-codeigniter)
- [pocketarc/codeigniter — 针对 PHP 8.5 的 CI3 分支](https://github.com/pocketarc/codeigniter)
- [CI3 PHP 8.3 问题追踪](https://github.com/bcit-ci/CodeIgniter/issues/6278)