---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter缓存系统概述
translated: true
type: note
---

### CodeIgniter 缓存库概览

CodeIgniter 的 `CI_Cache` 类是一个灵活的缓存系统，为多种后端存储（如内存、文件或外部服务）提供了统一的存取接口。该类继承自 `CI_Driver_Library`，能够动态加载驱动程序。它抽象了缓存操作，使开发者可以通过配置轻松切换后端，而无需修改应用代码。所有方法都委托给当前激活的"适配器"（驱动类），并具备故障恢复机制以保障可靠性。

该系统注重性能、可移植性和容错性——例如，当其他驱动失效时默认启用"dummy"（空操作）驱动，确保应用不会因缓存问题而崩溃。

### 支持的缓存驱动与适配器

该类支持多种驱动，定义在 `$valid_drivers` 中：

- **apc**：使用 PHP 内置的 APC（Alternative PHP Cache）实现内存存储（高速、内置）。
- **dummy**：空操作占位驱动（始终返回 TRUE 或 FALSE），用于开发测试或作为降级方案。
- **file**：将数据序列化后存储到指定目录（通过 `$_cache_path` 配置），适用于低流量场景。
- **memcached**：连接 Memcached 服务实现分布式内存缓存（高性能、可扩展）。
- **redis**：连接 Redis 内存键值存储，支持发布订阅等高级特性。
- **wincache**：专为 Windows IIS 设计的驱动（基于微软 WinCache）。

每个驱动都是独立的类（如 `CI_Cache_memcached`），实现 `get()`、`save()` 等方法。库会根据构造函数传入的 `$config['adapter']` 数组动态加载对应驱动。

### 初始化与配置

- **构造函数**：接收包含 `adapter`（主驱动）、`backup`（备用驱动）和 `key_prefix`（缓存键前缀，用于命名空间隔离）的配置数组。
  - 示例配置：`array('adapter' => 'redis', 'backup' => 'file', 'key_prefix' => 'myapp_')`。
- **降级逻辑**：初始化后通过 `is_supported($driver)` 检测主驱动可用性（该方法会调用驱动自身的 `is_supported()` 来验证 PHP 扩展或服务）。
  - 若主驱动失效则切换至备用驱动。若两者皆失效，会通过 `log_message()` 记录错误并启用 "dummy" 驱动。
  - 这种机制确保缓存系统始终存在可用适配器，避免应用崩溃。

文件类驱动的 `$_cache_path` 路径设置不在本类中初始化，可能由文件驱动类自行处理。

### 核心方法及运作机制

所有方法都会为 ID 自动添加 `key_prefix` 实现唯一性（如 `'myapp_user123'`），并将操作委托给当前适配器。返回值包括布尔值、数组或混合数据类型。

- **get($id)**：根据 ID 获取缓存数据。
  - 示例：`$data = $cache->get('user_profile');` —— 调用适配器的 `get()` 方法。
  - 若键存在且未过期则返回数据，否则返回 FALSE。
  - 不直接处理 TTL，由驱动自行管理（如 Redis/Memcached 在内部维护 TTL）。

- **save($id, $data, $ttl = 60, $raw = FALSE)**：存储数据并设置存活时间（秒）。
  - 示例：`$cache->save('user_profile', $profile_data, 3600);` —— 存储 1 小时有效数据。
  - `$raw` 标志（默认 FALSE）指示是否已序列化数据，驱动会按需处理序列化（如将数组/对象转为字符串）。
  - 成功返回 TRUE，便于条件逻辑处理（例如当存储失败时重新生成数据）。

- **delete($id)**：删除指定缓存项。
  - 示例：`$cache->delete('user_profile');` —— 永久移除数据。

- **increment($id, $offset = 1)** 与 **decrement($id, $offset = 1)**：对数值进行原子操作（适用于计数器场景）。
  - 示例：`$new_counter = $cache->increment('hits', 5);` —— 若驱动支持则原子增加 5（如 Redis/Memcached 支持原子操作，文件驱动可能模拟实现）。
  - 并非所有驱动都支持原始值操作（dummy 驱动始终失败），返回新值或 FALSE。

- **clean()**：清空当前驱动的所有缓存数据。
  - 示例：`$cache->clean();` —— 适用于更新后的缓存刷新。
  - "user" 类型针对用户数据，不涉及系统缓存。

- **cache_info($type = 'user')**：返回缓存元数据（如服务器状态、键数量或文件路径）。
  - 示例：`$info = $cache->cache_info();` —— 获取驱动返回的详细信息数组。

- **get_metadata($id)**：获取特定缓存项的详细信息（如过期时间、数据大小）。
  - 示例：`$meta = $cache->get_metadata('key');` —— 用于调试或优化。

- **is_supported($driver)**：检测驱动可用性（通过静态 `$support` 数组缓存检测结果避免重复检查）。

### 扩展机制

- **键前缀机制**：自动为所有 ID 添加前缀（适用于应用隔离或多租户场景）。通过配置启用可防止跨环境键名冲突。
- **日志记录**：使用 `log_message()` 记录调试/错误信息（如降级事件），与 CodeIgniter 日志系统无缝集成。
- **灵活性与容错性**：通过抽象后端存储，只需少量配置即可从文件缓存（低成本、本地）切换至 Redis（高速、分布式）。dummy 降级机制确保缓存故障不会中断应用——方法仅返回 FALSE，使代码能继续执行（例如转而从数据库获取数据）。
- **性能说明**：APC/Redis 等内存驱动具有亚毫秒级响应速度，文件驱动因磁盘 I/O 较慢。除特定驱动的边缘情况外，TTL 机制通常能被严格遵循。

该设计使 CodeIgniter 缓存系统具备高度模块化和可靠性。如需了解具体驱动实现，请查阅驱动文件（如 `Cache_memcached.php`）。由于此代码基于旧版（约 2.0-3.x），请始终参考官方文档获取版本特定说明。若需深入了解特定方法或驱动，可进一步探讨！
