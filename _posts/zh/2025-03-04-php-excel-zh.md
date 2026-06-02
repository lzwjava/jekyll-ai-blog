---
audio: false
generated: true
lang: zh
layout: post
title: PHPExcel库
translated: true
type: note
---

### 核心要点

- 要使用 "phpoffice/phpexcel": "^1.8"，需要通过 Composer 安装并使用 PHP 代码读写 Excel 文件。
- 研究表明该库已弃用，新项目建议使用 PhpSpreadsheet。
- 证据表明需要安装 mbstring、XML 和 XMLWriter 等 PHP 扩展。

### 安装方法

在 `composer.json` 文件中添加 `"phpoffice/phpexcel": "^1.8"` 并运行 `composer install`。这将下载该库，这是在 PHP 中操作 Excel 文件的基础。

### 基础用法

写入 Excel 文件：

- 通过 `require 'vendor/autoload.php';` 引入库
- 创建 PHPExcel 对象：`$objPHPExcel = new PHPExcel();`
- 设置单元格值，例如：`$sheet->setCellValue('A1', 'value');`
- 使用写入器保存文件，如：`$writer = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');` 后接 `$writer->save('filename.xlsx');`

读取 Excel 文件：

- 通过 `$objPHPExcel = PHPExcel_IOFactory::load('filename.xlsx');` 加载文件
- 访问单元格值，例如：`$cellValue = $sheet->getCell('A1')->getValue();`

### 意外发现

PHPExcel 支持多种文件格式（如 .xls 和 .xlsx），并在读取时能自动检测文件类型，这简化了使用流程。

---

### 调研笔记：全面指南 "phpoffice/phpexcel": "^1.8"

本笔记详细探讨了 PHPExcel 库的使用方法，特别是 Composer 依赖 "phpoffice/phpexcel": "^1.8" 指定的 1.8 或更高版本。考虑到该库已被弃用，本指南也强调了现代替代方案的考量，确保无论是初学者还是高级用户都能获得全面理解。内容结构涵盖安装、用法、依赖项和附加背景信息，确保包含研究中的所有相关细节。

#### 背景与语境

PHPExcel 是专为读写电子表格文件（特别是 .xls 和 .xlsx 等 Excel 格式）设计的 PHP 库。版本规范 "^1.8" 表示语义版本范围，即从 1.8 到但不包括 2.0 的所有版本。考虑到该库的历史，最新版本为 2015 年发布的 1.8.1。但研究表明 PHPExcel 已于 2017 年正式弃用，2019 年归档，建议迁移到其继任者 PhpSpreadsheet，原因包括缺乏维护和潜在安全问题。这一背景对用户至关重要，建议新项目谨慎使用，但本指南将按需求重点介绍指定版本的使用。

该库功能包括创建、读取和操作 Excel 文件，支持 Excel 以外的格式如 CSV 和 HTML。它曾是 PHPOffice 项目的一部分，该项目现已将重点转向具有改进功能和 PHP 标准兼容性的 PhpSpreadsheet。考虑到当前日期为 2025 年 3 月 3 日，以及该库的归档状态，用户应注意其局限性，特别是在新版 PHP 和安全更新方面。

#### 安装流程

要安装 "phpoffice/phpexcel": "^1.8"，需使用 PHP 依赖管理工具 Composer：

- 在 `composer.json` 文件的 "require" 部分添加依赖：`"phpoffice/phpexcel": "^1.8"`
- 在项目目录中运行命令 `composer install`。该命令将下载库并更新 `vendor` 目录中的必要文件

Composer 中的插入符（^）表示法遵循语义版本控制，确保安装 1.8、1.8.1 或任何补丁更新，但不会安装破坏兼容性的版本（即不包含 2.0 或更高版本）。鉴于该库最后发布版本是 2015 年的 1.8.1，通常解析为版本 1.8.1。

