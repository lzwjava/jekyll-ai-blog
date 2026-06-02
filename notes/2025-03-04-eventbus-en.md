---
audio: false
generated: true
lang: en
layout: post
title: Using EventBus in Android
translated: false
type: note
---

I'll explain how to use EventBus in Android, a popular publish/subscribe event bus library that simplifies communication between components like Activities, Fragments, and background threads.

First, add the EventBus dependency to your project. In your `build.gradle` (app module), include:

```gradle
implementation 'org.greenrobot:eventbus:3.3.1'
```

Here's a step-by-step guide:

1. **Define an Event Class**
Create a simple POJO class to represent your event:

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

2. **Register Subscriber**
In your Activity/Fragment where you want to receive events:

```java
import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Register to EventBus
        EventBus.getDefault().register(this);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Unregister to prevent memory leaks
        EventBus.getDefault().unregister(this);
    }

    // Subscriber method
    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onMessageEvent(MessageEvent event) {
        // Handle the event
        Toast.makeText(this, event.getMessage(), Toast.LENGTH_SHORT).show();
    }
}
```

3. **Post an Event**
From anywhere in your code (another Activity, Fragment, Service, etc.):

```java
// Post an event
EventBus.getDefault().post(new MessageEvent("Hello from EventBus!"));
```

Key Features and Options:

- **ThreadMode Options**:
  - `ThreadMode.MAIN`: Runs on Android's main thread (UI thread)
  - `ThreadMode.BACKGROUND`: Runs on a background thread
  - `ThreadMode.ASYNC`: Performs in a separate thread
  - `ThreadMode.POSTING`: Runs in the same thread as the poster

- **Sticky Events**:
For events that need to persist for late subscribers:

```java
// Posting a sticky event
EventBus.getDefault().postSticky(new MessageEvent("Sticky message"));

// Receiving sticky events
@Subscribe(sticky = true, threadMode = ThreadMode.MAIN)
public void onStickyEvent(MessageEvent event) {
    // Handle sticky event
}
```

- **Priority**:
Set priority for subscribers (higher number = higher priority):

```java
@Subscribe(threadMode = ThreadMode.MAIN, priority = 1)
public void onMessageEvent(MessageEvent event) {
    // This subscriber has higher priority
}
```

Best Practices:
1. Always unregister in `onDestroy()` to avoid memory leaks
2. Use specific event classes rather than generic objects
3. Handle exceptions in subscriber methods
4. Consider using sticky events for configuration changes
5. Be cautious with event posting from background threads to UI subscribers

Simple Example with Multiple Components:

```java
// Event Class
public class DataEvent {
    private int data;
    public DataEvent(int data) { this.data = data; }
    public int getData() { return data; }
}

// Sender (e.g., Fragment)
public class SenderFragment extends Fragment {
    private void sendData() {
        EventBus.getDefault().post(new DataEvent(42));
    }
}

// Receiver (e.g., Activity)
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
        textView.setText("Received: " + event.getData());
    }
}
```

EventBus is particularly useful for:
- Decoupling components
- Communicating between fragments
- Updating UI from background operations
- Handling configuration changes

Remember to handle the lifecycle properly and test your event flows thoroughly!
