import os
import shutil
import subprocess
import threading
import uuid
import re
import secrets
import string
import json
import zipfile
import tempfile
import base64
import hashlib
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging
from flasgger import Swagger
import requests
import time

# ---------------- Logging Configuration ----------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates', 'ui'))
app.config['SECRET_KEY'] = 'swab-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['BUILD_FOLDER'] = os.path.join(BASE_DIR, 'builds')
app.config['FLUTTER_TEMPLATE'] = os.path.join(BASE_DIR, 'templates', 'webview_app')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# ===== Webhook Helper =====

def send_webhook_notification(webhook_url, payload):
    """Send webhook notification in a safe, non-blocking way."""
    if not webhook_url:
        return

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        app.logger.warning(f"Webhook notification failed: {e}")

# ---------------- Swagger Configuration ----------------

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

Swagger(app, config=swagger_config)

# ---------------- Global Error Handlers ----------------

@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception occurred")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['BUILD_FOLDER'], exist_ok=True)

# Store build progress
build_progress = {}

# SWAB file encryption key derived from machine-specific identifier
SWAB_SALT = b'swab_project_file_v1'

def get_machine_key():
    """Generate a machine-specific encryption key"""
    # Combine multiple machine identifiers for uniqueness
    machine_id = f"{os.getenv('USER', 'user')}_{os.path.expanduser('~')}_{BASE_DIR}"
    machine_hash = hashlib.sha256(machine_id.encode()).digest()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SWAB_SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(machine_hash))
    return Fernet(key)

def encrypt_data(data: bytes) -> bytes:
    """Encrypt data using machine-specific key"""
    fernet = get_machine_key()
    return fernet.encrypt(data)

def decrypt_data(data: bytes) -> bytes:
    """Decrypt data using machine-specific key"""
    fernet = get_machine_key()
    return fernet.decrypt(data)

def sanitize_package_name(name):
    """Sanitize package name for Android/iOS"""
    return re.sub(r'[^a-zA-Z0-9_.]', '', name).lower()

