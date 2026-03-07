import sys
from Foundation import NSRunLoop, NSDate
from UserNotifications import (
    UNUserNotificationCenter,
    UNMutableNotificationContent,
    UNNotificationRequest,
    UNTimeIntervalNotificationTrigger,
    UNNotificationSound,
)

ALERT = 1 << 0
SOUND = 1 << 2


def request_authorization():
    center = UNUserNotificationCenter.currentNotificationCenter()
    state = {"done": False, "granted": False}

    def handler(granted, error):
        state["granted"] = bool(granted)
        state["done"] = True

    center.requestAuthorizationWithOptions_completionHandler_(ALERT | SOUND, handler)

    # Pump the runloop until the async auth callback fires
    while not state["done"]:
        NSRunLoop.currentRunLoop().runUntilDate_(
            NSDate.dateWithTimeIntervalSinceNow_(0.05)
        )

    return state["granted"]


def schedule_repeating_notification(title, body, seconds):
    if seconds < 60:
        raise ValueError(
            "macOS requires repeat interval >= 60 seconds for repeating triggers"
        )

    center = UNUserNotificationCenter.currentNotificationCenter()

    content = UNMutableNotificationContent.new()
    content.setTitle_(title)
    content.setBody_(body)
    # Optional sound (comment out if you prefer silent)
    content.setSound_(UNNotificationSound.defaultSound())

    trigger = UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(
        seconds, True
    )

    request = UNNotificationRequest.requestWithIdentifier_content_trigger_(
        "com.yourapp.reminder.clear-claude-code", content, trigger
    )

    def add_handler(error):
        if error is not None:
            print(f"[ERROR] Scheduling failed: {error}")
        else:
            print(f"[OK] Repeating notification scheduled every {seconds}s.")

    center.addNotificationRequest_withCompletionHandler_(request, add_handler)


def main():
    if not request_authorization():
        print(
            "Notifications not granted. Enable for Python in System Settings → Notifications."
        )
        sys.exit(1)

    schedule_repeating_notification("Reminder", "clear claude code context", 300)

    # Keep process alive so the system can deliver notifications
    print("Scheduled. Press Ctrl+C to exit.")
    try:
        while True:
            NSRunLoop.currentRunLoop().runUntilDate_(
                NSDate.dateWithTimeIntervalSinceNow_(1.0)
            )
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
