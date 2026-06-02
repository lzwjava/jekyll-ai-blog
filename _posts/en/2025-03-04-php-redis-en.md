---
audio: false
generated: true
lang: en
layout: post
title: Redis client for PHP
translated: false
type: note
---

To use the `"predis/predis": "1.1"` library in PHP, you're referring to a Redis client for PHP that can be installed via Composer. Here's a step-by-step guide to set it up and use it in your PHP project:

---

### 1. **Install Composer (if not already installed)**
If you don’t have Composer installed, download and install it from [getcomposer.org](https://getcomposer.org/). It’s a dependency manager for PHP.

---

### 2. **Set Up Your Project**
If you don’t already have a project, create a directory for it:
```bash
mkdir my-redis-project
cd my-redis-project
```

---

### 3. **Add Predis to Your Project**
Run the following Composer command to install version 1.1 of Predis:
```bash
composer require predis/predis:1.1
```
This will download Predis version 1.1 and generate a `composer.json` file (and a `vendor` directory with the library).

Alternatively, if you already have a `composer.json` file, you can manually add this line to it:
```json
{
    "require": {
        "predis/predis": "1.1"
    }
}
```
Then run:
```bash
composer install
```

---

### 4. **Include the Autoloader**
In your PHP script, include the Composer autoloader to load Predis:
```php
require 'vendor/autoload.php';
```

---

### 5. **Basic Usage Example**
Here’s a simple example of how to connect to a Redis server and use Predis:

```php
<?php
require 'vendor/autoload.php';

use Predis\Client;

// Create a new Redis client instance
$redis = new Client([
    'scheme' => 'tcp',
    'host'   => '127.0.0.1', // Replace with your Redis server host
    'port'   => 6379,        // Default Redis port
]);

// Set a key-value pair
$redis->set('mykey', 'Hello, Redis!');

// Get the value back
$value = $redis->get('mykey');
echo $value; // Outputs: Hello, Redis!

// Example with a list
$redis->lpush('mylist', 'item1');
$redis->lpush('mylist', 'item2');
$list = $redis->lrange('mylist', 0, -1);
print_r($list); // Outputs: Array ( [0] => item2 [1] => item1 )
?>
```

---

### 6. **Configuration Options**
You can customize the connection by passing an array of options to the `Client` constructor. For example:
```php
$redis = new Client([
    'scheme' => 'tcp',
    'host'   => 'redis.example.com',
    'port'   => 6379,
    'password' => 'yourpassword', // If authentication is required
    'database' => 0,              // Select a specific Redis database
]);
```

---

### 7. **Common Commands**
Predis supports most Redis commands directly as methods. Here are a few examples:
- **Strings**: `set`, `get`, `incr`, `decr`
- **Lists**: `lpush`, `rpush`, `lpop`, `rpop`, `lrange`
- **Sets**: `sadd`, `smembers`, `srem`
- **Hashes**: `hset`, `hget`, `hgetall`

For a full list, check the [Predis documentation](https://github.com/predis/predis) or the Redis command reference.

---

### 8. **Error Handling**
Wrap your Redis calls in a try-catch block to handle potential connection or runtime errors:
```php
try {
    $redis->set('test', 'value');
    echo $redis->get('test');
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
```

---

### 9. **Prerequisites**
- Ensure you have a Redis server running (e.g., locally via `redis-server` or on a remote host).
- PHP 5.3.0 or higher (Predis 1.1 is compatible with older PHP versions, but check your environment).

---

That’s it! You’re now set up to use Predis 1.1 in your PHP project. Let me know if you need help with specific Redis operations or troubleshooting!
