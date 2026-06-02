---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible自动化指南
translated: true
type: note
---

## 什么是 Ansible？

Ansible 是一款**开源自动化工具**，能够自动化：

- 配置管理
- 应用部署
- 任务自动化/编排
- 云资源调配

它采用**无代理架构**（被管理节点无需安装软件/代理），通过 **SSH**（Windows 使用 WinRM）进行通信，并使用 **YAML** 格式（人类可读的语法）。
Ansible 隶属红帽公司，是当今最流行的 DevOps 工具之一。

### 核心优势

- 简单易学（基于 YAML）
- 无代理（利用现有 SSH 连接）
- 幂等性（多次执行剧本结果一致）
- 庞大的模块库（超过 3000 个模块）
- 活跃的社区和 Galaxy（公共角色仓库）

## 核心概念

| 概念名称       | 功能说明                                                                     |
|----------------|-----------------------------------------------------------------------------|
| Inventory      | 被管理主机列表（IP 或主机名）。支持静态配置（ini/yaml）和动态获取。           |
| Playbook       | 包含一个或多个剧本的 YAML 文件，是编写自动化的核心载体。                     |
| Play           | 将主机组与任务/角色进行映射。                                                |
| Task           | 单个操作动作（如安装软件包、复制文件、重启服务）。                           |
| Module         | 执行特定操作的可复用代码单元（软件包、服务、文件、模板等）。                 |
| Role           | 包含任务、变量、模板、处理程序等的可复用目录结构。                           |
| Handler        | 由其他任务触发才执行的特殊任务（如重启 nginx）。                            |
| Facts          | 从远程主机采集的系统信息（操作系统、IP、内存等）。                           |
| Variables      | 用于定制剧本的参数（主机变量、组变量、角色变量、额外变量等）。               |

## 安装部署

### 控制节点（您的笔记本电脑/服务器）

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ansible -y

# RHEL/CentOS/Rocky
sudo dnf install ansible -y

# macOS (通过 Homebrew)
brew install ansible

# 或使用 pip（推荐获取最新版本）
python3 -m pip install --user ansible
```

验证版本：

```bash
ansible --version
```

## 主机清单

### 基础 INI 格式（`inventory.ini`）

```ini
[webservers]
web1.example.com
web2.example.com ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/mykey.pem

[dbservers]
db1.example.com ansible_host=192.168.1.50

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### YAML 格式（`inventory.yaml`）

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_user: ubuntu
    dbservers:
      hosts:
        db1.example.com:
```

测试连接：

```bash
ansible all -i inventory.ini -m ping
```

## 基础临时命令示例

```bash
# 采集系统信息
ansible webservers -m setup

# 为所有 Web 服务器安装 nginx
ansible webservers -m apt -a "name=nginx state=present" --become

# 复制文件
ansible webservers -m copy -a "src=/local/file.txt dest=/remote/file.txt"

# 重启服务器
ansible all -m reboot --become
```

## 编写第一个剧本

创建 `first_playbook.yml`：

{% raw %}

```yaml
---
- name: 配置 Web 服务器
  hosts: webservers
  become: yes                     # 提权执行
  vars:
    http_port: 80
    domain: example.com

  tasks:
    - name: 确保 nginx 已安装
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: 复制 nginx 配置文件
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ domain }}
      notify: 重启 nginx

    - name: 启用新站点配置
      file:
        src: /etc/nginx/sites-available/{{ domain }}
        dest: /etc/nginx/sites-enabled/{{ domain }}
        state: link

    - name: 确保 nginx 运行中
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: 重启 nginx
      service:
        name: nginx
        state: restarted
```

{% endraw %}

执行剧本：

```bash
ansible-playbook -i inventory.ini first_playbook.yml
```

## 常用功能模块

| 分类           | 模块                                         | 典型应用场景                             |
|----------------|---------------------------------------------|-----------------------------------------|
| 软件包管理     | apt, yum, dnf, pacman, pip                  | 安装软件                                |
| 文件管理       | file, copy, template, lineinfile, find      | 管理文件/目录                           |
| 系统管理       | service, systemd, user, group, reboot       | 管理服务、用户账户                      |
| 命令执行       | command, shell, script                      | 运行任意命令                           |
| 云平台管理     | ec2_instance, digital_ocean, azure_rm_*     | 调配云资源                              |
| 数据库管理     | postgresql_db, mysql_db, mongodb_user       | 管理数据库                              |
| 版本控制       | git                                         | 拉取代码                                |
| 信息采集       | setup                                       | 收集系统信息                            |

## 变量与系统信息

### 变量优先级（从高到低）

1. 命令行参数 `-e "var=value"`
2. 角色默认变量
3. 清单变量
4. 剧本变量
5. 主机信息/采集信息

### 变量使用示例

{% raw %}

```yaml
vars:
  app_name: myapp
  app_user: www-data

