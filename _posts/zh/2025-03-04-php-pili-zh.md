---
audio: false
generated: true
lang: zh
layout: post
title: Pili流媒体云PHP库
translated: true
type: note
---

### 核心要点
- 要使用 "pili-engineering/pili-sdk-php": "dev-master"，似乎需要通过 Composer 安装并配置七牛云凭证。
- 研究表明该包要求 PHP 5.3.0 或更高版本，用于七牛云的 Pili 流媒体云服务。
- 证据表明需要创建 Hub 对象并使用流操作（如生成 RTMP 地址），但具体方法可能有所不同。

### 安装步骤
首先确保已安装 Composer。在 `composer.json` 文件中添加包依赖：
```json
"require": {
    "pili-engineering/pili-sdk-php": "dev-master"
}
```
然后运行 `composer install` 或 `composer update`。在 PHP 脚本中引入：
```php
require 'vendor/autoload.php';
```

### 配置与使用
需要拥有七牛账户和 Pili Hub。设置访问密钥、秘密密钥和 Hub 名称后创建 Hub 对象：
```php
use Qiniu\Credentials;
use Pili\Hub;

$credentials = new Credentials('your_access_key', 'your_secret_key');
$hub = new Hub($credentials, 'your_hub_name');
```
创建或获取流，例如 `$stream = $hub->createStream('your_stream_key');`，并使用诸如 `$stream->rtmpPublishUrl(60)` 等方法进行操作。

### 注意事项
请注意 "dev-master" 是开发版本，可能不稳定，生产环境建议使用如 1.5.5 等标签版本。

---

### 使用 "pili-engineering/pili-sdk-php": "dev-master" 完整指南

本指南基于现有文档和示例，详细探讨如何使用 "dev-master" 版本的 "pili-engineering/pili-sdk-php" 包。内容涵盖安装、配置、使用及额外注意事项，帮助开发者全面理解 Pili 流媒体云服务的使用方法。

#### 背景与上下文
"pili-engineering/pili-sdk-php" 包是用于 PHP 的服务端库，专为与七牛云关联的 Pili 流媒体云服务交互而设计。"dev-master" 版本指最新的开发分支，可能包含新功能但稳定性不如标签版本。该包要求 PHP 5.3.0 或更高版本，截至 2025年3月3日 仍适用于多数 PHP 环境。

#### 安装流程
首先需要安装 Composer（PHP 依赖管理工具）。安装过程包括将包添加到项目的 `composer.json` 文件并运行 Composer 命令下载：

- 在 `composer.json` 的 "require" 部分添加：
  ```json
  "require": {
      "pili-engineering/pili-sdk-php": "dev-master"
  }
  ```
- 在终端执行 `composer install` 或 `composer update` 获取包及其依赖，这将创建包含必要文件的 `vendor` 目录
- 在 PHP 脚本中引入自动加载器以访问包类：
  ```php
  require 'vendor/autoload.php';
  ```

此流程确保包集成到项目中，利用 Composer 的自动加载功能便捷访问类。

#### 前置条件与配置
使用 SDK 前需要拥有七牛账户并设置 Pili Hub，因为 SDK 需与 Pili 流媒体云服务交互。这涉及从七牛获取访问密钥和秘密密钥，并在其平台创建 Hub。文档表明这些凭证是身份验证的必备要素。

配置时在 PHP 脚本中定义凭证：
- 访问密钥：您的七牛访问密钥
- 秘密密钥：您的七牛秘密密钥
- Hub 名称：您的 Pili Hub 名称（需预先存在）

配置示例如下：
```php
$accessKey = 'your_access_key';
$secretKey = 'your_secret_key';
$hubName = 'your_hub_name';
```

#### 创建和使用 Hub 对象
SDK 的核心是 Hub 对象，用于流管理。首先使用七牛密钥创建凭证对象：
```php
use Qiniu\Credentials;

$credentials = new Credentials($accessKey, $secretKey);
```
然后用这些凭证和 Hub 名称实例化 Hub 对象：
```php
use Pili\Hub;

$hub = new Hub($credentials, $hubName);
```
该 Hub 对象支持执行各种流相关操作，如创建、检索或列出流。

#### 流操作管理
流是 Pili 流媒体云的核心，SDK 通过 Hub 对象提供管理方法。创建新流：
```php
$streamKey = 'your_stream_key'; // 在 Hub 内必须唯一
$stream = $hub->createStream($streamKey);
```
检索现有流：
```php
$stream = $hub->getStream($streamKey);
```
流对象随后提供多种操作方法，基于现有文档总结如下表：

| **操作类型**          | **方法**                     | **功能说明**                                      |
|-------------------------|--------------------------------|------------------------------------------------------|
| 创建流          | `$hub->createStream($key)`     | 使用指定键创建新流             |
| 获取流             | `$hub->getStream($key)`        | 通过键检索现有流                 |
| 列出流           | `$hub->listStreams($marker, $limit, $prefix)` | 通过分页选项列出流               |
| RTMP 推流地址       | `$stream->rtmpPublishUrl($expire)` | 生成带过期时间的 RTMP 推流地址  |
| RTMP 播放地址          | `$stream->rtmpPlayUrl()`       | 生成流的 RTMP 播放地址           |
| HLS 播放地址           | `$stream->hlsPlayUrl()`        | 生成流媒体 HLS 播放地址             |
| 禁用流         | `$stream->disable()`           | 禁用流                                 |
| 启用流          | `$stream->enable()`            | 启用流                                  |
| 获取流状态      | `$stream->status()`            | 检索流的当前状态          |

例如生成 60 秒过期的 RTMP 推流地址：
```php
$expire = 60;
$url = $stream->rtmpPublishUrl($expire);
echo $url;
```
此地址可用于向 Pili 流媒体云发布流，过期机制确保临时访问安全。

#### 额外注意事项
- **版本稳定性**："dev-master" 是开发分支，可能不稳定。生产环境建议使用标签版本，例如 Packagist 上提供的 1.5.5 版本 [pili-engineering/pili-sdk-php 版本列表](https://packagist.org/p/pili-engineering/pili-sdk-php)。版本历史显示 API 添加和方法优化等更新，最早可追溯至 2016 年
- **错误处理**：文档建议在操作中使用 try-catch 块处理潜在异常，这在流创建和检索的示例中有所体现
- **文档与示例**：虽然具体示例不够详尽，但 GitHub 仓库 [Pili 流媒体云 PHP 服务端库](https://github.com/pili-engineering/pili-sdk-php) 提供了安装说明和功能列表，与其他语言 SDK（如 Python）的对比也显示出类似功能（如地址生成）

#### 对比分析
与其他 Pili SDK（如 Python 版本）比较可见相似模式：都需要凭证、Hub 设置和流操作。但 PHP 版本采用 Hub 和 Stream 类的面向对象方式，与 Python 的函数式风格形成对比。这符合 PHP 的典型开发实践，提供类型安全和 IDE 支持。

#### 总结
使用 "pili-engineering/pili-sdk-php": "dev-master" 需通过 Composer 安装，配置七牛凭证，创建 Hub 对象，并使用如 `rtmpPublishUrl` 等方法管理流。请确保环境满足 PHP 5.3.0+ 要求，生产环境需考虑稳定性。本指南提供完整入门指导，更多细节请参考官方文档和代码仓库。

### 关键引用
- [Pili 流媒体云 PHP 服务端库 GitHub](https://github.com/pili-engineering/pili-sdk-php)
- [pili-engineering/pili-sdk-php 版本 Packagist](https://packagist.org/p/pili-engineering/pili-sdk-php)
