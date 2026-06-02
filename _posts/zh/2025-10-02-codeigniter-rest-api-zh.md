---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter REST API 配置指南
translated: true
type: note
---

以下是一份清晰的分步指南，帮助您理解和使用您分享的 CodeIgniter REST API 配置文件（`application/config/rest.php`）。该文件用于配置 REST_Controller 库（一个用于在 CodeIgniter 中构建 RESTful API 的热门 PHP 库，例如 Phil Sturgeon 的 REST 库，现在某些版本中作为 CodeIgniter 框架的一部分进行维护）的行为。

我将解释：

- 该库的功能和关键前提条件。
- 如何设置和使用它。
- 您配置文件中的关键配置选项（附示例）。
- 一个简单的使用示例。
- 常见陷阱和安全提示。

如果您的疑问涉及特定方面（例如身份验证或限制），请进一步说明以获得更有针对性的建议！

### 1. **前提条件和设置**

- **这是什么？** 这是用于 CodeIgniter（一个 PHP 框架）的 REST_Controller 库。它允许您通过让控制器继承 `REST_Controller` 来构建 RESTful API（例如，响应 GET/POST 请求并返回 JSON/XML 的端点）。您的配置文件控制全局设置，如身份验证、响应格式、速率限制和安全性。

- **要求：**
  - CodeIgniter 3.x（或兼容版本；此配置适用于较旧的 3.x 版本）。
  - 如果您的 CodeIgniter 安装中尚未包含 REST_Controller 库，请安装它（可以从 GitHub 下载：`chriskacerguis/codeigniter-restserver`）。将库文件放置在 `application/libraries/` 目录中，并在 `application/config/autoload.php` 中自动加载：

       ```php
       $autoload['libraries'] = ['rest_controller'];
       ```

  - 数据库设置（可选；用于 API 密钥、日志记录或限制等功能）。运行配置注释中提供的 SQL 架构（例如，用于 `keys`、`logs`、`access`、`limits` 等表）。
  - 在 CodeIgniter 中启用美观的 URL（`application/config/routes.php`），以使用干净的 API 端点，如 `/api/users`。
  - 您的 `rest.php` 配置文件应放置在 `application/config/` 目录中，并在 `application/config/autoload.php` 中自动加载：

       ```php
       $autoload['config'] = ['rest'];
       ```

- **基本安装步骤：**
     1. 下载并解压 CodeIgniter。
     2. 添加 REST_Controller 库文件。
     3. 将您提供的 `rest.php` 复制到 `application/config/` 目录。
     4. 在 `routes.php` 中设置路由（例如，`$route['api/(:any)'] = 'api/$1';` 将 `/api/users` 映射到控制器）。
     5. 创建 API 控制器（参见下面的示例）。
     6. 使用 Postman 或 curl 等工具进行测试。

### 2. **关键配置选项**

我将总结您配置文件中的主要设置，按用途分组。这些设置控制全局行为。您可以根据需要修改它们（例如，启用 HTTPS 或更改默认格式）。

- **协议和输出：**
  - `$config['force_https'] = FALSE;`：强制所有 API 调用使用 HTTPS。在生产环境中设置为 `TRUE` 以增强安全性。
  - `$config['rest_default_format'] = 'json';`：默认响应格式（选项：json、xml、csv 等）。请求可以通过 URL 覆盖（例如，`/api/users.format=xml`）。
  - `$config['rest_supported_formats']`：允许的格式列表。出于安全考虑，可以移除不需要的格式。
  - `$config['rest_ignore_http_accept'] = FALSE;`：忽略客户端的 HTTP Accept 头以加快响应速度（如果在代码中始终使用 `$this->rest_format`，则很有用）。

- **身份验证（安全性）：**
  - `$config['rest_auth'] = FALSE;`：主要身份验证模式。选项：
    - `FALSE`：无需身份验证。
    - `'basic'`：HTTP 基本身份验证（用户名/密码以 base64 编码形式放在请求头中）。
    - `'digest'`：更安全的摘要身份验证。
    - `'session'`：检查 PHP 会话变量。
  - `$config['auth_source'] = 'ldap';`：验证凭据的来源（例如，配置数组、LDAP、自定义库）。
  - `$config['rest_valid_logins'] = ['admin' => '1234'];`：简单的用户名/密码数组（如果使用 LDAP，则忽略此设置）。
  - `$config['auth_override_class_method']`：为特定控制器/方法覆盖身份验证设置（例如，`'users' => 'view' => 'basic'`）。
  - `$config['auth_library_class/function']`：如果使用自定义库，指定用于验证的类/方法。
  - IP 控制：
    - `$config['rest_ip_whitelist_enabled/blacklist_enabled']`：基于 IP 对您的 API 进行过滤。
    - 可用于限制访问（例如，将您应用的 IP 加入白名单）。

