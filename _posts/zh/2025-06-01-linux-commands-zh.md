---
audio: false
generated: true
lang: zh
layout: post
title: 最实用的100个Linux命令
translated: true
type: note
---

根据您作为一位高度技术型、自学成才的全栈工程师背景，熟悉Linux环境、算法问题解决，并精通云平台、容器和分布式系统，我为您量身定制了这份**100个实用Linux命令**清单，专用于**Ubuntu**系统。这些命令的选择契合您在全栈开发、移动工程、机器学习和系统管理方面的专业经验，同时支持您的自学研究及开源贡献。它们涵盖文件管理、系统监控、网络、开发、自动化和高级脚本编写，与您在TEKsystems的工作、过往职务及个人项目息息相关。

命令按类别清晰分组，附有简要说明，着重强调对您技能组合的实际应用。我优先选择了能提升生产力、调试效率和系统优化能力的命令，假设您熟悉基于终端的工作流，并可能将这些命令用于开发、部署或研究任务。如果您需要，我可以提供特定命令的示例或脚本，或根据您的工作流（如开发与系统管理任务）生成命令使用频率图表。请随时告知！

### **文件与目录管理（15个命令）**

1. **ls** - 列出目录内容（`ls -la`查看详细信息及隐藏文件）
2. **cd** - 切换目录（`cd ~/projects`导航至GitHub项目文件夹）
3. **pwd** - 显示当前工作目录（适用于脚本编写或路径验证）
4. **mkdir** - 创建目录（`mkdir -p src/main/java`创建嵌套项目结构）
5. **rm** - 删除文件或目录（`rm -rf temp/`递归删除）
6. **cp** - 复制文件/目录（`cp -r src/ backup/`项目备份）
7. **mv** - 移动/重命名文件（`mv old.java new.java`代码重构）
8. **touch** - 创建空文件（`touch script.sh`新建脚本）
9. **find** - 搜索文件（`find / -name "*.java"`定位源文件）
10. **locate** - 快速按名称查找文件（`locate config.yaml`查找配置）
11. **du** - 估算磁盘使用量（`du -sh /var/log`检查日志大小）
12. **df** - 显示磁盘空间（`df -h`人性化格式显示）
13. **ln** - 创建链接（`ln -s /path/to/project symlink`创建快捷方式）
14. **chmod** - 修改文件权限（`chmod 755 script.sh`设置可执行脚本）
15. **chown** - 修改文件属主（`chown user:group file`部署时使用）

### **文本处理与操作（15个命令）**

16. **cat** - 显示文件内容（`cat log.txt`快速查看日志）
17. **less** - 交互式查看文件（`less server.log`浏览大型日志）
18. **more** - 分页显示文件输出（`more README.md`查看文档）
19. **head** - 显示文件开头行（`head -n 10 data.csv`数据预览）
20. **tail** - 显示文件末尾行（`tail -f app.log`实时日志监控）
21. **grep** - 搜索文本模式（`grep -r "error" /var/log`调试用）
22. **awk** - 处理文本列（`awk '{print $1}' access.log`日志解析）
23. **sed** - 流编辑器（`sed 's/old/new/g' file`文本替换）
24. **cut** - 提取行中字段（`cut -d',' -f1 data.csv`处理CSV）
25. **sort** - 排序行（`sort -n data.txt`数值排序）
26. **uniq** - 去除重复行（`sort file | uniq`提取唯一项）
27. **wc** - 统计行数/词数/字符数（`wc -l code.java`代码行数）
28. **tr** - 字符转换（`tr '[:lower:]' '[:upper:]' < file`大小写转换）
29. **tee** - 同时输出到文件与标准输出（`cat input | tee output.txt`记录日志）
30. **diff** - 比较文件差异（`diff old.java new.java`代码变更）

### **系统监控与性能（15个命令）**

31. **top** - 交互式系统进程监控（实时CPU/内存使用情况）
32. **htop** - 增强型进程查看器（`htop`更佳可视化）
33. **ps** - 列出进程（`ps aux | grep java`查看Java应用）
34. **free** - 查看内存使用（`free -m`以MB为单位）
35. **vmstat** - 虚拟内存统计（`vmstat 1`持续更新）
36. **iostat** - 监控I/O性能（`iostat -x`磁盘统计）
37. **uptime** - 显示系统运行时间及负载（`uptime`快速检查）
38. **lscpu** - 显示CPU信息（`lscpu`查看系统规格）
39. **lsblk** - 列出块设备（`lsblk`磁盘/分区详情）
40. **iotop** - 按进程监控磁盘I/O（`iotop`性能调试）
41. **netstat** - 网络统计（`netstat -tuln`查看监听端口）
42. **ss** - netstat现代替代品（`ss -tuln`查看套接字）
43. **dmesg** - 查看内核消息（`dmesg | grep error`系统问题排查）
44. **sar** - 收集系统活动数据（`sar -u 1`CPU监控）
45. **pmap** - 进程内存映射（`pmap -x <pid>`内存调试）

### **网络与连接（15个命令）**

