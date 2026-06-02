---
audio: false
generated: true
lang: zh
layout: post
title: 在Android中使用EventBus
translated: true
type: note
---

我将解释如何在 Android 中使用 EventBus，这是一个流行的发布/订阅事件总线库，可简化 Activity、Fragment 和后台线程等组件之间的通信。

首先，将 EventBus 依赖项添加到项目中。在 `build.gradle`（应用模块）中包含：

```gradle
implementation 'org.greenrobot:eventbus:3.3.1'
```

以下是分步指南：

1. **定义事件类**
创建一个简单的 POJO 类来表示事件：

```java
public class MessageEvent {
    private String message;

    public MessageEvent(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
```

2. **注册订阅者**
在要接收事件的 Activity/Fragment 中：

```java
import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 注册到 EventBus
        EventBus.getDefault().register(this);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 取消注册以防止内存泄漏
        EventBus.getDefault().unregister(this);
    }

    // 订阅者方法
    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onMessageEvent(MessageEvent event) {
        // 处理事件
        Toast.makeText(this, event.getMessage(), Toast.LENGTH_SHORT).show();
    }
}
```

3. **发布事件**
从代码中的任何位置（另一个 Activity、Fragment、Service 等）：

```java
// 发布事件
EventBus.getDefault().post(new MessageEvent("来自 EventBus 的问候！"));
```

主要功能和选项：

- **线程模式选项**：
  - `ThreadMode.MAIN`：在 Android 主线程（UI 线程）上运行
  - `ThreadMode.BACKGROUND`：在后台线程上运行
  - `ThreadMode.ASYNC`：在单独的线程中执行
  - `ThreadMode.POSTING`：在与发布者相同的线程中运行

- **粘性事件**：
适用于需要为延迟订阅者保留的事件：

```java
// 发布粘性事件
EventBus.getDefault().postSticky(new MessageEvent("粘性消息"));

// 接收粘性事件
@Subscribe(sticky = true, threadMode = ThreadMode.MAIN)
public void onStickyEvent(MessageEvent event) {
    // 处理粘性事件
}
```

- **优先级**：
为订阅者设置优先级（数字越大优先级越高）：

```java
@Subscribe(threadMode = ThreadMode.MAIN, priority = 1)
public void onMessageEvent(MessageEvent event) {
    // 此订阅者具有更高优先级
}
```

最佳实践：
1. 始终在 `onDestroy()` 中取消注册以避免内存泄漏
2. 使用特定的事件类而非通用对象
3. 在订阅者方法中处理异常
4. 考虑使用粘性事件处理配置变更
5. 注意从后台线程向 UI 订阅者发布事件的情况

多组件简单示例：

```java
// 事件类
public class DataEvent {
    private int data;
    public DataEvent(int data) { this.data = data; }
    public int getData() { return data; }
}

// 发送者（例如 Fragment）
public class SenderFragment extends Fragment {
    private void sendData() {
        EventBus.getDefault().post(new DataEvent(42));
    }
}

// 接收者（例如 Activity）
public class ReceiverActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EventBus.getDefault().register(this);
    }

    @Override
    protected void onDestroy() {
        EventBus.getDefault().unregister(this);
        super.onDestroy();
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onDataEvent(DataEvent event) {
        textView.setText("已接收：" + event.getData());
    }
}
```

EventBus 特别适用于：
- 解耦组件
- Fragment 之间的通信
- 从后台操作更新 UI
- 处理配置变更

请务必正确处理生命周期并彻底测试事件流！
