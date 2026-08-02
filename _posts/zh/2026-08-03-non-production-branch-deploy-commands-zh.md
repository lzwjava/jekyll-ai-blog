---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 非生产分支部署命令
translated: true
type: note
---

简短的回答是：**对于非生产分支，使用 `npx wrangler versions upload`**——这实际上是默认选项，因此你可以将该字段留空。

## 该命令的作用

Workers Builds（即你正在配置的 Git → Worker CI/CD）运行一个两步流程：

1. **构建命令**（可选）—— 编译你的项目
2. **部署命令** —— 部署 Worker，默认值为 `npx wrangler deploy`

对于提交到**非生产分支**（例如本仓库中的 `develop`、`nw`、`test`）的代码，部署命令会被替换为**非生产分支部署命令**，该命令：

- 默认使用 `npx wrangler versions upload`
- 将构建结果作为**带有 preview URL 的版本**上传（可在 Version History → View build 中看到）
- 不会**将其提升为活跃的生产环境部署——合并前测试是安全的

因此，除非你需要自定义设置，否则保留默认值即可。

## 何时需要自定义

| 场景 | 非生产分支部署命令 |
| --- | --- |
| 默认（推荐） | `npx wrangler versions upload` |
| 不同的包管理器 | `yarn exec wrangler versions upload` |
| 将预览部署到预发布环境 | `npx wrangler versions upload --env staging` |

## ⚠️ 针对*本项目*的重要注意事项

此仓库是一个 **Jekyll 静态博客**，而不是一个 Worker：

- 项目中**没有 `wrangler.jsonc`/`wrangler.toml`**，没有 Worker 源码，`package.json` 中也没有 `wrangler` 依赖
- Workers Builds 需要一个名称与仪表板中的 Worker 名称相匹配的 wrangler 配置文件，否则构建将失败
- 如果没有配置文件，`npx wrangler deploy` 会触发 **autoconfig**，它会为你创建一个生成 Worker 脚手架代码的 PR——这很可能不是你想要的 Jekyll 站点处理方式

对于这个项目，**Cloudflare Pages** 才是合适的产品：

- **构建命令：** `bundle install && bundle exec jekyll build`
- **输出目录：** `_site`
- **非生产分支：** Pages 会自动为预览运行相同的构建命令，并为每个分支分配一个 `*.pages.dev` 预览 URL——无需单独的部署命令

如果你仍然想将其放在 Workers 上（例如，通过具有 assets binding 的 Worker 来提供静态站点服务），你需要首先添加一个 wrangler 配置文件。需要我为你生成一个吗？
