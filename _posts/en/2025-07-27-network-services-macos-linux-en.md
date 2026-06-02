---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Services in macOS and Linux
translated: false
type: note
---

### Network Services and Related Terms in macOS and Linux

These terms appear to refer primarily to network service names, often defined in the `/etc/services` file on both macOS and Linux systems. This file maps service names to port numbers and protocols for standard network services. Some are official IANA-registered services, while others are aliases or protocol names commonly used in system configurations. Below is an explanation of each, based on standard usage in macOS (which uses a BSD-like base) and Linux distributions.

- **service**: This is a generic term for system daemons or processes in both macOS (via launchd) and Linux (via systemd or init systems). It's not a specific network service in `/etc/services`, but it may refer to the "service" command in Linux for managing legacy SysV init scripts, or broadly to any background service.

- **ircu**: Refers to the IRCU (Internet Relay Chat Undernet) service, a variant of IRC server software. It uses port 6667/tcp (and sometimes udp). In Linux, it could be associated with IRC daemons like ircu or undernet-ircu packages. Not commonly pre-installed on macOS or modern Linux, but available via ports or packages for chat servers.

- **complex-link**: Likely a misspelling or variant of "commplex-link", a network service registered on port 5001/tcp. It's used for communication multiplexing links (e.g., in some networking tools or protocols). In macOS, this port is associated with AirPort/Time Capsule configuration or router admin utilities (e.g., Netgear or Apple devices). On Linux, it may appear in firewall rules or netstat output for similar purposes.

- **dhcpc**: Alias for the DHCP client service, using port 68/udp (also known as bootpc). This is the client side of DHCP for obtaining IP addresses dynamically. In Linux, it's handled by processes like dhclient or dhcpcd; in macOS, by configd or bootpd (client mode).

- **zeroconf**: Refers to Zero Configuration Networking (Zeroconf), a protocol for automatic service discovery without manual configuration. In macOS, it's implemented as Bonjour (using mDNS on port 5353/udp). In Linux, it's typically Avahi (also on port 5353/udp). Used for discovering printers, shares, and other local network services.

- **ntp**: Network Time Protocol service for synchronizing system clocks over the network. Uses port 123/udp (and sometimes tcp). In Linux, handled by ntpd or chronyd; in macOS, by ntpd or the built-in time sync daemon.

- **http**: HyperText Transfer Protocol, the foundation of web communication. Uses port 80/tcp (sometimes udp). In both macOS and Linux, it's associated with web servers like Apache (httpd) or Nginx.

- **ssh**: Secure Shell protocol for secure remote access and file transfer. Uses port 22/tcp (and udp/sctp). In Linux and macOS, the daemon is sshd, enabled via system preferences or sshd_config.

- **hgvirtgrp**: This appears to be a reference to a user group related to virtualization, possibly a variant or typo for "libvirt group" in Linux (e.g., libvirt or libvirt-qemu group). In Linux, adding users to the libvirt group grants access to manage virtual machines via libvirt (for KVM/QEMU). In macOS, virtualization uses the Hypervisor framework, but there's no standard "hgvirtgrp" group— it may refer to custom groups for hypervisor/virtualization tools like QEMU or Virt-Manager. If it's a specific group, check `/etc/group` on your system.

These are commonly seen in tools like `netstat`, `lsof`, or firewall configurations (e.g., pf on macOS, iptables/ufw on Linux). For exact definitions, consult your system's `/etc/services` file or the IANA port registry.

**References**
[Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
[what is an open port with a commplex-link? - Apple Community](https://discussions.apple.com/thread/7747034)
[Running virt-manager and libvirt on macOS](https://www.arthurkoziel.com/running-virt-manager-and-libvirt-on-macos/)
