---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Apache 工作进程中央处理器过载导致
translated: true
type: note
---

查看 `top` 输出结果，情况如下：

## 问题分析

**12 个以上 Apache2 工作进程均处于 100% CPU 占用** —— 这是导致风扇噪音的根本原因。

关键观察点：
- 这些进程已持续运行 **35-58 分钟以上** 且 CPU 持续占满 100% —— 并非瞬时峰值
- 所有进程均为 `www-data`（Web 服务器工作进程），而非 `root`（非启动/配置进程）
- 各进程内存使用正常（约 61-71 MB RES），因此 **排除内存泄漏**
- 系统内存充足（剩余 28 GB），交换空间基本未使用

## 可能原因（按可能性排序）

1. **DDoS / 洪水攻击** —— 有人通过大量请求冲击服务器
2. **PHP/CGI 脚本失控** —— 某个接口存在死循环或计算密集型操作
3. **慢资源耗尽** —— 请求因等待缓慢的后端（数据库、上游代理）响应而导致工作进程堆积

## 实时诊断

检查正在响应的请求：
```bash
# 查看连接状态及被访问的 URL
sudo apachectl status          # 若启用 mod_status 模块可使用此命令
# 或
sudo cat /proc/$(pgrep -f apache2 | head -1)/net/tcp

# 检查访问日志中的洪水攻击特征
sudo tail -f /var/log/apache2/access.log | cut -d'"' -f2 | sort | uniq -c | sort -rn | head -20

# 检查攻击源 IP
sudo awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -20
```

检测是否是 PHP 脚本循环执行：
```bash
# 查看各工作进程实际执行的程序
sudo ls -la /proc/$(pgrep -f apache2 | head -1)/fd | grep php

# 对工作进程进行简要追踪
sudo strace -p $(pgrep -f apache2 | head -1) -c -e trace=all &
sleep 3 && sudo kill %1
```

## 快速缓解措施

若为 DDoS 攻击：
```bash
# 屏蔽攻击最频繁的 IP
sudo ufw deny from <attacker-ip>
# 若安装 mod_evasive / fail2ban 也可使用对应工具
```

若为失控脚本 —— 根据访问日志定位 URL，可封锁对应路由或修复脚本。

请执行 `sudo tail -100 /var/log/apache2/access.log` 并查看结果，这将有助于快速定位问题。