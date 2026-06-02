---
audio: false
generated: true
lang: en
layout: post
title: The History of Microcomputer
translated: false
type: note
---

The course **Microcomputer and Interface Technology**, as outlined, focuses on the architecture, programming, and interfacing of microcomputer systems, with a particular emphasis on the Intel 8086/8088 microprocessors and related interface technologies (e.g., 8255, 8253, 8251 chips). To provide a comprehensive history, I’ll trace the origins and evolution of the key technologies covered in the course, identify the key figures and companies behind their development, and explore the stories behind their creation. This includes the microcomputer itself, the 8086/8088 microprocessors, assembly language programming, memory systems, I/O interface technologies, and bus standards.

---

### **1. The Microcomputer: Origins and Evolution**

#### **What is a Microcomputer?**

A microcomputer is a small, affordable computer built around a microprocessor, integrating CPU, memory, and I/O capabilities. The course begins with an overview of microcomputer systems, rooted in the **Von Neumann architecture** (a CPU, memory for instructions and data, and I/O connected via buses).

#### **History and Discovery**

- **Pre-1970s: Foundations**
  - The concept of a programmable computer dates to **Charles Babbage**’s Analytical Engine (1830s), though it was never built. **Alan Turing**’s theoretical work (1936) and **John von Neumann**’s 1945 report on the EDVAC formalized the stored-program computer, where instructions and data share memory. This **Von Neumann architecture** became the blueprint for microcomputers.
  - Early computers (e.g., ENIAC, 1945) were massive, using vacuum tubes. The invention of the **transistor** (1947, **John Bardeen**, **Walter Brattain**, **William Shockley** at Bell Labs) and the **integrated circuit** (1958, **Jack Kilby** at Texas Instruments and **Robert Noyce** at Fairchild) enabled compact electronics.

- **1971: The First Microprocessor**
  - **Who Discovered It?**: **Intel**, specifically engineers **Federico Faggin**, **Ted Hoff**, and **Stan Mazor**, developed the **Intel 4004**, the first microprocessor, released in November 1971.
  - **Story**: Commissioned by Japanese calculator company Busicom, Intel was tasked with designing a chip for a programmable calculator. Ted Hoff proposed a single, general-purpose chip instead of multiple specialized chips, reducing cost and complexity. Federico Faggin led the design, cramming 2,300 transistors into a 4-bit processor (740 kHz, 12-bit address bus). The 4004 could execute 60,000 instructions per second, a leap for its time.
  - **Impact**: The 4004 powered the Busicom 141-PF calculator and inspired Intel to market it as a general-purpose processor, birthing the microprocessor industry.

- **1970s: Microcomputer Emergence**
  - **1974**: Intel’s **8080** (8-bit, 2 MHz) powered the **Altair 8800** (1975, MITS), the first commercially successful microcomputer. Marketed as a kit for hobbyists, it ran **CP/M** (an early OS) and inspired **Bill Gates** and **Paul Allen** to found Microsoft, writing a BASIC interpreter for it.
  - **1977**: The **Apple II** (Steve Wozniak, Steve Jobs), **Commodore PET**, and **TRS-80** made microcomputers accessible to consumers, with keyboards, displays, and software.
  - **Story**: The Altair’s success came from its open design and coverage in *Popular Electronics*. Hobbyists formed clubs (e.g., Homebrew Computer Club), fostering innovation. Wozniak’s Apple II design prioritized affordability and usability, using the MOS 6502 processor.

- **Course Context**: The course focuses on the **Intel 8086/8088**, introduced in 1978, which powered the **IBM PC** (1981), standardizing microcomputers for business and home use.

#### **Key Figures**

- **Federico Faggin**: Led 4004 design, later co-founded Zilog (Z80 processor).
- **Ted Hoff**: Conceived the microprocessor concept.
- **Robert Noyce and Gordon Moore**: Intel founders, drove IC and microprocessor development.
- **Ed Roberts**: MITS founder, created the Altair 8800.

---

### **2. The Intel 8086/8088 Microprocessor**

#### **What is It?**

The 8086 (16-bit, 5-10 MHz) and 8088 (8-bit external bus) are microprocessors central to the course, known for their segmented memory model, 1 MB address space, and x86 architecture, which remains dominant today.

#### **History and Discovery**

