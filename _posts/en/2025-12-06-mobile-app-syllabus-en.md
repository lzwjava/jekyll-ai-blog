---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Mobile Application Development Syllabus Translation
translated: false
type: note
---

Question: Please translate the full Guangdong Higher Education Self-Examination course "Mobile Application Development Technology (Practical)" (Course Code: 14568) syllabus and the sample exam paper into English, and format it neatly.

Answer:

# Guangdong Higher Education Self-Examination
**Course: Mobile Application Development Technology (Practical Assessment)**
**Course Code: 14568**

### I. Assessment Objectives
This is a highly practical course that requires students to independently analyze problems, solve problems, and design/develop applications. Through practical examination, students should:
1. Be familiar with the Android development environment.
2. Master Android project structure and the creation/use of related resources.
3. Master Android UI design, including common layouts and controls.
4. Master Android Activity lifecycle, event handling, Activity navigation, and parameter passing.
5. Master main Android storage methods (SharedPreferences, SQLite).
6. Master common drawing classes, animations, and audio/video playback.
7. Be familiar with JSON data parsing and network access methods.
8. Be familiar with Services, Broadcast mechanisms, Content Providers, and Content Observers.

### II. Reference Textbook
*Android Mobile Development Fundamentals and Case Tutorial*, edited by Heima Programmers, People's Posts and Telecommunications Press, October 2021.

### III. Exam Content
#### (I) Android Project Structure
1. Creating an Android project
2. Setting and using images/icons
3. Creating and using color resource files
4. Creating and using string resource files
5. Creating and using dimension resource files
6. Creating and using style resource files
7. Main configurations in AndroidManifest.xml

#### (II) UI Design and Event Handling
1. Layout design using single or multiple layouts
2. Common basic controls (TextView, EditText, Button, ImageView, RadioButton, CheckBox) and their properties
3. Event listening and handling, accessing controls in code, getting/modifying control properties
4. Using Intent for Activity navigation and parameter passing
5. Using RecyclerView

#### (III) Data Storage
1. Using SharedPreferences for simple data storage and retrieval
2. Using SQLite to create databases/tables and perform CRUD operations

#### (IV) Graphics, Images, and Multimedia
1. Custom drawing using View, Bitmap, BitmapFactory, Paint, Canvas, etc.
2. Playing audio with MediaPlayer and SoundPool
3. Playing video with VideoView or SurfaceView + MediaPlayer

#### (V) Broadcasts and Services
1. Creating and starting services using startService or bindService
2. Defining/registering BroadcastReceiver, sending broadcasts

### IV. Exam Format
The practical exam requires students to create a complete Android project divided into three parts, total **100 points**, exam duration **120 minutes**.

- **Part 1: Android Project Creation and Configuration** – 30 points
  Create project, add/use provided or required resources, configure the project.

- **Part 2: UI Design** – 40 points
  Use appropriate layouts and controls to build the required interface with reasonable property settings.

- **Part 3: Coding and Functionality Implementation** – 30 points
  Implement event handling, navigation & parameter passing, data storage, services/broadcasts, graphics/multimedia, etc.

### V. Exam Environment Requirements
1. JDK 1.8 or higher
2. Android Studio 4.1 or higher (stable version matching the JDK)

### VI. Sample Exam Paper
**Course: Mobile Application Development Technology (Practical)**
**Development Environment:** JDK 1.8, Android Studio 4.1
**Exam Duration:** 90 minutes (note: syllabus says 120 min, sample says 90 min)

**Task:** Design a **Body Weight Management Program**.
The user enters name, gender, height, and weight, clicks "Calculate", the app calculates BMI-related standard weight, then jumps to a second Activity to display advice.

#### Question 1: Android Project Creation and Configuration (30 points)
1. (5 points) Create an Android project named **test + your candidate number**.
2. (15 points) Add/modify resources:
   - Place provided images/resources into correct folders.
   - Add to colors.xml: `<color name="skyblue">#87ceeb</color>`
   - Modify strings.xml so the app title becomes your real name.
   - Add to styles.xml:
     ```xml
     <style name="CustomTitleFontStyle">
         <item name="android:textSize">16pt</item>
         <item name="android:textColor">#000000</item>
     </style>
     ```
3. (5 points) Create two Activities:
   - Launch Activity: **Activity1.java** with layout **activity1.xml**
   - Second Activity: **Activity2.java** with layout **activity2.xml**
4. (5 points) Add storage permissions to AndroidManifest.xml:
   ```xml
   <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
   <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
   ```

#### Question 2: UI Design (40 points)
**Activity1.xml:**
- (5 points) Choose appropriate layout(s) to achieve the interface.
- (20 points) Gender as horizontal RadioGroup (single selection only). Height and weight EditText with inputType="number" and proper hints. Other controls as shown.
- (5 points) Background color = skyblue, title "Standard Weight Calculator" uses style **CustomTitleFontStyle**.

**Activity2.xml:**
- (10 points) Contains a TextView with id **result**.

#### Question 3: Functionality Implementation (30 points)
**Activity1.java:**
On "Calculate" button click:
1. (5 points) Validate height and weight are within reasonable ranges (you define the range, perform necessary type conversion).
2. (10 points) Save input data to SharedPreferences file named **mydata** with keys:
   - name → your real name
   - gender → selected gender
   - height → entered height
   - weight → entered weight
   Export the generated **mydata.xml** file to your computer.
3. (5 points) Start Activity2 and pass gender, height, and weight via Intent extras.

**Activity2.java:**
In onCreate():
- (10 points) Retrieve passed data, convert types as needed, calculate standard weight using:
  - **Male:** (height cm − 80) × 70%
  - **Female:** (height cm − 70) × 60%
- Display the result as a complete sentence in the TextView with id **result**.

#### Submission Requirements
1. Take full screenshots of both running screens (including title bar) and paste into a Word document named **CandidateNumber.docx**.
2. Export the SharedPreferences file **mydata.xml**.
3. Compress the following into a single file named **CandidateNumber.rar**:
   - The entire **main** folder of the project
   - CandidateNumber.docx
   - mydata.xml
4. Upload the .rar file to the server designated by the exam proctor.

**Important:** All files must be saved in the exact location/filenames specified, otherwise zero points will be awarded.
