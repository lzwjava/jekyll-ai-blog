---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS Shell 命令
translated: true
type: note
---

以下是 200 个常用的 macOS shell 命令，已分类整理以便查阅。这些命令在文件系统导航、文件管理、系统监控等方面非常实用。

### 文件系统导航

- `ls` - 列出目录内容
- `cd` - 切换当前目录
- `pwd` - 显示当前工作目录路径
- `tree` - 以树状图显示目录结构（需安装）

### 文件操作

- `cp` - 复制文件或目录
- `mv` - 移动或重命名文件/目录
- `rm` - 删除文件或目录
- `touch` - 创建空文件或更新时间戳
- `mkdir` - 创建新目录
- `rmdir` - 删除空目录
- `ln` - 创建硬链接和符号链接
- `chmod` - 修改文件权限
- `chown` - 修改文件所有者和所属组
- `cat` - 连接并显示文件内容
- `less` - 分页查看文件内容
- `more` - 分页查看文件内容
- `head` - 显示文件开头部分
- `tail` - 显示文件末尾部分
- `nano` - 编辑文本文件
- `vi` - 编辑文本文件
- `vim` - 编辑文本文件（vi增强版）
- `find` - 在目录树中搜索文件
- `locate` - 快速按名称查找文件
- `grep` - 使用模式匹配搜索文本
- `diff` - 逐行比较文件差异
- `file` - 检测文件类型
- `stat` - 显示文件状态信息
- `du` - 估算文件空间使用量
- `df` - 报告文件系统磁盘空间使用情况
- `dd` - 转换和复制文件
- `tar` - 打包/解包归档文件
- `gzip` - 压缩/解压缩文件
- `gunzip` - 解压gzip压缩的文件
- `zip` - 打包压缩为ZIP格式
- `unzip` - 解压ZIP归档文件
- `rsync` - 远程文件同步工具
- `scp` - 安全跨主机复制文件
- `curl` - 数据传输工具
- `wget` - 网络文件下载工具

### 系统信息

- `uname` - 打印系统信息
- `top` - 显示系统进程
- `htop` - 交互式进程查看器（需安装）
- `ps` - 显示当前进程快照
- `kill` - 向进程发送信号
- `killall` - 按进程名终止进程
- `bg` - 将作业置于后台运行
- `fg` - 将作业置于前台运行
- `jobs` - 显示作业列表
- `nice` - 调整程序运行优先级
- `renice` - 修改运行中进程的优先级
- `time` - 统计命令执行时间
- `uptime` - 显示系统运行时长
- `who` - 显示已登录用户
- `w` - 显示已登录用户及活动
- `whoami` - 显示当前用户名
- `id` - 显示用户身份信息
- `groups` - 显示用户所属组
- `passwd` - 修改用户密码
- `sudo` - 以其他用户身份执行命令
- `su` - 切换用户身份
- `chroot` - 切换根目录环境
- `hostname` - 显示或设置主机名
- `ifconfig` - 配置网络接口
- `ping` - 向网络主机发送ICMP回显请求
- `traceroute` - 跟踪网络路由路径
- `netstat` - 显示网络统计信息
- `route` - 显示/操作IP路由表
- `dig` - DNS查询工具
- `nslookup` - 交互式DNS查询
- `host` - DNS查询工具
- `ftp` - 文件传输程序
- `ssh` - SSH客户端
- `telnet` - Telnet客户端
- `nc` - 网络调试工具
- `iftop` - 显示网络接口带宽使用（需安装）
- `nmap` - 网络扫描和安全审计工具（需安装）

### 磁盘管理

- `mount` - 挂载文件系统
- `umount` - 卸载文件系统
- `fdisk` - 磁盘分区工具
- `mkfs` - 创建文件系统
- `fsck` - 检查修复文件系统
- `df` - 报告磁盘空间使用
- `du` - 估算文件空间使用
- `sync` - 同步缓存数据到存储设备
- `dd` - 转换和复制文件
- `hdparm` - 硬盘参数设置
- `smartctl` - SMART磁盘监控工具（需安装）

### 软件包管理

- `brew` - Homebrew包管理器（需安装）
- `port` - MacPorts包管理器（需安装）
- `gem` - RubyGems包管理器
- `pip` - Python包安装工具
- `npm` - Node.js包管理器
- `cpan` - Perl包管理器

### 文本处理

