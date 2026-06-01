---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 反向代理设置故障排除
translated: true
type: note
---

如下所示：

```
Caddy 配置: /etc/caddy/Caddyfile
──────────────────────────────────────
:80 {
    reverse_proxy localhost:8888
}
```

Caddy 正在将 80 端口反向代理到 `localhost:8888`。8888 端口是经典的 **Jupyter Notebook** 端口。502 错误意味着 Jupyter 当前没有运行。

因此流程是：
```
互联网 → :80 (Caddy) → localhost:8888 (Jupyter，目前已停止)
```

这是标准的 AMD Dev Cloud 配置——他们提供 Caddy 作为 Jupyter 的前端入口。没什么大问题，但如果你不需要 Jupyter/网页访问，可以将其停止：

```
systemctl stop caddy && systemctl disable caddy
```

或者使用 UFW 阻止 80 端口。对于 GPT-2 训练，你不需要这些——SSH 就足够了。