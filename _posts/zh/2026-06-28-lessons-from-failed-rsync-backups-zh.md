---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rsync备份失败的教训
translated: true
type: note
---

现在我掌握了全局情况。上次出错的原因如下：

**问题1：SSH连接中断（rsync错误码255）**

```
rsync error: unexplained error (code 255) at ... io.c(453) [sender=2.6.9]
```

SSH连接在传输过程中意外中断。原始的`backup.sh`没有设置`ServerAliveInterval`——当大文件传输（Projects约27GB）长时间运行时，控制通道上没有数据流动，路由器或操作系统会静默关闭TCP连接。rsync遇到管道断裂，退出并返回错误码255。

**问题2：rsync版本过旧（2.6.9）**
macOS自带的rsync是2006年的2.6.9版本。该版本存在已知问题：

- 处理深层嵌套目录中的符号链接时存在问题（node_modules包含数千个符号链接）
- 不支持`--timeout`参数来从传输停滞中恢复
- 错误报告能力不如现代rsync 3.x版本

**问题3：node_modules符号链接数量庞大**
包含node_modules的项目（如`admin-vue3-micro-qiankun`）有数以万计的符号链接。备份日志中充斥着符号链接相关的输出。rsync 2.6.9在处理这些文件时表现不佳——扫描速度慢、链接解析出错、在文件列表阶段连接超时。

**问题4：照片库体积过大，无法一次性传输**
照片库（`照片图库.photoslibrary`）约4GB，包含4,888个原始文件。首次尝试（backup.sh → fix_backup.sh）失败。修复脚本逐步演化：

- `fix_backup2.sh`——将照片库按子目录分批传输（resources、originals、private等）
- `fix_backup3.sh`——进一步将originals/目录按十六进制子目录（0-F）拆分，每个子目录包含266-338个文件
- 即便如此，`backup4.log`显示所有16个originals子目录都呈现`0 vs XXX INCOMPLETE`状态——传输显示"OK"，但校验发现远程端文件数为0。`--inplace`标志或路径不匹配导致了静默数据丢失。

**问题5：原始脚本未使用`--partial`标志**
没有`--partial`参数时，中断的rsync会删除已部分传输的文件。因此每次连接中断都需要从头开始重新传输该文件。启用`--partial`后，rsync会保留部分传输的文件并从中断处继续传输。

**问题6：缺少超时保护机制**
原始脚本没有设置`--timeout=N`参数。当网络出现停滞时，rsync会无限期挂起。修复脚本后续添加了`--timeout=300`和`--timeout=600`参数。

**当前的`mini-backup.sh`如何解决这些问题：**

- `ServerAliveInterval=30` + `ServerAliveCountMax=10`——每30秒发送一次保活探测，连续10次失败后断开连接
- `--partial`——从中断处继续传输文件
- `--timeout=300`——传输停滞时不会无限期挂起
- 对已有备份进行增量rsync——当前传输的数据量大大减少
- 通过`--exclude`跳过node_modules会更好，但当前脚本尚未实现这一点

需要我添加`--exclude='node_modules'`和`--exclude='.git'`来跳过最大的问题目录吗？
