---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IPv6 Campus Network Project Guide
translated: false
type: note
---

Question: Translate the provided Chinese text about network course projects and self-study examination outline to English.

Answer: 

**Project 4: IPv6 Campus Network**

**I. Learning Objectives and Requirements**

With the development of the Internet, the number of users has increased rapidly, leading to a severe shortage of IPv4 addresses. By 2019, all IPv4 addresses had been allocated. To address the issues of IPv4 address shortage and poor security, the IETF proposed the next-generation Internet protocol—IPv6—in the 1990s. IPv6 uses 128-bit binary addresses, which not only solves the problem of network address resource scarcity but also provides support for the IP address demands of the Internet of Everything.

IPv6 supports an almost unlimited address space, employs new address configuration methods that simplify setup, and adopts a new packet format that improves packet processing efficiency, security, and better supports QoS.

As computer network technology advances, the application of IPv6 in enterprise networks is becoming more common. Building a campus network with IPv6 requires IPv6 routing technologies to achieve network communication.

**Learning Goals:**

1. Correctly perform basic IPv6 address configuration.

2. Correctly configure IPv6 static routes, default routes, and summary routes.

3. Use RIPng to achieve network connectivity.

4. Use OSPFv3 to achieve network connectivity.

**II. Assessment Knowledge Points and Requirements**

1. Basic IPv6 Address Configuration  
   - Memorize: Advantages of IPv6 addresses; IPv6 header structure.  
   - Understand: Differences between IPv6 and IPv4 in address length, packet format, and security; IPv6 address notation formats.  
   - Apply: Configure IPv6 addresses on different router interfaces.

2. Using IPv6 Static Routes and Default Routes to Achieve Network Connectivity  
   - Memorize: IPv6 address structure; IPv6 address types; IPv6 routing.  
   - Understand: Differences between IPv6 routing and IPv4 routing.  
   - Apply: Correctly configure IPv6 static routes; correctly configure IPv6 default routes; correctly configure IPv6 summary routes; describe various IPv6 address representations.

3. Using Dynamic Routing Protocol RIPng to Achieve Network Connectivity  
   - Memorize: RIPng; RIPng operation mechanism; RIPng packet format.  
   - Understand: Differences between RIPng and RIPv2; differences in configuration commands between RIPng and RIPv2.  
   - Apply: Correctly configure RIPng to achieve network connectivity.

4. Using Dynamic Routing Protocol OSPFv3 to Achieve Network Connectivity  
   - Memorize: Basic OSPFv3 concepts; OSPFv3 packets; OSPFv3 LSA types; OSPFv3 timers.  
   - Understand: Differences between OSPFv3 and OSPF.  
   - Apply: Correctly configure OSPFv3 routing protocol; flexibly use OSPFv3 to achieve network connectivity.

**III. Chapter Focus and Difficulties**

The focus of this chapter is to first understand the principles of IPv6 operation, the composition of IPv6 addresses, the functions provided by IPv6, and the effects of these functions. Proficiently master IPv6 address configuration commands on routers, master the configuration of IPv6 static routes, default routes, and summary routes, master RIPng configuration commands to achieve network connectivity, and especially master OSPFv3 configuration commands to achieve network connectivity, thereby completing the construction of a medium-sized campus network.

The difficulties are familiarizing oneself with the composition of IPv6 addresses, IPv6 configuration commands, routing protocol configuration commands and operating principles, and designing and completing configuration tasks for medium-sized campus network projects.

**Project 5: Building a Wireless Campus Network**

**I. Learning Objectives and Requirements**

With the rapid development of wireless network technology, mobile devices have become essential tools in people's lives and work, and wireless networks have become the most important access method for mobile terminals. The world has entered the mobile Internet era, with over 90% of Internet users accessing the Internet via wireless networks. China is vigorously promoting wireless network construction to achieve full coverage in areas such as rail transit, airports, schools, hospitals, and stations.

With the widespread use of mobile devices like smartphones, tablets, and laptops, Wireless Local Area Networks (WLAN) are increasingly applied in home networks, enterprise networks, industry networks, and operator networks.

Common WLAN networking methods include Fat AP and Fit AP. In home or small office networks, consumer-grade wireless routers cannot support roaming for wireless terminals in large-scale networks. Therefore, the scheme of Wireless Controller (Access Controller, AC) + Access Point (AP) is used for WLAN networking in large enterprises or campus networks, known as AC + Fit AP networking.

