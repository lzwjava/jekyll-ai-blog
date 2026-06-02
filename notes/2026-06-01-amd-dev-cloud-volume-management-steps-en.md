---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Dev Cloud Volume Management Steps
translated: false
type: note
---

## Comprehensive Summary: Volume Management on AMD Dev Cloud (DigitalOcean)

### 1. Investigating "200 is not ok" Volume Resize Error

**Checked doctl CLI code** at `/Users/lzwjava/projects/doctl/commands/volumes.go`:
- `--size` flag requires unit suffix (e.g. `200GiB`), bare `200` = 200 bytes → 0 GiB
- But the UI error was different — HTML shows `min="101" max="16384"`, current volume was 100 GiB

**Tested resize via API** — every size failed:
```bash
doctl compute volume-action resize 52743aec-... --size 101 --region atl1  # 422
doctl compute volume-action resize 52743aec-... --size 200 --region atl1  # 422
doctl compute volume-action resize 52743aec-... --size 500 --region atl1  # 422
```

Also tested via Python (curl), detaching first, different regions — all `422 "invalid size specified"`.

**Conclusion:** Resize API not supported for AMD Dev Cloud partner (GPU) volumes.

---

### 2. Moving Data to Volume (129.212.178.103)

**Checked disk usage:**
```bash
ssh root@129.212.178.103 'df -h && du -sh /root/ /var/ /opt/'
```
Result: `/root/` 37G (llama models), `/var/` 60G (containerd), `/opt/` 22G (ROCm)

**Mounted and moved llama models (37G):**
```bash
ssh root@129.212.178.103 'mount /dev/sda /mnt/volume_atl1_1780280110689'
ssh root@129.212.178.103 'rsync -a --progress /root/llama.cpp/models/ /mnt/volume_atl1_1780280110689/llama-models/'
ssh root@129.212.178.103 'rm -rf /root/llama.cpp/models && ln -s /mnt/volume_atl1_1780280110689/llama-models /root/llama.cpp/models'
```

**Investigated containerd (59G):**
```bash
ssh root@129.212.178.103 'docker images -a && docker ps -a && docker system df'
```
Found: `rocm:latest` (36GB), `ubuntu:24.04` (119MB), exited `rocm` container (Jupyter Lab), 36GB build cache.

**Cleaned up Docker artifacts:**
```bash
ssh root@129.212.178.103 'docker rm rocm'
ssh root@129.212.178.103 'docker rmi rocm:latest ubuntu:24.04'
ssh root@129.212.178.103 'docker builder prune --all -f'
ssh root@129.212.178.103 'docker system prune --all -f'
```

**Made mount persistent:**
```bash
ssh root@129.212.178.103 'echo "/dev/sda /mnt/volume_atl1_1780280110689 ext4 defaults,nofail 0 2" >> /etc/fstab'
```

**Result:** Root disk freed 95G (124G → 29G used).

---

### 3. Detaching Volume and Destroying GPU Droplet

**Unmounted volume:**
```bash
ssh root@129.212.178.103 'umount /mnt/volume_atl1_1780280110689'
```

**Detached volume:**
```bash
doctl compute volume-action detach 52743aec-5d63-11f1-a928-0a58ac126378 574422820 --wait
```

**Powered on droplet (needed for snapshot):**
```bash
doctl compute droplet-action power-on 574422820 --wait
```

**Created snapshot:**
```bash
doctl compute droplet-action snapshot 574422820 --snapshot-name "gpu-mi300x-snapshot-20260601" --wait
```

**Destroyed GPU droplet:**
```bash
doctl compute droplet delete 574422820 --force
```

**Verified:**
```bash
doctl compute snapshot list --resource droplet
doctl compute volume list
```

---

### Final State

| Resource | ID | Status | Cost/mo |
|----------|-----|--------|---------|
| GPU Droplet | 574422820 | DESTROYED | $0 |
| Snapshot | 230979911 | gpu-mi300x-snapshot-20260601 (30.6 GiB) | ~$1.53 |
| Volume | 52743aec-... | DETACHED (100 GiB, 37G llama-models) | ~$10 |
| **Total** | | | **~$11.50/mo** |

Was: ~$2+/hr = ~$1,460/mo if left running.

---

### 4. Extra Snapshots (potential cleanup)

```bash
doctl compute snapshot list --resource droplet
```

| Snapshot | Size | Cost/mo | Safe to delete? |
|----------|------|---------|-----------------|
| `7.2-gpu-mi300x1-...-1779256307024` | 132.77 GiB | $6.64 | Yes (original AMD image, re-downloadable) |
| `snap-snapshots-gpu-mi300x1-...-0530-2331` | 6.58 GiB | $0.33 | Yes |
| `gpu-mi300x-snapshot-20260601` | 30.62 GiB | $1.53 | No (your snapshot) |

```bash
# To delete old ones and save ~$7/mo:
doctl compute snapshot delete 229365612 --force
doctl compute snapshot delete 230740400 --force
```

---

### 5. Next Steps (when ready)

```bash
# Create cheap CPU droplet for data prep
doctl compute droplet create data-prep \
  --size s-2vcpu-4gb \
  --region atl1 \
  --image ubuntu-24-04-x64 \
  --ssh-keys <fingerprint>

# Attach volume
doctl compute volume-action attach 52743aec-... <new-droplet-id>

# SSH in, mount, download dataset, tokenize
ssh root@<new-ip>
mount /dev/sda /mnt/volume_atl1_1780280110689

# When data ready: detach, destroy CPU droplet
doctl compute volume-action detach 52743aec-... <new-droplet-id>
doctl compute droplet delete <new-id> --force

# Recreate GPU droplet from snapshot
doctl compute droplet create gpu-train \
  --size gpu-mi300x1-192gb \
  --region atl1 \
  --image 230979911 \
  --ssh-keys <fingerprint>

# Attach volume, train
doctl compute volume-action attach 52743aec-... <gpu-droplet-id>
```
