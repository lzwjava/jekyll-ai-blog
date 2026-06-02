---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comprehensive Introduction to Dnsmasq Software
translated: false
type: note
---

Question: What is a comprehensive introduction to dnsmasq?

Answer:

## What is dnsmasq?

Dnsmasq is free software providing Domain Name System (DNS) caching, a Dynamic Host Configuration Protocol (DHCP) server, router advertisement, and network boot features, intended for small computer networks. It has low requirements for system resources, can run on Linux, BSDs, Android, and macOS, and is included in most Linux distributions. Consequently, it is present in many home routers and IoT gadgets, and is also included in Android.

It is designed to be lightweight and have a small footprint, suitable for resource-constrained routers and firewalls. It has also been widely used for tethering on smartphones, portable hotspots, and to support virtual networking in virtualisation frameworks.

---

## Core Components and Features

### 1. DNS Subsystem

The DNS subsystem provides a local DNS server for the network, with forwarding of all query types to upstream recursive DNS servers and caching of common record types (A, AAAA, CNAME and PTR, also DNSKEY and DS when DNSSEC is enabled). Local DNS names can be defined by reading `/etc/hosts`, by importing names from the DHCP subsystem, or by configuration of a wide range of useful record types.

Dnsmasq accepts DNS queries and either answers them from a small, local cache or forwards them to a real, recursive DNS server. It loads the contents of `/etc/hosts` so that local hostnames which do not appear in the global DNS can be resolved, and also answers DNS queries for DHCP-configured hosts.

**Important distinction:** Dnsmasq is a *forwarding/stub* resolver, not a *recursive* resolver. This means dnsmasq always needs a recursive DNS resolver it can forward its queries to.

### 2. DHCP Subsystem

The DHCP subsystem supports DHCPv4, DHCPv6, BOOTP, and PXE. Both static and dynamic DHCP leases are supported, along with stateless mode in DHCPv6.

Dnsmasq's DHCP server supports static and dynamic DHCP leases, multiple networks, and IP address ranges. The DHCP server integrates with the DNS server and allows local machines with DHCP-allocated addresses to appear in the DNS.

### 3. TFTP Server

Dnsmasq includes a secure, read-only TFTP server to allow net/PXE boot of DHCP hosts and also supports BOOTP. The PXE support is full.

### 4. Router Advertisement (IPv6)

The Router Advertisement subsystem provides basic autoconfiguration for IPv6 hosts. It can be used stand-alone or in conjunction with DHCPv6. The M and O bits are configurable to control hosts' use of DHCPv6. Router advertisements can include the RDNSS option.

---

## Installation

**Debian / Ubuntu:**
```bash
sudo apt-get install dnsmasq
```

**CentOS / RHEL:**
```bash
sudo yum install dnsmasq
```

**Arch Linux:**
```bash
sudo pacman -S dnsmasq
```

After installation, enable and start the service:
```bash
sudo systemctl enable --now dnsmasq
```

---

## Configuration File

The primary configuration file is `/etc/dnsmasq.conf`. The file contains comments explaining the options. Drop-in configuration files can be placed in `/etc/dnsmasq.d/` with a `.conf` extension.

To verify your configuration syntax before applying:
```bash
dnsmasq --test
```

---

## Key Configuration Examples

### DNS Forwarding (upstream servers)
```ini
# /etc/dnsmasq.conf
server=8.8.8.8
server=1.1.1.1
```

### DNS Caching (local resolver)
```ini
listen-address=127.0.0.1
cache-size=1000
```

### DHCP Server
```ini
# Enable DHCP on a range with a 12-hour lease
dhcp-range=192.168.1.50,192.168.1.150,12h
```

### Static IP Assignment by MAC Address
```ini
dhcp-host=00:11:22:33:44:55,192.168.1.100
```

### Restrict to Specific Interface
```ini
interface=eth0
bind-interfaces
```

### Logging for Debugging
```ini
log-queries
log-facility=/var/log/dnsmasq.log
```

---

## DNSSEC Validation

When DNSSEC is enabled, dnsmasq validates DNS replies and caches DNSSEC data. When forwarding DNS queries, dnsmasq requests the DNSSEC records needed to validate the replies. The replies are validated and the result returned as the Authenticated Data bit in the DNS packet.