def generate_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_keystore(build_dir, config):
    """Generate a new Android keystore using keytool"""
    keystore_dir = os.path.join(build_dir, 'keystore')
    os.makedirs(keystore_dir, exist_ok=True)

    keystore_path = os.path.join(keystore_dir, 'release-keystore.jks')
    keystore_password = generate_password()
    key_alias = 'release'
    key_password = keystore_password  # Using same password for simplicity

    # Get app details for the certificate
    app_name = config.get('app_name', 'App')
    package_name = config.get('package_name', 'com.example.app')

    # Extract organization from package name
    package_parts = package_name.split('.')
    org_name = package_parts[1] if len(package_parts) > 1 else 'example'

    # Build the keytool command
    dname = f"CN={app_name}, OU=Mobile, O={org_name.capitalize()}, L=Unknown, ST=Unknown, C=US"

    keytool_cmd = [
        'keytool',
        '-genkeypair',
        '-v',
        '-keystore', keystore_path,
        '-keyalg', 'RSA',
        '-keysize', '2048',
        '-validity', '10000',
        '-alias', key_alias,
        '-storepass', keystore_password,
        '-keypass', key_password,
        '-dname', dname
    ]

    try:
        result = subprocess.run(
            keytool_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and os.path.exists(keystore_path):
            # Save keystore info to a file for user reference
            info_path = os.path.join(keystore_dir, 'keystore-info.txt')
            with open(info_path, 'w') as f:
                f.write("=== Android Keystore Information ===\n\n")
                f.write("IMPORTANT: Save this information securely!\n")
                f.write("You will need these credentials to update your app in the future.\n\n")
                f.write(f"Keystore File: release-keystore.jks\n")
                f.write(f"Keystore Password: {keystore_password}\n")
                f.write(f"Key Alias: {key_alias}\n")
                f.write(f"Key Password: {key_password}\n")
                f.write(f"\nGenerated for: {app_name} ({package_name})\n")

            return {
                'path': keystore_path,
                'password': keystore_password,
                'alias': key_alias,
                'key_password': key_password,
                'info_path': info_path
            }
    except subprocess.TimeoutExpired:
        pass
    except FileNotFoundError:
        # keytool not found
        pass

    return None

def setup_app_icon(project_dir, icon_path, build_id):
    """Setup app icon using icons_launcher package"""
    if not icon_path or not os.path.exists(icon_path):
        return False

    try:
        # Copy icon to project assets
        assets_dir = os.path.join(project_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)

        icon_dest = os.path.join(assets_dir, 'icon.png')
        shutil.copy(icon_path, icon_dest)

        # Create icons_launcher.yaml configuration
        icons_config = f"""icons_launcher:
  image_path: "assets/icon.png"
  platforms:
    android:
      enable: true
    ios:
      enable: true
    macos:
      enable: true
    windows:
      enable: true
    linux:
      enable: true
    web:
      enable: true
"""
        config_path = os.path.join(project_dir, 'icons_launcher.yaml')
        with open(config_path, 'w') as f:
            f.write(icons_config)

        # Add icons_launcher to dev_dependencies in pubspec.yaml
        pubspec_path = os.path.join(project_dir, 'pubspec.yaml')
        with open(pubspec_path, 'r') as f:
            pubspec_content = f.read()

        # Add icons_launcher if not present
        if 'icons_launcher:' not in pubspec_content:
            pubspec_content = pubspec_content.replace(
                'dev_dependencies:',
                'dev_dependencies:\n  icons_launcher: ^3.0.0'
            )
            with open(pubspec_path, 'w') as f:
                f.write(pubspec_content)

        # Run flutter pub get to get icons_launcher
        subprocess.run(
            ['flutter', 'pub', 'get'],
            cwd=project_dir,
            capture_output=True,
            timeout=120
        )

        # Run icons_launcher
        result = subprocess.run(
            ['dart', 'run', 'icons_launcher:create'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120
        )

        return result.returncode == 0
    except Exception as e:
        print(f"Icon setup error: {e}")
        return False

def rename_app(project_dir, app_name, package_name):
    """Rename app using the rename package"""
    try:
        # Add rename to dev_dependencies
        pubspec_path = os.path.join(project_dir, 'pubspec.yaml')
        with open(pubspec_path, 'r') as f:
            pubspec_content = f.read()

        if 'rename:' not in pubspec_content:
            pubspec_content = pubspec_content.replace(
                'dev_dependencies:',
                'dev_dependencies:\n  rename: ^3.0.2'
            )
            with open(pubspec_path, 'w') as f:
                f.write(pubspec_content)

        # Run flutter pub get
        subprocess.run(
            ['flutter', 'pub', 'get'],
            cwd=project_dir,
            capture_output=True,
            timeout=120
        )

        # Rename app name for all platforms
        subprocess.run(
            ['dart', 'run', 'rename', 'setAppName', '--value', app_name],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Rename bundle ID/package name for all platforms
        subprocess.run(
            ['dart', 'run', 'rename', 'setBundleId', '--value', package_name],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        return True
    except Exception as e:
        print(f"Rename error: {e}")
        return False

def run_build(build_id, config):
    """Run the Flutter build in a background thread"""
    try:
        build_progress[build_id] = {'status': 'preparing', 'progress': 5, 'message': 'Preparing build environment...'}

        # Create a unique build directory
        build_dir = os.path.join(app.config['BUILD_FOLDER'], build_id)
        os.makedirs(build_dir, exist_ok=True)

        # Copy template to build directory
        project_dir = os.path.join(build_dir, 'project')
        shutil.copytree(app.config['FLUTTER_TEMPLATE'], project_dir)

        build_progress[build_id] = {'status': 'configuring', 'progress': 10, 'message': 'Configuring app...'}

        # Update main.dart with app details and feature options
        main_dart_path = os.path.join(project_dir, 'lib', 'main.dart')
        with open(main_dart_path, 'r') as f:
            content = f.read()

        content = content.replace('{{APP_NAME}}', config['app_name'])
        content = content.replace('{{APP_URL}}', config['web_url'])

        # Replace WebView feature options
        def bool_to_dart(value):
            return 'true' if value else 'false'

        content = re.sub(
            r'static const bool ALLOW_ZOOM = \w+;',
            f'static const bool ALLOW_ZOOM = {bool_to_dart(config["allow_zoom"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_JAVASCRIPT = \w+;',
            f'static const bool ENABLE_JAVASCRIPT = {bool_to_dart(config["enable_javascript"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_DOM_STORAGE = \w+;',
            f'static const bool ENABLE_DOM_STORAGE = {bool_to_dart(config["enable_dom_storage"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_GEOLOCATION = \w+;',
            f'static const bool ENABLE_GEOLOCATION = {bool_to_dart(config["enable_geolocation"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_PULL_TO_REFRESH = \w+;',
            f'static const bool ENABLE_PULL_TO_REFRESH = {bool_to_dart(config["enable_pull_refresh"])};',
            content
        )
        content = re.sub(
            r'static const bool SHOW_NAVIGATION_BAR = \w+;',
            f'static const bool SHOW_NAVIGATION_BAR = {bool_to_dart(config["show_navigation"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_FILE_ACCESS = \w+;',
            f'static const bool ENABLE_FILE_ACCESS = {bool_to_dart(config["enable_file_access"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_CACHE = \w+;',
            f'static const bool ENABLE_CACHE = {bool_to_dart(config["enable_cache"])};',
            content
        )
        content = re.sub(
            r'static const bool ENABLE_MEDIA_AUTOPLAY = \w+;',
            f'static const bool ENABLE_MEDIA_AUTOPLAY = {bool_to_dart(config["enable_media_autoplay"])};',
            content
        )

        with open(main_dart_path, 'w') as f:
            f.write(content)

        # Update pubspec.yaml
        pubspec_path = os.path.join(project_dir, 'pubspec.yaml')
        with open(pubspec_path, 'r') as f:
            pubspec = f.read()

        # Handle placeholders from template
        pubspec = pubspec.replace('{{APP_PACKAGE_NAME}}', sanitize_package_name(config['app_name']))
        pubspec = pubspec.replace('{{APP_DESCRIPTION}}', config['app_description'])
        pubspec = pubspec.replace('{{APP_VERSION}}', config['app_version'])
        pubspec = pubspec.replace('{{APP_BUILD_NUMBER}}', str(config['build_number']))

        # Also handle old-style replacements for backwards compatibility
        pubspec = pubspec.replace('name: webview_app', f"name: {sanitize_package_name(config['app_name'])}")
        pubspec = pubspec.replace('description: "A new Flutter project."', f"description: \"{config['app_description']}\"")
        pubspec = pubspec.replace('version: 1.0.0+1', f"version: {config['app_version']}+{config['build_number']}")

        with open(pubspec_path, 'w') as f:
            f.write(pubspec)

        # Track if we generated a keystore
        keystore_generated = False
        keystore_info = None

        # Check if we need to generate a keystore for Android builds
        is_android = 'android' in config['platforms'] or 'android_aab' in config['platforms']
        has_keystore = config.get('keystore_path') and os.path.exists(config.get('keystore_path', ''))

        if is_android and not has_keystore:
            build_progress[build_id] = {'status': 'keystore', 'progress': 12, 'message': 'Generating signing keystore...'}
            keystore_info = generate_keystore(build_dir, config)
            if keystore_info:
                config['keystore_path'] = keystore_info['path']
                config['keystore_password'] = keystore_info['password']
                config['key_alias'] = keystore_info['alias']
                config['key_password'] = keystore_info['key_password']
                keystore_generated = True

        # Use rename package to set app name and bundle ID
        build_progress[build_id] = {'status': 'renaming', 'progress': 15, 'message': 'Setting app name and bundle ID...'}
        rename_app(project_dir, config['app_name'], config['package_name'])

        # Setup app icon if provided
        icon_path = config.get('icon_path')
        if icon_path and os.path.exists(icon_path):
            build_progress[build_id] = {'status': 'icons', 'progress': 18, 'message': 'Generating app icons...'}
            setup_app_icon(project_dir, icon_path, build_id)

        # Update Android config (for keystore)
        if 'android' in config['platforms'] or 'android_aab' in config['platforms']:
            update_android_config(project_dir, config)

        # Update iOS bundle ID
        if 'ios' in config['platforms']:
            update_ios_config(project_dir, config)

        # Update macOS bundle ID
        if 'macos' in config['platforms']:
            update_macos_config(project_dir, config)

        # Update Windows config
        if 'windows' in config['platforms']:
            update_windows_config(project_dir, config)

        # Update Linux config
        if 'linux' in config['platforms']:
            update_linux_config(project_dir, config)

        build_progress[build_id] = {'status': 'dependencies', 'progress': 22, 'message': 'Getting dependencies...'}

        # Run flutter pub get
        subprocess.run(['flutter', 'pub', 'get'], cwd=project_dir, check=True, capture_output=True, timeout=180)

        outputs = {}
        platform_count = len(config['platforms'])
        progress_per_platform = 65 / max(platform_count, 1)
        current_progress = 28

        for platform in config['platforms']:
            build_progress[build_id] = {
                'status': 'building',
                'progress': int(current_progress),
                'message': f'Building {get_platform_display_name(platform)}...'
            }

            try:
                output_path = build_platform(project_dir, build_dir, platform, config)
                if output_path:
                    outputs[platform] = output_path
            except Exception as e:
                outputs[platform] = f'Error: {str(e)}'

            current_progress += progress_per_platform

        # Prepare final status
        final_status = {
            'status': 'completed',
            'progress': 100,
            'message': 'Build completed!',
            'outputs': outputs
        }

        # Add keystore info if we generated one
        if keystore_generated and keystore_info:
            final_status['keystore_generated'] = True
            final_status['keystore_path'] = keystore_info['path']
            final_status['keystore_info_path'] = keystore_info.get('info_path')

        build_progress[build_id] = final_status
        # ✅ Webhook on success
        webhook_url = config.get('webhook_url')
        payload = {
            "build_id": build_id,
            "status": final_status.get('status'),
            "platforms": config.get('platforms'),
            "outputs": final_status.get('outputs')
        }

        threading.Thread(
            target=send_webhook_notification,
            args=(webhook_url, payload),
            daemon=True
        ).start()

    except Exception as e:
        error_status = {
            'status': 'error',
            'progress': 0,
            'message': f'Build failed: {str(e)}'
        }
        build_progress[build_id] = error_status

        # ✅ Webhook on failure
        webhook_url = config.get('webhook_url')
        payload = {
            "build_id": build_id,
            "status": "error",
            "error": str(e),
            "platforms": config.get('platforms')
        }

        threading.Thread(
            target=send_webhook_notification,
            args=(webhook_url, payload),
            daemon=True
        ).start()


def get_platform_display_name(platform):
    """Get display name for platform"""
    names = {
        'android': 'Android APK',
        'android_aab': 'Android AAB',
        'ios': 'iOS',
        'macos': 'macOS',
        'windows': 'Windows',
        'linux': 'Linux'
    }
    return names.get(platform, platform)

def update_android_config(project_dir, config):
    """Update Android configuration"""
    build_gradle_path = os.path.join(project_dir, 'android', 'app', 'build.gradle.kts')
    if os.path.exists(build_gradle_path):
        with open(build_gradle_path, 'r') as f:
            content = f.read()

        # Replace placeholders
        content = content.replace('{{APP_PACKAGE_NAME}}', config['package_name'])
        content = content.replace('{{APP_VERSION}}', config['app_version'])
        content = content.replace('{{APP_BUILD_NUMBER}}', str(config['build_number']))

        # Handle keystore configuration
        keystore_path = config.get('keystore_path', '')
        keystore_password = config.get('keystore_password', '')
        key_alias = config.get('key_alias', '')
        key_password = config.get('key_password', '')

        if keystore_path and os.path.exists(keystore_path):
            content = content.replace('{{KEYSTORE_PATH}}', keystore_path)
            content = content.replace('{{KEYSTORE_PASSWORD}}', keystore_password)
            content = content.replace('{{KEY_ALIAS}}', key_alias)
            content = content.replace('{{KEY_PASSWORD}}', key_password)
        else:
            # Remove signing config for release and use debug signing
            content = re.sub(
                r'signingConfigs\s*\{[^}]*create\("release"\)[^}]*\}[^}]*\}',
                '',
                content,
                flags=re.DOTALL
            )
            content = re.sub(
                r'signingConfig\s*=\s*signingConfigs\.getByName\("release"\)',
                'signingConfig = signingConfigs.getByName("debug")',
                content
            )

        # Also handle old-style replacements for backwards compatibility
        content = re.sub(
            r'namespace\s*=\s*"[^"]*"',
            f'namespace = "{config["package_name"]}"',
            content
        )
        content = re.sub(
            r'applicationId\s*=\s*"[^"]*"',
            f'applicationId = "{config["package_name"]}"',
            content
        )

        with open(build_gradle_path, 'w') as f:
            f.write(content)

    # Update AndroidManifest.xml label
    manifest_path = os.path.join(project_dir, 'android', 'app', 'src', 'main', 'AndroidManifest.xml')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            content = f.read()

        content = content.replace('{{APP_NAME}}', config['app_name'])
        content = re.sub(
            r'android:label="[^"]*"',
            f'android:label="{config["app_name"]}"',
            content
        )

        with open(manifest_path, 'w') as f:
            f.write(content)

def update_ios_config(project_dir, config):
    """Update iOS configuration"""
    info_plist_path = os.path.join(project_dir, 'ios', 'Runner', 'Info.plist')
    if os.path.exists(info_plist_path):
        with open(info_plist_path, 'r') as f:
            content = f.read()

        # Update bundle display name
        content = re.sub(
            r'(<key>CFBundleDisplayName</key>\s*<string>)[^<]*(</string>)',
            f'\\g<1>{config["app_name"]}\\g<2>',
            content
        )
        content = re.sub(
            r'(<key>CFBundleName</key>\s*<string>)[^<]*(</string>)',
            f'\\g<1>{config["app_name"]}\\g<2>',
            content
        )

        with open(info_plist_path, 'w') as f:
            f.write(content)

    # Update project.pbxproj for bundle ID
    pbxproj_path = os.path.join(project_dir, 'ios', 'Runner.xcodeproj', 'project.pbxproj')
    if os.path.exists(pbxproj_path):
        with open(pbxproj_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'PRODUCT_BUNDLE_IDENTIFIER\s*=\s*[^;]+;',
            f'PRODUCT_BUNDLE_IDENTIFIER = {config["package_name"]};',
            content
        )

        with open(pbxproj_path, 'w') as f:
            f.write(content)

def update_macos_config(project_dir, config):
    """Update macOS configuration"""
    info_plist_path = os.path.join(project_dir, 'macos', 'Runner', 'Info.plist')
    if os.path.exists(info_plist_path):
        with open(info_plist_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'(<key>CFBundleName</key>\s*<string>)[^<]*(</string>)',
            f'\\g<1>{config["app_name"]}\\g<2>',
            content
        )

        with open(info_plist_path, 'w') as f:
            f.write(content)

def update_windows_config(project_dir, config):
    """Update Windows configuration"""
    cmake_path = os.path.join(project_dir, 'windows', 'CMakeLists.txt')
    if os.path.exists(cmake_path):
        with open(cmake_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'project\([^)]+\)',
            f'project({sanitize_package_name(config["app_name"])} LANGUAGES CXX)',
            content
        )

        with open(cmake_path, 'w') as f:
            f.write(content)

def update_linux_config(project_dir, config):
    """Update Linux configuration"""
    cmake_path = os.path.join(project_dir, 'linux', 'CMakeLists.txt')
    if os.path.exists(cmake_path):
        with open(cmake_path, 'r') as f:
            content = f.read()

        content = re.sub(
            r'set\(BINARY_NAME\s+"[^"]*"\)',
            f'set(BINARY_NAME "{sanitize_package_name(config["app_name"])}")',
            content
        )

        with open(cmake_path, 'w') as f:
            f.write(content)

def build_platform(project_dir, build_dir, platform, config):
    """Build for a specific platform - always uses release mode"""
    output_dir = os.path.join(build_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    if platform == 'android':
        subprocess.run(
            ['flutter', 'build', 'apk', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        apk_path = os.path.join(project_dir, 'build', 'app', 'outputs', 'flutter-apk', 'app-release.apk')
        if os.path.exists(apk_path):
            output_path = os.path.join(output_dir, f'{config["app_name"]}.apk')
            shutil.copy(apk_path, output_path)
            return output_path

    elif platform == 'android_aab':
        subprocess.run(
            ['flutter', 'build', 'appbundle', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        aab_path = os.path.join(project_dir, 'build', 'app', 'outputs', 'bundle', 'release', 'app-release.aab')
        if os.path.exists(aab_path):
            output_path = os.path.join(output_dir, f'{config["app_name"]}.aab')
            shutil.copy(aab_path, output_path)
            return output_path

    elif platform == 'ios':
        subprocess.run(
            ['flutter', 'build', 'ios', '--release', '--no-codesign'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        return os.path.join(project_dir, 'build', 'ios', 'iphoneos', 'Runner.app')

    elif platform == 'web':
        subprocess.run(
            ['flutter', 'build', 'web', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=300
        )
        web_dir = os.path.join(project_dir, 'build', 'web')
        if os.path.exists(web_dir):
            output_path = os.path.join(output_dir, f'{config["app_name"]}_web.zip')
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', web_dir)
            return output_path

    elif platform == 'macos':
        subprocess.run(
            ['flutter', 'build', 'macos', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        app_path = os.path.join(project_dir, 'build', 'macos', 'Build', 'Products', 'Release')
        if os.path.exists(app_path):
            output_path = os.path.join(output_dir, f'{config["app_name"]}_macos.zip')
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', app_path)
            return output_path

    elif platform == 'windows':
        subprocess.run(
            ['flutter', 'build', 'windows', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        exe_dir = os.path.join(project_dir, 'build', 'windows', 'x64', 'runner', 'Release')
        if os.path.exists(exe_dir):
            output_path = os.path.join(output_dir, f'{config["app_name"]}_windows.zip')
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', exe_dir)
            return output_path

    elif platform == 'linux':
        subprocess.run(
            ['flutter', 'build', 'linux', '--release'],
            cwd=project_dir,
            check=True,
            capture_output=True,
            timeout=600
        )
        linux_dir = os.path.join(project_dir, 'build', 'linux', 'x64', 'release', 'bundle')
        if os.path.exists(linux_dir):
            output_path = os.path.join(output_dir, f'{config["app_name"]}_linux.zip')
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', linux_dir)
            return output_path

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files (icons, etc.)"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/build', methods=['POST'])
def start_build():

    """
    Start a new build process
    ---
    tags:
      - Build
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - app_name
            - app_version
            - build_number
            - web_url
            - platforms
          properties:
            app_name:
              type: string
            app_version:
              type: string
            build_number:
              type: string
            web_url:
              type: string
            platforms:
              type: array
              items:
                type: string
    responses:
      200:
        description: Build started successfully
      400:
        description: Invalid input
      500:
        description: Internal server error
    """


    try:
        logger.info("Received build request")

        data = request.json
        if not data:
            logger.warning("No JSON payload received")
            return jsonify({'error': 'Invalid JSON payload'}), 400

        # Validate required fields
        required_fields = [
            'app_name', 'app_description', 'app_version',
            'build_number', 'package_name', 'web_url', 'platforms'
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                logger.warning(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400

        if not data['platforms']:
            logger.warning("No platforms selected")
            return jsonify({'error': 'At least one platform must be selected'}), 400

        # Generate build ID
        build_id = str(uuid.uuid4())
        logger.info(f"Starting build with ID: {build_id}")
        
        if 'download_directory' in data and not isinstance(data['download_directory'], str):
            return jsonify({'error': 'download_directory must be a string'}), 400
        # Camera & Gallery config validation
        if 'enable_camera_access' in data and not isinstance(data['enable_camera_access'], bool):
            return jsonify({'error': 'enable_camera_access must be a boolean'}), 400

        if 'enable_gallery_access' in data and not isinstance(data['enable_gallery_access'], bool):
            return jsonify({'error': 'enable_gallery_access must be a boolean'}), 400

        if 'camera_permission_prompt' in data and not isinstance(data['camera_permission_prompt'], bool):
            return jsonify({'error': 'camera_permission_prompt must be a boolean'}), 400
        
        # QR / Barcode scanner config validation
        if 'enable_qr_scanner' in data and not isinstance(data['enable_qr_scanner'], bool):
            return jsonify({'error': 'enable_qr_scanner must be a boolean'}), 400

        if 'enable_barcode_scanner' in data and not isinstance(data['enable_barcode_scanner'], bool):
            return jsonify({'error': 'enable_barcode_scanner must be a boolean'}), 400

        if 'scanner_formats' in data and not isinstance(data['scanner_formats'], (list, str)):
            return jsonify({'error': 'scanner_formats must be a list or string'}), 400


        # Start build in background thread
        config = {
            'app_name': data['app_name'],
            'app_description': data['app_description'],
            'app_version': data['app_version'],
            'build_number': data['build_number'],
            'package_name': data['package_name'],
            'web_url': data['web_url'],
            'platforms': data['platforms'],
            # WebView feature options
            'allow_zoom': data.get('allow_zoom', True),
            'enable_javascript': data.get('enable_javascript', True),
            'enable_dom_storage': data.get('enable_dom_storage', True),
            'enable_geolocation': data.get('enable_geolocation', True),
            'enable_pull_refresh': data.get('enable_pull_refresh', True),
            'show_navigation': data.get('show_navigation', True),
            'enable_file_access': data.get('enable_file_access', True),
            'enable_cache': data.get('enable_cache', True),
            'enable_media_autoplay': data.get('enable_media_autoplay', False),

            # Camera & Gallery access config
            'enable_camera_access': data.get('enable_camera_access', True),
            'enable_gallery_access': data.get('enable_gallery_access', True),
            'camera_permission_prompt': data.get('camera_permission_prompt', True),

            # QR / Barcode scanner config
            'enable_qr_scanner': data.get('enable_qr_scanner', True),
            'enable_barcode_scanner': data.get('enable_barcode_scanner', True),
            'scanner_formats': data.get('scanner_formats', []),



            # Download manager config (backend support)
            'enable_download_manager': data.get('enable_download_manager', True),
            'download_directory': data.get('download_directory', 'Downloads'),
            'allow_large_downloads': data.get('allow_large_downloads', True),


            # Keystore config (optional)
            'keystore_path': data.get('keystore_path'),
            'keystore_password': data.get('keystore_password'),
            'key_alias': data.get('key_alias'),
            'key_password': data.get('key_password'),
            # Icon config (optional)
            'icon_path': data.get('icon_path'),
            # Web Hooks
            'webhook_url': data.get('webhook_url')
        }

        thread = threading.Thread(target=run_build, args=(build_id, config))
        thread.start()

        logger.info(f"Build thread started for build ID: {build_id}")
        return jsonify({'build_id': build_id})

    except Exception:
        logger.exception("Failed to start build process")
        return jsonify({
            'error': 'Failed to start build'
        }), 500

@app.route('/api/build/<build_id>/download/<platform>')
def download_build(build_id, platform):
    if build_id not in build_progress:
        return jsonify({'error': 'Build not found'}), 404

    progress = build_progress[build_id]
    if progress['status'] != 'completed':
        return jsonify({'error': 'Build not completed'}), 400

    # Handle keystore download
    if platform == 'keystore':
        if not progress.get('keystore_generated'):
            return jsonify({'error': 'No keystore was generated for this build'}), 404

        keystore_path = progress.get('keystore_path')

        if keystore_path and os.path.exists(keystore_path):
            # Create a zip with both keystore and info file
            build_dir = os.path.join(app.config['BUILD_FOLDER'], build_id)
            keystore_dir = os.path.join(build_dir, 'keystore')
            zip_path = os.path.join(build_dir, 'outputs', 'keystore-bundle.zip')

            shutil.make_archive(zip_path.replace('.zip', ''), 'zip', keystore_dir)

            if os.path.exists(zip_path):
                return send_file(zip_path, as_attachment=True, download_name='keystore-bundle.zip')

        return jsonify({'error': 'Keystore file not found'}), 404

    if platform not in progress.get('outputs', {}):
        return jsonify({'error': 'Platform output not found'}), 404

    output_path = progress['outputs'][platform]
    if output_path.startswith('Error:'):
        return jsonify({'error': output_path}), 400

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)

    return jsonify({'error': 'Output file not found'}), 404

@app.route('/api/upload/keystore', methods=['POST'])
def upload_keystore():
    if 'keystore' not in request.files:
        return jsonify({'error': 'No keystore file provided'}), 400

    file = request.files['keystore']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename, 'path': filepath})

    return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/upload/icon', methods=['POST'])
def upload_icon():
    if 'icon' not in request.files:
        return jsonify({'error': 'No icon file provided'}), 400

    file = request.files['icon']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        # Generate unique filename
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ['.png', '.jpg', '.jpeg']:
            return jsonify({'error': 'Invalid file type. Use PNG or JPG'}), 400

        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename, 'path': filepath})

    return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/project/save', methods=['POST'])
def save_project():
    """Save project as encrypted .swab file"""
    data = request.json

    # Validate required fields
    required_fields = ['app_name', 'app_version', 'build_number']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    app_name = data['app_name']
    app_version = data['app_version']
    build_number = data['build_number']

    # Create a temporary directory for the project
    temp_dir = tempfile.mkdtemp()

    try:
        # Create project structure
        project_data = {
            'app_name': app_name,
            'app_description': data.get('app_description', ''),
            'app_version': app_version,
            'build_number': build_number,
            'package_name': data.get('package_name', ''),
            'web_url': data.get('web_url', ''),
            # WebView settings
            'allow_zoom': data.get('allow_zoom', True),
            'enable_javascript': data.get('enable_javascript', True),
            'enable_dom_storage': data.get('enable_dom_storage', True),
            'enable_geolocation': data.get('enable_geolocation', True),
            'enable_pull_refresh': data.get('enable_pull_refresh', True),
            'show_navigation': data.get('show_navigation', True),
            'enable_file_access': data.get('enable_file_access', True),
            'enable_cache': data.get('enable_cache', True),
            'enable_media_autoplay': data.get('enable_media_autoplay', False),
            # Keystore info (credentials only, file stored separately)
            'keystore_password': data.get('keystore_password', ''),
            'key_alias': data.get('key_alias', ''),
            'key_password': data.get('key_password', ''),
        }

        # Save project.json
        project_json_path = os.path.join(temp_dir, 'project.json')
        with open(project_json_path, 'w') as f:
            json.dump(project_data, f, indent=2)

        # Create assets directory
        assets_dir = os.path.join(temp_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)

        # Copy icon if provided
        icon_path = data.get('icon_path')
        if icon_path and os.path.exists(icon_path):
            ext = os.path.splitext(icon_path)[1]
            shutil.copy(icon_path, os.path.join(assets_dir, f'icon{ext}'))

        # Copy keystore if provided
        keystore_path = data.get('keystore_path')
        if keystore_path and os.path.exists(keystore_path):
            shutil.copy(keystore_path, os.path.join(assets_dir, 'keystore.jks'))

        # Create the zip file
        zip_path = os.path.join(temp_dir, 'project.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file != 'project.zip':
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

        # Read and encrypt the zip
        with open(zip_path, 'rb') as f:
            zip_data = f.read()

        encrypted_data = encrypt_data(zip_data)

        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', app_name)
        filename = f"{safe_name}_v{app_version}_{build_number}.swab"

        # Save to outputs folder
        output_dir = os.path.join(app.config['BUILD_FOLDER'], 'saved_projects')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )

    except Exception as e:
        return jsonify({'error': f'Failed to save project: {str(e)}'}), 500

    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.route('/api/project/open', methods=['POST'])
def open_project():
    """Open and decrypt a .swab project file"""
    if 'project' not in request.files:
        return jsonify({'error': 'No project file provided'}), 400

    file = request.files['project']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.swab'):
        return jsonify({'error': 'Invalid file type. Please select a .swab file'}), 400

    temp_dir = tempfile.mkdtemp()

    try:
        # Read encrypted data
        encrypted_data = file.read()

        # Decrypt data
        try:
            decrypted_data = decrypt_data(encrypted_data)
        except Exception:
            return jsonify({'error': 'Cannot open this project file. It was created on a different machine or has been corrupted.'}), 403

        # Write decrypted zip to temp file
        zip_path = os.path.join(temp_dir, 'project.zip')
        with open(zip_path, 'wb') as f:
            f.write(decrypted_data)

        # Extract zip
        extract_dir = os.path.join(temp_dir, 'extracted')
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_dir)

        # Read project.json
        project_json_path = os.path.join(extract_dir, 'project.json')
        if not os.path.exists(project_json_path):
            return jsonify({'error': 'Invalid project file: missing project.json'}), 400

        with open(project_json_path, 'r') as f:
            project_data = json.load(f)

        # Handle assets
        assets_dir = os.path.join(extract_dir, 'assets')
        response_data = dict(project_data)

        # Copy icon to uploads if exists
        for ext in ['.png', '.jpg', '.jpeg']:
            icon_path = os.path.join(assets_dir, f'icon{ext}')
            if os.path.exists(icon_path):
                new_icon_name = f"{uuid.uuid4()}{ext}"
                new_icon_path = os.path.join(app.config['UPLOAD_FOLDER'], new_icon_name)
                shutil.copy(icon_path, new_icon_path)
                response_data['icon_path'] = new_icon_path
                break

        # Copy keystore to uploads if exists
        keystore_path = os.path.join(assets_dir, 'keystore.jks')
        if os.path.exists(keystore_path):
            new_keystore_name = f"{uuid.uuid4()}.jks"
            new_keystore_path = os.path.join(app.config['UPLOAD_FOLDER'], new_keystore_name)
            shutil.copy(keystore_path, new_keystore_path)
            response_data['keystore_path'] = new_keystore_path

        return jsonify({'success': True, 'project': response_data})

    except Exception as e:
        return jsonify({'error': f'Failed to open project: {str(e)}'}), 500

    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
