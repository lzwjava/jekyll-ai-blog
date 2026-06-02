---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 轻聊 iOS
translated: true
type: post
---

这是从 github 项目 [https://github.com/lzwjava/leanchat-ios](https://github.com/lzwjava/leanchat-ios) 的 README.md。

---

![许可证 MIT](https://img.shields.io/badge/license-MIT-green.svg?style=flat)&nbsp;
[![CocoaPods](http://img.shields.io/cocoapods/v/LeanChatLib.svg?style=flat)](http://cocoapods.org/?q=LeanChatLib)&nbsp;
[![CocoaPods](http://img.shields.io/cocoapods/p/LeanChatLib.svg?style=flat)](http://cocoapods.org/?q=LeanChatLib)&nbsp;
[![支持](https://img.shields.io/badge/support-iOS%207%2B%20-blue.svg?style=flat)](https://www.apple.com/nl/ios/)

![leanchat](https://cloud.githubusercontent.com/assets/5022872/8431636/4eff0aca-1f6d-11e5-8728-f8f450dac380.gif)

## 应用商店
LeanChat 可在应用商店获得。您可以访问 [https://itunes.apple.com/gb/app/leanchat/id943324553](https://itunes.apple.com/gb/app/leanchat/id943324553) 或在应用商店中搜索 LeanChat。

## 引言
该示例项目全面展示了 LeanCloud 的实时通信功能的应用。然而，它包含大量的 UI 代码和其他功能，不适合快速学习。如果您是 LeanMessage 的新手，我们推荐 [LeanMessage-Demo](https://github.com/leancloud/LeanMessage-Demo) 项目。熟悉后，您可以访问 [LeanCloud-Demos](https://github.com/leancloud/leancloud-demos) 选择您喜欢的 IM 外观进行集成。在集成过程中，如果遇到困难，可以参考 LeanChat 项目。

## LeanChat 项目结构

* [leanchat-android](https://github.com/leancloud/leanchat-android): Android 客户端
* [leanchat-ios](https://github.com/leancloud/leanchat-ios): iOS 客户端
* [leanchat-webapp](https://github.com/leancloud/leanchat-webapp): Web 客户端
* [leanchat-cloud-code](https://github.com/leancloud/leanchat-cloudcode): 服务器端

## 有价值的反馈

如果有任何问题，请随时提交一个 [issue](https://github.com/leancloud/leanchat-ios/issues)，说明您不理解的内容，我们会尽快提供帮助。

## 下载
请直接点击 Github 上显示的 `Download Zip` 图标下载最新版本。如果使用 `git clone`，可能会非常慢，因为它包含了大量的提交历史。在测试中，差异为：1.5M:40M。

![qq20150618-2 2x](https://cloud.githubusercontent.com/assets/5022872/8223520/4c25415a-15ab-11e5-912d-b5dab916ce86.png)

## 运行
```bash
  // LeanChat (复杂示例)
  cd LeanChat
  pod install --verbose  // 如果本地有 AVOSCloud 依赖库，可以添加 --no-repo-update 选项以加速过程
  open LeanChat.workspace

  // LeanChatExample (简单示例)
  cd LeanChatExample
  pod install --verbose --no-repo-update
  open LeanChatExample.xcworkspace

  // LeanChatSwift (Swift 示例)
  cd LeanChatSwift
  pod install --verbose --no-repo-update
  open LeanChatSwift.xcworkspace

  // LeanChatLib (封装 LeanCloud 通信组件和 UI 的库)
  cd LeanChatLib
  pod install --verbose --no-repo-update
  open LeanChatLib.xcworkspace
```

如果遇到类似于 `definition of 'AVUser' must be imported from module 'LeanChatLib.CDChatListVC' before it is required` 的问题，可以按住 Option 键，在 Produce 菜单中点击 [Clean Build Folder](http://stackoverflow.com/questions/8087065/xcode-4-clean-vs-clean-build-folder) 清除所有构建文件，然后重新编译。这个问题似乎是 CocoaPods 在执行复杂编译时的一个错误。可以查看此 [Gif](https://cloud.githubusercontent.com/assets/5022872/9230256/cf822fe4-4153-11e5-876d-ed819babad89.gif) 以获取更多详细信息。

请注意，由于默认使用生产证书，开发过程中离线消息不会有推送通知。然而，在线版本可以通过 [App Store](https://itunes.apple.com/gb/app/leanchat/id943324553) 下载，它提供推送通知。有关更多详细信息，可以参考此 [issue](https://github.com/leancloud/leanchat-ios/issues/40)。

## 子项目介绍
* LeanChatLib: 聊天的核心逻辑和 UI 库。使用它可以快速集成聊天功能，支持文本、音频、图片和表情消息，以及消息通知。还有一个对应的 [Android 版本](https://github.com/leancloud/leanchat-android)。
* LeanChatExample: LeanChatLib 的最简单用法示例。它展示了如何使用最少的代码调用 LeanChatLib 加入聊天，无论使用 LeanCloud 的用户系统还是自己的用户系统。
* LeanChat-ios: 完整的 LeanChat 应用。它包括了好友管理、群组管理、位置消息、附近用户、个人页、登录和注册等功能，基于 LeanCloud 的存储和通信能力。这是 LeanChatLib 的一个更复杂的应用。

## LeanChatLib 介绍

它封装了最近会话页面和聊天页面。LeanChat 和 LeanChatExample 项目都依赖于它。可以按照以下方法安装,
```
    pod 'LeanChatLib'
```

大多数时候，您会通过将源代码拖入项目来集成 LeanChatLib。在这种情况下，您需要先安装 `AVOSCloud.framework` 和 `AVOSCloudIM.framework`。如果没有使用 `pod install 'AVOSCloud'` 和 `pod install 'AVOSCloudIM'` 进行安装，可以根据 LeanCloud [快速上手指南](https://leancloud.cn/docs/start.html) 配置所需的 Frameworks。还需要安装其他两个依赖库 `JSBadgeView` 和 `DateTools`。在运行 `pod install` 以安装此示例时，将生成一个 Pods 目录，其中可以找到这两个 Pods。或者，可以在 [.podspec 文件](https://github.com/leancloud/leanchat-ios/blob/master/LeanChatLib.podspec#L9) 中进行配置，描述需要集成的源文件和需要引入的系统框架等。或者，请参考此 [票据](https://ticket.leancloud.cn/tickets/7666)。

## 如何在三步中添加 IM
1. 创建一个 LeanCloud 应用。
2. 添加 LeanChatLib pod 依赖，或者将 LeanChatLib 代码文件拖入您的项目中，以便更容易地进行 UI 定制和功能调整。
3. 在适当的地方添加以下代码,

在应用启动时初始化和配置 IM 用户，
```objc
    [AVOSCloud setApplicationId:@"YourAppId" clientKey:@"YourAppKey"];
    [CDChatManager manager].userDelegate = [[CDUserFactory alloc] init];
```

配置一个 UserFactory，它遵循 CDUserDelegate 协议。
```objc
#import "CDUserFactory.h"

#import <LeanChatLib/LeanChatLib.h>

@interface CDUserFactory ()<CDUserDelegate>

@end

@implementation CDUserFactory

#pragma mark - CDUserDelegate
-(void)cacheUserByIds:(NSSet *)userIds block:(AVIMArrayResultBlock)block{
    block(nil,nil); // 不要忘记它
}

-(id<CDUserModel>)getUserById:(NSString *)userId{
    CDUser* user=[[CDUser alloc] init];
    user.userId=userId;
    user.username=userId;
    user.avatarUrl=@"http://ac-x3o016bx.clouddn.com/86O7RAPx2BtTW5zgZTPGNwH9RZD5vNDtPm1YbIcu";
    return user;
}

@end
```

这里，CDUser 是应用程序中的用户对象，并且您可以在用户对象中实现 CDUserModel 协议。

CDUserModel,
```objc
@protocol CDUserModel <NSObject>

@required

-(NSString*)userId;

-(NSString*)avatarUrl;

-(NSString*)username;

@end
```

在登录时调用，
```objc
        [[CDChatManager manager] openWithClientId:selfId callback: ^(BOOL succeeded, NSError *error) {
            if (error) {
                DLog(@"%@", error);
            }
            else {
               //go Main Controller
            }
        }];
```

与某人聊天，
```objc
        [[CDChatManager manager] fetchConvWithOtherId : otherId callback : ^(AVIMConversation *conversation, NSError *error) {
            if (error) {
                DLog(@"%@", error);
            }
            else {
                LCEChatRoomVC *chatRoomVC = [[LCEChatRoomVC alloc] initWithConv:conversation];
                [weakSelf.navigationController pushViewController:chatRoomVC animated:YES];
            }
        }];
```

进行群聊，
```objc
        NSMutableArray *memberIds = [NSMutableArray array];
        [memberIds addObject:groupId1];
        [memberIds addObject:groupId2];
        [memberIds addObject:[CDChatManager manager].selfId];
        [[CDChatManager manager] fetchConvWithMembers:memberIds callback: ^(AVIMConversation *conversation, NSError *error) {
            if (error) {
                DLog(@"%@", error);
            }
            else {
                LCEChatRoomVC *chatRoomVC = [[LCEChatRoomVC alloc] initWithConv:conversation];
                [weakSelf.navigationController pushViewController:chatRoomVC animated:YES];
            }
        }];
```

在注销时，
```objc
    [[CDChatManager manager] closeWithCallback: ^(BOOL succeeded, NSError *error) {

    }];
```

然后，您就可以像截图中所示那样聊天。请注意，我们目前不推荐使用 pod 方法直接导入 LeanChatLib，因为有些接口和功能需要您进行自定义。因此，我们建议将 LeanChatLib 代码复制到项目中，以便更容易进行定制。
