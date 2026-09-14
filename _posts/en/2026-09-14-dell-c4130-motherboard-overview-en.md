---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dell C4130 Motherboard Overview
translated: false
type: note
---

**Question:** What is an introduction to the Dell C4130 board (system board / motherboard)?

**Answer:**

The Dell PowerEdge C4130 is a 1U rack server designed specifically for high-performance computing (HPC) and GPU-accelerated workloads. Here's an overview of its system board and key components:

---

**Overview**

The PowerEdge C4130 provides supercomputing agility and performance in an ultra-dense platform purpose-built for high-performance computing (HPC) and virtual desktop infrastructure (VDI) workloads. It is aimed at research, simulation, finance, energy exploration, and similar fields.

---

**System Board (Motherboard) Role**

The system board (also known as the motherboard) is the main printed circuit board in the system, with different connectors used to connect different components or peripherals of the system. The system board provides the electrical connections to these components.

---

**Key Specifications**

**Form Factor & Processor**

The C4130 is a 1U rack server supporting Intel Xeon processor E5-2600 v3/v4 product family with 2 processor sockets, using the C612 series chipset and up to 9.6 GT/s internal interconnect.

**Memory**

It supports DDR4 DIMMs at up to 2400 MT/s with 16 DIMM slots, accepting 4 GB, 8 GB, 16 GB, 32 GB, and 64 GB modules.

**GPU Support**

The system supports up to four graphics processing units (GPUs). All GPU cards must be of the same type and model — mixing GPUs is not supported. It supports both standard PCIe GPUs and SXM2-form-factor GPUs (with NVLink board configuration).

**Expansion Bus**

The C4130 supports PCIe Gen 3 expansion cards installed on the system board via expansion card risers, and supports four expansion card riser configurations.

**Storage**

Storage includes up to 2 × 1.8" SATA SSD boot drives, with an optional RAID controller (PERC H330). An optional data drive tray supports up to 4 × 2.5" SAS/SATA drives.

**Networking**

The system includes 2 × 1 GbE LOM (LAN on Motherboard) and supports up to 2 PCIe 3.0 low-profile adapters on the back, with support for InfiniBand FDR and NVIDIA GPUDirect. An optional 96-lane PCIe 3.0 switch is available for certain accelerator configurations.

**Power**

Power is supplied by a 1600 W hot-plug PSU, with an optional redundant 1+1 PSU configuration.

**Management**

Systems management includes IPMI 2.0 compliance, Dell OpenManage Essentials, Dell OpenManage Mobile, and Dell OpenManage Power Center. The board also integrates iDRAC (Integrated Dell Remote Access Controller) for out-of-band management.

---

**References:**

- [Dell PowerEdge C4130 Owner's Manual – Overview](https://www.dell.com/support/manuals/en-us/poweredge-c4130/c4130ownersmanual/dell-poweredge-c4130-overview?guid=guid-b5b8b87a-5190-41b9-aeed-94c256b9266a&lang=en-us)
- [Dell PowerEdge C4130 Spec Sheet (PDF)](https://gotomojo.com/wp-content/uploads/2018/04/EMEA-Spec-Sheets-C4130-Specifications.pdf)
- [Mojo Systems – C4130 Specs & Info](https://www.gotomojo.com/servers/dell-emc-poweredge/c-series/c4130/)
