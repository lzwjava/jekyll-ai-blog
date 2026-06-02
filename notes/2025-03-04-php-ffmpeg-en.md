---
audio: false
generated: true
lang: en
layout: post
title: Using ffmpeg in PHP
translated: false
type: note
---

### Key Points
- It seems likely that to use "php-ffmpeg/php-ffmpeg" version ~0.5, you first need to install FFMpeg on your system and then use Composer to install the PHP library.
- Research suggests including the autoload file and creating an instance of `FFMpeg\FFMpeg` for media manipulation, with options to specify binary paths if needed.
- The evidence leans toward using methods like `open()`, `save()`, and `frame()` for basic operations, but check the GitHub documentation for full details due to potential version-specific differences.

---

### Installation
First, ensure FFMpeg is installed on your system:
- On Ubuntu, use `sudo apt-get install ffmpeg`.
- On macOS, use `brew install ffmpeg`.
- On Windows, download from [this website](https://www.gyan.dev/ffmpeg/builds/) and follow the instructions.

Next, install the php-FFMpeg library via Composer with:
```
composer require php-FFMpeg/php-FFMpeg:~0.5
```

### Setup and Usage
Include the autoload file in your PHP script:
```php
require_once 'vendor/autoload.php';
```

Create an instance of `FFMpeg\FFMpeg`, optionally specifying paths if FFMpeg binaries aren't in the system PATH:
```php
use FFMpeg\FFMpeg;
$ff = FFMpeg::create(array(
    'binary' => '/path/to/FFMpeg',
    'ffprobe' => '/path/to/FFprobe'
));
```

Open a media file and perform operations, such as:
- Transcoding: `$video->save('output.mp4', new FFMpeg\Format\Video\X264());`
- Extracting a frame: `$frame = $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5)); $frame->save('frame.jpg');`
- Clipping: `$clip = $video->clip(FFMpeg\Coordinate\TimeCode::fromSeconds(10), FFMpeg\Coordinate\TimeCode::fromSeconds(20)); $clip->save('clip.mp4');`

For more details, refer to the library's documentation on [GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg).

---

### Survey Note: Comprehensive Guide to Using php-FFMpeg/php-FFMpeg Version ~0.5

This note provides an in-depth exploration of using the "php-FFMpeg/php-FFMpeg" library, specifically version approximately 0.5, based on available information. It expands on the direct answer by including all relevant details from the research, ensuring a thorough understanding for users seeking to implement this PHP library for media manipulation.

#### Background and Context
The "php-FFMpeg/php-FFMpeg" library is a PHP wrapper for the FFMpeg binary, enabling object-oriented manipulation of video and audio files. It supports tasks such as transcoding, frame extraction, clipping, and more, making it valuable for developers working on media-related applications. The version specification "~0.5" indicates any version greater than or equal to 0.5 and less than 1.0, suggesting compatibility with older PHP versions, likely found in the 0.x branch of the repository.

Given the current date, March 3, 2025, and the library's evolution, version 0.5 may be part of legacy support, with the main branch now requiring PHP 8.0 or higher. This note assumes the user is working within the constraints of this version, acknowledging potential differences in functionality compared to newer releases.

#### Installation Process
To begin, FFMpeg must be installed on the system, as the library relies on its binaries for operations. Installation methods vary by operating system:
- **Ubuntu**: Use the command `sudo apt-get install ffmpeg` to install via the package manager.
- **macOS**: Utilize Homebrew with `brew install ffmpeg` for a straightforward installation.
- **Windows**: Download the FFMpeg binaries from [this website](https://www.gyan.dev/ffmpeg/builds/) and follow the provided instructions, ensuring the executables are accessible in the system PATH or specified manually.

Following FFMpeg installation, the php-FFMpeg library is installed via Composer, the PHP package manager. The command `composer require php-FFMpeg/php-FFMpeg:~0.5` ensures the correct version is fetched. This process creates a `vendor` directory in the project, housing the library and its dependencies, with Composer managing autoloading for seamless integration.

#### Setup and Initialization
After installation, include the autoload file in your PHP script to enable access to the library's classes:
```php
require_once 'vendor/autoload.php';
```

Create an instance of `FFMpeg\FFMpeg` to start using the library. The creation method allows for configuration, particularly important if FFMpeg binaries are not in the system PATH:
```php
use FFMpeg\FFMpeg;
$ff = FFMpeg::create(array(
    'timeout' => 0,
    'thread_count' => 12,
    'binary' => '/path/to/your/own/FFMpeg',
    'ffprobe' => '/path/to/your/own/FFprobe'
));
```
This configuration supports setting timeouts, thread counts, and explicit binary paths, enhancing flexibility for different system setups. The default setup looks for binaries in the PATH, but manual specification ensures compatibility, especially on custom environments.

#### Core Usage and Operations
The library provides a fluent, object-oriented interface for media manipulation. Begin by opening a media file:
```php
$video = $ff->open('input.mp4');
```
This supports local filesystem paths, HTTP resources, and other FFMpeg-supported protocols, with a list of supported types available via the `ffmpeg -protocols` command.

##### Transcoding
Transcoding involves converting media to different formats. Use the `save` method with a format instance:
```php
$format = new FFMpeg\Format\Video\X264();
$video->save('output.mp4', $format);
```
The `X264` format is one example; the library supports various video and audio formats, implementable via `FFMpeg\Format\FormatInterface`, with specific interfaces like `VideoInterface` and `AudioInterface` for respective media types.

##### Frame Extraction
Extracting frames is useful for thumbnails or analysis. The following code extracts a frame at 5 seconds:
```php
$frame = $video->frame(FFMpeg\Coordinate\TimeCode::fromSeconds(5));
$frame->save('frame.jpg');
```
The `TimeCode` class, part of `FFMpeg\Coordinate`, ensures precise timing, with options for accuracy in image extraction.

##### Clipping
To clip a portion of the video, specify start and end times:
```php
$clip = $video->clip(FFMpeg\Coordinate\TimeCode::fromSeconds(10), FFMpeg\Coordinate\TimeCode::fromSeconds(20));
$clip->save('clip.mp4');
```
This creates a new video segment, maintaining the original quality and format, with the ability to apply additional filters if needed.

#### Advanced Features and Considerations
The library supports additional features, as outlined in the documentation:
- **Audio Manipulation**: Similar to video, audio can be transcoded with `FFMpeg\Media\Audio::save`, applying filters, adding metadata, and resampling.
- **GIF Creation**: Animated GIFs can be saved using `FFMpeg\Media\Gif::save`, with optional duration parameters.
- **Concatenation**: Combine multiple media files using `FFMpeg\Media\Concatenate::saveFromSameCodecs` for same codecs or `saveFromDifferentCodecs` for varied codecs, with resources for further reading at [this link](https://trac.ffmpeg.org/wiki/Concatenate), [this link](https://ffmpeg.org/ffmpeg-formats.html#concat-1), and [this link](https://ffmpeg.org/ffmpeg.html#Stream-copy).
- **Advanced Media Handling**: Supports multiple inputs/outputs with `-filter_complex`, useful for complex filtering and mapping, with built-in filter support.
- **Metadata Extraction**: Use `FFMpeg\FFProbe::create` for metadata, validating files with `FFMpeg\FFProbe::isValid` (available since v0.10.0, noting version 0.5 may lack this).

Coordinates, such as `FFMpeg\Coordinate\AspectRatio`, `Dimension`, `FrameRate`, `Point` (dynamic since v0.10.0), and `TimeCode`, provide precise control over media properties, though some features like dynamic points may not be available in version 0.5.

#### Version-Specific Notes
Given the "~0.5" specification, the library likely aligns with the 0.x branch, supporting older PHP versions. The GitHub repository indicates PHP 8.0 or higher for the main branch, with 0.x for legacy support. However, exact version 0.5 details were not explicitly found in releases, suggesting it may be part of commit history or branch commits. Users should verify compatibility, as newer features like certain coordinate types (e.g., dynamic points) may require versions beyond 0.5.

#### Documentation and Further Reading
While the Read the Docs page ([Read the Docs](https://FFMpeg-PHP.readthedocs.io/en/latest/)) appeared empty, the GitHub repository ([GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg)) contains comprehensive documentation within the README, covering API usage, formats, and examples. This is the primary resource for version 0.5, given the lack of specific online documentation for this legacy version.

#### Table: Summary of Key Operations and Methods

| Operation               | Method Example                                      | Description                                      |
|-------------------------|----------------------------------------------------|-------------------------------------------------|
| Open Media File         | `$ff->open('input.mp4')`                           | Loads a media file for manipulation             |
| Transcode Video         | `$video->save('output.mp4', new X264())`           | Converts to specified format                    |
| Extract Frame           | `$video->frame(TimeCode::fromSeconds(5))->save('frame.jpg')` | Extracts frame at specified time, saves as image |
| Clip Video              | `$video->clip(TimeCode::fromSeconds(10), TimeCode::fromSeconds(20))->save('clip.mp4')` | Creates clip between times, saves as new file   |
| Configure Instance      | `FFMpeg::create(array('binary' => '/path/to/FFMpeg'))` | Sets custom binary paths and options            |

This table encapsulates core functionality, aiding users in quick reference while implementing the library.

#### Unexpected Detail: Legacy Version Implications
An unexpected aspect is the potential limitation of version 0.5, given its placement in the 0.x branch for older PHP support. This may restrict access to modern features, such as dynamic coordinate points introduced in v0.10.0, requiring users to check branch commits for exact capabilities, adding a layer of complexity not immediately apparent in newer versions.

#### Conclusion
Using "php-FFMpeg/php-FFMpeg" version ~0.5 involves installing FFMpeg, setting up via Composer, and leveraging an object-oriented API for media tasks. While basic operations like transcoding and frame extraction are straightforward, version-specific differences may necessitate consulting the 0.x branch documentation on [GitHub](https://github.com/PHP-FFMpeg/PHP-FFMpeg). This comprehensive approach ensures users can effectively utilize the library, acknowledging both its power and potential legacy constraints.

---

### Key Citations
- [FFMpeg PHP Object Oriented Library Packagist](https://packagist.org/products/php-FFMpeg/php-FFMpeg)
- [PHP-FFMpeg GitHub Repository Documentation](https://github.com/PHP-FFMpeg/PHP-FFMpeg)
- [FFMpeg PHP Read the Docs Documentation](https://FFMpeg-PHP.readthedocs.io/en/latest/)
- [FFMpeg Download and Builds Website](https://www.gyan.dev/ffmpeg/builds/)
- [FFMpeg Concatenation Wiki Page](https://trac.ffmpeg.org/wiki/Concatenate)
- [FFMpeg Formats Documentation Page](https://ffmpeg.org/ffmpeg-formats.html#concat-1)
- [FFMpeg Command Line Tool Documentation](https://ffmpeg.org/ffmpeg.html#Stream-copy)
