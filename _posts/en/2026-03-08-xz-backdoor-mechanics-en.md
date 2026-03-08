---
audio: false
generated: true
image: false
lang: en
layout: post
title: XZ Backdoor Discovery and Mechanics
translated: false
type: note
---

**Question:** How did Andres Freund discover a 500ms SSH login delay and subsequently uncover a hidden backdoor in XZ Utils? Provide a comprehensive explanation, including how the backdoor technically works.

---

**Answer:**

## The XZ Utils Backdoor (CVE-2024-3094): A Comprehensive Story

---

### 1. Who is Andres Freund?

Andres Freund is a Microsoft employee and PostgreSQL developer. He is not a dedicated security researcher — he stumbled upon one of the most dangerous supply chain attacks in Linux history almost by accident.

---

### 2. How He Noticed the Problem

In March 2024, while benchmarking PostgreSQL on Debian Sid, Freund noticed SSH logins were taking 500ms instead of the normal 100ms. That seemingly trivial half-second difference was the first crack in the facade.

He also noticed that `sshd` processes were consuming a surprising amount of CPU, even when immediately failing due to wrong usernames.

Being the careful engineer he is, he ran Valgrind — a memory debugging tool — and it threw errors on the affected system. He traced it to `liblzma`, the compression library provided by XZ Utils.

On March 29, 2024, Freund shared the information on the oss-security mailing list, identifying malicious commits to the command-line utility XZ, impacting versions 5.6.0 and 5.6.1 for Linux.

---

### 3. The Multi-Year Social Engineering Campaign Behind It

This was not a simple hack. It was a **years-long, state-level-quality operation.**

A subsequent investigation found the campaign to insert the backdoor was a culmination of approximately three years of effort, between November 2021 and February 2024, by a user going by the name "Jia Tan" (GitHub handle JiaT75), who worked to gain a position of trust within the project.

The campaign involved:

**Step 1 — Building credibility.** Jia Tan started submitting legitimate, helpful patches to XZ Utils starting in early 2022. The code was good. The contributions were consistent.

**Step 2 — Pressure via fake personas.** After a period of pressure on the founder and head maintainer to hand over control of the project via apparent sock puppetry, Jia Tan gained the position of co-maintainer of XZ Utils. Suspected fake accounts used to apply pressure included usernames like "Jigar Kumar", "krygorin4545", and "misoeater91".

**Step 3 — Weaponizing the release process.** The modified `build-to-host.m4` file existed only in the release tarball uploaded to GitHub, never in the git repository. Anyone reviewing the source code would see clean commits while the distributed software contained the backdoor.

**Step 4 — Covering tracks.** Jia Tan released XZ Utils 5.6.0 as a tarball, which included "test" files containing the backdoor in binary (not plain text) form, making them more obfuscated. Following 5.6.0, they rushed out a 5.6.1 release to fix some failures that were occurring with the backdoor before they were spotted.

---

### 4. How the Backdoor Was Hidden (Build System Injection)

The injection was extremely clever and multi-staged:

The `m4/build-to-host.m4` macro is executed during the build process. It "uncorrupts" a malformed XZ file disguised as a code test (`bad-3-corrupt_lzma2.xz`). Afterward, a malicious Bash script is extracted and decrypted from another decoy test archive (`good-large-compressed.lzma`). This Bash script then extracts a binary file, decrypts it, and saves it as `liblzma_la-crc64-fast.o`, which gets added to the liblzma compilation process.

The malicious script also checks for various conditions, like the architecture of the machine — it only targets `x86_64 linux-gnu` systems.

Investigations confirmed this is dormant malware targeting a very specific set of systems: specifically the `x86_64` architecture, requiring both systemd and sshd. It was not targeting BSDs, Android phones, Wi-Fi routers, IoT devices, or Raspberry Pis — essentially, it had to be a standard Linux server.

---

### 5. How the Backdoor Actually Works (Technical Deep Dive)

This is the most sophisticated part. Here is how the backdoor achieves **unauthenticated Remote Code Execution (RCE)**:

#### Step A — Getting Into sshd Without Touching OpenSSH Source Code

OpenSSH normally does not load `liblzma`, but a common third-party patch used by several Linux distributions causes it to load `libsystemd`, which in turn loads `liblzma`. The backdoor code uses the glibc IFUNC mechanism to replace an existing function in OpenSSH called `RSA_public_decrypt` with a malicious version.

#### Step B — What is IFUNC?

IFUNC (indirect function) is a glibc feature that allows runtime selection of optimized function implementations based on hardware capabilities. In June 2023, Jia Tan introduced IFUNC resolvers (`crc32_resolve`, `crc64_resolve`) through seemingly legitimate commits. These resolvers were then exploited to replace OpenSSH's `RSA_public_decrypt` function at runtime. Because IFUNC runs early in process initialization, it is particularly stealthy.

