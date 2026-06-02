---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: RIG设置窗口控制器概述
translated: true
type: note
---

### 概述

这段 Objective-C 代码实现了 `RIGSettingWindowController` 类，用于管理 "Reveal-In-GitHub" (RIG) macOS 应用程序（可能是一个用于在 GitHub 仓库中快速定位选中代码的 Xcode 插件）的设置窗口。该窗口允许用户为不同的 GitHub 仓库配置自定义菜单项、键盘快捷键和正则表达式模式。它使用类似表格的视图（`RIGConfigCellsView`）来显示和编辑最多 10 个配置槽位（为保持 UI 一致性而填充了空配置）。

该类遵循 `NSTableViewDataSource` 和 `NSTableViewDelegate` 协议，表明它处理自定义单元格视图内表格视图的数据和事件。它与应用范围内的单例（如用于持久化的 `RIGSetting` 和用于 UI 反馈的 `RIGUtils`）集成。

主要职责：
- 加载和显示可配置项（例如菜单标题、快捷键、正则表达式模式）。
- 验证并保存更改。
- 提供用于保存、清除默认仓库设置和重置为默认值的按钮。

### 导入和定义

```objectivec
#import "RIGSettingWindowController.h"
#import "RIGConfigCellsView.h"
#import "RIGConfig.h"
#import "RIGPlugin.h"
#import "RIGUtils.h"
#import "RIGSetting.h"

#define kOutterXMargin 0
#define kOutterYMargin 0
```

- 导入语句引入了该类的头文件、用于渲染配置行的自定义视图（`RIGConfigCellsView`）、模型对象（用于单个设置的 `RIGConfig`，用于应用范围存储的 `RIGSetting`）和工具类（用于警报的 `RIGUtils`，可能用于插件生命周期的 `RIGPlugin`）。
- 定义设置了零边距，用于在窗口内全宽布局配置视图。

### 私有接口

```objectivec
@interface RIGSettingWindowController ()<NSTableViewDataSource, NSTableViewDelegate>

@property (nonatomic, strong) NSArray *configs;
@property (nonatomic, strong) RIGConfigCellsView *configCellsView;
@property (weak) IBOutlet NSView *mainView;
@property (weak) IBOutlet NSView *configsView;

@end
```

- 声明了一个私有扩展，用于内部属性和协议遵循。
- `configs`：包含用户设置的 `RIGConfig` 对象数组（例如菜单标题、最后按下的键、正则表达式模式）。
- `configCellsView`：将配置渲染为可编辑行的自定义视图（可能是可滚动表格或单元格堆栈）。
- `mainView` 和 `configsView`：指向 storyboard/nib 文件中容器视图的 IBOutlet；`configsView` 托管动态单元格。

### 实现

#### 初始化方法

```objectivec
- (void)awakeFromNib {
    [super awakeFromNib];
}

- (void)windowDidLoad {
    [super windowDidLoad];

    self.configs = [self displayConfigs];

    self.configCellsView = [[RIGConfigCellsView alloc] initWithFrame:CGRectMake(kOutterXMargin, kOutterYMargin, CGRectGetWidth(self.configsView.frame) - 2 * kOutterXMargin, [RIGConfigCellsView heightForConfigs:self.configs])];
    self.configCellsView.configs = self.configs;
    [self.configsView addSubview:self.configCellsView];
    [self.configCellsView reloadData];
}
```

- `awakeFromNib`：空的重写方法；当窗口从 nib（storyboard）加载时调用。仅调用父类实现。
- `windowDidLoad`：窗口完全加载后的核心设置。
  - 通过 `displayConfigs`（下文解释）加载 `configs`。
  - 创建一个 `configCellsView`，其框架在水平方向上填充 `configsView`（使用边距），在垂直方向上基于所有配置所需的总高度（由 `RIGConfigCellsView` 类方法计算）。
  - 将配置分配给视图，将其添加为子视图，并触发数据重新加载（可能刷新表格单元格）。

有一个被注释掉的 `updateConfigsViewHeight` 调用，表明曾考虑动态调整大小但被禁用——可能是因为单元格视图自动调整大小或窗口是固定的。

```objectivec
- (void)updateConfigsViewHeight {
    CGRect frame = self.configsView.frame;
    frame.size.height = CGRectGetHeight(self.configCellsView.frame);
    self.configsView.frame = frame;
}
```

- 用于将 `configsView` 调整为与单元格视图高度匹配的工具方法。当前未使用，但如果添加了更多配置，可以用于自动增长窗口。

#### 配置管理

```objectivec
- (NSMutableArray *)displayConfigs {
    NSMutableArray *configs = [NSMutableArray arrayWithArray:[RIGSetting setting].configs];
    while (configs.count < 10) {
        RIGConfig *config = [[RIGConfig alloc] init];
        config.menuTitle = @"";
        config.lastKey = @"";
        config.pattern = @"";
        [configs addObject:config];
    }
    return configs;
}
```

