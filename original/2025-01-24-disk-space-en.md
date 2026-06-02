---
audio: true
generated: false
image: false
lang: en
layout: post
title: Clean Up Disk Space
type: post
---

## Settings

Use the path Settings -> General -> Storage -> Storage settings to find out how disk space is occupied and delete unnecessary files.

## Find Large Files

Use `du` to find large files. For example, use the command `du -hL -d 1 | sort -h`.

In some directory, use `find . -type f -print0 | xargs -0 du -h | sort -rh | head -n 20`.

## Delete Applications

Delete applications in the application directory.

## Downloads

Remove downloaded package dmg files, which can be easily downloaded from the internet.

## Portable Disk

Purchase a portable disk and move some files there.

## iPhone

Import photos to your Mac and delete them after importing.
