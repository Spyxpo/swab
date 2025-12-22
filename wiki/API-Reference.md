# API Reference

SWAB provides a RESTful API for programmatic access to all functionality. This document covers all available endpoints.

---

## Table of Contents

- [Overview](#overview)
- [Build Endpoints](#build-endpoints)
- [Upload Endpoints](#upload-endpoints)
- [Project Endpoints](#project-endpoints)
- [Error Handling](#error-handling)

---

## Overview

### Base URL

```
http://localhost:5000/api
```

### Content Types

| Endpoint Type | Request | Response |
|---------------|---------|----------|
| Build/Project | `application/json` | `application/json` |
| File Upload | `multipart/form-data` | `application/json` |
| File Download | - | `application/octet-stream` |

### Authentication

Currently, SWAB does not require authentication. For production deployments, consider implementing authentication middleware.

---

## Build Endpoints

### Start a Build

Creates a new build job for the specified platforms.

```http
POST /api/build
Content-Type: application/json
```

#### Request Body

```json
{
  "app_name": "My App",
  "app_description": "A description of my app",
  "app_version": "1.0.0",
  "build_number": "1",
  "package_name": "com.example.myapp",
  "web_url": "https://example.com",
  "icon_path": "/path/to/icon.png",
  "webview_settings": {
    "allow_zoom": false,
    "enable_javascript": true,
    "enable_dom_storage": true,
    "enable_geolocation": false,
    "pull_to_refresh": true,
    "show_navigation_bar": false,
    "enable_file_access": false,
    "enable_cache": true,
    "media_autoplay": false
  },
  "platforms": ["android", "android_aab", "ios", "macos", "windows", "linux"],
  "keystore_path": "/path/to/keystore.jks",
  "keystore_password": "password",
  "key_alias": "alias",
  "key_password": "keypassword"
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app_name` | string | Yes | Display name for the app |
| `app_description` | string | No | Brief description |
| `app_version` | string | Yes | Semantic version (X.Y.Z) |
| `build_number` | string | Yes | Integer build number |
| `package_name` | string | Yes | Package identifier |
| `web_url` | string | Yes | Website URL to convert |
| `icon_path` | string | No | Path to uploaded icon |
| `webview_settings` | object | No | WebView configuration |
| `platforms` | array | Yes | Target platforms |
| `keystore_path` | string | No | Path to uploaded keystore |
| `keystore_password` | string | No | Keystore password |
| `key_alias` | string | No | Key alias in keystore |
| `key_password` | string | No | Key password |

#### WebView Settings Object

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `allow_zoom` | boolean | false | Enable pinch-to-zoom |
| `enable_javascript` | boolean | true | Execute JavaScript |
| `enable_dom_storage` | boolean | true | Enable localStorage |
| `enable_geolocation` | boolean | false | Allow location access |
| `pull_to_refresh` | boolean | true | Swipe to refresh |
| `show_navigation_bar` | boolean | false | Show nav controls |
| `enable_file_access` | boolean | false | Allow file access |
| `enable_cache` | boolean | true | Cache content |
| `media_autoplay` | boolean | false | Auto-play media |

#### Platforms Array

Valid values:
- `android` - Android APK
- `android_aab` - Android App Bundle
- `ios` - iOS application
- `macos` - macOS application
- `windows` - Windows executable
- `linux` - Linux binary

#### Response

```json
{
  "build_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Example

```bash
curl -X POST http://localhost:5000/api/build \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "My App",
    "app_version": "1.0.0",
    "build_number": "1",
    "package_name": "com.example.myapp",
    "web_url": "https://example.com",
    "platforms": ["android"]
  }'
```

---

### Get Build Status

Check the progress of a build job.

```http
GET /api/build/{build_id}/status
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `build_id` | string | UUID of the build |

#### Response

```json
{
  "status": "building",
  "progress": 45,
  "message": "Building Android APK...",
  "platforms": {
    "android": {
      "status": "building",
      "progress": 90
    },
    "ios": {
      "status": "pending",
      "progress": 0
    }
  }
}
```

#### Status Values

| Status | Description |
|--------|-------------|
| `pending` | Build not yet started |
| `building` | Build in progress |
| `completed` | Build finished successfully |
| `error` | Build failed |

#### Example

```bash
curl http://localhost:5000/api/build/550e8400-e29b-41d4-a716-446655440000/status
```

---

### Download Build Artifact

Download the built application for a specific platform.

```http
GET /api/build/{build_id}/download/{platform}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `build_id` | string | UUID of the build |
| `platform` | string | Target platform |

#### Platform Values

| Value | Output |
|-------|--------|
| `android` | APK file |
| `android_aab` | AAB file |
| `ios` | ZIP with .app |
| `macos` | ZIP with .app |
| `windows` | ZIP with .exe |
| `linux` | ZIP with binary |
| `keystore` | Generated keystore |

#### Response

Binary file download with appropriate headers:
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="MyApp-android.apk"
```

#### Example

```bash
curl -O http://localhost:5000/api/build/550e8400-e29b-41d4-a716-446655440000/download/android
```

---

## Upload Endpoints

### Upload App Icon

Upload an icon image for the application.

```http
POST /api/upload/icon
Content-Type: multipart/form-data
```

#### Form Data

| Field | Type | Description |
|-------|------|-------------|
| `file` | file | Image file (PNG, JPG) |

#### Response

```json
{
  "success": true,
  "path": "/uploads/icons/icon_abc123.png"
}
```

#### Example

```bash
curl -X POST http://localhost:5000/api/upload/icon \
  -F "file=@/path/to/icon.png"
```

---

### Upload Keystore

Upload an Android keystore file.

```http
POST /api/upload/keystore
Content-Type: multipart/form-data
```

#### Form Data

| Field | Type | Description |
|-------|------|-------------|
| `file` | file | Keystore file (.jks, .keystore) |

#### Response

```json
{
  "success": true,
  "path": "/uploads/keystores/keystore_xyz789.jks"
}
```

#### Example

```bash
curl -X POST http://localhost:5000/api/upload/keystore \
  -F "file=@/path/to/release.jks"
```

---

## Project Endpoints

### Save Project

Save the current project configuration as an encrypted `.swab` file.

```http
POST /api/project/save
Content-Type: application/json
```

#### Request Body

Complete project configuration (same as build request, with additional metadata).

```json
{
  "app_name": "My App",
  "app_description": "A description",
  "app_version": "1.0.0",
  "build_number": "1",
  "package_name": "com.example.myapp",
  "web_url": "https://example.com",
  "webview_settings": { ... },
  "icon_data": "base64-encoded-icon-data",
  "keystore_data": "base64-encoded-keystore-data",
  "keystore_password": "encrypted-password",
  "key_alias": "alias",
  "key_password": "encrypted-key-password"
}
```

#### Response

Binary download of encrypted `.swab` file:
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="My App.swab"
```

#### Example

```bash
curl -X POST http://localhost:5000/api/project/save \
  -H "Content-Type: application/json" \
  -d '{"app_name": "My App", ...}' \
  -o "My App.swab"
```

---

### Open Project

Load a previously saved project file.

```http
POST /api/project/open
Content-Type: multipart/form-data
```

#### Form Data

| Field | Type | Description |
|-------|------|-------------|
| `file` | file | SWAB project file (.swab) |

#### Response

```json
{
  "project": {
    "app_name": "My App",
    "app_description": "A description",
    "app_version": "1.0.0",
    "build_number": "1",
    "package_name": "com.example.myapp",
    "web_url": "https://example.com",
    "webview_settings": { ... },
    "icon_path": "/uploads/restored_icon.png",
    "keystore_path": "/uploads/restored_keystore.jks"
  }
}
```

#### Error Response

```json
{
  "error": "This project file was created on a different machine and cannot be opened here."
}
```

#### Example

```bash
curl -X POST http://localhost:5000/api/project/open \
  -F "file=@My App.swab"
```

---

## Error Handling

### Error Response Format

All errors return a JSON response with an `error` field:

```json
{
  "error": "Description of what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 413 | Payload Too Large - File exceeds limit |
| 500 | Internal Server Error |

### Common Errors

#### Invalid Package Name
```json
{
  "error": "Invalid package name format. Use reverse domain notation (e.g., com.example.app)"
}
```

#### Build Not Found
```json
{
  "error": "Build not found"
}
```

#### Platform Not Available
```json
{
  "error": "Platform 'ios' is not available on this system"
}
```

#### File Too Large
```json
{
  "error": "File size exceeds maximum limit of 50MB"
}
```

#### Machine Mismatch (Project Files)
```json
{
  "error": "This project file was created on a different machine and cannot be opened here."
}
```

---

## Rate Limiting

Currently, SWAB does not implement rate limiting. For production deployments, consider adding rate limiting middleware.

---

## Webhooks (Future)

Webhook support for build completion notifications is planned for future releases.

---

## SDK Examples

### Python

```python
import requests

# Start a build
response = requests.post('http://localhost:5000/api/build', json={
    'app_name': 'My App',
    'app_version': '1.0.0',
    'build_number': '1',
    'package_name': 'com.example.myapp',
    'web_url': 'https://example.com',
    'platforms': ['android']
})

build_id = response.json()['build_id']

# Check status
status = requests.get(f'http://localhost:5000/api/build/{build_id}/status')
print(status.json())

# Download when complete
if status.json()['status'] == 'completed':
    apk = requests.get(f'http://localhost:5000/api/build/{build_id}/download/android')
    with open('app.apk', 'wb') as f:
        f.write(apk.content)
```

### JavaScript

```javascript
// Start a build
const response = await fetch('http://localhost:5000/api/build', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    app_name: 'My App',
    app_version: '1.0.0',
    build_number: '1',
    package_name: 'com.example.myapp',
    web_url: 'https://example.com',
    platforms: ['android']
  })
});

const { build_id } = await response.json();

// Poll for status
const checkStatus = async () => {
  const status = await fetch(`http://localhost:5000/api/build/${build_id}/status`);
  return status.json();
};

// Download when complete
const downloadApk = async () => {
  const blob = await fetch(`http://localhost:5000/api/build/${build_id}/download/android`).then(r => r.blob());
  // Handle download...
};
```

---

## Next Steps

- [[Platform Build Guide]] - Platform-specific details
- [[Troubleshooting]] - API troubleshooting
- [[Home]] - Back to documentation home
