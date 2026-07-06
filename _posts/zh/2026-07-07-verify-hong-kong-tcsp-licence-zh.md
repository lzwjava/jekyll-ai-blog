---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 验证香港TCSP牌照
translated: true
type: note
---

**问题：** 如何验证香港公司注册代理的TCSP牌照？是否有官方政府网站可供查询？

**回答：**

有——香港设有官方的公开登记册。查询网站为 <https://www.tcsp.cr.gov.hk/tcspls/search/public-search，由公司注册处辖下的信托及公司服务提供者注册办事处运营。>

验证代理的步骤：

1. 要求代理提供其 **TCSP牌照号码**（格式如 `TC000123`）。任何合法代理都会将其印在网站页脚、发票或合作函上——持牌公司通常会公开标注，例如“TCSP牌照持有人（TC 0007484）”。如果对方犹豫不决，请立即放弃。
2. 通过牌照号码或公司名称在登记册中查询。确认三件事：**确切的法律实体名称**与您付款的对象一致（而非类似的内地实体）、牌照**状态有效/当前**、以及业务地址与对方提供的信息相符。
3. 通过公司注册处的e-Search（<https://www.e-services.cr.gov.hk）交叉核对实体本身，查看公司注册状态及申报记录。>

为何此事重要：自《打击洗钱条例》（第615章）生效以来，任何为客户提供公司成立服务的人士必须持牌，获批公司会自动出现在公共TCSP登记册中。淘宝/微信上许多标价¥4,380的“香港公司注册”卖家实为内地中介，转售持牌香港公司的服务——在此情况下，请获取将担任您公司秘书/注册地址的**实际香港TCSP**的名称，并验证该实体。

额外福利（CLI友好）：政府会在DATA.GOV.HK上以CSV/XLSX/API格式发布完整的TCSP持牌人清单，每月更新。因此您可以：

```bash
# 从data.gov.hk获取月度CSV（数据集：hk-cr-crtcspdata-list-tcsp-licensees）
# 然后：
grep -i "代理名称" tcsp_licensees.csv
```

注意：TCSP牌照是反洗钱/适当人选审查，而非质量保证。它确认该实体合法，但无法保证续期价格不会翻三倍。因此需双管齐下：验证牌照，并在付款前以书面形式获取续期及审计报价。

**参考资料：**

- [TCSP公共查询——公司注册处](https://www.tcsp.cr.gov.hk/tcspls/search/public-search)
- [TCSP持牌人清单——DATA.GOV.HK](https://data.gov.hk/en-data/dataset/hk-cr-crtcspdata-list-tcsp-licensees)
- [信托及公司服务提供者注册办事处](https://www.tcsp.cr.gov.hk/tcspls/index)