**Learning Goals:**

1. Correctly perform basic WLAN configuration.

2. Correctly perform WLAN security configuration.

3. Implement AC + AP direct-connected Layer 2 networking configuration.

4. Implement AC + AP side-hung Layer 3 networking configuration.

**II. Assessment Knowledge Points and Requirements**

1. Building Direct-Connected Layer 2 WLAN  
   - Memorize: Fat AP; Fit AP; AC controller; AC + Fit AP network construction; wireless radio frequency.  
   - Understand: Wireless network concepts; common wireless network devices; WLAN networking methods; WLAN forwarding modes.  
   - Apply: Proficiently master key WLAN configuration commands and formats; proficiently master DHCP server configuration; proficiently master Layer 2 switch configuration; proficiently master basic WLAN service configuration processes.

2. Building Side-Hung Layer 3 WLAN  
   - Memorize: Layer 3 networking; side-hung networking; WLAN roaming; black/white lists.  
   - Understand: Differences between Layer 3 and Layer 2 networking; advantages and disadvantages of side-hung Layer 3 WLAN.  
   - Apply: Proficiently master key WLAN configuration commands and formats; proficiently master DHCP server configuration; proficiently master Layer 3 WLAN networking configuration; proficiently master basic WLAN service configuration processes.

**III. Chapter Focus and Difficulties**

The focus is to understand WLAN operating principles, the functions of AC and AP, and the effects of these functions. Proficiently master WLAN configuration commands and initially acquire fault analysis methods. Distinguish the connections and differences between Layer 2 and Layer 3 WLAN. Correctly configure switches, routers, AC, and AP to implement WLAN functions and complete wireless campus network construction.

The difficulty is comprehensively mastering configuration commands for switches, routers, AC, AP, and other devices, possessing fault analysis and troubleshooting capabilities, and proficiently mastering basic WLAN service configuration processes to complete wireless campus network configuration tasks.

**Project 6: Building a Secure Campus Network**

**I. Learning Objectives and Requirements**

As network technology develops and its applications expand, networks have become indispensable in daily life. Campus networks, providing access and basic services to end users, face increasing security risks, such as non-human or natural faults, unintentional operational errors causing data loss, and malicious attacks from external or internal sources. Network security directly affects learning, work, and life, making it a focal point of societal concern, necessitating network security measures.

Measures to protect campus network security include installing antivirus software on hosts, using switch port security to prevent MAC, ARP, IP/MAC spoofing attacks, using IP access control lists (ACLs) to filter traffic and protect inter-subnet communication and sensitive devices, using NAT for internal host privacy protection, deploying firewalls at network exits to prevent unauthorized access and attacks, and establishing internal network security policies.

**Learning Goals:**

1. Implement switch port security configuration.

2. Implement remote management of network devices.

3. Implement basic ACL configuration.

4. Implement advanced ACL configuration.

5. Use dynamic NAPT to enable LAN access to the Internet.

6. Use static NAT to allow external hosts to access internal servers.

7. Perform basic firewall configuration and security policy configuration.

8. Implement NAT configuration to protect internal network security.

**II. Assessment Knowledge Points and Requirements**

1. Secure Computer Access  
   - Memorize: Port security dynamic MAC addresses; sticky MAC addresses.  
   - Understand: Role of port security; port security protection actions.  
   - Apply: Proficiently configure port security.

2. Remote Management of Network Devices  
   - Memorize: Telnet and STelnet; user authentication.  
   - Understand: Advantages and disadvantages of remote management; remote management security.  
   - Apply: Enable and configure remote management on switches and routers; correctly configure password and AAA authentication for remote management.

3. Using Basic ACL to Restrict Network Access  
   - Memorize: ACL rule principles; ACL rule matching order; ACL classifications.  
   - Understand: Main role of ACLs; ACL rule principles and matching.  
   - Apply: Proficiently configure basic ACLs on routers or switches.

4. Using Advanced ACL to Protect Server Ports from Attacks  
   - Memorize: Advanced ACL; IP protocol ports vs. router physical ports.  
   - Understand: Main role of advanced ACLs; advanced ACL rule principles and matching; differences from basic ACLs.  
   - Apply: Proficiently configure advanced ACLs; distinguish applications of both ACL types in different scenarios.

