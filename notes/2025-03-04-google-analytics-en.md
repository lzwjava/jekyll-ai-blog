---
audio: false
generated: true
lang: en
layout: post
title: Using Google Analytics
translated: false
type: note
---

To use Google Analytics, integrate it into your frontend project, and check the data using both the app and website, follow these steps. This guide assumes your frontend project is either a website or a mobile app and uses **Google Analytics 4 (GA4)**, the current standard as of 2023, since Universal Analytics is no longer supported for new data collection.

---

### 1. Set Up Google Analytics
Before integrating Google Analytics into your project, you need to create an account and configure it:

- **Create an Account**: Go to [analytics.google.com](https://analytics.google.com) and sign up with your Google account if you don’t already have one.
- **Create a GA4 Property**:
  - Click "Admin" in the bottom-left corner.
  - Under "Property," click "Create Property," fill in your project details, and select **Google Analytics 4**.
- **Add a Data Stream**: Depending on your frontend project type:
  - **For a Website**: Choose "Web," enter your website’s URL, and name the stream (e.g., "My Website").
  - **For a Mobile App**: Choose "App," select iOS or Android, and provide your app details (e.g., package name).

After setting up the data stream, you’ll get a **Measurement ID** (e.g., `G-XXXXXXXXXX`), which you’ll use for integration.

---

### 2. Integrate Google Analytics into Your Frontend Project
The integration process depends on whether your frontend project is a website or a mobile app.

#### For a Website
- **Add the Google Tag**:
  - In your GA4 property, go to "Data Streams," select your web stream, and find the "Tagging Instructions."
  - Copy the provided **Google Tag** script, which looks like this:
    ```html
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_MEASUREMENT_ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'YOUR_MEASUREMENT_ID');
    </script>
    ```
  - Paste this code into the `<head>` section of your website’s HTML, replacing `YOUR_MEASUREMENT_ID` with your actual Measurement ID.
- **For Single-Page Applications (SPAs)** (e.g., React, Angular, Vue):
  - The default script tracks only the initial page load. For SPAs, where pages don’t reload on route changes, use a library to track navigation. For example, in **React**:
    1. Install the `react-ga4` library:
       ```bash
       npm install react-ga4
       ```
    2. Initialize it in your app (e.g., in `index.js` or `App.js`):
       ```javascript
       import ReactGA from 'react-ga4';
       ReactGA.initialize('YOUR_MEASUREMENT_ID');
       ```
    3. Track page views on route changes (e.g., using React Router):
       ```javascript
       ReactGA.send({ hitType: "pageview", page: window.location.pathname });
       ```
       Call this whenever the route changes, such as in a `useEffect` hook tied to the router’s location.
  - Similar libraries exist for other frameworks (e.g., `ngx-analytics` for Angular, `vue-ga` for Vue—check for GA4 compatibility).
- **Optional**: Use **Google Tag Manager** (GTM) instead of hardcoding the tag for easier management of tracking scripts.

#### For a Mobile App
- **Using Firebase (Recommended)**:
  - If your app uses Firebase, enable **Google Analytics for Firebase**:
    1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com).
    2. Add your app to the project (iOS or Android).
    3. Follow the prompts to download the config file (e.g., `GoogleService-Info.plist` for iOS, `google-services.json` for Android) and add it to your app.
    4. Install the Firebase SDK:
       - **iOS**: Use CocoaPods (`pod 'Firebase/Analytics'`) and initialize in `AppDelegate`.
       - **Android**: Add dependencies in `build.gradle` and initialize in your app.
    5. Firebase automatically links to your GA4 property and starts collecting data.
- **Without Firebase**:
  - Use the standalone **Google Analytics SDK** for iOS or Android (less common now with GA4’s Firebase integration). Refer to the official documentation for setup, as it varies by platform.

---

### 3. Verify the Integration
- **For Websites**: After adding the tracking code:
  - Visit your website and open the **Real-time** report in Google Analytics (under "Reports" > "Real-time").
  - If you see your visit logged, the integration is working.
  - Alternatively, use a browser tool like **GA Checker** or the Chrome DevTools console to confirm `gtag` calls.
- **For Apps**: Check the Firebase Console or GA4 Real-time report after launching your app with the SDK installed. It may take a few minutes for data to appear.

---

### 4. Check the Data Using the App and Website
Once Google Analytics starts collecting data, you can view it in two ways:
- **Google Analytics Web Interface**:
  - Log in to [analytics.google.com](https://analytics.google.com).
  - Select your GA4 property.
  - Explore reports like:
    - **Real-time**: See live user activity.
    - **Audience**: Understand user demographics.
    - **Acquisition**: Track where users come from.
    - **Behavior**: Analyze user interactions (e.g., page views, events).
- **Google Analytics Mobile App**:
  - Download the official **Google Analytics app** from the App Store (iOS) or Google Play Store (Android).
  - Sign in with your Google account and select your property.
  - View a subset of reports (e.g., Real-time, Audience) on the go.

---

### Additional Notes
- **If Your Project Includes Both a Website and an App**: You can add multiple data streams (e.g., one for the website, one for the app) under the same GA4 property. This allows you to view combined or separate analytics in the same interface.
- **Tracking Events**: Beyond page views, track custom events (e.g., button clicks) using `gtag('event', ...)` for websites or Firebase’s `logEvent` for apps. Example for a website:
  ```javascript
  gtag('event', 'click', {
    'event_category': 'Button',
    'event_label': 'Submit'
  });
  ```
- **GA4 vs. Universal Analytics**: Use GA4 for new projects, as Universal Analytics stopped processing data after July 1, 2023.

By following these steps, you’ll successfully integrate Google Analytics into your frontend project and be able to monitor user data using both the Google Analytics website and mobile app. If your project type (website or app) requires specific clarification, adjust the integration steps accordingly!
