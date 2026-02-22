---
audio: false
generated: true
image: false
lang: en
layout: post
title: Create VLAN Command Guide
translated: false
type: note
---

Question: After logging into the switch, what command is used to create a VLAN in global configuration mode?

Answer: 

To create a VLAN on a Cisco switch (or similar CLI-based network devices) after logging in and entering **global configuration mode**, you use the following command:

```bash
vlan <vlan-id>
```

### Explanation:
- **`vlan`**: This is the command keyword that tells the switch you want to create or configure a VLAN.
- **`<vlan-id>`**: This is a placeholder for the actual VLAN number you wish to create. Valid VLAN IDs typically range from **1 to 4094**, though some ranges are reserved (e.g., VLAN 1 is default, VLANs 1002–1005 are reserved for legacy token ring/FDDI).

### Step-by-Step Example:
1. Log in to the switch.
2. Enter privileged EXEC mode:
   ```bash
   enable
   ```
3. Enter global configuration mode:
   ```bash
   configure terminal
   ```
4. Create a VLAN (for example, VLAN 10):
   ```bash
   vlan 10
   ```
5. (Optional) Name the VLAN:
   ```bash
   name Sales
   ```
6. Exit configuration mode:
   ```bash
   end
   ```

After executing `vlan 10`, the switch enters **VLAN configuration mode** (`config-vlan#`), where you can optionally assign a name or other parameters to the VLAN.

This matches the reference answer provided: **`vlan vlan-id`**.

References:  

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/17056-7.html)