# Frequently Asked Questions

Find answers to common questions about SWAB.

---

## General Questions

### What is SWAB?

**SWAB** (Spyxpo Web to App Builder) is a tool that converts any website into native mobile and desktop applications. It uses Flutter's WebView to wrap your website in a native app container, providing a seamless app experience without rewriting your website.

---

### Is SWAB free to use?

Yes, SWAB is open source and free to use. However, you may need paid developer accounts to publish apps:
- Google Play Store: $25 one-time fee
- Apple App Store: $99/year
- Microsoft Store: One-time registration fee

---

### Do I need coding experience?

No coding is required to use SWAB. The web interface guides you through the entire process. You only need to:
1. Enter your website URL
2. Configure basic app settings
3. Click build

---

### What websites work with SWAB?

Most websites work with SWAB, including:
- ✅ Static websites
- ✅ Single-page applications (React, Vue, Angular)
- ✅ WordPress sites
- ✅ E-commerce platforms
- ✅ Web applications

**Websites that may have issues:**
- ⚠️ Sites that block WebView user agents
- ⚠️ Sites with strict CORS policies
- ⚠️ Sites requiring specific browser features
- ⚠️ Sites with aggressive iframe protection

---

### Can I convert someone else's website?

Technically yes, but you should have permission or legal rights to do so. Converting a website you don't own may violate:
- Copyright laws
- Terms of service
- Trademark rights

Always ensure you have proper authorization.

---

## Build Questions

### How long does a build take?

Build times vary by platform and system:

| Platform | Typical Time | First Build |
|----------|--------------|-------------|
| Android APK | 2-4 minutes | 5-10 minutes |
| Android AAB | 2-4 minutes | 5-10 minutes |
| iOS | 3-5 minutes | 10-15 minutes |
| macOS | 2-3 minutes | 5-8 minutes |
| Windows | 2-3 minutes | 5-8 minutes |
| Linux | 1-2 minutes | 3-5 minutes |

First builds are slower because Flutter downloads dependencies.

---

### Can I build for all platforms at once?

You can select multiple platforms, and SWAB will build them sequentially. However:
- iOS and macOS require a Mac
- Windows builds require Windows
- Linux builds require Linux

For all platforms, you need multiple machines or a CI/CD system.

---

### Why is my build failing?

Common reasons:
1. **Missing SDK** - Platform tools not installed
2. **Invalid package name** - Use `com.example.app` format
3. **Network issues** - Flutter can't download dependencies
4. **Disk space** - Not enough storage

See [[Troubleshooting]] for detailed solutions.

---

### Where are build outputs stored?

Build outputs are stored in the `builds/` directory:
```
builds/
└── {build_id}/
    ├── android/
    │   └── app-release.apk
    ├── ios/
    │   └── Runner.app.zip
    └── ...
```

---

### Can I customize the app beyond WebView settings?

Yes, advanced users can modify the Flutter template in `templates/webview_app/`:
- `lib/main.dart` - Main app logic
- `pubspec.yaml` - Dependencies
- Platform-specific folders for native code

Changes to the template affect all future builds.

---

## Platform Questions

### Can I build iOS apps on Windows/Linux?

No. iOS and macOS apps can only be built on macOS due to Apple's requirements. Options:
- Use a Mac (physical or virtual)
- Use a cloud CI/CD service like Codemagic or GitHub Actions with macOS runners
- Rent a Mac in the cloud (MacStadium, MacinCloud)

---

### What Android versions are supported?

SWAB builds apps supporting:
- **Minimum**: Android 5.0 (API 21)
- **Target**: Latest stable Android version

This covers 95%+ of active Android devices.

---

### What iOS versions are supported?

SWAB builds apps supporting:
- **Minimum**: iOS 12.0
- **Target**: Latest stable iOS version

This covers most active iOS devices.

---

### Do the apps work offline?

Partially. If caching is enabled:
- Previously loaded pages may be available offline
- New content requires internet
- The app shows an offline indicator

For full offline support, your website should implement a service worker (PWA).

