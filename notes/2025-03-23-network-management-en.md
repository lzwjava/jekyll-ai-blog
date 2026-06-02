---
audio: false
generated: true
lang: en
layout: post
title: Network Performance and Management Tutorial
translated: false
type: note
---

**Tailored for Chinese Self-Study Exam (自考) in Computer Networks Technology**

---

## **1. Key Performance Metrics**

### **1.1 Latency (延迟)**

- **Definition**: Time taken for data to travel from source to destination (ms).
- **Components**:
  - **Propagation Delay**: Distance ÷ Speed of medium (e.g., fiber optic ≈ 2/3 speed of light).
  - **Transmission Delay**: Packet size ÷ Bandwidth.
  - **Queuing Delay**: Time spent in routers/switches.
  - **Processing Delay**: Time taken by devices to process headers.
- **Impact**: Critical for real-time apps (e.g., video calls, gaming).
- **Example**: High latency when accessing international sites (e.g., Chinese user connecting to a U.S. server).

### **1.2 Bandwidth (带宽)**

- **Definition**: Maximum data transfer rate (Mbps/Gbps).
- **Importance**: Determines network capacity.
- **Example**: 4K streaming requires ~25 Mbps; insufficient bandwidth causes buffering.

### **1.3 Jitter (抖动)**

- **Definition**: Variation in latency between packets.
- **Impact**: Disrupted VoIP calls or video conferencing.
- **Solution**: Use jitter buffers to smooth out delays.

### **1.4 Packet Loss (丢包率)**

- **Definition**: Percentage of packets failing to reach destination.
- **Causes**: Network congestion, faulty hardware, signal interference.
- **Impact**: Retransmissions slow down throughput (e.g., lag in online games).

---

## **2. Network Troubleshooting Tools**

### **2.1 Ping**

- **Function**: Tests connectivity and measures latency using ICMP echo requests.
- **Command**: `ping www.baidu.com`
  - **Key Output**: Round-trip time (RTT) and packet loss %.
  - **Continuous Ping**: `ping -t` (Windows) or `ping -c 10` (Linux).

### **2.2 Traceroute**

- **Function**: Maps the path of packets and identifies latency at each hop.
- **Command**:
  - Windows: `tracert www.qq.com`
  - Linux/macOS: `traceroute -I www.qq.com` (uses ICMP)
- **Mechanism**: Uses TTL (Time-to-Live) to force routers to return errors.

---

## **3. Network Configuration & Management Basics**

### **3.1 IP Addressing & Subnetting**

- **IPv4**: 32-bit address (e.g., `192.168.1.1`).
- **Subnetting**: Divide networks for efficiency (e.g., `/24` subnet = 256 addresses).

### **3.2 DHCP & DNS**

- **DHCP**: Automates IP assignment (e.g., home routers).
- **DNS**: Translates domain names to IPs (e.g., `www.taobao.com` → `140.205.220.96`).

### **3.3 Device Configuration**

- **Routers/Switches**: Use CLI (e.g., Cisco IOS) or GUI (e.g., Huawei web interface).
- **Security**: Firewalls, ACLs (Access Control Lists).

---

## **4. Quality of Service (QoS)**

### **4.1 Why QoS Matters**

- Prioritizes critical traffic (e.g., video conferencing over file downloads).

### **4.2 QoS Mechanisms**

- **Traffic Classification**: Tagging packets (e.g., DSCP for VoIP).
- **Queuing**: Priority queues (e.g., LLQ for voice traffic).
- **Shaping/Policing**: Limit bandwidth for non-critical apps.

### **4.3 Models**

- **DiffServ**: Scalable, class-based (e.g., enterprise networks).
- **IntServ**: Resource reservation for high-priority flows (complex, less common).

---

## **5. Exam Tips & Practice**

### **5.1 Key Formulas**

- **Total Latency** = Propagation + Transmission + Queuing + Processing Delay
- **Bandwidth-Delay Product** = Bandwidth × RTT (measures network capacity).

### **5.2 Scenario-Based Questions**

- **Example**: A user complains of choppy Zoom calls. Identify likely causes (jitter, packet loss) and tools (ping, traceroute).

### **5.3 Labs for Self-Study**

1. Use `ping` to compare latency to `www.baidu.com` vs. `www.amazon.com`.
2. Run `tracert` to analyze hops to a international website.
3. Configure a home router’s QoS settings to prioritize WeChat video.

---

**Summary**: Mastery of these concepts ensures efficient network design and troubleshooting, essential for real-world applications and exams. Focus on understanding metric interdependencies (e.g., how jitter affects VoIP) and practical tool usage.
