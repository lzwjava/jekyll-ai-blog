---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter自动加载系统概述
translated: true
type: note
---

### CodeIgniter 自动加载系统概述

在 CodeIgniter（一个 PHP 框架）中，`autoload.php` 文件（通常位于 `application/config/autoload.php`）允许您指定应在每个请求上自动加载的资源。这使得常用组件无需在每个控制器或其他地方手动加载即可使用，从而提高了效率并减少了代码重复。框架会在其初始化过程中，在路由请求之前加载这些资源。

该文件定义了一个 `$autoload` 数组，其中包含用于不同资源类型的子数组：包、库、驱动程序、辅助函数、配置文件、语言文件和模型。您可以在这些数组中填入要自动加载的资源名称。取消注释或修改相应行以启用加载；留空则跳过。

### 实际工作原理

CodeIgniter 的引导过程（通过 `index.php` 和 CI 核心）在系统初始化期间检查此文件。它会遍历 `$autoload` 数组，并通过以下方式加载每个指定的资源：

- 在相应的目录中查找文件（例如，核心库在 `system/libraries/`，自定义库在 `application/libraries/`）。
- 实例化类（对于库/模型）或包含文件（对于辅助函数/配置）。
- 使它们全局可用（例如，在控制器中可以通过 `$this->library_name` 访问库）。

如果找不到资源，可能会导致错误——请确保路径和名称正确。如果需要，您稍后可以使用诸如 `$this->load->library('session')` 之类的方法手动加载其他项目。

### 文件中各部分的详细说明

以下是基于所提供代码的逐节说明。我包含了每个数组的作用、使用说明和示例。默认值大多为空，以保持框架的轻量级。

#### 1. 自动加载包

```php
$autoload['packages'] = array();
```

- **目的**：加载第三方包。这些通常是可重用的库/辅助函数/模型集合，通常位于子目录中，如 `APPPATH.'third_party'` 或自定义路径。
- **工作原理**：将指定的目录添加到包路径数组中。然后，CodeIgniter 将在这些路径中搜索带有 `MY_` 前缀的类并根据需要加载它们。
- **用法**：示例：`$autoload['packages'] = array(APPPATH.'third_party', '/usr/local/shared');` – 替换诸如 `$this->load->add_package_path()` 之类的调用中的路径。
- **注意**：默认为空；对于在不更改核心的情况下扩展框架非常有用。

#### 2. 自动加载库

```php
$autoload['libraries'] = array();
```

- **目的**：加载类库（例如，会话管理、电子邮件等）。
- **工作原理**：从 `system/libraries/` 或 `application/libraries/` 加载并实例化类。常见的包括 'database'、'session'、'email'。
- **用法**：示例：`$autoload['libraries'] = array('database', 'email', 'session');` 或使用别名，如 `$autoload['libraries'] = array('user_agent' => 'ua');`（允许使用 `$this->ua` 而不是 `$this->user_agent`）。
- **注意**：数据库是特殊的——加载它会自动连接。避免过度自动加载以最小化内存使用。

#### 3. 自动加载驱动程序

```php
$autoload['drivers'] = array();
```

- **目的**：加载基于驱动程序的库，这些库提供多个可互换的实现（例如，缓存、图像处理）。
- **工作原理**：`CI_Driver_Library` 的子类。加载驱动程序类及其子目录。
- **用法**：示例：`$autoload['drivers'] = array('cache');` – 加载 `system/libraries/Cache/drivers/cache_apc_driver.php` 或类似文件。
- **注意**：驱动程序是模块化的；您在运行时指定要使用的驱动程序（例如，`$this->cache->apc->save()`）。

#### 4. 自动加载辅助函数文件

```php
$autoload['helper'] = array('base');
```

- **目的**：加载辅助函数（PHP 函数库，例如用于 URL、文件、表单）。
- **工作原理**：包含文件（例如，`application/helpers/base_helper.php`），使其函数全局可用。
- **用法**：示例：`$autoload['helper'] = array('url', 'file');` – 允许在不手动加载辅助函数的情况下调用 `site_url()`。
- **注意**：在您的文件中，'base' 是自动加载的——请确保 `base_helper.php` 存在。

#### 5. 自动加载配置文件

```php
$autoload['config'] = array();
```

- **目的**：加载默认 `config.php` 之外的自定义配置文件。
- **工作原理**：将额外的配置（例如，`application/config/custom.php`）合并到全局配置数组中。
- **用法**：示例：`$autoload['config'] = array('custom', 'seo');` – 将 `custom.php` 和 `seo.php` 作为配置加载。
- **注意**：如果使用默认配置，请留空；对于站点特定设置非常有用。

#### 6. 自动加载语言文件

```php
$autoload['language'] = array();
```

- **目的**：加载用于国际化的语言数组。
- **工作原理**：从 `application/language/english/`（或当前语言）加载文件，例如 `form_lang.php`。
- **用法**：示例：`$autoload['language'] = array('form', 'calendar');` – 加载 `form_lang.php`（不带 '_lang' 后缀）。
- **注意**：语言是根据配置自动检测的；很少需要全局加载。

#### 7. 自动加载模型

```php
$autoload['model'] = array('BaseDao');
```

- **目的**：加载用于数据库交互的模型类。
- **工作原理**：从 `application/models/` 加载并实例化，例如 `BaseDao.php`。
- **用法**：示例：`$autoload['model'] = array('user_model', 'BaseDao' => 'base');` – 允许使用 `$this->base` 作为别名。
- **注意**：在您的文件中，'BaseDao' 是自动加载的——请确保它是一个有效的模型类。

### 使用技巧

- **编辑文件**：修改 `autoload.php` 以添加项目。更改后进行测试以确保没有冲突。
- **性能**：自动加载所有内容可能会减慢请求速度；仅加载全局需要的内容。
- **手动加载**：如果某些内容未自动加载，请在控制器中使用 `$this->load->library('name');` 或类似方法。
- **版本说明**：这适用于 CodeIgniter 2.x/3.x。在 4.x 中，自动加载已转向基于 Composer（命名空间），但在旧版本中仍使用此类配置文件。

如果您对添加项目或排查错误有具体问题，请提供更多详细信息！
