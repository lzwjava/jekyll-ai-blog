---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Camoufox JS 获取详细选项缺失
translated: true
type: note
---

`npx camoufox-js fetch` 命令**没有**官方的 `--verbose` 或 `-v` 标志。

JavaScript 版本（`camoufox-js`）是一个轻量级的封装/移植版本，其 fetch 命令非常简单。它只显示基本的进度信息，例如：

```
正在获取 Camoufox 二进制文件...
正在下载 Camoufox... [----------------------------------------] 0% 1523.2s
```

没有内置的详细模式来显示更详细的日志（例如确切的下载 URL、HTTP 头部信息或逐块下载速度）。

### 在下载过程中获取更多信息的最佳方法

1. **与代理结合使用（正如您之前询问的）** —— 这仍然是最有用的方式：

   ```bash
   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
   ```

2. **强制重新下载**（如果之前的下载损坏了，这很有用）：

   ```bash
   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch --force
   ```

   （注意：`--force` 参数可能支持也可能不支持；如果显示错误，只需手动删除缓存文件夹并重试。）

3. **使用 npm/npx 详细模式查看更多输出**（有一点帮助）：

   ```bash
   npm_config_loglevel=verbose HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
   ```

4. **手动下载替代方案（最透明）**：
   - 首先，通过查看包内部找到真实的下载 URL。
   - 运行此命令来定位缓存和源代码位置：

     ```bash
     find ~/.cache -name "*camoufox*" 2>/dev/null || echo "未找到缓存"
     ```

   - 许多中国用户最终通过浏览器 + VPN/代理手动下载大型二进制文件，并将其放置在正确的缓存文件夹中。

### 针对您的情况（中国 + 下载缓慢）的快速提示

目前最实用的命令是：

```bash
HTTP_PROXY=http://127.0.0.1:7890 \
HTTPS_PROXY=http://127.0.0.1:7890 \
npx camoufox-js fetch
```

在运行之前，请确保您的代理（Clash、V2Ray 等）正在运行并设置为 **全局** 或 **代理模式**。

如果需要，可以先运行以下命令测试代理是否对下载有效：

```bash
HTTP_PROXY=http://127.0.0.1:7890 curl -I https://www.google.com
```

您是否需要手动查找和清除 Camoufox 下载缓存的命令，以便重新开始？

参考资料：

- <https://github.com/apify/camoufox-js>
- <https://www.npmjs.com/package/@askjo/camoufox-browser>
- <https://www.mintlify.com/jo-inc/camofox-browser/installation>
