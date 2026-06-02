---
audio: false
generated: true
lang: zh
layout: post
title: 七牛云PHP SDK
translated: true
type: note
---

要在 PHP 中使用 `"qiniu/php-sdk": "^7.0"`，您需要将七牛云 PHP SDK 集成到项目中。该 SDK 允许您与七牛云存储服务进行交互，例如上传文件、管理存储桶等。以下是入门指南：

---

### 1. 安装七牛云 PHP SDK

推荐通过 PHP 的依赖管理工具 Composer 安装 SDK。请确保系统已安装 Composer。

#### 步骤

- 打开终端并进入项目目录。
- 运行以下命令将七牛云 PHP SDK（7.x 版本）添加到项目：

  ```bash
  composer require qiniu/php-sdk "^7.0"
  ```

- Composer 会将 SDK 及其依赖项下载到 `vendor/` 目录，并生成自动加载文件。

如果未安装 Composer，可从 [getcomposer.org](https://getcomposer.org/) 下载。

---

### 2. 项目配置

安装完成后，需在 PHP 脚本中包含自动加载器以使用 SDK 类。

#### 示例

在项目目录中创建 PHP 文件（如 `index.php`），并在顶部添加以下行：

```php
require_once 'vendor/autoload.php';
```

这确保需要时自动加载 SDK 类。

---

### 3. 配置认证

使用七牛 SDK 需要七牛账户的 `AccessKey` 和 `SecretKey`，可从七牛账户仪表盘获取。

#### 示例

```php
use Qiniu\Auth;

$accessKey = '您的ACCESS_KEY';
$secretKey = '您的SECRET_KEY';

$auth = new Auth($accessKey, $secretKey);
```

将 `'您的ACCESS_KEY'` 和 `'您的SECRET_KEY'` 替换为实际凭证。

---

### 4. 基础用法：上传文件

使用七牛 SDK 最常见的任务之一是上传文件到存储桶。以下是上传本地文件的示例。

#### 示例

```php
use Qiniu\Storage\UploadManager;

$bucket = '您的存储桶名称'; // 替换为七牛存储桶名称
$filePath = '/路径/到/您的/file.txt'; // 要上传文件的本地路径
$key = 'file.txt'; // 文件在七牛存储中的名称（可设为 null 使用原文件名）

$token = $auth->uploadToken($bucket); // 生成上传令牌
$uploadMgr = new UploadManager();

list($ret, $error) = $uploadMgr->putFile($token, $key, $filePath);

if ($error !== null) {
    echo "上传失败：" . $error->message();
} else {
    echo "上传成功！文件哈希值：" . $ret['hash'];
}
```

- `$bucket`：七牛存储桶名称。
- `$filePath`：要上传文件的本地路径。
- `$key`：文件在七牛存储中的键名（名称）。若设为 `null`，七牛将基于文件哈希生成键名。
- `$token`：使用凭证和存储桶名称生成的上传令牌。
- `putFile` 方法返回数组：`$ret`（成功信息）和 `$error`（错误信息，如果有）。

---

### 5. 其他功能

七牛云 PHP SDK 还提供许多其他功能，例如：

- **管理存储桶**：使用 `Qiniu\Storage\BucketManager` 列出文件、删除文件或管理存储桶设置。
- **文件操作**：复制、移动或删除存储桶中的文件。
- **图片处理**：生成调整大小或格式化图片的 URL。

#### 示例：列出存储桶中的文件

```php
use Qiniu\Storage\BucketManager;

$bucketMgr = new BucketManager($auth);
list($ret, $error) = $bucketMgr->listFiles($bucket);

if ($error !== null) {
    echo "错误：" . $error->message();
} else {
    echo "存储桶中的文件：\n";
    foreach ($ret['items'] as $item) {
        echo $item['key'] . "\n";
    }
}
```

---

### 6. 错误处理

执行 SDK 操作后请务必检查 `$error` 变量。如果操作失败，`$error` 将包含错误详情。

#### 示例

```php
if ($error !== null) {
    var_dump($error);
} else {
    var_dump($ret);
}
```

---

### 7. 环境要求

- PHP 版本：SDK 版本 `^7.0` 支持 PHP 5.3.3 及以上（后续版本支持 PHP 8.x）。
- 扩展：确保启用 `cURL` 和 `xml` PHP 扩展，SDK 需要这些扩展。

可通过以下命令检查 PHP 版本和扩展：

```bash
php -v
php -m
```

---

### 8. 后续步骤

- **文档**：更多详情请参阅 [七牛云 PHP SDK 官方文档](https://developer.qiniu.com/kodo/sdk/php) 或 [GitHub 仓库](https://github.com/qiniu/php-sdk)。
- **示例**：查看 GitHub 仓库中的 `examples/` 目录获取更多用例。
- **支持**：如果遇到问题，请提交工单至七牛云支持（<support@qiniu.com>）或在社区论坛提问。

---

### 完整示例代码

以下是上传文件的完整脚本：

```php
<?php
require_once 'vendor/autoload.php';

use Qiniu\Auth;
use Qiniu\Storage\UploadManager;

$accessKey = '您的ACCESS_KEY';
$secretKey = '您的SECRET_KEY';
$bucket = '您的存储桶名称';
$filePath = '/路径/到/您的/file.txt';
$key = 'file.txt';

$auth = new Auth($accessKey, $secretKey);
$token = $auth->uploadToken($bucket);
$uploadMgr = new UploadManager();

list($ret, $error) = $uploadMgr->putFile($token, $key, $filePath);

if ($error !== null) {
    echo "上传失败：" . $error->message();
} else {
    echo "上传成功！文件哈希值：" . $ret['hash'];
}
```

将占位值（`您的ACCESS_KEY`、`您的SECRET_KEY`、`您的存储桶名称`、`/路径/到/您的/file.txt`）替换为实际数据，即可开始使用！

如有特定功能需要帮助，请随时告知！