- 从应用的单例 `RIGSetting` 加载现有配置。
- 用空的 `RIGConfig` 实例将数组填充到恰好 10 个项目。这确保了 UI 的一致性（例如 10 个可编辑行），即使用户保存的配置较少。空的配置在保存时会被过滤掉。

```objectivec
- (void)reloadConfigs {
    self.configs = [self displayConfigs];
    self.configCellsView.configs = self.configs;
    [self.configCellsView reloadData];
}
```

- 从存储中刷新显示的配置并更新视图。在重置后使用。

```objectivec
- (BOOL)isValidConfigs:(NSArray *)configs {
    for (RIGConfig *config in configs) {
        if (![config isValid]) {
            return NO;
        }
    }
    return YES;
}
```

- 遍历配置并对每个配置调用 `isValid`（可能检查非空的 `menuTitle` 和 `pattern`）。仅当所有配置都有效或为空时才返回 `YES`（但请参阅下面的过滤）。

```objectivec
- (NSArray *)filteredConfigs {
    NSMutableArray *filtered = [NSMutableArray array];
    NSArray *configs = self.configCellsView.configs;
    for (RIGConfig *config in configs) {
        if (config.menuTitle.length > 0 || config.lastKey.length > 0 || config.pattern.length > 0) {
            [filtered addObject:config];
        }
    }
    return filtered;
}
```

- 将 10 槽数组过滤为仅包含非空配置（基于任何字段有内容）。在验证/保存之前，这会去除空白项，因此 `isValidConfigs` 仅检查真实条目。

#### 动作处理程序 (IBAction)

这些通过 Interface Builder 连接到 UI 中的按钮。

```objectivec
- (IBAction)saveButtonClcked:(id)sender {
    NSArray *configs = [self filteredConfigs];
    if (![self isValidConfigs:configs]) {
        [RIGUtils showMessage:@"Please complete the config, should at least have menuTitle and pattern."];
        return;
    }
    [RIGSetting setting].configs = self.configCellsView.configs;
    [RIGUtils showMessage:@"Save succeed. Will Take effect when reopen Xcode."];
}
```

- **保存按钮**：过滤配置，验证它们（如果无效则显示错误警报），然后将完整（填充后）的数组保存回 `RIGSetting`。注意：它保存完整的 10 个槽位，但空白项在加载/过滤时会被忽略。显示成功消息，提示需要重启 Xcode（插件重新加载）。

方法名中的拼写错误："Clcked" 应为 "Clicked"。

```objectivec
- (IBAction)clearButtonClicked:(id)sender {
    RIGSetting *setting = [RIGSetting settingForGitPath:self.gitRepo.localPath];
    NSString *defaultRepo = setting.defaultRepo;
    if (defaultRepo == nil) {
        [RIGUtils showMessage:@"There's no default repo setting."];
    } else {
        setting.defaultRepo = nil;
        [RIGUtils showMessage:[NSString stringWithFormat:@"Succeed to clear current default repo(%@) setting. In the next time to open github, will ask you to select new default repo.", defaultRepo]];
    }
}
```

- **清除按钮**：通过 `settingForGitPath` 定位特定于项目的设置（假设 `self.gitRepo` 可用，可能在其他地方设置）。清除 `defaultRepo`（例如回退的 GitHub URL）。如果未设置则发出警报，或确认清除并附带详细信息。

注意：`self.gitRepo` 未在此处声明——可能是来自超类或类别的属性。

```objectivec
- (IBAction)resetMenusButtonClicked:(id)sender {
    [[RIGSetting setting] setConfigs:[RIGSetting defaultConfigs]];
    [self reloadConfigs];
}
```

- **重置按钮**：用应用默认配置（来自 `RIGSetting`）覆盖配置，然后重新加载 UI。没有确认对话框——直接执行操作。

### 潜在改进/注意事项

- **UI 流程**：窗口是非模态的（此处没有显式的显示调用），因此可能通过 `[controller showWindow:sender]` 呈现。由于插件性质，更改需要重启 Xcode。
- **验证**：依赖于 `RIGConfig.isValid`，此处未显示——可能确保必填字段（如标题和模式）非空。
- **边界情况**：填充到 10 个假设了固定的 UI；动态调整大小可以使用被注释的 `updateConfigsViewHeight`。重置/清除没有撤销/确认。
- **依赖关系**：与应用程序模型（`RIGConfig`、`RIGSetting`）紧密耦合——完全理解需要这些头文件。

此代码来自 2015 年，因此使用了较旧的 Cocoa 模式（例如，手动设置框架而非自动布局）。对于现代的 SwiftUI，它将是一个带有 `@State` 用于配置的 `View`。
