---
audio: false
generated: true
image: false
lang: en
layout: post
title: Complete CodeIgniter 3 to 4 Migration
translated: false
type: note
---

Question: How do I continue the CodeIgniter 3 to CodeIgniter 4 migration, specifically rewriting JSSDK.php and fixing the remaining blockers?

Answer:

Here's a comprehensive step-by-step guide to tackle the remaining migration work:

---

## CI3 → CI4 Migration: Completing the Refactor

### Step 1: Rewrite `JSSDK.php` for CI4

The core pattern change: replace `get_instance()` and CI3 loaders with constructor injection.

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
        // Pull from .env instead of CI3 constants
        $this->appId     = env('WECHAT_APP_ID');
        $this->appSecret = env('WECHAT_APP_SECRET');
        $this->debug     = (bool) env('WECHAT_DEBUG', false);

        // CI4 cache service instead of $this->load->driver('cache')
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

### Step 2: Port Constants to `.env`

**Old CI3 `constants.php`:**
```php
define('WECHAT_APP_ID',     'wx123456');
define('WECHAT_APP_SECRET', 'abc123');
define('WECHAT_DEBUG',      true);
```

**New CI4 `.env`:**
```ini
WECHAT_APP_ID     = wx123456
WECHAT_APP_SECRET = abc123
WECHAT_DEBUG      = true
```

Access anywhere via `env('WECHAT_APP_ID')`.

---

### Step 3: Create a `WeChatPlatform` Shim (if needed)

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

    // Proxy other methods as needed...
}
```

---

### Step 4: Fix Controllers (CI3 → CI4 Pattern)

**CI3 (old):**
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

**CI4 (new):**
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

### Step 5: Enable Cache in CI4

In `app/Config/Cache.php`, set your preferred driver:

```php
public string $handler = 'file'; // or 'redis', 'memcached'
```

For Redis:
```ini
# .env
cache.handler = redis
cache.redis.host = 127.0.0.1
cache.redis.port = 6379
```

---

### Step 6: Verify Routes

In `app/Config/Routes.php`:
```php
$routes->get('wechat',        'WeChatController::index');
$routes->post('wechat/oauth', 'WeChatController::oauth');
```

---

### Migration Checklist

| Task | Status |
|---|---|
| `WeChatClient.php` rewritten | ✅ Done |
| `JSSDK.php` rewritten | 🔧 Use code above |
| `WeChatPlatform` shim | 🔧 Use code above |
| Constants → `.env` | 🔧 Add entries |
| Controllers fixed | 🔧 Per-controller fix |
| Cache configured | 🔧 Check `Config/Cache.php` |
| Routes verified | 🔧 Check `Config/Routes.php` |

---

### Key CI3 → CI4 Mapping Summary

| CI3 | CI4 |
|---|---|
| `get_instance()` | Constructor injection |
| `$this->load->library('X')` | `new X()` or `Services::X()` |
| `$this->load->model('X')` | `new X()` (extends Model) |
| `$this->load->view()` | `return view()` |
| `$this->load->driver('cache')` | `Services::cache()` |
| `define('CONST', val)` | `env('CONST')` in `.env` |
| `$this->input->get()` | `$this->request->getGet()` |

Work through each file top-to-bottom using the pattern table above and the app will come back to life.
