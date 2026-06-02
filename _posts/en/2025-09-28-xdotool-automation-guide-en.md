---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-sonnet-4
title: xdotool Command Line Automation Guide
translated: false
type: note
---

## What is xdotool?

xdotool is a command-line automation tool for X11 (Linux desktop environments) that allows you to:

- Control mouse movements and clicks
- Send keystrokes to applications
- Manipulate windows (move, resize, focus)
- Search for windows by various criteria
- Automate desktop interactions programmatically

## Installation

```bash
# Ubuntu/Debian
sudo apt install xdotool

# Fedora/RHEL/CentOS
sudo dnf install xdotool

# Arch Linux
sudo pacman -S xdotool

# From source
git clone https://github.com/jordansissel/xdotool
cd xdotool
make
sudo make install
```

## Core Commands

### Window Information Commands

#### `getactivewindow`

Gets the window ID of the currently active/focused window.

```bash
xdotool getactivewindow
# Output: 52428807 (window ID)

# Get window title of active window
xdotool getactivewindow getwindowname
```

#### `getwindowfocus`

Similar to getactivewindow but may behave differently in some window managers.

```bash
xdotool getwindowfocus
```

#### `getwindowname`

Gets the title/name of a window.

```bash
# Get name of active window
xdotool getactivewindow getwindowname

# Get name of specific window ID
xdotool getwindowname 52428807
```

#### `getwindowpid`

Gets the process ID (PID) associated with a window.

```bash
xdotool getactivewindow getwindowpid
```

#### `getwindowgeometry`

Gets position and size information of a window.

```bash
xdotool getactivewindow getwindowgeometry
# Output: Window 52428807
#   Position: 100,50 (screen: 0)
#   Geometry: 800x600
```

#### `getdisplaygeometry`

Gets the screen/display dimensions.

```bash
xdotool getdisplaygeometry
# Output: 1920x1080
```

### Window Search and Selection

#### `search`

Search for windows by various criteria.

```bash
# Search by window name/title
xdotool search --name "Firefox"
xdotool search --name "Terminal"

# Search by class name
xdotool search --class "firefox"

# Search case-insensitive
xdotool search --name --onlyvisible --maxdepth 1 "terminal"

# Common search options:
# --name: search window titles
# --class: search window class names
# --classname: search window class instance names
# --onlyvisible: only visible windows
# --maxdepth N: limit search depth
# --limit N: limit number of results
# --desktop N: search specific desktop/workspace
```

#### `selectwindow`

Interactive window selection (click to select).

```bash
xdotool selectwindow
# Click on any window to get its ID
```

### Mouse Control

#### `click`

Simulate mouse clicks.

```bash
# Left click at current position
xdotool click 1

# Right click
xdotool click 3

# Middle click
xdotool click 2

# Double click
xdotool click --repeat 2 1

# Click at specific coordinates
xdotool mousemove 500 300 click 1

# Click with delay
xdotool click --delay 500 1
```

#### `getmouselocation`

Get current mouse cursor position.

```bash
xdotool getmouselocation
# Output: x:500 y:300 screen:0 window:52428807

# Get just coordinates
xdotool getmouselocation --shell
# Output: X=500 Y=300 SCREEN=0 WINDOW=52428807
```

#### Mouse Movement

```bash
# Move mouse to absolute position
xdotool mousemove 500 300

# Move mouse relative to current position
xdotool mousemove_relative 10 -20

# Move and click in one command
xdotool mousemove 500 300 click 1
```

### Keyboard Input

#### `key`

Send keystrokes to the active window.

```bash
# Send single key
xdotool key Return
xdotool key Escape
xdotool key Tab

# Send key combinations
xdotool key ctrl+c
xdotool key ctrl+alt+t
xdotool key shift+F10

# Send multiple keys in sequence
xdotool key ctrl+l type "https://google.com" key Return

# Common key names:
# - Letters: a, b, c, ... (lowercase)
# - Numbers: 1, 2, 3, ...
# - Special: Return, Escape, Tab, space, BackSpace, Delete
# - Function: F1, F2, ... F12
# - Modifiers: ctrl, alt, shift, super (Windows key)
# - Arrows: Up, Down, Left, Right
```

#### Text Input

```bash
# Type text (simulates typing each character)
xdotool type "Hello World"

# Type with delay between characters
xdotool type --delay 100 "Slow typing"

# Clear delay for fast typing
xdotool type --clearmodifiers --delay 0 "Fast text"
```

### Window Manipulation

```bash
# Focus/activate a window
xdotool windowactivate WINDOW_ID

# Minimize window
xdotool windowminimize WINDOW_ID

# Maximize window
xdotool windowmaximize WINDOW_ID

# Close window
xdotool windowclose WINDOW_ID

# Move window to position
xdotool windowmove WINDOW_ID 100 50

# Resize window
xdotool windowsize WINDOW_ID 800 600

# Move window to specific desktop
xdotool set_desktop_for_window WINDOW_ID 2

# Raise window to top
xdotool windowraise WINDOW_ID

# Map (show) window
xdotool windowmap WINDOW_ID

# Unmap (hide) window
xdotool windowunmap WINDOW_ID
```

### Advanced Features

#### `behave`

