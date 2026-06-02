---
audio: false
generated: true
lang: en
layout: post
title: Pili Streaming Cloud Library for PHP
translated: false
type: note
---

### Key Points
- It seems likely that to use "pili-engineering/pili-sdk-php": "dev-master", you need to install it via Composer and set up Qiniu credentials.
- Research suggests the package requires PHP 5.3.0 or higher and is for Pili Streaming Cloud, related to Qiniu.
- The evidence leans toward creating a Hub object and using stream operations like generating RTMP URLs, but exact methods may vary.

### Installation
First, ensure you have Composer installed. Add the package to your `composer.json` file with:
```json
"require": {
    "pili-engineering/pili-sdk-php": "dev-master"
}
```
Then, run `composer install` or `composer update`. In your PHP script, include:
```php
require 'vendor/autoload.php';
```

### Setup and Usage
You’ll need a Qiniu account and a Pili Hub. Set your access key, secret key, and hub name, then create a Hub object:
```php
use Qiniu\Credentials;
use Pili\Hub;

$credentials = new Credentials('your_access_key', 'your_secret_key');
$hub = new Hub($credentials, 'your_hub_name');
```
Create or get a stream, e.g., `$stream = $hub->createStream('your_stream_key');`, and use methods like `$stream->rtmpPublishUrl(60)` for operations.

### Unexpected Detail
Note that "dev-master" is a development version, potentially unstable, with tagged versions like 1.5.5 available for production.

---

### Comprehensive Guide on Using "pili-engineering/pili-sdk-php": "dev-master"

This guide provides a detailed exploration of how to use the "pili-engineering/pili-sdk-php" package with the "dev-master" version, based on available documentation and examples. It covers installation, setup, usage, and additional considerations, ensuring a thorough understanding for developers working with Pili Streaming Cloud services.

#### Background and Context
The "pili-engineering/pili-sdk-php" package is a server-side library for PHP, designed to interact with Pili Streaming Cloud, a service associated with Qiniu, a cloud storage and CDN provider. The "dev-master" version refers to the latest development branch, which may include recent features but could be less stable than tagged releases. The package requires PHP 5.3.0 or higher, making it accessible for many PHP environments as of March 3, 2025.

#### Installation Process
To begin, you must have Composer installed, a dependency manager for PHP. The installation involves adding the package to your project's `composer.json` file and running a Composer command to download it. Specifically:

- Add the following to your `composer.json` under the "require" section:
  ```json
  "require": {
      "pili-engineering/pili-sdk-php": "dev-master"
  }
  ```
- Execute `composer install` or `composer update` in your terminal to fetch the package and its dependencies. This will create a `vendor` directory with the necessary files.
- In your PHP script, include the autoloader to access the package classes:
  ```php
  require 'vendor/autoload.php';
  ```

This process ensures the package is integrated into your project, leveraging Composer's autoloading for easy class access.

#### Prerequisites and Setup
Before using the SDK, you need a Qiniu account and must set up a Pili Hub, as the SDK interacts with Pili Streaming Cloud services. This involves obtaining an Access Key and Secret Key from Qiniu and creating a hub within their platform. The documentation suggests these credentials are essential for authentication.

To set up, define your credentials in your PHP script:
- Access Key: Your Qiniu Access Key.
- Secret Key: Your Qiniu Secret Key.
- Hub Name: The name of your Pili Hub, which must exist prior to use.

An example setup looks like:
```php
$accessKey = 'your_access_key';
$secretKey = 'your_secret_key';
$hubName = 'your_hub_name';
```

#### Creating and Using the Hub Object
The core of the SDK is the Hub object, which facilitates stream management. First, create a Credentials object using your Qiniu keys:
```php
use Qiniu\Credentials;

$credentials = new Credentials($accessKey, $secretKey);
```
Then, instantiate a Hub object with these credentials and your hub name:
```php
use Pili\Hub;

$hub = new Hub($credentials, $hubName);
```
This Hub object allows you to perform various stream-related operations, such as creating, retrieving, or listing streams.

#### Working with Streams
Streams are central to Pili Streaming Cloud, and the SDK provides methods to manage them through the Hub object. To create a new stream:
```php
$streamKey = 'your_stream_key'; // Must be unique within the hub
$stream = $hub->createStream($streamKey);
```
To retrieve an existing stream:
```php
$stream = $hub->getStream($streamKey);
```
The stream object then offers various methods for operations, detailed in the following table based on available documentation:

| **Operation**          | **Method**                     | **Description**                                      |
|-------------------------|--------------------------------|------------------------------------------------------|
| Create Stream          | `$hub->createStream($key)`     | Creates a new stream with the given key.             |
| Get Stream             | `$hub->getStream($key)`        | Retrieves an existing stream by key.                 |
| List Streams           | `$hub->listStreams($marker, $limit, $prefix)` | Lists streams with pagination options.               |
| RTMP Publish URL       | `$stream->rtmpPublishUrl($expire)` | Generates an RTMP publish URL with expiration time.  |
| RTMP Play URL          | `$stream->rtmpPlayUrl()`       | Generates an RTMP play URL for the stream.           |
| HLS Play URL           | `$stream->hlsPlayUrl()`        | Generates an HLS play URL for streaming.             |
| Disable Stream         | `$stream->disable()`           | Disables the stream.                                 |
| Enable Stream          | `$stream->enable()`            | Enables the stream.                                  |
| Get Stream Status      | `$stream->status()`            | Retrieves the current status of the stream.          |

For example, to generate an RTMP publish URL with a 60-second expiration:
```php
$expire = 60;
$url = $stream->rtmpPublishUrl($expire);
echo $url;
```
This URL can be used for publishing streams to Pili Streaming Cloud, with the expiration ensuring temporary access.

#### Additional Considerations
- **Version Stability**: The "dev-master" version is the development branch, potentially unstable. For production, consider using a tagged version, such as 1.5.5, available on Packagist [pili-engineering/pili-sdk-php versions](https://packagist.org/p/pili-engineering/pili-sdk-php). The history shows updates like API additions and method refinements, with versions dating back to 2016.
- **Error Handling**: The documentation suggests using try-catch blocks for operations, as seen in examples for stream creation and retrieval, to handle potential exceptions.
- **Documentation and Examples**: While specific examples were not extensively detailed, the GitHub repository [Pili Streaming Cloud server-side library for PHP](https://github.com/pili-engineering/pili-sdk-php) provides installation instructions and feature lists, and comparisons with other language SDKs (e.g., Python) indicate similar functionality, such as URL generation.

#### Comparative Insights
Comparing with other Pili SDKs, such as the Python version, reveals similar patterns: both require credentials, hub setup, and stream operations. The PHP version, however, uses an object-oriented approach with Hub and Stream classes, contrasting with Python's more functional style. This aligns with PHP's typical development practices, offering type safety and IDE support.

#### Conclusion
Using "pili-engineering/pili-sdk-php": "dev-master" involves installing via Composer, setting up Qiniu credentials, creating a Hub object, and managing streams with methods like `rtmpPublishUrl`. Ensure your environment meets PHP 5.3.0+ requirements and consider stability for production use. This guide provides a comprehensive starting point, with further details available in the official documentation and repository.

### Key Citations
- [Pili Streaming Cloud server-side library for PHP GitHub](https://github.com/pili-engineering/pili-sdk-php)
- [pili-engineering/pili-sdk-php versions Packagist](https://packagist.org/p/pili-engineering/pili-sdk-php)
