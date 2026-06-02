---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 主要升级期间 GNOME 移除
translated: true
type: note
---

**是的，在 Ubuntu 主版本升级过程中，这绝对可能发生。** 以下是为什么以及如何发生的全面解释：

---

## 在 Ubuntu 22 → 24 升级过程中 GNOME 被卸载的原因

### 1. 软件包过渡和重命名的元包

在运行 `do-release-upgrade` 时，升级工具 (`ubuntu-release-upgrader`) 会解析发布版之间的依赖树。如果发生以下任何情况，桌面软件包可能会被移除：

- **元包冲突**：24.04 中的 `ubuntu-desktop` 可能具有与 22.04 不同的依赖项或过渡软件包名称
- **已保留的软件包**：如果您之前保留了任何 GNOME 相关的软件包 (`apt-mark hold`)，解析器可能会选择移除依赖软件包而不是升级它们
- **第三方 PPA**：提供修补 GNOME 软件包的 PPA 可能会导致冲突，从而导致解析器完全移除冲突的软件包

### 2. “Autoremove” 级联效应

Ubuntu 的升级过程会将许多软件包标记为“自动安装”。如果像 `ubuntu-desktop` 这样的元包被移除或替换，其所有自动安装的依赖项就会成为孤儿并符合自动移除条件。这会产生级联效应：

```
ubuntu-desktop removed
  → gdm3 marked for removal
    → gnome-shell marked for removal
      → gnome-session marked for removal
        → gnome-settings-daemon marked for removal
```

### 3. `rc` 状态是关键证据

`gdm3`、`gnome-shell` 和 `gnome-settings-daemon` 上的 `rc` 状态（已移除，但保留配置）确认这些软件包是由**包管理器干净地移除的**——不是损坏。这是一种受控移除，而不是崩溃。

### 4. `active (exited)` 的 GDM3 陷阱

这是一个特别令人困惑的症状。以下是流程：

```
systemd starts gdm3 service
  → triggers /etc/init.d/gdm3 (SysV compat)
    → script checks: test -x /usr/sbin/gdm3
      → binary missing → exits 0 (success!)
        → systemd reports: active (exited) ✓
```

服务看起来是健康的，但实际上什么都没做。结合 `graphical.target` 仍是默认目标且 `/etc/X11/default-display-manager` 仍指向缺失的二进制文件，系统会静默引导到 TTY 而不会记录任何错误。

---

## 如何在未来升级中防止这种情况

- **升级前**，手动安装元包：`sudo apt install ubuntu-desktop`
- **运行 `do-release-upgrade` 前禁用所有 PPA**
- **检查已保留的软件包**：`apt-mark showhold`
- **仔细审查升级摘要**——安装程序会显示要移除的软件包；注意 `gdm3`、`gnome-shell`、`ubuntu-desktop`

---

## 恢复

如已确认，修复方法很简单：

```bash
sudo apt install ubuntu-desktop
sudo reboot
```

这会重新安装完整的元包，拉回 GDM3、GNOME Shell 及其所有依赖项，并在下次启动时恢复图形登录。

参考资料：

- [Ubuntu Release Upgrade — Official Docs](https://ubuntu.com/server/docs/upgrade-introduction)
- [Ubuntu 24.04 LTS Release Notes](https://discourse.ubuntu.com/t/noble-numbat-release-notes/39890)
- [Debian Package Status Fields (`rc`, `ii`, etc.)](https://www.debian.org/doc/manuals/debian-faq/pkg-basics.en.html)