Set up window event behaviors (triggers).

```bash
# Execute command when window gains focus
xdotool behave WINDOW_ID focus exec echo "Window focused"

# Execute when window is created
xdotool behave WINDOW_ID create exec "notify-send 'New window'"

# Available events: focus, unfocus, mouse-enter, mouse-leave, create, destroy
```

#### `behave_screen_edge`

Trigger actions when mouse reaches screen edges.

```bash
# Execute command when mouse hits left edge
xdotool behave_screen_edge left exec "echo 'Left edge hit'"

# Available edges: left, right, top, bottom
```

## Practical Examples

### Basic Automation Scripts

#### Open Terminal and Run Command

```bash
#!/bin/bash
# Open terminal and run ls command
xdotool key ctrl+alt+t
sleep 1
xdotool type "ls -la"
xdotool key Return
```

#### Screenshot Active Window

```bash
#!/bin/bash
WINDOW=$(xdotool getactivewindow)
NAME=$(xdotool getwindowname $WINDOW | sed 's/[^a-zA-Z0-9]/_/g')
import -window $WINDOW "screenshot_${NAME}.png"
```

#### Focus Specific Application

```bash
#!/bin/bash
# Focus Firefox or open if not running
WINDOW=$(xdotool search --onlyvisible --class "firefox" | head -1)
if [ -n "$WINDOW" ]; then
    xdotool windowactivate $WINDOW
else
    firefox &
fi
```

### Window Management Scripts

#### Tile Windows Side by Side

```bash
#!/bin/bash
# Get screen geometry
eval $(xdotool getdisplaygeometry --shell)
HALF_WIDTH=$((WIDTH / 2))

# Get two most recent windows
WINDOWS=($(xdotool search --onlyvisible --maxdepth 1 "" | tail -2))

# Position first window on left
xdotool windowsize ${WINDOWS[0]} $HALF_WIDTH $HEIGHT
xdotool windowmove ${WINDOWS[0]} 0 0

# Position second window on right
xdotool windowsize ${WINDOWS[1]} $HALF_WIDTH $HEIGHT
xdotool windowmove ${WINDOWS[1]} $HALF_WIDTH 0
```

#### Center Active Window

```bash
#!/bin/bash
WINDOW=$(xdotool getactivewindow)
eval $(xdotool getdisplaygeometry --shell)
eval $(xdotool getwindowgeometry --shell $WINDOW)

NEW_X=$(((WIDTH - WINDOW_WIDTH) / 2))
NEW_Y=$(((HEIGHT - WINDOW_HEIGHT) / 2))

xdotool windowmove $WINDOW $NEW_X $NEW_Y
```

### Application-Specific Automation

#### Browser Automation

```bash
#!/bin/bash
# Open new tab and navigate
xdotool key ctrl+t
sleep 0.5
xdotool type "github.com"
xdotool key Return
```

#### Text Editor Automation

```bash
#!/bin/bash
# Select all and copy to clipboard
xdotool key ctrl+a
sleep 0.1
xdotool key ctrl+c
```

## Tips and Best Practices

### Timing and Delays

```bash
# Add delays for slow applications
xdotool key ctrl+alt+t
sleep 2  # Wait for terminal to open
xdotool type "echo hello"

# Use xdotool's built-in delays
xdotool key --delay 100 ctrl+alt+t
```

### Error Handling

```bash
#!/bin/bash
# Check if window exists before acting on it
WINDOW=$(xdotool search --name "MyApp" 2>/dev/null)
if [ -n "$WINDOW" ]; then
    xdotool windowactivate $WINDOW
else
    echo "Window not found"
    exit 1
fi
```

### Working with Multiple Windows

```bash
#!/bin/bash
# Act on all windows of a specific application
xdotool search --name "Firefox" | while read WINDOW; do
    xdotool windowactivate $WINDOW
    xdotool key F5  # Refresh
    sleep 0.5
done
```

### Debugging

```bash
# Enable verbose output
xdotool --verbose key Return

# Get detailed window information
xdotool search --name "Terminal" getwindowgeometry getwindowname getwindowpid
```

## Common Use Cases

1. **Window Management**: Focus, move, resize windows programmatically
2. **Application Testing**: Automate GUI testing scenarios
3. **Presentation Tools**: Automate slide navigation and window switching
4. **Gaming Macros**: Automate repetitive gaming tasks
5. **Accessibility**: Create custom input methods for users with disabilities
6. **System Administration**: Automate GUI-based admin tasks
7. **Development Tools**: Integrate with IDEs and development workflows

## Troubleshooting

### Common Issues

- **Commands not working**: Ensure X11 is running (not Wayland)
- **Permission issues**: Some operations may require appropriate user permissions
- **Window not found**: Use `xdotool search` to verify window exists and is visible
- **Timing issues**: Add appropriate delays between commands
- **Special characters**: Use proper escaping for special characters in text input

### Security Considerations

- xdotool can control any application, use with caution
- Avoid running untrusted xdotool scripts
- Be careful with automation that handles sensitive data
- Consider using `xdotool` in controlled environments only

This guide covers the essential and advanced features of xdotool. Experiment with these commands to create powerful desktop automation scripts tailored to your specific needs.