5. Secure Campus Network Internet Access  
   - Memorize: PPP; PAP; CHAP.  
   - Understand: Roles and differences between PAP and CHAP; application scenarios.  
   - Apply: Determine whether to use PAP or CHAP based on situations and configure correctly.

6. Using Static NAT for Internal Servers to Publish to the Internet  
   - Memorize: NAT; NAT types.  
   - Understand: NAT roles and advantages; NAT types and principles.  
   - Apply: Correctly configure static NAT.

7. Using Dynamic NAPT for LAN Hosts to Access the Internet  
   - Memorize: Dynamic NAT.  
   - Understand: Dynamic NAT roles, advantages, and principles.  
   - Apply: Correctly configure dynamic NAT.

8. Using Firewall to Hide Internal Network Addresses and Protect Internal Security  
   - Memorize: Firewall key technologies; security zones; firewall security policies; firewall operating modes.  
   - Understand: Firewall principles and functions; related configurations or devices for network security.  
   - Apply: Correctly plan and configure network security.

**III. Chapter Focus and Difficulties**

The focus is on advanced ACL principles and specific application configurations; understand ACL operating principles, functions, and effects, and proficiently select different ACLs based on scenarios. Master ACL configuration commands and initial fault analysis methods. Distinguish connections and differences between basic and advanced ACLs.

The difficulty is understanding advanced ACL principles, completing corresponding configurations, and troubleshooting advanced ACL issues. Learn to optimize advanced ACL command order or statements to improve efficiency.

**Project 7: Comprehensive Campus Network Training**

**I. Learning Objectives and Requirements**

With continuous technological progress, enterprise LAN construction and functions are becoming more complex. Equipment performance and status increasingly affect production quality and costs. Effectively building and maintaining unit computer networks to ensure safe and stable operation is a critical task for network maintenance personnel.

Deeply understand computer network principles, combine abstract concepts with practical technologies, further familiarize with switches, routers, and other devices, master general principles and steps for small- to medium-sized campus network system integration. Cultivate skills in network service construction, daily maintenance, and management, equipping students with essential knowledge and operational skills for network construction in an information society. Further develop self-learning ability and independent problem analysis and solving skills. For design issues, seek solutions through independent thinking, reference materials, and literature.

**Learning Goals:**

1. Implement network device management and maintenance.

2. Implement Layer 3 network architecture LAN communication.

3. Implement MSTP and VRRP for load-balanced enterprise networks.

4. Implement router DHCP service configuration.

5. Apply different routing protocols in enterprise networks.

6. Implement wireless network setup.

7. Implement firewall protection for enterprise networks.

**II. Assessment Knowledge Points and Requirements**

1. Network Device Management and Maintenance  
   - Memorize: Device communication status checks.  
   - Understand: Importance of device management and maintenance.  
   - Apply: Backup and restore device configuration files; manage backup file versions.

2. Load-Balanced Campus Network Comprehensive Training  
   - Memorize: MSTP (Multiple Spanning Tree Protocol); VRRP (Virtual Router Redundancy Protocol).  
   - Understand: Campus internal network setup processes and methods.  
   - Apply: Comprehensively apply VLAN, Trunk, link aggregation, switch DHCP service, static routing, OSPF dynamic routing, AC, AP, NAT, PPP, CHAP, MSTP, VRRP, etc., to build a classic Layer 3 campus network model.

3. Enterprise Network Comprehensive Training  
   - Memorize: Enterprise internal setup; enterprise wireless network setup.  
   - Understand: Campus internal network setup processes and methods.  
   - Apply: Comprehensively apply VLAN, SVI, router DHCP service configuration, NAT, static routing protocols, wireless configuration, firewall, OSPF, etc., to deepen proficiency in campus network technologies.

**III. Chapter Focus and Difficulties**

The focus is using learned knowledge to configure switches, routers, firewalls, AC, AP, etc., master basic steps and processes for campus LAN setup, master LAN security technologies and protection measures, and implement LAN construction and configuration.

The difficulty is troubleshooting complex network faults, which often requires multi-angle testing and analysis. Through experience, accurately identify fault points. More practice and summarization are needed to reduce errors in networking, quickly solve problems, and improve experience and capabilities.

**IV. Explanation of the Outline and Assessment Implementation Requirements**

**I. Purpose and Role of the Course Self-Study Examination Outline**

