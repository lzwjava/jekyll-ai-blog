---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: 诊断系统卡顿原因
translated: true
type: note
---

当系统在长时间运行的脚本期间卡住时，确实令人沮丧！您提供的Python代码虽然采用了逐行顺序处理文件的方式（这对内存管理很友好），但您描述的系统卡死和鼠标无响应现象，强烈表明这是**系统级资源耗尽**或**磁盘I/O瓶颈**导致的问题，而非脚本内部的内存泄漏。

以下是潜在原因分析和解决方案：

## 💾 系统卡死的潜在原因

系统卡死很可能是因为脚本消耗了关键系统资源，导致整个Ubuntu桌面环境（**GNOME/Wayland/Xorg**）失去响应。

-----

### 1. **磁盘I/O饱和（最可能原因）**

读写大量数据到磁盘，特别是在循环处理多个文件时，可能导致磁盘带宽饱和。

* **Parquet读取**：虽然Parquet格式效率很高，但读取20个大文件仍会涉及海量的顺序及随机磁盘读取操作
* **文本写入**：持续向输出文件`fineweb_extracted_all.txt`追加内容会导致不间断的磁盘写入
* **问题根源**：当磁盘（特别是**SATA机械硬盘**或低端**SATA固态硬盘**）完全被应用程序的I/O操作饱和时，系统处理其他I/O（包括桌面环境数据读写、鼠标移动和内核进程）的能力会严重下降，导致系统全局冻结

### 2. **内存/交换空间颠簸（可能性较小，但需考虑）**

虽然您的代码不会将所有数据存储在内存中，但操作系统和pandas仍需要**工作内存**和**页面缓存**

* **DataFrame开销**：即使逐行处理，加载单个Parquet文件的完整DataFrame（`df = pd.read_parquet(parquet_file)`）仍需要与该文件大小成比例的内存。如果系统**RAM**有限且DataFrame很大，操作系统可能开始大量使用磁盘上的**交换分区**
* **问题根源**：交换速度远慢于RAM。如果系统频繁在RAM和磁盘间交换数据（**颠簸**），会加剧I/O瓶颈（原因1），从而 effectively 使整个系统停滞

### 3. **CPU负载峰值（不太可能导致持续卡死）**

虽然您的脚本不是CPU密集型，但**pandas I/O操作**偶尔会使用多核或导致短暂的CPU峰值，但这通常只会造成系统变慢，而非完全卡死

-----

## 🛠️ 解决方案与故障排除步骤

要解决此问题，您需要减轻系统负载或在卡死发生时监控实际情况

### 1. 监控系统资源

下次运行脚本前，先打开终端并运行系统监控工具：

* **`htop`**（监控CPU和内存使用情况）
* **`iotop`**（监控磁盘I/O使用情况 - 这是诊断您问题的关键工具）
* **`nmon`**（全面查看所有资源）

在脚本运行时观察**`iotop`**。如果Python进程的**IO**列（或顶部的整体磁盘利用率）持续接近**100%**，那么磁盘I/O饱和就是根本原因

### 2. 实施I/O限流（最佳编码解决方案）

可以引入短暂的战略性延迟，让磁盘有机会"追赶"进度并释放资源给操作系统

* **添加小延迟**：在处理大量行后添加`time.sleep()`

<!-- end list -->

```python
# ... 在内层循环中：
                    if text_content and text_content.strip():
                        f.write(text_content.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")

                    total_rows_processed += 1

                    # 进度报告
                    if i % 10000 == 0:
                        print(f"文件 {file_idx + 1} - 已处理 {i} 行，总计：{total_rows_processed}")

                        # ✨ 添加此行让系统得以喘息
                        # 数值（如0.1秒）可能需要调整
                        import time
                        time.sleep(0.1)
```

### 3. 优化文本提取（提升I/O效率）

不使用Python逐行迭代（这种方式通常较慢且I/O密集），而是让**pandas**高效处理提取，每个文件只写入一次

```python
# 替代方案：
# for i, row in df.iterrows(): ...
# 和逐行写入...

# 使用这种向量化方法：
text_col = None
for col in ['text', 'content', 'article', 'text_content', 'body']:
    if col in df.columns:
        text_col = col
        break

if text_col:
    # 1. 选择文本列
    texts = df[text_col].astype(str).tolist()

    # 2. 将此文件的所有文本合并为一个字符串
    # 应用分隔符'<|endoftext|><|endoftext|><|endoftext|>'
    file_output = "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n".join(texts)

    # 3. 一次性写入整个文件内容
    f.write(file_output.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")

    total_rows_processed += len(df) # 更新整个DataFrame的计数
```

这种向量化方法大幅减少了零散、缓慢的磁盘**写入**调用，将其转换为每个Parquet文件一次大型快速写入。这应该能显著缓解I/O瓶颈问题。