To enable DNSSEC on Arch Linux / Debian:
```ini
conf-file=/usr/share/dnsmasq/trust-anchors.conf
dnssec
```

---

## PXE / Network Boot

PXE requires a DHCP and a TFTP server; both can be provided by dnsmasq. A basic PXE setup in `dnsmasq.conf`:
```ini
enable-tftp
tftp-root=/srv/tftp
pxe-service=x86PC,"PXELINUX (BIOS)",bios/lpxelinux
pxe-service=X86-64_EFI,"PXELINUX (EFI)",efi64/syslinux.efi
```

Dnsmasq can also be set to behave as a "proxy DHCP", only serving PXE-specific information to the client when another DHCP server is already running on the network.

---

## Ad Blocking / DNS Filtering

Records added to your local `/etc/hosts` file with the format `0.0.0.0 annoyingsite.com` can be used to prevent references to that domain from being resolved by your browser. This can quickly evolve to a local ad blocker when combined with adblocking site list providers. If done on a router, one can efficiently remove advertising content for an entire household or company.

Some ISPs rewrite NXDOMAIN responses, forcing browsers to a search page when a domain doesn't exist. Dnsmasq can filter out these "bogus" NXDOMAIN records, preventing this potentially unwanted behavior.

---

## Split DNS (VPN / Internal Domains)

Specified sub-domains can be directed to their own upstream DNS servers, making VPN configuration easy.

```ini
# Route internal domains to a private DNS server
server=/internal.company.com/10.0.0.1
```

---

## Authoritative DNS Mode

Authoritative DNS mode allows local DNS names to be exported to a zone in the global DNS. Dnsmasq acts as the authoritative server for this zone, and also provides zone transfer to secondaries for the zone, if required.

---

## Common Use Cases

| Use Case | How dnsmasq Helps |
|---|---|
| Home/office router | DNS forwarding + DHCP for all LAN devices |
| Development environment | Local domain resolution (e.g., `myapp.local`) |
| VPN split routing | Route specific domains to internal DNS |
| Network booting (PXE) | DHCP + TFTP for diskless boot |
| Ad blocking | Block domains via `/etc/hosts` or `address=` directives |
| IoT network | Lightweight DHCP + DNS for constrained environments |
| Virtual machine networks | DNS/DHCP for `libvirt`/VirtualBox/VMware guest networks |

---

## Platform Support

Supported platforms include Linux (with glibc and uclibc), Android, *BSD, and macOS. Dnsmasq is included in most Linux distributions and the ports systems of FreeBSD, OpenBSD, and NetBSD. Dnsmasq provides full IPv6 support.

---

## Limitations to Know

- Dnsmasq is **not** recommended as a public-facing DNS server. It is designed to provide its services within a private network.
- It is a stub/forwarding resolver, **not** a full recursive resolver like Unbound or BIND.
- For larger enterprise setups with fast failover requirements, alternatives like KEA DHCP may be more appropriate.

---

## Signals and Runtime Control

| Signal | Effect |
|---|---|
| `SIGHUP` | Reload `/etc/hosts` and configuration |
| `SIGUSR1` | Dump cache statistics to log |
| `SIGUSR2` | Rotate log file |

---

## Summary

Dnsmasq is an elegant, all-in-one network services daemon ideal for small-to-medium networks. Its strength lies in combining DNS caching/forwarding, DHCP, TFTP, PXE boot, and IPv6 router advertisement into a single lightweight binary with a simple, well-documented configuration file. It is the de facto standard for embedded routers, home labs, development environments, and IoT networks worldwide.

References:

- [dnsmasq Official Documentation](https://thekelleys.org.uk/dnsmasq/doc.html)
- [dnsmasq Man Page](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
- [dnsmasq - Wikipedia](https://en.wikipedia.org/wiki/Dnsmasq)
- [dnsmasq - ArchWiki](https://wiki.archlinux.org/title/Dnsmasq)
- [dnsmasq - Gentoo Wiki](https://wiki.gentoo.org/wiki/Dnsmasq)
- [dnsmasq Command Guide - TutorialsPoint](https://www.tutorialspoint.com/unix_commands/dnsmasq.htm)
- [OPNsense dnsmasq Documentation](https://docs.opnsense.org/manual/dnsmasq.html)