#### Step C — Function Hooking via rtld-audit

The attacker utilized the IFUNC and `rtld-audit` mechanisms to achieve hijack replacement of the `RSA_public_decrypt()` function. The backdoor sets three hook functions to increase success rate: `RSA_public_decrypt()`, `EVP_PKEY_set1_RSA()`, and `RSA_get0_key()`. If any of these are successfully hooked, the process exits and cleans up traces of the `rtld-audit`.

#### Step D — Delivering the Malicious Payload via RSA Key

Via this hook, the binary examines the RSA public modulus (the "N" value) passed inside the RSA struct. The value is decoded with a hardcoded decryption key, and the data's validity is checked using the **Ed448 elliptic curve signing algorithm**.

The hooked `RSA_public_decrypt` verifies a signature on the server's host key by a fixed Ed448 key, then passes a payload to `system()`. It is RCE — not just auth bypass — and the payload is gated and unreplayable. The payload is extracted from the N value (the public key) passed to `RSA_public_decrypt`, checked against a simple fingerprint, and decrypted with a fixed ChaCha20 key before the Ed448 signature verification.

This means: **only the attacker** who holds the corresponding Ed448 private key could trigger this backdoor.

#### Step E — No Logs Left Behind

No log messages at the INFO level or higher are written by OpenSSH when successful exploitation occurs. This makes detection by log analysis in production environments highly unlikely.

#### Step F — Anti-Replay Protection

The attacker set an anti-replay feature to avoid possible capture or hijacking of the backdoor communication. The backdoor also replaces the incoming RSA public key with an empty one after the main hook function completes, to avoid logging any malicious data from the attacker.

---

### 6. What Could Have Happened

This backdoor almost became one of the most widespread and effective intrusion enablers ever — one that would have dwarfed the SolarWinds backdoor. The attackers were almost able to gain immediate access to any Linux machine running an infected distro, which includes Fedora, Ubuntu, and Debian.

Alex Stamos noted this could have been "the most widespread and effective backdoor ever planted in any software product." Had it remained undetected, it would have given its creators a master key to any of the affected servers.

---

### 7. Why It Was Caught Just in Time

Standard static analysis and vulnerability scanning tools would not have caught this backdoor. The malicious code existed only in release tarballs (not Git), was obfuscated across multiple binary test files, and used legitimate build system mechanisms. Detection required observing runtime behavior anomalies — the 500ms SSH delay.

The backdoor had found its way into testing releases of distributions like Debian Sid, Fedora 41, and Fedora Rawhide, but was caught before propagating into more highly used stable releases.

---

### 8. Attribution

Security researcher Dave Aitel suggested the multi-year patience, operational security, and sophistication of the campaign align with APT29 (Cozy Bear) tradecraft, associated with Russia's Foreign Intelligence Service (SVR). While attribution remains unconfirmed, the resources and time invested in the campaign exceed what is typical for individual or criminal actors.

---

### Summary Flow Diagram

```
Jia Tan (2021–2024)
  └─► Gains trust as XZ maintainer
      └─► Injects malicious code in release tarballs only (not git)
          └─► Build process secretly compiles backdoor into liblzma
              └─► sshd loads libsystemd → loads liblzma (unintentional)
                  └─► IFUNC hook replaces RSA_public_decrypt at runtime
                      └─► Attacker sends SSH cert with embedded payload (in RSA N value)
                          └─► Ed448 signature verified → system() executes attacker's command
                              └─► Full RCE on server, pre-authentication, no logs
```

---

**References:**

- [Elastic Security Labs — 500ms to Midnight](https://www.elastic.co/security-labs/500ms-to-midnight)
- [Wikipedia — XZ Utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)
- [Akamai — XZ Utils Backdoor Everything You Need to Know](https://www.akamai.com/blog/security-research/critical-linux-backdoor-xz-utils-discovered-what-to-know)
- [SoftwareSeni — Multi-Year Social Engineering Campaign](https://www.softwareseni.com/the-xz-utils-backdoor-cve-2024-3094-and-the-multi-year-social-engineering-campaign-behind-it/)
- [GitHub — xz-utils backdoor situation (thesamesam)](https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27)
- [Pentest-Tools — CVE-2024-3094 Technical Analysis](https://pentest-tools.com/blog/xz-utils-backdoor-cve-2024-3094)
- [Securelist — XZ Backdoor Hook Analysis](https://securelist.com/xz-backdoor-part-3-hooking-ssh/113007/)
- [Red Hat — Understanding Red Hat's Response](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident)
- [Datadog Security Labs — CVE-2024-3094](https://securitylabs.datadoghq.com/articles/xz-backdoor-cve-2024-3094/)