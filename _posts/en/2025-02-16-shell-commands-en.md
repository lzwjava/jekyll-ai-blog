---
audio: true
generated: true
image: false
layout: post
title: macOS Shell Commands
type: note
---

Here are 200 commonly used macOS shell commands, categorized for easier reference. These commands are useful for navigating the file system, managing files, system monitoring, and more.

### File System Navigation
- `ls` - List directory contents.
- `cd` - Change the current directory.
- `pwd` - Print the current working directory.
- `tree` - Display directories as trees (if installed).

### File Operations
- `cp` - Copy files or directories.
- `mv` - Move or rename files or directories.
- `rm` - Remove files or directories.
- `touch` - Create an empty file or update the timestamp.
- `mkdir` - Create a new directory.
- `rmdir` - Remove an empty directory.
- `ln` - Create hard and symbolic links.
- `chmod` - Change file permissions.
- `chown` - Change file owner and group.
- `cat` - Concatenate and display file content.
- `less` - View file content page by page.
- `more` - View file content page by page.
- `head` - Display the first lines of a file.
- `tail` - Display the last lines of a file.
- `nano` - Edit text files.
- `vi` - Edit text files.
- `vim` - Edit text files (enhanced version of `vi`).
- `find` - Search for files in a directory hierarchy.
- `locate` - Find files by name quickly.
- `grep` - Search text using patterns.
- `diff` - Compare files line by line.
- `file` - Determine file type.
- `stat` - Display file or file system status.
- `du` - Estimate file space usage.
- `df` - Report file system disk space usage.
- `dd` - Convert and copy a file.
- `tar` - Store, list, or extract files in an archive.
- `gzip` - Compress or decompress files.
- `gunzip` - Decompress files compressed with gzip.
- `zip` - Package and compress files.
- `unzip` - Extract compressed files in a ZIP archive.
- `rsync` - Remote file and directory synchronization.
- `scp` - Secure copy files between hosts.
- `curl` - Transfer data from or to a server.
- `wget` - Download files from the web.

### System Information
- `uname` - Print system information.
- `top` - Display system processes.
- `htop` - Interactive process viewer (if installed).
- `ps` - Report a snapshot of current processes.
- `kill` - Send a signal to a process.
- `killall` - Kill processes by name.
- `bg` - Run jobs in the background.
- `fg` - Run jobs in the foreground.
- `jobs` - List active jobs.
- `nice` - Run a program with modified scheduling priority.
- `renice` - Alter priority of running processes.
- `time` - Time a command's execution.
- `uptime` - Show how long the system has been running.
- `who` - Show who is logged on.
- `w` - Show who is logged on and what they are doing.
- `whoami` - Print the current user name.
- `id` - Print user and group information.
- `groups` - Print the groups a user is in.
- `passwd` - Change user password.
- `sudo` - Execute a command as another user.
- `su` - Switch user.
- `chroot` - Run a command with a different root directory.
- `hostname` - Show or set the system's host name.
- `ifconfig` - Configure a network interface.
- `ping` - Send ICMP ECHO_REQUEST to network hosts.
- `traceroute` - Trace the route to a network host.
- `netstat` - Network statistics.
- `route` - Show or manipulate the IP routing table.
- `dig` - DNS lookup utility.
- `nslookup` - Query Internet name servers interactively.
- `host` - DNS lookup utility.
- `ftp` - Internet file transfer program.
- `ssh` - OpenSSH SSH client.
- `telnet` - User interface to the TELNET protocol.
- `nc` - Netcat, arbitrary TCP and UDP connections and listens.
- `iftop` - Display bandwidth usage on an interface (if installed).
- `nmap` - Network exploration tool and security/port scanner (if installed).

### Disk Management
- `mount` - Mount a filesystem.
- `umount` - Unmount a filesystem.
- `fdisk` - Partition table manipulator for Linux.
- `mkfs` - Build a Linux filesystem.
- `fsck` - Check and repair a Linux filesystem.
- `df` - Report file system disk space usage.
- `du` - Estimate file space usage.
- `sync` - Synchronize cached writes to persistent storage.
- `dd` - Convert and copy a file.
- `hdparm` - Get/set hard disk parameters.
- `smartctl` - Control and monitor SMART-enabled ATA/SCSI-3 drives (if installed).

### Package Management
- `brew` - Homebrew package manager (if installed).
- `port` - MacPorts package manager (if installed).
- `gem` - RubyGems package manager.
- `pip` - Python package installer.
- `npm` - Node.js package manager.
- `cpan` - Perl package manager.

