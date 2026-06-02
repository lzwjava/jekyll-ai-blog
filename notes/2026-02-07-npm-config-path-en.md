---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Find Your Npm Config File Path
translated: false
type: note
---

`npm config get userconfig` is a command that shows you the file path to your **user-level npm configuration file**.

## What it does

When you run this command, npm will output the location of your `.npmrc` file that stores user-specific npm settings. This is typically:

- **Linux/Mac**: `~/.npmrc` (in your home directory)
- **Windows**: `C:\Users\YourUsername\.npmrc`

## Example

```bash
$ npm config get userconfig
/home/username/.npmrc
```

## What's in this file?

The userconfig file stores your personal npm configuration settings, such as:

- Registry URLs (where npm downloads packages from)
- Authentication tokens for private registries
- Proxy settings
- Default package settings
- Any custom configuration you've set with `npm config set`

## Related commands

- `npm config list` - Shows all your current npm configuration settings
- `npm config edit` - Opens your userconfig file in your default editor
- `npm config set <key> <value>` - Sets a configuration value in your userconfig file

This is useful when you need to manually edit your npm configuration file or troubleshoot configuration issues.
