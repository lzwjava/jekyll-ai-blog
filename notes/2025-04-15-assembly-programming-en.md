---
audio: false
generated: true
lang: en
layout: post
title: Assembly Language Programming
translated: false
type: note
---

Below is a comprehensive tutorial for **Part 2: Assembly Language Programming**, covering the topics outlined: *8086 Instruction Set (Data Transfer, Arithmetic, Logic, and Control Flow Instructions), Assembly Language Programming (Sequential, Branch, and Loop Structures), and Interrupt Service Routines*. This tutorial is designed to be thorough, accessible, and practical, building on the fundamentals of microcomputers (e.g., 8086/8088 architecture). It assumes basic knowledge of CPU registers and memory addressing.

---

## Part 2: Assembly Language Programming

Assembly language is a low-level programming language that provides direct control over a microprocessor’s operations. For the Intel 8086/8088, assembly language allows programmers to write instructions that map closely to machine code, offering fine-grained control over hardware resources like registers, memory, and I/O devices.

### 1. 8086 Instruction Set

The 8086 instruction set is a collection of commands that the CPU understands, categorized by their function: **data transfer**, **arithmetic**, **logic**, and **control flow**. Each instruction operates on registers, memory, or immediate values, using the 8086’s addressing modes (e.g., register, direct, indirect).

#### a. Data Transfer Instructions
These instructions move data between registers, memory, and immediate values.

- **MOV (Move)**:
  - Syntax: `MOV destination, source`
  - Function: Copies data from source to destination.
  - Example: `MOV AX, BX` (copy BX to AX); `MOV AX, [1234h]` (copy data from memory address DS:1234h to AX).
  - Notes: Does not affect flags; source and destination must be the same size (8-bit or 16-bit).
- **XCHG (Exchange)**:
  - Syntax: `XCHG destination, source`
  - Function: Swaps contents of source and destination.
  - Example: `XCHG AX, BX` (swap AX and BX).
- **PUSH (Push onto Stack)**:
  - Syntax: `PUSH source`
  - Function: Pushes 16-bit data onto the stack, decrements SP by 2.
  - Example: `PUSH AX` (save AX on stack).
- **POP (Pop from Stack)**:
  - Syntax: `POP destination`
  - Function: Pops 16-bit data from stack to destination, increments SP by 2.
  - Example: `POP BX` (restore BX from stack).
- **LEA (Load Effective Address)**:
  - Syntax: `LEA destination, source`
  - Function: Loads the address of a memory operand into a register.
  - Example: `LEA BX, [SI+4]` (load address of DS:SI+4 into BX).
- **IN/OUT**:
  - Syntax: `IN destination, port`; `OUT port, source`
  - Function: Transfers data to/from I/O ports.
  - Example: `IN AL, 60h` (read keyboard port); `OUT 61h, AL` (write to speaker port).

#### b. Arithmetic Instructions
These perform mathematical operations, updating flags (e.g., ZF, CF, SF, OF) based on results.

- **ADD (Add)**:
  - Syntax: `ADD destination, source`
  - Function: Adds source to destination, stores result in destination.
  - Example: `ADD AX, BX` (AX = AX + BX).
- **SUB (Subtract)**:
  - Syntax: `SUB destination, source`
  - Function: Subtracts source from destination.
  - Example: `SUB CX, 10` (CX = CX - 10).
- **INC (Increment)**:
  - Syntax: `INC destination`
  - Function: Increments destination by 1.
  - Example: `INC BX` (BX = BX + 1).
- **DEC (Decrement)**:
  - Syntax: `DEC destination`
  - Function: Decrements destination by 1.
  - Example: `DEC CX` (CX = CX - 1).
- **MUL (Multiply, Unsigned)**:
  - Syntax: `MUL source`
  - Function: Multiplies AL (8-bit) or AX (16-bit) by source, stores result in AX or DX:AX.
  - Example: `MUL BX` (DX:AX = AX * BX).
- **DIV (Divide, Unsigned)**:
  - Syntax: `DIV source`
  - Function: Divides AX (8-bit) or DX:AX (16-bit) by source, stores quotient in AL/AX, remainder in AH/DX.
  - Example: `DIV BX` (AX = DX:AX / BX, DX = remainder).
