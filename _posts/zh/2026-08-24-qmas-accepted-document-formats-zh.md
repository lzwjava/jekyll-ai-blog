---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QMAS 接受的文件格式
translated: true
type: note
---

问题：香港优秀人才入境计划（QMAS）在线申请系统接受哪些文件格式的上传？

答案：

QMAS 在线申请系统接受以下格式：（[Immigration Department Web App][1]）

| 格式        | 推荐用途                                                             |
| ----------- | -------------------------------------------------------------------- |
| PDF         | ✅ 证书、合同、银行流水、成绩单的最佳选择                             |
| JPEG / JPG  | 适用于护照页、身份证、照片                                           |
| PNG         | 可接受，适用于截图/扫描图像                                          |
| GIF         | 可接受，但不推荐                                                    |
| TIF / TIFF  | 可接受，主要用于专业扫描                                             |

限制：（[Immigration Department Web App][1]）

* 最大文件大小：**每个文件 5 MB**
* 无照片文件：可接受灰度扫描
* 有照片文件：请使用彩色扫描

---

我对 QMAS 的建议：

## 几乎全部使用 PDF

示例：

```
01 Passport.pdf
02 ID Card.pdf

03 Net Worth/
   bank_statement.pdf
   property_certificate.pdf

04 Education/
   degree_certificate.pdf
   transcript.pdf

05 Work Experience/
   LeanCloud_employment.pdf
   HSBC_employment.pdf
   Meitai_employment.pdf

06 Income/
   tax_record.pdf
   salary_slips.pdf

07 IELTS.pdf

08 Achievement/
   github_projects.pdf
   blog_statistics.pdf
```

---

## 扫描设置

推荐：

```
分辨率：
300 dpi

色彩：
证书/照片使用彩色

格式：
PDF

压缩：
中等
```

一份 10 页的 PDF 通常应小于 5 MB。

---

## 关于护照

更好：

```
passport.pdf
```

包含：

* 个人信息页
* 签证页
* 香港入境盖章（如有）

除非必要，不要单独上传 PNG 页面。

---

## 关于照片

使用：

```
photo.jpg
```

因为这是图像要求。系统接受 JPEG/PNG，但 JPEG 通常最稳妥。（[Government of Hong Kong][2]）

---

## 文件数量很重要

QMAS 对每个类别有最大上传数量限制。例如：（[Government of Hong Kong][2]）

* 护照：最多 5 个文件
* 资产净值：最多 3 个文件
* 学历：最多 10 个文件
* 工作经验：最多 10 个文件
* 成就：最多 10 个文件

因此，不要上传 50 张小图片：

不佳：

```
salary1.png
salary2.png
salary3.png
salary4.png
...
```

更好：

```
salary_records_2023_2026.pdf
```

将相关页面合并到一个 PDF 中。

---

针对您的情况（AI 工程师 + 可能申请 QMAS）：

我会准备一份 **专业的 PDF 文件包**：

```
QMAS_Application/
├── Identity.pdf
├── Education.pdf
├── Career_History.pdf
├── AI_Achievements.pdf
├── Financial_Status.pdf
├── Income.pdf
├── IELTS.pdf
└── Family_Documents.pdf
```

这样便于入境事务处官员审阅。

[1]: https://webapp.es2.immd.gov.hk/applies2-client/static/faq/pnv-qmas/en-US/entry_faq.html?utm_source=chatgpt.com "ESERVICES2"
[2]: https://www.gov.hk/en/nonresidents/visarequire/visasentrypermits/applyqmas.htm?pla=null&utm_source=chatgpt.com "GovHK: Online Application for Entry to Hong Kong under the Quality Migrant Admission Scheme"
