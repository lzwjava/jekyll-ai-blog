---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 暂时跳过并行测试
translated: true
type: note
---

摘要：在此场景下，顺序执行是正确的选择。你的1860个测试用例已能在约8秒内完成——在这个规模下，并行执行只会增加开销而无收益。并行模式下出现的“Bad file descriptor”错误表明某些测试涉及与进程分叉冲突的I/O操作，但所有测试仍能通过。如果将来加入更慢的测试（如API调用、模型加载），你可以切换到`-n auto`，因为xdist现在已在开发依赖中。
