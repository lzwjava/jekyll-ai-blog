---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Warp的Windows路径空格问题
translated: true
type: note
---

这是一个Warp Windows验证问题——它不接受在shell命令字段中直接包含空格的路径。

**解决方法：使用引号括起路径或使用短路径形式**

按顺序尝试以下选项：

**选项1：带引号的路径**
```
"C:\Program Files\Git\bin\bash.exe" --login -i
```

**选项2：使用正斜杠（MSYS风格）**
```
C:/Program Files/Git/bin/bash.exe --login -i
```

**选项3：8.3短路径（始终有效）**
```
C:\PROGRA~1\Git\bin\bash.exe --login -i
```

先验证你的8.3路径——在PowerShell中运行以下命令：
```powershell
cmd /c "for %I in ("C:\Program Files\Git\bin\bash.exe") do echo %~sI"
```

**选项4：使用 `cmd /c` 作为包装**
```
cmd /c "C:\Program Files\Git\bin\bash.exe" --login -i
```

**选项5：指向 `git-cmd.exe` 填充程序**
```
C:\Program Files\Git\git-cmd.exe --command=usr/bin/bash.exe --login -i
```

---

另外值得注意：Warp在Windows上仍较新，且Git Bash支持尚不完善。如果以上方法均无效，实际的做法是**将WSL2设为默认配置文件**——零摩擦、完整Linux环境，且Warp的shell集成完美支持。
