---
audio: false
generated: true
lang: en
layout: post
title: Qiniu PHP SDK
translated: false
type: note
---

To use the `"qiniu/php-sdk": "^7.0"` in PHP, you’ll need to integrate the Qiniu PHP SDK into your project. This SDK allows you to interact with Qiniu Cloud Storage services, such as uploading files, managing buckets, and more. Below is a step-by-step guide to get you started:

---

### 1. Install the Qiniu PHP SDK

The recommended way to install the SDK is via Composer, a dependency manager for PHP. Ensure you have Composer installed on your system.

#### Steps

- Open your terminal and navigate to your project directory.
- Run the following command to add the Qiniu PHP SDK (version 7.x) to your project:

  ```bash
  composer require qiniu/php-sdk "^7.0"
  ```

- Composer will download the SDK and its dependencies into the `vendor/` directory and generate an autoload file.

If you don’t have Composer installed, you can download it from [getcomposer.org](https://getcomposer.org/).

---

### 2. Set Up Your Project

After installation, you need to include the autoloader in your PHP script to use the SDK classes.

#### Example

Create a PHP file (e.g., `index.php`) in your project directory and add the following line at the top:

```php
require_once 'vendor/autoload.php';
```

This ensures that the SDK classes are automatically loaded when needed.

---

### 3. Configure Authentication

To use the Qiniu SDK, you’ll need your Qiniu `AccessKey` and `SecretKey`, which you can obtain from your Qiniu account dashboard.

#### Example

```php
use Qiniu\Auth;

$accessKey = 'YOUR_ACCESS_KEY';
$secretKey = 'YOUR_SECRET_KEY';

$auth = new Auth($accessKey, $secretKey);
```

Replace `'YOUR_ACCESS_KEY'` and `'YOUR_SECRET_KEY'` with your actual credentials.

---

### 4. Basic Usage: Uploading a File

One of the most common tasks with the Qiniu SDK is uploading files to a bucket. Here’s an example of how to upload a local file.

#### Example

```php
use Qiniu\Storage\UploadManager;

$bucket = 'YOUR_BUCKET_NAME'; // Replace with your Qiniu bucket name
$filePath = '/path/to/your/file.txt'; // Path to the file you want to upload
$key = 'file.txt'; // The name of the file in Qiniu storage (can be null to use the original filename)

$token = $auth->uploadToken($bucket); // Generate an upload token
$uploadMgr = new UploadManager();

list($ret, $error) = $uploadMgr->putFile($token, $key, $filePath);

if ($error !== null) {
    echo "Upload failed: " . $error->message();
} else {
    echo "Upload successful! File hash: " . $ret['hash'];
}
```

- `$bucket`: The name of your Qiniu bucket.
- `$filePath`: The local path to the file you want to upload.
- `$key`: The file key (name) under which it will be stored in Qiniu. If set to `null`, Qiniu will generate a key based on the file’s hash.
- `$token`: An upload token generated using your credentials and bucket name.
- The `putFile` method returns an array: `$ret` (success info) and `$error` (error info, if any).

---

### 5. Additional Features

The Qiniu PHP SDK provides many other functionalities, such as:

- **Managing Buckets**: Use `Qiniu\Storage\BucketManager` to list files, delete files, or manage bucket settings.
- **File Operations**: Copy, move, or delete files in your bucket.
- **Image Processing**: Generate URLs for resized or formatted images.

#### Example: Listing Files in a Bucket

```php
use Qiniu\Storage\BucketManager;

$bucketMgr = new BucketManager($auth);
list($ret, $error) = $bucketMgr->listFiles($bucket);

if ($error !== null) {
    echo "Error: " . $error->message();
} else {
    echo "Files in bucket:\n";
    foreach ($ret['items'] as $item) {
        echo $item['key'] . "\n";
    }
}
```

---

### 6. Error Handling

Always check the `$error` variable after SDK operations. If an operation fails, `$error` will contain details about what went wrong.

#### Example

```php
if ($error !== null) {
    var_dump($error);
} else {
    var_dump($ret);
}
```

---

### 7. Requirements

- PHP version: The SDK version `^7.0` supports PHP 5.3.3 and higher (up to PHP 8.x in later releases).
- Extensions: Ensure the `cURL` and `xml` PHP extensions are enabled, as they are required by the SDK.

You can check your PHP version and extensions with:

```bash
php -v
php -m
```

---

### 8. Where to Go Next

- **Documentation**: For more details, refer to the [official Qiniu PHP SDK documentation](https://developer.qiniu.com/kodo/sdk/php) or the [GitHub repository](https://github.com/qiniu/php-sdk).
- **Examples**: Check the `examples/` directory in the GitHub repo for more use cases.
- **Support**: If you encounter issues, submit a ticket to Qiniu support (<support@qiniu.com>) or ask in their community forums.

---

### Full Example Code

Here’s a complete script to upload a file:

```php
<?php
require_once 'vendor/autoload.php';

use Qiniu\Auth;
use Qiniu\Storage\UploadManager;

$accessKey = 'YOUR_ACCESS_KEY';
$secretKey = 'YOUR_SECRET_KEY';
$bucket = 'YOUR_BUCKET_NAME';
$filePath = '/path/to/your/file.txt';
$key = 'file.txt';

$auth = new Auth($accessKey, $secretKey);
$token = $auth->uploadToken($bucket);
$uploadMgr = new UploadManager();

list($ret, $error) = $uploadMgr->putFile($token, $key, $filePath);

if ($error !== null) {
    echo "Upload failed: " . $error->message();
} else {
    echo "Upload successful! File hash: " . $ret['hash'];
}
```

Replace the placeholder values (`YOUR_ACCESS_KEY`, `YOUR_SECRET_KEY`, `YOUR_BUCKET_NAME`, `/path/to/your/file.txt`) with your actual data, and you’re good to go!

Let me know if you need help with a specific feature!
