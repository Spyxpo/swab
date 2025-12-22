# Troubleshooting

This guide helps you resolve common issues when using SWAB.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Build Errors](#build-errors)
- [Platform-Specific Issues](#platform-specific-issues)
- [WebView Issues](#webview-issues)
- [Project File Issues](#project-file-issues)
- [Server Issues](#server-issues)

---

## Installation Issues

### Python Version Error

**Symptom:**
```
SyntaxError: invalid syntax
```
or
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**

Ensure you're using Python 3.8 or higher:
```bash
python3 --version
```

If needed, install a newer version:
```bash
# macOS
brew install python@3.11

# Ubuntu
sudo apt install python3.11

# Windows
winget install Python.Python.3.11
```

---

### Flask Installation Failed

**Symptom:**
```
ERROR: Could not install packages due to an OSError
```

**Solution:**

1. Upgrade pip:
   ```bash
   python3 -m pip install --upgrade pip
   ```

2. Try with user flag:
   ```bash
   pip install --user -r requirements.txt
   ```

3. Or use virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

### Flutter Not Found

**Symptom:**
```
flutter: command not found
```

**Solution:**

1. Verify Flutter is installed:
   ```bash
   which flutter
   ```

2. Add Flutter to PATH:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$PATH:/path/to/flutter/bin"
   ```

3. Restart terminal and verify:
   ```bash
   flutter doctor
   ```

---

## Build Errors

### Build Stuck at 0%

**Symptom:**
Progress bar stays at 0%, no status updates.

**Possible Causes:**
1. Flutter not in PATH
2. Missing platform tools
3. Server error

**Solution:**

1. Check server logs in terminal
2. Verify Flutter works:
   ```bash
   flutter doctor -v
   ```
3. Try a test build manually:
   ```bash
   cd templates/webview_app
   flutter pub get
   flutter build apk
   ```

---

### "Package name is invalid"

**Symptom:**
```
Error: Invalid package name format
```

**Solution:**

Use proper reverse domain notation:
- ✅ `com.example.myapp`
- ✅ `io.company.appname`
- ❌ `MyApp`
- ❌ `com.example.My-App` (no hyphens)
- ❌ `com.example.123app` (can't start with number)

---

### "Could not find pubspec.yaml"

**Symptom:**
```
Error: Could not find a file named "pubspec.yaml"
```

**Solution:**

The Flutter template is missing or corrupted:

1. Check template exists:
   ```bash
   ls templates/webview_app/pubspec.yaml
   ```

2. If missing, re-clone repository:
   ```bash
   git checkout templates/webview_app
   ```

---

### Build Timeout

**Symptom:**
Build stops after a long time with no output.

**Solution:**

1. Increase timeout in `app.py`:
   ```python
   # Find the subprocess call and increase timeout
   timeout=600  # 10 minutes
   ```

2. Run Flutter pub get beforehand:
   ```bash
   cd templates/webview_app
   flutter pub get
   ```

3. Check network connection (Flutter downloads dependencies)

---

### Out of Disk Space

**Symptom:**
```
No space left on device
```

**Solution:**

1. Clear old builds:
   ```bash
   rm -rf builds/*
   ```

2. Clear Flutter cache:
   ```bash
   flutter clean
   rm -rf ~/.pub-cache
   ```

3. Clear Gradle cache (Android):
   ```bash
   rm -rf ~/.gradle/caches
   ```

---

## Platform-Specific Issues

### Android: "SDK not found"

**Symptom:**
```
Android SDK not found
```

**Solution:**

1. Set ANDROID_HOME:
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
   ```

2. Or configure Flutter:
   ```bash
   flutter config --android-sdk /path/to/sdk
   ```

---

### Android: "License not accepted"

**Symptom:**
```
Android license status unknown
```

**Solution:**

```bash
flutter doctor --android-licenses
```

Press `y` to accept all licenses.

---

### Android: Keystore Generation Failed

**Symptom:**
```
keytool error: java.lang.Exception
```

**Solution:**

1. Verify Java is installed:
   ```bash
   java -version
   keytool -help
   ```

2. If not, install JDK:
   ```bash
   # macOS
   brew install openjdk@11

   # Ubuntu
   sudo apt install openjdk-11-jdk
   ```

---

### iOS: "Xcode not installed"

**Symptom:**
```
Xcode installation is incomplete
```

**Solution:**

1. Install Xcode from App Store
2. Accept license:
   ```bash
   sudo xcodebuild -license accept
   ```
3. Install command line tools:
   ```bash
   xcode-select --install
   ```

---

### iOS: CocoaPods Error

**Symptom:**
```
CocoaPods not installed
```

**Solution:**

```bash
sudo gem install cocoapods
cd ios
pod install
```

If Ruby issues:
```bash
brew install cocoapods
```

---

### Windows: Visual Studio Error

**Symptom:**
```
Unable to find Visual Studio
```

**Solution:**

1. Install Visual Studio with C++ workload
2. Or install Build Tools only:
   - Download [Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"

---

### Linux: Missing Libraries

**Symptom:**
```
Package libgtk-3-dev was not found
```

**Solution:**

Install required packages:
```bash
# Ubuntu/Debian
sudo apt install clang cmake ninja-build pkg-config libgtk-3-dev

# Fedora
sudo dnf install clang cmake ninja-build gtk3-devel

# Arch
sudo pacman -S clang cmake ninja gtk3
```

---

## WebView Issues

### Website Not Loading

**Symptom:**
Blank screen or loading forever in the app.

**Possible Causes:**

1. **HTTPS required** - Some sites require HTTPS
2. **CORS issues** - Website blocks iframe/webview
3. **Network issues** - No internet connection

**Solution:**

1. Test URL in browser first
2. Check if site works in WebView:
   - Some sites block WebView user agents
   - Contact site owner if you control the website
3. Enable cache for offline access

---

### JavaScript Not Working

**Symptom:**
Interactive features don't work.

**Solution:**

Ensure JavaScript is enabled in WebView settings:
- `enable_javascript: true`

---

### Geolocation Not Working

**Symptom:**
Location requests fail.

**Solution:**

1. Enable geolocation in WebView settings
2. Ensure app has location permissions
3. User must grant permission when prompted

---

### Pull to Refresh Not Working

**Symptom:**
Swipe down doesn't refresh.

**Solution:**

1. Enable in WebView settings:
   - `pull_to_refresh: true`
2. Some websites intercept scroll events - disable if conflicting

---

## Project File Issues

### "Cannot open project file"

**Symptom:**
```
This project file was created on a different machine
```

**Cause:**
SWAB project files are encrypted with machine-specific keys.

**Solution:**

Project files cannot be transferred between machines. You must:
1. Recreate the project on the new machine
2. Or export/import settings manually (not the .swab file)

---

### "Corrupted project file"

**Symptom:**
```
Error decrypting project file
```

**Solution:**

The file may be corrupted:
1. Check file wasn't modified
2. Try redownloading from backup
3. Recreate project if necessary

---

## Server Issues

### Port Already in Use

**Symptom:**
```
Address already in use
```

**Solution:**

1. Kill the existing process:
   ```bash
   # Find process
   lsof -i :5000

   # Kill it
   kill -9 <PID>
   ```

2. Or use a different port:
   ```python
   app.run(port=5001)
   ```

---

### CORS Errors (API Access)

**Symptom:**
```
Access-Control-Allow-Origin
```

**Solution:**

If accessing API from another domain, add CORS headers:

```python
from flask_cors import CORS
CORS(app)
```

---

### Upload Size Limit

**Symptom:**
```
Request Entity Too Large
```

**Solution:**

Increase the limit in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

---

### Memory Issues

**Symptom:**
Server crashes during build.

**Solution:**

1. Close other applications
2. Increase swap space (Linux):
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

---

## Getting More Help

### Debug Mode

Run with verbose output:
```bash
FLASK_DEBUG=1 python app.py
```

### Check Logs

Look for errors in terminal output where SWAB is running.

### Flutter Verbose

Test Flutter directly:
```bash
flutter build apk -v
```

### Report Issues

If you can't resolve the issue:
1. Search [existing issues](https://github.com/user/swab/issues)
2. Create a new issue with:
   - Operating system and version
   - Python and Flutter versions
   - Complete error message
   - Steps to reproduce

---

## Next Steps

- [[FAQ]] - Frequently asked questions
- [[Platform Build Guide]] - Platform-specific details
- [[Home]] - Back to documentation home
