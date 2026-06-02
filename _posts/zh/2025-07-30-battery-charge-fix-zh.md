---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 电池电量估算修复
translated: true
type: note
---

错误 `Cannot estimate time to full charge (sysfs files not found)` 表明脚本在 `/sys/class/power_supply/BAT0/` 目录中找不到预期的电池信息文件。这可能是因为：

1. 电池名称不是 `BAT0`（例如可能是 `BAT1` 或其他名称）。
2. 特定文件（`charge_now`、`charge_full`、`current_now`）在您的联想笔记本电脑上不可用或名称不同。
3. 运行脚本的用户缺少访问这些文件的权限。

以下是修复后的 Python 脚本，能够动态检测电池名称并处理 sysfs 文件名的变化（例如某些系统使用 `energy_now` 而非 `charge_now`）。该脚本还包含更好的错误处理和权限检查：

```python
import psutil
import os
import glob

def find_battery_path():
    """在 /sys/class/power_supply 中查找电池目录"""
    battery_paths = glob.glob('/sys/class/power_supply/BAT*')
    if not battery_paths:
        return None
    return battery_paths[0]  # 返回找到的第一个电池（例如 BAT0 或 BAT1）

def get_battery_info():
    try:
        # 使用 psutil 获取电池信息
        battery = psutil.sensors_battery()

        if battery is None:
            print("未检测到电池")
            return

        # 电池百分比
        percent = battery.percent
        print(f"电池电量：{percent:.2f}%")

        # 检查电池是否正在充电
        is_charging = battery.power_plugged
        status = "充电中" if is_charging else "放电中"
        print(f"状态：{status}")

        # 估算剩余时间（仅在放电时）
        if not is_charging and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            remaining_secs = battery.secsleft
            hours = remaining_secs // 3600
            minutes = (remaining_secs % 3600) // 60
            print(f"预计剩余时间：{hours} 小时 {minutes} 分钟")
        elif is_charging:
            # 尝试使用 sysfs 估算充满电所需时间
            battery_path = find_battery_path()
            if not battery_path:
                print("无法估算充满电时间（在 sysfs 中未找到电池）")
                return

            try:
                # 检查基于电荷量或能量的文件
                charge_now_file = os.path.join(battery_path, 'charge_now')
                energy_now_file = os.path.join(battery_path, 'energy_now')
                charge_full_file = os.path.join(battery_path, 'charge_full')
                energy_full_file = os.path.join(battery_path, 'charge_full_design')
                current_now_file = os.path.join(battery_path, 'current_now')

                # 确定要使用的文件类型（电荷量或能量）
                if os.path.exists(charge_now_file) and os.path.exists(charge_full_file):
                    now_file, full_file = charge_now_file, charge_full_file
                elif os.path.exists(energy_now_file) and os.path.exists(energy_full_file):
                    now_file, full_file = energy_now_file, energy_full_file
                else:
                    print("无法估算充满电时间（未找到电荷量/能量文件）")
                    return

                # 读取电池数据
                with open(now_file, 'r') as f:
                    charge_now = int(f.read().strip())
                with open(full_file, 'r') as f:
                    charge_full = int(f.read().strip())
                with open(current_now_file, 'r') as f:
                    current_now = int(f.read().strip())

                if current_now > 0:
                    charge_remaining = charge_full - charge_now
                    seconds_to_full = (charge_remaining / current_now) * 3600
                    hours = int(seconds_to_full // 3600)
                    minutes = int((seconds_to_full % 3600) // 60)
                    print(f"预计充满电时间：{hours} 小时 {minutes} 分钟")
                else:
                    print("无法估算充满电时间（current_now 为 0）")
            except PermissionError:
                print("无法估算充满电时间（权限被拒绝）。请尝试使用 sudo 运行")
            except FileNotFoundError:
                print(f"无法估算充满电时间（在 {battery_path} 中未找到 sysfs 文件）")
            except Exception as e:
                print(f"估算充满电时间时出错：{e}")
        else:
            print("无剩余时间估算可用")

    except Exception as e:
        print(f"获取电池信息时出错：{e}")

if __name__ == "__main__":
    get_battery_info()
```

### 所做更改

1. **动态电池检测**：
   - 使用 `glob.glob('/sys/class/power_supply/BAT*')` 查找电池目录（例如 `BAT0`、`BAT1`），而不是硬编码 `BAT0`
   - 返回找到的第一个电池，如果未检测到电池则返回 `None`

2. **支持电荷量和能量文件**：
   - 检查 `charge_now`/`charge_full` 和 `energy_now`/`energy_full` 文件，因为某些系统使用基于能量的指标（以瓦时为单位）而不是基于电荷量的指标（以微安时为单位）
   - 根据可用性选择适当的文件对

3. **改进的错误处理**：
   - 单独处理 `PermissionError`，建议在访问被拒时使用 `sudo` 运行
   - 如果未找到 sysfs 文件或 `current_now` 为零，提供具体反馈

4. **格式化输出**：
   - 将电池百分比限制为两位小数（`{percent:.2f}`）以获得更清晰的输出

### 使用方法

1. **安装 `psutil`（如果尚未安装）**：

   ```bash
   sudo pip3 install psutil
   ```

2. **保存脚本**：
   - 将更新后的脚本保存为 `battery_info.py`

3. **运行脚本**：
   - 在终端中执行：

     ```bash
     python3 battery_info.py
     ```

   - 如果出现"权限被拒绝"错误，请尝试使用提升的权限运行：

     ```bash
     sudo python3 battery_info.py
     ```

4. **检查电池路径**：
   - 要验证电池名称和可用文件，请运行：

     ```bash
     ls /sys/class/power_supply
     ```

     然后检查电池目录的内容（例如 `BAT0` 或 `BAT1`）：

     ```bash
     ls /sys/class/power_supply/BAT0
     ```

   - 查找类似 `charge_now`、`charge_full`、`energy_now`、`energy_full` 或 `current_now` 的文件。如果它们不同（例如使用 `energy_full_design` 而不是 `charge_full`），脚本应该能够处理，但如果您需要进一步调整，请告知我

### 调试提示

- 如果脚本仍然报告"未找到 sysfs 文件"，请检查 `/sys/class/power_supply/BAT*` 中的确切文件名。某些联想笔记本电脑可能使用非标准名称或 sysfs 支持有限
- 如果看到"权限被拒绝"，使用 `sudo` 运行应该可以解决，但请注意提升权限的风险
- 如果检测到电池但未提供时间估算，可能是因为 `current_now` 为零（当系统未主动报告充电电流时常见）。在这种情况下，脚本将回退到指示无估算可用

### 示例输出

在您的系统（联想小新-14-IAH8）上，您可能会看到：

```
电池电量：49.62%
状态：充电中
预计充满电时间：1 小时 45 分钟
```

或者，如果文件仍然缺失：

```
电池电量：49.62%
状态：充电中
无法估算充满电时间（在 /sys/class/power_supply/BAT0 中未找到 sysfs 文件）
```

### 如果问题仍然存在

如果脚本仍然无法找到 sysfs 文件，请分享以下命令的输出：

```bash
ls -l /sys/class/power_supply
ls -l /sys/class/power_supply/BAT*/*
```

这将有助于确定确切的文件名和权限。然后我可以进一步调整脚本以匹配您的系统配置。

[psutil 文档](https://psutil.readthedocs.io/en/latest/)
[Linux sysfs 电源供应](https://www.kernel.org/doc/html/latest/power/power_supply_class.html)