The course self-study examination outline is determined based on the professional self-study examination plan and the characteristics of self-study examinations. Its purpose is to guide and regulate individual self-study, social assistance, and course examination proposition.

The outline specifies the course learning content and depth, defines the scope and standards of the self-study examination. It serves as the basis for writing self-study textbooks and counseling materials, for social assistance organizations in counseling, for self-learners in studying textbooks and mastering content scope and depth, and for examination proposition.

**II. Relationship Between the Course Outline and Textbook**

The course outline is the basis for learning and assessment. The textbook provides the basic content and scope for mastering course knowledge, expanding and developing the outline's specified knowledge and content.

**III. Recommended Self-Study Textbook**

*Network Device Configuration and Management Project Tutorial (Huawei eNSP Simulator Edition)*, edited by Zhang Wenku, Peng Suhe, Chen Waiping, published by Electronic Industry Press, 1st edition, 2022.

**IV. Guidance on Self-Study Requirements and Methods**

The basic requirements of this outline are determined based on the professional examination plan and training goals. They specify basic content and mastery levels. Knowledge points form the main body of the course content and are the primary assessment focus.

To effectively guide individual and social self-study, the outline indicates chapter focuses and difficulties.

**(I) Systematic Learning, In-Depth Focus**

Self-learners should first have basic understanding of computer networks and technical concepts (e.g., IP addresses, network protocols). Then systematically study each chapter, memorize required concepts, deeply understand basic theories and methods, and master focuses. Projects 2, 3, 6, and 7 require extensive practice to deepen mastery.

**(II) Scientific Learning Methods, Clarify Relationships**

Before exams, review learned content, clarify relationships among basic concepts, theories, and configuration methods to aid memory, deepen understanding, and master configuration commands proficiently.

**(III) Deeply Understand Textbook Examples, Combine Theory and Practice**

Networking technology is practice-oriented. Self-learners should deeply understand textbook examples, practice diligently, and master device configuration commands through hands-on work, not just memorization, to improve problem analysis and solving abilities and achieve practical application.

**V. Requirements for Social Assistance**

Focus on key chapters, sub-key chapters, and general chapters, suggesting basic self-study or assisted study hours (e.g., 2-3 hours per credit). Emphasize correct guidance, proper direction, and balancing knowledge learning with ability improvement.

**(I) Help Self-Learners Organize Relationships**

Assistants should help clarify relationships between key and general content, ensuring comprehensive mastery while deepening key topics.

**(II) Suggested Assisted Study Hours**

2-3 hours per credit.

**VI. Explanation of Assessment Content**

All knowledge points required for learning and mastery are assessment content. Chapters consist of knowledge points, assessed at four cognitive levels.

**VII. Regulations on Examination Proposition**

1. Closed-book written exam, 150 minutes, scored out of 100, passing at 60.

2. Covers basic requirements, knowledge points, and details across chapters, emphasizing focuses with greater coverage.

3. No questions beyond outline scope or higher than specified ability levels. Focus on basic concepts, knowledge, theories, and methods. Avoid biased or unusual questions.

4. Approximate score distribution: Memorize 30%, Understand 40%, Apply 30%.

5. Difficulty levels: Easy 20%, Moderately easy 30%, Moderately difficult 30%, Difficult 20%.

6. Main question types: Single-choice, fill-in-the-blank, short answer, comprehensive application.

**Appendix: Question Type Examples**

**I. Single-Choice Question**

Routing occurs at the _____ layer of the TCP/IP model.  
A. Application layer  B. Network layer  C. Transport layer  D. Physical layer

**II. Fill-in-the-Blank Question**

Common routing protocols in LANs include ___, ______, and ________.

**III. Short Answer Question**

Switches distinguish port types based on different handling of VLAN tags on links. What are the types, and briefly describe their names and roles?

**IV. Comprehensive Application Question**

(Note: Comprehensive questions resemble practical assessments but can be answered in written exams by recording configuration and planning processes.)

To achieve mutual communication between computers in the diagram, complete the configuration process for Switch 1 and Switch 2.

2. Based on the topology diagram below, configure dynamic OSPF routing protocol to achieve full network connectivity.

Requirements:  
(1) Configure IP addresses on router and switch ports;  
(2) Assign IP addresses, subnet masks, and default gateways to each computer;  
(3) Configure dynamic OSPF routing protocol to achieve full network connectivity.