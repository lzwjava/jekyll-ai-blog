---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu 24.04上运行Oracle XE
translated: true
type: note
---

这台笔记本电脑运行的是 **Ubuntu 24.04.4 LTS (x86_64)**，因此官方软件包中没有完全匹配的——但以下是详细分析：

| 选项 | 结论 |
|---|---|
| **Windows 64位** (`.zip`) | ❌ 你使用的是Linux，不是Windows。 |
| **Oracle Linux 8** (`.rpm`) | ✅ **最佳选择** — 这个RPM是你想在Ubuntu上尝试的。 |
| **RHEL 8 预安装RPM** | ❌ 仅作为补充包。 |

---

## 推荐方法

**在Ubuntu上安装OL8 RPM** — 这不是官方支持的，但这是最常用的方法。在此系统上：

1. **安装 `alien`** 以将 `.rpm` 转换为 `.deb`：
   ```bash
   sudo apt update && sudo apt install alien
   ```

2. **转换并安装**：
   ```bash
   alien --scripts -d oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm
   sudo dpkg -i oracle-database-xe-21c-1.0-1.ol8.x86_64.deb
   ```

3. **运行配置脚本**：
   ```bash
   sudo /etc/init.d/oracle-xe-21c configure
   ```

> ⚠️ **注意事项**：这是一个社区解决方案，并非官方支持。预计需要手动解决依赖问题（例如 `libaio1`、`bc`）。有些用户报告说使用 `rpm --nodeps` 加上手动链接修复比使用 `alien` 效果更好。

---

## 替代方案（推荐更简单的方法）

**在Docker中运行Oracle XE** — 完全避免操作系统兼容性问题：

```bash
docker run -d --name oracle21c \
  -p 1521:1521 -p 5500:5500 \
  -e ORACLE_PDB=XE \
  -e ORACLE_PWD=your_password \
  container-registry.oracle.com/database/express:21.3.0-xe
```

这在Ubuntu 24.04上运行良好，且更易于维护。

---

**总结**：如果你必须原生安装，请使用 **OL8 `.rpm`** 并借助 `alien`。但我建议改用 **Docker** — 这是在此系统上阻力最小的方式。