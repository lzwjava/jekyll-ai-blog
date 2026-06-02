---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Switching and Routing Technologies Overview
translated: false
type: note
---

### Overview of the Course

The course "Switching and Routing Technologies" (专业代码: 510201) is part of China's National Higher Education Self-study Examination (自学考试) system, administered in Guangdong province. This subject falls under computer science and information technology majors, focusing on the principles, configuration, and application of network switches and routers. Topics typically include VLANs, STP (Spanning Tree Protocol), routing protocols (e.g., RIP, OSPF), IP addressing, subnetting, and basic network troubleshooting. As a relatively new course (likely introduced or updated in recent years to align with modern networking standards like those in CCNA-level curricula), exam questions emphasize both theoretical understanding and practical configuration skills, often drawing from Cisco-like IOS commands or similar.

Exams in this system are usually a mix of multiple-choice, fill-in-the-blank, short-answer, and configuration-based questions. Below, I've compiled example questions based on standard topics for this course. These are illustrative, inspired by similar national-level IT exams (e.g., NCRE Level 4 Network Engineer and computer network finals). For real preparation, refer to official Guangdong Self-Exam resources or textbooks like "Computer Networks" by Andrew Tanenbaum (adapted editions).

### Example Questions

#### Section 1: Multiple-Choice Questions (单选题)

These test foundational concepts. Each has one correct answer.

1. **In a LAN environment, which protocol is used to prevent loops in switched networks by blocking redundant paths?**
   A) VLAN
   B) STP (Spanning Tree Protocol)
   C) OSPF
   D) RIP
   *Answer: B. STP elects a root bridge and blocks ports to avoid loops.*

2. **For a Class C IP address (e.g., 192.168.1.0/24), how many usable hosts can it support if the host portion cannot be all zeros or all ones?**
   A) 256
   B) 254
   C) 512
   D) 128
   *Answer: B. A /24 subnet has 256 addresses total, minus 2 for network and broadcast.*

3. **In router configuration, which command enables OSPF process ID 1 on a Cisco-like device?**
   A) router ospf 1
   B) enable ospf
   C) ip ospf process 1
   D) configure ospf id 1
   *Answer: A. This enters OSPF configuration mode.*

4. **What is the primary function of a Layer 2 switch in a network?**
   A) Route packets between subnets
   B) Forward frames based on MAC addresses within the same broadcast domain
   C) Perform NAT for internet access
   D) Encrypt data for secure transmission
   *Answer: B. Switches operate at the data link layer.*

5. **In VLAN trunking, which protocol encapsulates Ethernet frames for inter-switch communication?**
   A) ISL (Inter-Switch Link)
   B) ARP
   C) ICMP
   D) DHCP
   *Answer: A. ISL is a Cisco proprietary trunking protocol; 802.1Q is the standard alternative.*

#### Section 2: Fill-in-the-Blank Questions (填空题)

Complete the statements with the missing terms.

1. **The default administrative distance for a static route in most routing tables is ____.**
   *Answer: 1 (or 0 for connected routes).*

2. **To configure a port as a trunk on a switch, the command is `switchport mode ____`.**
   *Answer: trunk.*

3. **In subnetting a /24 network into 4 equal subnets, the new subnet mask is ____ (in dotted decimal).**
   *Answer: 255.255.255.192 (/26).*

4. **RIP is a ____-hop count routing protocol limited to 15 hops to prevent routing loops.**
   *Answer: distance-vector.*

5. **The STP port states include blocking, listening, learning, and ____.**
   *Answer: forwarding.*

#### Section 3: Short-Answer Questions (简答题)

Provide brief explanations (2-4 sentences).

1. **Explain the difference between a switch and a router, and when you would use each in a network design.**
   *Sample Answer: A switch connects devices within the same network segment at Layer 2, using MAC addresses for fast local forwarding. A router connects different networks at Layer 3, using IP addresses to route traffic between subnets. Use a switch for LAN expansion (e.g., office wiring) and a router for inter-VLAN or internet connectivity.*

2. **Describe how VLANs improve network security and management.**
   *Sample Answer: VLANs segment a physical network into logical broadcast domains, isolating traffic (e.g., separating HR from engineering departments) to enhance security and reduce congestion. They allow centralized management via trunk links and prevent unauthorized access across segments without physical rewiring.*

3. **What is the purpose of the `ip route` command, and give an example for a default gateway.**
   *Sample Answer: The `ip route` command statically defines routes in a routing table. Example: `ip route 0.0.0.0 0.0.0.0 192.168.1.1` sets the default gateway to 192.168.1.1 for all unknown destinations.*

#### Section 4: Configuration-Based Questions (配置题)

These simulate practical scenarios, often requiring command sequences (assume Cisco IOS syntax, common in such exams).

1. **Given a switch with interfaces FastEthernet0/1-3 connected to PCs in VLAN 10 and FastEthernet0/24 as a trunk to another switch, write the commands to configure VLAN 10 and assign ports.**
   *Sample Commands:*

   ```
   vlan 10
   name Sales
   exit
   interface range fa0/1 - 3
   switchport mode access
   switchport access vlan 10
   exit
   interface fa0/24
   switchport mode trunk
   switchport trunk allowed vlan 10
   ```

2. **On a router, configure a static route to reach network 10.0.0.0/8 via next-hop 172.16.1.1.**
   *Sample Command:*

   ```
   ip route 10.0.0.0 255.0.0.0 172.16.1.1
   ```

3. **Enable STP on a switch and set it as the root bridge for VLAN 1.**
   *Sample Commands:*

   ```
   spanning-tree vlan 1 root primary
   ```

### Preparation Tips

- **Practice Focus:** Emphasize hands-on simulation using tools like Packet Tracer or GNS3 for configurations.
- **Exam Format:** Guangdong self-exams are typically 150 marks, 3 hours, with 60%+ pass rate. Check the official site (eeagd.edu.cn) for 2025 schedules.
- **Resources:**
  - [National Computer Rank Examination Level 4 Samples](https://ncre.neea.edu.cn/html1/report/1508/288-1.htm)
  - [Computer Networks MOOC (South China University of Technology)](https://www.icourse163.org/course/HCIT-1001754308)
  - [General Computer Network Question Bank](https://cloud.tencent.com/developer/article/2097713)

For official past papers, visit the Guangdong Education Exam Authority portal. If you need more tailored examples or solutions, provide specific topics!
