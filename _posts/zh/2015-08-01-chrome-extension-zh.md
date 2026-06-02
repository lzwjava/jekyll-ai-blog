---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 构建一个Chrome扩展
translated: true
type: post
---

你是否曾经打开过太多浏览器标签页，并希望有一个工具来自动管理它们？在本博客文章中，我们将详细介绍如何创建一个名为“Tabs Killer”的Chrome扩展程序，它会在标签页数量超过用户定义的限制时自动关闭最旧的标签页。我将逐步分解代码，解释其工作原理，并提供见解，帮助你构建自己的Chrome扩展程序。

在本文结束时，你将了解Chrome扩展的结构、如何使用Chrome API以及如何创建一个带有设置的弹出界面。

---

## “Tabs Killer” 干什么？

“Tabs Killer”是一个Chrome扩展程序，它：
- 监控打开的标签页数量。
- 允许用户设置最大标签页限制。
- 当限制超过时，自动关闭最旧的标签页。
- 提供白名单功能，以保护特定标签页（例如基于URL模式）不被关闭。

该扩展程序包括一个用于配置设置的弹出界面和一个用于处理标签页管理的后台脚本。

---

## 项目结构

这是“Tabs Killer”扩展程序的文件结构：

```
tabs-killer/
├── manifest.json         # 扩展配置
├── popup.html            # 弹出界面
├── popup.js             # 弹出逻辑
├── background.html       # 后台页面
├── app.build.js          # 主应用逻辑（假设）
├── js/
│   ├── lib/              # 外部库（jQuery、Underscore、Bootstrap、RequireJS）
│   ├── tabmanager.js     # 标签页管理逻辑（假设）
│   └── settings.js       # 设置管理（假设）
├── css/
│   └── popup.css         # 弹出样式
└── img/
    ├── icon16.png        # 16x16 图标
    ├── icon48.png        # 48x48 图标
    └── icon128.png       # 128x128 图标
```

---

## 第1步：清单文件（`manifest.json`）

`manifest.json` 文件是任何Chrome扩展程序的核心。它定义了元数据、权限和关键组件。

```json
{
  "manifest_version": 2,
  "name": "Tabs Killer",
  "description": "当标签页过多时自动关闭最旧的标签页。",
  "version": "1.0",
  "browser_action": {
    "default_icon": "img/icon128.png",
    "default_popup": "popup.html"
  },
  "icons": {
    "128": "img/icon128.png",
    "48": "img/icon48.png",
    "16": "img/icon16.png"
  },
  "background": {
    "page": "background.html"
  },
  "permissions": [
    "tabs",
    "storage"
  ],
  "content_security_policy": "script-src 'self' 'unsafe-eval'; object-src 'self'"
}
```

### 说明：
- **`manifest_version`**：必须是 `2`（Chrome 已废弃版本 1）。
- **`name`、`description`、`version`**：基本元数据。
- **`browser_action`**：定义扩展的工具栏图标和弹出界面（`popup.html`）。
- **`icons`**：不同尺寸的图标（用于Chrome Web Store和工具栏）。
- **`background`**：指定一个持续运行的后台页面（`background.html`）。
- **`permissions`**：请求访问 `tabs` API（管理标签页）和 `storage` API（保存设置）。
- **`content_security_policy`**：允许 `unsafe-eval` 以用于 RequireJS 等库（在生产中谨慎使用）。

---

## 第2步：弹出界面（`popup.html`）

当用户点击扩展图标时，弹出界面会出现。它使用 Bootstrap 进行样式设置，并包括一个带有“选项”部分的选项卡界面。

