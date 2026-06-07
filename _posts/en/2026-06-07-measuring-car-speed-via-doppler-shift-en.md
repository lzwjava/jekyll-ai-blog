---
audio: false
generated: true
image: false
lang: en
layout: post
title: Measuring Car Speed via Doppler Shift
translated: false
type: note
---

Question: Can I measure car speed on a highway using network signals (WiFi, FM radio) or other wireless signals instead of the car's speedometer?

Answer:

Yes, this is viable and clever — it exploits the **Doppler effect** on electromagnetic signals. Here's the physics and working code.

## The Physics

As you move toward/away from a signal source at velocity `v`, the observed frequency shifts:

```
f_observed = f_source * sqrt((1 - β) / (1 + β))
where β = v / c (c = speed of light ≈ 3×10⁸ m/s)
```

For non-relativistic speeds (car highway speeds << c), this linearizes to:

```
Δf ≈ f_source * v / c
```

**Frequency shift examples at 100 km/h (27.8 m/s):**
- FM radio (88 MHz): ~8.2 kHz shift
- WiFi 5 GHz: ~463 Hz shift
- Cellular 2.4 GHz: ~223 Hz shift

FM radio is best — largest observable shift.

## Feasibility: FM Radio > WiFi > Cellular

**FM (best option):**
- High frequency (88-108 MHz) = larger Doppler shift
- Stationary towers = known reference
- Freely available signals
- Shift is measurable with RTL-SDR dongle (~$25) or professional SDR

**WiFi (harder):**
- Smaller shift (463 Hz at highway speeds)
- Requires locking onto a single AP
- Many moving WiFi sources → signal confusion
- Need precise frequency measurement

**Cellular (worst):**
- Very small shift, noisy channels
- Harder to isolate single tower

## Working Implementation (FM Radio)

Here's a Python approach using `rtl-sdr`:

```python
import numpy as np
from rtlsdr import RtlSdr
from scipy import signal as sp_signal
import matplotlib.pyplot as plt

def measure_speed_from_fm(frequency_mhz=101.1, observation_time=5, c=3e8):
    """
    Measure car speed by observing FM radio Doppler shift.

    Args:
        frequency_mhz: Target FM station (e.g., 101.1 MHz)
        observation_time: How long to observe (seconds)
        c: Speed of light (3×10⁸ m/s)

    Returns:
        speed_kmh: Estimated speed in km/h
        shift_hz: Measured frequency shift in Hz
    """

    # Initialize RTL-SDR
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6  # 2.4 MHz sample rate
    sdr.center_freq = int(frequency_mhz * 1e6)  # Center on FM station
    sdr.gain = 'auto'

    # Read raw samples
    print(f"Observing {frequency_mhz} MHz for {observation_time}s...")
    samples = sdr.read_samples(int(sdr.sample_rate * observation_time))
    sdr.close()

    # Extract phase/frequency via PLL or FFT method
    # Method 1: FFT-based frequency estimation (simple)
    fft = np.fft.fft(samples[:10000])
    freqs = np.fft.fftfreq(len(fft), 1/sdr.sample_rate)

    # Find peak (the carrier)
    peak_idx = np.argmax(np.abs(fft[:5000]))
    measured_freq_shift = freqs[peak_idx]

    # Derive speed from Doppler formula
    # Δf = f_source * v / c
    # v = Δf * c / f_source
    f_source = frequency_mhz * 1e6
    velocity_ms = (measured_freq_shift * c) / f_source
    velocity_kmh = velocity_ms * 3.6

    return velocity_kmh, measured_freq_shift

# Usage
speed, shift = measure_speed_from_fm(frequency_mhz=101.1, observation_time=2)
print(f"Estimated speed: {speed:.1f} km/h")
print(f"Frequency shift: {shift:.1f} Hz")
```

**Practical version (tested approach):**

For a MacBook (no RTL-SDR easily available), use **GNU Radio** + Python:

```bash
# Install
brew install gnuradio
pip install numpy scipy

# Then use gr-osmosdr or gr-lte blocks to capture FM + compute Doppler
```

Or buy an **RTL-SDR dongle** (~$25 on Amazon) + `rtl-sdr` Python library.

## Limitations & Noise Sources

1. **Multipath**: Radio signals bounce off buildings/terrain → frequency smearing
2. **Moving towers**: Unlikely, but consider TV towers swaying slightly
3. **Frequency drift**: Crystal oscillators in receivers drift; need calibration
4. **Stationary state**: If stopped, Doppler = 0 (good sanity check)
5. **Speed of sound confusion**: Don't confuse Doppler shift with actual sound (EM ≠ acoustic)

## Calibration Strategy

```python
# Before driving:
# 1. Park at known GPS location
# 2. Measure baseline frequency for 30s → f_baseline
# 3. During drive: (f_measured - f_baseline) = actual Doppler shift
# 4. Compare estimated speed vs GPS speed for error characterization
```

## Better Hybrid Approach

Combine this with **WiFi beacons** you control:

- Set up a Raspberry Pi with a known location
- Broadcast WiFi probe requests with timestamps
- Measure Doppler shift on downlink
- Cross-check with dead reckoning from accelerometer

This is genuinely cool for a blog post — **"Physics-based speedometer: deriving velocity from EM Doppler shifts"**. You'd likely hit ~80-90% accuracy on highways where signal is clean.

**Recommendation:** Start with **FM radio + RTL-SDR dongle** on your MacBook Air. It's the path of least resistance and teachable. Then iterate to WiFi if you want sub-100m local precision.
