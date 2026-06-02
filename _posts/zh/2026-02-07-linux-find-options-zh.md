---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 精通 Linux Find 命令选项
translated: true
type: note
---

`find` 命令是 Unix/Linux 中用于搜索文件和目录最强大的工具之一。以下是关于其选项和功能的详尽指南。

## Basic Syntax

```bash
find [path...] [expression]
```

## Starting Points and Paths

你可以指定一个或多个起始目录：

```bash
find /home /var /tmp -name "*.log"    # 搜索多个目录
find . -name "file.txt"                # 当前目录
find / -name "config"                  # 整个文件系统
```

## Tests and Filters

**基于名称的搜索：**

- `-name pattern` - 区分大小写的名称匹配（支持通配符）
- `-iname pattern` - 不区分大小写的名称匹配
- `-path pattern` - 匹配完整路径
- `-ipath pattern` - 不区分大小写的路径匹配
- `-regex pattern` - 使用 regular expression 匹配路径
- `-iregex pattern` - 不区分大小写的 regex

```bash
find . -name "*.txt"
find . -iname "README*"
find . -regex ".*\.(jpg|png|gif)"
```

**基于类型的搜索：**

- `-type f` - 普通文件
- `-type d` - 目录
- `-type l` - Symbolic links
- `-type b` - Block devices
- `-type c` - Character devices
- `-type p` - Named pipes (FIFOs)
- `-type s` - Sockets

```bash
find /var -type d -name "log*"
find . -type f -name "*.sh"
```

**基于大小的搜索：**

- `-size n[cwbkMG]` - 文件大小 (c=bytes, w=2-byte words, b=512-byte blocks, k=KB, M=MB, G=GB)
- 使用 `+` 表示大于，`-` 表示小于，无前缀表示精确匹配

```bash
find . -size +100M              # 大于 100MB
find . -size -1k                # 小于 1KB
find /var/log -size +50M -size -100M  # 介于 50-100MB 之间
```

**基于时间的搜索：**

- `-mtime n` - n 天前修改过
- `-atime n` - n 天前访问过
- `-ctime n` - n 天前状态改变过
- `-mmin n` - n 分钟前修改过
- `-amin n` - n 分钟前访问过
- `-cmin n` - n 分钟前状态改变过
- `-newer file` - 比指定文件更新
- `-newerXY reference` - 更灵活的时间比较

```bash
find . -mtime -7                # 过去 7 天内修改过
find . -mtime +30               # 超过 30 天前修改过
find . -mmin -60                # 过去 1 小时内修改过
find . -newer reference.txt     # 比 reference.txt 更新
```

**基于权限的搜索：**

- `-perm mode` - 精确匹配权限
- `-perm -mode` - 包含所有指定的权限位
- `-perm /mode` - 包含任一指定的权限位

```bash
find . -perm 644                # 精确为 644
find . -perm -644               # 至少为 644
find /bin -perm /u+s,g+s        # 设置了 SUID 或 SGID
```

**基于所有权的搜索：**

- `-user name` - 属于该用户
- `-group name` - 属于该组
- `-uid n` - 属于该用户 ID
- `-gid n` - 属于该组 ID
- `-nouser` - 无有效属主
- `-nogroup` - 无有效属组

```bash
find /home -user john
find . -nouser                  # 查找孤儿文件
```

**深度控制：**

- `-maxdepth n` - 最多向下搜索 n 层
- `-mindepth n` - 至少从第 n 层开始搜索
- `-depth` - 在处理目录本身之前先处理目录内容

```bash
find . -maxdepth 2 -name "*.txt"
find . -mindepth 3 -type f
```

**其他实用测试：**

- `-empty` - 空文件或目录
- `-executable` - 可执行文件
- `-readable` - 可读文件
- `-writable` - 可写文件
- `-links n` - 具有 n 个 hard links 的文件
- `-inum n` - inode 编号为 n 的文件
- `-samefile name` - 指向相同 inode 的文件

```bash
find . -empty -type d           # 空目录
find /usr/bin -executable -type f
```

## Logical Operators

使用逻辑运算符组合测试：

- `-a` 或 `-and` - 逻辑与（若省略则默认为此项）
- `-o` 或 `-or` - 逻辑或
- `-not` 或 `!` - 逻辑非
- `( expression )` - 分组（在 shell 中需转义括号）

```bash
find . -name "*.txt" -o -name "*.md"
find . -type f -not -name "*.log"
find . \\( -name "*.c" -o -name "*.h" \\) -a -mtime -7
```

## Actions

**显示操作：**

- `-print` - 打印完整路径（默认）
- `-print0` - 以 null 分隔符打印（配合 xargs -0 使用更安全）
- `-printf format` - 自定义格式输出
- `-ls` - 以 ls -dils 格式列出
- `-fls file` - 类似 -ls 但写入文件

```bash
find . -name "*.txt" -print0
find . -printf "%p\t%s bytes\n"
```

**执行操作：**

- `-exec command {} \;` - 对每个文件执行命令
- `-exec command {} +` - 对多个文件批量执行命令
- `-execdir command {} \;` - 在文件所在目录执行
- `-ok command {} \;` - 类似 -exec 但会提示确认

```bash
find . -name "*.tmp" -exec rm {} \;
find . -type f -exec chmod 644 {} +
find . -name "*.jpg" -execdir convert {} {}.png \;
```

**删除：**

- `-delete` - 删除匹配的文件（请谨慎使用！）

```bash
find . -name "*.bak" -delete
find . -type f -empty -delete
```

**其他操作：**

- `-quit` - 在第一次匹配后立即退出
- `-prune` - 不进入该目录

```bash
find . -name ".git" -prune -o -type f -print
```

## Practical Examples

```bash
# 在 home 目录中查找大文件
find ~ -type f -size +500M -exec ls -lh {} \;

# 查找并压缩旧日志文件
find /var/log -name "*.log" -mtime +90 -exec gzip {} \;

# 查找损坏的 symbolic links
find . -type l ! -exec test -e {} \; -print

# 查找今天修改的文件
find . -type f -mtime 0

# 查找全网可写文件（安全检查）
find / -perm -002 -type f 2>/dev/null

# 查找 setuid 文件（安全审计）
find / -perm -4000 -type f 2>/dev/null

# 按扩展名统计文件数量
find . -type f | sed 's/.*\.//' | sort | uniq -c

# 查找重复的文件名
find . -type f -printf "%f\n" | sort | uniq -d

# 清理临时文件
find /tmp -type f -atime +7 -user $(whoami) -delete
```

## Performance Tips

- 将限制性最强的测试放在前面
- 尽早使用 `-maxdepth` 来限制搜索范围
- 使用 `-prune` 跳过不需要的目录
- 对包含空格的文件名使用 `-print0` 配对 `xargs -0`
- 重定向 stderr 以避免权限错误提示：`2>/dev/null`

`find` 命令极其灵活，可以通过管道和命令替换与其他 Unix 工具结合，创建强大的文件管理工作流。
