---
audio: false
generated: true
lang: zh
layout: post
title: qBittorrent文件校验：SHA-1哈希算法
translated: true
type: note
---

当你在 qBittorrent 中移动文件位置并在继续做种前重新检查文件时，它正在确保新位置中的文件与原先处理的文件相同。这种验证在种子下载中至关重要，以防止共享不正确或损坏的数据。以下是该过程的运作原理及其使用的算法：

### qBittorrent 如何验证文件
qBittorrent 不会简单地相信移动后的文件是正确的——它会通过将文件与种子文件中存储的信息进行比较来检查其完整性。在种子下载中，数据被分割成称为**分块**的较小部分，每个分块都有一个唯一的哈希值。这些哈希值包含在种子文件中，并作为每个数据分块的指纹。当你将文件移动到新位置时，qBittorrent 会使用这些分块哈希来确认文件未被更改。

该过程可以分为以下步骤：

1. **指定新位置**：你通过设置新的文件路径告诉 qBittorrent 文件现在的位置。
2. **将文件映射到种子**：qBittorrent 将新位置中的文件与种子中列出的文件进行匹配，通常使用文件名和大小（因为这些信息在种子文件中）。
3. **验证分块哈希**：qBittorrent 逐块读取新文件中的数据，计算每个分块的哈希值，并将其与种子文件中存储的相应哈希值进行比较。
4. **确认完整性**：如果所有计算出的哈希值与种子的哈希值匹配，则确认文件相同，qBittorrent 可以恢复做种。如果任何分块的哈希值不匹配，则该分块被标记为不完整或缺失，qBittorrent 可能需要重新下载它。

### 它使用什么算法？
qBittorrent 不使用完整文件校验和（例如整个文件的 MD5 或 SHA-256），因为那样会缓慢且低效，尤其是对于大文件。相反，它依赖于 BitTorrent 协议定义的**分块哈希**。用于这些分块哈希的算法是 **SHA-1**，一种广泛使用的加密哈希函数。每个数据分块（根据种子不同，可能是几千字节到几兆字节）都使用 SHA-1 进行哈希计算，而 qBittorrent 检查的正是这些哈希值。

使用分块哈希而不是完整文件校验和有两个主要优点：
- **效率**：检查较小的分块比哈希整个文件更快。
- **粒度**：如果出现问题，qBittorrent 可以精确定位需要修复的分块，而不是拒绝整个文件。

### 为什么这很重要
这种基于哈希的验证确保你从新位置做种的数据与其他对等方期望的数据匹配，从而维护种子群的完整性。如果没有这种检查，移动文件可能导致共享损坏或不匹配的数据，从而扰乱种子下载过程。

简而言之，当你在 qBittorrent 中移动文件位置时，它会通过计算每个分块的 **SHA-1 哈希**并将其与种子文件中的哈希值进行比较来重新检查文件。这就是它在恢复做种前确认一切正确的方式。

---

为了演示 qBittorrent 在移动文件位置时如何使用分块哈希（特别是 SHA-1 哈希）来验证文件完整性，这里有一个简单的 Python 脚本。qBittorrent 遵循 BitTorrent 协议，将文件分割成块，计算每个块的 SHA-1 哈希，并使用这些哈希来确保文件内容无论位于何处都保持不变。该脚本通过创建示例文件、计算其分块哈希、验证相同的副本，然后展示修改如何导致验证失败来模拟此过程。

### 说明
- **分块哈希**：脚本将文件分割成固定大小的块（例如 10 字节），并为每个块计算 SHA-1 哈希，模拟种子文件存储这些哈希的方式。
- **验证**：它检查文件的计算哈希是否与预期哈希匹配，从而确保完整性。
- **模拟**：它创建一个文件，复制它（模拟移动），验证它，然后修改副本并再次验证以显示如何检测更改。

以下是带有清晰注释的脚本：

```python
import hashlib
import shutil
import os

def compute_piece_hashes(file_path, piece_size):
    """计算文件中每个分块的 SHA-1 哈希值。"""
    hashes = []
    with open(file_path, 'rb') as f:
        while True:
            piece = f.read(piece_size)
            if not piece:
                break
            hash_obj = hashlib.sha1(piece)
            hashes.append(hash_obj.hexdigest())
    return hashes

def verify_file_integrity(file_path, piece_size, expected_hashes):
    """通过比较分块哈希来验证文件的完整性。"""
    current_hashes = compute_piece_hashes(file_path, piece_size)
    if len(current_hashes) != len(expected_hashes):
        return False
    for current, expected in zip(current_hashes, expected_hashes):
        if current != expected:
            return False
    return True

# 创建具有已知内容的示例文件
with open('file1.txt', 'w') as f:
    f.write("Hello, this is a test file.")

piece_size = 10  # 字节，为演示而设置较小值

# 从 file1.txt 计算预期哈希（模拟种子哈希）
expected_hashes = compute_piece_hashes('file1.txt', piece_size)
print("预期哈希:", [h[:8] for h in expected_hashes])  # 显示前8个字符以提高可读性

# 将 file1.txt 复制到 file2.txt 以模拟移动文件
shutil.copyfile('file1.txt', 'file2.txt')

# 根据预期哈希验证 file2.txt（应通过）
is_valid = verify_file_integrity('file2.txt', piece_size, expected_hashes)
print("file2.txt 验证（未更改）:", "有效" if is_valid else "无效")

# 修改 file2.txt 以模拟损坏或更改
with open('file2.txt', 'a') as f:
    f.write(" Modified")

# 再次验证（由于内容更改应失败）
is_valid = verify_file_integrity('file2.txt', piece_size, expected_hashes)
print("file2.txt 验证（已修改）:", "有效" if is_valid else "无效")

# 清理创建的文件
os.remove('file1.txt')
os.remove('file2.txt')
```

### 工作原理
1. **文件创建**：将 "Hello, this is a test file."（25 字节）写入 `file1.txt`。
2. **哈希计算**：将 `file1.txt` 分割成每个 10 字节的块（例如 "Hello, thi"、"s is a tes"、"t file."），计算 SHA-1 哈希，并将其存储为 `expected_hashes`。
3. **模拟移动**：将 `file1.txt` 复制到 `file2.txt`，表示文件已移动到新位置。
4. **初始验证**：根据 `expected_hashes` 检查 `file2.txt`。由于内容相同，它打印 "有效"。
5. **修改**：将 " Modified" 追加到 `file2.txt`，更改其内容和大小（现在为 34 字节，分割为 4 个块）。
6. **第二次验证**：检查修改后的 `file2.txt`。块的数量或其哈希值不同，因此它打印 "无效"。
7. **清理**：删除临时文件。

### 输出示例
```
预期哈希: ['dffd6021', 'a2b3c4d5', 'e6f789ab']  # 示例哈希前缀
file2.txt 验证（未更改）: 有效
file2.txt 验证（已修改）: 无效
```
（实际哈希值会有所不同，但遵循此模式。）

该脚本通过比较分块哈希来说明了 qBittorrent 如何确保文件完整性，即使在文件移动后也能检测到任何更改，使其成为该过程简单而有效的演示。