---

### Can I submit to app stores?

Yes! SWAB produces store-ready outputs:
- **Google Play**: Upload the AAB file
- **Apple App Store**: Sign in Xcode, then upload
- **Microsoft Store**: Create MSIX package
- **Linux Stores**: Create Snap or Flatpak

---

## Feature Questions

### Can I add push notifications?

Not currently built-in. Push notifications require:
1. Backend server for sending notifications
2. Platform-specific configuration (FCM, APNs)
3. Custom Flutter code

This is planned for a future release.

---

### Can I access device features (camera, contacts)?

The WebView can access:
- ✅ Camera (via HTML5 API)
- ✅ Geolocation (if enabled)
- ✅ File uploads (if enabled)
- ✅ Local storage

For deeper integration, you'd need to modify the Flutter template.

---

### Can I customize the splash screen?

The splash screen uses your app icon. For a custom splash:
1. Modify `android/app/src/main/res/drawable/launch_background.xml`
2. Modify `ios/Runner/Assets.xcassets/LaunchImage.imageset/`

---

### Can I add a custom user agent?

Yes, by modifying `lib/main.dart` in the template:
```dart
initialSettings: InAppWebViewSettings(
  userAgent: 'Your Custom User Agent',
  // ... other settings
),
```

---

### Does it support multiple URLs/pages?

Yes, the WebView supports full navigation. Users can:
- Click links to navigate
- Use back/forward (if navigation bar enabled)
- Access any page on the same domain

For different domains, you may need to configure allowed URLs.

---

## Security Questions

### Is my website data secure?

SWAB:
- ✅ Uses HTTPS by default (if your site supports it)
- ✅ Encrypts project files with machine-specific keys
- ✅ Doesn't store your data on external servers
- ✅ Runs entirely on your local machine

---

### Are project files transferable?

No. Project files (`.swab`) are encrypted with a machine-specific key and can only be opened on the same computer where they were created. This prevents unauthorized access if the file is shared.

---

### How is my keystore protected?

When saved in a project:
- Keystore is encrypted with AES-256
- Machine-specific encryption key
- PBKDF2 key derivation with 480,000 iterations

Never share your `.swab` files or raw keystore files.

---

## Technical Questions

### What technologies does SWAB use?

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask 3.0+ |
| Frontend | HTML5, CSS3, JavaScript |
| App Framework | Flutter (Dart) |
| WebView | flutter_inappwebview |
| Encryption | Cryptography library (Fernet) |

---

### Can I use SWAB as a service (API only)?

Yes! SWAB provides a REST API. See [[API Reference]] for:
- Starting builds programmatically
- Checking build status
- Downloading artifacts

---

### What's the difference between APK and AAB?

| Feature | APK | AAB |
|---------|-----|-----|
| File size | Larger | Optimized per device |
| Installation | Direct install | Via Play Store |
| Store required | No | Yes (Play Store) |
| Updates | Manual | Automatic |

Use APK for testing, AAB for Play Store.

---

### Can I run SWAB in Docker?

Not officially supported, but possible with:
1. A Docker image with Python, Flutter, and platform SDKs
2. Volume mounts for builds and uploads
3. Port exposure for the web interface

Android builds work; iOS builds still require macOS.

---

### How do I update SWAB?

```bash
cd swab
git pull origin stable
pip install -r requirements.txt
```

Your projects and settings are preserved.

---

## Getting Help

### Where can I report bugs?

Open an issue on GitHub:
- [GitHub Issues](https://github.com/user/swab/issues)

Include:
- Operating system
- Python and Flutter versions
- Complete error message
- Steps to reproduce

---

### Can I contribute to SWAB?

Yes! Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See the repository for contribution guidelines.

---

### Is there a community?

- **GitHub Discussions**: For questions and ideas
- **Issues**: For bug reports and feature requests

---

## Next Steps

- [[Getting Started]] - Installation and first steps
- [[Configuration Guide]] - Detailed settings
- [[Troubleshooting]] - Problem solving
- [[Home]] - Documentation home
