---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU Tiling: Why 2048 Beats 2047"
translated: false
type: note
---

Question: **After GPU divides matrix multiplication into tiles (for example 128×128 blocks), how is the actual calculation performed? Why are sizes like 2048 faster than 2047?**

Answer:

Your intuition is correct. The key idea is:

**Normal matrix multiplication is row × column. GPU changes it into tile × tile multiplication.**

genui{"linear_algebra_optimization":{"type_id":"MATRIX_MULTIPLICATION_ROW_COLUMN_RULE","locale_override":"en-US"}}

## 1. Normal matrix multiplication

Suppose:

```
A = M × K
B = K × N

C = A × B

C = M × N
```

Each element:

```
C[i][j] = A[i][0]*B[0][j]
       + A[i][1]*B[1][j]
       + ...
       + A[i][K-1]*B[K-1][j]
```

A single C element needs:

* one row from A
* one column from B

Example:

```
A row:

[a0 a1 a2 a3]


B column:

[b0
 b1
 b2
 b3]


C:

a0*b0 + a1*b1 + a2*b2 + a3*b3
```

---

## 2. GPU says: don't calculate one element, calculate a block

A GPU has thousands of CUDA cores.

Instead of:

```
thread 1 -> C[0][0]
thread 2 -> C[0][1]
thread 3 -> C[0][2]
...
```

it does:

```
CUDA block

calculate:

C tile

128 × 128
```

So one GPU block produces:

```
C:

+----------------+
|                |
|   128 x 128    |
|    tile        |
|                |
+----------------+
```

---

## 3. Matrix is divided into tiles

Example:

2048 × 2048 matrix:

```
A

+----+----+----+
|128 |128 |128 |
+----+----+----+
|128 |128 |128 |
+----+----+----+
|128 |128 |128 |
+----+----+----+
```

Actually:

```
2048 / 128 = 16

so:

16 × 16 tiles
```

The GPU sees:

```
A:

A00 A01 A02 ... A0F
A10 A11 A12 ... A1F
...
A15 A16 ... A1F
```

Same for B:

```
B00 B01 ... B0F
...
```

---

## 4. Tile multiplication

The formula becomes:

```
C_tile(i,j)

=

A_tile(i,0) × B_tile(0,j)

+

A_tile(i,1) × B_tile(1,j)

+

...

+

A_tile(i,15) × B_tile(15,j)
```

Example:

To calculate:

```
C tile:

C[3][5]
```

(not one number, but a 128×128 area)

GPU does:

```
A30 × B05

+

A31 × B15

+

A32 × B25

...

+

A3F × B F5
```

Each operation is:

```
128×128 matrix multiplication
```

---

## 5. Why 2048 is faster than 2047?

Because:

```
2048 / 128 = 16 exactly
```

The GPU workload:

```
16 × 16 = 256 tiles
```

Perfect.

---

But:

```
2047 / 128 = 15.99
```

You need:

```
ceil(2047/128)

= 16
```

tiles anyway.

So GPU allocates:

```
16 × 16 tiles
```

but the last tile has:

```
128×128
```

space while actual data is:

```
127×127
```

The unused area is called:

**padding / masked computation**

GPU still has to launch the same kernel.

---

## 6. Tensor Core makes this even more obvious

Modern NVIDIA GPUs have Tensor Cores.

Example:

Ampere:

```
16×16×16 MMA
```

meaning:

```
C = A×B+C

A:16×16
B:16×16
C:16×16
```

Hopper:

larger internal tiles.

The hardware likes:

```
multiple of:

8
16
32
64
128
```

because memory movement and tensor core instructions are fixed shapes.

---

## 7. Memory is the other reason

GPU computation is:

```
HBM/VRAM
      |
      v
L2 cache
      |
      v
shared memory
      |
      v
registers
      |
      v
Tensor Core
```

A tile allows:

```
load once

A tile
B tile

reuse many times
```

Example:

Without tiling:

```
read A[i,k]
read B[k,j]

for every C
```

Huge memory traffic.

With tiling:

```
load:

A 128×128
B 128×128


into shared memory


reuse:

128×128 outputs
```

Much higher FLOPS.

---

So the mental model:

```
CPU style:

C[i][j]
    =
row A
    dot
column B


GPU style:

divide matrices

↓

tiles

↓

each CUDA block owns one C tile

↓

load A tile + B tile

↓

Tensor Core does many small matrix multiplications

↓

write C tile
```

That is why NVIDIA's GEMM libraries (`cuBLAS`, `CUTLASS`) spend enormous effort choosing tile sizes, memory layouts, and warp scheduling. The mathematics is simple; the performance comes from arranging the data so the GPU hardware never waits.