```html
<!doctype html>
<html>
<head>
  <title>Tabs Killer 扩展的弹出界面</title>
  <link rel="stylesheet" href="js/lib/bootstrap/css/bootstrap.css" type="text/css"/>
  <link rel="stylesheet" href="css/popup.css"/>
  <script src="js/lib/jquery.min.js"></script>
  <script src="js/lib/underscore.js"></script>
  <script src="js/lib/bootstrap/js/bootstrap.min.js"></script>
  <script src="js/lib/bootstrap/js/bootstrap-tab.js"></script>
  <script src="js/lib/require.js"></script>
  <script src="app.build.js"></script>
  <script src="popup.js"></script>
</head>
<body>
  <ul class="nav nav-tabs">
    <li><a href="#tabOptions" target="#tabOptions" data-toggle="tab">选项</a></li>
  </ul>
  <div class="tab-content">
    <div class="tab-pane active" id="tabOptions">
      <form class="well">
        <fieldset>
          <legend>设置</legend>
          <p>
            <label for="maxTabs">保持的最大标签页数</label>
            <input type="text" id="maxTabs" class="span1" name="maxTabs"> 个标签页
          </p>
        </fieldset>
        <div id="status" class="alert alert-success invisible"></div>
        <fieldset>
          <legend>自动锁定</legend>
          <label for="white-list-input">包含字符串的标签页 URL：</label>
          <input type="text" id="white-list-input"/>
          <button class="btn-mini add-on" disabled id="white-list-add">添加</button>
          <table class="table table-bordered table-striped" id="white-list">
            <thead>
              <tr>
                <th>URL 模式</th>
                <th></th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </fieldset>
      </form>
    </div>
  </div>
  <script type="text/html" id="url-item-template">
    <tr>
      <td><%=url%></td>
      <td><a class="deleteLink" href="#">移除</a></td>
    </tr>
  </script>
</body>
</html>
```

### 说明：
- **库**：使用 jQuery、Underscore、Bootstrap 和 RequireJS 进行功能和样式设置。
- **UI 元素**：
  - 一个文本输入（`#maxTabs`）用于设置最大标签页数。
  - 一个白名单输入（`#white-list-input`）和“添加”按钮（`#white-list-add`）用于保护特定 URL。
  - 一个表格（`#white-list`）用于显示白名单模式，并带有“移除”链接。
  - 一个状态消息（`#status`）用于显示保存反馈。
- **模板**：一个 Underscore.js 模板（`#url-item-template`）动态生成表格行。

---

## 第3步：弹出逻辑（`popup.js`）

此脚本处理弹出界面的交互性，例如保存设置和管理白名单。

```javascript
require([], function () {
  var GlobalObject = chrome.extension.getBackgroundPage().GlobalObject;

  Popup = {};
  Popup.optionsTab = {};

  Popup.optionsTab.init = function (context) {
    function onBlurInput() {
      var key = this.id;
      Popup.optionsTab.saveOption(key, $(this).val());
    }
    $('#maxTabs').keyup(_.debounce(onBlurInput, 200));
    Popup.optionsTab.loadOptions();
  };

  Popup.optionsTab.loadOptions = function () {
    $('#maxTabs').val(GlobalObject.settings.get('maxTabs'));
    var whiteList = GlobalObject.settings.get('whiteList');
    Popup.optionsTab.buildWhiteListTable(whiteList);

    var $whiteListInput = $('#white-list-input');
    var $whiteListAdd = $('#white-list-add');

    var isValid = function (pattern) {
      return /\S/.test(pattern);
    };

    $whiteListInput.on('input', function () {
      if (isValid($whiteListInput.val())) {
        $whiteListAdd.removeAttr('disabled');
      } else {
        $whiteListAdd.attr('disabled', 'disabled');
      }
    });

    $whiteListAdd.click(function () {
      if (!isValid($whiteListInput.val())) return;
      whiteList.push($whiteListInput.val());
      $whiteListInput.val('').trigger('input').focus();
      Popup.optionsTab.saveOption('whiteList', whiteList);
      Popup.optionsTab.buildWhiteListTable(whiteList);
    });
  };

  Popup.optionsTab.saveOption = function (key, value, hideStatus) {
    if (!hideStatus) $('#status').html('');
    GlobalObject.settings.set(key, value);
    if (!hideStatus) {
      $('#status').removeClass('invisible').css('opacity', '100')
        .html('保存中...').delay(50).animate({opacity: 0});
    }
  };

  Popup.optionsTab.buildWhiteListTable = function (whiteList) {
    var urlItemTemplate = _.template($("#url-item-template").html());
    var $wlTable = $('table#white-list tbody');
    $wlTable.html('');
    for (var i = 0; i < whiteList.length; i++) {
      var $tr = $(urlItemTemplate({url: whiteList[i]}));
      var $deleteLink = $tr.find('a.deleteLink').parent();
      $deleteLink.click(function () {
        whiteList.splice(whiteList.indexOf($(this).data('pattern')), 1);
        Popup.optionsTab.saveOption('whiteList', whiteList, true);
        Popup.optionsTab.buildWhiteListTable(whiteList);
      }).data('pattern', whiteList[i]);
      $wlTable.append($tr);
    }
  };

  $(document).ready(function () {
    $('a[data-toggle="tab"]').on('show', function (e) {
      var tabId = e.target.hash;
      if (tabId === '#tabOptions') {
        Popup.optionsTab.init($('div#tabOptions'));
      }
    });
    $('a[href="#tabOptions"]').click();
  });
});
```

