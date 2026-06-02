---
audio: false
generated: true
lang: en
layout: post
title: PHP Tool for Generating QR Codes
translated: false
type: note
---

### Key Points

- It seems likely that to use "endroid/qr-code" version 2.2.2, you need to install it via Composer and ensure the GD extension is enabled.
- Research suggests you can generate QR codes using the Builder class, setting parameters like data, size, and writer, then save or output the result.
- The evidence leans toward the library supporting PNG, SVG, and other formats, with options for logos and labels, but verify for version 2.2.2.

### Installation

First, install the library using Composer with the command:

```
composer require endroid/qr-code:2.2.2
```

Ensure your PHP setup has the GD extension enabled, as it's required for image generation.

### Usage Example

Here’s a basic example using the Builder class, which is likely compatible with version 2.2.2:

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

This creates a QR code for a URL and saves it as a PNG file. You can also output it as a data URI for web display.

### Additional Notes

The library supports various writers (e.g., PNG, SVG) and allows customization like adding logos or labels. However, given version 2.2.2 is older, some features in current documentation (like advanced logo options) might not be available, so check the documentation for that specific version on [GitHub](https://github.com/endroid/qr-code).

---

### Survey Note: Detailed Guide on Using "endroid/qr-code" Version 2.2.2

This note provides a comprehensive guide on using the "endroid/qr-code" library, version 2.2.2, for generating QR codes in PHP applications. It expands on the direct answer by including all relevant details from the research, ensuring a thorough understanding for developers, especially those new to the library. The content is structured to mimic a professional article, with tables for clarity and inline URLs for further reference.

#### Introduction

The "endroid/qr-code" library is a PHP tool for generating QR codes, widely used for applications like product tracking, document management, and marketing. Version 2.2.2, specified in the query, is an older release, and while the library is noted as abandoned on [Packagist](https://packagist.org/packages/endroid/qr-code), it remains functional for basic QR code generation. This guide outlines installation and usage, with a focus on ensuring compatibility with version 2.2.2, acknowledging potential differences from newer versions.

#### Installation Process

To begin, you must install the library via Composer, the PHP package manager. The command is:

```
composer require endroid/qr-code:2.2.2
```

This ensures you get the exact version 2.2.2. A critical requirement is the GD extension for PHP, which must be enabled and configured, as it is essential for image generation. Without it, the library cannot produce visual QR codes.

| Step                  | Details                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| Install Command       | `composer require endroid/qr-code:2.2.2`                                |
| PHP Requirement       | Ensure GD extension is enabled (check `phpinfo()` for confirmation)     |

Research indicates that the library's GitHub repository ([GitHub](https://github.com/endroid/qr-code)) and [Packagist](https://packagist.org/packages/endroid/qr-code) pages confirm this installation method, with no specific version 2.2.2 documentation found, suggesting reliance on general usage patterns.

#### Usage Details

The library offers two primary methods for QR code generation: using the Builder class or directly with the QrCode class. Given the query's focus on usage, the Builder approach is recommended for its simplicity, though both are detailed here for completeness.

##### Using the Builder Class

The Builder class provides a fluent interface for configuring QR codes. Based on examples from recent documentation, a basic implementation is:

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

This code creates a QR code for the URL, using PNG format, with ISO-8859-1 encoding for better scanner compatibility and high error correction. You can also output it as a data URI:

```php
$qrCodeDataUri = $qrCode->getDataUri();
```

This is useful for embedding in HTML, e.g., `<img src="<?php echo $qrCodeDataUri; ?>">`.

However, given version 2.2.2's age, some classes like `ErrorCorrectionLevelHigh` might be named differently (e.g., `ErrorCorrectionLevel::HIGH` in older versions). Research from Stack Overflow posts ([Stack Overflow](https://stackoverflow.com/questions/40777377/endroid-qr-code)) suggests older versions used methods like `setErrorCorrection('high')`, so verify the API for 2.2.2.

##### Using the QrCode Class Directly

For more control, you can use the QrCode class, as seen in examples:

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

This method is more verbose but allows fine-tuning, such as setting foreground and background colors, which might be relevant for version 2.2.2. Again, check the documentation for method availability.

#### Configuration Options

The library supports various writers for different output formats, as detailed in the table below, based on current documentation, with a note to verify for version 2.2.2:

| Writer Class          | Format   | Notes                                                                 |
|-----------------------|----------|----------------------------------------------------------------------|
| PngWriter             | PNG      | Compression level configurable, default -1                           |
| SvgWriter             | SVG      | Suitable for vector graphics, no compression options                 |
| WebPWriter            | WebP     | Quality 0-100, default 80, good for web use                          |
| PdfWriter             | PDF      | Unit in mm, default, good for print                                 |

Encoding options include UTF-8 (default) and ISO-8859-1, with the latter recommended for barcode scanner compatibility. Round block size modes (margin, enlarge, shrink, none) can improve readability, but their availability in 2.2.2 needs confirmation.

#### Advanced Features and Considerations

For advanced use, such as embedding logos, the Builder class supports methods like `logoPath()` and `logoResizeToWidth()`, as seen in a Medium article ([Medium](https://johnrix.medium.com/creating-qr-codes-with-embedded-images-in-php-d926e4546b31)). However, these might be post-2.2.2 additions, so test for compatibility. Validation of generated QR codes is possible but impacts performance and is disabled by default, a detail from [GitHub](https://github.com/endroid/qr-code).

Given the library's abandonment note on [Packagist](https://packagist.org/packages/endroid/qr-code), it's worth noting potential security or maintenance concerns, though for basic use, it remains viable. For Symfony users, there's a bundle ([GitHub](https://github.com/endroid/qr-code-bundle)), but that's outside general PHP usage.

#### Version-Specific Notes

Research showed no direct documentation for version 2.2.2, with GitHub tags not listing it, suggesting it might be an older release or typo. The current repository shows versions up to 6.0.0, and [Packagist](https://packagist.org/packages/endroid/qr-code) lists it as abandoned, recommending endroid/qr-code, which is confusing as it's the same package. This indicates potential renaming or versioning issues, so users should lock dependencies and test upgrades.

#### Conclusion

Using "endroid/qr-code" version 2.2.2 involves installing via Composer, ensuring GD extension, and generating QR codes with the Builder or QrCode class. While examples are based on current documentation, verify API differences for 2.2.2, especially for advanced features. For further details, consult the library's GitHub page and related Stack Overflow discussions.

#### Key Citations

- [QR Code Generator GitHub Repository](https://github.com/endroid/qr-code)
- [endroid/qr-code Packagist Page](https://packagist.org/packages/endroid/qr-code)
- [Creating QR Codes with Embedded Images Medium Article](https://johnrix.medium.com/creating-qr-codes-with-embedded-images-in-php-d926e4546b31)
- [Endroid QR Code Stack Overflow Discussion](https://stackoverflow.com/questions/40777377/endroid-qr-code)
