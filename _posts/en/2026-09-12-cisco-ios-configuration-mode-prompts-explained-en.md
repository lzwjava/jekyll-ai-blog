---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cisco IOS Configuration Mode Prompts Explained
translated: false
type: note
---

Question: What does `switch(config)#` mean in Cisco IOS, especially compared with `switch(vlan)#`?

Answer:

These prompts tell you **which configuration mode you are currently in**.

```text
Switch>
```

**User EXEC mode** — basic commands.

```text
Switch#
```

**Privileged EXEC mode** — administrative commands.

```text
Switch(config)#
```

**Global configuration mode** — you are configuring the whole switch.

You usually enter it with:

```text
Switch# configure terminal
Switch(config)#
```

From there, you can enter more specific configuration modes.

For example:

```text
Switch(config)# vlan 100
Switch(config-vlan)#
```

Now you're configuring **VLAN 100 specifically**.

Then:

```text
Switch(config-vlan)# name SALES
```

You can think of it as a hierarchy:

```text
Switch#
  └── configure terminal
       └── Switch(config)#
            ├── vlan 100
            │    └── Switch(config-vlan)#
            │
            └── interface GigabitEthernet0/1
                 └── Switch(config-if)#
```

So **`(config)` means "global configuration mode"**, while **`(config-vlan)` means "VLAN configuration sub-mode."**

One small correction: Cisco IOS normally displays **`Switch(config-vlan)#`**, not `Switch(vlan)#`.

I can also walk you through the full `Switch# → Switch(config)# → Switch(config-if)# → Switch(config-vlan)#` flow with a concrete VLAN setup.
