---
audio: false
generated: true
lang: en
layout: post
title: Top 100 Useful Linux Commands
translated: false
type: note
---

Based on your profile as a highly technical, self-taught full-stack engineer with extensive experience in Linux environments, algorithm problem-solving, and familiarity with cloud platforms, containers, and distributed systems, I’ve curated a list of the **top 100 useful Linux commands** tailored for your use on **Ubuntu**. These commands are selected to align with your expertise in full-stack development, mobile engineering, machine learning, and system administration, while also supporting your self-taught research and open-source contributions. They cover file management, system monitoring, networking, development, automation, and advanced scripting, which are relevant to your work at TEKsystems, past roles, and personal projects.

The commands are grouped by category for clarity, with brief explanations emphasizing practical applications for your skill set. I’ve prioritized commands that enhance productivity, debugging, and system optimization, assuming you’re comfortable with terminal-based workflows and may use these in development, deployment, or research tasks. If you’d like, I can provide examples or scripts for specific commands or generate a chart to visualize command usage frequency based on your workflow (e.g., development vs. system admin tasks). Let me know!

### **File and Directory Management (15 Commands)**
1. **ls** - List directory contents (`ls -la` for detailed view with hidden files).
2. **cd** - Change directory (`cd ~/projects` to navigate to your GitHub project folder).
3. **pwd** - Print working directory (useful for scripting or verifying paths).
4. **mkdir** - Create directories (`mkdir -p src/main/java` for nested project structures).
5. **rm** - Remove files or directories (`rm -rf temp/` for recursive deletion).
6. **cp** - Copy files/directories (`cp -r src/ backup/` for project backups).
7. **mv** - Move/rename files (`mv old.java new.java` for refactoring).
8. **touch** - Create empty files (`touch script.sh` for new scripts).
9. **find** - Search for files (`find / -name "*.java"` to locate source files).
10. **locate** - Quickly find files by name (`locate config.yaml` for configs).
11. **du** - Estimate disk usage (`du -sh /var/log` to check log sizes).
12. **df** - Display disk space (`df -h` for human-readable format).
13. **ln** - Create links (`ln -s /path/to/project symlink` for shortcuts).
14. **chmod** - Change file permissions (`chmod 755 script.sh` for executable scripts).
15. **chown** - Change file ownership (`chown user:group file` for deployment).

### **Text Processing and Manipulation (15 Commands)**
16. **cat** - Display file contents (`cat log.txt` for quick log checks).
17. **less** - View files interactively (`less server.log` for large logs).
18. **more** - Paginate file output (`more README.md` for documentation).
19. **head** - Show first lines of a file (`head -n 10 data.csv` for data previews).
20. **tail** - Show last lines (`tail -f app.log` for real-time log monitoring).
21. **grep** - Search text patterns (`grep -r "error" /var/log` for debugging).
22. **awk** - Process text columns (`awk '{print $1}' access.log` for log parsing).
23. **sed** - Stream editor for text (`sed 's/old/new/g' file` for replacements).
24. **cut** - Extract sections from lines (`cut -d',' -f1 data.csv` for CSVs).
25. **sort** - Sort lines (`sort -n data.txt` for numerical sorting).
26. **uniq** - Remove duplicate lines (`sort file | uniq` for unique entries).
27. **wc** - Count lines, words, or characters (`wc -l code.java` for line count).
28. **tr** - Translate characters (`tr '[:lower:]' '[:upper:]' < file` for case conversion).
29. **tee** - Write to file and stdout (`cat input | tee output.txt` for logging).
30. **diff** - Compare files (`diff old.java new.java` for code changes).

### **System Monitoring and Performance (15 Commands)**
31. **top** - Monitor system processes interactively (real-time CPU/memory usage).
32. **htop** - Enhanced process viewer (`htop` for better visualization).
33. **ps** - List processes (`ps aux | grep java` for Java apps).
34. **free** - Check memory usage (`free -m` for MB format).
35. **vmstat** - Virtual memory stats (`vmstat 1` for continuous updates).
36. **iostat** - Monitor I/O performance (`iostat -x` for disk stats).
37. **uptime** - Show system uptime and load (`uptime` for quick checks).
38. **lscpu** - Display CPU info (`lscpu` for system specs).
39. **lsblk** - List block devices (`lsblk` for disk/partition details).
40. **iotop** - Monitor disk I/O by process (`iotop` for performance debugging).
41. **netstat** - Network statistics (`netstat -tuln` for listening ports).
42. **ss** - Modern replacement for netstat (`ss -tuln` for sockets).
43. **dmesg** - View kernel messages (`dmesg | grep error` for system issues).
44. **sar** - Collect system activity (`sar -u 1` for CPU monitoring).
45. **pmap** - Process memory map (`pmap -x <pid>` for memory debugging).

