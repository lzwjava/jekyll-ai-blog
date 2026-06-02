---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Switching and Routing Technology Syllabus
translated: false
type: note
---

Question: Translate the provided Chinese text of the Guangdong Higher Education Self-Study Examination course syllabus for "Switching and Routing Technology" (course code: 13833) into English.

Answer:

# Guangdong Province Higher Education Self-Study Examination Course Syllabus: Switching and Routing Technology
(Course Code: 13833)

## I. Course Nature and Objectives

### 1. Course Nature and Characteristics
Through studying this course, students will gain a certain understanding of computer network knowledge, thereby acquiring the corresponding abilities of a network engineer.

### 2. Course Objectives
This book follows the tasks of actual enterprise network work as the main line, primarily explaining network fundamentals, switch configuration, router configuration, security configuration, IPv6 configuration, and comprehensive training. The content adopts a "project-task" structural system, introducing teaching projects from real-world work site requirements and practical applications, cultivating students' skills to complete work tasks and solve problems.
Through this course, students will master network fundamentals and common network protocols, learn to configure switches and routers from mainstream vendors according to different application environments and actual needs, develop the ability to build, manage, and maintain small and medium-sized enterprise networks, lay a solid foundation for future related applications, development, and further research in the field of network technology, align with the training objectives for high-quality technical skills talents, and meet the job requirements of related work fields and occupational positions in this major. This course plays a major supporting and significantly promoting role in cultivating students' professional qualities and abilities.

### 3. Connections and Differences with Related Courses
Studying this course requires basic computer knowledge and network fundamentals, as well as some understanding of computer network equipment. Prerequisite courses such as "Computer Network Technology" and "Structured Cabling Technology" provide basic understanding of computer network architecture and structured cabling system processing capabilities. This course provides supporting capabilities in network interconnection, network protocol applications, etc., for subsequent courses like "Network Management Training," "Network Attack and Defense Technology," and "Graduation Design."

### 4. Course Focus and Difficulties
This course is the core course in the "Network Construction and Management Capabilities" module of the Computer Network Technology major. The key focuses of this course are:
(1) Understand the content and knowledge areas involved in enterprise network planning and design, master network topology planning and IP address planning;
(2) Master the working principles and main functions of switches, master technologies and applications such as VLAN, Spanning Tree, and link aggregation;
(3) Master the working principles and main functions of routers, understand routing protocols like RIP and OSPF, master static routing, dynamic routing technologies, and route redistribution;
(4) Understand LAN access to the Internet technologies, common WAN protocols, master Network Address Translation (NAT) technology and applications;
(5) Master basic network security technologies, master Access Control List (ACL) technology and proficiently apply ACL to control network security;
(6) Familiar with installation and debugging techniques for common network equipment.

## II. Assessment Objectives
This book follows the tasks of actual enterprise network work as the main line, primarily explaining network fundamentals, switch configuration, router configuration, security configuration, IPv6 configuration, and comprehensive training. The content adopts a "project-task" structural system. The main assessment objectives are:

**Memorization:**
(1) Proficiently master IP address subnetting planning, independently complete IP address planning and reasonable allocation for a medium-sized campus network;
(2) Proficiently consult relevant technical manuals and materials, troubleshoot configuration errors according to manual guidance;

**Comprehension:**
(3) Proficiently complete basic configuration of switches (Layer 2 and Layer 3 switches); according to network business needs, correctly configure and apply network performance optimization technologies such as VLAN, Spanning Tree, and link aggregation; master basic capabilities in building switched networks;
(4) Proficiently complete basic router configuration; according to network business needs and actual engineering environments, correctly plan and set up network routing, including static and dynamic routing configuration; master basic inter-network interconnection capabilities;
(5) Configure WAN protocols (e.g., PPP); proficiently master router Network Address Translation (NAT) configuration and applications;
(6) Master switch and router network security configurations, proficiently write Access Control Lists (ACL), apply ACL technology to control network security;

**Application:**
(7) Correctly select switches, routers, and other network equipment to build small and medium-sized enterprise networks; initially possess comprehensive configuration and debugging capabilities for network equipment; possess basic network management and maintenance abilities.

## III. Course Content and Assessment Requirements

### Project 1: Understanding eNSP and Basic VRP Operations

#### 1. Learning Objectives and Requirements
1. Understand the role of the eNSP simulator;
2. Understand the origin and development of the VRP operating system;
3. Recognize the eNSP main interface and network connection cables;
4. Familiarize with VRP command views and basic operations.

