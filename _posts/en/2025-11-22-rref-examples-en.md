---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: RREF Step-by-Step Examples
translated: false
type: note
---

## Example 1: Simple 3×3 Matrix

**Starting matrix:**
```
[  2   4   -2  |  2 ]
[  1   3    1  |  4 ]
[  3   7   -1  |  8 ]
```

### Step 1: Make first pivot = 1
Divide Row 1 by 2:
```
[  1   2   -1  |  1 ]
[  1   3    1  |  4 ]
[  3   7   -1  |  8 ]
```

### Step 2: Eliminate below the first pivot
- Row 2 = Row 2 - Row 1
- Row 3 = Row 3 - 3(Row 1)

```
[  1   2   -1  |  1 ]
[  0   1    2  |  3 ]
[  0   1    2  |  5 ]
```

### Step 3: Make second pivot = 1 (already is!)
The second pivot (in Row 2, Column 2) is already 1.

### Step 4: Eliminate above and below second pivot
- Row 1 = Row 1 - 2(Row 2)
- Row 3 = Row 3 - Row 2

```
[  1   0   -5  | -5 ]
[  0   1    2  |  3 ]
[  0   0    0  |  2 ]
```

### Step 5: Move to third column
The third column has no pivot (it's all zeros below), so we're done!

**Final RREF:**
```
[  1   0   -5  | -5 ]
[  0   1    2  |  3 ]
[  0   0    0  |  2 ]
```

Notice: Leading 1s in a staircase pattern, zeros below AND above each pivot, zeros on the left.

---

## Example 2: 3×4 Matrix (More Zeros)

**Starting matrix:**
```
[  1   2   3   4  |  5 ]
[  2   4   7   8  | 12 ]
[  1   2   5   6  |  9 ]
```

### Step 1: First pivot is already 1
Column 1, Row 1 has a 1. Good!

### Step 2: Eliminate below first pivot
- Row 2 = Row 2 - 2(Row 1)
- Row 3 = Row 3 - Row 1

```
[  1   2   3   4  |  5 ]
[  0   0   1   0  |  2 ]
[  0   0   2   2  |  4 ]
```

### Step 3: Move to second column
Column 2 is all zeros below the first row. Skip to column 3!

### Step 4: Make third pivot = 1
Row 2 already has a 1 in Column 3. Move it to Row 2 (already there).

### Step 5: Eliminate above and below third pivot
- Row 1 = Row 1 - 3(Row 2)
- Row 3 = Row 3 - 2(Row 2)

```
[  1   2   0   4  | -1 ]
[  0   0   1   0  |  2 ]
[  0   0   0   2  |  0 ]
```

### Step 6: Make fourth pivot = 1
Divide Row 3 by 2:
```
[  1   2   0   4  | -1 ]
[  0   0   1   0  |  2 ]
[  0   0   0   1  |  0 ]
```

### Step 7: Eliminate above fourth pivot
Row 1 = Row 1 - 4(Row 3):
```
[  1   2   0   0  | -1 ]
[  0   0   1   0  |  2 ]
[  0   0   0   1  |  0 ]
```

**Final RREF:**
```
[  1   2   0   0  | -1 ]
[  0   0   1   0  |  2 ]
[  0   0   0   1  |  0 ]
```

Notice: Pivots in columns 1, 3, and 4. Column 2 has no pivot (it's a free variable). Zeros everywhere else in pivot columns.

---

## Key Points to Remember

- **Always work left to right, top to bottom**
- **One column at a time** – finish it completely before moving on
- **Each pivot becomes 1**
- **Eliminate BOTH above and below** each pivot (that's what makes it "reduced")
- **Once a column is done, don't mess with it** – only work below the current row for new pivots
- If a column has all zeros, skip it (no pivot there)

The systematic approach prevents you from going in circles!
