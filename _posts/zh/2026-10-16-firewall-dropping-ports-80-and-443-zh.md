---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 防火墙丢弃端口80和443
translated: true
type: note
---

## 根本原因已找到：防火墙正在丢弃80/443端口

端口定时测试是关键——它能区分防火墙的**DROP**和死服务：

| 端口 | 结果 | 含义 |
| ------ | -------- | --------- |
| **22** | **开放** | 主机可达，SSH允许 |
| **80** | 超时（6.00秒） | 数据包**被静默丢弃** |
| **443** | 超时（6.01秒） | 数据包**被静默丢弃** |
| **8080** | 在**0.02秒**内被拒绝 | 数据包**到达主机**，操作系统返回"没有服务在监听" |

关键对比是80/443与8080。8080端口在20毫秒内返回RST，证明网络数据包**确实**到达了你的VM。但80和443一直挂起到超时——这是防火墙在丢弃它们，而不是Web服务器宕机。如果nginx只是被停止了，你会得到像8080那样的快速RST，浏览器会显示`ERR_CONNECTION_REFUSED`而不是`ERR_TIMED_OUT`。

所以服务器是活的，SSH正常工作，但有什么东西在显式丢弃Web流量。

## DNS已修复——那部分生效了

```
www.funlive.io.  600  IN  A  34.150.108.243   ✅（Google和Cloudflare一致）
```

你的`ERR_TIMED_OUT`（不是NXDOMAIN）确认`www`现在能正确解析。故障从DNS转移到了防火墙。

**然而，根域名仍然有两条记录：**

```
funlive.io.  600  IN  A  34.150.108.243
funlive.io.  600  IN  A  162.255.119.114    ← 仍然存在，删除这条
```

你已解决了`www`的NXDOMAIN问题，但还没有删除Namecheap的URL转发记录。

## 需要检查的内容

我无法SSH进入验证——以下是两个需要检查的地方：

**1. GCP VPC防火墙**（最可能的原因）。前往Compute Engine → VM → Firewall rules，或检查标签是否不匹配：

```bash
gcloud compute firewall-rules list --format="table(name,allowed[].map().firewall_rule().list(),sourceRanges.list(),targetTags.list())"
```

你需要一条允许来自`0.0.0.0/0`的`tcp:80`和`tcp:443`的入站规则，**并且**VM必须带有该规则选择的target tag。规则存在但VM缺少对应的网络标签，正是导致这种症状的经典原因。

**2. 主机防火墙**——由于80/443被丢弃而8080能透过到内核，主机级别的规则可能专门针对Web端口：

```bash
sudo ufw status verbose          # 如果显示"deny"入站，就是这个原因
sudo iptables -L INPUT -n -v | head -30
sudo ss -tlnp | grep -E ':80|:443'
```

如果`ss`显示80/443没有任何监听，你需要同时启动Web服务器**和**修复防火墙——两者都需要。

**关于之前的502说明：**你的本地代理（`127.0.0.1:7890`）对任何不可达的主机都返回相同的502——我确认过它对黑洞IP产生相同的头部签名。所以502和超时是同一个根本问题：Web端口不可达，只是不同路径下的错误文本不同。

打开防火墙后测试：`curl -I http://34.150.108.243/`应该返回带有`Server:`头的真实状态行，而不是代理的空502。
