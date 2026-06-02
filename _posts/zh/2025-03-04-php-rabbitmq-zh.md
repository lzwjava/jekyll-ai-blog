---
audio: false
generated: true
lang: zh
layout: post
title: 在PHP中使用RabbitMQ
translated: true
type: note
---

### 核心要点

- 要使用 "php-amqplib/php-amqplib" 2.6.* 版本，似乎需要通过 Composer 安装，并遵循使用 RabbitMQ 发送和接收消息的基本步骤。
- 该过程涉及建立连接、声明队列，并使用 `basic_publish` 方法发送消息，以及使用带有循环的 `basic_consume` 方法接收消息，这可能与新版本略有不同。
- 研究表明，对于 2.6.* 版本，消费过程需要一个带有 `wait()` 的手动循环，这与可能使用更简单的 `consume()` 方法的新版本不同。

---

### 安装与设置

要开始使用 "php-amqplib/php-amqplib" 2.6.* 版本，首先通过运行以下命令使用 Composer 安装：

```bash
composer require "php-amqplib/php-amqplib:2.6.*"
```

确保 RabbitMQ 已安装并在您的系统上运行，通常可通过 `localhost:5672` 访问，使用默认凭据（`guest/guest`）。如果您的设置不同，请调整这些设置。

### 发送消息

要发送消息，请包含必要的 PHP 文件并创建连接：

```php
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
```

声明队列并发布您的消息：

```php
$channel->queue_declare('hello', false, false, false, false);
$msg = new AMQPMessage('Hello World!');
$channel->basic_publish($msg, '', 'hello');
echo " [x] Sent 'Hello World!'\n";
```

最后，关闭连接：

```php
$channel->close();
$connection->close();
```

### 接收消息

对于接收，类似地设置，但定义一个回调函数来处理消息：

