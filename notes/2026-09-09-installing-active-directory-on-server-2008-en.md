---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing Active Directory on Server 2008
translated: false
type: note
---

Question: **What is Active Directory, and how do I install it on Windows Server 2008? What are the prerequisites?**

Answer:

## 1. What is Active Directory?

**Active Directory (AD)** is Microsoft's directory service for managing computers, users, groups, and policies in a Windows domain.

The core idea is:

```text
                    Active Directory
                          │
                    Domain Controller
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Users            Groups         Computers
          │
       Policies
          │
    Authentication
```

Instead of every PC having its own independent accounts:

```text
PC1:
  alice
  bob

PC2:
  alice
  bob

PC3:
  alice
  bob
```

you create a central domain:

```text
                  example.local
                       │
              Domain Controller
                       │
        ┌──────────────┼──────────────┐
        │              │              │
      Alice           Bob          Admins
        │              │
      PC-01           PC-02
```

Then Alice can log into a domain-joined computer using:

```text
EXAMPLE\alice
```

The Domain Controller authenticates her and applies the organization's policies.

AD is built around several important concepts:

| Concept                    | Meaning                                               |
| -------------------------- | ----------------------------------------------------- |
| **Domain**                 | Administrative/security boundary                      |
| **Domain Controller (DC)** | Server running AD DS                                  |
| **AD DS**                  | Active Directory Domain Services                      |
| **User**                   | Identity/account                                      |
| **Group**                  | Collection of users/computers                         |
| **OU**                     | Organizational Unit; container for organizing objects |
| **Group Policy**           | Centralized configuration/security rules              |
| **DNS**                    | Critical for locating AD services                     |
| **Kerberos**               | Main authentication protocol                          |

---

# 2. Windows Server 2008 terminology

On Windows Server 2008, you install the **Active Directory Domain Services (AD DS)** role.

There are two major steps:

```text
Windows Server 2008
        │
        ▼
Install AD DS role
        │
        ▼
Run dcpromo
        │
        ▼
Promote server to Domain Controller
```

`dcpromo` is particularly important in Server 2008.

---

# 3. Prerequisites

For a basic lab, you don't need much.

### Hardware

Something like:

```text
CPU:      1+ core
RAM:      2 GB+
Disk:     ~40 GB+
Network:  Ethernet/virtual NIC
```

For a real production DC, obviously use much more robust hardware/redundancy.

### OS

You need a Windows Server 2008 installation.

For example:

```text
Windows Server 2008 Standard
Windows Server 2008 Enterprise
Windows Server 2008 Datacenter
```

Preferably **x64** for a serious environment.

---

# 4. Give the server a static IP

This is important.

For example:

```text
IP:       192.168.1.10
Mask:     255.255.255.0
Gateway:  192.168.1.1
DNS:      192.168.1.10
```

Notice:

```text
DNS = itself
```

Once this machine becomes a DC and DNS server, it will normally provide DNS for the domain.

Don't build an AD environment where the DC's address changes randomly.

---

# 5. Give the server a sensible hostname

For example:

```text
DC01
```

You can do:

```text
Control Panel
    → System
    → Change settings
    → Computer Name
    → Change
```

Set:

```text
Computer name: DC01
```

Then reboot.

I'd use something like:

```text
DC01.example.local
```

rather than leaving the machine as:

```text
WIN-ABC123
```

---

# 6. Install Active Directory Domain Services

On Server 2008:

```text
Server Manager
    → Roles
    → Add Roles
```

Select:

```text
Active Directory Domain Services
```

Then:

```text
Install
```

After the role installation completes, **the machine is not yet a Domain Controller**.

This distinction is important:

```text
AD DS role installed
        ≠
Domain Controller
```

You still need to promote it.

---

# 7. Run `dcpromo`

Open:

```text
Start
→ Run
```

and execute:

```cmd
dcpromo
```

You should get the Active Directory Domain Services Installation Wizard.

The wizard essentially asks:

> What kind of AD domain do you want to create/join?

For your first server, choose:

```text
Create a new domain in a new forest
```

Then enter a domain name.

For a lab:

```text
example.local
```

or:

```text
ad.example.com
```

For learning, `example.local` is fine.

---

# 8. Choose the forest/domain functional level