- **1976-1978: Development**
  - **Who Discovered It?**: Intel’s team, led by **Stephen Morse** (architecture and instruction set), **Bruce Ravenel** (microcode), and **Jim McKevitt** (project management), designed the 8086, released in June 1978. The 8088 followed in 1979.
  - **Story**: Intel aimed to leapfrog 8-bit processors (e.g., 8080, Z80) to compete in a growing market. The 8086 was designed as a 16-bit processor with a 20-bit address bus, supporting 1 MB of memory (vs. 64 KB for 8-bit chips). Its instruction set was backward-compatible with the 8080, easing software transitions. The 8088, with an 8-bit external bus, reduced system cost, making it attractive for IBM.
  - **Challenges**: The 8086’s complexity (29,000 transistors) pushed Intel’s fabrication limits. Its segmented memory model (64 KB segments, offset addressing) was a compromise to balance performance and compatibility.

- **1981: IBM PC Adoption**
  - **Story**: IBM, entering the PC market, chose the 8088 for its **IBM PC** (model 5150) due to its cost-effectiveness and Intel’s support. The decision was influenced by **Bill Lowe**’s team at IBM’s Boca Raton lab, who prioritized an open architecture using off-the-shelf components. The 8088 ran at 4.77 MHz, and the PC’s success standardized the x86 architecture.
  - **Impact**: The IBM PC’s open design allowed clones (e.g., Compaq, Dell), fueling the PC industry. Microsoft’s **MS-DOS**, developed for the PC, became the dominant OS.

