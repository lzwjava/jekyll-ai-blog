---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kalman Filters for Clean Blog Data
translated: false
type: note
---

Nice repo! For a Jekyll-style blog like this, a Kalman filter is perfect for turning noisy time-series into clean visuals or interactive demos. Here are practical ways to use it—and a drop-in pipeline you can paste into your repo.

## What you can do with Kalman on your blog

* Smooth noisy **pageview stats** (daily visitors, bounce, session length) so readers see trends, not jitters.
* Denoise **build/test metrics** (e.g., warnings per day, errors in `conversion_errors.log`) before plotting.
* Clean **sensor-ish series** you might share—GPS paths, typing speed over time, scroll depth, etc.
* Publish **educational posts**: interactive demos that show how process/measurement noise change the estimate.

---

## Quick win: turn your Python into a static chart in the blog

If you just want a figure for a post, change the last line of your script from `plt.show()` to:

```python
plt.savefig("assets/kalman/toy.png", dpi=200, bbox_inches="tight")
```

Then embed in a post:

```markdown
![Kalman demo](/assets/kalman/toy.png)
```

---

## Turn-key pipeline: smooth any CSV series and publish PNG + JSON

### 1) Put your data here

Create `assets/data/pageviews.csv` with either `t,value` or `date,value`:

```
date,value
2025-07-01, 1023
2025-07-02, 980
2025-07-03, 1135
```

### 2) Add a reusable script

Create `scripts/kalman/smooth_series.py`:

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
    plt.plot(t, y, ".", label="Measurements")
    plt.plot(t, est, "-", linewidth=2, label="Kalman estimate")
    plt.xlabel("t")
    plt.ylabel("value")
    plt.title("Kalman smoothing (constant-velocity model)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="input CSV (t,value) or (date,value)")
    ap.add_argument("--out-prefix", required=True, help="e.g. assets/kalman/pageviews")
    ap.add_argument("--dt", type=float, default=1.0, help="time step between samples")
    ap.add_argument("--q", type=float, default=0.05, help="process variance (accel^2)")
    ap.add_argument("--r", type=float, default=4.0, help="measurement variance")
    args = ap.parse_args()

    t, y = read_csv_series(args.inp)
    est = smooth_series(t, y, dt=args.dt, q=args.q, r=args.r)

    out_png = f"{args.out_prefix}.png"
    out_json = f"{args.out_prefix}.json"
    plot_and_save(t, y, est, out_png)

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w") as f:
        json.dump({"t": t.tolist(), "y": y.tolist(), "est": est.tolist()}, f)
    print(f"Wrote {out_png} and {out_json}")

if __name__ == "__main__":
    main()
```

### 3) Add a Make target

In `Makefile`:

```make
kalman:
	python3 scripts/kalman/smooth_series.py --in assets/data/pageviews.csv \
		--out-prefix assets/kalman/pageviews --dt 1.0 --q 0.05 --r 4.0
```

Run:

```bash
make kalman
```

You’ll get:

* `assets/kalman/pageviews.png` – ready to embed
* `assets/kalman/pageviews.json` – for optional interactivity

### 4) Embed in a post (static)

Create `notes/2025-08-17-kalman-pageviews.md`:

```markdown
---
layout: post
title: Smoothing blog stats with a Kalman filter
---

Below: red dots are raw daily pageviews; blue line is the Kalman estimate.

![Pageviews (Kalman)](/assets/kalman/pageviews.png)
```

---

## Optional: a tiny client-side visual (no libraries)

Drop this snippet into the post after generating the JSON. It draws two polylines (raw vs. estimate) with plain SVG.

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

## Notes on your Python snippet

* Your model is the standard **constant-velocity** state `[position, velocity]` with measurement of position. Your `Q` matches the constant-acceleration driving noise form. Good!
* For numerical stability I switched the covariance update to the **Joseph form**, which keeps `P` positive semidefinite.
* For blogging, prefer `plt.savefig(...)` over `plt.show()` so your build (local or CI) produces artifacts in `assets/`.

---

## Other fun blog ideas

* Post a **mouse-tracking demo**: show a raw cursor trail vs. a Kalman-smoothed trail.
* Share a **GPS walk**: upload a CSV of lat/long, Kalman-smooth it, and render as an SVG path.
* **AB-test metrics**: denoise conversion rates before plotting so readers don’t overreact to noise.
* **Rust/Python side-by-side**: implement the same filter in `rust/` and `scripts/` and compare outputs (no table needed—just two overlaid plots).

If you want, tell me which dataset you’d like to smooth first (pageviews, error counts, etc.), and I’ll tailor the CSV schema and the `q/r` defaults for you.