- `awk` - 文本模式扫描处理语言
- `sed` - 流文本编辑器
- `sort` - 文本行排序
- `uniq` - 报告或忽略重复行
- `cut` - 截取文件列内容
- `paste` - 合并文件行内容
- `join` - 基于相同字段合并文件
- `tr` - 字符替换/删除工具
- `iconv` - 字符编码转换
- `strings` - 提取文件中的可打印字符串
- `wc` - 统计文件行数/词数/字节数
- `nl` - 为文件添加行号
- `od` - 以多种格式导出文件
- `xxd` - 生成十六进制转储

### Shell脚本

- `echo` - 输出文本行
- `printf` - 格式化输出
- `test` - 条件表达式测试
- `expr` - 表达式求值
- `read` - 读取标准输入
- `export` - 设置环境变量
- `unset` - 删除变量或函数
- `alias` - 创建命令别名
- `unalias` - 删除命令别名
- `source` - 在当前shell执行文件
- `exec` - 执行命令
- `trap` - 信号捕获处理
- `set` - 设置shell选项
- `shift` - 移动位置参数
- `getopts` - 解析位置参数
- `type` - 显示命令类型
- `which` - 定位命令路径
- `whereis` - 查找命令相关文件

### 开发工具

- `gcc` - GNU C/C++编译器
- `make` - 项目构建工具
- `cmake` - 跨平台构建系统
- `autoconf` - 自动配置脚本生成器
- `automake` - Makefile生成工具
- `ld` - GNU链接器
- `ar` - 静态库管理工具
- `nm` - 目标文件符号查看器
- `objdump` - 目标文件信息查看器
- `strip` - 去除符号表
- `ranlib` - 生成静态库索引
- `gdb` - GNU调试器
- `lldb` - LLVM调试器
- `valgrind` - 内存调试工具（需安装）
- `strace` - 系统调用跟踪工具（需安装）
- `ltrace` - 库调用跟踪工具（需安装）
- `perf` - 系统性能分析工具
- `time` - 命令执行时间统计
- `xargs` - 标准输入构建命令行
- `m4` - 宏处理器
- `cpp` - C预处理器
- `flex` - 词法分析器生成器
- `bison` - 语法分析器生成器
- `bc` - 高精度计算器
- `dc` - 逆波兰式计算器

### 版本控制

- `git` - 分布式版本控制系统
- `svn` - Subversion版本控制系统
- `hg` - Mercurial版本控制系统
- `cvs` - 并发版本系统

### 其他工具

- `man` - 查看手册页
- `info` - 查看Info文档
- `apropos` - 搜索手册页描述
- `whatis` - 显示命令简要说明
- `history` - 查看命令历史
- `yes` - 重复输出字符串
- `cal` - 显示日历
- `date` - 显示/设置系统时间
- `sleep` - 延时等待
- `watch` - 定期执行命令并全屏显示
- `xargs` - 标准输入构建命令行
- `seq` - 生成数字序列
- `shuf` - 生成随机序列
- `tee` - 双向数据流重定向
- `tput` - 终端功能控制
- `stty` - 终端设置
- `clear` - 清屏
- `reset` - 重置终端
- `script` - 终端会话记录
- `wall` - 向所有用户发送消息
- `write` - 向指定用户发送消息
- `mesg` - 控制终端写入权限
- `talk` - 用户间对话工具
- `ytalk` - 多用户对话工具（需安装）
- `crontab` - 定时任务管理
- `at` - 单次定时任务
- `batch` - 批处理任务调度
- `nice` - 调整运行优先级
- `renice` - 修改运行中进程优先级
- `time` - 命令执行时间统计
- `ulimit` - 用户资源限制
- `pr` - 文本格式化打印
- `lp` - 打印文件
- `lpr` - 打印文件
- `lpq` - 查看打印队列
- `lprm` - 移除打印任务
- `enscript` - 带语法高亮的文本转换工具（需安装）
- `a2ps` - ASCII转PostScript工具
- `ps2pdf` - PostScript转PDF
- `pdf2ps` - PDF转PostScript
- `gs` - PostScript解释器
- `convert` - 图像格式转换（需安装）
- `mogrify` - 图像批处理工具（需安装）
- `exiftool` - 元数据编辑工具（需安装）
- `jpegoptim` - JPEG优化工具（需安装）
- `optipng` - PNG优化工具（需安装）

这些命令涵盖了广泛的功能，对于希望通过终端高效管理和操作macOS系统的用户来说至关重要。
