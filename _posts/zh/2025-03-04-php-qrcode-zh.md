---
audio: false
generated: true
lang: zh
layout: post
title: PHP二维码生成工具
translated: true
type: note
---

### 核心要点

- 要使用"endroid/qr-code" 2.2.2版本，需要通过Composer安装并确保启用GD扩展
- 研究表明可以使用Builder类生成二维码，设置数据、尺寸和写入器等参数，然后保存或输出结果
- 证据表明该库支持PNG、SVG等格式，并提供Logo和标签选项，但需针对2.2.2版本进行验证

### 安装方法

首先使用Composer命令安装该库：

```
composer require endroid/qr-code:2.2.2
```

请确保PHP环境已启用GD扩展，这是图像生成的必要条件。

### 使用示例

以下是使用Builder类的基础示例，该示例很可能兼容2.2.2版本：

```php
use Endroid\QrCode\Builder\Builder;
use Endroid\QrCode\Encoding\Encoding;
use Endroid\QrCode\ErrorCorrectionLevel\ErrorCorrectionLevelHigh;
use Endroid\QrCode\Writer\PngWriter;

$url = 'https://example.com';
$qrCode = Builder::create()
    ->writer(new PngWriter())
    ->data($url)
    ->encoding(new Encoding('ISO-8859-1'))
    ->errorCorrectionLevel(new ErrorCorrectionLevelHigh())
    ->build();
$qrCode->saveToFile('qr_code.png');
```

此代码为URL创建二维码并保存为PNG文件。也可将其输出为数据URI用于网页显示。

### 补充说明

