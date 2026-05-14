---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bash Timeout for Long Commands
translated: false
type: note
---

Question: How can I instruct Claude to provide a shell command for me to run if a command takes longer than 1 minute, and how should I write that in the `CLAUDE.md` file?

Answer:

You can set up a timeout mechanism in Bash so that if a command takes longer than 1 minute, it will stop and print an alternative command for you to run manually. For example, you can use the `timeout` command in Linux:

```bash
# Run your command with a 1-minute timeout
timeout 60s python3.11 sample.py --init_from=gpt2-medium --start="Hello, my name is" --num_samples=3 --max_new_tokens=200

# Check the exit status
if [ $? -eq 124 ]; then
    echo "Command timed out. Run manually with:"
    echo "python3.11 sample.py --init_from=gpt2-medium --start=\"Hello, my name is\" --num_samples=3 --max_new_tokens=200"
fi
```

Explanation:

* `timeout 60s ...` runs the command for up to 60 seconds.
* If it exceeds 60 seconds, it exits with code `124`.
* The `if [ $? -eq 124 ]` block catches this and prints a command you can copy and run manually.

To document this in your `CLAUDE.md` file, you could add a section like this:

````markdown
### Handling Long-Running Commands

If a command is expected to take a long time, use `timeout` to limit its execution to 1 minute. If it times out, Claude will provide a shell command that you can run manually:

```bash
timeout 60s <your_command_here>
if [ $? -eq 124 ]; then
    echo "Command timed out. Run manually with:"
    echo "<your_command_here>"
fi
````

Replace `<your_command_here>` with the actual command you want to run.

```

This way, Claude’s guidance is explicitly documented, and you can safely run commands that might otherwise hang indefinitely.  

If you want, I can also :contentReference[oaicite:0]{index=0} so you don’t have to manually edit each one.  

Do you want me to do that?
```