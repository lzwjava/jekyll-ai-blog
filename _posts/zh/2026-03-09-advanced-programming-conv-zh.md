---
audio: false
generated: true
image: false
lang: zh
layout: post
model: none
title: 高级编程 - 对话
translated: true
type: note
---

A: 嘿，我一直在准备广东的 08074 Advanced Computer Programming 考试。内容太多了——Python data types、OOP、algorithms、GUI、databases、networking。我们从哪里开始呢？

B: 好问题。我们从 data types 开始吧，因为它们是基础。在 Python 中，关键区别在于 mutable 和 immutable 类型。Lists 和 dicts 是 mutable 的，而 tuples 和 strings 不是——这会影响它们传递给函数时的行为。

A: 对，immutability 就是为什么 Python 中的 strings 可以安全地用作 dictionary keys。Tuples 也是。但我总是提醒学生：只是因为 tuple 是 immutable 的，并不意味着里面的对象也是——如果 tuple 包含一个 list，那个 list 仍然可以被 mutate。

B: 这是个经典陷阱。接下来是 control structures——考试喜欢测试 nested loops 和 loops 中的 `break`、`continue` 和 `else` 的使用。你知道吗？Python 的 loop `else` 只在 loop 没有被 break 退出时才运行？这让很多学生感到惊讶。

A: 是的！这是 Python 独特但强大的特性之一。它在 search loops 中超级有用——如果你找到项目，就 break；如果没找到，else block 就能干净地处理“未找到”情况，而不需要 flag variable。

