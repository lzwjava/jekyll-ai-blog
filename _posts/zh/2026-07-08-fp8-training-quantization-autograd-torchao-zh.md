---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FP8训练：量化、自动微分、Torchao
translated: true
type: note
---

问题：解释这个用于 nanochat 的最小 FP8 训练实现是如何工作的——量化数学、三 GEMM 自动求导函数、`_scaled_mm` 布局约束，以及它为何/如何与 torchao 的张量子类方法不同。

答案：

## 1. 为什么用 FP8

在 H100/MI300X 上，张量核心存在吞吐量层级：FP8 GEMM 的每秒浮点运算数 (FLOPs) 大约是 BF16 GEMM 的两倍（每个周期的峰值 FLOP 数相同，但 FP8 每个操作数只使用一半的位数，因此 cuBLAS/cuBLASLt 和 CUTLASS 内核可以在相同的硅面积上推动更多 MAC/周期）。问题是 FP8 总共只有 8 位（1 位符号 + 4/5 位指数 + 3/2 位尾数），因此不能简单地将权重/激活静态地转换为 FP8——你需要**动态缩放**，以使张量的值保持在 FP8 的可表示范围内，而不会因下溢/溢出而丢失所有精度。

该文件只实现了一种方式：**张量级动态缩放**——每个张量一个标量缩放因子，每次前向/反向调用时根据张量的实际最大值重新计算。这是最便宜的变体（cuBLAS 在 `_scaled_mm` 内部为你处理缩放）；行级缩放需要更复杂的 CUTLASS 内核，因为每一行需要自己的缩放因子，并且要在累加过程中传递。

## 2. 量化数学

```python
fp8_max = torch.finfo(fp8_dtype).max          # 例如 e4m3fn 为 448.0
amax = x.float().abs().max()                   # 张量级最大幅值
scale = fp8_max / amax.double().clamp(min=EPS)  # 将 [0, amax] 映射到 [0, fp8_max]
x_fp8 = (x.float() * scale).clamp(-fp8_max, fp8_max).to(fp8_dtype)
inv_scale = scale.reciprocal()
```

这只是将零点固定在 0 的最小-最大仿射量化（对称量化）。在缩放除法中使用 `.double()` 的原因：FP8 量化误差累积很快，如果 `torch.compile` 以与 eager 模式不同的方式追踪此过程（不同的融合顺序 → 不同的中间舍入），则会在编译和未编译运行之间产生数值偏差。在 fp64 中进行除法消除了这种歧义——这与 torchao 使用的技巧相同。

注意传递给 `_scaled_mm` 的是 `inv_scale`，而不是 `scale`。这是因为 `_scaled_mm` 的约定是：*通过乘以 `scale_a * scale_b` 进行反量化*——因此它需要你用于量化的乘数的倒数。这是一个经典的“API 需要哪个方向的缩放因子”陷阱；弄反了会导致输出相差 `scale²`。

## 3. 格式选择：e4m3 与 e5m2

|  | 指数位 | 尾数位 | 动态范围 | 精度 |
|---|---|---|---|---|
| e4m3 | 4 | 3 | ±448（NVIDIA）/ ±240（AMD fnuz） | 更高（每个八度 8 个尾数级别） |
| e5m2 | 5 | 2 | ±57344 | 更低，范围更广 |

激活和权重（用于前向，即 `input @ weight.T`）使用 e4m3，因为它们的分布相对有界，并且你需要尾数精度。梯度使用 e5m2，因为梯度幅度在不同层/步骤之间变化多个数量级（梯度消失/爆炸区域），你宁愿要范围而不是精度——e4m3 梯度张量会不断截断或下溢。

AMD 的 ROCm 没有像 NVIDIA 那样实现 IEEE-754 风格的 FP8 次正规数——它使用“fnuz”（有限，无负零）变体，指数偏置偏移，因此幅度范围更小（240 对 448）。代码通过 `torch.version.hip` 检测并选择正确的 dtype——这一行使其能够在你的 RTX 4070（实际上 Ada 的 FP8 张量核心速度不快，但 MI300X 可以）和 AMD Dev Cloud 之间移植：

```python
_IS_AMD = torch.cuda.is_available() and hasattr(torch.version, 'hip') and torch.version.hip is not None
FP8_E4M3 = torch.float8_e4m3fnuz if _IS_AMD else torch.float8_e4m3fn
```

## 4. `_scaled_mm` 布局要求——弄错就会崩溃的部分

cuBLAS 的 FP8 内核（底层是 `cublasLtMatmul`）有一个硬件约束：**A 必须是行主序，B 必须是列主序**。这不是 PyTorch API 的选择，这实际上是 FP8 张量核心指令的连接方式（它们按行读取 A，按列读取 B，这与常规 GEMM 内核偏好特定布局的原因相同——加载路径上的内存合并）。

