---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding IP Subnet Notation
translated: false
type: note
---

Question: Explain an IP subnet like `130.22.14.192/26`.

Answer:

An IPv4 subnet is usually written as:

```text
IP_ADDRESS / PREFIX_LENGTH
```

For example:

```text
130.22.14.192/26
```

The `/26` means **the first 26 bits are the network portion**, and the remaining **6 bits are available for hosts**.

### 1. IPv4 is 32 bits

```text
130.22.14.192
│    │  │  │
│    │  │  └── 8 bits
│    │  └───── 8 bits
│    └──────── 8 bits
└───────────── 8 bits

Total = 32 bits
```

Convert the address to binary:

```text
130       .22        .14        .192
10000010  .00010110 .00001110 .11000000
```

With `/26`:

```text
10000010.00010110.00001110.11000000
<-------- 26 network bits -------->
                              <-6->
                               host
```

So the subnet mask is:

```text
/26
```

equivalent to:

```text
255.255.255.192
```

because:

```text
11111111.11111111.11111111.11000000
   255      255      255      192
```

### 2. How many IPs?

There are 6 host bits:

```text
2^6 = 64
```

So `/26` gives **64 addresses per subnet**.

For `130.22.14.192/26`:

```text
Network:    130.22.14.192
Broadcast:  130.22.14.255

Addresses:
130.22.14.192  ← network address
130.22.14.193  ← first usable host
...
130.22.14.254  ← last usable host
130.22.14.255  ← broadcast
```

Traditionally, that means:

```text
64 total addresses
62 usable host addresses
```

because the network and broadcast addresses aren't assigned to normal hosts.

### 3. Why does `/26` start at `.192`?

The interesting part is the last octet:

```text
/26 → mask = 255.255.255.192
```

The block size is:

```text
256 - 192 = 64
```

Therefore `/26` subnets in a `/24` are:

```text
130.22.14.0/26
130.22.14.64/26
130.22.14.128/26
130.22.14.192/26
```

Each one contains 64 addresses:

```text
0   ───── 63
64  ───── 127
128 ───── 191
192 ───── 255
```

So:

```text
130.22.14.192/26
```

means:

```text
network = 130.22.14.192
range   = 130.22.14.192 → 130.22.14.255
hosts   = 130.22.14.193 → 130.22.14.254
broadcast = 130.22.14.255
```

### 4. The general formula

For:

```text
A.B.C.D/n
```

`n` tells you how many bits belong to the network.

```text
network bits = n
host bits    = 32 - n
addresses    = 2^(32-n)
```

Examples:

| CIDR  | Host bits | Total IPs | Typical usable |
| ----- | --------: | --------: | -------------: |
| `/24` |         8 |       256 |            254 |
| `/25` |         7 |       128 |            126 |
| `/26` |         6 |        64 |             62 |
| `/27` |         5 |        32 |             30 |
| `/28` |         4 |        16 |             14 |
| `/30` |         2 |         4 |              2 |
| `/32` |         0 |         1 |             1* |

The key mental model is:

```text
/24
11111111.11111111.11111111.00000000
|------ network ------|host bits|

/26
11111111.11111111.11111111.11000000
|---------- network ---------|host|
```

So **increasing `/N` makes the subnet smaller**:

```text
/24 → 256 IPs
/25 → 128 IPs
/26 →  64 IPs
/27 →  32 IPs
```

One useful next step is to learn how to calculate the **network address, broadcast address, and host range mentally from any CIDR like `10.42.17.83/21`**; I can give you a tiny algorithm and a few examples.