- **API 密钥（可选安全层）：**
  - `$config['rest_enable_keys'] = FALSE;`：启用 API 密钥检查（密钥存储在数据库表 `keys` 中）。客户端必须在请求头中发送密钥（例如，`X-API-KEY`）。
  - `$config['rest_key_column/name/length']`：自定义密钥字段和请求头名称。
  - 与 `$config['rest_enable_access']` 结合使用，以将密钥限制为特定的控制器/方法。

- **日志记录和限制：**
  - `$config['rest_enable_logging/limits'] = FALSE;`：启用基于数据库的请求日志记录（URI、参数等）或速率限制（例如，每个密钥每小时 X 次调用）。
  - 表：`logs`、`limits`（运行注释中的 SQL 以创建这些表）。
  - `$config['rest_limits_method']`：应用限制的方式（按 API 密钥、URL 等）。
  - 在控制器中为每个方法自定义（例如，`$this->method['get']['limit'] = 100;`）。

- **其他：**
  - `$config['rest_ajax_only'] = FALSE;`：仅限 AJAX 请求（否则返回 505 错误）。
  - `$config['rest_language'] = 'english';`：错误消息的语言。

修改方法：编辑 `rest.php` 并重启您的应用。仔细测试更改！

### 3. **使用方法：分步使用指南**

设置完成后，通过构建继承 `REST_Controller` 的控制器来创建 API 端点。以下是高级流程：

1. **创建控制器：**
   - 在 `application/controllers/` 目录中，创建 `Api.php`（或例如，为特定资源创建 `Users.php`）：

     ```php
     <?php
     defined('BASEPATH') OR exit('No direct script access allowed');
     require_once(APPPATH . 'libraries/REST_Controller.php');

     class Api extends REST_Controller {
         public function __construct() {
             parent::__construct();
             // 可选：为每个方法设置身份验证、限制
             $this->load->database();
             $this->method['index_get']['limit'] = 100; // 100 次请求/小时
         }

         // GET /api
         public function index_get() {
             $data = ['message' => '欢迎使用 API', 'status' => 'success'];
             $this->response($data, REST_Controller::HTTP_OK);
         }

         // POST /api/users
         public function users_post() {
             $data = $this->input->post(); // 获取 POST 数据
             if (empty($data['name'])) {
                 $this->response(['error' => '需要提供姓名'], REST_Controller::HTTP_BAD_REQUEST);
             }
             // 处理（例如，插入数据库）
             $this->response(['message' => '用户已创建'], REST_Controller::HTTP_CREATED);
         }

         // PUT /api/users/{id}
         public function users_put($id) {
             $data = $this->put(); // 获取 PUT 数据
             // 更新 ID 为 $id 的用户
             $this->response(['message' => '用户已更新'], REST_Controller::HTTP_OK);
         }

         // 等等，用于 DELETE 等方法
     }
     ```

2. **发送请求：**
   - 使用任何 HTTP 客户端：
     - GET：`curl http://yourdomain.com/api` → 返回 JSON {"message": "欢迎使用 API", "status": "success"}
     - POST：`curl -X POST http://yourdomain.com/api/users -d "name=John"` → 创建用户。
   - 如果使用身份验证/密钥，请包含请求头（例如，`Authorization: Basic base64(user:pass)` 或 `X-API-KEY: yourkey`）。

3. **测试和调试：**
   - 检查 CodeIgniter 日志以查找错误。
   - 如果身份验证失败，请确保凭据设置正确。
   - 对于限制/日志记录，查询您的数据库表。

### 4. **常见提示和最佳实践**

- **安全性：** 在生产环境中始终使用 HTTPS（`force_https = TRUE`）。如果向外部客户端公开，请启用密钥。对输入进行清理以防止 SQL 注入。
- **错误处理：** 响应包含 `status` 和 `error` 字段（可在配置中自定义）。使用 CodeIgniter 的性能分析器进行调试。
- **性能：** 如果启用了日志记录/限制，您的数据库将处理查询——监控性能是否变慢。
- **升级：** 此配置适用于较旧的 CodeIgniter 版本。对于 CI 4，请使用其内置的 API 资源（此设置可能需要调整）。
- **故障排除：**
  - “无响应”？检查路由、自动加载和库路径。
  - 身份验证问题？验证 `$auth_source` 和凭据。
  - 格式错误？确保您的格式在 `rest_supported_formats` 中。
- **资源：** 文档位于 codeigniter-restserver.org。有关 CI4 迁移，请参阅官方文档。

如果这未能解答您的具体问题，或者您需要针对特定用例（例如启用 OAuth）的代码，请提供更多详细信息！
