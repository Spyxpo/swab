# SWAB - Spyxpo Web to App Builder

<p align="center">
  <img src="https://raw.githubusercontent.com/user/swab/stable/static/images/logo.png" alt="SWAB Logo" width="200"/>
</p>

**SWAB** (Spyxpo Web to App Builder) is a powerful tool that converts any website into native mobile and desktop applications without requiring any coding. Built with Flask and Flutter, it provides a seamless experience for transforming web content into installable apps across 6 major platforms.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Platform Support** | Build for Android, iOS, macOS, Windows, and Linux from a single configuration |
| **No Coding Required** | Simple web interface - just enter your URL and configure settings |
| **Customizable WebView** | Control JavaScript, zoom, geolocation, caching, and more |
| **Android Signing** | Automatic keystore generation or use your own signing keys |
| **Project Management** | Save and load projects with encrypted `.swab` files |
| **Live Preview** | Preview your website in different device frames before building |
| **Real-time Progress** | Track build progress with live status updates |

---

## Supported Platforms

| Platform | Output Format | Requirements |
|----------|--------------|--------------|
| Android | APK, AAB (App Bundle) | Android Studio, Android SDK |
| iOS | .app (for Xcode signing) | macOS, Xcode |
| macOS | .app (bundled as ZIP) | macOS, Xcode |
| Windows | .exe (bundled as ZIP) | Windows, Visual Studio C++ |
| Linux | Binary (bundled as ZIP) | Linux, Clang, CMake, GTK |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/user/swab.git
cd swab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## Documentation

| Page | Description |
|------|-------------|
| [[Getting Started]] | Installation guide and first steps |
| [[Configuration Guide]] | App settings and WebView options |
| [[Platform Build Guide]] | Platform-specific build instructions |
| [[API Reference]] | REST API endpoints and usage |
| [[Troubleshooting]] | Common issues and solutions |
| [[FAQ]] | Frequently asked questions |

---

## How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │───▶│  Flask Backend  │───▶│ Flutter Builder │
│   (Configure)   │    │   (Process)     │    │   (Compile)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌───────────────────────────────┘
                       ▼
        ┌──────────────────────────────────────┐
        │         Native Applications          │
        ├──────┬──────┬──────┬─────────┬───────┤
        │ APK  │ iOS  │macOS │ Windows │ Linux │
        └──────┴──────┴──────┴─────────┴───────┘
```

1. **Configure** - Enter app details, URL, and WebView settings via the web interface
2. **Process** - Flask backend validates input and prepares the Flutter template
3. **Build** - Flutter compiles native apps for selected platforms
4. **Download** - Get your ready-to-distribute application packages

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask 3.0+ |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| App Framework | Flutter, Dart |
| WebView | flutter_inappwebview, webview_flutter |
| Encryption | Cryptography (Fernet) |
| Build System | Flutter CLI, Platform SDKs |

---

## Project Structure

```
swab/
├── app.py                    # Flask backend server
├── requirements.txt          # Python dependencies
├── templates/
│   ├── ui/index.html        # Web interface
│   └── webview_app/         # Flutter app template
├── static/
│   ├── css/style.css        # Styling
│   ├── js/main.js           # Frontend logic
│   └── images/              # Assets
├── builds/                   # Build outputs
└── uploads/                  # User uploads
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Support

- **Issues**: [GitHub Issues](https://github.com/user/swab/issues)
- **Documentation**: This Wiki
- **Updates**: Watch this repository for updates