```python
def _to_col_major(x):
    return x.t().contiguous().t()
```

逐步解释：如果 `x` 是 `[N, K]` 行主序（步幅为 `(K, 1)`），那么 `x.t()` 是 `[K, N]`，步幅为 `(1, K)`——这从逻辑上已经是列主序了，但它是一个*视图*，如果底层存储在该视图的遍历顺序中不是连续的，内核无法简单地重新解释步幅——某些路径需要一个实际物化的列主序缓冲区。`.t().contiguous().t()`：转置（视图），强制以该转置顺序复制（`.contiguous()` 现在将内存物理布局为 `[K,N]` 行主序 = `[N,K]` 列主序），再转置回来以恢复逻辑上的 `[N,K]` 形状。净效果：形状相同，内存布局不同，如果需要则强制复制。

前向传递是免费的情况：

```python
output = torch._scaled_mm(
    input_fp8,          # [B, K] 连续 → 行主序，A 正确 ✓
    weight_fp8.t(),     # weight_fp8 是 [N, K] 连续 → .t() 是 [K, N] 步幅为 (1, K) → 已经是列主序 ✓ 无需复制
    ...
)
```

这就是为什么 `nn.Linear` 将 `weight` 存储为 `[out_features, in_features]` 而不是相反——这不仅仅是约定，它使得 `weight.t()` 可以免费用作 `input @ weight.T` 的列主序操作数。

反向传播需要另外两个 GEMM，这里的布局不是免费的：

```python
# grad_input = grad_output @ weight       [B,N] @ [N,K] -> [B,K]
go_fp8, go_inv = _to_fp8(grad_output, FP8_E5M2)     # [B,N] 行主序，A 正确 ✓
w_col = _to_col_major(w_fp8)                         # w_fp8 是 [N,K] 行主序，需要转换为列主序 — 复制
grad_input = torch._scaled_mm(go_fp8, w_col, ...)

# grad_weight = grad_output.T @ input     [N,B] @ [B,K] -> [N,K]
go_T = go_fp8.t().contiguous()   # go_fp8.t() 视图是 [N,B] 列主序；但 A 需要行主序 -> 物理复制
in_col = _to_col_major(in_fp8)   # in_fp8 是 [B,K] 行主序，需要列主序 -> 复制
grad_weight = torch._scaled_mm(go_T, in_col, ...)
```

因此每步每线性层你得到：1 次免费转置（前向），反向传播中 2 次强制复制（`w_col`，`in_col`）+ 1 次强制复制（`go_T`）= 3 个物理 FP8 张量复制。这些成本较低（FP8 = 1 字节/元素，并且张量已经量化，所以是一个快速的带步幅重映射的 memcpy），但它们是真正的受 GPU 带宽限制的内核——这是文档字符串中提到的“粘合操作”开销之外的实际开销。

## 5. `use_fast_accum`

```python
use_fast_accum=True   # 前向
use_fast_accum=False  # 反向（两个 GEMM）
```

`_scaled_mm` 的快速累积模式在张量核心流水线内部以降低的精度累积部分点积（跳过部分 FP32 累积阶段）以获得额外吞吐量。前向输出进入非线性/损失函数，那里可以容忍更多一点噪声；梯度直接决定数千步的权重更新，因此累积舍入误差会复合——因此在反向传播中使用完全累积精度。这反映了 torchao 和 NVIDIA 自己的方案（例如 Transformer Engine）的做法。

## 6. autograd.Function 本身

```python
@torch._dynamo.allow_in_graph
class _Float8Matmul(torch.autograd.Function):
```

`torch.autograd.Function` 是手写自定义前向/反向对的标准方式，当你想绕过 PyTorch 的逐操作自动求导追踪时使用（这里：因为 FP8 转换、`_scaled_mm` 调用和布局调整不是你希望在自动求导图中单独记录的东西——你想要一个原子性的“FP8 线性”节点，其反向传播由你手动定义）。

`ctx.save_for_backward(input_fp8, input_inv, weight_fp8, weight_inv)`——注意它保存的是**已经量化的 FP8 张量**，而不是原始的 fp32/bf16 张量。这是一个节省内存的技巧：FP8 张量比 fp32/bf16 小 4 倍/2 倍，因此反向传播的激活内存相应减少——这是 FP8 训练在原始矩阵乘法速度之外的主要实际优势之一，因为激活内存通常是 192GB MI300X 与 12GB 4070 上批大小的约束条件。

