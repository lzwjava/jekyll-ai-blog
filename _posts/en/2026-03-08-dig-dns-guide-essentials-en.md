---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dig Command DNS Guide Essentials
translated: false
type: note
---

**Question:** What is a comprehensive introduction to the `dig` command for DNS purposes?

**Answer:**

---

## What is `dig`?

`dig` (Domain Information Groper) is a powerful tool used for querying the Domain Name System (DNS). It is commonly used to troubleshoot domain resolution issues and obtain detailed information about DNS records. The `dig` utility is part of the Berkeley Internet Name Domain (BIND) suite, a widely used DNS software package maintained by the Internet Systems Consortium (ISC).

For network administrators and developers, it is an indispensable tool for diagnosing DNS problems, verifying configurations, and gaining a deeper understanding of how domain names are resolved into IP addresses.

---

## Installation

On most Linux distributions, the `dig` command is part of the `dnsutils` or `bind-utils` package. On Debian-based systems like Ubuntu, you can install it using your distribution's package manager.

```bash
# Ubuntu/Debian
sudo apt install dnsutils

# CentOS/RHEL
sudo yum install bind-utils

# Verify installation
dig -v
```

`dig` comes pre-installed on most macOS versions and some Linux distributions.

---

## Basic Syntax

```bash
dig [@server] [domain] [type] [options]
```

Where:

- `@server` — Optional. Specifies the DNS server to query. If omitted, `dig` uses the default server.
- `domain` — The domain name you are querying about.
- `query-type` — The type of DNS record you want (e.g., A, MX, NS). If not specified, `dig` defaults to querying A records.

By default, `dig` directs its queries to the DNS server listed in the `/etc/resolv.conf` file, but it also provides the flexibility to query any other name server directly.

---

## Understanding the Output Sections

A typical `dig` response contains the following sections:

### 1. Header Section

The HEADER section summarizes the DNS query and response details. It includes information about the query type (e.g., standard query), the response status (e.g., NOERROR for a successful response), and flags indicating key attributes like recursion.

### 2. Question Section

This section displays the query details, including the domain name and record type being requested. For example, a query for the A record of `example.com` indicates a request to resolve the domain to an IPv4 address.

### 3. Answer Section

The answer section contains the actual DNS record(s) returned for the query, such as IP addresses for an A record lookup. For example: `example.com. 3600 IN A 93.184.216.34` — this shows that `example.com` resolves to the IPv4 address `93.184.216.34` with a Time-to-Live (TTL) of 3600 seconds.

### 4. Authority Section

If the queried DNS server is authoritative for the domain, this section lists the authoritative name servers responsible for the domain. For example: `example.com. 172800 IN NS a.iana-servers.net.`

### 5. Additional Section

This section may contain extra information, such as IP addresses for the authoritative name servers listed in the Authority section.

### 6. Footer / Stats

In the footer section, you find the latency time in milliseconds, in addition to which DNS server was used to solve the request.

---

## Common DNS Record Types

| Record | Purpose |
|--------|---------|
| `A` | IPv4 address of a domain |
| `AAAA` | IPv6 address of a domain |
| `MX` | Mail exchange servers |
| `NS` | Authoritative name servers |
| `CNAME` | Canonical name (alias) |
| `TXT` | Text records (SPF, DKIM, etc.) |
| `PTR` | Reverse DNS (IP → hostname) |
| `SOA` | Start of Authority record |

---

## Practical Examples

### 1. Basic DNS Lookup (A Record)

```bash
dig google.com
```

### 2. Short Output Only

```bash
dig +short google.com
```

`+short` displays only the most relevant information, such as the IP address for an A record.

### 3. Query a Specific Record Type

```bash
dig google.com MX
dig google.com NS
dig google.com TXT
dig google.com AAAA
```

### 4. Query Using a Specific DNS Server

```bash
dig @8.8.8.8 google.com
```

By default, the `dig` command queries the name servers listed in `/etc/resolv.conf`. You can change this using the `@` symbol followed by a hostname or IP address of the name server.

### 5. Trace the Full DNS Resolution Path

```bash
dig +trace google.com
```

The `+trace` command is used for tracing the DNS lookup path. This option makes iterative queries to resolve the name lookup, querying name servers starting from the root and traversing down the namespace tree using iterative queries following referrals along the way.

### 6. Reverse DNS Lookup (IP to Hostname)

```bash
dig -x 8.8.8.8
```

Use the `-x` option with an IP address to find the associated domain name. Reverse DNS lookup will only work if a PTR record is present.

### 7. Query Only the Answer Section (Clean Output)

```bash
dig +noall +answer google.com
```

`+noall` suppresses all sections of the output except those explicitly requested. `+answer` shows only the answer section of the output, and is typically used with `+noall`.

### 8. Batch Query from a File

```bash
dig -f domains.txt +short
```

Instead of performing a `dig` query for each domain at a time, a list of domains can be queried at once. Enter the domain names in a file (1 domain per line) and perform the `dig` query on the file.

### 9. Check DNSSEC Information

```bash
dig +dnssec google.com
```

This command queries DNS records with DNSSEC (Domain Name System Security Extensions) information.

### 10. Get Statistics

```bash
dig +stats google.com
```

The `+stats` option is used to view the statistics section.

---

## Key Options Summary

| Option | Description |
|--------|-------------|
| `+short` | Show only the essential result |
| `+noall` | Suppress all output sections |
| `+answer` | Show only the answer section |
| `+trace` | Trace full resolution from root |
| `+nocmd` | Omit the initial command line |
| `+stats` | Show query statistics |
| `+dnssec` | Include DNSSEC data |
| `@server` | Query a specific DNS server |
| `-x` | Reverse DNS lookup |
| `-f file` | Batch lookup from file |

---

## `dig` vs `nslookup`

`dig` provides more detailed output and advanced query options, while `nslookup` is simpler but less powerful for DNS troubleshooting. Most DNS administrators and sysadmins prefer `dig` due to its scriptability and comprehensive output.

---

## Common Use Cases

You can use the `dig` command to: diagnose your name servers; check all of them or each individual server and their response; check all of the available DNS records or individual DNS records and their parameters; trace IP addresses and see the hostnames that correspond to them; do a query through a specific port; see the TTL value of the DNS records; and trace the route of a DNS query.

---

**References:**

- [phoenixnap.com — dig Command in Linux with Examples](https://phoenixnap.com/kb/linux-dig-command-examples)
- [geeksforgeeks.org — dig command in Linux with Examples](https://www.geeksforgeeks.org/linux-unix/dig-command-in-linux-with-examples/)
- [linuxize.com — How to Use dig Command to Query DNS](https://linuxize.com/post/how-to-use-dig-command-to-query-dns-in-linux/)
- [cloudns.net — 10 Most Used DIG Commands](https://www.cloudns.net/blog/10-most-used-dig-commands/)
- [ditig.com — Dig Cheat Sheet](https://www.ditig.com/dig-cheat-sheet)
- [cyberciti.biz — Linux and Unix dig Command Examples](https://www.cyberciti.biz/faq/linux-unix-dig-command-examples-usage-syntax/)
- [howtouselinux.com — Dig Command in Linux: A Comprehensive Guide](https://www.howtouselinux.com/post/linux-dig-dns)