研究确认 Packagist 上的 phpoffice/phpexcel 页面已标记为弃用，建议改用 phpoffice/phpspreadsheet，但仍可按用户要求安装使用。

#### 基础用法：写入 Excel

安装完成后，使用 PHPExcel 需要引入自动加载文件进行类加载，然后使用其类进行电子表格操作：

- **引入自动加载文件：** 在 PHP 脚本开头添加 `require 'vendor/autoload.php';`。这行代码确保所有通过 Composer 安装的库（包括 PHPExcel）都能自动加载，利用该库 2015 年结构的 PSR-0 自动加载

- **创建新 PHPExcel 对象：** 使用 `$objPHPExcel = new PHPExcel();` 初始化新电子表格。该对象代表整个工作簿，支持多工作表和各种属性

- **操作工作表：** 使用 `$sheet = $objPHPExcel->getSheet(0);` 访问活动工作表（第一个工作表），或使用 `$sheet = $objPHPExcel->createSheet();` 创建新工作表。工作表从零开始索引，因此 `getSheet(0)` 指向第一个工作表

- **设置单元格值：** 使用 `setCellValue` 方法填充单元格，例如 `$sheet->setCellValue('A1', 'Hello');`。该方法接受单元格引用（如 'A1'）和要插入的值，值可以是文本、数字或公式

- **保存文件：** 要保存文件，需为所需格式创建写入器。对于 Excel 2007 及以上版本（.xlsx），使用 `$writer = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');`，然后使用 `$writer->save('filename.xlsx');` 保存。其他格式包括用于 .xls（Excel 95）的 'Excel5' 或用于逗号分隔值的 'CSV'

写入操作示例脚本：

```php
require 'vendor/autoload.php';
$objPHPExcel = new PHPExcel();
$sheet = $objPHPExcel->getSheet(0);
$sheet->setCellValue('A1', 'Hello');
$sheet->setCellValue('B1', 'World');
$writer = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');
$writer->save('hello_world.xlsx');
```

这将创建一个简单的 Excel 文件，A1 单元格为 "Hello"，B1 单元格为 "World"。

#### 基础用法：读取 Excel

读取 Excel 文件模式类似，但从加载文件开始：

- **加载文件：** 使用 `$objPHPExcel = PHPExcel_IOFactory::load('filename.xlsx');` 加载现有 Excel 文件。IOFactory 通常能自动检测文件类型，但也可以指定读取器，例如显式指定类型：`$objReader = PHPExcel_IOFactory::createReader('Excel2007'); $objPHPExcel = $objReader->load('filename.xlsx');`

- **访问工作表和单元格：** 加载后，如前所述访问工作表，例如 `$sheet = $objPHPExcel->getSheet(0);`。使用 `$cellValue = $sheet->getCell('A1')->getValue();` 获取单元格值，返回指定单元格的内容

读取示例：

```php
require 'vendor/autoload.php';
$objPHPExcel = PHPExcel_IOFactory::load('hello_world.xlsx');
$sheet = $objPHPExcel->getSheet(0);
$cellValue = $sheet->getCell('A1')->getValue();
echo $cellValue; // 输出 "Hello"
```

这将读取 A1 的值，演示基本检索操作。

#### 依赖项与要求

PHPExcel 有特定的 PHP 要求和运行所需的扩展：

- **PHP 版本：** 根据 Packagist 元数据，需要 PHP 5.2 或 7.0 及以上版本。考虑到当前日期 2025 年 3 月 3 日，大多数现代 PHP 安装应满足此要求，但旧版设置可能需要更新
- **扩展：** 该库依赖 `ext-mbstring`、`ext-XML` 和 `ext-XMLWriter`，必须在 PHP 配置中启用。这些扩展分别处理字符串编码、XML 解析和 XML 写入，对 Excel 文件操作至关重要

用户应使用 `phpinfo()` 或检查 `php.ini` 文件来验证这些扩展是否启用，确保不会出现兼容性问题。