- **ADC (Add with Carry)** and **SBB (Subtract with Borrow)**:
  - Function: Handle multi-word arithmetic using the carry flag.
  - Example: `ADC AX, BX` (AX = AX + BX + CF).

#### c. Logic Instructions
These perform bitwise operations and manipulate binary data.

- **AND (Bitwise AND)**:
  - Syntax: `AND destination, source`
  - Function: Performs bitwise AND, stores result in destination.
  - Example: `AND AX, 0FFh` (clear upper byte of AX).
- **OR (Bitwise OR)**:
  - Syntax: `OR destination, source`
  - Function: Performs bitwise OR.
  - Example: `OR BX, 1000h` (set bit 12 in BX).
- **XOR (Bitwise XOR)**:
  - Syntax: `XOR destination, source`
  - Function: Performs bitwise XOR.
  - Example: `XOR AX, AX` (clear AX to 0).
- **NOT (Bitwise NOT)**:
  - Syntax: `NOT destination`
  - Function: Inverts all bits in destination.
  - Example: `NOT BX` (BX = ~BX).
- **SHL/SHR (Shift Left/Right)**:
  - Syntax: `SHL destination, count`; `SHR destination, count`
  - Function: Shifts bits left/right, fills with 0 (SHR) or sign bit (SAL/SAR).
  - Example: `SHL AX, 1` (AX = AX * 2).
- **ROL/ROR (Rotate Left/Right)**:
  - Function: Rotates bits, wrapping around through carry flag.
  - Example: `ROL BX, 1` (rotate BX left by 1 bit).

#### d. Control Flow Instructions
These alter the program’s execution sequence, enabling jumps, loops, and subroutines.

- **JMP (Jump)**:
  - Syntax: `JMP label`
  - Function: Unconditionally jumps to a label.
  - Example: `JMP start` (goto label `start`).
  - Variants:
    - Short jump (±127 bytes).
    - Near jump (within segment).
    - Far jump (different segment).
- **Conditional Jumps**:
  - Syntax: `Jcc label` (e.g., JZ, JNZ, JC, JNC)
  - Function: Jumps based on flag states.
  - Examples:
    - `JZ loop_end` (jump if zero flag set).
    - `JC error` (jump if carry flag set).
    - Common conditions: JZ (zero), JNZ (not zero), JS (sign), JO (overflow).
- **LOOP (Loop)**:
  - Syntax: `LOOP label`
  - Function: Decrements CX, jumps to label if CX ≠ 0.
  - Example: `LOOP process` (repeat until CX = 0).
  - Variants:
    - `LOOPE/LOOPZ`: Loop if CX ≠ 0 and ZF = 1.
    - `LOOPNE/LOOPNZ`: Loop if CX ≠ 0 and ZF = 0.
- **CALL (Call Subroutine)**:
  - Syntax: `CALL label`
  - Function: Pushes return address onto stack, jumps to subroutine.
  - Example: `CALL compute_sum` (call subroutine).
- **RET (Return)**:
  - Syntax: `RET`
  - Function: Pops return address from stack, resumes execution.
  - Example: `RET` (return from subroutine).
- **INT (Interrupt)**:
  - Syntax: `INT number`
  - Function: Triggers a software interrupt, calling an interrupt service routine (ISR).
  - Example: `INT 21h` (DOS system call).
- **IRET (Interrupt Return)**:
  - Function: Returns from an ISR, restoring flags and return address.

---

### 2. Assembly Language Programming

Assembly language programs are written as human-readable instructions that are assembled into machine code. The 8086 uses a **segmented memory model**, with code, data, and stack segments defined explicitly.

#### a. Program Structure
A typical 8086 assembly program includes:
- **Directives**: Instructions for the assembler (e.g., NASM, MASM).
  - `SEGMENT`: Defines code, data, or stack segments.
  - `ORG`: Sets origin address.
  - `DB/DW`: Defines byte/word data.
- **Instructions**: CPU operations (e.g., MOV, ADD).
- **Labels**: Mark locations for jumps or data.
- **Comments**: Explain code (e.g., `; comment`).

