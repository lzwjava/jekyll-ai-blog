---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: SSH Config Host Aliases Guide
translated: false
type: note
---

Question: How to create aliases in ~/.ssh/config so I can use short names instead of typing full IP addresses or long hostnames in the ssh command?

Answer: 

You can easily create short, memorable names (aliases/Host shortcuts) for servers in your `~/.ssh/config` file.

### Most common and clean way (recommended)

```bash
# ~/.ssh/config

Host myserver          # ← this is the short name you'll type
    HostName 192.168.1.45
    User username
    Port 22            # optional - only if not using default 22
    # IdentityFile ~/.ssh/my_special_key   # optional

Host web
    HostName 10.55.3.120
    User ubuntu

Host prod-db
    HostName 172.31.45.189
    User ec2-user
    IdentityFile ~/.ssh/prod-db-key.pem

Host jump
    HostName bastion.company.com
    User admin
    ForwardAgent yes
```

After adding entries like this, you can simply connect with:

```bash
ssh myserver
ssh web
ssh prod-db
ssh jump
```

### Quick minimal version (just IP → name)

```bash
Host home-nas
    HostName 192.168.178.55

Host rpi
    HostName 192.168.178.88
```

Then:

```bash
ssh home-nas
ssh rpi
```

### Useful real-world examples

```bash
# 1. Short name + different user + key
Host forge
    HostName 85.236.12.44
    User git
    IdentityFile ~/.ssh/forge_key

# 2. Using wildcard (nice for many similar servers)
Host *.staging
    User deploy
    IdentityFile ~/.ssh/staging_key.pem

Host web-*
    User ubuntu
    IdentityFile ~/.ssh/web-servers.pem

# Then you can do:
# ssh web-03.staging
# ssh web-17

# 3. Jump host / bastion example
Host internal-*
    ProxyJump jump.company.com
    User ubuntu

# Then: ssh internal-db01
```

### Steps to set it up

1. Open or create the file:

```bash
nano ~/.ssh/config
# or
code ~/.ssh/config
# or
vim ~/.ssh/config
```

2. Add your Host blocks (make sure there is a blank line between different Host entries)

3. Set correct permissions (very important!):

```bash
chmod 600 ~/.ssh/config
```

4. Start using it right away — no ssh restart needed

```bash
ssh myserver
# or even tab-completion usually works
```

That's the cleanest and most popular way people handle dozens/hundreds of servers.

References:  

- [OpenSSH official documentation - ssh_config](https://man.openbsd.org/ssh_config)
- [Common SSH config patterns](https://linux.die.net/man/5/ssh_config)