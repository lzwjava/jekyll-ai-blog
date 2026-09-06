---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cacti Network Monitoring Overview
translated: false
type: note
---

**Question:** What is Cacti, the network monitoring software?

**Answer:**

**What is Cacti?**

Cacti is an open-source, web-based network monitoring, performance, fault, and configuration management framework designed as a front-end application for the open-source, industry-standard data logging tool RRDtool.

**Origins**

Cacti originated in 2001 when Ian Berry, a high school student working at a small ISP, recognized a need for an accessible and efficient tool to visualize and monitor network data. Drawing on his programming skills in PHP and MySQL, Berry developed Cacti to make data monitoring more user-friendly than RRDtool, the existing tool at the time.

**Core Technology Stack**

Cacti uses RRDtool, PHP, and stores data in MySQL. It supports the use of SNMP and graphics with RRDtool. Cacti is a complete frontend to RRDtool — it stores all of the necessary information to create graphs and populate them with data in a MySQL database, and the frontend is completely PHP-driven.

**What It Monitors**

Cacti is designed to visualize time-series data such as CPU load, bandwidth usage, disk I/O, and memory utilization. It relies on SNMP data provided by network devices (routers, switches, servers, etc.), then processes and presents this data graphically, allowing users to easily identify trends.

**Key Features**

Cacti fully supports SNMPv1, SNMPv2, and SNMPv3, making it compatible with nearly all network devices. Graph templates allow quick creation of consistent, reusable performance charts, and admins can replicate graphs for hundreds of devices with minimal manual work.

The Cacti end-user front end supports both User and User Groups security models and supports Role Based Access Control (RBAC). Source users can be locally defined or sourced from LDAP, Active Directory, and other protocols via Apache and Nginx Basic Authentication, including Single Sign-On (SSO) providers. The Cacti framework can also be extended with plugins to add additional features.

**Who Uses It?**

Cacti is primarily used by Telco providers and Network Operation Centers throughout the world, in addition to being the heart of the commercial Spectrum LSF RTM solution which monitors High Performance Computing (HPC) clusters based on IBM LSF.

**Why Choose Cacti?**

Cacti offers enterprise-level monitoring without licensing costs, making it cost-effective for organizations of any size. Compared to heavy monitoring solutions like Zabbix or Nagios, Cacti consumes fewer system resources and remains stable even in long-term use.

---

**References:**

- [Cacti (software) — Wikipedia](https://en.wikipedia.org/wiki/Cacti_(software))
- [Vendor Insights: Cacti — Network Admin Tools](https://www.netadmintools.com/cacti/)
- [Cacti Monitoring Tool: A Complete Guide — bckinfo.com](https://bckinfo.com/cacti-monitoring-tool-a-complete-guide-for-modern-it-infrastructure/)
- [Cacti Software: Network Monitoring & Performance Tools — Click Magixo](https://clickmagixo.com/cacti-software)
- [Cacti official site](https://www.cacti.net/)