46. **ping** - 测试网络连通性（`ping google.com`可达性测试）
47. **curl** - 获取URL数据（`curl -X POST api`API测试）
48. **wget** - 下载文件（`wget file.tar.gz`项目依赖）
49. **netcat** - 网络工具（`nc -l 12345`简易服务器）
50. **ifconfig** - 网络接口信息（`ifconfig eth0`IP详情）
51. **ip** - 现代网络配置（`ip addr`接口详情）
52. **nslookup** - DNS查询（`nslookup domain.com`DNS调试）
53. **dig** - 详细DNS查询（`dig domain.com`DNS记录）
54. **traceroute** - 追踪网络路径（`traceroute google.com`路由追踪）
55. **telnet** - 测试端口连通性（`telnet localhost 8080`服务测试）
56. **scp** - 安全复制文件（`scp file user@server:/path`文件传输）
57. **rsync** - 高效文件同步（`rsync -avz src/ dest/`备份用）
58. **ufw** - 管理防火墙（`ufw allow 80`Web服务器访问）
59. **iptables** - 配置防火墙规则（`iptables -L`规则列表）
60. **nmap** - 网络扫描（`nmap localhost`开放端口扫描）

### **开发与脚本编写（15个命令）**

61. **gcc** - 编译C程序（`gcc -o app code.c`构建应用）
62. **javac** - 编译Java代码（`javac Main.java`Java项目）
63. **java** - 运行Java程序（`java -jar app.jar`执行应用）
64. **python3** - 运行Python脚本（`python3 script.py`机器学习任务）
65. **node** - 运行Node.js（`node app.js`JavaScript项目）
66. **npm** - 管理Node包（`npm install`前端依赖）
67. **git** - 版本控制（`git commit -m "update"`GitHub仓库）
68. **make** - 构建项目（`make -f Makefile`自动化构建）
69. **mvn** - Maven构建工具（`mvn package`Java项目）
70. **gradle** - Gradle构建工具（`gradle build`Android项目）
71. **docker** - 管理容器（`docker run -p 8080:8080 app`部署用）
72. **kubectl** - 管理Kubernetes（`kubectl get pods`集群管理）
73. **virtualenv** - Python虚拟环境（`virtualenv venv`机器学习）
74. **gdb** - 调试程序（`gdb ./app`C/Java调试）
75. **strace** - 追踪系统调用（`strace -p <pid>`调试用）

### **软件包管理（10个命令）**

76. **apt** - 软件包管理器（`apt install vim`安装软件）
77. **apt-get** - 高级包管理工具（`apt-get upgrade`系统更新）
78. **dpkg** - 管理.deb包（`dpkg -i package.deb`手动安装）
79. **apt-cache** - 查询包信息（`apt-cache search java`包搜索）
80. **snap** - 管理snap包（`snap install code`安装VS Code）
81. **update-alternatives** - 管理默认应用（`update-alternatives --config java`）
82. **add-apt-repository** - 添加PPA（`add-apt-repository ppa:repo`软件源）
83. **apt-file** - 查找包文件（`apt-file search /bin/bash`调试用）
84. **dpkg-query** - 查询已安装包（`dpkg-query -l`包列表）
85. **apt-mark** - 标记软件包（`apt-mark hold package`防止升级）

### **系统管理与安全（15个命令）**

86. **sudo** - 以root权限运行命令（`sudo apt update`管理任务）
87. **su** - 切换用户（`su - user`切换账户）
88. **passwd** - 修改密码（`passwd user`安全设置）
89. **useradd** - 添加用户（`useradd -m dev`新建账户）
90. **usermod** - 修改用户（`usermod -aG sudo dev`权限设置）
91. **groupadd** - 创建用户组（`groupadd developers`访问控制）
92. **chgrp** - 修改组所有权（`chgrp -R dev /project`团队协作）
93. **crontab** - 计划任务（`crontab -e`自动化脚本）
94. **systemctl** - 管理服务（`systemctl start nginx`Web服务器）
95. **journalctl** - 查看系统日志（`journalctl -u docker`服务日志）
96. **who** - 列出登录用户（`who`服务器监控）
97. **last** - 显示登录历史（`last`安全审计）
98. **shutdown** - 关机（`shutdown -h now`系统关机）
99. **reboot** - 重启系统（`reboot`更新后重启）
100. **env** - 显示环境变量（`env | grep PATH`调试用）

### **针对您背景的特别说明**

- **开发侧重**：`git`、`mvn`、`docker`和`kubectl`等命令契合您的全栈和容器化工作流，特别适用于您10个GitHub项目及云平台经验（AWS、Azure、阿里云）
- **调试与性能**：包含`strace`、`gdb`、`htop`和`dmesg`等工具，满足您后端和系统调试需求（基于8年后端经验）
- **网络功能**：`curl`、`netcat`和`nmap`等命令支持您的API和网络专业知识，适用于微服务或云部署测试
- **自动化**：`crontab`和`rsync`便于自动化备份或部署，与您的自由职业和企业角色相关
- **研究与学习**：文本处理工具（`grep`、`awk`、`sed`）适用于解析日志或数据集，支持您在视觉恢复领域的自学研究

如需深入了解任何类别（如`awk`或`sed`脚本示例、Docker工作流或云特定命令），或需要可视化命令使用频率的图表（按任务类型分类），请随时告知！您也可以查看GitHub作品集获取项目相关命令，或分享当前TEKsystems任务详情以获取更精准的建议。
