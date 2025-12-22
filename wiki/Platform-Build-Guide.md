# Platform Build Guide

This guide provides detailed instructions for building apps on each supported platform.

---

## Table of Contents

- [Android](#android)
- [iOS](#ios)
- [macOS](#macos)
- [Windows](#windows)
- [Linux](#linux)
- [Cross-Platform Building](#cross-platform-building)

---

## Android

### Requirements

| Component | Version | Installation |
|-----------|---------|--------------|
| Android Studio | Latest | [Download](https://developer.android.com/studio) |
| Android SDK | API 21+ | Via Android Studio |
| Java JDK | 11+ | Via Android Studio or [AdoptOpenJDK](https://adoptopenjdk.net) |
| Flutter | 3.0+ | [Flutter Install](https://flutter.dev/docs/get-started/install) |

### Setup Verification

```bash
flutter doctor --android-licenses
flutter doctor
```

Ensure you see a green checkmark next to Android toolchain.

### Build Outputs

| Type | File | Use Case |
|------|------|----------|
| APK | `app-release.apk` | Direct installation, testing |
| AAB | `app-release.aab` | Google Play Store upload |

### APK vs AAB

**APK (Android Package)**
- Single file containing entire app
- Larger file size
- Can be installed directly on devices
- Best for: Testing, direct distribution, alternative stores

**AAB (Android App Bundle)**
- Optimized by Google Play for each device
- Smaller download for users
- Required for new Google Play apps
- Best for: Google Play Store distribution

### Signing Configuration

#### Option 1: Auto-generated Keystore

Leave keystore fields empty. SWAB generates a debug keystore:
- Location: `builds/{build_id}/keystore.jks`
- Password: `android`
- Key Alias: `key`
- Valid for: Testing only

#### Option 2: Production Keystore

1. **Create a keystore:**
   ```bash
   keytool -genkey -v \
     -keystore release-key.jks \
     -keyalg RSA \
     -keysize 2048 \
     -validity 10000 \
     -alias release
   ```

2. **Upload in SWAB interface**

3. **Enter credentials:**
   - Keystore Password
   - Key Alias
   - Key Password

### Google Play Store Upload

1. Build with AAB format
2. Create a Google Play Developer account ($25 one-time fee)
3. Create a new app in Google Play Console
4. Upload the AAB file
5. Complete store listing, content rating, pricing
6. Submit for review

### Troubleshooting

**"SDK not found"**
```bash
flutter config --android-sdk /path/to/android/sdk
```

**"License not accepted"**
```bash
flutter doctor --android-licenses
```

**Build fails with memory error**
Add to `android/gradle.properties`:
```properties
org.gradle.jvmargs=-Xmx4096m
```

---

## iOS

### Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| macOS | 10.15+ | Required for Xcode |
| Xcode | 14.0+ | [App Store](https://apps.apple.com/app/xcode/id497799835) |
| CocoaPods | Latest | `sudo gem install cocoapods` |
| Apple Developer Account | - | Required for distribution |

### Setup Verification

```bash
xcode-select --install
sudo xcodebuild -license accept
pod --version
flutter doctor
```

Ensure you see a green checkmark next to Xcode.

### Build Output

SWAB produces an unsigned `.app` file in a ZIP archive. This must be signed using Xcode.

### Code Signing Process

1. **Open Xcode**

2. **Open the iOS project:**
   ```
   builds/{build_id}/ios/Runner.xcworkspace
   ```

3. **Configure signing:**
   - Select the Runner project
   - Go to "Signing & Capabilities"
   - Select your Team
   - Enable "Automatically manage signing"

4. **Build for release:**
   - Product → Archive
   - Wait for archive to complete
   - Click "Distribute App"

### Distribution Options

| Method | Audience | Requirements |
|--------|----------|--------------|
| App Store | Public | Apple Developer ($99/year) |
| TestFlight | Beta testers | Apple Developer ($99/year) |
| Ad Hoc | Up to 100 devices | Apple Developer ($99/year) |
| Enterprise | Organization | Apple Enterprise ($299/year) |

### App Store Upload

1. Archive the app in Xcode
2. Click "Distribute App"
3. Select "App Store Connect"
4. Upload to App Store Connect
5. Complete app metadata in App Store Connect
6. Submit for review

### Troubleshooting

**"No signing certificate"**
- Xcode → Preferences → Accounts → Manage Certificates
- Click + and create a new certificate

**CocoaPods issues**
```bash
cd ios
pod deintegrate
pod install
```

**Minimum deployment target**
SWAB sets iOS 12.0 as minimum. For newer features, edit:
```
ios/Podfile
```

---

## macOS

### Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| macOS | 10.15+ | Required |
| Xcode | 14.0+ | For toolchain |
| Flutter | 3.0+ | With macOS support |

### Setup Verification

```bash
flutter config --enable-macos-desktop
flutter doctor
```

### Build Output

- `MyApp.app` bundled in a ZIP file
- Ready to run on macOS
- Not signed or notarized

### Code Signing and Notarization

For distribution outside the Mac App Store:

1. **Sign the app:**
   ```bash
   codesign --deep --force --verify --verbose \
     --sign "Developer ID Application: Your Name" \
     MyApp.app
   ```

2. **Create a ZIP:**
   ```bash
   ditto -c -k --keepParent MyApp.app MyApp.zip
   ```

3. **Submit for notarization:**
   ```bash
   xcrun notarytool submit MyApp.zip \
     --apple-id "your@email.com" \
     --password "app-specific-password" \
     --team-id "TEAMID"
   ```

4. **Staple the notarization:**
   ```bash
   xcrun stapler staple MyApp.app
   ```

### Mac App Store

1. Open the project in Xcode
2. Configure App Sandbox entitlements
3. Archive and upload to App Store Connect

### Troubleshooting

**"App is damaged and can't be opened"**
The app is not signed. Right-click → Open, or sign the app.

**Permission denied**
```bash
chmod +x MyApp.app/Contents/MacOS/*
```

---

## Windows

### Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| Windows | 10/11 | 64-bit required |
| Visual Studio | 2019+ | With C++ workload |
| Windows SDK | 10.0.17763.0+ | Via Visual Studio |
| Flutter | 3.0+ | With Windows support |

### Visual Studio Setup

1. Download [Visual Studio](https://visualstudio.microsoft.com/)
2. Run installer
3. Select "Desktop development with C++"
4. Ensure Windows 10 SDK is checked
5. Install

### Setup Verification

```bash
flutter config --enable-windows-desktop
flutter doctor
```

### Build Output

- Executable bundled in a ZIP file
- Contains all DLL dependencies
- Ready to run

### Creating an Installer

Use [Inno Setup](https://jrsoftware.org/isinfo.php) to create an installer:

```iss
[Setup]
AppName=My App
AppVersion=1.0.0
DefaultDirName={pf}\MyApp
OutputBaseFilename=MyApp-Setup

[Files]
Source: "build\windows\runner\Release\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{commonprograms}\My App"; Filename: "{app}\myapp.exe"
```

### Microsoft Store

For Microsoft Store distribution:
1. Create MSIX package using Flutter's build tools
2. Register as Microsoft Partner
3. Upload to Partner Center

### Troubleshooting

**"VCRUNTIME140.dll not found"**
Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

**Build fails with CMake error**
Ensure CMake is installed and in PATH:
```powershell
winget install Kitware.CMake
```

---

## Linux

### Requirements

| Component | Version | Installation |
|-----------|---------|--------------|
| Linux | Any modern distro | - |
| Clang | Latest | `sudo apt install clang` |
| CMake | 3.10+ | `sudo apt install cmake` |
| GTK 3 | 3.22+ | `sudo apt install libgtk-3-dev` |
| Ninja | Latest | `sudo apt install ninja-build` |
| pkg-config | Latest | `sudo apt install pkg-config` |

### Ubuntu/Debian Setup

```bash
sudo apt update
sudo apt install clang cmake ninja-build pkg-config libgtk-3-dev
```

### Fedora Setup

```bash
sudo dnf install clang cmake ninja-build gtk3-devel
```

### Arch Linux Setup

```bash
sudo pacman -S clang cmake ninja gtk3
```

### Setup Verification

```bash
flutter config --enable-linux-desktop
flutter doctor
```

### Build Output

- Binary bundled in a ZIP file
- Includes shared libraries
- Bundle contains `lib/` and `data/` directories

### Creating Packages

#### Debian Package (.deb)

Use [flutter_to_debian](https://pub.dev/packages/flutter_to_debian) package.

#### AppImage

```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure and package
```

#### Snap

Create `snap/snapcraft.yaml`:
```yaml
name: myapp
version: '1.0.0'
summary: My App
description: A web app converted to native

parts:
  myapp:
    plugin: dump
    source: build/linux/x64/release/bundle
```

### Troubleshooting

**"libgtk-3.so.0 not found"**
```bash
sudo apt install libgtk-3-0
```

**Font rendering issues**
```bash
sudo apt install fonts-noto
```

---

## Cross-Platform Building

### Build Matrix

| Host OS | Android | iOS | macOS | Windows | Linux |
|---------|---------|-----|-------|---------|-------|
| macOS | ✅ | ✅ | ✅ | ❌ | ❌ |
| Windows | ✅ | ❌ | ❌ | ✅ | ❌ |
| Linux | ✅ | ❌ | ❌ | ❌ | ✅ |

### CI/CD Integration

For automated builds across all platforms, consider:

- **GitHub Actions** - Use matrix builds with macOS, Windows, Linux runners
- **Codemagic** - Flutter-focused CI/CD with all platforms
- **Bitrise** - Mobile-focused with good Flutter support

### Example GitHub Actions Workflow

```yaml
name: Build Apps

on: [push]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter build apk

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter build ios --no-codesign

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter build windows
```

---

## Next Steps

- [[Configuration Guide]] - Detailed configuration options
- [[API Reference]] - Programmatic build access
- [[Troubleshooting]] - Common issues and solutions
