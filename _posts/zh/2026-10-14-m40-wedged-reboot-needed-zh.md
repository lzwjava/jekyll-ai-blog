---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40卡死，需要重启
translated: true
type: note
---

我得在这里停下来，交给你处理：M40 现在**卡住了，需要重启**。

## 发生了什么

1. 解绑成功了，但 `rmmod nvidia` 失败了，因为 `gnome-shell` 和 `github-desktop` 占用了 `/dev/nvidia*`（nvidia 模块的引用计数为 36）。
2. 在设备半脱离状态下，`modprobe nouveau` 卡住了，而我重新绑定 `nvidia` 的尝试现在在内核中卡死：

   ```
   sh  D  device_driver_attach -> bind_store   (stuck >2 min)
   ```

3. 当前状态：M40 已解绑，没有 `/dev/dri/renderD128`，nouveau 未加载。**其他一切正常** —— 你的桌面和 Intel GPU 不受影响。

这只能通过重启来恢复。`nouveau` 仍被列入黑名单，因此 `nvidia` 驱动会在启动时自动恢复。

## 我做的修改，防止这种情况再次发生

`tools/muda-gpu-mode.sh` 现在会检查 nvidia 模块的引用计数，并在其被占用时**拒绝**切换，同时打印安全操作步骤。新增了 `--force` 选项（会先停止显示管理器）。已提交为 `368bb6b`。

## 我需要你做什么

重启以恢复 GPU：

```sh
sudo reboot
```

（或者让我来执行，但请先关闭未保存的工作 —— 我看不到你打开了什么）。

## 如果你想之后重试 nouveau

请从**文本控制台**进行操作，这样就没有东西占用 nvidia 设备：

```sh
# 按 Ctrl+Alt+F3，登录
cd ~/projects/muda
sudo systemctl isolate multi-user.target      # 退出 GUI 会话
sudo tools/muda-gpu-mode.sh nouveau
MUDA_DRIVER=nouveau ./build/mudainfo          # 粘贴此输出
MUDA_DRIVER=nouveau ./build/test_memory
sudo systemctl isolate graphical.target       # 或重启以恢复桌面
```

`--force` 标志会替你执行 `isolate multi-user.target` 这一步，但在 GUI 内执行会关闭你的会话。

对于这次卡死我很抱歉 —— 根本原因是桌面占用了 nvidia 设备，而原始脚本没有检查这一点。一旦你重启完成，请粘贴 nouveau 下 `mudainfo` 的输出，我会继续构建原生计算路径。
