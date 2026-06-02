---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing Oracle 12c on Ubuntu
translated: false
type: note
---

### Installing Oracle Database 12c Release 1 (12.1.0.2 with patch 12.1.2?) from Tarball on Ubuntu 22.04 x86_64

The file `v12.1.2_linuxx64_server_dec.tar.gz` appears to be a tarball for Oracle Database 12c Release 1 (likely version 12.1.0.2 bundled with the 12.1.2 patch, server edition, possibly "dec" for deconfigured). This is an older version of Oracle Database (from ~2013-2014), and Oracle does **not officially support Ubuntu**. Installation on Ubuntu 22.04 (which uses modern libraries like glibc 2.35) can work but may require workarounds for compatibility issues, such as library linking or kernel parameters. Expect potential errors with dependencies—test in a VM first.

**Warnings:**
- Oracle 12c is end-of-life for extended support (as of 2022), so use for testing/production at your own risk. Consider newer versions like 19c or 23ai for production.
- You'll need root/sudo access.
- Minimum hardware: 2 GB RAM (8 GB recommended), 2 CPU cores, 10 GB free disk space for software (more for DB).
- Backup your system before proceeding.
- If this tarball is not from Oracle's official source, verify its integrity (e.g., checksums) to avoid malware.

#### Step 1: Prepare Your System
1. **Update Ubuntu**:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Required Dependencies**:
   Oracle 12c needs specific libraries. Install them via apt:
   ```
   sudo apt install -y oracle-java8-installer bc binutils libaio1 libaio-dev libelf-dev libnuma-dev libstdc++6 unixodbc unixodbc-dev
   ```
   - If `oracle-java8-installer` isn't available (it's in older repos), add Oracle's Java PPA or download JDK 8 manually:
     ```
     sudo add-apt-repository ppa:webupd8team/java -y
     sudo apt update
     sudo apt install oracle-java8-installer -y
     ```
     Accept the license during installation. Set JAVA_HOME:
     ```
     echo 'export JAVA_HOME=/usr/lib/jvm/java-8-oracle' >> ~/.bashrc
     source ~/.bashrc
     ```

3. **Create Oracle User and Groups**:
   Run as root or with sudo:
   ```
   sudo groupadd -g 54321 oinstall
   sudo groupadd -g 54322 dba
   sudo useradd -u 54321 -g oinstall -G dba -s /bin/bash oracle
   sudo passwd oracle  # Set a password for the oracle user
   ```

4. **Configure Kernel Parameters**:
   Edit `/etc/sysctl.conf`:
   ```
   sudo nano /etc/sysctl.conf
   ```
   Add these lines (adjust for your RAM/disk; these are minimums):
   ```
   fs.file-max = 6815744
   kernel.sem = 250 32000 100 128
   kernel.shmmni = 4096
   kernel.shmall = 1073741824
   kernel.shmmax = 4398046511104
   kernel.panic_on_oops = 1
   net.core.rmem_default = 262144
   net.core.rmem_max = 4194304
   net.core.wmem_default = 262144
   net.core.wmem_max = 1048576
   fs.aio-max-nr = 1048576
   vm.swappiness = 0
   ```
   Apply changes:
   ```
   sudo sysctl -p
   ```

5. **Set Shell Limits for Oracle User**:
   Edit `/etc/security/limits.conf`:
   ```
   sudo nano /etc/security/limits.conf
   ```
   Add:
   ```
   oracle soft nproc 2047
   oracle hard nproc 16384
   oracle soft nofile 1024
   oracle hard nofile 65536
   oracle soft stack 10240
   oracle hard stack 32768
   ```
   Edit `/etc/pam.d/login` and add:
   ```
   sudo nano /etc/pam.d/login
   ```
   Append: `session required pam_limits.so`

6. **Create Directories**:
   ```
   sudo mkdir -p /u01/app/oracle/product/12.1.0/dbhome_1
   sudo mkdir -p /u01/app/oraInventory
   sudo chown -R oracle:oinstall /u01
   sudo chmod -R 775 /u01
   ```

