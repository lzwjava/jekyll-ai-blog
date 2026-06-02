---
audio: false
generated: true
image: false
lang: en
layout: post
title: Battery Charge Estimation Fix
translated: false
type: note
---

The error `Cannot estimate time to full charge (sysfs files not found)` indicates that the script couldn't find the expected battery information files in `/sys/class/power_supply/BAT0/`. This can happen if:
1. The battery is named something other than `BAT0` (e.g., `BAT1` or another name).
2. The specific files (`charge_now`, `charge_full`, `current_now`) are not available or have different names on your Lenovo laptop.
3. The user running the script lacks permission to access these files.

Here's a fixed Python script that dynamically detects the battery name and handles variations in sysfs file names (e.g., `energy_now` instead of `charge_now` for some systems). It also includes better error handling and permission checks:

```python
import psutil
import os
import glob

def find_battery_path():
    """Find the battery directory in /sys/class/power_supply."""
    battery_paths = glob.glob('/sys/class/power_supply/BAT*')
    if not battery_paths:
        return None
    return battery_paths[0]  # Return the first battery found (e.g., BAT0 or BAT1)

def get_battery_info():
    try:
        # Get battery information using psutil
        battery = psutil.sensors_battery()

        if battery is None:
            print("No battery detected.")
            return

        # Battery percentage
        percent = battery.percent
        print(f"Battery Percentage: {percent:.2f}%")

        # Check if battery is charging
        is_charging = battery.power_plugged
        status = "Charging" if is_charging else "Discharging"
        print(f"Status: {status}")

        # Estimate remaining time (only when discharging)
        if not is_charging and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            remaining_secs = battery.secsleft
            hours = remaining_secs // 3600
            minutes = (remaining_secs % 3600) // 60
            print(f"Estimated Time Remaining: {hours} hours, {minutes} minutes")
        elif is_charging:
            # Try to estimate time to full charge using sysfs
            battery_path = find_battery_path()
            if not battery_path:
                print("Cannot estimate time to full charge (no battery found in sysfs).")
                return

            try:
                # Check for charge or energy-based files
                charge_now_file = os.path.join(battery_path, 'charge_now')
                energy_now_file = os.path.join(battery_path, 'energy_now')
                charge_full_file = os.path.join(battery_path, 'charge_full')
                energy_full_file = os.path.join(battery_path, 'charge_full_design')
                current_now_file = os.path.join(battery_path, 'current_now')

                # Determine which files to use (charge or energy)
                if os.path.exists(charge_now_file) and os.path.exists(charge_full_file):
                    now_file, full_file = charge_now_file, charge_full_file
                elif os.path.exists(energy_now_file) and os.path.exists(energy_full_file):
                    now_file, full_file = energy_now_file, energy_full_file
                else:
                    print("Cannot estimate time to full charge (charge/energy files not found).")
                    return

                # Read battery data
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
                    print(f"Estimated Time to Full Charge: {hours} hours, {minutes} minutes")
                else:
                    print("Cannot estimate time to full charge (current_now is 0).")
            except PermissionError:
                print("Cannot estimate time to full charge (permission denied). Try running with sudo.")
            except FileNotFoundError:
                print(f"Cannot estimate time to full charge (sysfs files not found in {battery_path}).")
            except Exception as e:
                print(f"Error estimating time to full charge: {e}")
        else:
            print("No remaining time estimate available.")

    except Exception as e:
        print(f"Error retrieving battery information: {e}")

if __name__ == "__main__":
    get_battery_info()
```

### Changes Made
1. **Dynamic Battery Detection**:
   - Uses `glob.glob('/sys/class/power_supply/BAT*')` to find the battery directory (e.g., `BAT0`, `BAT1`) instead of hardcoding `BAT0`.
   - Returns the first battery found or `None` if no battery is detected.

2. **Support for Charge and Energy Files**:
   - Checks for both `charge_now`/`charge_full` and `energy_now`/`energy_full` files, as some systems use energy-based metrics (in watt-hours) instead of charge-based (in microampere-hours).
   - Selects the appropriate pair of files based on availability.

3. **Improved Error Handling**:
   - Handles `PermissionError` separately to suggest running with `sudo` if access is denied.
   - Provides specific feedback if sysfs files are not found or if `current_now` is zero.

4. **Formatted Output**:
   - Limits battery percentage to two decimal places (`{percent:.2f}`) for cleaner output.

### How to Use
1. **Install `psutil` (if not already installed)**:
   ```bash
   sudo pip3 install psutil
   ```

2. **Save the Script**:
   - Save the updated script as, e.g., `battery_info.py`.

3. **Run the Script**:
   - Execute in a terminal:
     ```bash
     python3 battery_info.py
     ```
   - If you get a "permission denied" error, try running with elevated privileges:
     ```bash
     sudo python3 battery_info.py
     ```

4. **Check Battery Path**:
   - To verify the battery name and available files, run:
     ```bash
     ls /sys/class/power_supply
     ```
     Then, check the contents of the battery directory (e.g., `BAT0` or `BAT1`):
     ```bash
     ls /sys/class/power_supply/BAT0
     ```
   - Look for files like `charge_now`, `charge_full`, `energy_now`, `energy_full`, or `current_now`. If they differ (e.g., `energy_full_design` instead of `charge_full`), the script should handle it, but let me know if you need further tweaks.

### Debugging Tips
- If the script still reports "sysfs files not found," check the exact file names in `/sys/class/power_supply/BAT*`. Some Lenovo laptops may use non-standard names or have limited sysfs support.
- If you see "permission denied," running with `sudo` should resolve it, but be cautious with elevated privileges.
- If the battery is detected but no time estimate is provided, it could be due to `current_now` being zero (common when the system isn't actively reporting charging current). In this case, the script will fall back to indicating that no estimate is available.

### Example Output
On your system (Lenovo XiaoXin-14-IAH8), you might see something like:
```
Battery Percentage: 49.62%
Status: Charging
Estimated Time to Full Charge: 1 hours, 45 minutes
```
Or, if files are still missing:
```
Battery Percentage: 49.62%
Status: Charging
Cannot estimate time to full charge (sysfs files not found in /sys/class/power_supply/BAT0).
```

### If Issues Persist
If the script still fails to find the sysfs files, please share the output of:
```bash
ls -l /sys/class/power_supply
ls -l /sys/class/power_supply/BAT*/*
```
This will help identify the exact file names and permissions. I can then tailor the script further to match your system's configuration.

[psutil Documentation](https://psutil.readthedocs.io/en/latest/)
[Linux sysfs Power Supply](https://www.kernel.org/doc/html/latest/power/power_supply_class.html)