For a pure Server 2008 lab, you can select an appropriate Server 2008 functional level.

Conceptually:

```text
Forest
└── Domain
    └── Domain Controllers
```

The **forest** is the highest-level AD boundary.

For your first installation:

```text
New forest
    ↓
New domain
    ↓
This server becomes first DC
```

---

# 9. DNS

The wizard will ask about DNS.

For a normal AD deployment, you generally want DNS installed/configured with the domain controller.

Why?

Because AD isn't simply:

```text
LDAP + users
```

DNS is fundamental to AD service discovery.

A client needs to discover things like:

```text
Where is the Domain Controller?
Where is Kerberos?
Where is LDAP?
Where are the domain services?
```

DNS records allow it to discover those services.

Conceptually:

```text
PC01
 │
 │ DNS query
 ▼
DNS
 │
 ├── _ldap._tcp
 ├── _kerberos._tcp
 └── DC01
       │
       ▼
Domain Controller
```

This is one of the most important things to understand when learning AD.

---

# 10. Directory Services Restore Mode password

The wizard asks you to create a:

```text
Directory Services Restore Mode (DSRM)
```

password.

This is **not simply the normal domain administrator password**.

Keep it somewhere safe.

It's used for special AD recovery/maintenance operations.

---

# 11. Database locations

You'll see paths such as:

```text
C:\Windows\NTDS
C:\Windows\SYSVOL
```

For a simple lab, accepting the defaults is fine.

The important pieces are roughly:

```text
NTDS
 └── Active Directory database

SYSVOL
 └── Group Policy
 └── logon scripts
 └── replicated domain files
```

The AD database is commonly:

```text
NTDS.dit
```

That's one of the central files of Active Directory.

---

# 12. Reboot

After `dcpromo` finishes:

```text
reboot
```

Now your server has become a Domain Controller.

Before:

```text
Windows Server
```

After:

```text
Windows Server
     +
AD DS
     +
DNS
     +
Domain Controller
     +
Kerberos
     +
LDAP
     +
SYSVOL
```

---

# 13. Verify it

After reboot, open:

```cmd
dsa.msc
```

This opens:

```text
Active Directory Users and Computers
```

You should see your domain:

```text
example.local
```

You can also run:

```cmd
dcdiag
```

This performs a series of Domain Controller diagnostics.

And:

```cmd
ipconfig /all
```

Check that DNS points to your AD DNS server.

You can also inspect:

```cmd
nslookup
```

and:

```cmd
net share
```

A healthy DC should expose things such as:

```text
NETLOGON
SYSVOL
```

---

# 14. Join another Windows machine

Now suppose you have:

```text
DC01
192.168.1.10
example.local
```

and another machine:

```text
PC01
192.168.1.20
```

Configure PC01's DNS:

```text
DNS server = 192.168.1.10
```

**This is critical.**

Then:

```text
PC01
  │
  │ DNS
  ▼
192.168.1.10
  │
  ▼
DC01
  │
  ▼
example.local
```

On PC01:

```text
System
→ Computer Name
→ Change
→ Domain
```

enter:

```text
example.local
```

Windows asks for domain credentials.

After successful authentication, reboot.

Now you can log in as:

```text
EXAMPLE\alice
```

instead of a purely local account:

```text
PC01\alice
```

---

# 15. The minimal lab architecture

If you're learning AD, I'd actually build this as a VM lab:

```text
             Virtual Network
                  │
       ┌──────────┴──────────┐
       │                     │
     DC01                  PC01
       │                     │
 Windows Server 2008      Windows 7
       │
 AD DS
 DNS
 Kerberos
 LDAP
```

Example:

```text
DC01
IP:       192.168.100.10
DNS:      192.168.100.10
Domain:   lab.local

PC01
IP:       192.168.100.20
DNS:      192.168.100.10
Domain:   lab.local
```

Then experiment with:

```text
Users
Groups
OUs
Group Policy
Domain join
Kerberos
DNS
LDAP
NTLM
File permissions
Login scripts
```

That gives you a much better understanding than simply clicking through the installation wizard.

One important caveat: **Windows Server 2008 is extremely old and unsupported today.** It's useful for understanding legacy AD and historical environments, but for a fresh lab I'd normally use a newer Windows Server version unless you're specifically trying to reproduce a 2008 environment.