#### 附加功能与格式

除了基本读写功能，PHPExcel 还支持各种文件格式，这对只熟悉 Excel 的用户来说是个意外发现：

- 通过 'Excel2007' 写入器/读取器支持 Excel 2007（.xlsx）
- 通过 'Excel5' 支持 Excel 95（.xls）
- 通过 'CSV' 支持 CSV 文件
- 通过 'HTML' 支持 HTML

保存时指定写入器类型；读取时 IOFactory 通常自动检测，但为可靠性可使用显式读取器。例如保存为 .xls：

```php
$writer = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
$writer->save('filename.xls');
```

这种灵活性对遗留系统或特定格式需求很有用，但用户应注意特定格式的限制，特别是旧版 Excel。

#### 弃用与迁移建议

关键点是 PHPExcel 已被弃用。研究表明它于 2019 年归档，最后更新于 2015 年，且不再维护。这引发了安全漏洞和与 PHP 7.0 以上版本（特别是 PHP 8.x 等现代标准）兼容性的担忧。GitHub 仓库和 Packagist 页面都建议迁移到 PhpSpreadsheet，后者提供命名空间、PSR 兼容性和积极开发。

对用户而言这意味着：

- 对使用 PHPExcel 1.8 的现有项目，需谨慎继续，确保进行安全性和兼容性测试
- 对新项目，强烈建议考虑 PhpSpreadsheet，并提供迁移工具（如 PhpSpreadsheet 文档中所述）

考虑到当前日期，这一建议尤其重要，可确保用户与现代、受支持的库保持一致。

#### 文档与深入学习

要深入探索，PHPExcel 的官方文档可在其 GitHub 仓库的 Documentation 文件夹中找到，但访问可能需要下载开发者文档 DOC 等文件。网上教程（如 SitePoint 上的教程）提供实用示例，涵盖图表和格式设置，扩展了基础用法。Stack Overflow 讨论串也提供社区见解，但鉴于该库状态，应注意过时答案。

#### 对比表格：PHPExcel vs. PhpSpreadsheet

为辅助决策，以下是基于研究的重点差异对比表：

| 功能特性             | PHPExcel (1.8)                 | PhpSpreadsheet               |
|----------------------|--------------------------------|------------------------------|
| 最后更新             | 2015年                         | 持续维护（截至2025年）       |
| 命名空间             | 无，根命名空间                 | 有，PSR-4兼容                |
| 维护状态             | 已弃用，2019年归档             | 积极维护                     |
| PHP 版本支持         | 最高支持 7.0                   | PHP 7.4+                     |
| 文件格式支持         | Excel、CSV、HTML 等            | 增强支持，包括 ODS、PDF      |
| 性能表现             | 中等，内存消耗大               | 经过优化，可扩展性强         |

该表强调现代需求应向 PhpSpreadsheet 转移，但 PHPExcel 在遗留场景中仍可运行。

#### 总结

使用 "phpoffice/phpexcel": "^1.8" 需要通过 Composer 安装，利用其类进行 Excel 操作，并确保满足 PHP 扩展要求。虽然功能正常，但其弃用状态需要谨慎对待，新项目建议使用 PhpSpreadsheet。本指南提供全面的入门指导，包含示例、依赖项和附加资源供用户深入探索。

### 主要引用

- [Packagist phpoffice/phpexcel 页面含安装细节](https://packagist.org/packages/phpoffice/phpexcel)
- [SitePoint 使用 PHPExcel 生成 Excel 文件和图表教程](https://www.sitepoint.com/generate-excel-files-charts-phpexcel/)
- [PHPExcel GitHub 仓库归档状态](https://github.com/PHPOffice/PHPExcel)
- [从 PHPExcel 迁移到 PhpSpreadsheet 指南](https://phpspreadsheet.readthedocs.io/en/latest/topics/migration-from-PHPExcel/)