- **Legacy**: The x86 architecture evolved through the 80286 (1982), 80386 (1985), and modern processors (e muttered, requiring periodic refreshing. Static RAM (SRAM) was faster but costlier.
  - **ROM**: Stored firmware, with variants like **EPROM** (erasable via UV light, George Perlegos, 1971) and **EEPROM** (electrically erasable, Eli Harari, 1977).
  - **Course Context**: The course covers memory expansion (e.g., address decoding), critical for 8086 systems with 1 MB address spaces.

#### **Key Figures**

- **Robert Noyce**: Co-invented the IC, enabling dense memory chips.
- **Ted Hoff**: Early DRAM designs at Intel.
- **Dov Frohman**: Invented EPROM at Intel.

---

### **5. I/O and Interface Technology**

#### **What is It?**

I/O interfaces connect the CPU to peripherals (e.g., keyboards, printers). The course covers **8255A** (parallel), **8253/8254** (timer), **8251A** (serial), and interrupt systems (e.g., **8259A**).

#### **History and Discovery**

- **1970s: Need for I/O**
  - Early microcomputers used simple I/O ports, but peripherals demanded specialized chips. Intel developed a family of peripheral controllers for the 8080 and 8086.
  - **Story**: As microcomputers grew complex, direct CPU control of I/O became inefficient. Intel’s peripheral chips offloaded tasks, improving performance.

- **8255A Programmable Peripheral Interface (1977)**
  - **Who?**: Intel, designed for 8080/8086 systems.
  - **Story**: The 8255A provided three 8-bit ports, configurable in modes for basic I/O, strobed I/O, or bidirectional transfers. It simplified interfacing with devices like keyboards and displays, becoming a staple in PCs.
  - **Impact**: Used in IBM PC parallel ports (e.g., printers).

- **8253/8254 Programmable Interval Timer (1977/1982)**
  - **Who?**: Intel, evolved from earlier timer designs.
  - **Story**: The 8253 offered three 16-bit counters for timing (e.g., system clocks) or counting (e.g., pulse measurement). The 8254 improved reliability. Used in PC speakers, DRAM refresh, and real-time clocks.
  - **Impact**: Essential for PC timing functions.

- **8251A Serial Interface (1976)**
  - **Who?**: Intel, for serial communication.
  - **Story**: The 8251A handled asynchronous (e.g., RS-232) and synchronous protocols, enabling modems and terminals. It was critical for early networking.
  - **Impact**: Powered PC serial ports (COM ports).

- **8259A Interrupt Controller (1979)**
  - **Who?**: Intel, designed for interrupt-driven systems.
  - **Story**: The 8259A managed up to 8 interrupt sources, with cascading for more, allowing peripherals to signal the CPU efficiently. It was integral to the IBM PC’s interrupt system.
  - **Impact**: Standardized interrupt handling in PCs.

- **Data Transfer Modes**
  - **Program-Controlled I/O**: CPU polled devices, simple but slow.
  - **Interrupt-Driven**: Peripherals triggered interrupts, taught in the course via the 8259A.
  - **DMA**: The **Intel 8237** DMA controller (1980) enabled high-speed transfers, used in disk controllers.

#### **Key Figures**

- **Intel Engineers**: Unnamed teams designed these chips, building on 8080/8086 ecosystems.
- **Gary Kildall**: CP/M OS leveraged these chips, influencing PC I/O standards.

---

### **6. Buses and Expansion**

#### **What is It?**

Buses standardize CPU-memory-peripheral communication. The course covers **ISA**, **PCI**, and modern interfaces (**USB**, **SPI**, **I²C**).

#### **History and Discovery**

- **1970s: Early Buses**
  - The **S-100 bus** (1975, Ed Roberts, MITS) was an early standard for Altair-like systems, adopted by hobbyists.
  - **Story**: The S-100’s openness fostered a microcomputer ecosystem but lacked standardization.

- **1981: ISA Bus**
  - **Who?**: IBM, for the IBM PC.
  - **Story**: Designed for the 8088, the ISA (Industry Standard Architecture) bus supported 8-bit (PC) and 16-bit (PC/AT) cards. Its simplicity and IBM’s market dominance made it a standard, though slow (8 MHz).
  - **Impact**: Used for expansion cards (e.g., sound, graphics) until the 1990s.

- **1992: PCI Bus**
  - **Who?**: Intel, with contributions from IBM and Compaq.
  - **Story**: PCI (Peripheral Component Interconnect) addressed ISA’s limitations, offering 33 MHz speed, 32-bit data paths, and plug-and-play. It became the standard for 1990s PCs.
  - **Impact**: Evolved into PCIe, used today.

- **Modern Interfaces**
  - **USB (1996)**: Developed by a consortium (Intel, Microsoft, Compaq, etc.), led by **Ajay Bhatt** at Intel. USB unified peripheral connections with hot-plugging and scalability (1.5 Mbps to 480 Mbps for USB 2.0).
  - **SPI (1980s)**: Motorola’s serial bus for high-speed, short-distance communication (e.g., SD cards).
  - **I²C (1982)**: Philips’ two-wire bus for low-speed peripherals (e.g., sensors).
  - **Story**: USB emerged from the need for a universal connector, replacing serial/parallel ports. SPI and I²C were designed for embedded systems, simplifying chip communication.

#### **Key Figures**

- **Ajay Bhatt**: USB’s lead architect.
- **IBM Engineers**: Defined ISA for the PC.
- **Intel Teams**: Drove PCI and USB standards.

---

### **The Course’s Context and Instructor**

- **Yang Quansheng**: Little public information exists about the instructor, likely a professor or engineer specializing in computer engineering. The course’s focus on 8086 and Intel chips suggests it was designed in the 1980s-1990s, when these technologies dominated education in China and globally, particularly for engineering programs.
- **Story Behind the Course**:
  - In the 1980s, China prioritized computer science and electronics education to catch up with Western technology. Courses like this were critical for training engineers in microcomputer design, embedded systems, and industrial automation.
  - The 8086/8088 and Intel’s peripheral chips were ideal for teaching due to their simplicity, widespread use, and documentation. The course’s inclusion of modern interfaces (USB, SPI, I²C) reflects updates to remain relevant.
  - **Target Majors**: Computer Science, Electronic Engineering, and Automation align with the course’s focus on hardware design, programming, and system integration, key skills for industries like robotics, telecommunications, and computing.

---

### **Significance and Legacy**

- **Microcomputers**: Transformed computing from room-sized machines to personal and embedded devices. The 8086/8088’s x86 architecture remains the backbone of PCs and servers.
- **Assembly Programming**: Though less common, it’s vital for low-level tasks (e.g., OS kernels, firmware).
- **Interface Chips**: The 8255, 8253, and 8251’s principles persist in modern microcontrollers (e.g., Arduino, STM32).
- **Buses**: ISA and PCI paved the way for PCIe, while USB, SPI, and I²C dominate modern systems.
- **Educational Impact**: Courses like this trained generations of engineers, contributing to global tech advancements, particularly in China’s tech boom.

---

### **Modern Relevance**

- **Embedded Systems**: Microcontroller-based systems use similar I/O, interrupt, and timing concepts.
- **Legacy Systems**: Some industrial and military systems still use 8086-based designs.
- **Education**: The 8086’s simplicity makes it a timeless teaching tool for computer architecture.
- **x86 Evolution**: Modern CPUs (e.g., Intel Core, AMD Ryzen) trace their lineage to the 8086.

---

If you need specific details (e.g., technical specs of the 8255, USB’s development, or Yang Quansheng’s background) or want to explore related topics (e.g., China’s tech education in the 1980s), let me know!
