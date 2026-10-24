---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向 Tiny M 的 W4A4 NVFP4 GEMV
translated: true
type: note
---

`fp4_gemv_kernel` 是 `kernels/fp4_gemv/fp4_gemv.cu` 中的单一计算内核——一个手写的 **W4A4 NVFP4 GEMV，用于极小 M**（decode/MTP-verify MLP），针对 sm_120a 优化。它精确计算 tensor-core b12x 语义，只是用 FP16-向量 ALU 路径替代了 `mma`：

```
out[t,n] = alpha * Σ_g (sa[t,g]·sw[n,g]) * Σ_{i<16} qa[t,16g+i]·qw[n,16g+i]
```

每个 token t 对应一个 GEMV：激活值 `qa`（NVFP4/e2m1）与权重 `qw` 做点积，每 16 个值为一组，乘以激活值缩放因子 `sa` × 权重缩放因子 `sw`，再乘以全局 `alpha`（= input_scale · weight_scale_2）。

### 模板与启动形状

```cpp
template <int K, int T, int kRowsPerWarp, int kBlockRows>
__global__ void fp4_gemv_kernel(const uint8_t* xq, const uint8_t* xs,
                                const uint8_t* wq, const uint8_t* ws,
                                const float* alpha, __nv_bfloat16* out, int n)
```

- `K` = 归约维度，`T` = token 数量（运行时 M，1–8，通过 `switch (m)` 分派），`kRowsPerWarp` = 1 或 2，`kBlockRows` = 8 或 16。
- Grid = `n / kBlockRows`（每个 CTA 对应一个输出行块），block = `kBlockRows/kRowsPerWarp × 32` 线程。
- 每个 CTA 覆盖所有 M 个 token × 完整 K，用于其 8/16 个输出行——这就是“小 M”技巧：不在 token 维度上浪费 tensor-core 的 tile 填充。

### 数据布局辅助（NVFP4 块缩放重排）

- `decode16(packed, h[8])`：通过 `cvt.rn.f16x2.e2m1x2`（原生 PTX）将 16 个打包的 e2m1 字节解包到 8 个 `f16x2` 寄存器。精确：e2m1 精确解码为 f16。
- `hfma2` = `fma.rn.f16x2`，`group_sum` 将一个 `f16x2` 拆回两个 fp32 并相加。
- `sf_offset(row, group, groups)`：在 **重排的 128×4 布局** 中定位块缩放因子——`(row/128)·(groups/4) + group/4` 选择 512 字节块，然后 `(row%32)·16 + ((row%128)/32)·4 + group%4` 选择块内的字节。
- `weight_row(flat)`：对 CTA 的行块进行逆重排——扁平行 0..3 → {0, 32, 64, 96}（一个“四元组”），4..7 → {1,33,65,97}，以此类推。

四元组映射的意义：对于一个 64 列缩放 tile，CTA 的 4 行的缩放因子是 **64 个连续字节** → 各自只需一次 `uint4` 加载。

### 阶段 1 —— 序曲（缩放因子到共享内存）

- `w_scale[kBlockRows][kGroups]`：每个 lane 任务从 `ws` 中为每个（tile, 四元组）加载一个 `uint4`，并将 4 个字节散射到 `w_scale[quartet*4+quartile][kt*4]`——重建每行每组的权重缩放因子表。
- `x_scale[T][kGroups]`：激活值缩放因子，通过 `sf_offset` 获得。
- 一次 `__syncthreads()`；权重/激活缩放因子在整个内核生命周期中常驻。

### 阶段 2 —— 组并行主循环

```cpp
for (phase = 0; phase < kPhases; ++phase) {
    g = phase * 32 + lane;                        // 每个 lane 负责一个 16 值组
    // 解码权重组 -> wv[r][8] f16x2, wsc[r] = e4m3(scale)
    for (t = 0; t < T; ++t)
      for (r = 0; r < kRowsPerWarp; ++r)
        h = Σ_i hfma2(wv[r][i], xv[i], 0);         // f16x2 偶/奇部分和，精确
        acc[r][t] += group_sum(h) * wsc[r] * xsc;
}
```

**这就是整个内核的浓缩：** lanes 以 16 值组为单位步进 K，每个阶段每个 lane 处理一个组（32 个 lane 所以每阶段 32 个组）；每个 lane 将每组的乘积累加到寄存器累加器 `acc[kRowsPerWarp][T]` 中。由 `FP4_GEMV_UNROLL`（默认 4，可调）展开。

### 阶段 3 —— 尾声

对于每个（row, token）：通过 **warp-shuffle reduce** 归约 32 个 lane 的 `acc`（每个 lane 持有不同的组偏移），然后 lane 0 写入 `out[t·n + row[r]] = bf16(acc · alpha)`。K × 1 行 → 32 个部分组和 → 完整点积。

### 数值精度——为何每组精确

- e2m1 → f16：精确。8 个 ≤2^6 值的乘积：每个 f16 部分和 ≤ 8·36 = 288 < 512，因此每个 `fma.rn.f16x2` **精确**（f16 ulp 低于 512 时为 1/4）。
- 偶数和奇数的部分和在 fp32 中精确相加；`sa·sw`（两个 e4m3）精确；group_sum · (sa·sw) ≤ 2^20 位，在 fp32 中仍然精确。
- 因此与 b12x tensor-core 路径的唯一区别是 **跨组 fp32 加法的顺序**——因而“在内核测试中与 b12x 位等价”，使其成为安全的替代方案。

为什么采用这种形状：当 M ≤ 5（down K=17408） / M ≤ 4（gate_up N=34816, K=5120）时，tensor-core tile 会浪费大部分 M 维度的工作，因此 FP16-向量路径（将 K 分割到 lanes 上）更快；超过这些 M 值时，`.cu` 头注释说明 b12x “同样快或更快”，Python 调度会回退到 `flashinfer_scaled_fp4_mm(..., backend="b12x")`。
