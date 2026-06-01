---
audio: false
generated: true
image: false
lang: en
layout: post
title: Migrating Models and Containerd Data
translated: false
type: note
---

&1  43.1s

╭─ ⚕ Hermes ──────────────────────────────────────────────────────────────────────────────────────────╮
    Models copied (~37G). Now swap and move containerd data.
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
  ┊ 💻 preparing terminal…
  💻 ssh root@129.212.178.103 " # Swap: remove originals, symlink models to volume rm -rf /root/llama.c
pp/models ln -s /mnt/volume_atl1_1780280110689/llama-models /root/llama.cpp/models ls -la /root/llama.c
pp/models echo '===' # Now move containerd data (59G) echo '=== Stopping containerd ===' systemctl stop
 containerd sleep 2 echo '=== Moving containerd data ===' rsync -a --progress /var/lib/containerd/ /mnt
/volume_atl1_1780280110689/containerd-data/ " 2>&1  (06m13s)
 
 ⚕ mimo-v2.5-pro │ 96.9K/1M │ [█░░░░░░░░░] 9% │ 35m │ ⏱ 9m 13s 
───────────────────────────────────────────────────────────────────