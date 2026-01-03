---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 移动应用开发练习题
translated: true
type: note
---

问题：根据广东省高等教育自学考试课程《移动应用开发技术（实践考核）》（课程代码：14568），提供 30 道单选题（每题 4 个选项），涵盖大纲中的核心内容，且风格和难度与样卷相似。不要提供正确答案。

回答：

以下是 30 道供练习或备考使用的单选题：

1. 在 Android Studio 中创建新项目时，基础的空白应用通常选择哪种模板？  
   A) Empty Activity  
   B) Basic Activity  
   C) Navigation Drawer Activity  
   D) Blank Fragment

2. 像图片这类 drawable 资源应该放置在哪个文件夹中？  
   A) res/values  
   B) res/layout  
   C) res/drawable  
   D) res/menu

3. 如何在 colors.xml 中定义一个名为 "primary_color" 的颜色资源？  
   A) <color name="primary_color">#FF5722</color>  
   B) <string name="primary_color">#FF5722</string>  
   C) <item name="primary_color">#FF5722</item>  
   D) <resource name="primary_color">#FF5722</resource>

4. 若要更改设备上显示的应用程序名称，应修改 strings.xml 中的哪个字符串资源？  
   A) app_title  
   B) app_name  
   C) application_label  
   D) title_text

5. 哪个文件必须声明项目中使用的所有 Activities？  
   A) build.gradle  
   B) AndroidManifest.xml  
   C) activity_main.xml  
   D) styles.xml

6. 哪种布局将其子控件排列在单行（水平）或单列（垂直）中？  
   A) RelativeLayout  
   B) ConstraintLayout  
   C) LinearLayout  
   D) FrameLayout

7. 若要在 EditText 中仅允许输入数字以表示身高，应设置哪个属性？  
   A) android:inputType="text"  
   B) android:inputType="number"  
   C) android:inputType="phone"  
   D) android:inputType="decimal"

8. 哪种控件最适合在“男”和“女”之间进行单项选择？  
   A) CheckBox  
   B) Spinner  
   C) 包含 RadioButton 的 RadioGroup  
   D) ToggleButton

9. 如何在 XML 中为 TextView 应用自定义样式？  
   A) android:style="@style/CustomTitleFontStyle"  
   B) android:theme="@style/CustomTitleFontStyle"  
   C) android:layout_style="@style/CustomTitleFontStyle"  
   D) android:textStyle="@style/CustomTitleFontStyle"

10. 在现代 Android 应用中，推荐使用哪个组件来显示可滚动的列表项？  
    A) ListView  
    B) GridView  
    C) RecyclerView  
    D) ScrollView

11. 在代码中为 Button 设置点击监听器，通常使用哪个方法？  
    A) button.setOnClickListener()  
    B) button.addClickListener()  
    C) button.onClick()  
    D) button.setClickEvent()

12. 哪个 Intent 方法用于启动另一个 Activity？  
    A) startService()  
    B) sendBroadcast()  
    C) startActivity()  
    D) bindService()

13. 若要将 String 类型的值 "height"（内容为 170）传递给另一个 Activity，应使用哪个方法？  
    A) intent.putExtra("height", 170)  
    B) intent.addExtra("height", 170)  
    C) intent.setData("height", 170)  
    D) intent.putData("height", 170)

14. 在接收端 Activity 中，如何检索名为 "weight" 的 int 类型 extra 数据？  
    A) getIntent().getIntExtra("weight", 0)  
    B) getExtras().getInteger("weight")  
    C) intent.getData("weight")  
    D) bundle.getInt("weight")

15. Android 中用于简单的键值对（key-value）持久化存储的类是哪个？  
    A) SQLiteDatabase  
    B) FileOutputStream  
    C) SharedPreferences  
    D) ContentValues

16. 若要获取 MODE_PRIVATE 模式下名为 "mydata" 的 SharedPreferences 实例，应使用哪个方法？  
    A) getSharedPreferences("mydata", Context.MODE_PRIVATE)  
    B) getPreferences("mydata", Context.MODE_WORLD_READABLE)  
    C) openSharedPreferences("mydata")  
    D) getDefaultSharedPreferences("mydata")

17. 如何将 String 值保存到 SharedPreferences 中？  
    A) editor.putString("key", value); editor.commit();  
    B) editor.saveString("key", value);  
    C) preferences.write("key", value);  
    D) editor.add("key", value); editor.apply();

18. 在 SQLite 中执行创建、插入、更新、删除等数据库操作时，主要使用哪个类？  
    A) SQLiteOpenHelper  
    B) Cursor  
    C) ContentResolver  
    D) DatabaseUtils

19. 在 SQLite 中执行原始 SQL 语句，应使用 SQLiteDatabase 的哪个方法？  
    A) execSQL()  
    B) rawQuery()  
    C) runSQL()  
    D) querySQL()

20. 在 View 中进行自定义绘制时，通常会用到哪些类？  
    A) Paint  
    B) Bitmap  
    C) Canvas  
    D) 以上全部

21. 若要将图像文件解码为 Bitmap，通常使用哪个类？  
    A) BitmapFactory  
    B) ImageDecoder  
    C) DrawableFactory  
    D) AssetManager

22. 哪种类最适合高效地播放短促的音效？  
    A) MediaPlayer  
    B) SoundPool  
    C) AudioTrack  
    D) ExoPlayer

23. 若要以简单的方式播放视频，通常使用哪个控件？  
    A) ImageView  
    B) SurfaceView  
    C) VideoView  
    D) TextureView

24. 若要启动一个在后台运行且不进行绑定的 Service，应使用哪个方法？  
    A) bindService()  
    B) startService()  
    C) createService()  
    D) runService()

25. 哪个组件用于响应系统或自定义的广播通知？  
    A) Service  
    B) BroadcastReceiver  
    C) ContentProvider  
    D) Activity

26. 若要发送自定义广播，应使用 Context 的哪个方法？  
    A) sendBroadcast(Intent)  
    B) broadcastIntent(Intent)  
    C) dispatchBroadcast(Intent)  
    D) publishBroadcast(Intent)

27. 在 AndroidManifest.xml 中，如何添加像 WRITE_EXTERNAL_STORAGE 这样的权限？  
    A) <permission android:name="..."/>  
    B) <uses-permission android:name="..."/>  
    C) <allow-permission android:name="..."/>  
    D) <request-permission android:name="..."/>

28. AndroidManifest.xml 中的哪个属性用于设置启动 Activity（launcher Activity）？  
    A) 包含 ACTION_MAIN 和 CATEGORY_LAUNCHER 的 <intent-filter>  
    B) <launcher-activity>  
    C) <main-activity>  
    D) <default-activity>

29. 若要从颜色资源中为 Activity 的根布局设置背景颜色，应使用哪个属性？  
    A) android:background="@color/skyblue"  
    B) android:colorBackground="@color/skyblue"  
    C) android:layout_color="@color/skyblue"  
    D) android:fillColor="@color/skyblue"

30. 导出用于提交的 SharedPreferences 文件时，它通常位于设备/模拟器的哪个目录下？  
    A) /data/data/<package_name>/shared_prefs/  
    B) /res/values/  
    C) /assets/  
    D) /drawable/