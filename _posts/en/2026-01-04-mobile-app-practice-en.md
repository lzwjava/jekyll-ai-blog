---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Mobile App Development Practice Questions
translated: false
type: note
---

Question: Provide 30 multiple-choice questions (with 4 options each) based on the Guangdong Higher Education Self-Examination course "Mobile Application Development Technology (Practical Assessment)" (Course Code: 14568), covering the topics in the syllabus and similar in style and difficulty to the sample exam paper. Do not reveal the correct answers.

Answer:

Here are 30 multiple-choice questions for practice or exam preparation:

1. When creating a new Android project in Android Studio, which template is typically chosen for a basic empty app?
   A) Empty Activity
   B) Basic Activity
   C) Navigation Drawer Activity
   D) Blank Fragment

2. In which folder should drawable resources like images be placed?
   A) res/values
   B) res/layout
   C) res/drawable
   D) res/menu

3. How do you define a color resource named "primary_color" in colors.xml?
   A) <color name="primary_color">#FF5722</color>
   B) <string name="primary_color">#FF5722</string>
   C) <item name="primary_color">#FF5722</item>
   D) <resource name="primary_color">#FF5722</resource>

4. To change the application name displayed on the device, which string resource in strings.xml should be modified?
   A) app_title
   B) app_name
   C) application_label
   D) title_text

5. Which file must declare all Activities used in the project?
   A) build.gradle
   B) AndroidManifest.xml
   C) activity_main.xml
   D) styles.xml

6. Which layout arranges its children in a single horizontal or vertical row?
   A) RelativeLayout
   B) ConstraintLayout
   C) LinearLayout
   D) FrameLayout

7. To allow only numeric input in an EditText for height, which attribute should be set?
   A) android:inputType="text"
   B) android:inputType="number"
   C) android:inputType="phone"
   D) android:inputType="decimal"

8. Which control is best suited for single selection between "Male" and "Female"?
   A) CheckBox
   B) Spinner
   C) RadioGroup with RadioButtons
   D) ToggleButton

9. How do you apply a custom style to a TextView in XML?
   A) android:style="@style/CustomTitleFontStyle"
   B) android:theme="@style/CustomTitleFontStyle"
   C) android:layout_style="@style/CustomTitleFontStyle"
   D) android:textStyle="@style/CustomTitleFontStyle"

10. Which component is recommended for displaying a scrollable list of items in modern Android apps?
    A) ListView
    B) GridView
    C) RecyclerView
    D) ScrollView

11. To set an onClick listener for a Button in code, which method is commonly used?
    A) button.setOnClickListener()
    B) button.addClickListener()
    C) button.onClick()
    D) button.setClickEvent()

12. Which Intent method is used to start another Activity?
    A) startService()
    B) sendBroadcast()
    C) startActivity()
    D) bindService()

13. To pass a String value "height" with value 170 to another Activity, which method is used?
    A) intent.putExtra("height", 170)
    B) intent.addExtra("height", 170)
    C) intent.setData("height", 170)
    D) intent.putData("height", 170)

14. In the receiving Activity, how do you retrieve an int extra named "weight"?
    A) getIntent().getIntExtra("weight", 0)
    B) getExtras().getInteger("weight")
    C) intent.getData("weight")
    D) bundle.getInt("weight")

15. Which class is used for simple key-value persistent storage in Android?
    A) SQLiteDatabase
    B) FileOutputStream
    C) SharedPreferences
    D) ContentValues

16. To get a SharedPreferences instance named "mydata" in MODE_PRIVATE, which method is used?
    A) getSharedPreferences("mydata", Context.MODE_PRIVATE)
    B) getPreferences("mydata", Context.MODE_WORLD_READABLE)
    C) openSharedPreferences("mydata")
    D) getDefaultSharedPreferences("mydata")

17. How do you save a String value to SharedPreferences?
    A) editor.putString("key", value); editor.commit();
    B) editor.saveString("key", value);
    C) preferences.write("key", value);
    D) editor.add("key", value); editor.apply();

18. Which class is used to perform database operations like create, insert, update, delete in SQLite?
    A) SQLiteOpenHelper
    B) Cursor
    C) ContentResolver
    D) DatabaseUtils

19. To execute raw SQL in SQLite, which method of SQLiteDatabase is used?
    A) execSQL()
    B) rawQuery()
    C) runSQL()
    D) querySQL()

20. Which class is commonly used for custom drawing in a View?
    A) Paint
    B) Bitmap
    C) Canvas
    D) All of the above

21. To decode an image file into a Bitmap, which class is typically used?
    A) BitmapFactory
    B) ImageDecoder
    C) DrawableFactory
    D) AssetManager

22. Which class is best for playing short sound effects efficiently?
    A) MediaPlayer
    B) SoundPool
    C) AudioTrack
    D) ExoPlayer

23. To play a video in a simple way, which control is commonly used?
    A) ImageView
    B) SurfaceView
    C) VideoView
    D) TextureView

24. To start a Service that runs in the background without binding, which method is used?
    A) bindService()
    B) startService()
    C) createService()
    D) runService()

25. Which component is used to respond to system or custom broadcasts?
    A) Service
    B) BroadcastReceiver
    C) ContentProvider
    D) Activity

26. To send a custom broadcast, which method of Context is used?
    A) sendBroadcast(Intent)
    B) broadcastIntent(Intent)
    C) dispatchBroadcast(Intent)
    D) publishBroadcast(Intent)

27. In AndroidManifest.xml, how are permissions like WRITE_EXTERNAL_STORAGE added?
    A) <permission android:name="..."/>
    B) <uses-permission android:name="..."/>
    C) <allow-permission android:name="..."/>
    D) <request-permission android:name="..."/>

28. Which attribute in AndroidManifest.xml sets the launcher Activity?
    A) <intent-filter> with ACTION_MAIN and CATEGORY_LAUNCHER
    B) <launcher-activity>
    C) <main-activity>
    D) <default-activity>

29. To set the background color of an Activity's root layout from a color resource, which attribute is used?
    A) android:background="@color/skyblue"
    B) android:colorBackground="@color/skyblue"
    C) android:layout_color="@color/skyblue"
    D) android:fillColor="@color/skyblue"

30. When exporting a SharedPreferences file for submission, it is typically located in which directory on the device/emulator?
    A) /data/data/<package_name>/shared_prefs/
    B) /res/values/
    C) /assets/
    D) /drawable/
