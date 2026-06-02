---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卡尔曼滤波器在博客数据清洗中的应用
translated: true
type: note
---

不错的代码库！对于像这样的Jekyll风格博客，卡尔曼滤波器非常适合将嘈杂的时间序列数据转化为清晰的视觉效果或交互式演示。以下是实际应用方式——以及一个可直接粘贴到代码库中的即用型处理流程。

## 在博客中应用卡尔曼滤波的场景

* 平滑嘈杂的**页面访问统计**（日访问量、跳出率、会话时长），让读者看到趋势而非波动
* 在绘制图表前对**构建/测试指标**去噪（例如每日警告数、`conversion_errors.log`中的错误数）
* 清理可能分享的**类传感器序列**——GPS轨迹、实时打字速度、滚动深度等
* 发布**教学文章**：展示过程/测量噪声如何改变估计值的交互式演示

---

## 快速实现：将Python图表转为博客静态图片

若只需为文章生成图表，将脚本最后一行从`plt.show()`改为：

```python
plt.savefig("assets/kalman/toy.png", dpi=200, bbox_inches="tight")
```

然后在文章中嵌入：

```markdown
![卡尔曼演示](/assets/kalman/toy.png)
```

---

## 开箱即用流程：平滑任意CSV序列并发布PNG+JSON

### 1) 准备数据文件

创建`assets/data/pageviews.csv`，包含`t,value`或`date,value`列：

```
date,value
2025-07-01, 1023
2025-07-02, 980
2025-07-03, 1135
```

### 2) 添加可复用脚本

创建`scripts/kalman/smooth_series.py`：

```python
#!/usr/bin/env python3
import argparse, csv, json, math, os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class Kalman1DConstVel:
    def __init__(self, dt, q, r, x0=None, v0=0.0):
        self.dt = float(dt)
        self.A = np.array([[1.0, self.dt],
                           [0.0, 1.0]])
        self.H = np.array([[1.0, 0.0]])
        # Q for constant-acceleration driving noise (σ_a^2 = q)
        self.Q = q * np.array([[0.25*self.dt**4, 0.5*self.dt**3],
                               [0.5*self.dt**3,    self.dt**2]])
        self.R = np.array([[r]])
        self.x = np.array([[x0 if x0 is not None else 0.0],
                           [v0]])
        self.P = np.eye(2) * 1.0

    def predict(self):
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        # z is scalar measurement of position
        z = np.array([[float(z)]])
        y = z - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.P.shape[0])
        # Joseph form for numerical stability
        self.P = (I - K @ self.H) @ self.P @ (I - K @ self.H).T + K @ self.R @ K.T

    def current_pos(self):
        return float(self.x[0, 0])

def read_csv_series(path):
    ts, ys = [], []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        cols = {k.lower(): k for k in r.fieldnames}
        has_date = "date" in cols
        for row in r:
            if has_date:
                # Convert to ordinal spacing; we’ll treat samples as 1-step apart visually
                ts.append(datetime.fromisoformat(row[cols["date"]]).toordinal())
            else:
                ts.append(float(row[cols.get("t", "t")]))
            ys.append(float(row[cols.get("value", "value")]))
    # If dates were used, reindex t as 0..N-1 for plotting simplicity
    if len(ts) and isinstance(ts[0], int):
        ts = list(range(len(ts)))
    return np.array(ts, dtype=float), np.array(ys, dtype=float)

def smooth_series(t, y, dt, q, r):
    kf = Kalman1DConstVel(dt=dt, q=q, r=r, x0=y[0])
    est = []
    for z in y:
        kf.predict()
        kf.update(z)
        est.append(kf.current_pos())
    return np.array(est, dtype=float)

def plot_and_save(t, y, est, out_png):
    plt.figure(figsize=(10, 5))
    plt.plot(t, y, ".", label="测量值")
    plt.plot(t, est, "-", linewidth=2, label="卡尔曼估计值")
    plt.xlabel("t")
    plt.ylabel("数值")
    plt.title("卡尔曼平滑（恒定速度模型）")
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="输入CSV (t,value) 或 (date,value)")
    ap.add_argument("--out-prefix", required=True, help="输出路径前缀 如 assets/kalman/pageviews")
    ap.add_argument("--dt", type=float, default=1.0, help="采样时间间隔")
    ap.add_argument("--q", type=float, default=0.05, help="过程方差（加速度平方）")
    ap.add_argument("--r", type=float, default=4.0, help="测量方差")
    args = ap.parse_args()

    t, y = read_csv_series(args.inp)
    est = smooth_series(t, y, dt=args.dt, q=args.q, r=args.r)

    out_png = f"{args.out_prefix}.png"
    out_json = f"{args.out_prefix}.json"
    plot_and_save(t, y, est, out_png)

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as f:
        json.dump({"t": t.tolist(), "y": y.tolist(), "est": est.tolist()}, f)
    print(f"已生成 {out_png} 和 {out_json}")

if __name__ == "__main__":
    main()
```

