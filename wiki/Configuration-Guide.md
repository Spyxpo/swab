# Configuration Guide

This guide covers all configuration options available in SWAB.

---

## Table of Contents

- [App Configuration](#app-configuration)
- [WebView Settings](#webview-settings)
- [Android Signing Configuration](#android-signing-configuration)
- [Platform-Specific Settings](#platform-specific-settings)
- [Server Configuration](#server-configuration)

---

## App Configuration

### Basic Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| App Name | String | Yes | The display name shown under the app icon |
| Description | String | No | Brief description of the app |
| Version | String | Yes | Semantic version (e.g., `1.0.0`) |
| Build Number | Integer | Yes | Incremental build number for updates |
| Package Name | String | Yes | Unique identifier (reverse domain notation) |
| Web URL | URL | Yes | The website URL to convert |
| App Icon | Image | No | App icon (1024x1024px recommended) |

### App Name Guidelines

- Keep it short (max 30 characters recommended)
- Avoid special characters that may cause issues on some platforms
- This name appears on home screens and app stores

### Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH`

| Component | When to Increment | Example |
|-----------|-------------------|---------|
| MAJOR | Breaking changes | 1.0.0 → 2.0.0 |
| MINOR | New features | 1.0.0 → 1.1.0 |
| PATCH | Bug fixes | 1.0.0 → 1.0.1 |

### Build Number

- Must be an integer
- Must increment with each release
- Used by app stores to identify newer versions
- Example progression: 1, 2, 3, 4...

### Package Name Format

The package name (also called Bundle ID on iOS) must:
- Use reverse domain notation
- Contain only lowercase letters, numbers, and dots
- Not start or end with a dot
- Be unique across all app stores

**Valid Examples:**
```
com.example.myapp
com.company.appname
io.mysite.webapp
```

**Invalid Examples:**
```
MyApp              # No domain format
com.example.My-App # No hyphens or uppercase
.com.example.app   # Can't start with dot
```

---

## WebView Settings

Access these settings by clicking the "WebView Settings" button in the interface.

### JavaScript

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable JavaScript** | `true` | Allow JavaScript execution in WebView |

**When to disable:**
- Static websites with no interactivity
- Security-sensitive applications
- When you want to reduce resource usage

### Zoom Control

| Setting | Default | Description |
|---------|---------|-------------|
| **Allow Zoom** | `false` | Enable pinch-to-zoom functionality |

**When to enable:**
- Content-heavy websites
- Websites with small text
- Accessibility requirements

### DOM Storage

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable DOM Storage** | `true` | Allow localStorage and sessionStorage |

**When to disable:**
- Privacy-focused applications
- When you don't need persistent data

### Geolocation

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable Geolocation** | `false` | Allow location access requests |

**When to enable:**
- Maps and navigation apps
- Location-based services
- Store finders

**Note:** Users will still be prompted to grant permission.

### Pull to Refresh

| Setting | Default | Description |
|---------|---------|-------------|
| **Pull to Refresh** | `true` | Swipe down gesture to refresh page |

**When to disable:**
- Apps with custom swipe gestures
- Single-page applications with internal refresh
- Games or interactive content

### Navigation Bar

| Setting | Default | Description |
|---------|---------|-------------|
| **Show Navigation Bar** | `false` | Display back/forward/refresh controls |

**When to enable:**
- Multi-page websites
- When users need to navigate history
- Complex web applications

### File Access

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable File Access** | `false` | Allow file uploads and downloads |

**When to enable:**
- Apps with file upload forms
- Document management systems
- Social media apps

### Cache

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable Cache** | `true` | Cache content for offline access |

**When to disable:**
- Real-time data applications
- When you always need fresh content
- Sensitive financial data

### Media Autoplay

| Setting | Default | Description |
|---------|---------|-------------|
| **Media Autoplay** | `false` | Auto-play videos and audio |

**When to enable:**
- Video streaming apps
- Music players
- Interactive experiences

**Note:** Some platforms may still require user interaction for audio.

---

## Android Signing Configuration

### Keystore Overview

A keystore is required to sign Android applications. You have two options:

1. **Auto-generated Keystore** - SWAB creates a debug keystore automatically
2. **Custom Keystore** - Use your own production keystore

### Auto-generated Keystore

When no keystore is provided:
- SWAB generates a keystore using Java's `keytool`
- Suitable for testing and development
- Not recommended for production releases

### Custom Keystore Configuration

| Field | Description |
|-------|-------------|
| Keystore File | Your `.jks` or `.keystore` file |
| Keystore Password | Password for the keystore |
| Key Alias | Alias of the signing key |
| Key Password | Password for the specific key |

### Creating a Production Keystore

```bash
keytool -genkey -v \
  -keystore my-release-key.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias my-key-alias
```

You'll be prompted for:
- Keystore password
- Key password
- Your name and organization details

### Keystore Best Practices

1. **Never lose your keystore** - You cannot update apps without the original keystore
2. **Store passwords securely** - Use a password manager
3. **Backup your keystore** - Keep copies in secure locations
4. **Use strong passwords** - Minimum 8 characters, mixed case, numbers, symbols
5. **Different passwords** - Use different passwords for keystore and key

---

## Platform-Specific Settings

### Android

| Setting | Location | Description |
|---------|----------|-------------|
| Min SDK | auto | Minimum Android API level (21) |
| Target SDK | auto | Target Android API level (latest) |
| Permissions | AndroidManifest.xml | Automatically configured |

### iOS

| Setting | Location | Description |
|---------|----------|-------------|
| Bundle ID | Info.plist | Set from Package Name |
| Deployment Target | auto | Minimum iOS version (12.0) |
| Code Signing | Manual | Requires Xcode configuration |

### macOS

| Setting | Location | Description |
|---------|----------|-------------|
| Bundle Name | Info.plist | Set from App Name |
| Deployment Target | auto | Minimum macOS version (10.14) |

### Windows

| Setting | Location | Description |
|---------|----------|-------------|
| App Name | CMakeLists.txt | Set from App Name |
| Version | auto | Set from Version field |

### Linux

| Setting | Location | Description |
|---------|----------|-------------|
| Binary Name | CMakeLists.txt | Set from App Name |
| Version | auto | Set from Version field |

---

## Server Configuration

### Flask Configuration

Located in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['BUILD_FOLDER'] = './builds'
app.config['FLUTTER_TEMPLATE'] = './templates/webview_app'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `SECRET_KEY` | `swab-secret-key...` | Flask session encryption key |
| `UPLOAD_FOLDER` | `./uploads` | Directory for uploaded files |
| `BUILD_FOLDER` | `./builds` | Directory for build outputs |
| `FLUTTER_TEMPLATE` | `./templates/webview_app` | Flutter template location |
| `MAX_CONTENT_LENGTH` | 50MB | Maximum upload file size |

### Production Configuration

For production deployment, update:

```python
# Use environment variable for secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')

# Disable debug mode
app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## Environment Variables

You can configure SWAB using environment variables:

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET_KEY` | Override Flask secret key |
| `SWAB_UPLOAD_DIR` | Custom upload directory |
| `SWAB_BUILD_DIR` | Custom build directory |

---

## Next Steps

- [[Platform Build Guide]] - Detailed platform-specific instructions
- [[API Reference]] - REST API documentation
- [[Troubleshooting]] - Common configuration issues
