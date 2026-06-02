---
audio: false
generated: true
lang: en
layout: post
title: Publishing an iOS App to the App Store
translated: false
type: note
---

To use the Apple Developer Program to upload an iOS app, whether for personal or corporate use, you need to enroll in the program, prepare and package your app, upload it, and manage updates. Below is a step-by-step guide addressing all aspects of your query, including the Dun & Bradstreet (D-U-N-S) number requirement for corporate use, packaging the app, uploading the archive, and updating apps via Apple’s site.

---

### 1. Enrolling in the Apple Developer Program

#### For Individuals (Personal Use)
- **Create an Apple ID**:
  If you don’t have one, go to [appleid.apple.com](https://appleid.apple.com) and sign up using a personal email address.
- **Enroll in the Program**:
  - Visit [developer.apple.com/programs/](https://developer.apple.com/programs/) and click "Enroll."
  - Sign in with your Apple ID.
  - Agree to the terms, provide your personal legal name and address, and pay the annual fee of $99 USD.
- **Key Note**: Your personal name will appear as the seller on the App Store.

#### For Corporations (Organizational Use)
- **Obtain a D-U-N-S Number**:
  - A D-U-N-S Number is a unique nine-digit identifier assigned by Dun & Bradstreet to verify your organization’s legal entity status. Apple requires this for corporate accounts.
  - Check if your organization already has one at [dnb.com](https://www.dnb.com). If not, request it for free via their website—processing can take up to two weeks.
- **Enroll in the Program**:
  - Use an Apple ID tied to your organization (e.g., a business email).
  - Go to [developer.apple.com/programs/](https://developer.apple.com/programs/) and click "Enroll."
  - Select "Organization" and provide:
    - Legal entity name
    - Headquarters address
    - D-U-N-S Number
  - The person enrolling must have legal authority to agree to Apple’s terms on behalf of the organization.
  - Pay the $99 USD annual fee.
- **Key Note**: Your organization’s name will appear as the seller on the App Store.

---

### 2. Preparing and Packaging the App
- **Develop Your App in Xcode**:
  - Use Xcode, Apple’s official development tool, to build your iOS app.
  - Ensure it meets [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).
  - Set the deployment target and update the app’s version and build numbers in the project settings.
- **Archive the App**:
  - Open your project in Xcode.
  - Select "Generic iOS Device" (or any simulator) as the build target.
  - Go to **Product** > **Archive** in the menu bar.
  - Xcode will compile your app and create an archive, which is a packaged version ready for distribution, including code, resources, and signing information.

---

### 3. Uploading the App Archive
- **Using Xcode**:
  - After archiving, the Organizer window opens automatically in Xcode.
  - Select your archive and click **Distribute App**.
  - Choose **App Store Connect** as the distribution method.
  - Follow the prompts to validate and upload the archive to App Store Connect.
- **Using Transporter (Alternative)**:
  - Download the [Transporter app](https://apps.apple.com/us/app/transporter/id1450874784) from the Mac App Store.
  - Sign in with your Apple ID.
  - Add the archived app file (exported as a `.ipa` file from Xcode) and upload it to App Store Connect.
  - This option is useful for advanced users or bulk uploads.

---

### 4. Updating Apps Using Apple’s Site (App Store Connect)
- **Access App Store Connect**:
  - Go to [appstoreconnect.apple.com](https://appstoreconnect.apple.com) and log in with your Apple ID.
- **Manage Your App**:
  - Select your app from the dashboard.
  - Navigate to the **App Store** tab.
  - Update metadata (e.g., app description, screenshots, keywords).
  - Under "Versions," select the new build you uploaded.
- **Submit for Review**:
  - Click **Submit for Review** to send the update to Apple’s review team.
  - After approval, you can release it manually or schedule an automatic release.

---

### Additional Notes
- **Corporate-Specific Details**:
  - Ensure your D-U-N-S Number and organizational information are accurate to avoid enrollment delays.
  - You can invite team members (e.g., developers, testers) to your account via App Store Connect and assign roles like "Developer" or "Admin."
- **Common Challenges and Tips**:
  - **Code Signing Issues**: Verify your certificates and provisioning profiles in Xcode under **Signing & Capabilities**. Use the "Automatically manage signing" option if unsure.
  - **App Review Rejections**: Test your app thoroughly to comply with Apple’s guidelines and avoid delays.
  - **D-U-N-S Delays**: Apply for your D-U-N-S Number early if you’re a corporation, as it’s a prerequisite for enrollment.

---

With these steps, you can successfully use the Apple Developer Program to upload and update your iOS app, whether as an individual or a corporation. For further details, refer to Apple’s official documentation at [developer.apple.com](https://developer.apple.com).