### 3) 添加Make目标

在`Makefile`中：

```make
kalman:
 python3 scripts/kalman/smooth_series.py --in assets/data/pageviews.csv \
  --out-prefix assets/kalman/pageviews --dt 1.0 --q 0.05 --r 4.0
```

运行：

```bash
make kalman
```

将获得：

* `assets/kalman/pageviews.png`——可直接嵌入
* `assets/kalman/pageviews.json`——用于可选交互功能

### 4) 在文章中嵌入（静态）

创建`notes/2025-08-17-kalman-pageviews.md`：

```markdown
---
layout: post
title: 使用卡尔曼滤波器平滑博客统计
---

下图：红点为原始日页面访问量，蓝线为卡尔曼估计值。

![页面访问量（卡尔曼）](/assets/kalman/pageviews.png)
```

---

## 可选：轻量级客户端可视化（无需库）

在生成JSON后，将此代码段插入文章。使用纯SVG绘制两条折线（原始值 vs 估计值）。

```html
<div id="kalman-chart"></div>
<script>
(async function () {
  const res = await fetch("/assets/kalman/pageviews.json");
  const { t, y, est } = await res.json();
  const W = 800, H = 240, pad = 20;
  const xmin = 0, xmax = t.length - 1;
  const ymin = Math.min(...y, ...est), ymax = Math.max(...y, ...est);
  const sx = x => pad + (x - xmin) / (xmax - xmin || 1) * (W - 2*pad);
  const sy = v => H - pad - (v - ymin) / (ymax - ymin || 1) * (H - 2*pad);
  const toPts = arr => arr.map((v,i)=>`${sx(i)},${sy(v)}`).join(" ");

  const svg = `
  <svg viewBox="0 0 ${W} ${H}" width="100%" height="auto" style="background:#fff;border:1px solid #eee">
    <polyline points="${toPts(y)}" fill="none" stroke="currentColor" stroke-opacity="0.35" stroke-width="1"/>
    <polyline points="${toPts(est)}" fill="none" stroke="currentColor" stroke-width="2"/>
  </svg>`;
  document.getElementById("kalman-chart").innerHTML = svg;
})();
</script>
```

---

## 关于Python代码段的说明

* 您的模型采用标准**恒定速度**状态`[位置, 速度]`，仅测量位置。您的`Q`矩阵符合恒定加速度驱动噪声形式。很好！
* 为保持数值稳定性，我将协方差更新改为**约瑟夫形式**，确保`P`保持半正定
* 对于博客场景，推荐使用`plt.savefig(...)`替代`plt.show()`，便于构建系统（本地或CI）在`assets/`目录生成成果物

---

## 其他有趣的博客创意

* 发布**鼠标轨迹演示**：展示原始光标轨迹与卡尔曼平滑轨迹的对比
* 分享**GPS行走路径**：上传经纬度CSV，经卡尔曼平滑后渲染为SVG路径
* **AB测试指标**：在绘图前对转化率去噪，避免读者对噪声过度反应
* **Rust/Python并行实现**：在`rust/`和`scripts/`中实现相同滤波器，对比输出结果（无需表格——只需叠加两张图表）

如果您需要，请告知希望首先平滑哪种数据集（页面访问量、错误计数等），我将为您定制CSV结构和`q/r`参数的默认值。