7. **Swap Space** (if RAM < 8 GB, add swap):
   For 2 GB RAM, create 2 GB swapfile:
   ```
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

8. **Disable Firewall/SElinux** (if enabled):
   ```
   sudo ufw disable  # Or configure ports 1521, 5500 if needed
   sudo apt remove apparmor -y  # If AppArmor interferes
   ```

#### Step 2: Extract the Tarball
Switch to the oracle user:
```
su - oracle
cd ~/Downloads  # Or wherever the file is
```
Extract (this creates the database home directory structure):
```
tar -xzf v12.1.2_linuxx64_server_dec.tar.gz -C /u01/app/oracle/product/12.1.0/
```
- This should create `/u01/app/oracle/product/12.1.0/dbhome_1` with files like `runInstaller`.
- If the tarball extracts to a different structure, adjust paths accordingly (e.g., `database/` dir).

#### Step 3: Run the Installer
Still as oracle user:
```
cd /u01/app/oracle/product/12.1.0/dbhome_1
./runInstaller
```
- The GUI installer will launch (requires X11 forwarding if SSH; use `ssh -X` or enable X11).
- **Installation Options**:
  - Select "Create and configure a database software only" or "Single instance database installation" (for server edition).
  - ORACLE_HOME: `/u01/app/oracle/product/12.1.0/dbhome_1`
  - Inventory: `/u01/app/oraInventory`
  - If it's just software (no DB creation), choose "Install database software only".
- Follow the wizard: Accept defaults where possible, but set passwords for SYS/SYSTEM.
- Ignore any "prereq" warnings initially—fix post-install if needed.

If GUI fails (e.g., DISPLAY error), run silent install:
```
./runInstaller -silent -responseFile /path/to/responsefile.rsp
```
You'll need to prepare a response file (sample in the extracted dir, e.g., `db_install.rsp`). Edit it with your settings (ORACLE_HOME, etc.) and run.

#### Step 4: Post-Installation
1. **Run root.sh** (as root):
   ```
   sudo /u01/app/oraInventory/orainstRoot.sh
   sudo /u01/app/oracle/product/12.1.0/dbhome_1/root.sh
   ```

2. **Set Environment Variables** (for oracle user, add to `~/.bash_profile`):
   ```
   export ORACLE_HOME=/u01/app/oracle/product/12.1.0/dbhome_1
   export PATH=$ORACLE_HOME/bin:$PATH
   export ORACLE_SID=orcl  # Change to your SID
   export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
   export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib
   ```
   ```
   source ~/.bash_profile
   ```

3. **Create a Database** (if not done during install):
   ```
   dbca  # Database Configuration Assistant (GUI/silent)
   ```
   Or use SQL*Plus for manual creation.

4. **Start/Stop Services**:
   ```
   sqlplus / as sysdba
   STARTUP;  # Or shutdown
   ```
   Add to systemd for auto-start (create `/etc/systemd/system/oracle.service` with exec to `dbstart`).

#### Troubleshooting Common Issues on Ubuntu 22.04
- **Glibc/Dependency Errors**: Oracle 12c expects glibc <=2.17. Ubuntu 22.04 has 2.35—use `ldd` to check, or install compat libs:
  ```
  sudo apt install libc6:i386 libncurses5:i386 libstdc++6:i386
  ```
  If linker errors, set `LD_PRELOAD` or use a Docker container with Oracle Linux.
- **Java/Display Issues**: Ensure JDK 8 is set (`java -version` should show 1.8). For headless: `export DISPLAY=:0`.
- **Out of Memory**: Increase ulimit or RAM. Edit `runInstaller` params if needed.
- **Patch 12.1.2**: If not bundled, download from My Oracle Support and apply with `opatch` after install.
- **Logs**: Check `/u01/app/oraInventory/logs/installActions*.log` for errors.
- **Compatibility Fix**: Some users symlink libs (e.g., `sudo ln -s /lib/x86_64-linux-gnu/libpthread.so.0 /u01/app/oracle/product/12.1.0/dbhome_1/lib/libpthread_nonshared.a`—research per error).

#### Verification
- Run `sqlplus / as sysdba` and execute `SELECT * FROM v$version;`.
- Listener: `lsnrctl start`.

If you encounter specific errors, provide the log output for more help. For official (though RHEL-focused) docs, see Oracle's 12c install guide. If this is for a different product (not DB), clarify the tarball contents!
