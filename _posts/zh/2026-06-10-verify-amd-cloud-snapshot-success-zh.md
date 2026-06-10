---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 验证AMD云快照成功
translated: true
type: note
---

问题：在 AMD Developer Cloud 中创建快照时，如何在依赖它之前验证它确实成功了——以免丢失工作并需要重新进行设置？

答案：

核心问题：UI 中出现快照行**并不**意味着该快照是可恢复的。基于 DigitalOcean 的 API（AMD Dev Cloud 运行在 DO 衍生堆栈上）通过状态标记快照，其中只有一种状态是安全的。

通过轮询操作和快照状态进行验证——永远不要只相信 UI 列表。

```bash
# 一次性设置这些变量
export DO_TOKEN="<API_KEY>"
DROPLET_ID=574444990   # 你的 MI300X 实例

API="https://api.digitalocean.com/v2"
AUTH=(-H "Authorization: Bearer $DO_TOKEN" -H "Content-Type: application/json")
```

触发快照并捕获操作 ID——这是你真正需要监控的对象：

```bash
ACTION_ID=$(curl -s -X POST "${API}/droplets/${DROPLET_ID}/actions" \
  "${AUTH[@]}" \
  -d '{"type":"snapshot","name":"mi300x-'"$(date +%Y%m%d-%H%M%S)"'"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"]["id"])')

echo "操作: $ACTION_ID"
```

持续轮询直到操作状态变为 `completed`（不是 `in-progress`，并且一定要捕获 `errored`）：

```bash
while true; do
  STATUS=$(curl -s "${API}/actions/${ACTION_ID}" "${AUTH[@]}" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"]["status"])')
  echo "$(date +%T) -> $STATUS"
  case "$STATUS" in
    completed) echo "✅ 快照操作已完成"; break ;;
    errored)   echo "❌ 快照失败——不要删除源，重新运行"; exit 1 ;;
    *)         sleep 20 ;;
  esac
done
```

操作完成是必要但还不够的条件。确认快照存在、大小非零，并且报告的大小对于一个 192GB 的机器来说是合理的（你现有的快照约为 133GB）：

```bash
curl -s "${API}/droplets/${DROPLET_ID}/snapshots" "${AUTH[@]}" \
  | python3 -c '
import sys, json
snaps = json.load(sys.stdin)["snapshots"]
latest = sorted(snaps, key=lambda s: s["created_at"])[-1]
gb = latest["size_gigabytes"]
print(f'\''名称={latest["name"]} 大小={gb}GB 区域={latest["regions"]}'\'')
assert gb and gb > 1, "❌ 大小为零或过小——快照无效，重新制作"
assert latest["regions"], "❌ 未附加区域——不可恢复"
print("✅ 快照看起来可恢复")
'
```

可随时重新运行的单行健康检查：

```bash
curl -s "${API}/droplets/${DROPLET_ID}/snapshots" "${AUTH[@]}" \
  | python3 -c 'import sys,json;[print(s["name"],s["size_gigabytes"],"GB",s["created_at"]) for s in json.load(sys.stdin)["snapshots"]]'
```

三个表示“可以安全删除并稍后重建”的门槛条件：

1. 操作状态 `status == completed`（不仅仅是已提交）
2. 快照出现在 `/snapshots` 中，且 `size_gigabytes > 0`
3. `regions` 非空（没有区域的快照无法用于创建实例）

在 MI300X 机器上一个实际需要注意的问题：快照要求实例处于静止状态。如果你有正在运行的 ROCm 进程或 HBM 相关工作流中存在大量脏页，请先同步并最好关机以确保磁盘映像一致：

```bash
sync && sync
# 可选但最安全的做法以获得干净映像：
# sudo poweroff   # 然后通过 API 对已关机的实例进行快照
```

将整个过程封装起来，这样你就不会在误报的情况下继续操作：

```bash
snapshot_safe() {
  local id=$1 name=$2
  local aid=$(curl -s -X POST "${API}/droplets/${id}/actions" "${AUTH[@]}" \
    -d "{\"type\":\"snapshot\",\"name\":\"${name}\"}" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["id"])')
  while :; do
    local st=$(curl -s "${API}/actions/${aid}" "${AUTH[@]}" \
      | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["status"])')
    [ "$st" = completed ] && break
    [ "$st" = errored ] && { echo "失败"; return 1; }
    sleep 20
  done
  curl -s "${API}/droplets/${id}/snapshots" "${AUTH[@]}" \
    | python3 -c 'import sys,json;s=sorted(json.load(sys.stdin)["snapshots"],key=lambda x:x["created_at"])[-1];import os;os._exit(0 if s["size_gigabytes"]>1 and s["regions"] else 1)' \
    && echo "✅ 已验证" || { echo "❌ 未验证"; return 1; }
}
```

只有在 `snapshot_safe` 返回 0 之后，才应该销毁实例以停止大约 2 美元/小时的费用消耗。

一个注意事项：AMD Dev Cloud 可能不会在 `api.digitalocean.com` 暴露完整的 DigitalOcean 公共 API——可能是一个单独的端点或令牌范围。请检查其仪表板/文档中的实际基础 URL；如果 API 不可达，则相同的逻辑需要手动应用：刷新快照列表，确认大小在预期的 ~130GB+ 范围内，并且不要在执行清理之前（直到它显示为实际的尺寸）才进行。
