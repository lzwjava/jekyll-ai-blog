---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter钩子机制详解
translated: true
type: note
---

### 什么是 CodeIgniter 中的钩子？

CodeIgniter 中的钩子提供了一种无需修改框架核心文件即可扩展功能的方式。它们允许你在执行周期的特定节点（例如控制器加载前后、输出重写或缓存处理时）运行自定义代码。这种方式通过将你的代码与官方代码库分离，保持了框架的可升级性。

钩子在 `application/config/hooks.php` 中定义，并在 `application/config/config.php` 中通过设置 `$config['enable_hooks'] = TRUE;` 启用。

### 启用钩子

1. 打开 `application/config/config.php`
2. 设置配置变量：

   ```php
   $config['enable_hooks'] = TRUE;
   ```

   这会使 CodeIgniter 检查并执行钩子文件

### 定义钩子

钩子在 `application/config/hooks.php` 中以数组形式配置。每个钩子数组需指定：

- `class`：（必需）类名（必须与文件名匹配）
- `function`：（必需）类中的方法名
- `filename`：（必需）类文件名（不含 .php 后缀）
- `filepath`：（可选）文件目录路径，默认为 `application/hooks/`
- `params`：（可选）传递给方法的参数数组

请将钩子类放置在 `application/hooks/` 目录中

### 钩子触发点

CodeIgniter 提供以下预定义的钩子执行节点：

- **pre_system**：系统加载前执行（此时其他组件尚未运行）
- **pre_controller**：控制器调用前立即执行
- **post_controller_constructor**：控制器实例化后但方法执行前运行
- **post_controller**：控制器执行完毕后运行
- **display_override**：替代输出到浏览器的默认行为（重写 _display 创建/退出控制器文件）
- **cache_override**：替代加载缓存的默认行为（重写 _display 缓存）
- **post_system**：网页完全发送到浏览器后执行

### 使用示例

假设需要在控制器运行前记录每个请求，可以创建针对 `pre_controller` 的钩子：

1. 创建文件 `application/hooks/my_hook.php`：

   ```php
   <?php
   class My_hook {
       public function log_request() {
           // 示例：记录到文件或数据库
           log_message('info', 'Controller about to be called: ' . $this->uri->uri_string());
       }
   }
   ```

2. 在 `application/config/hooks.php` 中添加：

   ```php
   $hook['pre_controller'] = array(
       'class' => 'My_hook',
       'function' => 'log_request',
       'filename' => 'my_hook.php',
       'filepath' => 'hooks', // 可选参数，默认为 application/hooks/
       'params' => array() // 可选参数
   );
   ```

现在每次控制器即将运行时，`log_request` 方法都会自动执行。

### 最佳实践

- 谨慎使用钩子，优先考虑扩展控制器或使用类库
- 始终在开发环境中测试钩子，确保不会干扰核心逻辑
- 更多细节请参考 CodeIgniter 官方用户指南中关于钩子的章节
