---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断与修复CPU使用率过高问题
translated: true
type: note
---

## 发生了什么（简述）

服务器风扇噪音增大是因为 **Apache 工作进程陷入 100% CPU 占用**。
调查显示：

* 多个 `apache2` 进程达到 **100% CPU 占用**
* 持续运行 **35–58 分钟**（并非短暂现象）
* 内存使用正常 → **并非内存泄漏**
* RAM 大部分空闲 → **属于 CPU 密集型问题**

随后确定了根本原因：

**Uptime-Kuma 持续轮询 Nextcloud 仪表板端点：**

```
/apps/dashboard/
```

在 **Nextcloud 33.0.0** 中，该仪表板会加载一个 **PresetManager**，该管理器会遍历所有应用/配置。
该路径中的某些操作导致 **执行极慢或陷入无限循环**。

因此每一次健康检查请求：

```
Uptime-Kuma → /apps/dashboard/ → 重度循环 → CPU 100%
```

由于 Uptime-Kuma 持续轮询，它 **反复触发高消耗代码**，导致 Apache 工作进程堆积。

结果：

* 工作进程堆积
* CPU 峰值飙升
* 平均负载攀升（修复后从 11 → 9 → 3.6）
* 风扇高速运转

---

## 重启后 CPU 下降的原因

Apache 重启时：

* 旧的僵死工作进程被终止
* 队列被清空
* 仪表板轮询停止
* 负载迅速下降

因此：

```
负载 11 → 3.68，用时不足 2 分钟
CPU 空闲率 99%
风扇恢复安静
```

---

## 正确的修复方法（重要）

不要将仪表板用作健康检查端点。

### ❌ 错误做法（消耗大的 UI 页面）

```
/apps/dashboard/
```

此页面会加载：

* UI
* 应用
* 配置
* PresetManager
* 循环

### ✅ 正确做法（轻量级健康检查端点）

```
/status.php
```

返回：

```json
{"installed":true,"maintenance":false,"needsDbUpgrade":false}
```

速度极快，无 UI，无循环。

因此将 Uptime-Kuma 监控目标改为：

```
https://你的nextcloud域名/status.php
```

---

## "分析" 部分详解

### 1. 为何 12 个工作进程 100% CPU 占用很重要

Apache 使用工作进程。
如果 12 个工作进程僵死：

* 所有 CPU 核心繁忙
* 新请求排队
* 系统负载增加
* 风扇高速运转

这就是 **工作进程耗尽**。

---

### 2. 列出的 3 种可能原因

#### (1) DDoS / 洪水攻击

来自互联网的请求过多。

检查方法：

```
tail access.log
```

查找重复的 URL 或 IP。

---

#### (2) PHP 脚本失控  ← 正是此原因

某个端点陷入循环或执行极慢。

例如：

```
/apps/dashboard/
```

每个请求都消耗大量 CPU。

---

#### (3) 后端响应缓慢

工作进程在等待：

* 数据库
* Redis
* 上游代理

但通常 CPU 不会达到 100% —— 它们会在等待时处于空闲状态。

因此可能性较小。

---

## 诊断命令详解

### 查看被访问的 URL

```
sudo tail -f /var/log/apache2/access.log
```

实时显示请求。

---

### 查找最频繁访问的 URL

```
cut -d'"' -f2 | sort | uniq -c | sort -rn | head
```

示例输出：

```
2000 GET /apps/dashboard/
50   GET /status.php
```

由此可知仪表板是问题所在。

---

### 查找攻击源 IP

```
awk '{print $1}' access.log | sort | uniq -c | sort -rn
```

显示：

```
5000 127.0.0.1
```

表示是本地监控器（Uptime-Kuma）。

---

## 导致无限 CPU 循环的原因

因为：

```
Uptime-Kuma (每 10 秒)
        ↓
GET /apps/dashboard/
        ↓
Nextcloud 加载应用
        ↓
PresetManager 遍历配置
        ↓
缓慢/无限循环
        ↓
CPU 100%
        ↓
请求未完成
        ↓
Uptime-Kuma 发送新请求
        ↓
更多工作进程僵死
```

这就是 **反馈循环导致的系统崩溃**。

---

## 最终修复清单

### 1. 更改 Uptime-Kuma 监控 URL

```
/apps/dashboard/
      ↓
/status.php
```

### 2. 更新 Nextcloud

您当前版本：

```
33.0.0
```

升级至：

```
33.0.1+
```

此 Bug 可能已修复。

---

### 3. 可选：保护 Apache 工作进程

限制最大工作进程数：

```
/etc/apache2/mods-enabled/mpm_prefork.conf
```

示例：

```
MaxRequestWorkers 20
```

防止 CPU 失控。

---

## 总结

风扇噪音源于：

```
Uptime-Kuma 轮询
        ↓
Nextcloud 仪表板
        ↓
PresetManager 循环
        ↓
Apache 工作进程僵死
        ↓
CPU 100%
```

修复方法：

```
更改监控端点 → /status.php
更新 Nextcloud
```

此举可永久防止该循环。