该库支持多种写入器（如PNG、SVG），并允许自定义选项如添加Logo或标签。但由于2.2.2版本较旧，当前文档中的某些功能（如高级Logo选项）可能不可用，建议查阅该特定版本的[GitHub文档](https://github.com/endroid/qr-code)。

---

### 技术指南：详细使用"endroid/qr-code" 2.2.2版本指南

本指南全面介绍了在PHP应用中使用"endroid/qr-code"库2.2.2版本生成二维码的方法。基于调研结果扩展了直接答案，包含所有相关细节，确保开发者（特别是库的新用户）能透彻理解。内容结构仿照专业文章格式，配有清晰表格和内联URL参考。

#### 引言

"endroid/qr-code"库是用于生成二维码的PHP工具，广泛应用于产品追踪、文档管理和营销等领域。查询中指定的2.2.2版本是较旧的发行版，虽然该库在[Packagist](https://packagist.org/packages/endroid/qr-code)上标记为已弃用，但仍可用于基础二维码生成。本指南重点说明安装和使用方法，确保与2.2.2版本的兼容性，同时指出与新版本的潜在差异。

#### 安装流程

首先必须通过PHP包管理器Composer安装该库。命令如下：

```
composer require endroid/qr-code:2.2.2
```

这将确保获取精确的2.2.2版本。关键要求是启用PHP的GD扩展，该扩展必须启用并配置妥当，因为它是图像生成的基础。若无此扩展，库将无法生成可视化二维码。

| 步骤                  | 详情                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| 安装命令              | `composer require endroid/qr-code:2.2.2`                                |
| PHP要求               | 确保GD扩展已启用（可通过`phpinfo()`验证）                               |

研究表明，该库的GitHub仓库([GitHub](https://github.com/endroid/qr-code))和[Packagist](https://packagist.org/packages/endroid/qr-code)页面均确认此安装方法，但未找到2.2.2版本的特定文档，建议参考通用使用模式。

#### 使用详情

该库提供两种主要二维码生成方法：使用Builder类或直接使用QrCode类。鉴于查询聚焦于使用方式，推荐采用Builder方式因其简洁性，但为完整性此处同时说明两种方法。

##### 使用Builder类

Builder类提供流畅接口用于配置二维码。基于最新文档示例，基础实现如下：

```php
use Endroid\QrCode\Builder\Builder;
use Endroid\QrCode\Encoding\Encoding;
use Endroid\QrCode\ErrorCorrectionLevel\ErrorCorrectionLevelHigh;
use Endroid\QrCode\Writer\PngWriter;

$url = 'https://example.com';
$qrCode = Builder::create()
    ->writer(new PngWriter())
    ->data($url)
    ->encoding(new Encoding('ISO-8859-1'))
    ->errorCorrectionLevel(new ErrorCorrectionLevelHigh())
    ->build();
$qrCode->saveToFile('qr_code.png');
```

此代码为URL创建二维码，使用PNG格式，采用ISO-8859-1编码以提升扫描器兼容性，并设置高纠错级别。也可输出为数据URI：

```php
$qrCodeDataUri = $qrCode->getDataUri();
```

这在HTML嵌入时很有用，例如：`<img src="<?php echo $qrCodeDataUri; ?>"`。

但由于2.2.2版本较旧，某些类名（如`ErrorCorrectionLevelHigh`）可能命名不同（旧版本中可能是`ErrorCorrectionLevel::HIGH`）。Stack Overflow的调研([Stack Overflow](https://stackoverflow.com/questions/40777377/endroid-qr-code))表明旧版本使用类似`setErrorCorrection('high')`的方法，因此请验证2.2.2版本的API。

##### 直接使用QrCode类

如需更多控制，可直接使用QrCode类，示例如下：

```php
use Endroid\QrCode\QrCode;
use Endroid\QrCode\Writer\PngWriter;

$qrCode = new QrCode('Life is too short to be generating QR codes');
$qrCode->setSize(300);
$qrCode->setMargin(10);
$writer = new PngWriter();
$result = $writer->write($qrCode);
$result->saveToFile('qrcode.png');
```

此方法更详细但允许微调，例如设置前景色和背景色，这可能与2.2.2版本相关。同样需要检查方法的可用性。

#### 配置选项

该库支持多种写入器以适应不同输出格式，详情见下表（基于当前文档，但需验证2.2.2版本兼容性）：

| 写入器类              | 格式     | 备注                                                                 |
|-----------------------|----------|----------------------------------------------------------------------|
| PngWriter             | PNG      | 可配置压缩级别，默认-1                                               |
| SvgWriter             | SVG      | 适用于矢量图形，无压缩选项                                           |
| WebPWriter            | WebP     | 质量0-100，默认80，适合网页使用                                      |
| PdfWriter             | PDF      | 单位毫米，默认值，适合打印                                           |

编码选项包括UTF-8（默认）和ISO-8859-1，后者推荐用于提升条码扫描器兼容性。圆形块尺寸模式（边距、放大、缩小、无）可提升可读性，但其在2.2.2版本中的可用性需确认。

#### 高级功能与注意事项

对于高级用法（如嵌入Logo），Builder类支持`logoPath()`和`logoResizeToWidth()`等方法（参考Medium文章([Medium](https://johnrix.medium.com/creating-qr-codes-with-embedded-images-in-php-d926e4546b31))）。但这些可能是2.2.2之后新增的功能，请测试兼容性。生成二维码的验证功能可用但影响性能且默认禁用，此细节来自[GitHub](https://github.com/endroid/qr-code)。

鉴于该库在[Packagist](https://packagist.org/packages/endroid/qr-code)的弃用说明，需注意潜在的安全或维护问题，但对于基础使用仍可行。Symfony用户可使用配套包([GitHub](https://github.com/endroid/qr-code-bundle))，但这超出通用PHP使用范围。

#### 版本特定说明

调研显示没有2.2.2版本的直接文档，GitHub标签也未列出该版本，暗示它可能是旧发行版或存在拼写错误。当前仓库显示版本达6.0.0，且[Packagist](https://packagist.org/packages/endroid/qr-code)将其标记为弃用并推荐endroid/qr-code（这与原包名相同令人困惑）。这表明可能存在重命名或版本管理问题，建议用户锁定依赖关系并测试升级。

#### 结论

使用"endroid/qr-code" 2.2.2版本需通过Composer安装，确保GD扩展启用，并使用Builder或QrCode类生成二维码。虽然示例基于当前文档，但需验证2.2.2版本的API差异，特别是高级功能。更多详情请查阅该库的GitHub页面和相关Stack Overflow讨论。

#### 关键引用

- [二维码生成器GitHub仓库](https://github.com/endroid/qr-code)
- [endroid/qr-code Packagist页面](https://packagist.org/packages/endroid/qr-code)
- [创建带嵌入图像二维码的Medium文章](https://johnrix.medium.com/creating-qr-codes-with-embedded-images-in-php-d926e4546b31)
- [Endroid二维码Stack Overflow讨论](https://stackoverflow.com/questions/40777377/endroid-qr-code)
