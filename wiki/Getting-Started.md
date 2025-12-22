# Getting Started

This guide will help you install SWAB and create your first app.

---

## Prerequisites

Before installing SWAB, ensure you have the following installed on your system:

### Required for All Platforms

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.8 or higher | Backend server |
| Flutter SDK | 3.0 or higher | App building |
| Git | Any recent version | Cloning repository |

### Platform-Specific Requirements

#### For Android Builds
- **Android Studio** (latest version)
- **Android SDK** (API level 21+)
- **Java JDK** 11 or higher (for keystore generation)

#### For iOS Builds (macOS only)
- **Xcode** 14.0 or higher
- **CocoaPods** (`sudo gem install cocoapods`)

#### For macOS Builds (macOS only)
- **Xcode** 14.0 or higher
- **Xcode Command Line Tools** (`xcode-select --install`)

#### For Windows Builds (Windows only)
- **Visual Studio 2019 or later** with "Desktop development with C++" workload
- **Windows 10 SDK**

#### For Linux Builds (Linux only)
- **Clang** (`sudo apt install clang`)
- **CMake** (`sudo apt install cmake`)
- **GTK 3** development libraries (`sudo apt install libgtk-3-dev`)
- **Ninja build** (`sudo apt install ninja-build`)

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/user/swab.git
cd swab
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Flutter Installation

```bash
flutter doctor
```

Ensure all checkmarks are green for the platforms you want to build for.

### Step 5: Run SWAB

```bash
python app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6: Open the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

---

## Creating Your First App

### 1. Enter App Information

Fill in the basic app details:

| Field | Description | Example |
|-------|-------------|---------|
| **App Name** | Display name for your app | My Awesome App |
| **Description** | Brief description | A mobile app for my website |
| **Version** | Semantic version | 1.0.0 |
| **Build Number** | Integer for updates | 1 |
| **Package Name** | Unique identifier | com.example.myawesomeapp |

### 2. Set the Website URL

Enter the full URL of the website you want to convert:
```
https://example.com
```

> **Note**: Ensure the URL is accessible and loads correctly in a browser.

### 3. Upload App Icon (Optional)

- Click "Browse" or drag and drop an image
- Recommended size: **1024x1024 pixels**
- Supported formats: PNG, JPG

### 4. Configure WebView Settings (Optional)

Click "WebView Settings" to customize behavior:

| Setting | Default | Description |
|---------|---------|-------------|
| JavaScript | Enabled | Execute JavaScript in WebView |
| Zoom | Disabled | Allow pinch-to-zoom |
| DOM Storage | Enabled | Enable localStorage |
| Geolocation | Disabled | Allow location access |
| Pull to Refresh | Enabled | Swipe down to refresh |
| Navigation Bar | Disabled | Show back/forward buttons |
| File Access | Disabled | Allow file uploads |
| Cache | Enabled | Cache content offline |
| Media Autoplay | Disabled | Auto-play media |

### 5. Select Target Platforms

Check the platforms you want to build for:

- [ ] Android (APK)
- [ ] Android (App Bundle)
- [ ] iOS
- [ ] macOS
- [ ] Windows
- [ ] Linux

### 6. Configure Android Signing (If building for Android)

**Option A: Auto-generate Keystore**
- Leave the keystore section empty
- SWAB will automatically generate a debug keystore

**Option B: Use Your Own Keystore**
1. Upload your `.jks` or `.keystore` file
2. Enter the keystore password
3. Enter the key alias
4. Enter the key password

### 7. Build the App

1. Click **"Build App"**
2. Watch the progress bar and status updates
3. Wait for the build to complete (typically 2-5 minutes per platform)

### 8. Download Your App

Once complete, download buttons will appear for each platform:
- **Android APK** - Ready to install on devices
- **Android AAB** - For Google Play Store upload
- **iOS** - .app file for Xcode signing
- **macOS/Windows/Linux** - ZIP archive with executable

---

## Saving Your Project

Save your configuration for future use:

1. Click **"Save Project"** in the toolbar
2. A `.swab` file will be downloaded
3. This file contains all your settings, encrypted and machine-specific

---

## Loading a Project

To load a previously saved project:

1. Click **"Open Project"** in the toolbar
2. Select your `.swab` file
3. All settings will be restored

> **Note**: Projects are encrypted with machine-specific keys and can only be opened on the same computer where they were created.

---

## Next Steps

- [[Configuration Guide]] - Learn about all configuration options
- [[Platform Build Guide]] - Platform-specific build instructions
- [[Troubleshooting]] - Solutions to common issues

---

## Video Tutorial

*Coming soon*
