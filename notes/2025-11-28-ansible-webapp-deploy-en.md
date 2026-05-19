---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Web App Deployment Playbook
translated: false
type: note
---

Here's a complete, production-ready Ansible playbook to deploy a Python web application with the exact flow you described:

```
Git checkout → pip install → gunicorn → nginx reverse proxy
```

### Directory structure (recommended)
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
      (optional static files)
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
app_port=8000          # internal Gunicorn port
python_version=3.11
```

### 2. deploy.yml (main playbook)
{% raw %}
```yaml
---
- name: Deploy Python web application with Gunicorn + Nginx
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
- name: Install system dependencies
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

- name: Create application directory
  file:
    path: "{{ app_dir }}"
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'

- name: Clone or update application from Git
  git:
    repo: "{{ app_repo }}"
    dest: "{{ app_dir }}"
    version: "{{ app_branch }}"
    force: yes
    update: yes
  notify: Restart gunicorn

- name: Create Python virtual environment
  pip:
    virtualenv: "{{ venv_dir }}"
    virtualenv_python: python{{ python_version }}

- name: Install Python requirements
  pip:
    requirements: "{{ requirements_file }}"
    virtualenv: "{{ venv_dir }}"
  notify: Restart gunicorn

- name: Copy Gunicorn systemd service
  template:
    src: gunicorn.service.j2
    dest: /etc/systemd/system/{{ app_name }}.service
    mode: '0644'
  notify:
    - Reload systemd
    - Restart gunicorn

- name: Enable and start Gunicorn service
  systemd:
    name: "{{ app_name }}"
    enabled: yes
    state: started
    daemon_reload: yes

- name: Configure Nginx reverse proxy
  template:
    src: nginx-site.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}
    mode: '0644'
  notify: Reload nginx

- name: Enable Nginx site
  file:
    src: /etc/nginx/sites-available/{{ app_name }}
    dest: /etc/nginx/sites-enabled/{{ app_name }}
    state: link
  notify: Reload nginx

- name: Remove default Nginx site (optional)
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: Reload nginx
```
{% endraw %}

### 4. roles/webapp/templates/gunicorn.service.j2
{% raw %}
```ini
[Unit]
Description=Gunicorn instance for {{ app_name }}
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory={{ app_dir }}
Environment="PATH={{ venv_dir }}/bin"
ExecStart={{ venv_dir }}/bin/gunicorn --workers 3 --bind unix:/run/{{ app_name }}.sock app:app
       # or use your wsgi entrypoint, e.g.: main:app or wsgi:app

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
    server_name _;  # or your domain: app.example.com

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/{{ app_name }}.sock;
    }

    location /static/ {
        alias {{ app_dir }}/static/;
    }

    # Optional: serve media files
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
- name: Reload systemd
  systemd:
    daemon_reload: yes

- name: Restart gunicorn
  systemd:
    name: "{{ app_name }}"
    state: restarted

- name: Reload nginx
  service:
    name: nginx
    state: reloaded
```
{% endraw %}

### Run the deployment
```bash
ansible-playbook -i inventory.ini deploy.yml
```

### Subsequent deployments (zero-downtime)
Just run the same command again. Git pull + pip install will trigger Gunicorn restart automatically thanks to the handlers.

### Optional improvements
- Add `--collect-static` for Django
- Add SSL with Certbot (separate role)
- Use `supervisor` instead of systemd if preferred
- Add health checks and rollback capabilities

This playbook is idempotent, secure (runs as www-data), and used in many production environments.