---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 芯片设计迭代路径
translated: true
type: note
---

问题：基于我的背景（广东NOIP前300名，后来自学Android/iOS/前端/后端/英语/AI），学习芯片设计对我来说应该也不难。我应该找到真正的芯片专家，在推理芯片和训练芯片上进行小型迭代实验，从像基本加法器这样简单的东西开始吗？

回答：

部分同意，但需要对框架做一处修正：芯片设计并不是像iOS→Android→后端那样的"另一门需要掌握的语言"。那些都是冯·诺依曼架构硬件上的软件迁移——相同的抽象栈（编译器、操作系统、指令集），只是语法不同。数字IC设计是一个不同的物理栈：门电路→标准单元→布局布线→时序收敛→DRC/LVS→GDSII→光刻掩模版→晶圆厂。学习曲线陡峭不是因为概念难（加法器很简单），而是因为**工具链**的失败模式比你接触过的任何软件栈都多，而且流片后你无法用`print`来调试硅片。

不过，你的直觉在方向上是正确的，并且在2026年比历史上任何时候都更容易实现。原因如下，以及实际的路径。

**为什么加法器优先的迭代方法是对的**

你已经从nanochat/GPT-2-from-scratch中具备了这种思维：从最小、可端到端验证的东西开始，然后扩展复杂性。同样的原则适用于硅片：

1. 用Verilog实现全加器→用`iverilog`/`cocotb`仿真
2. 行波进位加法器→同上
3. 综合到门级（Yosys）→查看网表
4. 在开放PDK上进行布局布线（OpenROAD/LibreLane）→查看实际版图
5. 提交到真正的多项目晶圆（Tiny Tapeout）→获得流片回来的芯片

这完全镜像了你GPT-2-from-scratch的方法：不要直接跳到DeepSeek v4 MoE，先构建能训练的最小的Transformer。

**现在使得这一切真正可行的工具链**

这是值得精确了解的部分，因为五年前整个栈还不存在可访问的形式：

- **Yosys** — 开源RTL综合（Verilog→门级网表）
- **OpenROAD / LibreLane** — 自动化布局布线，目标是无人工干预的24小时流程
- **开放PDK** — SkyWater 130nm（谷歌赞助）、GlobalFoundries 180nm、IHP SG13G2 130nm——这些是实际的晶圆厂工艺设计套件，开源，而过去这需要NDA和六位数费用
- **Tiny Tapeout** — 多项目晶圆穿梭服务，将数百个小型设计拼接到一个共享芯片上，将成本从约1万美元以上降低到每个项目几百美元

具体来说：由于开源的EDA工具（如LibreLane和OpenROAD）、谷歌的开源PDK（SkyWater 130nm、GlobalFoundries 180nm、IHP 130nm）以及像Tiny Tapeout这样将数百个设计复用到共享芯片上的低成本穿梭计划，独立设计师现在可以在不破产的情况下流片定制ASIC。有记录显示，一位独立工程师独自在SKY130A工艺上流片了一个完整的BLAKE2s哈希加速器，另一位则构建了一个小型脉动阵列（矩阵乘法/训练加速器的实际构建模块）作为Tiny Tapeout提交，明确利用穿梭计划作为工具，同时掌握完全独立流片所需缺失的技能。

当前穿梭计划的状况，如果你想看实际时间线：Tiny Tapeout IHP 26a于2025年11月启动，2026年3月关闭提交，芯片预计2026年9月返回——所以从提交到拿到物理芯片大约需要6-9个月。还有SKY 26b穿梭计划于2026年4月启动，提交于2026年5月关闭。注意，IHP穿梭计划现在附带限制性贷款条款（芯片归IHP所有，不得商业使用，不得转售）——SkyWater穿梭计划才是你真正拥有所制造东西的渠道，因此在提交设计前请检查每个穿梭计划的条款。

**"推理芯片" vs "训练芯片"如何打破你的计划**

要诚实地看待这里的范围，因为这是你软件栈迁移类比最薄弱的地方：

- **Tiny Tapeout上的玩具加法器/ALU**——单人几周内真的可行，几个月内拿到真实芯片。很好的学习项目。
- **真正的推理加速器**（在INT8矩阵乘法上超过CPU的东西）——需要脉动阵列、权重的SRAM、内存接口，以及足够的面面积/功耗预算以避免成为玩具。可作为爱好级演示器实现（见上述脉动阵列示例——2x2阵列，特意做小以成为好的穿梭计划参与者）。
- **训练芯片**——需要高精度浮点运算、梯度累积，以及关键的高带宽内存级内存带宽。这不是单人周末项目，甚至不是单人一年项目——这是Groq/Cerebras/Tenstorrent规模团队的领域，真正的工艺节点需要数亿美元的NRE（非经常性工程）成本，并需要访问最前沿（而非开放）的PDK。你的MI300X经验让你对*为什么*这很难有了真实直觉（HBM带宽、内存-计算比）——用这种直觉正确衡量"玩具ASIC"和"真正训练芯片"之间的差距，不要让"我学了iOS和Android，芯片只是另一个领域"的表面叙事缩小这个差距。

**鉴于你的实际限制（房贷、12个月服务公司现金流、无芯片收入路径）的实用建议**

芯片设计是一个合理的20%精力产品赌注，而不是第一阶段的收入杠杆。目前没有广州/粤港澳/香港的客户付费让你流片ASIC——你的付费技能面是模型训练、微调、代理基础设施、LLM工具。把芯片当作你对待nanochat的方式：一项复合技能投资，放在收入之后，而非转向。

本周我实际推荐的具体起点：

```bash
# Yosys + 一个全加器，在仿真中验证，在你的RTX 4070机器甚至Air上
sudo apt install yosys iverilog
mkdir chip-101 && cd chip-101
cat > adder.v << 'EOF'
module full_adder(input a, b, cin, output sum, cout);
  assign sum  = a ^ b ^ cin;
  assign cout = (a & b) | (cin & (a ^ b));
endmodule
EOF
yosys -p "read_verilog adder.v; synth; show" adder.v
```

然后跟随Tiny Tapeout Verilog模板（如果你想要零摩擦，使用基本的Wokwi模板；如果你想真正学习流程，使用原始HDL），并瞄准当前开放的SKY穿梭计划。这就是你在硅片领域的"GPT-2 760M从头开始"等价物——小、完整、端到端，另一端产出真实硬件。

参考文献：

- [Tiny Tapeout](https://tinytapeout.com/)
- [BLAKE2s哈希加速器：单人流片之旅](https://essenceia.github.io/projects/blake2s_hashing_accelerator_a_solo_tapeout_journey/)
- [流片前两周——脉动阵列项目](https://essenceia.github.io/projects/two_weeks_until_tapeout/)
- [Tiny Tapeout IHP 26a穿梭计划状态](https://tinytapeout.com/chips/ttihp26a/)
- [Tiny Tapeout SKY 26b穿梭计划状态](https://tinytapeout.com/chips/ttsky26b/)
- [Tiny Tapeout IHP穿梭计划贷款条款变更](https://www.hackster.io/news/tiny-tapeout-opens-an-ihp-shuttle-for-your-open-source-chip-designs-but-beware-the-new-terms-77e0b292cae4)