**Example Program Structure (MASM syntax)**:
```asm
.model small
.stack 100h
.data
    message db 'Hello, World!$'
.code
main proc
    mov ax, @data    ; Initialize DS
    mov ds, ax
    mov dx, offset message ; Load message address
    mov ah, 09h      ; DOS print string function
    int 21h          ; Call DOS interrupt
    mov ah, 4Ch      ; Exit program
    int 21h
main endp
end main
```

#### b. Sequential Structures
Sequential code executes instructions in order, without jumps or loops.

**Example: Adding Two Numbers**
```asm
mov ax, 5        ; AX = 5
mov bx, 10       ; BX = 10
add ax, bx       ; AX = AX + BX (15)
mov [result], ax ; Store result in memory
```
- Instructions execute one after another.
- Common for simple calculations or data initialization.

#### c. Branch Structures
Branching uses conditional/unconditional jumps to alter program flow based on conditions.

**Example: Compare and Branch**
```asm
mov ax, 10       ; AX = 10
cmp ax, 15       ; Compare AX with 15
je equal         ; Jump if AX == 15
mov bx, 1        ; Else, BX = 1
jmp done
equal:
    mov bx, 0    ; BX = 0 if equal
done:
    ; Continue program
```
- **CMP**: Sets flags based on subtraction (AX - 15).
- **JE**: Jumps if ZF = 1 (equal).
- Useful for if-then-else logic.

#### d. Loop Structures
Loops repeat instructions until a condition is met, often using `LOOP` or conditional jumps.

**Example: Sum Numbers 1 to 10**
```asm
mov cx, 10       ; Loop counter = 10
mov ax, 0        ; Sum = 0
sum_loop:
    add ax, cx   ; Add CX to sum
    loop sum_loop ; Decrement CX, loop if CX ≠ 0
    ; AX = 55 (1 + 2 + ... + 10)
```
- `LOOP` simplifies counter-based iteration.
- Alternative: Use `CMP` and `JNZ` for custom conditions.

**Example with Conditional Loop**
```asm
mov ax, 0        ; Counter
mov bx, 100      ; Limit
count_up:
    inc ax       ; AX++
    cmp ax, bx   ; Compare with 100
    jle count_up ; Jump if AX <= 100
```
- Flexible for non-counter-based loops.

#### e. Subroutines
Subroutines modularize code, allowing reuse via `CALL` and `RET`.

**Example: Square a Number**
```asm
main:
    mov ax, 4    ; Input
    call square  ; Call subroutine
    ; AX = 16
    jmp exit
square:
    push bx      ; Save BX
    mov bx, ax   ; Copy AX
    mul bx       ; AX = AX * BX
    pop bx       ; Restore BX
    ret          ; Return
exit:
    ; End program
```
- **PUSH/POP**: Save/restore registers to avoid side effects.
- Stack manages return addresses automatically.

---

### 3. Interrupt Service Routines (ISRs)

Interrupts allow the CPU to respond to external or internal events (e.g., keyboard input, timer ticks) by pausing the current program and executing an ISR.

#### Interrupt Mechanism
- **Interrupt Vector Table (IVT)**:
  - Located at memory 0000:0000h–0000:03FFh.
  - Stores addresses of ISRs for 256 interrupt types (0–255).
  - Each entry: Segment:Offset (4 bytes).
- **Types**:
  - **Hardware Interrupts**: Triggered by devices (e.g., IRQ).
  - **Software Interrupts**: Triggered by `INT` instruction (e.g., INT 21h for DOS).
  - **Exceptions**: CPU errors (e.g., divide by zero).
- **Process**:
  1. Interrupt occurs.
  2. CPU saves flags, CS, and IP on stack.
  3. Jumps to ISR via IVT.
  4. ISR executes, ends with `IRET` to restore state.

#### Writing an ISR
ISRs must:
- Preserve registers (PUSH/POP).
- Handle the interrupt quickly.
- End with `IRET`.

