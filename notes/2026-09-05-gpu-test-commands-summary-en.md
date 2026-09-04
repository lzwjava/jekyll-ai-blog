---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Test Commands Summary
translated: false
type: note
---

I've read the PDF (`显卡测试命令手册.pdf`, 25 pages). Here is the **Section 6. Common Commands Summary** in English.

## 6. Common Commands Summary

### NVIDIA (N-card) Test Procedure

| Step | Description | Command / Action |
|------|-------------|-------------------|
| 1 | Power on, press **F8** to select **Legacy/Traditional mode** boot | — |
| 2 | Select the matching program for the GPU: **1/2/3** = mainly for N-cards, **4/5/6** = mainly for A-cards | — |
| 3 | The program auto-runs (pass or FAIL — ignore for now), then type | `LS` |
| 4 | View the test programs in the home directory (e.g. GT610 ~ GTX980i) | — |
| 5 | Enter a test version directory, e.g. 400.250 | `CD 400.250` |
| 6 | Run the test command | `./MATS –e 10` |
| 7 | If it runs, the GPU power supply is OK; if not, check GPU conditions or try another version | — |
| 8 | View test results (FBI0A0 = VRAM; no numbers after = OK, numbers = FAIL) | `nano report.txt` |
| 9 | Exit the editor | `Ctrl+X` or `Ctrl+Z` |
| 9' | Return to home directory | `CD ..` |
| 10 | Restart / Power off | `reboot` / `poweroff` |

### When the GPU has no display — use iGPU to test dGPU (Steps 11–30)

1. **Steps 11–14**: Plug external monitor into the motherboard. Press **Del** to enter BIOS (ASUS H170 PRO used as example) → press **F7** for Advanced → **Advanced** → **System Agent (SA) Configuration** → **Graphics Configuration** → set **Primary Display** to **CPU Graphics** (iGPU) or **PCIE** (dGPU) → **F10** to save and exit.
2. **Step 16**: Enter version 400.250 and run `./mats –e 10`
3. **Step 18**: **Set up the environment first** (mandatory when using iGPU to test dGPU):
   ```
   ./mods gputest.js -skip_rm_state_init -notest
   ```
4. **Step 19**: You must see a **PASS** screen before continuing; if not, the GPU has a hardware fault (power or core).
5. **Step 20**: Run the test in the background:
   ```
   ./mats -n 1 -e 5
   ```
6. **Step 21**: View results:
   ```
   less report.txt
   ```
   (FBI0A0 followed by all zeros = PASS; numbers = FAIL)
7. **Step 27 — N-card VRAM layout**:
   - Dual-sided card: side A = high bytes 32–63, side B = low bytes 0–31
   - Single-sided card: left (bottom) = high bytes 32–63, right (top) = low bytes 0–31
8. **Step 29 — Secondary verification** (confirm core vs VRAM fault):
   ```
   ./mods gputest.js -oqa -test 118 -matsinfo
   ```

### AMD (A-card) Test Key Commands

- Select **option 4** for RX580 and below. For 240: `./240` → view results `./240g`; channels `ChC/ChD/ChA/ChB/ChE/ChF/ChG` with no numbers = OK.
- For RX580: `./rx580a6` → view results `./rx580a6g`; `ChB1/ChA0/ChA1/ChC0/ChC1` showing `55555555` = channel fault.
- For RX5700: `CD rx57009` → `./tserver –boardtest=memfa` → view results `Pico memfa.log`.
- **A-card VRAM layout**: low bytes on the left (bottom) 0–31, high bytes on the right (top) 32–63.

> Note: Steps 3 and 9 each appear twice in the original manual (the duplicate "9" is actually the second occurrence and overlaps with step 8's layout).
