
<img src="https://raw.githubusercontent.com/Spyxpo/swab/dev/images/logo.png" width="50" height="50">

# SWAB (Spyxpo Web to App Builder)

**Convert any website into an iOS/Android/Windows/macOS/Linux app.**

This is a preview build for testing purposes major update coming soon.

- [Downloads](https://github.com/Spyxpo/swab/releases/latest)
- [Features](#features)
- [Coming Soon](#coming-soon)

## Supported OS

- Windows
- macOS
- Linux

## Steps

- [Requirements](#requirements)
- [Installation](#installation)
- [Update](#update)
- [Clean](#clean)
- [Release](#release)
- [Known Issues](#known-issues)

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/Spyxpo/swab/dev/screenshots/screenshot-1.png)

## Requirements

Add Flutter, Python, Android Studio, JDK and JRE in environment variables/.bashrc/.zshrc.

> Do restart your computer before installing the app.

- [Git](https://git-scm.com/downloads/)
- [Flutter](https://flutter.dev/docs/get-started/install/)
- [NodeJS](https://nodejs.org/en/download/)
- [Python 3.8 or above](https://www.python.org/downloads/)
- [Android Studio](https://developer.android.com/studio)
- [Xcode (only for macOS)](https://apps.apple.com/us/app/xcode/id497799835?mt=12)
- [JDK](https://www.oracle.com/java/technologies/downloads/)
- [JRE](https://www.java.com/en/download/)

> Python3 modules that are required.

```bash
pip3 install pillow 
pip3 install icnsutil
pip3 install userpath
pip3 install wget
```

or

```bash
pip install pillow 
pip install icnsutil
pip install userpath
pip install wget
```

## Installation

```bash
git clone https://github.com/Spyxpo/swab.git
cd swab
python3 run.py
```

or

```bash
git clone https://github.com/Spyxpo/swab.git
cd swab
python run.py
```

## Update

```bash
cd swab
git pull
```

or

```bash
cd swab
python3 update.py
```

or

```bash
cd swab
python update.py
```

## Clean

Clean your project folder.

```bash
cd swab
python3 clean.py
```

or

```bash
cd swab
python clean.py
```

## Known Issues

All issues that are known to us are listed here, we are working on fixing them.

- "build.py" only builds executable for Windows OS.
- "Not Responding" while building apps, this occurs when you are building apps so this does not affect your build process.

## Release

> Create a Keystore (For signing app and uploading on Play Store)

Keep your keystore file backed up(backup .jks file, alias name and passwords of your keystore file)

```bash
keytool -genkey -v -keystore upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload -storetype JKS
```

## Features

- [X] Android Support (.apk & .aab)
- [X] macOS Support
- [X] Windows Support
- [X] Linux Support
- [X] App works without internet
- [X] Javascript enabled
- [X] Play Store ready app
- [X] Your own keystore
- [X] External url opener
- [X] Deep Linking
- [X] App update popup
- [X] Loading Indicator
- [X] Splash Screen
- [X] Desktop apps custom icon
- [X] Auto Preqrequisites installation for Windows
- [X] Create custom Keystore for Android App

## Coming soon

- [ ] Auto prequisites installation
- [ ] Dessktop app installer
- [ ] Desktop app update popup
- [ ] Desktop app Splash Screen
- [ ] Desktop app External url opener
- [ ] Desktop app Deep Linking
- [ ] Desktop app Loading Indicator
- [ ] Notifications
- [ ] Local HTML website
- [ ] Admob support
- [ ] Admin app
- [ ] Deep Linking enhancements
- [ ] Pull to refresh
- [ ] iOS app

## Authors

- [Mantresh Khurana](https://github.com/mantreshkhurana/)