vars_files:
  - secrets.yml

tasks:
  - name: 创建应用用户
    user:
      name: "{{ app_user }}"
      shell: /bin/bash
```

{% endraw %}

### 使用系统信息

{% raw %}

```yaml
- name: 显示操作系统信息
  debug:
    msg: "当前系统为 {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}"
```

{% endraw %}

## 条件与循环

### 条件判断

```yaml
tasks:
  - name: 仅在 RedHat 系统安装 Apache
    yum:
      name: httpd
      state: present
    when: ansible_facts['os_family'] == "RedHat"
```

### 循环操作

{% raw %}

```yaml
- name: 创建多个用户
  user:
    name: "{{ item }}"
    state: present
  loop:
    - alice
    - bob
    - charlie

- name: 安装软件包列表
  apt:
    name: "{{ item }}"
    state: present
  loop: "{{ packages }}"
  vars:
    packages:
      - nginx
      - git
      - vim
```

{% endraw %}

## 角色 – 最佳实践目录结构

```
myrole/
├── defaults/
│   └── main.yml
├── vars/
│   └── main.yml
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── templates/
│   └── nginx.conf.j2
├── files/
├── meta/
│   └── main.yml
└── README.md
```

在剧本中调用角色：

```yaml
- hosts: webservers
  roles:
    - common
    - nginx
    - myapp
```

获取海量现成角色：

```bash
ansible-galaxy search postgres
ansible-galaxy install geerlingguy.postgres
```

## 实际应用场景

| 应用场景                       | 典型剧本/角色案例                                           |
|-------------------------------|-----------------------------------------------------------|
| 服务器初始化                  | 安装基础软件包、创建用户、配置 SSH 密钥、设置防火墙        |
| Web 应用部署                  | 拉取代码 → pip 安装依赖 → 启动 gunicorn → 配置 nginx 反向代理 |
| 数据库搭建                    | 安装 PostgreSQL/MySQL → 创建数据库/用户 → 恢复数据转储     |
| 持续部署                      | Webhook 触发 → 拉取最新代码 → 运行测试 → 部署更新         |
| 云资源调配                    | 启动 EC2 实例 → 加入负载均衡器 → 安装应用                 |
| 安全加固                      | CIS 基准检测角色、禁用 root 登录、更新软件包               |
| 监控系统搭建                  | 安装 Prometheus/Node exporter、Grafana、Alertmanager      |
| 备份自动化                    | rsync/数据库转储 → 同步至 S3 → 清理历史备份               |
| 多环境管理                    | 通过不同变量管理开发/预发/生产环境                        |

## 最佳实践

1. 复用代码优先使用角色结构
2. 使用 `ansible-vault` 加密敏感数据

   ```bash
   ansible-vault create secrets.yml
   ansible-playbook site.yml --ask-vault-pass
   ```

3. 使用 Git 进行剧本/角色版本控制
4. 首次运行使用 `--check` 模式（预演）

   ```bash
   ansible-playbook site.yml --check
   ```

5. 为任务打标签实现选择性运行

   ```yaml
   tags: ['nginx', 'web']
   ```

   执行：`ansible-playbook site.yml --tags web`
6. 按需使用 `pre_tasks` 和 `post_tasks`
7. 避免硬编码密码 – 使用 vault 或查询插件

## 常用命令速查

```bash
ansible all -m ping
ansible all -m setup                    # 采集系统信息
ansible-playbook playbook.yml --check   # 预演模式
ansible-playbook playbook.yml -t nginx  # 运行指定标签
ansible-vault encrypt secrets.yml
ansible-galaxy role install geerlingguy.nginx
ansible-galaxy collection install community.docker
```

## 学习资源

- 官方文档：<https://docs.ansible.com>
- Ansible Galaxy：<https://galaxy.ansible.com>
- Jeff Geerling 优质角色集：<https://github.com/geerlingguy>
- 书籍：《Ansible for DevOps》（Jeff Geerling 著）

循序渐进：从临时命令 → 简单剧本 → 角色封装 → 完整基础设施即代码。

您已掌握在生产环境中高效使用 Ansible 的全部基础知识！