#### 2. Assessment Knowledge Points and Requirements
1. Understanding eNSP and Basic VRP Operations
**Memorization:** Understand the role of the eNSP simulator; understand the origin and development of the VRP operating system; recognize the eNSP main interface and network connection cables.
**Comprehension:** Familiarize with VRP commands and basic operations.
**Application:** Correctly install the eNSP simulator; use eNSP to build and configure networks; master VRP platform applications; familiarize with basic VRP operations.

#### 3. Chapter Focus and Difficulties
1. Teaching Focus: eNSP simulator installation steps, adding network devices, and connecting device cables; Teaching Difficulty: eNSP simulator installation;
2. Learning Difficulty: Proficiently mastering relevant VRP command statements.

### Project 2: Building a Small Campus Network Using Switches

#### 1. Learning Objectives and Requirements
Switch technology plays a pivotal role in modern high-speed networks, with enterprise networks relying on switches to segment networks and achieve high-speed connections. Switches are classified into multiple levels, generally Layer 2 and Layer 3 switches. Layer 2 switches are data link layer devices that recognize MAC address information in packets, forward based on MAC addresses, and record these MAC addresses with corresponding ports in an internal address table. The most important function of Layer 3 switches is to accelerate fast forwarding of data within large LANs, incorporating routing forwarding capabilities. Switches have wide applications: in simple scenarios, they can replace hubs as central connection points for multiple hosts; in complex applications, switches can connect to one or more other switches to establish, manage, and maintain redundant links and VLAN connectivity. Through learning and practice in this chapter, students will become familiar with switch configuration and proficient in switch management and maintenance.

Learning Objectives:
1. Use terminal software to correctly connect to switches;
2. Proficiently configure various network parameters and port statuses on switches;
3. Learn methods for dividing VLANs on switches;
4. Learn methods for configuring communication within the same VLAN across switches;
5. Learn methods for achieving inter-VLAN communication using Layer 3 switches;
6. Proficiently configure switch link aggregation technology;
7. Proficiently configure Spanning Tree and Rapid Spanning Tree;
8. Proficiently configure switch VRRP technology;
9. Proficiently configure switch DHCP technology.

#### 2. Assessment Knowledge Points and Requirements
1. **Basic Switch Configuration**
**Memorization:** Switch management methods; Console port login management; Switch command view modes.
**Comprehension:** Switch port types; Switch port duplex modes; Switch port speeds.
**Application:** Basic switch configuration.

2. **Achieving Network Isolation Between Different Departments**
**Memorization:** VLAN technology introduction; VLAN frame format; VLAN division methods.
**Comprehension:** Advantages and disadvantages of VLAN technology.
**Application:** VLAN technology working principles; Key VLAN command formats.

3. **Achieving Cross-Switch Access Within the Same Department**
**Memorization:** Link types; Port types; Processing of packets received/sent by different port types.
**Comprehension:** Role of Trunk links; Differences between Access and Trunk ports.
**Application:** Cross-switch VLAN working principles; Access and Trunk port configuration commands; Configuration for computer communication in the same VLAN across different switches.

4. **Using Layer 3 Switches to Achieve Inter-Department Network Access**
**Memorization:** Layer 3 switches; Differences between Layer 3 and Layer 2 switches.
**Comprehension:** Differences between Layer 3 switches and routers; Layer 3 switch routing principles.
**Application:** Connections between computers, switches, and routers; Inter-VLAN routing configuration; VLAN configuration.

5. **Improving Backbone Link Bandwidth**
**Memorization:** Link aggregation.
**Comprehension:** Advantages of link aggregation.
**Application:** Link aggregation configuration.

6. **Avoiding Network Loops**
**Memorization:** Network loops; STP; RSTP.
**Comprehension:** Principles of network loop generation; Basic principles and processes of STP and RSTP.
**Application:** RSTP configuration.

7. **Improving Network Stability**
**Memorization:** VRRP related terms; Virtual router.
**Comprehension:** Role and working process of VRRP.
**Application:** VRRP configuration; Tracert command configuration and role.

8. **Achieving Dynamic Address Acquisition for Department Computers**
**Memorization:** DNS addresses; IP address conflicts; DHCP technology.
**Comprehension:** Role of DHCP technology.
**Application:** DHCP configuration; DHCP service troubleshooting.

#### 3. Chapter Focus and Difficulties
The focus of this chapter is to first understand the working principles of Layer 2 and Layer 3 switches, the functions of switches, and the effects of these functions. Familiarize with and understand the role of VLAN division, as well as how different switch port types process VLAN data frames. How to correctly configure switches to enable related functions, thereby completing the construction of a small campus network.
The difficulty is familiarizing with configuration commands for various switch functions, and performing reliability design and configuration tasks for small campus network projects.

