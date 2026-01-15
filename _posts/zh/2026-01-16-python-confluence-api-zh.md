---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Python API 创建 Confluence 页面
translated: true
type: note
---

**Question:** 如何使用 Atlassian Python package 通过其 API 创建 Confluence 页面？

**Answer:**

用于与 Confluence（以及其他 Atlassian 产品）交互最流行且持续维护的 Python library 是 **atlassian-python-api**。

### Installation

```bash
pip install atlassian-python-api
```

### Basic Usage to Create a Page

#### 1. 针对 Confluence **Server / Data Center**
使用 username + password（或在较新版本中使用 personal access token）。

```python
from atlassian import Confluence

confluence = Confluence(
    url='https://your-confluence-server.com',          # 或 http://localhost:8090
    username='your-username',
    password='your-password-or-pat'
)

# 在 space 中创建一个一级页面
status = confluence.create_page(
    space='YOUR_SPACE_KEY',           # 例如 'DEV' 或 'DOC'
    title='My New Page Title',
    body='<h1>Hello World</h1><p>This page was created via Python.</p>',
    parent_id=None,                   # None = 一级页面
    type='page',
    representation='storage'          # 'storage' = 基于 XHTML 的编辑器格式
)

print(status)  # 成功后返回包含已创建页面信息的 dict
```

#### 2. 针对 Confluence **Cloud**
使用您的 **email** + **API token**（推荐）。

在以下地址生成 token：https://id.atlassian.com/manage-profile/security/api-tokens

```python
from atlassian import Confluence

confluence = Confluence(
    url='https://your-site.atlassian.net',
    username='your.email@company.com',   # 必须是您的 Atlassian 账号 email
    password='YOUR_API_TOKEN',           # API token，不是账号密码
    cloud=True                           # 对 Cloud 版很重要（某些版本需要此参数）
)

# create_page 调用方式同上
new_page = confluence.create_page(
    space='SPACEKEY',
    title='API Created Page 2026',
    body='<ac:structured-macro ac:name="info"><ac:rich-text-body><p>Created with atlassian-python-api</p></ac:rich-text-body></ac:structured-macro>',
    representation='storage'
)

print(new_page['id'])         # 新页面的 ID
print(new_page['_links']['webui'])  # 访问该页面的相对链接
```

#### 3. 创建子页面 (child / sub-page)
```python
parent_page_id = '123456789'   # 通过 confluence.get_page_id(space, title) 或手动获取

confluence.create_page(
    space='DOC',
    title='Child Page',
    body='Content here...',
    parent_id=parent_page_id,
    representation='storage'
)
```

#### 4. 其他有用的 create_page 参数
- `type`: `'page'` (默认) 或 `'blogpost'`
- `representation`: `'storage'` (XHTML, 推荐), `'wiki'` (Confluence wiki markup), `'atlas_doc_format'` (ADF – 较新的 Cloud 格式)
- `editor`: `'v2'` (近期版本中的默认值)
- `full_width`: `True` / `False` (宽页面布局)
- `minor_edit`: `True` (更新时使用 – 不会通知关注者)

#### 5. 推荐的现代 Cloud 方法（使用较新的拆分类）
```python
from atlassian.confluence import ConfluenceCloud

confluence = ConfluenceCloud(
    url='https://your-domain.atlassian.net',
    token='YOUR_API_TOKEN'          # 仅需 Token – 此处无需 username
)

confluence.create_page(
    space='SPACE',
    title='Modern Cloud Example',
    body='<p>Using ConfluenceCloud class</p>',
    representation='storage'
)
```

### Troubleshooting Tips
- **401 Unauthorized** → Token/Email 错误或在该 Space 中没有 "Add Pages" 权限。
- **403 Forbidden** → 缺少 Space 权限或该 Space 受到限制。
- **Body format issues** → 对于 HTML/XHTML，请使用 `'storage'` representation。对于含有大量 macro 的页面，建议从现有页面复制 HTML（通过 ?expand=body.storage 获取）。
- 始终检查返回的 dict – 它包含 `'id'`、`'title'`、`'_links'` 等关键信息。

更多示例：https://github.com/atlassian-api/atlassian-python-api/tree/master/examples/confluence

完整文档：https://atlassian-python-api.readthedocs.io/confluence.html

**References:**

- [https://atlassian-python-api.readthedocs.io/confluence.html](https://atlassian-python-api.readthedocs.io/confluence.html)
- [https://github.com/atlassian-api/atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api)
- [https://pypi.org/project/atlassian-python-api/](https://pypi.org/project/atlassian-python-api/)