```php
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
$channel->queue_declare('hello', false, false, false, false);

$callback = function ($msg) {
    echo ' [x] Received ', $msg->body, "\n";
};

$channel->basic_consume('hello', '', false, true, false, false, $callback);
while (count($channel->callbacks)) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

请注意，对于 2.6.* 版本，您需要带有 `wait()` 的循环来持续消费，这是一个与新版本可能使用的更简单的 `consume()` 方法相比出乎意料的细节。

---

### 调研笔记："php-amqplib/php-amqplib" 2.6.* 版本的详细用法

本节提供了关于使用 "php-amqplib/php-amqplib" 库（特别是 2.6.* 版本）与 RabbitMQ（一个流行的消息队列系统）交互的全面指南。这些信息来源于官方文档、教程和版本特定细节，确保开发人员能够透彻理解。

#### 背景与上下文

"php-amqplib/php-amqplib" 是一个用于与 RabbitMQ 通信的 PHP 库，实现了 AMQP 0.9.1 协议。2.6.* 版本是一个较旧的发布版本，虽然截至 2025 年 3 月该库已发展到 3.x.x 版本，但了解此特定版本的用法对于遗留系统或特定项目需求至关重要。该库由包括 Ramūnas Dronga 和 Luke Bakken 在内的贡献者维护，并且有从事 RabbitMQ 工作的 VMware 工程师的积极参与 ([GitHub - php-amqplib/php-amqplib](https://github.com/php-amqplib/php-amqplib))。

RabbitMQ 教程，例如官方 RabbitMQ 网站上的教程，提供了通常适用但可能反映新版本的示例。对于 2.6.* 版本，需要进行调整，特别是在消费过程中，如下所述。

#### 安装过程

首先，使用 PHP 依赖管理器 Composer 安装该库。在您的项目目录中运行以下命令：

```bash
composer require "php-amqplib/php-amqplib:2.6.*"
```

此命令确保库被下载并配置以供使用，Composer 负责管理依赖项。确保 RabbitMQ 已安装并运行，通常可通过 `localhost:5672` 访问，使用默认凭据（`guest/guest`）。对于生产环境，根据需要调整主机、端口和凭据，并参考 [CloudAMQP PHP Documentation](https://www.cloudamqp.com/docs/php.html) 以了解托管代理设置。

#### 发送消息：逐步指南

发送消息涉及建立连接并发布到队列。过程如下：

1. **包含必需文件：**
   使用 Composer 自动加载器包含该库：

   ```php
   require_once __DIR__ . '/vendor/autoload.php';
   use PhpAmqpLib\Connection\AMQPStreamConnection;
   use PhpAmqpLib\Message\AMQPMessage;
   ```

2. **创建连接和通道：**
   初始化到 RabbitMQ 的连接并打开一个通道：

   ```php
   $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
   $channel = $connection->channel();
   ```

   参数依次为主机、端口、用户名和密码，默认值如上所示。有关 SSL 或其他配置，请参考 [RabbitMQ PHP Tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-php)。

3. **声明队列并发布：**
   声明一个队列以确保其存在，然后发布消息：

   ```php
   $channel->queue_declare('hello', false, false, false, false);
   $msg = new AMQPMessage('Hello World!');
   $channel->basic_publish($msg, '', 'hello');
   echo " [x] Sent 'Hello World!'\n";
   ```

   此处，`queue_declare` 创建一个名为 'hello' 的队列，具有默认设置（非持久、非排他、自动删除）。`basic_publish` 将消息发送到该队列。

4. **关闭连接：**
   发送后，关闭通道和连接以释放资源：

   ```php
   $channel->close();
   $connection->close();
   ```

此过程是跨版本的标准过程，变更日志中未提及 2.6.* 版本与后续版本相比有显著变化。

#### 接收消息：版本特定细节

在 2.6.* 版本中接收消息需要特别注意，因为其消费机制与新版本不同。详细过程如下：

1. **包含必需文件：**
   与发送类似，包含自动加载器和必要的类：

   ```php
   require_once __DIR__ . '/vendor/autoload.php';
   use PhpAmqpLib\Connection\AMQPStreamConnection;
   ```

2. **创建连接和通道：**
   像之前一样建立连接和通道：

   ```php
   $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
   $channel = $connection->channel();
   ```

3. **声明队列：**
   确保队列存在，与发送方的声明匹配：

   ```php
   $channel->queue_declare('hello', false, false, false, false);
   ```

4. **定义回调：**
   创建一个回调函数来处理接收到的消息：

   ```php
   $callback = function ($msg) {
       echo ' [x] Received ', $msg->body, "\n";
   };
   ```

   此函数将为每条消息调用，在此示例中打印消息体。

5. **消费消息：**
   对于 2.6.* 版本，使用 `basic_consume` 注册回调，然后进入一个循环以持续消费：

   ```php
   $channel->basic_consume('hello', '', false, true, false, false, $callback);
   while (count($channel->callbacks)) {
       $channel->wait();
   }
   ```

   `basic_consume` 方法接受队列名称、消费者标签、no-local、no-ack、排他、no-wait 和回调等参数。带有 `wait()` 的循环保持消费者运行，检查消息。这是一个重要的细节，因为根据 API 文档审查，新版本（例如 3.2）可能使用 `consume()` 方法，而该方法在 2.6.* 版本中不可用。

6. **关闭连接：**
   消费后，关闭资源：

   ```php
   $channel->close();
   $connection->close();
   ```

一个出乎意料的细节是 2.6.* 版本需要手动循环，这对于生产使用可能需要额外的错误处理，例如捕获连接问题的异常。

#### 版本特定注意事项

2.6.*版本是旧版本系列的一部分，虽然变更日志没有明确列出它，但 2.5 到 2.7 左右的版本显示了诸如心跳支持和 PHP 5.3 兼容性等增强功能。对于大消息，2.6.* 版本支持在通道上使用 `setBodySizeLimit` 来处理内存限制，如果需要则截断消息，详细信息见 [GitHub - php-amqplib/php-amqplib](https://github.com/php-amqplib/php-amqplib)。

与 3.2 版本相比，变化包括 PHP 8 支持和像 `consume()` 这样的新方法，但发送和基本消费的核心功能保持相似。用户应测试兼容性，特别是与 PHP 版本的兼容性，因为根据变更日志条目，2.6.* 版本可能支持 PHP 5.3 到 7.x。

#### 故障排除与最佳实践

- 如果发送失败，请检查 RabbitMQ 日志中的资源警报，例如磁盘空间低于 50 MB，并通过 [RabbitMQ Configuration Guide](https://www.rabbitmq.com/configure.html#config-items) 调整设置。
- 对于消费，确保消费者持续运行；在生产环境中使用像 Supervisor 这样的工具进行守护进程化。
- 在 Linux 上使用 `rabbitmqctl list_queues` 或在 Windows 上使用 `rabbitmqctl.bat list_queues`（作为特权用户）列出队列，根据 [RabbitMQ Command Line Tools](https://www.rabbitmq.com/cli.html)。

#### 表格：关键方法的版本比较

| 方法                | 2.6.* 版本行为                            | 3.2 版本行为                            |
|---------------------|------------------------------------------|----------------------------------------|
| `basic_publish`     | 标准，发布到队列                         | 未改变，用法相同                       |
| `basic_consume`     | 需要带有 `wait()` 的循环进行消费         | 类似，但 `consume()` 方法可用          |
| `setBodySizeLimit`  | 支持大消息，如果设置则截断               | 支持，功能相同                         |
| PHP 兼容性          | 可能支持 5.3 到 7.x                      | 支持 PHP 7.x 和 8.x                    |

此表突出了消费方面的关键差异，这对 2.6.* 版本用户至关重要。

#### 结论

使用 "php-amqplib/php-amqplib" 2.6.* 版本涉及标准的 Composer 安装，通过 `basic_publish` 发送消息，并通过带有手动循环的 `basic_consume` 接收消息。虽然与新版本相似，但消费过程需要额外注意，这使得开发人员必须为遗留系统进行测试和调整。更多详细信息，请查阅官方 RabbitMQ 教程和 GitHub 仓库。

---

### 关键引用

- [GitHub - php-amqplib/php-amqplib 使用最广泛的 RabbitMQ PHP 客户端](https://github.com/php-amqplib/php-amqplib)
- [RabbitMQ 教程 - "Hello World!" PHP 示例](https://www.rabbitmq.com/tutorials/tutorial-one-php)
- [CloudAMQP PHP 文档 开始使用 CloudAMQP 和 PHP](https://www.cloudamqp.com/docs/php.html)
- [php-amqplib/php-amqplib Packagist 前身为 videlalvaro/php-amqplib](https://packagist.org/packages/php-amqplib/php-amqplib)
- [GitHub - php-amqplib/php-amqplib CHANGELOG 文件](https://github.com/php-amqplib/php-amqplib/blob/master/CHANGELOG.md)
- [RabbitMQ 配置指南 配置项和设置](https://www.rabbitmq.com/configure.html#config-items)
- [RabbitMQ 命令行工具 CLI 参考和用法](https://www.rabbitmq.com/cli.html)
