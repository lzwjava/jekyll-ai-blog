---
audio: false
generated: true
lang: zh
layout: post
title: 在PHP中使用ffmpeg
translated: true
type: note
---

### 核心要点

- 要使用 "php-ffmpeg/php-ffmpeg" 版本 ~0.5，似乎需要先在系统上安装 FFMpeg，然后使用 Composer 安装该 PHP 库。
- 研究表明，需要包含自动加载文件并创建 `FFMpeg\FFMpeg` 实例以进行媒体操作，如果需要，可以指定二进制路径选项。
- 证据倾向于使用诸如 `open()`、`save()` 和 `frame()` 等方法进行基本操作，但由于可能存在版本特定差异，请查阅 GitHub 文档以获取完整详细信息。

---

### 安装

首先，确保系统上已安装 FFMpeg：

- 在 Ubuntu 上，使用 `sudo apt-get install ffmpeg`。
- 在 macOS 上，使用 `brew install ffmpeg`。
- 在 Windows 上，从[此网站](https://www.gyan.dev/ffmpeg/builds/)下载并按照说明操作。

接下来，通过 Composer 安装 php-FFMpeg 库：

```
composer require php-FFMpeg/php-FFMpeg:~0.5
```

### 设置与使用

在您的 PHP 脚本中包含自动加载文件：

```php
require_once 'vendor/autoload.php';
```

创建 `FFMpeg\FFMpeg` 的实例，如果 FFMpeg 二进制文件不在系统 PATH 中，可以选择指定路径：

```php
use FFMpeg\FFMpeg;
$ff = FFMpeg::create(array(
    'binary' => '/path/to/FFMpeg',
    'ffprobe' => '/path/to/FFprobe'
));
```

打开媒体文件并执行操作，例如：

- 转码：`$video->save('output.mp4', new FFMpeg\Format\Video\X264());`
- 提取帧：`$frame = $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5)); $frame->save('frame.jpg');`
- 剪辑：`$clip = $video->clip(FFMpeg\Coordinate\TimeCode::fromSeconds(10), FFMpeg\Coordinate\TimeCode::fromSeconds(20)); $clip->save('clip.mp4');`

更多详细信息，请参阅该库在 [GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg) 上的文档。

---

### 调研笔记：使用 php-FFMpeg/php-FFMpeg 版本 ~0.5 的全面指南

本笔记基于现有信息，深入探讨了如何使用 "php-FFMpeg/php-FFMpeg" 库，特别是大约 0.5 版本。它在直接回答的基础上扩展，包含了研究中的所有相关细节，确保寻求实现此 PHP 库进行媒体操作的用户能够透彻理解。

#### 背景与上下文

"php-FFMpeg/php-FFMpeg" 库是 FFMpeg 二进制文件的 PHP 包装器，支持以面向对象的方式操作视频和音频文件。它支持转码、帧提取、剪辑等任务，对于从事媒体相关应用程序开发的开发人员来说非常有价值。版本规范 "~0.5" 表示任何大于或等于 0.5 且小于 1.0 的版本，表明其与旧版 PHP 兼容，很可能位于存储库的 0.x 分支中。

考虑到当前日期是 2025 年 3 月 3 日，以及该库的演变，版本 0.5 可能属于遗留支持范畴，主分支现在要求 PHP 8.0 或更高版本。本笔记假设用户在此版本的约束下工作，并承认与新版本相比在功能上可能存在差异。

#### 安装过程

首先，必须在系统上安装 FFMpeg，因为该库依赖其二进制文件进行操作。安装方法因操作系统而异：

- **Ubuntu**：使用命令 `sudo apt-get install ffmpeg` 通过包管理器安装。
- **macOS**：使用 Homebrew 和 `brew install ffmpeg` 进行简单安装。
- **Windows**：从[此网站](https://www.gyan.dev/ffmpeg/builds/)下载 FFMpeg 二进制文件，并按照提供的说明操作，确保可执行文件可在系统 PATH 中访问或手动指定。

安装 FFMpeg 后，通过 PHP 包管理器 Composer 安装 php-FFMpeg 库。命令 `composer require php-FFMpeg/php-FFMpeg:~0.5` 确保获取正确的版本。此过程在项目中创建一个 `vendor` 目录，用于存放该库及其依赖项，Composer 管理自动加载以实现无缝集成。

#### 设置与初始化

安装后，在您的 PHP 脚本中包含自动加载文件以启用对该库类的访问：

```php
require_once 'vendor/autoload.php';
```

创建 `FFMpeg\FFMpeg` 的实例以开始使用该库。创建方法允许进行配置，如果 FFMpeg 二进制文件不在系统 PATH 中，这一点尤其重要：

```php
use FFMpeg\FFMpeg;
$ff = FFMpeg::create(array(
    'timeout' => 0,
    'thread_count' => 12,
    'binary' => '/path/to/your/own/FFMpeg',
    'ffprobe' => '/path/to/your/own/FFprobe'
));
```

此配置支持设置超时、线程数和显式二进制路径，增强了不同系统设置的灵活性。默认设置会在 PATH 中查找二进制文件，但手动指定可确保兼容性，尤其是在自定义环境中。

#### 核心用法与操作

该库为媒体操作提供了一个流畅的、面向对象的接口。首先打开一个媒体文件：

```php
$video = $ff->open('input.mp4');
```

这支持本地文件系统路径、HTTP 资源以及 FFMpeg 支持的其他协议，支持的格式列表可通过 `ffmpeg -protocols` 命令获取。

##### 转码

转码涉及将媒体转换为不同的格式。使用带有格式实例的 `save` 方法：

```php
$format = new FFMpeg\Format\Video\X264();
$video->save('output.mp4', $format);
```

`X264` 格式是一个例子；该库支持各种视频和音频格式，可通过 `FFMpeg\Format\FormatInterface` 实现，特定接口如 `VideoInterface` 和 `AudioInterface` 分别用于相应的媒体类型。

##### 帧提取

提取帧对于缩略图或分析非常有用。以下代码在 5 秒处提取一帧：

```php
$frame = $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5));
$frame->save('frame.jpg');
```

`TimeCode` 类是 `FFMpeg\Coordinate` 的一部分，可确保精确计时，并具有在图像提取中提高精度的选项。

##### 剪辑

要剪辑视频的一部分，请指定开始和结束时间：

```php
$clip = $video->clip(FFMpeg\Coordinate\TimeCode::fromSeconds(10), FFMpeg\Coordinate\TimeCode::fromSeconds(20));
$clip->save('clip.mp4');
```

这将创建一个新的视频片段，保持原始质量和格式，并能够在需要时应用其他过滤器。

#### 高级功能与注意事项

该库支持其他功能，如文档中所述：

- **音频操作**：与视频类似，可以使用 `FFMpeg\Media\Audio::save` 对音频进行转码，应用过滤器、添加元数据和重采样。
- **GIF 创建**：可以使用 `FFMpeg\Media\Gif::save` 保存动画 GIF，并可选择持续时间参数。
- **拼接**：使用 `FFMpeg\Media\Concatenate::saveFromSameCodecs` 合并具有相同编解码器的多个媒体文件，或使用 `saveFromDifferentCodecs` 合并具有不同编解码器的文件，进一步阅读资源请参阅[此链接](https://trac.ffmpeg.org/wiki/Concatenate)、[此链接](https://ffmpeg.org/ffmpeg-formats.html#concat-1) 和 [此链接](https://ffmpeg.org/ffmpeg.html#Stream-copy)。
- **高级媒体处理**：支持使用 `-filter_complex` 进行多个输入/输出，适用于复杂的过滤和映射，并具有内置过滤器支持。
- **元数据提取**：使用 `FFMpeg\FFProbe::create` 获取元数据，使用 `FFMpeg\FFProbe::isValid` 验证文件（自 v0.10.0 起可用，注意版本 0.5 可能缺少此功能）。

坐标，例如 `FFMpeg\Coordinate\AspectRatio`、`Dimension`、`FrameRate`、`Point`（自 v0.10.0 起动态）和 `TimeCode`，提供了对媒体属性的精确控制，尽管某些功能（如动态点）在版本 0.5 中可能不可用。

#### 版本特定说明

鉴于 "~0.5" 规范，该库很可能与支持旧版 PHP 的 0.x 分支保持一致。GitHub 存储库表明主分支需要 PHP 8.0 或更高版本，0.x 用于遗留支持。然而，在发布版本中未明确找到确切的 0.5 版本详细信息，这表明它可能是提交历史或分支提交的一部分。用户应验证兼容性，因为某些新功能（例如某些坐标类型，如动态点）可能需要 0.5 以上的版本。

#### 文档与进一步阅读

虽然 Read the Docs 页面 ([Read the Docs](https://FFMpeg-PHP.readthedocs.io/en/latest/)) 显示为空，但 GitHub 存储库 ([GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg)) 的 README 中包含全面的文档，涵盖了 API 用法、格式和示例。鉴于此遗留版本缺乏特定的在线文档，这是版本 0.5 的主要资源。

#### 表格：关键操作与方法总结

| 操作               | 方法示例                                      | 描述                                      |
|--------------------|---------------------------------------------|------------------------------------------|
| 打开媒体文件       | `$ff->open('input.mp4')`                   | 加载媒体文件以进行操作                   |
| 视频转码           | `$video->save('output.mp4', new X264())`   | 转换为指定格式                           |
| 提取帧             | `$video->frame(TimeCode::fromSeconds(5))->save('frame.jpg')` | 在指定时间提取帧，保存为图像             |
| 视频剪辑           | `$video->clip(TimeCode::fromSeconds(10), TimeCode::fromSeconds(20))->save('clip.mp4')` | 在时间点之间创建剪辑，保存为新文件       |
| 配置实例           | `FFMpeg::create(array('binary' => '/path/to/FFMpeg'))` | 设置自定义二进制路径和选项               |

此表格封装了核心功能，有助于用户在实现该库时快速参考。

#### 意外细节：遗留版本的影响

一个意想不到的方面是版本 0.5 的潜在限制，因为它位于支持旧版 PHP 的 0.x 分支中。这可能会限制对现代功能的访问，例如在 v0.10.0 中引入的动态坐标点，要求用户检查分支提交以获取确切功能，这增加了在新版本中不立即显现的复杂性。

#### 结论

使用 "php-FFMpeg/php-FFMpeg" 版本 ~0.5 涉及安装 FFMpeg、通过 Composer 进行设置以及利用面向对象的 API 执行媒体任务。虽然转码和帧提取等基本操作很简单，但版本特定差异可能需要查阅 [GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg) 上的 0.x 分支文档。这种全面的方法确保用户可以有效地利用该库，同时承认其强大功能和潜在的遗留约束。

---

### 关键引用

- [FFMpeg PHP Object Oriented Library Packagist](https://packagist.org/products/php-FFMpeg/php-FFMpeg)
- [PHP-FFMpeg GitHub Repository Documentation](https://github.com/PHP-FFMpeg/PHP-FFMpeg)
- [FFMpeg PHP Read the Docs Documentation](https://FFMpeg-PHP.readthedocs.io/en/latest/)
- [FFMpeg Download and Builds Website](https://www.gyan.dev/ffmpeg/builds/)
- [FFMpeg Concatenation Wiki Page](https://trac.ffmpeg.org/wiki/Concatenate)
- [FFMpeg Formats Documentation Page](https://ffmpeg.org/ffmpeg-formats.html#concat-1)
- [FFMpeg Command Line Tool Documentation](https://ffmpeg.org/ffmpeg.html#Stream-copy)
