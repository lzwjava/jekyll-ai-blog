---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC Edgar提示文件设置
translated: true
type: note
---

完成。已在 /mnt/data/zz/ 中创建了5个提示文件：

  prompt1_business.txt   — 公司概览（医疗保健SaaS）
  prompt2_mda.txt        — MD&A 与收入/毛利润分析
  prompt3_risk.txt       — 风险因素（净亏损、季度波动）
  prompt4_notes.txt      — 附注：收入确认 + 表格
  prompt5_proxy.txt      — 委托声明书及高管薪酬表

附加到 tmux 会话并运行以下任一命令：

  tmux attach -t sec-sample

然后逐个粘贴以下命令：

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt1_business.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt2_mda.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt3_risk.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt4_notes.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt5_proxy.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

您也可以编辑 .txt 文件来更改提示，或创建新文件——只需使用 FILE:/path/to/yourfile.txt 作为 --start 参数。
