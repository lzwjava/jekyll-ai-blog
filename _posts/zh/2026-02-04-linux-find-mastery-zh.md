---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 精通 Linux Find 命令
translated: true
type: note
---

`find` 命令是 Linux 中搜索文件和 directory 最强大的工具之一。它根据你指定的标准在 directory 层级结构中进行递归搜索。

## Basic Syntax

```bash
find [path...] [expression]
```

## Common Use Cases

**按文件名搜索：**
```bash
find /path -name "filename.txt"
find /path -iname "*.pdf"  # case-insensitive
```

**按文件类型搜索：**
```bash
find /path -type f  # 仅限 files
find /path -type d  # 仅限 directories
find /path -type l  # symbolic links
```

**按大小搜索：**
```bash
find /path -size +100M  # 大于 100MB
find /path -size -1k    # 小于 1KB
find /path -size 50M    # 正好 50MB
```

**按修改时间搜索：**
```bash
find /path -mtime -7   # 最近 7 天内修改过
find /path -mtime +30  # 修改时间超过 30 天
find /path -mmin -60   # 最近 60 分钟内修改过
```

**按权限搜索：**
```bash
find /path -perm 644   # 正好为 644
find /path -perm -644  # 至少为 644
find /path -perm /u+w  # 用户具有写权限
```

**按所有者搜索：**
```bash
find /path -user username
find /path -group groupname
```

**结合逻辑运算符：**
```bash
find /path -name "*.log" -and -size +10M
find /path -name "*.txt" -or -name "*.md"
find /path -not -name "*.tmp"
find /path \\( -name "*.jpg" -or -name "*.png" \\) -and -size +1M
```

## Executing Commands on Results

**删除文件：**
```bash
find /path -name "*.tmp" -delete
find /path -name "*.log" -exec rm {} \;
```

**对每个文件执行命令：**
```bash
find /path -type f -exec chmod 644 {} \;
find /path -name "*.txt" -exec grep "pattern" {} \;
```

**对多个文件执行命令（更高效）：**
```bash
find /path -name "*.txt" -exec grep "pattern" {} +
```

**交互式确认：**
```bash
find /path -name "*.bak" -ok rm {} \;
```

## Advanced Options

**限制搜索深度：**
```bash
find /path -maxdepth 2 -name "*.txt"  # 仅搜索 2 层深度
find /path -mindepth 1 -name "*.txt"  # 跳过起始目录
```

**查找空文件或目录：**
```bash
find /path -empty
find /path -type f -empty  # 仅限空文件
```

**按访问/状态更改时间查找：**
```bash
find /path -atime -7   # 最近 7 天内访问过
find /path -ctime +30  # 状态更改超过 30 天
```

**查找比参考文件新/旧的文件：**
```bash
find /path -newer reference_file
find /path -not -newer reference_file
```

**搜索多个路径：**
```bash
find /path1 /path2 /path3 -name "*.conf"
```

**打印带有详细信息的结果：**
```bash
find /path -name "*.txt" -ls
find /path -name "*.txt" -printf "%p - %s bytes\n"
```

## Practical Examples

**查找并压缩旧的日志文件：**
```bash
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;
```

**在 home directory 中查找大文件：**
```bash
find ~ -type f -size +100M -exec ls -lh {} \; 2>/dev/null
```

**查找今天修改过的文件：**
```bash
find /path -type f -mtime 0
```

**查找重复的文件名：**
```bash
find /path -type f -printf "%f\n" | sort | uniq -d
```

**按扩展名查找并统计文件数量：**
```bash
find /path -type f -name "*.jpg" | wc -l
```

**查找所有人可写的文件（安全检查）：**
```bash
find /path -type f -perm -002
```

**查找 setuid 文件（安全检查）：**
```bash
find / -perm -4000 -type f 2>/dev/null
```

## Performance Tips

`find` 命令从左到右处理选项，因此为了获得更好的性能，请将最具限制性的标准放在前面。在表达式早期使用 `-name` 或 `-type`，并将类似 `-exec` 这样高开销的操作放在最后。

对于索引系统上的快速搜索，可以考虑使用 `locate` 进行简单的文件名搜索，尽管 `find` 提供了更多的灵活性，并且始终显示当前 filesystem 的状态。