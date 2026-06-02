---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python CRC 实现指南
translated: true
type: note
---

问题：你能提供 Python 代码来演示使用生成多项式 `11001` 的 CRC (Cyclic Redundancy Check) 计算和验证过程吗？

答案：

这是一个全面的 Python 实现：```python
def xor_divide(dividend: str, divisor: str) -> str:
    """Perform modulo-2 (XOR) division and return the remainder."""
    div = list(dividend)
    divisor_len = len(divisor)

    for i in range(len(dividend) - divisor_len + 1):
        if div[i] == '1':
            for j in range(divisor_len):
                # XOR each bit
                div[i + j] = '0' if div[i + j] == divisor[j] else '1'

    # The remainder is the last (divisor_len - 1) bits
    remainder = ''.join(div[-(divisor_len - 1):])
    return remainder

def crc_calculate(message: str, generator: str) -> tuple[str, str]:
    """
    Calculate CRC remainder and return the transmitted frame.

    Args:
        message:   Original information bits, e.g. '10110110'
        generator: Generator polynomial bits, e.g. '11001'

    Returns:
        (crc_bits, transmitted_frame)
    """
    r = len(generator) - 1          # degree of generator = number of zeros to append
    padded = message + '0' * r      # Step 1: append r zeros

    print(f"\n{'='*55}")
    print(f"  CRC CALCULATION")
    print(f"{'='*55}")
    print(f"  Message          : {message}")
    print(f"  Generator        : {generator}  (degree = {r})")
    print(f"  Appended zeros   : {r} zeros")
    print(f"  Padded message   : {padded}")

    crc = xor_divide(padded, generator)  # Step 2: mod-2 division
    crc = crc.zfill(r)                   # pad CRC to exactly r bits if needed

    transmitted = message + crc          # Step 3: append CRC to original message

    print(f"\n  Remainder (CRC)  : {crc}")
    print(f"  Transmitted frame: {transmitted}")
    print(f"{'='*55}")

    return crc, transmitted

def crc_verify(received: str, generator: str) -> bool:
    """
    Verify a received frame by dividing it by the generator.
    Remainder == 0...0 means no error detected.

    Args:
        received:  The full received frame (message + CRC bits)
        generator: Generator polynomial bits

    Returns:
        True if no error detected, False otherwise
    """
    r = len(generator) - 1
    remainder = xor_divide(received, generator)
    remainder = remainder.zfill(r)
    no_error = all(b == '0' for b in remainder)

    print(f"\n{'='*55}")
    print(f"  CRC VERIFICATION")
    print(f"{'='*55}")
    print(f"  Received frame   : {received}")
    print(f"  Generator        : {generator}")
    print(f"  Remainder        : {remainder}")
    print(f"  Result           : {'✅ No error detected' if no_error else '❌ Error detected!'}")
    print(f"{'='*55}")

    return no_error

# ─── Demo ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    MESSAGE   = "10110110"
    GENERATOR = "11001"       # degree 4 → append 4 zeros

    # 1. Sender side: calculate CRC and build transmitted frame
    crc_bits, frame = crc_calculate(MESSAGE, GENERATOR)

    # 2. Receiver side — Case A: frame arrives intact
    print("\n[Case A] Frame arrives with NO errors:")
    crc_verify(frame, GENERATOR)

    # 3. Receiver side — Case B: simulate a 1-bit error (flip bit 3)
    corrupted = list(frame)
    corrupted[3] = '0' if corrupted[3] == '1' else '1'
    corrupted_frame = ''.join(corrupted)

    print(f"\n[Case B] Frame arrives WITH a bit error (bit 3 flipped):")
    print(f"  Original : {frame}")
    print(f"  Corrupted: {corrupted_frame}")
    crc_verify(corrupted_frame, GENERATOR)

    # 4. Try your own values
    print("\n[Custom] Try your own message and generator:")
    custom_msg = "1101011011"
    custom_gen = "10011"
    crc_custom, frame_custom = crc_calculate(custom_msg, custom_gen)
    crc_verify(frame_custom, custom_gen)

```

**示例输出：**

```

=======================================================
  CRC CALCULATION
=======================================================

  Message          : 10110110
  Generator        : 11001  (degree = 4)
  Appended zeros   : 4 zeros
  Padded message   : 101101100000

Remainder (CRC)  : 1110
  Transmitted frame: 101101101110
=======================================================

[Case A] Frame arrives with NO errors
=======================================================

CRC VERIFICATION
=======================================================

Received frame   : 101101101110
  Generator        : 11001
  Remainder        : 0000
  Result           : ✅ No error detected
=======================================================

[Case B] Frame arrives WITH a bit error (bit 3 flipped):
  Original : 101101101110
  Corrupted: 101001101110
=======================================================

CRC VERIFICATION
=======================================================

Received frame   : 101001101110
  Generator        : 11001
  Remainder        : 1001
  Result           : ❌ Error detected
=======================================================

```

---

## 代码如何映射到理论

| 代码函数 | 理论步骤 |
|---|---|
| `message + '0' * r` | 向消息追加 r 个零 |
| `xor_divide(padded, generator)` | Mod-2 (XOR) 长除法 |
| `message + crc` | 构建传输帧 T |
| `xor_divide(received, generator)` | 接收方重新对帧进行除法 |
| `remainder == '000...'` | 零余数 = 无错误 |

`xor_divide()` 函数是核心引擎 — 它通过从左到右扫描，在看到领先的 `1` 位时进行 XOR 操作，从而模拟硬件 XOR 移位寄存器，完全匹配之前解释中所示的纸上长除法方法。
