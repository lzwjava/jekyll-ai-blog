---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Cache System Overview
translated: false
type: note
---

### Overview of CodeIgniter's Cache Library

CodeIgniter's `CI_Cache` class is a flexible caching system that provides a unified interface for storing and retrieving data across various backends (like in-memory, file-based, or external services). It extends `CI_Driver_Library`, which loads drivers dynamically. The class abstracts cache operations, allowing developers to switch backends easily via configuration without changing application code. All methods delegate to the active "adapter" (a driver class), with fallback support for reliability.

The system emphasizes performance, portability, and fault tolerance—e.g., it defaults to a "dummy" (no-op) driver if others fail, ensuring the app doesn't break due to cache issues.

### Supported Cache Drivers and Adapters

The class supports several drivers, defined in `$valid_drivers`:

- **apc**: Uses PHP's APC (Alternative PHP Cache) for in-memory storage (fast, built-in).
- **dummy**: A placeholder that does nothing (always returns TRUE or FALSE); used as a fallback for development/testing.
- **file**: Stores data as serialized files in a directory (specified by `$_cache_path`), suitable for low-traffic sites.
- **memcached**: Interface to the Memcached service for distributed, in-memory caching (high-performance, scalable).
- **redis**: Interface to Redis, another in-memory key-value store with features like pub/sub and atomic operations.
- **wincache**: Windows-specific for IIS (uses Microsoft WinCache).

Each driver is a separate class (e.g., `CI_Cache_memcached`) implementing methods like `get()`, `save()`, etc. The library loads the driver dynamically based on the `$config['adapter']` array passed to the constructor.

### Initialization and Configuration

- **Constructor**: Takes a `$config` array with keys for `adapter` (primary driver), `backup` (fallback driver), and `key_prefix` (string prepended to all cache keys for namespacing/isolation).
  - Example config: `array('adapter' => 'redis', 'backup' => 'file', 'key_prefix' => 'myapp_')`.
- **Fallback Logic**: After initializing, it checks if the primary adapter is supported using `is_supported($driver)` (which calls the driver's `is_supported()` method, testing for required PHP extensions or services).
  - If primary fails, it switches to the backup driver. If both fail, it logs an error and defaults to "dummy" (via `log_message()`).
  - This ensures the cache always has a working adapter, preventing crashes.

The `$_cache_path` is set for file-based drivers, but it's not initialized here—likely handled in the file driver class.

### Key Methods and How They Operate

Methods prepend the `key_prefix` to IDs for unique scoping (e.g., `'myapp_user123'`) and delegate to the active adapter. All operations return booleans, arrays, or mixed data on success/failure.

- **get($id)**: Retrieves cached data by ID.
  - Example: `$data = $cache->get('user_profile');` —calls the adapter's `get()` method.
  - If the key exists and hasn't expired, returns the data; otherwise, returns FALSE.
  - No direct TTL enforcement here; handled by the driver (e.g., Redis or Memcached enforce TTL internally).

- **save($id, $data, $ttl = 60, $raw = FALSE)**: Stores data with a time-to-live (TTL) in seconds.
  - Example: `$cache->save('user_profile', $profile_data, 3600);` —stores with 1-hour expiration.
  - `$raw` flag (false by default) indicates if data is serialized—drivers handle serialization if needed (e.g., arrays/objects become strings).
  - Returns TRUE on success, facilitating conditional logic (e.g., generate and cache data if saving fails).

- **delete($id)**: Removes a specific cache item.
  - Example: `$cache->delete('user_profile');` —permanent removal.

- **increment($id, $offset = 1)** and **decrement($id, $offset = 1)**: Atomic operations for numeric values (useful for counters).
  - Example: `$new_counter = $cache->increment('hits', 5);` —increments by 5 if supported by driver (e.g., Redis/Memcached are atomic; file-based may simulate).
  - Not all drivers support raw/inc/dec (dummy always fails); returns new value or FALSE.

- **clean()**: Clears all cache data for the current driver.
  - Example: `$cache->clean();` —useful for flushing after updates.
  - The "user" type targets user-specific data, not system caches.

- **cache_info($type = 'user')**: Returns metadata about the cache (e.g., server stats, key counts, or file paths).
  - Example: `$info = $cache->cache_info();` —an array of details from the driver.

- **get_metadata($id)**: Gets details about a specific cached item (e.g., expiration time, size).
  - Example: `$meta = $cache->get_metadata('key');` —helps debug or optimize.

- **is_supported($driver)**: Checks driver availability (caches results using a static `$support` array to avoid repeated checks).

### Additional Mechanics

- **Key Prefixing**: Applied automatically to all IDs (e.g., for app isolation or multi-tenancy). Enabled via config to prevent key collisions across environments.
- **Logging**: Uses `log_message()` for debug/ error messages (e.g., fallbacks), integrating with CodeIgniter's logging system.
- **Flexibility and Fault Tolerance**: By abstracting backends, you can switch from file caching (cheap, local) to Redis (fast, distributed) with minimal changes. The dummy fallback means cache failures don't halt the app—methods just return FALSE, letting code proceed (e.g., fetch from DB instead).
- **Performance Notes**: Drivers like APC/Redis are in-memory (fast access, sub-millisecond). File-based is slower due to disk I/O. TTLs are generally obeyed by drivers except in rare driver-specific edge cases.

This design makes CodeIgniter's caching modular and reliable. For details on specific drivers, check the driver files (e.g., `Cache_memcached.php`). Always refer to the official CodeIgniter docs for version-specific nuances, as this code is from an older version (around 2.0-3.x). If you have a specific method or driver in mind, I can dive deeper!
