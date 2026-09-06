---
audio: false
generated: true
image: false
lang: en
layout: post
title: IBM Tivoli NetView Introduction
translated: false
type: note
---

**Question:** What is IBM Tivoli NetView, and what is it used for?

**Answer:**

## IBM Tivoli NetView — Introduction

### What Is It?

IBM Tivoli NetView is distributed network management software that helps keep important business systems available. It discovers TCP/IP networks, displays topologies, monitors network health, and gathers performance data so that you can quickly identify the root cause of network failures.

Now officially known as **IBM Z NetView** (formerly IBM Tivoli NetView for z/OS), it provides functions to help maintain the highest degree of availability for IBM Z networks, offering an extensive set of tools for managing and maintaining complex, multivendor, multiplatform networks and systems from a single point of control.

---

### Core Purpose

NetView provides advanced correlation facilities to automate any network or system event, support for both TCP/IP and SNA networks, a set of user interfaces to meet the needs of any user, and management functions that work with other products to provide a complete picture of your networks and systems.

---

### Key Components

Using the NetView program, you can manage complex networks and systems from multiple independent software vendors from a single point. Its major components include:

- **Command Facility** — used to send commands and receive messages; provides base functions and services for other components such as intercomponent communication, presentation services, database services, and automation facilities.
- **Hardware Monitor** — collects and displays events and statistical data for both hardware and software to identify failing resources in a network, providing probable cause and recommended actions.
- **Session Monitor** — tracks SNA sessions across the network.
- **SNA Topology Manager** — manages System Network Architecture resources.
- **NetView Management Console** — the graphical workstation interface.
- **Correlation Engine** — correlates events to automate responses.
- **Integrated TCP/IP Services** — manages modern IP network resources.

---

### Automation Capabilities

Automated Operations Network (AON) is built into NetView and has components including Helpdesk, AutoView, Dynamic Display Facility (DDF), Control File and Common Routines. Originally a set of productivity aids, it eventually became a standard feature of NetView.

---

### Integration With Other IBM Products

Today, NetView integrates with other IBM Z tools like GDPS and Tivoli Business Service Manager. NetView also supports CICS, DB2, and IMS subsystem monitoring through the IBM System Z Automation product. NetView also supports enhanced logging and visualization through the Consolidated Audit, NetView, and z/OS Log (Canzlog) feature for consolidated message logging.

IBM Tivoli Network Manager IP Edition is also tightly integrated with IBM Tivoli Netcool/OMNIbus and, when installed together with the IBM Netcool Operations Insight infrastructure solution, serves as a key component providing network discovery, device monitoring, topology visualization, and root cause analysis (RCA) capabilities.

---

### In Summary

| Aspect | Detail |
| --- | --- |
| Vendor | IBM (Tivoli brand) |
| Platform | Primarily z/OS (mainframe) |
| Network Support | SNA + TCP/IP |
| Primary Use | Network monitoring, automation, fault management |
| Modern Name | IBM Z NetView |

---

**References:**

- [IBM Z NetView v6.3 Overview — IBM Docs](https://www.ibm.com/docs/SSZJDU_6.3.0/com.ibm.iznetview.doc_6.3.0/netv630_welcome_kc.htm)
- [Tivoli NetView — ESM Solutions](http://www.esm-solutions.com/software/tivoli/tivoli-netview.html)
- [A Love Letter to NetView — TechChannel](https://techchannel.com/networking/networking-management-and-monitoring/)
- [Tivoli Network Manager Support — IBM](https://www.ibm.com/mysupport/s/topic/0TO500000002JCmGAM/tivoli-network-manager)
