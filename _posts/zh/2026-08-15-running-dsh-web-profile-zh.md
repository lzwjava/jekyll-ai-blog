---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 运行 dsh Web 配置文件
translated: true
type: note
---

`npx @deepseek-ai/dsh web` **是**运行命令 —— “是否继续？”提示只是 npx 正在将包下载到其缓存中；下载完成后，npx 会立即执行它。一旦缓存，后续运行将不再提示。

因此，在 `/mnt/data/bilingual-gpt` 目录下：

```sh
npx @deepseek-ai/dsh web
```

这会启动 **web 配置文件**（`--profile web` 的别名）：一个提供 DeepSeek Harness 浏览器界面的服务器。

有用的变体：

```sh
npx @deepseek-ai/dsh web --port 8080        # 指定端口（0 表示让操作系统选择）
npx @deepseek-ai/dsh web --host 0.0.0.0     # 绑定主机
npx @deepseek-ai/dsh web --help             # web 应用自身的标志
```

注意：

- 如果提示令你烦恼，可以一次性安装并完全跳过 npx：

  ```sh
  npm install -g @deepseek-ai/dsh
  dsh web
  ```

- 该代理由真实的 DeepSeek API 调用支持，因此请先导出 `DEEPSEEK_API_KEY`（或将其放入 `.env` 文件中），否则 web 界面将无法回答任何问题。
- 如果不使用 `--port`，则会在配置文件的已组合主机/端口上提供服务（可通过配置文件补丁进行设置；服务器启动时会打印其监听地址）。

然后在浏览器中打开打印出的 URL（通常为 `http://localhost:3080`）。
