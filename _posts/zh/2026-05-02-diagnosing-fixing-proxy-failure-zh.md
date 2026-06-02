---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断与修复代理故障
translated: true
type: note
---

## 问题修复回顾

### 根因诊断 — 准确

日志明确指出：

```
dial tcp 5.223.42.176:19400: connect: connection refused
```

每次连接失败都指向 SS 1。通过 `journalctl` 输出直接定位问题是正确做法，无需猜测。

### REST API 切换代理 — 方法正确且快速

通过 `PUT /proxies/Proxy` 在运行时切换活动代理是恰当选择。无需重启，即刻生效，这正是 mihomo REST API 的设计用途。

### 配置文件重排序 — 思路正确但执行欠妥

意图正确：将 Hysteria2 设为默认代理，避免重启后回退。但 `sed` 实现方式存在缺陷：

```bash
# 此操作导致问题 — 两行命令包含重叠的字符串
sed -i 's/      - My SS 1/      - My Hysteria2 2/' ...
sed -i 's/      - My Hysteria2 2$/      - My SS 1/' ...
```

第二条 sed 命令在已修改的内容上运行，导致两行最终都变为 "My SS 1"。本应一开始就使用 Python 脚本，或直接手动写入正确配置。虽然 Python 修复方案最终奏效，但这属于额外增加的补救步骤。

### 未能优化的细节

**当前代理组类型为 `select`，而非 `fallback`。** 这意味着 mihomo 不会自动尝试第二个代理，仅使用手动选中的代理。因此：

- 若 Hysteria2 失效，流量将再次静默失败
- 用户仍需通过 API 或仪表板手动切换

更优的长期配置方案应为：

```yaml
proxy-groups:
  - name: "Proxy"
    type: fallback          # 支持故障自动切换
    url: http://cp.cloudflare.com/generate_204
    interval: 300
    proxies:
      - My Hysteria2 2
      - My SS 1
```

此配置会每 5 分钟对两个代理进行健康检查，并在主代理失效时自动切换。

### 总结

| 步骤 | 执行质量 |
|------|---------|
| 基于日志的诊断 | 良好 |
| 通过 REST API 运行时修复 | 良好 |
| 配置重排序思路 | 良好 |
| sed 命令执行 | 不佳 — 破坏了配置文件 |
| Python 修复方案 | 合格 |
| 未建议采用 `fallback` 分组 | 错过优化机会 |
