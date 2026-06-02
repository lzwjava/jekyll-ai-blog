---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 移动应用开发教学大纲翻译
translated: true
type: note
---

# 广东高等教育自学考试

**课程：移动应用开发技术（实践考核）**
**课程代码：14568**

### 一、考核目标

本课程是一门实践性很强的课程，要求考生独立进行问题的分析、解决和应用设计开发。通过实践考核，应使考生：

1. 熟悉Android开发环境。
2. 掌握Android项目结构、相关资源的创建与使用。
3. 掌握Android UI设计，包括常用布局和控件。
4. 掌握Android Activity生命周期、事件处理、Activity导航及参数传递。
5. 掌握Android主要存储方式（SharedPreferences、SQLite）。
6. 掌握常用绘图类、动画、音视频播放。
7. 熟悉JSON数据解析与网络访问方式。
8. 熟悉Services、Broadcast机制、Content Providers和Content Observers。

### 二、参考教材

《Android移动开发基础与案例教程》，黑马程序员主编，人民邮电出版社，2021年10月。

### 三、考核内容

#### (一) Android项目结构

1. 创建Android项目
2. 设置和使用图片/图标
3. 创建和使用颜色资源文件
4. 创建和使用字符串资源文件
5. 创建和使用尺寸资源文件
6. 创建和使用样式资源文件
7. AndroidManifest.xml中的主要配置

#### (二) UI设计和事件处理

1. 单一或多种布局进行界面设计
2. 常见基本控件（TextView、EditText、Button、ImageView、RadioButton、CheckBox）及其属性
3. 事件监听和处理，在代码中访问控件，获取/修改控件属性
4. 使用Intent进行Activity导航和参数传递
5. 使用RecyclerView

#### (三) 数据存储

1. 使用SharedPreferences进行简单数据存储和读取
2. 使用SQLite创建数据库/表并进行CRUD操作

#### (四) 图形、图像和多媒体

1. 使用View、Bitmap、BitmapFactory、Paint、Canvas等进行自定义绘图
2. 使用MediaPlayer和SoundPool播放音频
3. 使用VideoView或SurfaceView + MediaPlayer播放视频

#### (五) 广播和服务

1. 使用startService或bindService创建和启动服务
2. 定义/注册BroadcastReceiver，发送广播

### 四、考核方式

实践考核要求考生完成一个完整的Android项目，分为三个部分，总分**100分**，考试时长**120分钟**。

- **第一部分：Android项目创建与配置** – 30分
  创建项目，添加/使用提供的或要求的资源，配置项目。

- **第二部分：UI设计** – 40分
  使用适当的布局和控件构建所需界面，合理设置属性。

- **第三部分：编码与功能实现** – 30分
  实现事件处理、导航与参数传递、数据存储、服务/广播、图形/多媒体等功能。

### 五、考试环境要求

1. JDK 1.8或更高版本
2. Android Studio 4.1或更高版本（与JDK匹配的稳定版本）

### 六、样题

**课程：移动应用开发技术（实践考核）**
**开发环境：** JDK 1.8, Android Studio 4.1
**考试时长：** 90分钟（注：大纲为120分钟，样题为90分钟）

**任务：** 设计一个**身体重量管理程序**。
用户输入姓名、性别、身高、体重，点击“计算”按钮，应用程序计算BMI相关标准体重，然后跳转到第二个Activity显示建议。

#### 第1题：Android项目创建与配置 (30分)

1. (5分) 创建一个Android项目，项目名为 **test + 考生号**。
2. (15分) 添加/修改资源：
   - 将提供的图片/资源放入正确的文件夹。
   - 在colors.xml中添加：`<color name="skyblue">#87ceeb</color>`
   - 修改strings.xml，使应用标题变为你的真实姓名。
   - 在styles.xml中添加：

     ```xml
     <style name="CustomTitleFontStyle">
         <item name="android:textSize">16pt</item>
         <item name="android:textColor">#000000</item>
     </style>
     ```

3. (5分) 创建两个Activity：
   - 启动Activity：**Activity1.java**，布局文件 **activity1.xml**
   - 第二个Activity：**Activity2.java**，布局文件 **activity2.xml**
4. (5分) 在AndroidManifest.xml中添加存储权限：

   ```xml
   <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
   <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
   ```

#### 第2题：UI设计 (40分)

**Activity1.xml：**

- (5分) 选择合适的布局实现界面。
- (20分) 性别为水平RadioGroup（只能单选）。身高和体重EditText的inputType="number"并设置合适的提示文本。其他控件如图所示。
- (5分) 背景颜色=skyblue，标题“标准体重计算器”使用样式**CustomTitleFontStyle**。

**Activity2.xml：**

- (10分) 包含一个id为**result**的TextView。

#### 第3题：功能实现 (30分)

**Activity1.java：**
“计算”按钮点击事件：

1. (5分) 验证身高和体重是否在合理范围（自行定义范围，进行必要的类型转换）。
2. (10分) 将输入数据保存到SharedPreferences文件**mydata**中，键值对如下：
   - name → 你的真实姓名
   - gender → 选定的性别
   - height → 输入的身高
   - weight → 输入的体重
   将生成的**mydata.xml**文件导出到你的电脑。
3. (5分) 启动Activity2，并通过Intent extras传递性别、身高和体重。

**Activity2.java：**
在onCreate()中：

- (10分) 检索传递的数据，根据需要进行类型转换，计算标准体重：
  - **男性：** (身高 cm − 80) × 70%
  - **女性：** (身高 cm − 70) × 60%
- 将结果以完整的句子形式显示在id为**result**的TextView中。

#### 提交要求

1. 截取两个运行屏幕的完整截图（包括标题栏），粘贴到名为**考生号.docx**的Word文档中。
2. 导出SharedPreferences文件 **mydata.xml**。
3. 将以下内容压缩为一个文件，名为**考生号.rar**：
   - 项目的整个**main**文件夹
   - 考生号.docx
   - mydata.xml
4. 将.rar文件上传到监考老师指定的服务器。

**重要：** 所有文件必须保存到指定位置/文件名，否则视为0分。
