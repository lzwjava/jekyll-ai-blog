---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 清理磁盘空间
translated: true
type: post
---

## 设置

使用路径设置 -> 通用 -> 存储 -> 存储设置，查看磁盘空间的使用情况并删除不必要的文件。

## 查找大文件

使用 `du` 查找大文件。例如，使用命令 `du -hL -d 1 | sort -h`。

在某个目录中，使用 `find . -type f -print0 | xargs -0 du -h | sort -rh | head -n 20`。

## 删除应用程序

在应用程序目录中删除应用程序。

## 下载

删除下载的软件包 dmg 文件，这些文件可以从互联网上轻松下载。

## 便携磁盘

购买一个便携磁盘并将一些文件移动到那里。

## 手机

将照片导入到您的 Mac，并在导入后删除它们。
