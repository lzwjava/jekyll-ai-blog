---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深南电路：三位一体商业模式
translated: true
type: note
---

问题：**什么是深南电路（Shennan Circuits / SCC）？**

回答：

![Image](https://images.openai.com/static-rsc-4/wWXFAisRVSBp4FDIFwx1bR42BeZbYiFVFrxoXDK1izC1DHNxK5ApNPuBnQZeVWPy637GuF-PJzKc5L_ilwykDsJTxHrmxecv2uVwOcGFW4n4nQOgjRXi3BoeUkzECC0S-BTxJjt2_C1qfCC4KsRzPq6SCCL3bw5T1Ujxk4sW5b79UomRXKIKlPLi4MF3MSqf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/y22TF8RVoKn1z7Km4lTMydzkyzSf_8MBPZdLB6FvokyXX4qnVyVGWSKCTjJyu0mifqErAEYmjRRVLtjEhGdpH7YnnbavyGZWAM3C4TDkkoJPSWQr0fRdIHY77PRs75P6rd60LBPoj64ZI_LnLF6n__SjLT3xBQ5r3KffrjV3NzqNwnXK75YrxwrQSzRaFpyt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/E353jnIsRe7d3wxSPFS-mtzQDXh5uySDI3dXLHvGmmzvg5x9LAZ-QyEoAcKgxJ8hR_BtFsQr2o3iC2gG9ybF8aZYtp0xgZ3nrG8KGjDIg2SzAH7zekSRtSJcOwOyzY_LvVs-0tE11W5RgYYrglKgFKnibQfAV2Y6kzIF8uYTarvxKQGPlrAGcLFr_ypbiB3s?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kzJj380ecKQrOmNnpMc8mSPXr3U8MBPZdLB6FvokyXX4qnVyVGWSKCTjJyu0mifqErAEYmjRRVLtjEhGdpH7YnnbavyGZWAM3C4TDkkoJPSWQr0fRdIHY77PRs75P6rd60LBPoj64ZI_LnLF6n__SjLT3xBQ5r3KffrjV3NzqNwnXK75YrxwrQSzRaFpyt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kzJj380ecKQrOmnNnpMc8mSPXr3U8MBPZdLB6FvokyXX4qnVyVGWSKCTjJyu0mifqErAEYmjRRVLtjEhGdpH7YnnbavyGZWAM3C4TDkkoJPSWQr0fRdIHY77PRs75P6rd60LBPoj64ZI_LnLF6n__SjLT3xBQ5r3KffrjV3NzqNwnXK75YrxwrQSzRaFpyt?purpose=fullsize)

**深南电路股份有限公司（Shennan Circuits, SCC）**是一家专注于**PCB、半导体封装基板和电子装联**的中国大型电子制造企业。公司成立于**1984年**，总部位于深圳，在深圳证券交易所上市，股票代码为**002916**。（[SCC][1]）

最简单的理解模型如下：

```text
Chip
  │
  ▼
┌─────────────────────┐
│ Packaging substrate │  ← connects chip/package
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        PCB          │  ← connects components
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       PCBA          │  ← PCB + chips/components
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Electronic system   │
└─────────────────────┘
```

SCC将这一模式称为**“三位一体”**业务模型：**PCB + 封装基板 + 电子装联**。其制造/服务能力大致覆盖电子封装产业链的第1至第3层级。（[Cninfo][2]）

### 1. PCB仍是核心业务

PCB = **印刷电路板**。

例如，一台AI服务器可能包含：

```text
NVIDIA GPU
   ↓
GPU package
   ↓
GPU board / accelerator PCB
   ↓
Server motherboard
   ↓
Network / storage / power boards
```

SCC负责制造连接这些组件的复杂PCB。

其重要的PCB应用领域包括：

* 电信
* 数据中心/服务器
* AI计算基础设施
* 汽车电子
* 工业控制
* 医疗设备

该公司尤其专注于**高速、高频、高层数和高密度PCB**。（[新浪财经][3]）

### 2. 封装基板是半导体的一部分

如果您关注**AI硬件**，这可能更有趣。

封装基板大致位于以下位置：

```text
        Silicon die
           │
           ▼
    ┌──────────────┐
    │   Package    │
    │ ┌──────────┐ │
    │ │   Die    │ │
    │ └──────────┘ │
    └──────┬───────┘
           │
     Package substrate
           │
           ▼
          PCB
```

它比普通PCB精密得多，为芯片封装与主板之间提供电气连接、机械支撑和热管理功能。

SCC生产的基板适用于：

* 内存
* 应用处理器
* 射频
* FC-CSP
* FC-BGA
* 其他半导体封装

根据其2025年年报，其2025年封装基板营收为**人民币41.5亿元**，同比增长**30.8%**。（[新浪财经][3]）

此外，该公司当时正在提升更高层数**FC-BGA**基板的能力，22层及以下产品已量产，24层及以上产品处于开发/样品阶段。（[FinancialFilings][4]）

### 3. PCBA / 电子装联

第三项业务大致如下：

```text
Bare PCB
   +
CPU / GPU / memory / PMIC / capacitors / connectors...
   ↓
SMT / THT / assembly
   ↓
PCBA
   ↓
Testing
   ↓
Electronic system
```

因此，SCC不仅仅是销售裸电路板，它还能进一步参与下游环节：**设计→PCB制造→元器件组装→测试→系统组装**。（[Cninfo][2]）

---

## 规模

2025年是SCC业绩强劲增长的一年。

| 2025 | 营收 | 同比 |
| -------------------- | ---------: | ----------: |
| **总计** | 人民币 **236.5亿** | **+32.05%** |
| PCB | 人民币 **143.6亿** | **+36.84%** |
| 封装基板 | 人民币 **41.5亿** | **+30.80%** |
| 电子装联 | 人民币 **30.7亿** | **+8.93%** |

因此，PCB仍然是最大业务板块，约占**总营收的61%**。（[新浪财经][3]）

而且这越来越成为一个**AI基础设施的故事**：SCC的2025年年报明确指出，AI计算基础设施投资的增长正在推动高端电子电路的需求，其2026年战略也聚焦于抓住这一结构性增长。（[深圳证券交易所][5]）

公司报告称，根据Prismark 2025年第四季度报告，预计其2025年营收将在全球PCB制造商中排名**第四**。（[FinancialFilings][4]）

### 在半导体/AI硬件生态系统中的位置

我们可以这样理解这个生态系统：

```text
TSMC / Samsung / Intel
        │
        │ wafers / dies
        ▼
Chip designers
NVIDIA / AMD / Broadcom / etc.
        │
        ▼
Packaging / OSAT
        │
        ▼
┌───────────────────────────┐
│     Shennan Circuits      │
│                           │
│  IC substrate             │
│       ↓                   │
│  PCB                      │
│       ↓                   │
│  PCBA / electronic system │
└───────────────────────────┘
        │
        ▼
Server / networking / telecom
        │
        ▼
AI data center
```

因此，**SCC并非像NVIDIA那样的芯片设计公司，也不像台积电那样是半导体代工厂**。

它是一家**电子互连与制造公司**，处于芯片与完整电子系统之间。

对于您关注的领域，特别相关的是：**AI加速器、高速网络、服务器和数据中心对PCB和封装基板的要求越来越高**。这也是SCC从AI基础设施资本开支周期中受益的原因之一。（[Cninfo][2]）

**参考资料：**

* [深南电路 — 公司简介](https://www.scc.com.cn/scc/gysn/index.html?utm_source=chatgpt.com)
* [深南电路 — 2025年年报](https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=11992852&stockid=002916&utm_source=chatgpt.com)
* [深南电路 — 2026年半年度报告](https://static.cninfo.com.cn/finalpage/2026-08-27/1225512708.PDF?utm_source=chatgpt.com)
* [深南电路 — 产品与技术](https://www.scc.com.cn/scc/cpjs/index.html?utm_source=chatgpt.com)

[1]: https://www.scc.com.cn/scc/gysn/index.html?utm_source=chatgpt.com "深南电路 - 关于深南"
[2]: https://static.cninfo.com.cn/finalpage/2026-08-27/1225512708.PDF?utm_source=chatgpt.com "深南电路股份有限公司 2026 年半年度报告全文"
[3]: https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=11992852&stockid=002916&utm_source=chatgpt.com "深南电路(002916)_公司公告_深南电路：2025年年度报告新浪财经_新浪网"
[4]: https://financialfilings.com/filings/shennan-circuits-co-ltd/annual-report/2026/36790692/?utm_source=chatgpt.com "Shennan Circuits Co., Ltd. - Annual Report 2025 | FinancialFilings"
[5]: https://disc.static.szse.cn/disc/disk03/finalpage/2026-03-13/342c7f6b-cc0c-4592-9d25-9f95ae113d57.PDF?utm_source=chatgpt.com "深南电路股份有限公司 2025 年年度报告全文"
