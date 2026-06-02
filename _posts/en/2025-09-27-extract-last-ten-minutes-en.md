---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Extracting last ten audio minutes
translated: false
type: note
---

To get the last 10 minutes of the audio file `lobby-zh.ogg`, you need to use the following information:

1.  **Total Duration:** The input file duration is `00:33:34.40`.
2.  **Desired Segment Length:** 10 minutes (or 600 seconds).
3.  **Start Time Calculation:** You need to calculate the point 10 minutes *before* the end of the file.

### Calculation

*   Total duration in seconds:
    $$(33 \times 60) + 34.40 = 1980 + 34.40 = 2014.40 \text{ seconds}$$
*   Start time:
    $$2014.40 \text{ seconds} - 600 \text{ seconds} = 1414.40 \text{ seconds}$$

In `HH:MM:SS.sss` format:
$$1414.40 \text{ seconds} = 23 \text{ minutes and } 34.40 \text{ seconds} \quad (1414.40 / 60 = 23.5733\dots)$$
$$\text{Start Time} = 00:23:34.40$$

### FFmpeg Command

You will use the `-ss` (seek to position) input option combined with the `-t` (duration) option.

1.  `-ss 00:23:34.40`: Sets the starting position for the extraction.
2.  `-t 00:10:00`: Sets the duration of the output segment to exactly 10 minutes.

```bash
ffmpeg -i lobby-zh.ogg -ss 00:23:34.40 -t 00:10:00 last_10_minutes.ogg
```

**Note:** If you want to use the output file's original bitrate/codec settings, you can add `-c copy` for faster processing:

```bash
ffmpeg -i lobby-zh.ogg -ss 00:23:34.40 -t 00:10:00 -c copy last_10_minutes_copy.ogg
```
