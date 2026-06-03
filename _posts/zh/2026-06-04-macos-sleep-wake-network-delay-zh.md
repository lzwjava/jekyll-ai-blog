---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 睡眠唤醒网络延迟
translated: true
type: note
---

这是经典的 macOS 从睡眠中唤醒的网络问题。

当你打开屏幕盖时，macOS 从睡眠状态恢复。WiFi 接口重新连接，但网络栈尚未完全就绪 —— TCP 连接会在 SSL 握手阶段失败，因为底层套接字在网络实际可用之前就发生了连接重置或超时。

整个过程如下：

1. 打开屏幕盖 → macOS 唤醒
2. WiFi 重新连接（需要 2-5 秒）
3. DNS 开始正常工作
4. TCP 连接变得稳定
5. TLS/SSL 握手成功

你在第 2-3 步、网络尚未稳定时执行了 `git pull`。

解决方法很简单 —— 打开屏幕盖后等待几秒，然后重试：

```bash
git pull
```

如果你希望更稳健一点，可以用重试机制包装一下：

```bash
for i in 1 2 3; do git pull && break; sleep 3; done
```

或者如果这种情况经常发生，你可以强制 git 使用特定的 TLS 后端并添加连接超时：

```bash
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 10
```

这样，如果连接在前 10 秒内速度太慢，git 会重试，而不是立即因 SSL 错误而失败。

另外 —— 如果你在使用代理（我知道你用了 hysteria2），代理隧道本身在睡眠后也需要重新建立，这会导致更多的延迟。`SSL_ERROR_SYSCALL` 特别表明连接在握手过程中被重置，这正是网络在正在进行的连接中突然断开时会出现的现象。