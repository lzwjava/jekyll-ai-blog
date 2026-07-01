---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 允许浏览，禁止模型迁移
translated: true
type: note
---

问题：当使用赛门铁克 Web 过滤器（Blue Coat ProxySG）作为公司代理时，我们能否为 huggingface.co 编写一条特殊规则，允许员工浏览/探索网站，但阻止推送或拉取模型？

答案：

可以——但你无法通过单一的域名规则实现。关键在于，Hugging Face 上的“浏览”和“模型传输”分布在**不同的主机名和 HTTP 方法**上，因此你要针对这些进行过滤，而不是针对整个 `huggingface.co`。

## HF 流量的实际分布情况

| 活动 | 主机 / 路径 | 方法 |
| --- | --- | --- |
| 浏览模型卡片、搜索、文档 | `huggingface.co`（HTML、`/models`、`/datasets`） | `GET` |
| Web UI XHR/API | `huggingface.co/api/...` | `GET` |
| **拉取**（下载权重） | `cdn-lfs.huggingface.co`、`cdn-lfs-us-1.huggingface.co`、`*.hf.co`，LFS 指针解析到这些地址 | `GET`（大文件） |
| 解析文件 blob | `huggingface.co/.../resolve/...` | `GET` |
| **推送**（上传权重） | `huggingface.co/.../*.git/...`、LFS 的 `POST/PUT` 到 `cdn-lfs*` | `POST`、`PUT` |
| Git 操作 | `huggingface.co/<repo>.git/info/refs?service=git-receive-pack`（推送）vs `git-upload-pack`（拉取） | `GET`/`POST` |

这就是关键所在：**git smart-HTTP 将意图暴露在 URL 中**。`git-upload-pack` = 克隆/拉取，`git-receive-pack` = 推送。

## 推荐的 ProxySG / WebFilter 策略（CPL）

允许网站类别，然后分层添加方法/主机/路径例外。顺序很重要——最具体的拒绝规则放在前面。

```
<Proxy>
; --- 阻止模型推送（git receive-pack + LFS 上传）---
url.host=huggingface.co url.path.regex="git-receive-pack" deny
request.method=(POST,PUT) url.host.regex="cdn-lfs.*\.huggingface\.co" deny
request.method=(POST,PUT) url.host.regex="cdn-lfs.*\.hf\.co" deny

; --- 阻止模型拉取（通过 LFS CDN + resolve 端点的权重下载）---
url.host.regex="cdn-lfs.*\.huggingface\.co" deny
url.host.regex="cdn-lfs.*\.hf\.co" deny
url.path.regex="/resolve/" deny
url.path.regex="git-upload-pack" deny

; --- 允许主域名上的其他所有操作（浏览、搜索、文档、API）---
url.host=huggingface.co allow
url.host=hf.co allow
</Proxy>
```

效果：员工可以阅读模型卡片、数据集、文档以及 API 驱动的 UI，但任何实际的 blob 传输（`/resolve/`、LFS CDN）以及任何 git 推送/拉取都会被阻止。

## 需要注意的问题

1. **HTTPS = 需要 SSL 拦截。**所有 HF 流量都是 TLS 加密的。如果在 ProxySG 上没有 SSL 拦截（MITM），你只能根据 **SNI 主机名**进行过滤，无法过滤路径或方法。这意味着你可以阻止 `cdn-lfs*.huggingface.co`（会同时阻止下载和上传），但**无法区分** `git-upload-pack` 和 `git-receive-pack`，也无法阻止 `/resolve/`。因此：
   - **无 SSL 拦截** → 最简单的策略是：允许 `huggingface.co`，拒绝所有 `cdn-lfs*` 主机。浏览正常，下载失效（因为权重存储在 CDN 上），上传也失效。你失去了“允许拉取，阻止推送”的细粒度，但得到了“允许浏览，阻止传输”。
   - **有 SSL 拦截** → 可以像上述 CPL 那样实现完整的路径/方法控制。

2. **`hf_transfer` / CLI 回退。**`huggingface-cli download` 和 `hf_hub_download` 实际字节是通过 `cdn-lfs*` 获取的，因此 CDN 拒绝规则会捕获它们。但需留意 `HF_ENDPOINT` 覆盖以及员工可能设置的其他镜像配置。

3. **小文件可能漏网。**低于 LFS 阈值的配置文件、tokenizer JSON 和小型模型分片会直接从 `huggingface.co/.../resolve/` 提供，而不经过 CDN。如果你只屏蔽 CDN 主机，这些文件仍然可以下载。为了彻底，应阻止 `/resolve/`（需要 SSL 拦截）。

4. **xet 后端。**HF 正在将大文件存储迁移到 Xet（`*.xethub.hf.co` / `cas-*.huggingface.co`）。将这些主机加入 CDN 拒绝列表，否则通过新路径的下载将绕过 `cdn-lfs` 规则。

## 从代理后面的客户端进行合理性测试

```bash
# 应该成功（浏览）
curl -sI https://huggingface.co/models | head -1

# 应该被阻止（拉取）
huggingface-cli download gpt2 --quiet || echo "拉取被阻止 ✓"

# 应该被阻止（推送）—— 干运行
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/<​USER>/<​REPO> && \
  cd <​REPO> && git push 2>&1 | grep -qi deny && echo "推送被阻止 ✓"
```

结论：实现清晰的“可浏览，不可传输”策略需要 SSL 拦截。如果没有，拒绝 `cdn-lfs*` / xet CDN 主机，并接受你实际阻止的是**所有**模型传输，而不仅仅是推送。
