---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenWrt Hysteria2 via PassWall2 Guide
translated: false
type: note
---

I'll search for information about OpenWrt support for Hysteria2.Let me search for more specific information about OpenWrt packages and libraries for Hysteria2.Question: Does OpenWrt have libraries that support Hysteria2?

Answer:

Yes, OpenWrt does have library support for Hysteria2, primarily through the **PassWall2** plugin ecosystem. Here's what you need to know:

## Official Support

OpenWrt supports Hysteria2 through the LuCI app openwrt-passwall, which is the primary way to implement Hysteria2 on OpenWrt routers.

## PassWall2 Package

PassWall2 includes Hysteria and Hysteria2 for high-performance UDP transport. The latest PassWall2 releases include the Hysteria package version 2.7.1, making it readily available in the package repositories.

## Installation Method

You can install PassWall2 by downloading the IPK package from the releases page and uploading it to your router via SCP, LuCI upload, or wget. The package format depends on your router's package manager (either opkg or apk).

## Protocol Support

Hysteria2 is specifically supported through the sing-box implementation within PassWall2, which handles Hysteria2 protocol support.

## Compilation Note

There have been some compilation issues reported in the official OpenWrt repository, but the PassWall2 ecosystem maintains pre-built binary packages that work reliably across various router architectures.

## Summary

OpenWrt does not natively include Hysteria2 in its core libraries, but the community-maintained **PassWall2 plugin** provides comprehensive support with pre-compiled packages, making Hysteria2 easily accessible for most OpenWrt users without requiring manual compilation.

References:

- [PassWall2 GitHub Repository](https://github.com/Openwrt-Passwall/openwrt-passwall2)
- [Hysteria Official Installation Page](https://v1.hysteria.network/docs/installation/)
- [OpenWrt PassWall Build - SourceForge](https://sourceforge.net/projects/openwrt-passwall-build/files/)