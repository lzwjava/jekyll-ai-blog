---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 编程中重复的好处
translated: true
type: post
---

> export PATH=/opt/homebrew/opt/ruby/bin:/opt/homebrew/opt/openjdk/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:"$HOME/Library/Python/3.9/bin":/Library/TeX/texbin:/Users/lzwjava/bin:/Users/lzwjava/platform-tools:/Users/lzwjava/Downloads/google-cloud-sdk/bin

在这种情况下，避免使用变量：

`"$HOME/Library/Python/3.9/bin"`

> export PATH=/opt/homebrew/opt/ruby/bin:/opt/homebrew/opt/openjdk/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/lzwjava/Library/Python/3.9/bin:/Library/TeX/texbin:/Users/lzwjava/bin:/Users/lzwjava/platform-tools:/Users/lzwjava/Downloads/google-cloud-sdk/bin

第二个版本似乎有些重复，`/Users/lzwjava` 目录出现了多次，但它更简洁，也更容易阅读。

在编程中，重复实际上是有益的。我们并不总是需要通过变量或函数来抽象或简化一切。在这种情况下，`/Users/lzwjava` 这个家目录不太可能经常变化，所以重复它是完全可以接受的。

这就像我们提到人的名字一样：如果我们过多使用代词如“他”、“她”或“他们”，就会让人不清楚我们在说谁。名字本身不太可能改变，直接使用名字反而能增加清晰度。

抽象和简化很重要，但有时它们也会引入不必要的复杂性。有时，重复反而更简单、更容易理解。