`@torch._dynamo.allow_in_graph`——告诉 Dynamo（`torch.compile` 背后的追踪器）“不要尝试追踪此函数内部的 Python 控制流，只在 FX 图中记录一个不透明调用节点，并依赖类自己的前向/反向进行自动求导。”没有这个，`torch.compile` 会尝试直接追踪 autograd.Function 的 Python 主体，在 `ctx.save_for_backward` 处阻塞，并导致图中断或产生语义错误的结果。

## 7. 这与 torchao 的根本区别

torchao 的 `Float8TrainingTensor` 是一个**张量子类**：它将 FP8 数据 + 缩放因子包装为适当的 `torch.Tensor` 子类型，并实现 `__torch_dispatch__`，这意味着每个触及此张量类型的 aten 操作（`aten.mm`、`aten.t`、`aten.reshape`、`aten.clone`...）都会被拦截并重新路由到 FP8 感知的内核。这很强大——这意味着任意代码（`x.reshape(...).clone()[0:10]`）“正常运作”并保持 FP8 感知，而无需你编写特定于矩阵乘法的 autograd.Function。但它需要为几乎每个可能触及张量的操作设置一个分发处理程序，因此大约 2000 行代码。

相反，此文件将 FP8 特性视为**一个线性层矩阵乘法的局部实现细节**，而不是一个通过张量类型系统传播的属性。`Float8Linear.forward` 接收普通的 bf16 张量并返回普通的 bf16 张量——FP8 永远不会离开此函数。这就是为什么它大约只有 150 行：你不是在构建一个类型系统，而是在编写三个 GEMM 调用。

具体来说，编译图的影响：使用 torchao，如果你有 `Float8Linear -> LayerNorm -> Float8Linear`，Inductor 会将 amax/scale/cast 操作视为单独的图节点，并且有可能将 LayerNorm 的输出写入与下一层的 `amax` 归约融合（相同的内存传递）。使用这种方法，Inductor 将 `Float8Linear` 视为一个不透明的调用——它可以优化所有*周围*的操作（融合注意力内部操作，融合归一化），但将 FP8 边界视为一堵硬墙。实际上，矩阵乘法本身在 FLOPs 上比粘合操作高出几个数量级，因此这种融合损失对总步骤时间来说只是一个舍入误差——根据其自身的文档字符串，此文件“略快”的实际原因是避免了张量子类分发开销（Python 级别的 `__torch_dispatch__` 调用不是免费的）以及更简单的编译图（在 Dynamo/Inductor 追踪上花费更少时间）。

## 8. `convert_to_float8_training`——模块修改函数

```python
def _convert(mod, prefix=""):
    for name, child in mod.named_children():
        fqn = f"{prefix}.{name}" if prefix else name
        _convert(child, fqn)   # 后序：先递归到子节点
        if isinstance(child, nn.Linear) and not isinstance(child, Float8Linear):
            if module_filter_fn is None or module_filter_fn(child, fqn):
                setattr(mod, name, Float8Linear.from_float(child))
```

后序遍历（先子节点后父节点）在这里很重要，主要是为了在通过 `setattr` 中途修改树时 `named_children()` 迭代的正确性——先递归避免了在访问子节点之前替换节点可能导致的任何顺序问题。`module_filter_fn` 是你用来跳过例如最终 `lm_head`（词汇量大小，可能不是 16 的倍数，某些 FP8 内核需要）或嵌入层附近的线性层的钩子，在这些地方 FP8 对收敛的损害超过了其价值（这与 DeepSeek-v2/v3 论文报告的一致——它们将某些层，如输出投影或 MoE 路由器，保持在高精度）。

`Float8Linear.from_float` 使用 `torch.device("meta")` 构建新的模块外壳而不分配实际存储，然后重新分配 `.weight`/`.bias` 指向*原始*张量——转换过程零额外 GPU 内存，仅是一个类型级的垫片。这与 `nn.Module._apply` 内部相同的模式，并且符合你希望将 FP8 集成到现有 GPT-2/nanochat 检查点加载路径而不触及状态字典的方式。

## 针对你的 MI300X 运行的实际注意事项

鉴于你正在进行 nanochat 并朝着 DeepSeek v4 MoE 前进：MoE 路由器/门控线性层正是你希望用 `module_filter_fn` 从 FP8 中排除的层（相对于专家 FFN 的小维度，并且路由决策对精度敏感——由量化噪声导致的错误路由令牌是一个比常规 FFN 中略微偏离的梯度更大的正确性风险）。另外值得检查：MI300X 的 FP8 张量核心吞吐量优势相对于 BF16 是真实的，但在某些基准测试中小于 H100，这是由于不同的矩阵核心代际（CDNA3 与 Hopper）——在假设两倍数字之前，值得在你的实际形状上对 `_scaled_mm` 与普通 `bf16 @ bf16` 进行性能分析。