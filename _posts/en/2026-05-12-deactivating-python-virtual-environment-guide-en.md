---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deactivating Python Virtual Environment Guide
translated: false
type: note
---

Question: How do I deactivate a Python virtual environment and return to the default system Python?

Answer:

To exit/deactivate the virtual environment, simply run:

```bash
deactivate
```

After running `deactivate`, your prompt will change from `(venv) lzw@to:...` back to `lzw@to:...`, and you'll be using the system Python again.

---

**Verify you're back to system Python:**

```bash
which python3
python3 --version
```

---

**In your case**, since the venv was built with Python 3.13 (which isn't installed), after deactivating you can run your command using the available system Python explicitly:

```bash
PYTORCH_ALLOC_CONF=expandable_segments:True \
python3.11 -u train.py config/train_fineweb_gpt3.py 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

Or just `python3` if it points to 3.11 or 3.12 on your system.

---

**Optional — Recreate the venv with the correct Python version:**

If you want to fix the venv properly instead of using system Python directly:

```bash
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # reinstall dependencies
```
