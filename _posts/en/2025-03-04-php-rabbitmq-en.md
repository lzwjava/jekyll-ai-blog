---
audio: false
generated: true
lang: en
layout: post
title: Using RabbitMQ in PHP
translated: false
type: note
---

### Key Points
- It seems likely that to use "php-amqplib/php-amqplib" version 2.6.*, you need to install it via Composer and follow basic steps for sending and receiving messages with RabbitMQ.
- The process involves setting up a connection, declaring a queue, and using methods like `basic_publish` for sending and `basic_consume` with a loop for receiving, which may differ slightly from newer versions.
- Research suggests that for version 2.6.*, the consuming process requires a manual loop with `wait()`, unlike newer versions that might use a `consume()` method.

---

### Installation and Setup
To get started with "php-amqplib/php-amqplib" version 2.6.*, first install it using Composer by running:

```bash
composer require "php-amqplib/php-amqplib:2.6.*"
```

Ensure RabbitMQ is installed and running on your system, typically accessible at `localhost:5672` with default credentials (`guest/guest`). Adjust these settings if your setup differs.

### Sending Messages
To send a message, include the necessary PHP files and create a connection:

```php
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();
```

Declare a queue and publish your message:

```php
$channel->queue_declare('hello', false, false, false, false);
$msg = new AMQPMessage('Hello World!');
$channel->basic_publish($msg, '', 'hello');
echo " [x] Sent 'Hello World!'\n";
```

Finally, close the connection:

```php
$channel->close();
$connection->close();
```

### Receiving Messages
For receiving, set up similarly but define a callback for message handling:

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

Note that for version 2.6.*, you need the loop with `wait()` to keep consuming, which is an unexpected detail compared to newer versions that might use a simpler `consume()` method.

---

### Survey Note: Detailed Usage of "php-amqplib/php-amqplib" Version 2.6.*

This section provides a comprehensive guide on using the "php-amqplib/php-amqplib" library, specifically version 2.6.*, for interacting with RabbitMQ, a popular message queue system. The information is derived from official documentation, tutorials, and version-specific details, ensuring a thorough understanding for developers.

