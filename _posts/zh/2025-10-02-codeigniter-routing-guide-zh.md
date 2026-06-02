---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter路由指南
translated: true
type: note
---

### CodeIgniter 路由系统概述

CodeIgniter 的路由系统允许你将 URL（URI）映射到特定的控制器类和方法，从而覆盖默认的 URL 模式 `example.com/controller/method/id/`。这对于创建 SEO 友好的 URL、处理 RESTful API 或简单地自定义请求处理方式非常有用。

提供的代码片段来自 CodeIgniter 的 `routes.php` 配置文件。它定义了一个关联数组 `$route`，其中每个键都是一个 URI 模式，值可以是一个字符串（`controller/method`）或一个按 HTTP 方法（例如 GET、POST）指定不同行为的数组。这种设置支持标准路由和特定方法路由。

我将基于 CodeIgniter 的标准行为和你代码中的示例，详细说明**如何定义路由**、**路由的工作原理**以及**如何使用路由**。完整细节请参考 CodeIgniter 官方用户指南关于路由的部分：https://codeigniter.com/userguide4/general/routing.html。

#### 1. **如何定义路由**
路由在 `application/config/routes.php` 中定义为数组。你向 `$route[]` 添加条目。以下是语法：

- **基本路由**：将任何 HTTP 方法映射到控制器/方法。
  ```
  $route['uri_segment'] = 'controller/method';
  ```
  - 示例：`$route['login'] = 'users/login';` 表示任何对 `/login` 的请求都会路由到 `Users::login()`。

- **方法特定路由**：对于 RESTful API，你可以为每个 HTTP 方法（GET、POST、PUT 等）指定不同的控制器/方法。这使用数组。
  ```
  $route['uri_segment'] = array(
      'METHOD1' => 'controller/method1',
      'METHOD2' => 'controller/method2'
  );
  ```
  - 你代码中的示例：`$route['self'] = array('POST' => 'users/update', 'GET' => 'users/self');` 表示：
    - POST 到 `/self` → `Users::update()`。
    - GET 到 `/self` → `Users::self()`。

- **通配符占位符**：使用类似正则表达式的模式来捕获 URL 的动态部分（作为参数传递给方法）。
  - `(:any)`：匹配任何字符（除了斜杠）——例如，用于 slugs 或字符串。
  - `(:num)` 或 `(\d+)`：仅匹配数字——用于 ID。
  - 自定义正则表达式：用括号包裹，例如 `(foo|bar)` 用于特定匹配。
  - 你代码中的示例：
    - `$route['users/(\d+)']['GET'] = 'users/one/$1';`：GET `/users/123` 路由到 `Users::one(123)`。
    - `$route['lives/(\d+)/notify'] = 'lives/notifyLiveStart/$1';`：任何方法到 `/lives/123/notify` 路由到 `Lives::notifyLiveStart(123)`。

- **保留路由**：
  - `$route['default_controller'] = 'welcome';`：如果未提供 URI（例如根 URL），则加载此控制器（→ `Welcome` 控制器）。
  - `$route['404_override'] = 'errors/page_missing';`：用于未匹配路由的控制器/方法（自定义 404）。
  - `$route['translate_uri_dashes'] = FALSE;`：如果为 TRUE，将 URI 中的破折号转换为控制器/方法名称的下划线（例如 `my-controller` → `my_controller`）。

- **顺序很重要**：路由按出现的顺序匹配。将特定路由（带通配符的）定义在通用路由之前，以避免冲突。
- **HTTP 方法**：如果未指定，路由适用于所有方法。你的代码使用数组进行精确指定，这对于 API 非常有用。

**在你的代码中定义路由的提示**：
- 在 `$route['translate_uri_dashes']` 之前添加新路由。
- 使用像 Postman 这样的工具测试 API 路由，以确保命中正确的控制器/方法。
- 对于复杂的应用，按部分分组路由（如你使用注释 `// users` 所做的那样）。

