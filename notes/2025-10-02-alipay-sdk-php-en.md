---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Alipay SDK PHP Integration Guide
translated: false
type: note
---

### Prerequisites

To integrate Alipay SDK in PHP, you'll need:

- A valid Alipay merchant account (sign up at <https://open.alipay.com>).
- RSA key pairs: Generate a private key for your server and upload the public key to Alipay for signing transactions.
- PHP 5.6+ (preferably 7.x for better security), with extensions like cURL and OpenSSL enabled.
- Download the Alipay SDK from their official GitHub (e.g., <https://github.com/alipay/alipay-sdk-php>) – note the provided code snippet appears to be for an older version (~2016); the latest SDK uses newer APIs like Alipay Trade APIs. If you're using the legacy mobile security pay, it may still work but is deprecated.

### Setting Up the SDK

1. **Download and Include**: Download the SDK ZIP from Alipay's developer portal or GitHub. Extract it to your project directory (e.g., `vendor/alipay-sdk`).
2. **Include Files**: In your PHP script, include the main SDK file, e.g.:

   ```php
   require_once 'path/to/alipay-sdk/AopClient.php'; // For modern SDK
   ```

   For the legacy version in your snippet, you might need custom includes like `AopSdk.php`.

3. **Configure Keys and Account**:
   - Generate RSA keys (2048-bit) using OpenSSL commands or online tools. Example:

     ```bash
     openssl genrsa -out private_key.pem 2048
     openssl rsa -in private_key.pem -pubout -out public_key.pem
     ```

   - Fill in the `$config` array as shown in your snippet:
     - `partner`: Your Alipay partner ID (16 digits starting with 2088).
     - `private_key`: Your PEM-encoded private key (raw, without headers like -----BEGIN PRIVATE KEY-----).
     - `alipay_public_key`: Alipay's public key (copy from your Alipay console).
     - Other fields: Use HTTPS for `transport`, and place `cacert.pem` (download from Alipay docs) in the script directory for SSL verification.

### Initializing the SDK

Create an AopClient instance and pass the config:

```php
use Orvibo\AopSdk\AopClient; // Adjust namespace for your SDK version

$aopClient = new AopClient();
$aopClient->gatewayUrl = 'https://openapi.alipay.com/gateway.do'; // Production URL
$aopClient->appId = 'your_app_id'; // Newer SDK uses appId instead of partner
$aopClient->rsaPrivateKey = $config['private_key'];
$aopClient->alipayrsaPublicKey = $config['alipay_public_key'];
$aopClient->apiVersion = '1.0';
$aopClient->signType = 'RSA2'; // Modern SDK prefers RSA2
$aopClient->postCharset = $config['input_charset'];
$aopClient->format = 'json';
```

For legacy mobile pay as in your snippet, you'd use older classes like `AlipaySign`.

### Making a Payment Request

1. **Build Request Parameters**:

   ```php
   $request = new AlipayTradeAppPayRequest(); // Or similar for your SDK version
   $request->setBizContent("{" .
       "\"body\":\"Test transaction\"," .
       "\"subject\":\"Test Subject\"," .
       "\"out_trade_no\":\"123456789\"," .
       "\"timeout_express\":\"30m\"," .
       "\"total_amount\":\"0.01\"," .
       "\"product_code\":\"QUICK_MSECURITY_PAY\"" .
       "}");
   $request->setNotifyUrl($config['service']); // Your notification URL
   ```

2. **Execute the Request**:

   ```php
   $response = $aopClient->sdkExecute($request);
   echo $response; // This signed string is used in your app's Alipay SDK
   ```

3. **In Your Mobile App (if integrating with app)**: Pass the response to your app's native Alipay SDK (e.g., Android/iOS) to complete the payment.

### Handling Notifications and Responses

- **Asynchronous Notifications**: Set up a callback PHP script at the `notify_url` to verify Alipay's notifications.

  ```php
  $aopClient->rsaCheckV1($_POST, $alipayPublicKey, 'RSA2'); // Verify signature
  // Process payment status (e.g., update database)
  ```

- **Synchronous Return**: After payment, Alipay redirects to your `return_url` (if set).

### Testing and Deployment

- Use Alipay's sandbox environment for testing: <https://openhome.alipay.com/platform/devEnv.htm>.
- Common issues: Ensure keys are correctly formatted (no extra lines). Use RSA2 for better security.
- Security Tips: Store keys securely (not in version control). Always verify signatures to prevent tampering.

If this is for the old SDK, consider upgrading to Alipay's latest PHP SDK (e.g., via Composer: `composer require alipay/openapisdk`) for better features and security. For detailed docs, visit <https://docs.open.alipay.com/>. If you encounter errors, share your code and logs for troubleshooting.
