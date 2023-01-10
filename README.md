
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

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/Spyxpo/swab/dev/screenshots/screenshot-1.png)

## Requirements

Add Flutter, Python, Android Studio, JDK and JRE in environment variables/.bashrc/.zshrc. (If you are using binary release then you don't have to add anything in environment variables/.bashrc/.zshrc.)

> Do restart your computer before installing the app.

- [Flutter](https://flutter.dev/docs/get-started/install/)
- [Rust](https://www.rust-lang.org/tools/install)
- [Python 3.8 or above](https://www.python.org/downloads/)
- [Android Studio](https://developer.android.com/studio)
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

> Rust modules that are required.

```bash
cargo install tauri-cli
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

## Release

> Create a Keystore (For signing app and uploading on Play Store)

Keep your keystore file backed up(backup your_file_name.keystore file, alias name and passwords of your keystore file).

Change everything that is inside ``, e.g. \`File_Name.keystore\` to my_keystore.keystore. You can create your keystore easily using SWAB.

```bash
keytool -genkey -noprompt -v -keystore `File_Name`.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias `Alias_Name` -storetype PKCS12 -storepass `Store_Pass` -keypass `Key_Pass` -dname "CN=`Your_Name`, OU=`Your_Organization_Unit`, O=`Organization`, L=`Your_City_Or_Locality`, S=`Your_State_Or_Province`, C=`Two_Letter_Country_Code`"
```

## Menu Bar

- [File](#file)
  - [New](#new)
     - Create a new project.
  - [Open](#open)
    - Open a project.
  - [Save As](#save-as)
    - Save a project.
  - [Exit](#exit)
    - Exit the app.
- [Commands](#commands)
  - [Build](#build)
    - Build the app.
  - [Clean](#clean)
    - Clean the project folder.
  - [Clean Build](#clean-build)
    - Clean the build folder.
  - [Create a Keystore](#create-a-keystore)
    - Create a keystore file.
  - [Open Build Folder](#open-build-folder)
    - Open the build folder.
- [About](#about)
  - [Visit Website](#visit-website)
    - Visit the website.
  - [Changelog](#changelog)
    - View the changelog.
  - [Source Code](#source-code)
    - View the source code.
  - [View License](#view-license)
    - View the license.

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
- [X] Auto Prerequisites installation for Windows
- [X] Create custom Keystore for Android App

## Coming soon

- [ ] Migrate to Rust Completely
- [ ] Auto Prerequisites installation
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
