---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 查找您的 Npm 配置文件路径
translated: true
type: note
---

`npm config get userconfig` 是一个用于显示 **user-level npm configuration file**（用户级 npm 配置文件）文件路径的命令。

## What it does

当你运行此命令时，npm 会输出存储用户特定 npm 设置的 `.npmrc` 文件位置。通常路径为：

- **Linux/Mac**: `~/.npmrc`（在你的用户主目录下）
- **Windows**: `C:\Users\YourUsername\.npmrc`

## Example

```bash
$ npm config get userconfig
/home/username/.npmrc
```

## What's in this file?

userconfig 文件存储了你的个人 npm configuration 设置，例如：

- Registry URLs（npm 下载 package 的地址）
- 用于私有 registries 的 Authentication tokens
- Proxy 设置
- 默认的 package 设置
- 任何你通过 `npm config set` 设置的自定义配置

## Related commands

- `npm config list` - 显示你当前所有的 npm configuration 设置
- `npm config edit` - 在默认编辑器中打开你的 userconfig 文件
- `npm config set <key> <value>` - 在你的 userconfig 文件中设置配置值

当你需要手动编辑 npm 配置文件或排查配置问题（troubleshoot configuration issues）时，这个命令非常有用。
