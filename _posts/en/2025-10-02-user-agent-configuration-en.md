---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter User Agent Configuration Arrays
translated: false
type: note
---

### Overview
This PHP code snippet is part of the CodeIgniter framework (a PHP web framework), specifically from the User Agent Class configuration file. It defines four arrays (`$platforms`, `$browsers`, `$mobiles`, and `$robots`) that map user agent string fragments to human-readable names for browsers, operating systems, mobile devices, and web crawlers/bots. The code is used to parse and identify the type of device, browser, or bot visiting a website based on the HTTP User-Agent header sent by clients.

The arrays are associative (key-value pairs), where keys are partial strings from user agent strings (case-insensitive matches), and values are the corresponding display names. CodeIgniter's User Agent library uses these for detection, such as determining if a visitor is on Android, using Chrome, or is a search bot.

### $platforms Array
This array identifies operating systems or platforms. The keys are substrings that might appear in the User-Agent header, and values are clean names for display.

- **Example entries**:
  - `'windows nt 10.0'` → `'Windows 10'`
  - `'android'` → `'Android'`
  - `'os x'` → `'Mac OS X'`
- **Purpose**: Helps detect the client's OS (e.g., Windows, iOS, Linux) for analytics, content customization, or feature tweaks.
- **Note**: Order matters for accuracy, as some substrings might overlap (e.g., `'windows'` is a catch-all at the end).

### $browsers Array
Identifies web browsers. Browsers often report multiple identifiers, so the order prioritizes subtypes first (as per the comment).

- **Example entries**:
  - `'Chrome'` → `'Chrome'`
  - `'MSIE'` → `'Internet Explorer'`
  - `'Firefox'` → `'Firefox'`
  - Special case: `'Opera.*?Version'` (regex-like match) for modern Opera that reports as "Opera/9.80" with a version.
- **Purpose**: Determines the browser (e.g., Chrome, Safari) to serve browser-specific features or redirects.
- **Regex note**: Some keys use basic regex patterns (e.g., `.*?` for wildcard matching), handled in the library.

### $mobiles Array
Maps user agent flags for mobile devices, phones, and related devices/browsers. It's larger and includes phones, tablets, game consoles, and fallback categories.

- **Structured sections**:
  - Phones/Manufacturers: `'iphone'` → `'Apple iPhone'`, `'samsung'` → `'Samsung'`.
  - Operating Systems: `'android'` → `'Android'`, `'symbian'` → `'Symbian'`.
  - Browsers: `'opera mini'` → `'Opera Mini'`, `'fennec'` → `'Firefox Mobile'`.
  - Other/Fallback: `'mobile'` → `'Generic Mobile'` for unmatched mobile indicators.
- **Purpose**: Flags mobile devices for responsive design, mobile-only features, or app redirects. Includes legacy entries (some commented out as outdated).

### $robots Array
Lists common web crawlers and bots. Keys are substrings from bot user agents.

- **Example entries**:
  - `'googlebot'` → `'Googlebot'`
  - `'bingbot'` → `'Bing'`
  - `'yandex'` → `'YandexBot'`
- **Purpose**: Identifies crawlers for SEO handling, like serving different content to bots (e.g., no ads) or logging bot traffic.

### Usage in CodeIgniter
- The User Agent Class loads this file and uses methods like `is_browser()`, `is_mobile()`, `is_robot()`, and `platform()` to parse the User-Agent string.
- It performs case-insensitive searches through these arrays to match keys against the string.
- For discrepancies (e.g., new devices/browsers not listed), you'd update these arrays manually or via community extensions.

### Additional Notes
- **Security**: This is purely for data collection; it doesn't execute harmful code. User-Agent strings can be spoofed, so don't rely on this for critical security checks.
- **Updates**: CodeIgniter versions may have added/modified entries; this looks like an older snapshot (e.g., Edge as 'Spartan' is outdated).
- **How to test**: In a PHP script, you could load this and use `strpos` or regex to match against a sample User-Agent string.

If you provide a specific part or have a question about implementation, let me know!
