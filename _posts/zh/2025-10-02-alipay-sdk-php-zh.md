---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 支付宝SDK PHP集成指南
translated: true
type: note
---

### 前置准备
要在 PHP 中集成支付宝 SDK，您需要：
- 有效的支付宝商户账户（在 https://open.alipay.com 注册）
- RSA 密钥对：为服务器生成私钥，并将公钥上传至支付宝用于交易签名
- PHP 5.6+（建议使用 7.x 版本以获得更好安全性），并启用 cURL 和 OpenSSL 等扩展
- 从支付宝官方 GitHub（如 https://github.com/alipay/alipay-sdk-php）下载 SDK——请注意提供的代码片段适用于旧版本（约 2016 年）；最新 SDK 使用新的 API（如支付宝交易 API）。若使用旧版移动安全支付，可能仍可运行但已过时

### SDK 配置步骤
1. **下载与引入**：从支付宝开发者平台或 GitHub 下载 SDK 压缩包，解压至项目目录（如 `vendor/alipay-sdk`）
2. **文件引入**：在 PHP 脚本中引入主 SDK 文件，例如：
   ```php
   require_once 'path/to/alipay-sdk/AopClient.php'; // 适用于新版 SDK
   ```
   若使用代码片段中的旧版本，可能需要自定义引入如 `AopSdk.php`

3. **密钥与账户配置**：
   - 使用 OpenSSL 命令或在线工具生成 RSA 密钥（2048 位）。示例：
     ```bash
     openssl genrsa -out private_key.pem 2048
     openssl rsa -in private_key.pem -pubout -out public_key.pem
     ```
   - 按代码片段所示填写 `$config` 数组：
     - `partner`：支付宝合作身份 ID（16 位数字，以 2088 开头）
     - `private_key`：PEM 编码的私钥（原始格式，不含 -----BEGIN PRIVATE KEY----- 等头信息）
     - `alipay_public_key`：支付宝公钥（从支付宝控制台复制）
     - 其他字段：`transport` 使用 HTTPS，并将 `cacert.pem`（从支付宝文档下载）置于脚本目录用于 SSL 验证

### SDK 初始化
创建 AopClient 实例并传入配置：
```php
use Orvibo\AopSdk\AopClient; // 根据 SDK 版本调整命名空间

$aopClient = new AopClient();
$aopClient->gatewayUrl = 'https://openapi.alipay.com/gateway.do'; // 生产环境地址
$aopClient->appId = 'your_app_id'; // 新版 SDK 使用 appId 替代 partner
$aopClient->rsaPrivateKey = $config['private_key'];
$aopClient->alipayrsaPublicKey = $config['alipay_public_key'];
$aopClient->apiVersion = '1.0';
$aopClient->signType = 'RSA2'; // 新版 SDK 推荐使用 RSA2
$aopClient->postCharset = $config['input_charset'];
$aopClient->format = 'json';
```

若使用代码片段中的旧版移动支付，需使用较旧类如 `AlipaySign`

### 发起支付请求
1. **构建请求参数**：
   ```php
   $request = new AlipayTradeAppPayRequest(); // 根据 SDK 版本调整
   $request->setBizContent("{" .
       "\"body\":\"测试交易\"," .
       "\"subject\":\"测试商品\"," .
       "\"out_trade_no\":\"123456789\"," .
       "\"timeout_express\":\"30m\"," .
       "\"total_amount\":\"0.01\"," .
       "\"product_code\":\"QUICK_MSECURITY_PAY\"" .
       "}");
   $request->setNotifyUrl($config['service']); // 您的通知回调地址
   ```

2. **执行请求**：
   ```php
   $response = $aopClient->sdkExecute($request);
   echo $response; // 此签名字符串将用于应用的支付宝 SDK
   ```

3. **移动端集成**：将响应传递至移动端原生支付宝 SDK（如 Android/iOS）以完成支付

### 通知与响应处理
- **异步通知**：在 `notify_url` 设置回调 PHP 脚本以验证支付宝通知
  ```php
  $aopClient->rsaCheckV1($_POST, $alipayPublicKey, 'RSA2'); // 验证签名
  // 处理支付状态（如更新数据库）
  ```
- **同步返回**：支付完成后，支付宝将跳转至设置的 `return_url`

### 测试与部署
- 使用支付宝沙箱环境进行测试：https://openhome.alipay.com/platform/devEnv.htm
- 常见问题：确保密钥格式正确（无多余空行）。推荐使用 RSA2 增强安全性
- 安全建议：安全存储密钥（勿放入版本控制）。始终验证签名防篡改

若使用旧版 SDK，建议升级至支付宝最新 PHP SDK（如通过 Composer：`composer require alipay/openapisdk`）以获得更佳功能与安全性。详细文档请访问 https://docs.open.alipay.com/。若遇错误，请提供代码与日志以便排查
