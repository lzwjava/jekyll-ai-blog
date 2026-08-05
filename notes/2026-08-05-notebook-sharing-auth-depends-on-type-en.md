---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Notebook Sharing: Auth Depends on Type"
translated: false
type: note
---

Question: If you share a Jupyter notebook, do others get access without needing a password or SSH?

Answer: Depends on *what* you're sharing — "sharing a notebook" collapses two very different things.

**1. Sharing the `.ipynb` file (static)** — yes, zero auth needed

```bash
# just the file — JSON with cells + outputs baked in
cat notebook.ipynb | head -20
```

Anyone can open it in GitHub preview, `nbviewer`, VS Code, or `jupyter nbconvert --to html notebook.ipynb`. It's a snapshot. No kernel, no execution, no password. This is what most people mean by "sharing a notebook."

**2. Sharing a *live* server (interactive)** — auth still applies unless you explicitly strip it

Default Jupyter binds to localhost and requires a token:

```bash
jupyter notebook --no-browser
# http://localhost:8888/?token=abc123...
```

To let others hit it *without* SSH tunneling, you expose the port:

```bash
jupyter notebook --ip=0.0.0.0 --port=8888
```

But it still demands the token/password unless you nuke that too:

```bash
jupyter notebook --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
```

That last combo is what people usually mean by "no password needed" — and it's a genuinely bad idea on any network you don't fully trust, since anyone hitting that port gets an arbitrary code execution shell on your machine (it's literally a REPL over HTTP).

**3. Colab / Kaggle / hosted notebooks** — "share" button gives a link, auth is handled by their platform login (Google account etc.), not SSH. You're not exposing your own machine.

So: static file → no auth, correct. Live kernel → still needs *some* barrier (token, password, or platform login) unless you deliberately disable it, which trades convenience for "anyone on the network owns your box."

If you're doing this for remote GPU work, safer pattern than `--ip=0.0.0.0` + no-token is still SSH port forward:

```bash
ssh -L 8888:localhost:8888 user@remote-gpu-host
```

keeps the server bound to localhost on the remote side, token intact, and you tunnel instead of exposing the port publicly.

References:

- [Jupyter Notebook Security docs](https://jupyter-notebook.readthedocs.io/en/stable/security.html)