### Project 3: Building a Medium-Sized Campus Network Using Routers

#### 1. Learning Objectives and Requirements
Routers are indispensable network devices connecting various LANs and WANs on the Internet. They automatically select routes based on the overall network communication situation, sending information to other network devices in the best path and in sequence, thereby achieving routing and forwarding of information. The continuous expansion of network scale provides a good foundation and broad platform for the development of "routing." As the Internet's requirements for data transmission efficiency increase, the role of "routing" in network communication becomes increasingly important.
Routers provide mechanisms for heterogeneous network interconnection, enabling data packets from one network to be sent to another. Routing is the path information guiding IP packet transmission. Routing protocols are pre-agreed rules and standards in the process of guiding IP packet transmission. Routing protocols support routable protocols by sharing routing information between routers. Routing information is passed between adjacent routers, ensuring all routers know paths to other routers. In summary, routing protocols create routing tables describing network topology; routing protocols work with routers to perform route selection and packet forwarding. In practical applications, routers typically connect many different networks; to achieve communication between multiple networks, routing protocols must be configured on routers.

Learning Objectives:
1. Achieve router settings in the simulator;
2. Proficiently use basic router configuration commands;
3. Achieve router one-arm routing configuration;
4. Achieve two methods of router DHCP configuration;
5. Achieve static routing configuration for routers and Layer 3 switches;
6. Achieve default routing configuration for routers and Layer 3 switches;
7. Achieve floating routing configuration for routers and Layer 3 switches;
8. Achieve dynamic routing RIPv2 protocol configuration for routers and Layer 3 switches;
9. Achieve dynamic routing OSPF protocol configuration for routers and Layer 3 switches.

#### 2. Assessment Knowledge Points and Requirements
1. **Router Configuration in Simulator**
**Memorization:** Console port login management; Router command view modes.
**Comprehension:** Router port types; Router module addition; Router port naming rules.
**Application:** Proficiently switch between different router ports.

2. **Basic Router Configuration**
**Memorization:** Understanding routers; Representation of router modules and port types.
**Comprehension:** Router working principles and roles.
**Application:** Basic router command applications, achieving basic router configuration.

3. **Achieving Dynamic Address Acquisition for Department Computers**
**Memorization:** DHCP; Interface address pool; Global address pool.
**Comprehension:** Role of DHCP; Differences between interface and global address pools.
**Application:** Correctly implement two methods for DHCP dynamic acquisition on routers.

4. **Using One-Arm Routing to Achieve Inter-Department Network Access**
**Memorization:** One-arm routing; ARP broadcast.
**Comprehension:** One-arm routing working principles; Role of ARP broadcast.
**Application:** Correctly implement one-arm routing configuration; correctly enable ARP broadcast function.

5. **Using Static Routing to Achieve Network Connectivity**
**Memorization:** Static routing; Routing table.
**Comprehension:** Principles and role of static routing.
**Application:** Implement static routing configuration; view routing table for simple fault analysis.

6. **Using Default and Floating Routing to Achieve Network Connectivity**
**Memorization:** Default routing; Floating routing.
**Comprehension:** Principles and role of default routing; Principles and application scenarios of floating routing.
**Application:** Correctly implement default and floating routing configuration.

7. **Using Dynamic Routing RIPv2 Protocol to Achieve Network Connectivity**
**Memorization:** RIP introduction; RIP versions; RIP timers.
**Comprehension:** Principles and role of RIP; Differences between RIPv1 and RIPv2.
**Application:** Correctly implement RIPv2 configuration; resolve routing configuration faults.

8. **Using Dynamic Routing OSPF Protocol to Achieve Network Connectivity**
**Memorization:** OSPF protocol introduction; OSPF protocol areas.
**Comprehension:** Principles and role of OSPF protocol; Role of OSPF areas and differences between backbone and non-backbone areas.
**Application:** Correctly implement single-area OSPF configuration.

#### 3. Chapter Focus and Difficulties
The focus of this chapter is to first understand router working principles, router functions, and the effects of these functions. Proficiently master router configuration commands, initially possess fault analysis methods. Distinguish connections and differences between routers and Layer 3 switches. How to correctly configure routers to enable related functions, thereby completing the construction of a medium-sized campus network.
The difficulty is familiarizing with configuration commands for various router functions, as well as routing protocol configuration commands and working principles, and designing and completing configuration tasks for medium-sized campus network projects.