#### 2. **路由的工作原理**
CodeIgniter 的路由器按以下顺序处理每个传入请求：
1. **解析 URI**：将 URL 分解为段（例如 `/users/123/edit` → 段：`users`、`123`、`edit`）。
2. **匹配路由**：从上到下检查 `$route` 数组。它首先查找精确匹配，然后查找带通配符的模式。
   - 如果找到匹配，则映射到指定的控制器/方法，并将动态部分（例如 `123`）作为方法参数传递。
   - 如果没有匹配，则回退到默认模式（`Controller::method/id/`）。
3. **加载控制器和方法**：CodeIgniter 实例化控制器，调用方法，并传递任何 URI 段或捕获的组。
4. **方法特定处理**：如果路由是数组（如你的代码中所示），它会检查请求中的 HTTP 方法（GET、POST 等）。
5. **回退**：未匹配的请求触发 404，或者如果设置了 `$route['404_override']`，则使用该设置。

**示例流程**：
- 请求：`POST https://example.com/lives`
- 匹配：`$route['lives']['POST'] = 'lives/create';`
- 结果：调用 `Lives::create()`，无参数。
- 如果请求是 `GET https://example.com/lives/456`，它将匹配 `$route['lives/(\d+)']['GET'] = 'lives/one/$1';` → `Lives::one(456)`。

**关键机制**：
- **动态参数**：捕获的组（例如 `$1`）作为参数传递给方法。确保你的控制器方法期望它们。
- **安全性**：路由通过隐藏 URL 来防止直接访问敏感控制器。
- **性能**：简单的数组查找；除非有数百个路由，否则没有显著开销。

#### 3. **如何使用路由**
使用路由意味着如上所述设置它们，然后在你的应用程序（控制器、视图等）中利用它们。

- **在控制器中**：假设路由处理 URL 映射；编写期望路由请求的方法。
  - 示例：对于 `$route['login']['POST'] = 'users/login';`，创建一个 `Users.php` 控制器，其中包含一个 `login()` 方法，该方法处理 POST 数据（例如通过 `$this->input->post()`）。

- **生成 URL**：使用 CodeIgniter 的 `site_url()` 或 `base_url()` 与你的路由键来生成链接/按钮。
  - 示例：在视图中，`<a href="<?= site_url('login'); ?>">登录</a>` 指向路由的 URL，但你的代码定义了它命中哪个控制器。

- **测试路由**：
  - 使用你的 Web 浏览器或 API 工具（例如 Postman）访问像 `/users/register` 这样的 URL。
  - 如果路由失败，检查 `application/logs/log-{date}.php` 中的错误。
  - 添加调试：临时重置 `$route['404_override']` 并在测试控制器中使用 var_dump 查看参数。

- **RESTful 用法（如你的代码中所示）**：你的路由设置为类似 API 的结构。例如：
  - 创建资源：发送 POST 到 `/lives` → 创建直播事件。
  - 读取：GET `/lives/123` → 获取直播事件 #123。
  - 更新：POST `/lives/123` → 更新直播事件 #123。

- **常见陷阱与提示**：
  - **重复**：避免重叠路由（例如 `lives` 和 `lives/(\d+)`）；将特定路由放在前面。
  - **未指定的方法**：如果路由是字符串，它适用于所有 HTTP 方法。使用数组以获得精确性。
  - **开发时**：在控制器中启用 CodeIgniter 的 Profiler（`$this->output->enable_profiler(TRUE);`）来调试路由。
  - **版本控制**：你的 routes.php 在版本控制中——更改会影响实时路由。
  - **扩展**：如果你需要高级功能（例如命名空间支持），考虑 CodeIgniter 4 或第三方库，因为 CI 3（你的代码）较旧。

如果你对文件中的特定路由有疑问（例如为什么使用 `(\d+)` 或如何添加新路由），请提供更多细节！对于 CodeIgniter 设置，请确保在你的 index.php 中定义了 `CI_VERSION`。