### 说明：
- **初始化**：连接到后台页面的 `GlobalObject` 以获取设置和标签页管理。
- **`init`**：设置事件监听器，例如对 `#maxTabs` 的防抖输入。
- **`loadOptions`**：加载保存的设置（最大标签页和白名单）并填充 UI。
- **`saveOption`**：将设置保存到 `GlobalObject.settings` 并显示“保存中...”动画。
- **`buildWhiteListTable`**：动态构建白名单表格，并带有删除功能。
- **事件监听器**：处理输入验证、添加白名单条目和选项卡切换。

---

## 第4步：后台逻辑（`background.html` 和假设脚本）

后台页面（`background.html`）持续运行并加载核心逻辑。

```javascript
// background.js（假设，基于提供的片段）
GlobalObject = {};

require(['tabmanager', 'settings'], function (tabmanager, settings) {
  var startup = function () {
    GlobalObject.settings = settings;
    GlobalObject.tabmanager = tabmanager;
    settings.init();
    tabmanager.init();
  };
  startup();
});
```

### 假设：
- **`settings.js`**：管理存储（例如 `chrome.storage`）以保存设置，如 `maxTabs` 和 `whiteList`。
- **`tabmanager.js`**：使用 `tabs` API 监控并根据 `maxTabs` 限制和 `whiteList` 关闭标签页。

假设的 `tabmanager.js` 示例：
```javascript
var tabmanager = {
  init: function () {
    chrome.tabs.onCreated.addListener(this.checkTabCount);
  },
  checkTabCount: function () {
    chrome.tabs.query({}, function (tabs) {
      var maxTabs = GlobalObject.settings.get('maxTabs') || 10;
      var whiteList = GlobalObject.settings.get('whiteList') || [];
      if (tabs.length > maxTabs) {
        var tabsToRemove = tabs.filter(tab => !whiteList.some(pattern => tab.url.includes(pattern)));
        chrome.tabs.remove(tabsToRemove[0].id); // 移除最旧的标签页
      }
    });
  }
};
```

---

## 如何测试扩展程序

1. 打开 Chrome 并转到 `chrome://extensions/`。
2. 启用“开发者模式”（右上角切换）。
3. 点击“加载已解压的扩展程序”并选择 `tabs-killer` 文件夹。
4. 点击扩展图标打开弹出界面并测试设置。

---

## 编写自己的 Chrome 扩展程序的技巧

1. **从小开始**：从一个简单的清单和一个弹出或后台脚本开始。
2. **使用 Chrome API**：根据需要利用 `chrome.tabs`、`chrome.storage` 等。
3. **调试**：使用 `console.log` 和 Chrome 的开发者工具（右键点击弹出界面 > 检查）。
4. **安全性**：在生产中避免使用 `unsafe-eval`；使用更严格的内容安全策略。
5. **UI 库**：Bootstrap 和 jQuery 简化了 UI 开发，但保持扩展程序轻量。

---

## 结论

“Tabs Killer” 展示了如何结合弹出界面、后台逻辑和 Chrome API 创建一个功能扩展程序。有了这个基础，你可以进一步自定义它——添加通知、改进标签页关闭逻辑或增强 UI。

欢迎实验代码并分享你自己的 Chrome 扩展程序想法！编码愉快！