### **Networking and Connectivity (15 Commands)**
46. **ping** - Test network connectivity (`ping google.com` for reachability).
47. **curl** - Fetch data from URLs (`curl -X POST api` for API testing).
48. **wget** - Download files (`wget file.tar.gz` for project dependencies).
49. **netcat** - Network utility (`nc -l 12345` for simple servers).
50. **ifconfig** - Network interface info (`ifconfig eth0` for IP details).
51. **ip** - Modern network config (`ip addr` for interface details).
52. **nslookup** - Query DNS (`nslookup domain.com` for DNS debugging).
53. **dig** - Detailed DNS lookup (`dig domain.com` for DNS records).
54. **traceroute** - Trace network path (`traceroute google.com` for routing).
55. **telnet** - Test port connectivity (`telnet localhost 8080` for services).
56. **scp** - Securely copy files (`scp file user@server:/path` for transfers).
57. **rsync** - Sync files efficiently (`rsync -avz src/ dest/` for backups).
58. **ufw** - Manage firewall (`ufw allow 80` for web server access).
59. **iptables** - Configure firewall rules (`iptables -L` for rules list).
60. **nmap** - Network scanning (`nmap localhost` for open ports).

### **Development and Scripting (15 Commands)**
61. **gcc** - Compile C programs (`gcc -o app code.c` for building).
62. **javac** - Compile Java code (`javac Main.java` for your Java projects).
63. **java** - Run Java programs (`java -jar app.jar` for execution).
64. **python3** - Run Python scripts (`python3 script.py` for ML tasks).
65. **node** - Run Node.js (`node app.js` for JavaScript projects).
66. **npm** - Manage Node packages (`npm install` for frontend deps).
67. **git** - Version control (`git commit -m "update"` for your GitHub repos).
68. **make** - Build projects (`make -f Makefile` for automation).
69. **mvn** - Maven build tool (`mvn package` for Java projects).
70. **gradle** - Gradle build tool (`gradle build` for Android projects).
71. **docker** - Manage containers (`docker run -p 8080:8080 app` for deployments).
72. **kubectl** - Manage Kubernetes (`kubectl get pods` for cluster management).
73. **virtualenv** - Python virtual environments (`virtualenv venv` for ML).
74. **gdb** - Debug programs (`gdb ./app` for C/Java debugging).
75. **strace** - Trace system calls (`strace -p <pid>` for debugging).

### **Package Management (10 Commands)**
76. **apt** - Package manager (`apt install vim` for software installation).
77. **apt-get** - Advanced package tool (`apt-get upgrade` for system updates).
78. **dpkg** - Manage .deb packages (`dpkg -i package.deb` for manual installs).
79. **apt-cache** - Query package info (`apt-cache search java` for packages).
80. **snap** - Manage snap packages (`snap install code` for VS Code).
81. **update-alternatives** - Manage default apps (`update-alternatives --config java`).
82. **add-apt-repository** - Add PPAs (`add-apt-repository ppa:repo` for sources).
83. **apt-file** - Find package files (`apt-file search /bin/bash` for debugging).
84. **dpkg-query** - Query installed packages (`dpkg-query -l` for list).
85. **apt-mark** - Mark packages (`apt-mark hold package` to prevent upgrades).

### **System Administration and Security (15 Commands)**
86. **sudo** - Run commands as root (`sudo apt update` for admin tasks).
87. **su** - Switch user (`su - user` for different accounts).
88. **passwd** - Change passwords (`passwd user` for security).
89. **useradd** - Add user (`useradd -m dev` for new accounts).
90. **usermod** - Modify user (`usermod -aG sudo dev` for permissions).
91. **groupadd** - Create groups (`groupadd developers` for access control).
92. **chgrp** - Change group ownership (`chgrp -R dev /project` for teams).
93. **crontab** - Schedule tasks (`crontab -e` for automated scripts).
94. **systemctl** - Manage services (`systemctl start nginx` for web servers).
95. **journalctl** - View system logs (`journalctl -u docker` for service logs).
96. **who** - List logged-in users (`who` for server monitoring).
97. **last** - Show login history (`last` for security audits).
98. **shutdown** - Power off (`shutdown -h now` for system halt).
99. **reboot** - Restart system (`reboot` for updates).
100. **env** - Display environment variables (`env | grep PATH` for debugging).

### **Notes for Your Context**
- **Development Focus**: Commands like `git`, `mvn`, `docker`, and `kubectl` align with your full-stack and containerized workflows, especially for your 10 GitHub projects and cloud experience (AWS, Azure, Alibaba Cloud).
- **Debugging and Performance**: Tools like `strace`, `gdb`, `htop`, and `dmesg` are included for your backend and system debugging needs, given your 8 years of backend experience.
- **Networking**: Commands like `curl`, `netcat`, and `nmap` support your API and networking expertise, useful for testing microservices or cloud deployments.
- **Automation**: `crontab` and `rsync` are handy for automating backups or deployments, relevant to your freelance and corporate roles.
- **Research and Learning**: Text processing tools (`grep`, `awk`, `sed`) are useful for parsing logs or datasets, which could support your self-taught research on vision restoration.

If you want a deeper dive into any category (e.g., scripting examples for `awk` or `sed`, Docker workflows, or cloud-specific commands), or if you’d like a chart visualizing command usage (e.g., frequency by task type), let me know! You can also check your GitHub portfolio for specific project-related commands or share more details about your current TEKsystems tasks for tailored recommendations.
