---
audio: false
generated: true
image: false
lang: en
layout: post
title: Active Directory Domain Explained
translated: false
type: note
---

Question: What does **域 (domain)** mean in **Active Directory (AD)**?

Answer:

In **Active Directory**, **域 (domain)** is the **main administrative boundary and security unit** that groups users, computers, servers, and policies under one organization.

Think of an AD domain as a **managed namespace + security database**.

Example:

```
Company: example.com

Active Directory Domain:
    example.com

Objects inside:
    Users:
        alice@example.com
        bob@example.com

    Computers:
        PC001
        Server001

    Groups:
        Developers
        HR

    Policies:
        Password rules
        Software deployment
        Security settings
```

The domain is where AD stores and manages:

* **User accounts**
* **Computer accounts**
* **Groups**
* **Permissions**
* **Authentication information**
* **Group Policy settings**

When Alice logs into a company laptop:

```
Alice
  |
  | username/password
  v
Domain Controller
  |
  | checks AD database
  v
example.com domain
  |
  +--> Alice account exists?
  +--> Password correct?
  +--> Group memberships?
  +--> Policies?
```

The domain controller (DC) is the server that provides this service.

---

### Why call it "domain"?

It comes from the DNS concept of a domain.

For example:

```
example.com
```

is a DNS domain.

AD often uses the same namespace:

```
AD Domain:
    example.com

User:
    alice@example.com

Computer:
    laptop01.example.com
```

But AD domain is not just a website domain. It adds identity management and security.

---

### Domain vs Workgroup

Before AD, Windows used **workgroups**:

```
Workgroup:
    PC1
    PC2
    PC3
```

Each computer manages its own users:

```
PC1:
    Alice
    Bob

PC2:
    Alice
    Bob
```

Problems:

* Passwords duplicated
* No central control
* Hard to manage thousands of machines

AD domain:

```
             Domain Controller
                    |
          +---------+---------+
          |         |         |
        PC1       PC2       PC3
```

One identity system controls everything.

---

### Domain vs Forest vs Tree

AD hierarchy:

```
Forest
 |
 +-- Tree
      |
      +-- Domain
            |
            +-- Organizational Units (OU)
                  |
                  +-- Users
                  +-- Computers
                  +-- Groups
```

Example:

```
Forest:
    Microsoft Corporation

Domains:
    microsoft.com
    research.microsoft.com
    europe.microsoft.com
```

A **domain** is the basic management boundary.

A **forest** is the largest trust/security boundary.

---

A simple analogy:

* **Forest** = a country
* **Domain** = a province
* **OU** = a city/district
* **User/computer** = citizens/buildings

The domain answers: **"Who belongs to this organization, and what are they allowed to do?"**

I can also explain how **AD authentication works internally (Kerberos tickets, LDAP, NTLM)** if you are studying network/security.