### Text Processing
- `awk` - Pattern scanning and processing language.
- `sed` - Stream editor for filtering and transforming text.
- `sort` - Sort lines of text files.
- `uniq` - Report or omit repeated lines.
- `cut` - Remove sections from each line of files.
- `paste` - Merge lines of files.
- `join` - Join lines of two files on a common field.
- `tr` - Translate or delete characters.
- `iconv` - Convert text from one encoding to another.
- `strings` - Find printable strings in files.
- `wc` - Print newline, word, and byte counts for each file.
- `nl` - Number lines of files.
- `od` - Dump files in various formats.
- `xxd` - Make a hexdump or do the reverse.

### Shell Scripting
- `echo` - Display a line of text.
- `printf` - Format and print data.
- `test` - Evaluate an expression.
- `expr` - Evaluate expressions.
- `read` - Read a line from standard input.
- `export` - Set an environment variable.
- `unset` - Unset values and attributes of shell variables and functions.
- `alias` - Create an alias for a command.
- `unalias` - Remove an alias.
- `source` - Execute commands from a file in the current shell.
- `exec` - Execute a command.
- `trap` - Trap signals and other events.
- `set` - Set or unset shell options and positional parameters.
- `shift` - Shift positional parameters.
- `getopts` - Parse positional parameters.
- `type` - Describe a command.
- `which` - Locate a command.
- `whereis` - Locate the binary, source, and manual page files for a command.

### Development Tools
- `gcc` - GNU project C and C++ compiler.
- `make` - Directory-oriented makefile processor.
- `cmake` - Cross-platform makefile generator.
- `autoconf` - Generate configure scripts.
- `automake` - Generate Makefile.in files.
- `ld` - The GNU linker.
- `ar` - Create, modify, and extract from archives.
- `nm` - List symbols from object files.
- `objdump` - Display information from object files.
- `strip` - Discard symbols from object files.
- `ranlib` - Generate index to archive.
- `gdb` - The GNU debugger.
- `lldb` - The LLVM debugger.
- `valgrind` - Instrumentation framework for building dynamic analysis tools (if installed).
- `strace` - Trace system calls and signals (if installed).
- `ltrace` - Trace library calls (if installed).
- `perf` - Performance analysis tools for Linux.
- `time` - Time a command's execution.
- `xargs` - Build and execute command lines from standard input.
- `m4` - Macro processor.
- `cpp` - The C Preprocessor.
- `flex` - Fast Lexical Analyzer generator.
- `bison` - Yacc-compatible parser generator.
- `bc` - An arbitrary precision calculator language.
- `dc` - An arbitrary precision calculator.

### Version Control
- `git` - Distributed version control system.
- `svn` - Subversion version control system.
- `hg` - Mercurial distributed version control system.
- `cvs` - Concurrent Versions System.

### Miscellaneous
- `man` - Format and display the online manual pages.
- `info` - Read Info documents.
- `apropos` - Search the manual page names and descriptions.
- `whatis` - Display one-line manual page descriptions.
- `history` - Display or manipulate the history list.
- `yes` - Output a string repeatedly until killed.
- `cal` - Display a calendar.
- `date` - Display or set the date and time.
- `sleep` - Delay for a specified amount of time.
- `watch` - Execute a program periodically, showing output fullscreen.
- `xargs` - Build and execute command lines from standard input.
- `seq` - Print a sequence of numbers.
- `shuf` - Generate random permutations.
- `tee` - Read from standard input and write to standard output and files.
- `tput` - Initialize a terminal or query terminfo database.
- `stty` - Change and print terminal line settings.
- `clear` - Clear the terminal screen.
- `reset` - Reset the terminal to a sane state.
- `script` - Make typescript of terminal session.
- `wall` - Write a message to all users.
- `write` - Send a message to another user.
- `mesg` - Control write access to your terminal.
- `talk` - Talk to another user.
- `ytalk` - Yet another talk program (if installed).
- `crontab` - Maintain crontab files for individual users.
- `at` - Schedule commands to be executed once at a later time.
- `batch` - Schedule commands to be executed in a batch queue.
- `nice` - Run a program with modified scheduling priority.
- `renice` - Alter priority of running processes.
- `time` - Time a command's execution.
- `ulimit` - Set or report user resource limits.
- `pr` - Convert text files for printing.
- `lp` - Send files to a printer.
- `lpr` - Print files.
- `lpq` - Show printer queue status.
- `lprm` - Remove jobs from the printer queue.
- `enscript` - Convert text to PostScript, HTML, or RTF, with syntax highlighting (if installed).
- `a2ps` - Any to PostScript filter.
- `ps2pdf` - Convert PostScript to PDF.
- `pdf2ps` - Convert PDF to PostScript.
- `gs` - Ghostscript interpreter.
- `convert` - Convert between image formats (if installed).
- `mogrify` - Resize, rotate, and transform images (if installed).
- `exiftool` - Read, write, and edit meta information in files (if installed).
- `jpegoptim` - Optimize JPEG files (if installed).
- `optipng` - Optimize PNG files (if installed).

These commands cover a wide range of functionalities and are essential for users who want to efficiently manage and interact with their macOS system through the terminal.