#### Background and Context
"php-amqplib/php-amqplib" is a PHP library for communicating with RabbitMQ, implementing the AMQP 0.9.1 protocol. Version 2.6.* is an older release, and while the library has evolved to version 3.x.x by March 2025, understanding its usage in this specific version is crucial for legacy systems or specific project requirements. The library is maintained by contributors including Ramūnas Dronga and Luke Bakken, with significant involvement from VMware engineers working on RabbitMQ ([GitHub - php-amqplib/php-amqplib](https://github.com/php-amqplib/php-amqplib)).

RabbitMQ tutorials, such as those on the official RabbitMQ website, provide examples that are generally applicable but may reflect newer versions. For version 2.6.*, adjustments are necessary, particularly in the consuming process, as detailed below.

#### Installation Process
To begin, install the library using Composer, the PHP dependency manager. Run the following command in your project directory:

```bash
composer require "php-amqplib/php-amqplib:2.6.*"
```

This command ensures the library is downloaded and configured for use, with Composer managing dependencies. Ensure RabbitMQ is installed and running, typically accessible at `localhost:5672` with default credentials (`guest/guest`). For production, adjust host, port, and credentials as needed, and consult [CloudAMQP PHP Documentation](https://www.cloudamqp.com/docs/php.html) for managed broker setups.

#### Sending Messages: Step-by-Step
Sending messages involves establishing a connection and publishing to a queue. Here’s the process:

1. **Include Required Files:**
   Use the Composer autoloader to include the library:

   ```php
   require_once __DIR__ . '/vendor/autoload.php';
   use PhpAmqpLib\Connection\AMQPStreamConnection;
   use PhpAmqpLib\Message\AMQPMessage;
   ```

2. **Create Connection and Channel:**
   Initialize a connection to RabbitMQ and open a channel:

   ```php
   $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
   $channel = $connection->channel();
   ```

   The parameters are host, port, username, and password, with defaults as shown. For SSL or other configurations, refer to [RabbitMQ PHP Tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-php).

3. **Declare Queue and Publish:**
   Declare a queue to ensure it exists, then publish a message:

   ```php
   $channel->queue_declare('hello', false, false, false, false);
   $msg = new AMQPMessage('Hello World!');
   $channel->basic_publish($msg, '', 'hello');
   echo " [x] Sent 'Hello World!'\n";
   ```

   Here, `queue_declare` creates a queue named 'hello' with default settings (non-durable, non-exclusive, auto-delete). `basic_publish` sends the message to the queue.

4. **Close Connection:**
   After sending, close the channel and connection to free resources:

   ```php
   $channel->close();
   $connection->close();
   ```

This process is standard across versions, with no significant changes noted in the changelog for version 2.6.* compared to later releases.

#### Receiving Messages: Version-Specific Details
Receiving messages in version 2.6.* requires careful attention, as the consuming mechanism differs from newer versions. Here’s the detailed process:

1. **Include Required Files:**
   Similar to sending, include the autoloader and necessary classes:

   ```php
   require_once __DIR__ . '/vendor/autoload.php';
   use PhpAmqpLib\Connection\AMQPStreamConnection;
   ```

2. **Create Connection and Channel:**
   Establish the connection and channel as before:

   ```php
   $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
   $channel = $connection->channel();
   ```

3. **Declare Queue:**
   Ensure the queue exists, matching the sender’s declaration:

   ```php
   $channel->queue_declare('hello', false, false, false, false);
   ```

4. **Define Callback:**
   Create a callback function to handle received messages:

   ```php
   $callback = function ($msg) {
       echo ' [x] Received ', $msg->body, "\n";
   };
   ```

   This function will be called for each message, printing the body in this example.

5. **Consume Messages:**
   For version 2.6.*, use `basic_consume` to register the callback, then enter a loop to keep consuming:

   ```php
   $channel->basic_consume('hello', '', false, true, false, false, $callback);
   while (count($channel->callbacks)) {
       $channel->wait();
   }
   ```

   The `basic_consume` method takes parameters for queue name, consumer tag, no-local, no-ack, exclusive, no-wait, and callback. The loop with `wait()` keeps the consumer running, checking for messages. This is an important detail, as newer versions (e.g., 3.2) might use a `consume()` method, which was not available in 2.6.* based on API documentation review.

6. **Close Connection:**
   After consuming, close the resources:

   ```php
   $channel->close();
   $connection->close();
   ```

An unexpected detail is the need for the manual loop in version 2.6.*, which may require additional error handling for production use, such as catching exceptions for connection issues.

#### Version-Specific Considerations
Version 2.6.* is part of the older releases, and while the changelog does not explicitly list it, versions around 2.5 to 2.7 show enhancements like heartbeat support and PHP 5.3 compatibility. For large messages, version 2.6.* supports `setBodySizeLimit` on the channel to handle memory limits, truncating messages if needed, with details in [GitHub - php-amqplib/php-amqplib](https://github.com/php-amqplib/php-amqplib).

Comparing to version 3.2, changes include PHP 8 support and new methods like `consume()`, but the core functionality for sending and basic consuming remains similar. Users should test for compatibility, especially with PHP versions, as 2.6.* likely supports PHP 5.3 to 7.x, per changelog entries.

#### Troubleshooting and Best Practices
- If sending fails, check RabbitMQ logs for resource alarms, such as disk space below 50 MB, and adjust settings via [RabbitMQ Configuration Guide](https://www.rabbitmq.com/configure.html#config-items).
- For consuming, ensure the consumer runs continuously; use tools like Supervisor for daemonizing in production.
- List queues using `rabbitmqctl list_queues` on Linux or `rabbitmqctl.bat list_queues` on Windows as a privileged user, per [RabbitMQ Command Line Tools](https://www.rabbitmq.com/cli.html).

#### Table: Version Comparison for Key Methods

| Method             | Version 2.6.* Behavior                          | Version 3.2 Behavior                          |
|--------------------|------------------------------------------------|----------------------------------------------|
| `basic_publish`    | Standard, publishes to queue                    | Unchanged, same usage                        |
| `basic_consume`    | Requires loop with `wait()` for consuming       | Similar, but `consume()` method available     |
| `setBodySizeLimit` | Supported for large messages, truncates if set | Supported, same functionality                |
| PHP Compatibility  | Likely 5.3 to 7.x                               | Supports PHP 7.x and 8.x                     |

This table highlights the key difference in consuming, which is critical for version 2.6.* users.

#### Conclusion
Using "php-amqplib/php-amqplib" version 2.6.* involves standard Composer installation, with sending messages via `basic_publish` and receiving via `basic_consume` with a manual loop. While similar to newer versions, the consuming process requires additional attention, making it essential for developers to test and adjust for legacy systems. For further details, consult the official RabbitMQ tutorials and GitHub repository.

---

### Key Citations
- [GitHub - php-amqplib/php-amqplib The most widely used PHP client for RabbitMQ](https://github.com/php-amqplib/php-amqplib)
- [RabbitMQ tutorial - "Hello World!" PHP example](https://www.rabbitmq.com/tutorials/tutorial-one-php)
- [CloudAMQP PHP Documentation Get started with CloudAMQP and PHP](https://www.cloudamqp.com/docs/php.html)
- [php-amqplib/php-amqplib Packagist Formerly videlalvaro/php-amqplib](https://packagist.org/packages/php-amqplib/php-amqplib)
- [GitHub - php-amqplib/php-amqplib CHANGELOG file](https://github.com/php-amqplib/php-amqplib/blob/master/CHANGELOG.md)
- [RabbitMQ Configuration Guide Config items and settings](https://www.rabbitmq.com/configure.html#config-items)
- [RabbitMQ Command Line Tools CLI reference and usage](https://www.rabbitmq.com/cli.html)
