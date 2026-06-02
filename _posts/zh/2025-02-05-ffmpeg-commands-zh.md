---
audio: true
generated: false
image: false
lang: zh
layout: post
title: FFmpeg 命令
translated: true
type: post
---

这里有一些我常用的ffmpeg命令。


```bash
ffmpeg -i IMG_4066.mov -vf "fps=10,scale=320:-1:flags=lanczos" output.gif

ffmpeg -i ml_1.mp4 -filter:v "crop=1600:900:0:90" -c:a copy -y ml_1_out.mp4

ffmpeg -i merge3.mp3 -i ml_1_cut.mp4 -filter_complex \
"[0:a][1:a]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[a]" \
-map 1:v -map "[a]" -c:v copy -c:a aac -shortest -y ml_1_out_m.mp4

ffmpeg -i nk.mp3 -filter:a "volume=0.1" -y nk_1.mp3

file="$1"

ffmpeg -loop 1 -i "${file}.jpg" -i "${file}.mp3" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest "$HOME/Downloads/${file}.mp4"

ffmpeg -i steve-jobs-lost-interview.mp3 -f segment -segment_time 420 -c copy steve%03d.mp3
```
