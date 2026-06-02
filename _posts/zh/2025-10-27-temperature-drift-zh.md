---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 温度引起的放大器零点漂移
translated: true
type: note
---

**C. 温度对晶体管参数的影响**

在直接耦合的多级放大电路中，由于无需耦合电容即可同时传输交流与直流信号，直流偏置电压的微小变化会在各级间被放大，导致零点漂移（即零输入时出现非期望的输出偏移）。虽然电源波动或元件失配等因素都会产生影响，但温度变化是引发该现象的主因。晶体管参数如基极-发射极电压（V_BE）和电流增益（β）会随温度显著变化——通常V_BE以约2mV/°C的速率下降——这种效应在多级电路中会产生累积偏移，使得热效应成为最突出且最难抑制的问题。

[如何抑制直接耦合放大电路的零点漂移](https://en.eeworld.com.cn/news/mndz/eic73044.html)
[第五讲 放大器](https://feng.stafpu.bu.edu.eg/Electrical%20Engineering/2460/crs-13711/Files/EEDP_Lect%2005_Amplifiers_2m.pdf)