B: 来说说 functions。考试经常测试 default arguments 和 *args/**kwargs。重要的是，default argument values 在定义时只被 evaluate 一次，而不是每次调用——所以使用 mutable default 如 list 是个著名的 bug，等着发生。

A: 没错。如果你写 `def add(item, lst=[])` 并多次调用，你就是在所有调用中共享同一个 list。修复方法是用 `None` 作为 default，并在 function body 内创建 list。这是考试中非常常见的陷阱。

B: 现在是 OOP——这是个大章节。Python 中的 encapsulation 通过约定实现，使用单下划线表示 protected，双下划线表示 name-mangled private attributes。语言不强制执行，但它向其他开发者传达意图。

A: 还有 inheritance——Python 支持 multiple inheritance，通过 MRO（Method Resolution Order）。Python 使用 C3 linearization algorithm 来决定哪个 parent class 的 method 先被调用，从左到右遍历 base classes。

B: Python 中的 polymorphism 实际上是 duck typing——如果一个对象有你需要的方法，它就能工作，不管它的 class 是什么。这就是为什么 lists 和 custom iterators 都能无缝地在 for loop 中工作。

A: Special methods 也被大量测试。`__init__` 是 constructor，`__str__` 用于 human-readable output，`__repr__` 用于 developer-facing representation，而 `__len__`、`__getitem__` 让 custom objects 像 sequences 一样行为。

B: 转向 algorithms 和 data structures。考试涵盖 list comprehensions、dictionary comprehensions 和 set operations。像 `[x**2 for x in range(10) if x % 2 == 0]` 这样的 comprehension 既简洁又高效——避免了重复 list.append 的开销。

A: Recursion 是另一个关键话题。经典例子是 factorial 和 Fibonacci，但考试可能问 recursive directory traversal 或 tree traversal。始终记住 Python 的 default recursion limit 是 1000——对于 deep recursion，你需要增加它或使用 iteration。

B: 对于 sorting，学生应该理解 Python 的内置 `sort()` 使用 Timsort——merge sort 和 insertion sort 的 hybrid，stable 且平均 O(n log n)。`key=` 参数让你按 custom criteria 排序，而不改变数据。

A: Binary search 也被测试——它需要一个 sorted list，并在每步 halve search space。bisect module 优雅地实现了它。学生应该理解为什么它是 O(log n)：每次 comparison 消除一半剩余 candidates。

B: Exception handling 至关重要。try-except-else-finally 结构很重要：`else` block 只在没有 exception 被 raised 时运行，而 `finally` 总是运行——即使 try block 中有 return。这让 finally 完美适合 cleanup，如关闭 files。

A: 你可以通过 subclassing Exception 来 raise custom exceptions。这是好的设计——让 callers 能单独 catch 你的 specific error type，而不是 generic errors。考试可能让你定义一个 custom exception 并用 meaningful message raise 它。

B: File I/O——安全的 pattern 是使用 `with open(filename) as f`，它是 context manager。它确保即使内部出错，file 也会正确关闭。用 `for line in f` 逐行读取对 large files 是 memory-efficient 的。

A: 对于 serialization，JSON 是 human-readable 和 cross-platform 的——用 `json.dumps()` 序列化，`json.loads()` 反序列化。Pickle 是 Python-specific 的，能序列化几乎任何 Python object，但不要 unpickle untrusted data。

B: `os` 和 `sys` modules 经常出现。`os.path.join` 以 platform-independent 方式构建 paths，`os.listdir` 列出 directory contents，`os.makedirs` 创建 nested directories。`sys.argv` 给出 command-line arguments，`sys.exit` 终止程序。

A: datetime module 也被测试。你用 `datetime.date(year, month, day)` 创建 date，两个 dates 相减给出 `timedelta` object。用 `strftime` 格式化，`strptime` 解析是考试喜欢的 practical skills。

B: 现在是 GUI，用 tkinter——核心概念是 event loop。你创建 widgets 如 `Label`、`Button`、`Entry`，用 pack 或 grid 放入 window，bind callbacks 到 events，然后调用 `mainloop()` 阻塞并处理 events，直到 window 关闭。

A: Geometry managers 很重要：`pack` 线性堆叠 widgets，`grid` 按 rows 和 columns 放置，`place` 用 absolute coordinates。对于考试，grid 对 forms 和 layouts 最灵活——你可以 span 多个 columns。

B: Database 用 SQLite3——用 `sqlite3.connect()` 连接，获取 cursor，execute SQL statements，commit changes。关键 workflow 是：connect, cursor, execute, commit, close。用 `?` placeholders 的 parameterized queries 防止 SQL injection。

A: 还有 fetching——`fetchone()` 返回一行，`fetchall()` 返回所有 rows 作为 tuples 的 list。用 `CREATE TABLE IF NOT EXISTS` 创建 tables 是好 practice，避免重复运行出错。这在 practical coding questions 中出现。

B: Network programming——socket module 是基础。你通过 bind socket 到 address 和 port 创建 TCP server，listen connections，然后在 loop 中 accept() 每个 client。Client connects，sends data，receives response。

A: `requests` library 简化 HTTP——`requests.get(url)` 获取 page，response 的 `.json()` 自动解析 JSON。对于考试，知道如何 handle response status codes 和 parse JSON responses 就够了。

B: Functional programming——lambda 创建 inline anonymous functions。`map(func, iterable)` 对每个 element 应用 function，`filter(func, iterable)` 只保留 function 返回 True 的 elements。这些是 explicit for loops 的干净替代。

A: Decorators 对很多学生来说优雅但 intimidating。一个 decorator 只是一个 function，它接受另一个 function 作为 input 并返回一个 new function。它 wrap original 来添加 behavior——如 logging 或 timing——而不修改 original code。

B: Generators 是 memory-efficient iterators。Generator function 用 `yield` 而非 `return`——每次 `next()` 调用从上次暂停处 resume execution。这适合处理 large datasets，而不一次性加载所有到 memory。

A: Context managers 通过 `__enter__` 和 `__exit__` 实现 `with` statements。你可以写自己的 context manager，让 setup 在 `__enter__` 中发生，teardown——如关闭 database connection——在 `__exit__` 中自动发生。

B: 对于 multithreading，`threading` module 让你 concurrently 运行 tasks。但 Python 的 GIL（Global Interpreter Lock）意味着一次只有一个 thread 执行 Python bytecode。Threading 适合 I/O-bound tasks，但不适合 CPU-bound computation。

A: 对于 CPU-bound work，`multiprocessing` 是答案——每个 process 有自己的 memory space 和 GIL，所以它们真正并行运行在 multiple cores 上。考试可能让你区分何时用 threading vs multiprocessing。

B: 总结一下，考试结构测试 theory——如解释 decorator 或 generator 做什么——和 practical coding。我的建议：为每个 concept 写实际 code，而不只是阅读。Hands-on practice 是 internalize 这些 patterns 的唯一方式。

A: 绝对同意。而且彻底 review standard library——os, sys, datetime, random, json, sqlite3, threading。这些几乎出现在每个 practical question 中。知道如何在单个程序中 combine 它们是 pass 和 high score 的区别。

A: 我们深入 decorators 吧，因为学生往往只 memorize syntax 而不懂 mechanics。本质上，decorator 用 wrapper 替换 function。当你在 function 上写 @my_decorator 时，Python 立即调用 my_decorator(original_func) 并将结果 bind 回同一个 name。

B: 对，这就是为什么 wrapper function 必须接受和 original 相同的 arguments——或用 *args 和 **kwargs 泛化。如果你忘了 return wrapper 的结果，decorated function 会 silently return None，这是 subtle 而 frustrating 的 bug。

A: 还有丢失 original function metadata 的问题。Decoration 后，func.__name__ 显示 wrapper 的 name，而不是 original。修复是用 @functools.wraps(func) 在你的 decorator 内——它将 original 的 name、docstring 和 signature 复制到 wrapper 上。

B: Stacking decorators 是另一个 exam topic。当你 stack @decorator_a 和 @decorator_b 时，Python bottom-up 应用它们——decorator_b 先 wrap，然后 decorator_a wrap 结果。但调用 function 时 execution order 是 top-down，所以 @decorator_a 的 wrapper 先运行。

A: 现在 generators——让我们精确地说 yield 如何内部工作。当调用 generator function 时，它根本不 execute。它返回一个 generator object。只有调用该 object 的 next() 时才开始 execution，并在每个 yield 暂停，preserving 整个 local state。

B: 这种 state preservation 让 generators 强大。Local variables、instruction pointer，甚至 call stack——在 yields 间都被 frozen。一个逐行读取 huge log file 的 generator 只用很少 memory，而不是将整个 file 加载到 list 中。

A: Generator expressions 也可测试——它们像 list comprehensions 但用 parentheses 而非 brackets。像 `(x**2 for x in range(1000))`。它们是 lazy 的：按需 compute 每个 value，不像 list comprehensions 预先 compute 所有并存储。

B: 你也可以用 send() method 向 generator 发送 values。Yielded expression 可以接收 sent value，让 generators 成为 two-way communication channels。这是 coroutines 的基础，不过对于这个考试，理解 basic yield behavior 是优先。

A: 让我们更精确地谈 iterators。一个 iterator 是任何有 __iter__ 和 __next__ methods 的 object。__iter__ 返回 self，__next__ 返回下一个 value 或 raise StopIteration。For loop 自动调用这些——对 iterable 调用 iter()，然后反复 next()。

B: 这就是为什么你能在 custom class 上 iterate——只需实现返回 self 的 __iter__ 和你的 logic 的 __next__。一旦 raise StopIteration，for loop 就干净退出。这比 index-based loops 对 custom data structures 如 linked lists 或 trees 更干净。

A: Context managers——学生应该能两种方式写一个：用有 __enter__ 和 __exit__ 的 class，和用 contextlib 的 @contextmanager decorator。Decorator 方法优雅：yield 前是 setup，yield 是 with block 的 body，yield 后是 teardown。

B: __exit__ method 接收三个 arguments：exc_type, exc_val, exc_tb——这些描述 with block 内发生的任何 exception。如果 __exit__ 返回 True，exception 被 suppressed。返回 None 或 False 让它 propagate。这给你 error handling 的 fine-grained control。

A: 现在深入 exam 的 multithreading。threading.Thread class 接受 target function 和 optional args。你调用 .start() 开始 execution，.join() 等待它完成。没有 join()，main program 可能在 threads 完成前 exit。

B: Race conditions 是主要 hazard。如果两个 threads 同时 modify shared variable，结果不可预测。修复是用 threading.Lock——一个 thread acquire lock，做工作，然后 release。另一个 thread 阻塞直到 lock 可用。

A: With statement 和 locks 配合完美——`with lock:` 在 entry 时 acquire，在 exit 时 release，即使内部有 exception。这比手动调用 lock.acquire() 和 lock.release() 安全得多，你可能在 error paths 中忘记 release。

B: 对于 multiprocessing module，interface 几乎和 threading 一样，但每个 Process 在自己的 Python interpreter 和 memory 中运行。Processes 间 sharing data 需要 explicit mechanisms 如 Queue 或 Pipe——不能像 threads 那样直接 share variable。

A: 让我们更深入 tkinter。StringVar、IntVar 和 DoubleVar 是特殊 variable types，当 value 变化时 auto-notify widgets。将 StringVar bind 到 Entry widget 的 textvariable option，读取 .get() 就能得到当前 input，而无需 manual event handling。

B: Message boxes 是 practical exam material——`messagebox.showinfo()`、`messagebox.showerror()` 和 `messagebox.askyesno()` 创建 popup dialogs。askyesno 变体返回 True 或 False，所以可用于 destructive operations 如删除 records 前确认。

A: Canvas widget 值得知道——它让你 programmatically 绘制 shapes、lines、text，甚至 images。你调用 `canvas.create_rectangle()`、`canvas.create_oval()` 等，用 coordinate arguments。它对 simple data visualization 或 exam coding questions 中的 game boards 很有用。

B: Tkinter 中的 event binding，用 bind() method 将 events map 到 callbacks。Event string format 重要：'<Button-1>' 是左键点击，'<KeyPress-Return>' 是 Enter 键，'<Motion>' 跟踪 mouse movement。Callback 接收 event object，包含 x, y coordinates 等。

A: 现在深入 SQLite3。Transactions 是关键——默认下，Python 中的 sqlite3 对 DDL 是 autocommit，但对 DML 如 INSERT、UPDATE、DELETE 需要 explicit commit()。忘记 commit 是学生在 coding questions 中最常见的错误。

B: 用 `with sqlite3.connect() as conn:` 将 connection 作为 context manager，能自动 handle commit 和 rollback——clean exit 时 commit，exception 时 rollback。这是 safest pattern，并在 exam answers 中显示对 transactions 的好理解。

A: Row objects vs tuples——默认，fetchall() 返回 tuples。但如果你设置 `conn.row_factory = sqlite3.Row`，你就得到支持 index 和 column-name access 的 Row objects。所以 `row['name']` 而非 `row[0]`——在 larger queries 中更 readable。

B: Sockets 的 network programming 中，TCP 和 UDP 的区别可测试。TCP 用 SOCK_STREAM——connection-oriented、reliable、ordered。UDP 用 SOCK_DGRAM——connectionless、更快，但无 delivery guarantee。大多数 exam questions 聚焦 TCP。

A: TCP server workflow 有 specific sequence：socket() 创建 socket，bind() 分配 address 和 port，listen() 进入 listening mode，然后 accept() 阻塞直到 client connects，返回特定 client 的 new socket 加 client 的 address。

B: Client 侧：socket() 创建，然后 connect() 向 server 的 address 和 port 发起 handshake。然后 send() 和 recv() 交换 data。Recv() argument 是 buffer size——通常 1024 或 4096 bytes。始终用 .decode('utf-8') 将 bytes decode 到 string。

A: 一个常见 exam question 是让你写 echo server——server 接收 message 并 unchanged 发送回去。它测试你是否理解完整的 socket lifecycle，包括 exchange 后关闭 client socket 和 done 时关闭 server socket。

B: Requests library 为 HTTP 抽象了所有这些。值得注意：始终在处理 body 前 check `response.status_code`。200 表示 success，404 表示 not found，500 表示 server error。Shortcut `response.raise_for_status()` 对任何 4xx 或 5xx code 抛 exception。

A: 让我们回顾 exception handling 的 edge cases。你可以用 tuple 在一个 except clause catch multiple exception types：`except (ValueError, TypeError) as e`。`as e` bind exception instance，所以你能 print `str(e)` 显示 error message。

B: Exception chaining 是 advanced 但可能出现——当你 catch 一个 exception 并 raise 另一个时，Python 自动 chain 它们。你也可以用 `raise NewException(...) from original_exception` explicitly set cause，它在 tracebacks 中清楚显示。

A: 对于 modules 和 packages，学生应该知道 package 只是有 __init__.py file 的 directory。当 import package 时，Python 运行 __init__.py。你可以在那里放 import statements，让 submodule contents 在 package level 可用——这就是为什么能 `from mypackage import MyClass` 而非 full path。

B: if __name__ == '__main__' guard 对 reusable modules 必不可少。当 file 直接运行时，__name__ 是 '__main__'。当被 import 时，__name__ 是 module 的 file name。Guard 防止 test code 或 demo 在被另一个 script import 时执行。

A: Random module 在 practical questions 中经常测试。`random.randint(a, b)` 返回包括两端点的 integer。`random.choice(seq)` 从 sequence 中挑一个 element。`random.shuffle(lst)` in-place shuffle list。`random.sample(population, k)` 返回 k 个 unique elements，不修改 original。

B: 对于 datetime module，计算两个 dates 间 difference 是 practical skill。两个 date objects 相减给出 timedelta，`.days` 给出天数。将 `timedelta(days=30)` 加到 date 给出 30 天后的 date——对 deadline calculations 很有用。

A: 更广义地说 comprehensions。Dictionary comprehension 如 `{k: v for k, v in items if v > 0}` 在一个 expression 中既 filter 又 transform。Set comprehension 用 curly braces 自动 deduplicate。这些不只是 syntactic sugar——往往比 equivalent loop code 更快。

B: Nested comprehensions 也值得注意。`[[0]*cols for _ in range(rows)]` 正确创建 2D matrix——每个 row 是 separate list。Naive `[[0]*cols]*rows` 看起来类似，但创建的 rows 都是 same object，所以 modify 一个 row 会 modify 所有。

A: 这是个很好的 exam trap。再加一个：shallow copy vs deep copy。`list2 = list1[:]` 或 `list(list1)` 创建 shallow copy——outer list 是 new，但 nested objects 仍 shared。`copy.deepcopy(list1)` recursively copy 一切，所以 nested lists 完全 independent。

B: 考试 prep 的最后冲刺——pickling。`pickle.dump(obj, file)` 序列化到 binary file，`pickle.load(file)` 反序列化。它能 handle 几乎任何 Python object，包括 custom class instances。但绝不要从 untrusted sources unpickle——deserialization 时可能 execute arbitrary code。

A: JSON serialization 更 safe 和 portable。唯一 limitation 是 JSON 只支持 basic types：strings, numbers, lists, dicts, booleans, None。如果你需要 serialize custom object，必须 subclass json.JSONEncoder 并 override default() method 写 custom encoder。

B: 好了，我给个 high-level exam strategy。彻底掌握 data types。能写一个有 inheritance 的 class，override __str__ 和至少一个 other special method。能 from scratch 写 generator、decorator 和 context manager，而不 lookup 任何东西。

A: 对于 practical coding sections：始终在 file 和 database operations 周围 handle exceptions，始终用 with-statements 关闭 resources，并 mentally test output——在写 final answer 前 line by line trace code。这些 habits 区分 good scores 和 great ones。

B: 最后一点——os.walk() function 极有用，常出现在 file system questions。它为 tree 中的每个 directory yield 三元组：dirpath, dirnames, filenames。你可以用 for loop over os.walk() 在三行 code 中 recurse 整个 folder structure。

A: 完美的结束语。考试奖励那些能读懂问题、识别 right module 和 pattern，并高效写 clean、correct code 的学生。Master standard library，理解 Python object model 如何真正工作，你会在 08074 上表现很好。大家好运。