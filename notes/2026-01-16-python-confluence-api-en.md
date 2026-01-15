---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Create Confluence Pages Using Python API
translated: false
type: note
---

**Question:** How to use the Atlassian Python package to create a Confluence page using its API?

**Answer:**

The most popular and maintained Python library for interacting with Confluence (and other Atlassian products) is **atlassian-python-api**.

### Installation
```bash
pip install atlassian-python-api
```

### Basic Usage to Create a Page

#### 1. For Confluence **Server / Data Center**
Use username + password (or personal access token in newer versions).

```python
from atlassian import Confluence

confluence = Confluence(
    url='https://your-confluence-server.com',          # or http://localhost:8090
    username='your-username',
    password='your-password-or-pat'
)

# Create a top-level page in a space
status = confluence.create_page(
    space='YOUR_SPACE_KEY',           # e.g. 'DEV' or 'DOC'
    title='My New Page Title',
    body='<h1>Hello World</h1><p>This page was created via Python.</p>',
    parent_id=None,                   # None = top-level page
    type='page',
    representation='storage'          # 'storage' = XHTML-based editor format
)

print(status)  # Returns dict with the created page info if successful
```

#### 2. For Confluence **Cloud**
Use your **email** + **API token** (recommended).

Generate token at: https://id.atlassian.com/manage-profile/security/api-tokens

```python
from atlassian import Confluence

confluence = Confluence(
    url='https://your-site.atlassian.net',
    username='your.email@company.com',   # Must be your Atlassian account email
    password='YOUR_API_TOKEN',           # API token, NOT account password
    cloud=True                           # Important for Cloud (some versions need it)
)

# Same create_page call as above
new_page = confluence.create_page(
    space='SPACEKEY',
    title='API Created Page 2026',
    body='<ac:structured-macro ac:name="info"><ac:rich-text-body><p>Created with atlassian-python-api</p></ac:rich-text-body></ac:structured-macro>',
    representation='storage'
)

print(new_page['id'])         # The new page ID
print(new_page['_links']['webui'])  # Relative link to view the page
```

#### 3. Create a child / sub-page (most common real use case)
```python
parent_page_id = '123456789'   # Get this from confluence.get_page_id(space, title) or manually

confluence.create_page(
    space='DOC',
    title='Child Page',
    body='Content here...',
    parent_id=parent_page_id,
    representation='storage'
)
```

#### 4. Other useful create_page parameters
- `type`: `'page'` (default) or `'blogpost'`
- `representation`: `'storage'` (XHTML, recommended), `'wiki'` (Confluence wiki markup), `'atlas_doc_format'` (ADF – newer Cloud format)
- `editor`: `'v2'` (default in recent versions)
- `full_width`: `True` / `False` (wide page layout)
- `minor_edit`: `True` (when updating – doesn't notify watchers)

#### 5. Recommended modern Cloud approach (using newer split classes)
```python
from atlassian.confluence import ConfluenceCloud

confluence = ConfluenceCloud(
    url='https://your-domain.atlassian.net',
    token='YOUR_API_TOKEN'          # Token only – no username needed here
)

confluence.create_page(
    space='SPACE',
    title='Modern Cloud Example',
    body='<p>Using ConfluenceCloud class</p>',
    representation='storage'
)
```

### Troubleshooting Tips
- **401 Unauthorized** → Wrong token/email or insufficient "Add Pages" permission in the space.
- **403 Forbidden** → Missing space permissions or restricted space.
- **Body format issues** → Use `'storage'` representation for HTML/XHTML. For macro-heavy pages, copy HTML from an existing page (via ?expand=body.storage).
- Always check the returned dict – it contains `'id'`, `'title'`, `'_links'`, etc.

More examples: https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/confluence

Full documentation: https://atlassian-python-api.readthedocs.io/confluence.html

**References:**

- [https://atlassian-python-api.readthedocs.io/confluence.html](https://atlassian-python-api.readthedocs.io/confluence.html)
- [https://github.com/atlassian-api/atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api)
- [https://pypi.org/project/atlassian-python-api/](https://pypi.org/project/atlassian-python-api/)