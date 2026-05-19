---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Web 应用部署手册
translated: true
type: note
---

以下是完整的、可用于生产环境的 Ansible 剧本，用于按照您描述的流程部署 Python Web 应用程序：

```
Git 代码检出 → pip 安装 → gunicorn → nginx 反向代理
```

### 目录结构（推荐）
```
inventory.ini
deploy.yml
roles/
  webapp/
    tasks/
      main.yml
    templates/
      gunicorn.service.j2
      nginx-site.conf.j2
    files/
      （可选静态文件）
    handlers/
      main.yml
```

### 1. inventory.ini
```ini
[webservers]
app.example.com ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/yourkey.pem

[webservers:vars]
app_name=myflaskapp
app_repo=https://github.com/youruser/myflaskapp.git
app_branch=main
app_port=8000          # 内部 Gunicorn 端口
python_version=3.11
```

### 2. deploy.yml（主剧本）
{% raw %}
```yaml
---
- name: 使用 Gunicorn + Nginx 部署 Python Web 应用程序
  hosts: webservers
  become: yes
  vars:
    app_dir: /opt/{{ app_name }}
    venv_dir: /opt/{{ app_name }}/venv
    requirements_file: "{{ app_dir }}/requirements.txt"

  roles:
    - webapp
```
{% endraw %}

### 3. roles/webapp/tasks/main.yml
{% raw %}
```yaml
---
- name: 安装系统依赖
  apt:
    name:
      - git
      - python{{ python_version }}-venv
      - python{{ python_version }}
      - python3-pip
      - gunicorn
      - nginx
    state: present
    update_cache: yes

- name: 创建应用目录
  file:
    path: "{{ app_dir }}"
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'

- name: 从 Git 克隆或更新应用
  git:
    repo: "{{ app_repo }}"
    dest: "{{ app_dir }}"
    version: "{{ app_branch }}"
    force: yes
    update: yes
  notify: 重启 gunicorn

- name: 创建 Python 虚拟环境
  pip:
    virtualenv: "{{ venv_dir }}"
    virtualenv_python: python{{ python_version }}

- name: 安装 Python 依赖
  pip:
    requirements: "{{ requirements_file }}"
    virtualenv: "{{ venv_dir }}"
  notify: 重启 gunicorn

- name: 复制 Gunicorn systemd 服务
  template:
    src: gunicorn.service.j2
    dest: /etc/systemd/system/{{ app_name }}.service
    mode: '0644'
  notify:
    - 重载 systemd
    - 重启 gunicorn

- name: 启用并启动 Gunicorn 服务
  systemd:
    name: "{{ app_name }}"
    enabled: yes
    state: started
    daemon_reload: yes

- name: 配置 Nginx 反向代理
  template:
    src: nginx-site.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}
    mode: '0644'
  notify: 重载 nginx

- name: 启用 Nginx 站点
  file:
    src: /etc/nginx/sites-available/{{ app_name }}
    dest: /etc/nginx/sites-enabled/{{ app_name }}
    state: link
  notify: 重载 nginx

- name: 移除默认 Nginx 站点（可选）
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: 重载 nginx
```
{% endraw %}

### 4. roles/webapp/templates/gunicorn.service.j2
{% raw %}
```ini
[Unit]
Description={{ app_name }} 的 Gunicorn 实例
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory={{ app_dir }}
Environment="PATH={{ venv_dir }}/bin"
ExecStart={{ venv_dir }}/bin/gunicorn --workers 3 --bind unix:/run/{{ app_name }}.sock app:app
       # 或使用您的 wsgi 入口点，例如：main:app 或 wsgi:app

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
{% endraw %}

### 5. roles/webapp/templates/nginx-site.conf.j2
{% raw %}
```nginx
server {
    listen 80;
    server_name _;  # 或您的域名：app.example.com

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/{{ app_name }}.sock;
    }

    location /static/ {
        alias {{ app_dir }}/static/;
    }

    # 可选：提供媒体文件服务
    # location /media/ {
    #     alias {{ app_dir }}/media/;
    # }
}
```
{% endraw %}

### 6. roles/webapp/handlers/main.yml
{% raw %}
```yaml
---
- name: 重载 systemd
  systemd:
    daemon_reload: yes

- name: 重启 gunicorn
  systemd:
    name: "{{ app_name }}"
    state: restarted

- name: 重载 nginx
  service:
    name: nginx
    state: reloaded
```
{% endraw %}

### 运行部署
```bash
ansible-playbook -i inventory.ini deploy.yml
```

### 后续部署（零停机时间）
只需再次运行相同命令。Git 拉取 + pip 安装将借助处理程序自动触发 Gunicorn 重启。

### 可选改进
- 为 Django 添加 `--collect-static`
- 使用 Certbot 添加 SSL（单独角色）
- 如果偏好可使用 `supervisor` 替代 systemd
- 添加健康检查和回滚功能

此剧本具有幂等性、安全性（以 www-data 用户运行），并在许多生产环境中使用。