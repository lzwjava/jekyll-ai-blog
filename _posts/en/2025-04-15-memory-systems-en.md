---
audio: false
generated: true
lang: en
layout: post
title: Memory Systems Tutorial
translated: false
type: note
---

This tutorial covers the key concepts of memory systems, focusing on memory classification, RAM/ROM principles, and address decoding techniques. Let's break this down into comprehensive sections.

## 1. Memory Classification

Computer memory can be broadly classified into two main categories:

### 1.1 By Function
- **Primary Memory**: Directly accessible by the CPU
  - RAM (Random Access Memory): Temporary storage
  - ROM (Read-Only Memory): Permanent storage
- **Secondary Memory**: External storage devices (hard drives, SSDs, etc.)

### 1.2 By Data Retention
- **Volatile Memory**: Loses data when power is off (most RAM)
- **Non-volatile Memory**: Retains data without power (ROM, Flash)

### 1.3 By Access Method
- **Random Access**: Any location can be accessed directly (RAM, ROM)
- **Sequential Access**: Data accessed in sequence (magnetic tapes)

## 2. RAM Working Principles

RAM (Random Access Memory) is the computer's main working memory.

### 2.1 DRAM (Dynamic RAM)
- Stores each bit in a tiny capacitor and transistor
- Requires periodic refresh to maintain data (typically every few milliseconds)
- Higher density, lower cost, more common in main memory
- Operation cycle: row address strobe (RAS) → column address strobe (CAS) → data access

### 2.2 SRAM (Static RAM)
- Uses flip-flop circuits to store each bit
- Doesn't need refreshing, retains data as long as power is supplied
- Faster, but more expensive and lower density than DRAM
- Used in cache memory

### 2.3 RAM Organization
- Organized in a matrix format of rows and columns
- Each cell has a unique address (row + column)
- Data bits are typically organized in word lengths (8, 16, 32, 64 bits)

## 3. ROM Working Principles

ROM (Read-Only Memory) stores permanent or semi-permanent data.

### 3.1 Types of ROM
- **Mask ROM**: Programmed during manufacturing, cannot be modified
- **PROM (Programmable ROM)**: Can be programmed once by the user
- **EPROM (Erasable PROM)**: Can be erased with UV light and reprogrammed
- **EEPROM (Electrically EPROM)**: Can be electrically erased and reprogrammed
- **Flash Memory**: Modern form of EEPROM, allows block-wise erasure

### 3.2 ROM Operation
- Contains pre-written data at manufacture or programming time
- Reading: Address → decoder → sense amplifier → output buffers
- Writing (for writable types): Higher voltage used to modify the storage cells

## 4. Memory Expansion

As programs become more complex, memory expansion is often necessary.

### 4.1 Capacity Expansion
- **Chip Selection**: Using multiple memory chips to increase total memory
- **Word Length Expansion**: Combining chips to increase data bus width
- **Address Space Expansion**: Increasing addressable memory space

### 4.2 Memory Banks
- Memory organized into banks that can be accessed independently
- Allows for interleaving, reducing average access time
- Facilitates parallel operations in modern architectures

## 5. Address Decoding Techniques

Address decoding is crucial for accessing the correct memory location.

### 5.1 Linear Selection (Full Decoding)
- Each address line directly connects to one memory location
- Simple but inefficient for large memory spaces
- Example: In a system with 16 address lines, we need 2^16 (65,536) individual connections

### 5.2 Decoder-Based Selection
- **Address Decoders**: Convert binary address to one-hot selection signals
- **2-to-4 Decoder**: Takes 2 address bits, activates one of 4 output lines
- **3-to-8 Decoder**: Takes 3 address bits, activates one of 8 output lines
- Common ICs: 74LS138 (3-to-8), 74LS154 (4-to-16)

### 5.3 Partial Decoding
- Not all address bits are decoded, conserving hardware
- Multiple memory locations may map to the same physical location
- Creates memory "shadows" or "mirrors"

### 5.4 Memory Mapping
- **Contiguous Mapping**: Memory blocks arranged sequentially
- **Paged Mapping**: Memory divided into fixed-size pages
- **Segmented Mapping**: Memory divided into variable-sized segments

## 6. Implementation Examples

### 6.1 Simple RAM Expansion Example
To expand a 32K × 8 RAM system to 128K × 8:
1. Use four 32K × 8 RAM chips
2. Use 2 higher-order address bits to select among the four chips
3. Connect remaining address lines to all chips in parallel
4. Use a 2-to-4 decoder for chip selection

### 6.2 Address Decoding Circuit

For a system with memory mapped at address range 0x8000-0x9FFF:
1. Address lines A15-A13 must be "100" (for 0x8000-0x9FFF)
2. Use AND gates to detect this pattern
3. Enable the appropriate memory chip when this pattern is detected

This completes our overview of memory systems, focusing on classification, working principles, and expansion techniques. The understanding of these concepts is fundamental to designing and working with computer systems effectively.