**Example: Custom Timer ISR**
```asm
.data
old_vec dw 2 dup(0) ; Store old interrupt vector
.code
install_isr:
    cli             ; Disable interrupts
    mov ax, 0
    mov es, ax      ; ES = 0 (IVT segment)
    mov bx, 1Ch*4   ; Timer interrupt (1Ch)
    mov ax, es:[bx] ; Save old vector
    mov old_vec, ax
    mov ax, es:[bx+2]
    mov old_vec+2, ax
    mov ax, offset my_isr ; Set new vector
    mov es:[bx], ax
    mov ax, cs
    mov es:[bx+2], ax
    sti             ; Enable interrupts
    ret
my_isr:
    push ax
    inc word ptr [counter] ; Increment counter
    pop ax
    iret            ; Return from interrupt
```
- Hooks timer interrupt (1Ch, ~18.2 Hz).
- Increments a counter variable.
- Preserves registers and uses `IRET`.

**Example: DOS Interrupt (INT 21h)**
```asm
mov ah, 09h      ; Print string function
mov dx, offset msg ; Address of '$'-terminated string
int 21h          ; Call DOS
```
- INT 21h provides OS services (e.g., I/O, file handling).
- AH specifies the function code.

#### Practical Notes
- **Saving State**: ISRs must preserve all registers to avoid corrupting the main program.
- **Priority**: Hardware interrupts may preempt others (managed by PIC).
- **Debugging**: Use tools like DEBUG.COM or modern emulators (e.g., DOSBox, Bochs).

---

### Example Program: Factorial Calculation
This program calculates the factorial of a number (e.g., 5! = 120) using a loop and subroutine.

```asm
.model small
.stack 100h
.data
    num dw 5        ; Input number
    result dw ?     ; Store result
.code
main proc
    mov ax, @data
    mov ds, ax      ; Initialize DS
    mov ax, num     ; Load number
    call factorial  ; Compute factorial
    mov result, ax  ; Store result
    mov ah, 4Ch     ; Exit
    int 21h
main endp
factorial proc
    push bx
    mov bx, ax      ; BX = n
    mov ax, 1       ; AX = result
fact_loop:
    cmp bx, 1
    jle done        ; If BX <= 1, exit
    mul bx          ; AX = AX * BX
    dec bx          ; BX--
    jmp fact_loop
done:
    pop bx
    ret
factorial endp
end main
```
- **Logic**:
  - Input: num = 5.
  - Loop: AX = AX * BX, BX-- until BX = 1.
  - Result: AX = 5 * 4 * 3 * 2 * 1 = 120.
- **Features**:
  - Subroutine for modularity.
  - Stack for register preservation.
  - Sequential and loop structures.

---

### Best Practices
1. **Comment Code**: Assembly is cryptic; explain every step.
2. **Minimize Register Use**: Avoid unnecessary overwrites.
3. **Test Incrementally**: Use debuggers to trace execution.
4. **Handle Edge Cases**: Check for overflow, zero, or negative inputs.
5. **Optimize**: Reduce instructions (e.g., use XOR AX, AX instead of MOV AX, 0).

---

### Summary
- **8086 Instruction Set**:
  - **Data Transfer**: MOV, PUSH, POP for moving data.
  - **Arithmetic**: ADD, SUB, MUL for calculations.
  - **Logic**: AND, OR, XOR for bit manipulation.
  - **Control Flow**: JMP, LOOP, CALL for program flow.
- **Programming Structures**:
  - **Sequential**: Linear execution for simple tasks.
  - **Branch**: Conditional jumps for decisions.
  - **Loop**: LOOP or Jcc for repetition.
  - **Subroutines**: CALL/RET for modular code.
- **Interrupts**:
  - ISRs handle events via IVT.
  - Preserve state, end with IRET.
  - Used for hardware (e.g., timer) and software (e.g., DOS) interrupts.

---

### Practice Questions
1. Write a program to reverse a string in memory.
2. Implement a subroutine to check if a number is prime.
3. Create an ISR for the keyboard interrupt (INT 09h) to count keypresses.
4. Explain the difference between `JMP` and `CALL`.
5. Optimize this code: `MOV AX, 0; MOV BX, AX; ADD BX, 5`.

---

This tutorial covers the essentials of 8086 assembly programming, with examples and explanations to build practical skills. If you’d like to explore specific instructions, advanced techniques (e.g., string operations), or emulation tools, let me know!
