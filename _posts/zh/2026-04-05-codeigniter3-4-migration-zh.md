---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 完全从 CodeIgniter 3 迁移到 4
translated: true
type: note
---

问题：如何继续进行CodeIgniter 3到CodeIgniter 4的迁移，特别是重写JSSDK.php以及修复剩余的阻塞问题？

回答：

以下是完成剩余迁移工作的全面分步指南：

---

## CI3 → CI4 迁移：完成重构

### 第1步：为CI4重写`JSSDK.php`

核心模式变更：将`get_instance()`和CI3的加载器替换为构造函数注入。

```php
<?php
// app/Libraries/JSSDK.php

namespace App\Libraries;

use CodeIgniter\HTTP\CURLRequest;
use Config\Services;

class JSSDK
{
    protected string $appId;
    protected string $appSecret;
    protected bool   $debug;
    protected $cache;

    public function __construct()
    {
        // 从.env文件读取，而不是CI3的常量
        $this->appId     = env('WECHAT_APP_ID');
        $this->appSecret = env('WECHAT_APP_SECRET');
        $this->debug     = (bool) env('WECHAT_DEBUG', false);

        // 使用CI4的缓存服务，替代$this->load->driver('cache')
        $this->cache = Services::cache();
    }

    public function getSignPackage(string $url): array
    {
        $jsapiTicket = $this->getJsApiTicket();
        $timestamp   = time();
        $nonceStr    = $this->createNonceStr();

        $rawString = "jsapi_ticket={$jsapiTicket}"
                   . "&noncestr={$nonceStr}"
                   . "&timestamp={$timestamp}"
                   . "&url={$url}";

        $signature = sha1($rawString);

        return [
            'appId'     => $this->appId,
            'nonceStr'  => $nonceStr,
            'timestamp' => $timestamp,
            'url'       => $url,
            'signature' => $signature,
            'rawString' => $rawString,
            'debug'     => $this->debug,
        ];
    }

    protected function getJsApiTicket(): string
    {
        $cacheKey = 'wechat_jsapi_ticket_' . $this->appId;

        if ($ticket = $this->cache->get($cacheKey)) {
            return $ticket;
        }

        $accessToken = $this->getAccessToken();
        $url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket"
             . "?type=jsapi&access_token={$accessToken}";

        $result = $this->httpGet($url);
        $ticket = $result['ticket'];

        $this->cache->save($cacheKey, $ticket, 7000);

        return $ticket;
    }

    protected function getAccessToken(): string
    {
        $cacheKey = 'wechat_access_token_' . $this->appId;

        if ($token = $this->cache->get($cacheKey)) {
            return $token;
        }

        $url = "https://api.weixin.qq.com/cgi-bin/token"
             . "?grant_type=client_credential"
             . "&appid={$this->appId}"
             . "&secret={$this->appSecret}";

        $result = $this->httpGet($url);
        $token  = $result['access_token'];

        $this->cache->save($cacheKey, $token, 7000);

        return $token;
    }

    protected function httpGet(string $url): array
    {
        $client   = Services::curlrequest();
        $response = $client->get($url);
        return json_decode($response->getBody(), true);
    }

    protected function createNonceStr(int $length = 16): string
    {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        $str   = '';
        for ($i = 0; $i < $length; $i++) {
            $str .= $chars[random_int(0, strlen($chars) - 1)];
        }
        return $str;
    }
}
```

---

### 第2步：将常量迁移到`.env`

**旧的CI3 `constants.php`：**
```php
define('WECHAT_APP_ID',     'wx123456');
define('WECHAT_APP_SECRET', 'abc123');
define('WECHAT_DEBUG',      true);
```

**新的CI4 `.env`：**
```ini
WECHAT_APP_ID     = wx123456
WECHAT_APP_SECRET = abc123
WECHAT_DEBUG      = true
```

可以通过`env('WECHAT_APP_ID')`在任何地方访问。

---

### 第3步：创建一个`WeChatPlatform`适配层（如果需要）

```php
<?php
// app/Libraries/WeChatPlatform.php

namespace App\Libraries;

class WeChatPlatform
{
    protected JSSDK $jssdk;
    protected WeChatClient $client;

    public function __construct()
    {
        $this->jssdk   = new JSSDK();
        $this->client  = new WeChatClient();
    }

    public function getSignPackage(string $url): array
    {
        return $this->jssdk->getSignPackage($url);
    }

    // 根据需求代理其他方法...
}
```

---

### 第4步：修复控制器（CI3 → CI4模式）

**CI3（旧）：**
```php
class WeChatController extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->library('JSSDK');
        $this->load->model('WeChatModel');
    }

    public function index() {
        $package = $this->jssdk->getSignPackage(current_url());
        $this->load->view('wechat/index', ['package' => $package]);
    }
}
```

**CI4（新）：**
```php
<?php
// app/Controllers/WeChatController.php

namespace App\Controllers;

use App\Libraries\JSSDK;
use App\Models\WeChatModel;

class WeChatController extends BaseController
{
    protected JSSDK $jssdk;
    protected WeChatModel $wechatModel;

    public function __construct()
    {
        $this->jssdk        = new JSSDK();
        $this->wechatModel  = new WeChatModel();
    }

    public function index(): string
    {
        $package = $this->jssdk->getSignPackage(current_url());
        return view('wechat/index', ['package' => $package]);
    }
}
```

---

### 第5步：在CI4中启用缓存

在`app/Config/Cache.php`中，设置你偏好的驱动：

```php
public string $handler = 'file'; // 或者 'redis', 'memcached'
```

对于Redis：
```ini
# .env
cache.handler = redis
cache.redis.host = 127.0.0.1
cache.redis.port = 6379
```

---

### 第6步：验证路由

在`app/Config/Routes.php`中：
```php
$routes->get('wechat',        'WeChatController::index');
$routes->post('wechat/oauth', 'WeChatController::oauth');
```

---

### 迁移清单

| 任务 | 状态 |
|---|---|
| `WeChatClient.php` 已重写 | ✅ 已完成 |
| `JSSDK.php` 已重写 | 🔧 使用以上代码 |
| `WeChatPlatform` 适配层 | 🔧 使用以上代码 |
| 常量已迁移到 `.env` | 🔧 添加条目 |
| 控制器已修复 | 🔧 逐个控制器修复 |
| 缓存已配置 | 🔧 检查 `Config/Cache.php` |
| 路由已验证 | 🔧 检查 `Config/Routes.php` |

---

### CI3 → CI4关键映射总结

| CI3 | CI4 |
|---|---|
| `get_instance()` | 构造函数注入 |
| `$this->load->library('X')` | `new X()` 或 `Services::X()` |
| `$this->load->model('X')` | `new X()`（扩展Model） |
| `$this->load->view()` | `return view()` |
| `$this->load->driver('cache')` | `Services::cache()` |
| `define('CONST', val)` | 在`.env`中使用 `env('CONST')` |
| `$this->input->get()` | `$this->request->getGet()` |

使用上表中的模式和代码，按顺序处理每个文件，应用程序将恢复正常运行。
