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
import plistlib
import platform
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Firebase Admin SDK
firebase_initialized = False
db = None

def init_firebase():
    global firebase_initialized, db
    if not firebase_initialized:
        try:
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'serviceAccount.json')
            print(f"[Firebase Init] BASE_DIR: {BASE_DIR}")
            print(f"[Firebase Init] Original cred_path: {cred_path}")
            # Resolve relative paths from BASE_DIR
            if not os.path.isabs(cred_path):
                cred_path = os.path.join(BASE_DIR, cred_path)
            print(f"[Firebase Init] Resolved cred_path: {cred_path}")
            print(f"[Firebase Init] File exists: {os.path.exists(cred_path)}")
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                firebase_initialized = True
                print("Firebase Admin SDK initialized successfully")
            else:
                print(f"Warning: Firebase credentials file not found at {cred_path}")
                print("Firebase features will be disabled. Download serviceAccount.json from Firebase Console.")
        except Exception as e:
            print(f"Warning: Failed to initialize Firebase Admin SDK: {e}")
            import traceback
            traceback.print_exc()
            print("Firebase features will be disabled.")

# Try to initialize Firebase on module load
init_firebase()

# Firebase configuration for client-side
def get_firebase_config():
    return {
        'api_key': os.getenv('FIREBASE_API_KEY', ''),
        'auth_domain': os.getenv('FIREBASE_AUTH_DOMAIN', ''),
        'project_id': os.getenv('FIREBASE_PROJECT_ID', ''),
        'storage_bucket': os.getenv('FIREBASE_STORAGE_BUCKET', ''),
        'messaging_sender_id': os.getenv('FIREBASE_MESSAGING_SENDER_ID', ''),
        'app_id': os.getenv('FIREBASE_APP_ID', ''),
        'measurement_id': os.getenv('FIREBASE_MEASUREMENT_ID', '')
    }

# Authentication decorator
def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not firebase_initialized:
            return jsonify({'error': 'Firebase not configured'}), 503

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401

        id_token = auth_header.split('Bearer ')[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            request.user = decoded_token
            return f(*args, **kwargs)
        except firebase_admin.exceptions.FirebaseError as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401

    return decorated_function

# ==================== APPLE SIGNING SECURITY ====================

class SecureAppleSigning:
    """Secure handler for Apple code signing credentials"""

    def __init__(self, build_id):
        self.build_id = build_id
        self.keychain_name = None
        self.keychain_password = None
        self.profile_uuid = None
        self.temp_files = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup all sensitive data on exit"""
        self.cleanup()

    def cleanup(self):
        """Securely cleanup keychain and temporary files"""
        # Delete temporary keychain
        if self.keychain_name:
            try:
                subprocess.run(
                    ['security', 'delete-keychain', self.keychain_name],
                    capture_output=True,
                    timeout=30
                )
            except Exception:
                pass

        # Remove provisioning profile from system
        if self.profile_uuid:
            try:
                profile_path = os.path.expanduser(
                    f'~/Library/MobileDevice/Provisioning Profiles/{self.profile_uuid}.mobileprovision'
                )
                if os.path.exists(profile_path):
                    os.remove(profile_path)
            except Exception:
                pass

        # Securely delete temporary files
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    # Overwrite with random data before deletion for security
                    with open(temp_file, 'wb') as f:
                        f.write(secrets.token_bytes(os.path.getsize(temp_file)))
                    os.remove(temp_file)
            except Exception:
                pass

        # Clear sensitive data from memory
        self.keychain_password = None

    def create_temporary_keychain(self):
        """Create a temporary keychain for this build"""
        self.keychain_name = f"swab-build-{self.build_id}.keychain-db"
        self.keychain_password = secrets.token_hex(32)

        # Create the keychain
        result = subprocess.run(
            ['security', 'create-keychain', '-p', self.keychain_password, self.keychain_name],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(f"Failed to create keychain: {result.stderr}")

        # Set keychain settings (no auto-lock, no timeout)
        subprocess.run(
            ['security', 'set-keychain-settings', self.keychain_name],
            capture_output=True,
            timeout=30
        )

        # Unlock the keychain
        subprocess.run(
            ['security', 'unlock-keychain', '-p', self.keychain_password, self.keychain_name],
            capture_output=True,
            timeout=30
        )

        # Add to search list (required for codesign to find it)
        result = subprocess.run(
            ['security', 'list-keychains', '-d', 'user'],
            capture_output=True,
            text=True,
            timeout=30
        )

        current_keychains = result.stdout.strip().replace('"', '').split('\n')
        current_keychains = [k.strip() for k in current_keychains if k.strip()]

        subprocess.run(
            ['security', 'list-keychains', '-d', 'user', '-s', self.keychain_name] + current_keychains,
            capture_output=True,
            timeout=30
        )

        return self.keychain_name

    def import_certificate(self, cert_path, cert_password):
        """Import a .p12 certificate into the temporary keychain"""
        if not self.keychain_name:
            self.create_temporary_keychain()

        # Validate certificate file
        if not os.path.exists(cert_path):
            raise Exception("Certificate file not found")

        if not cert_path.endswith(('.p12', '.pfx')):
            raise Exception("Invalid certificate format. Use .p12 or .pfx file")

        # Import certificate with codesign access
        result = subprocess.run(
            [
                'security', 'import', cert_path,
                '-k', self.keychain_name,
                '-P', cert_password,
                '-T', '/usr/bin/codesign',
                '-T', '/usr/bin/security',
                '-T', '/usr/bin/productbuild'
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            if 'incorrect password' in result.stderr.lower() or 'mac verify failure' in result.stderr.lower():
                raise Exception("Invalid certificate password")
            raise Exception(f"Failed to import certificate: {result.stderr}")

        # Set key partition list to allow codesign access without prompts
        subprocess.run(
            [
                'security', 'set-key-partition-list',
                '-S', 'apple-tool:,apple:,codesign:',
                '-s', '-k', self.keychain_password,
                self.keychain_name
            ],
            capture_output=True,
            timeout=30
        )

        return True

    def validate_provisioning_profile(self, profile_path):
        """Validate and extract info from provisioning profile"""
        if not os.path.exists(profile_path):
            raise Exception("Provisioning profile not found")

        if not profile_path.endswith('.mobileprovision'):
            raise Exception("Invalid provisioning profile format")

        # Extract plist from provisioning profile using security cms
        result = subprocess.run(
            ['security', 'cms', '-D', '-i', profile_path],
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception("Invalid provisioning profile")

        try:
            plist_data = plistlib.loads(result.stdout)
        except Exception:
            raise Exception("Failed to parse provisioning profile")

        # Extract relevant information
        profile_info = {
            'uuid': plist_data.get('UUID'),
            'name': plist_data.get('Name'),
            'team_id': plist_data.get('TeamIdentifier', [None])[0],
            'bundle_id': plist_data.get('Entitlements', {}).get('application-identifier', ''),
            'expiration_date': plist_data.get('ExpirationDate'),
            'creation_date': plist_data.get('CreationDate'),
            'platform': plist_data.get('Platform', ['iOS']),
            'is_development': 'get-task-allow' in str(plist_data.get('Entitlements', {})),
        }

        # Check if profile is expired
        from datetime import datetime
        if profile_info['expiration_date']:
            if isinstance(profile_info['expiration_date'], datetime):
                if profile_info['expiration_date'] < datetime.now():
                    raise Exception("Provisioning profile has expired")

        # Extract app bundle ID (remove team prefix)
        if profile_info['bundle_id']:
            parts = profile_info['bundle_id'].split('.')
            if len(parts) > 1 and parts[0] == profile_info['team_id']:
                profile_info['app_bundle_id'] = '.'.join(parts[1:])
            else:
                profile_info['app_bundle_id'] = profile_info['bundle_id']

        self.profile_uuid = profile_info['uuid']
        return profile_info

    def install_provisioning_profile(self, profile_path):
        """Install provisioning profile to system location"""
        profile_info = self.validate_provisioning_profile(profile_path)

        # Create provisioning profiles directory if needed
        profiles_dir = os.path.expanduser('~/Library/MobileDevice/Provisioning Profiles')
        os.makedirs(profiles_dir, exist_ok=True)

        # Copy profile with UUID as filename
        dest_path = os.path.join(profiles_dir, f"{profile_info['uuid']}.mobileprovision")
        shutil.copy(profile_path, dest_path)

        self.temp_files.append(dest_path)  # Track for cleanup

        return profile_info

    def get_signing_identity(self):
        """Get the signing identity from the keychain"""
        if not self.keychain_name:
            raise Exception("No keychain created")

        result = subprocess.run(
            ['security', 'find-identity', '-v', '-p', 'codesigning', self.keychain_name],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception("Failed to find signing identity")

        # Parse the output to get identity
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'Apple Distribution' in line or 'iPhone Distribution' in line or 'Mac Developer' in line or 'Apple Development' in line:
                # Extract the identity hash
                parts = line.split('"')
                if len(parts) >= 2:
                    return parts[1]

        raise Exception("No valid signing identity found in certificate")

    def create_export_options_plist(self, build_dir, config, profile_info):
        """Create ExportOptions.plist for xcodebuild"""

        # Determine export method based on profile type
        if profile_info.get('is_development'):
            method = 'development'
        elif 'app-store' in profile_info.get('name', '').lower():
            method = 'app-store'
        else:
            method = 'ad-hoc'

        export_options = {
            'method': method,
            'teamID': config.get('team_id') or profile_info.get('team_id'),
            'signingStyle': 'manual',
            'provisioningProfiles': {
                config.get('package_name'): profile_info.get('name') or profile_info.get('uuid')
            }
        }

        # Add additional options for App Store
        if method == 'app-store':
            export_options['uploadSymbols'] = True
            export_options['uploadBitcode'] = False

        plist_path = os.path.join(build_dir, 'ExportOptions.plist')
        with open(plist_path, 'wb') as f:
            plistlib.dump(export_options, f)

        self.temp_files.append(plist_path)
        return plist_path


def validate_apple_certificate(cert_path, password):
    """Validate a .p12 certificate file without importing"""
    if not os.path.exists(cert_path):
        return {'valid': False, 'error': 'Certificate file not found'}

    # Use openssl to validate (more portable than security command)
    result = subprocess.run(
        ['openssl', 'pkcs12', '-in', cert_path, '-passin', f'pass:{password}', '-noout'],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        if 'mac verify failure' in result.stderr.lower():
            return {'valid': False, 'error': 'Invalid password'}
        return {'valid': False, 'error': 'Invalid certificate file'}

    # Get certificate info
    result = subprocess.run(
        ['openssl', 'pkcs12', '-in', cert_path, '-passin', f'pass:{password}', '-nokeys', '-clcerts'],
        capture_output=True,
        text=True,
        timeout=30
    )

    cert_info = {}
    if result.returncode == 0:
        # Parse certificate subject
        for line in result.stdout.split('\n'):
            if 'subject=' in line.lower():
                cert_info['subject'] = line.split('=', 1)[1].strip() if '=' in line else ''
            elif 'notafter=' in line.lower():
                cert_info['expires'] = line.split('=', 1)[1].strip() if '=' in line else ''

    return {'valid': True, 'info': cert_info}


def is_macos():
    """Check if running on macOS (required for Apple signing)"""
    return platform.system() == 'Darwin'

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates', 'ui'))
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'swab-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['BUILD_FOLDER'] = os.path.join(BASE_DIR, 'builds')
app.config['FLUTTER_TEMPLATE'] = os.path.join(BASE_DIR, 'templates', 'webview_app')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

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

    except Exception as e:
        build_progress[build_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Build failed: {str(e)}'
        }

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

def build_ios_signed(project_dir, build_dir, config):
    """Build signed iOS app (.ipa) using Apple credentials"""
    output_dir = os.path.join(build_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    apple_cert_path = config.get('apple_certificate_path')
    apple_cert_password = config.get('apple_certificate_password')
    apple_profile_path = config.get('apple_provisioning_profile_path')

    with SecureAppleSigning(os.path.basename(build_dir)) as signer:
        try:
            # Create temporary keychain and import certificate
            signer.create_temporary_keychain()
            signer.import_certificate(apple_cert_path, apple_cert_password)

            # Install and validate provisioning profile
            profile_info = signer.install_provisioning_profile(apple_profile_path)

            # Get signing identity
            signing_identity = signer.get_signing_identity()

            # Create ExportOptions.plist
            export_options_path = signer.create_export_options_plist(build_dir, config, profile_info)

            # Build the iOS app with Flutter (this creates the xcarchive)
            subprocess.run(
                ['flutter', 'build', 'ios', '--release'],
                cwd=project_dir,
                check=True,
                capture_output=True,
                timeout=600,
                env={**os.environ, 'CODE_SIGN_IDENTITY': signing_identity}
            )

            # Find the .app file
            app_path = os.path.join(project_dir, 'build', 'ios', 'iphoneos', 'Runner.app')

            if not os.path.exists(app_path):
                raise Exception("iOS build failed - .app not found")

            # Create archive directory structure
            archive_dir = os.path.join(build_dir, 'archive')
            archive_path = os.path.join(archive_dir, f'{config["app_name"]}.xcarchive')
            products_dir = os.path.join(archive_path, 'Products', 'Applications')
            os.makedirs(products_dir, exist_ok=True)

            # Copy .app to archive
            shutil.copytree(app_path, os.path.join(products_dir, 'Runner.app'))

            # Create Info.plist for archive
            archive_info = {
                'ApplicationProperties': {
                    'ApplicationPath': 'Products/Applications/Runner.app',
                    'CFBundleIdentifier': config.get('package_name'),
                    'CFBundleShortVersionString': config.get('app_version', '1.0.0'),
                    'CFBundleVersion': str(config.get('build_number', 1)),
                    'SigningIdentity': signing_identity,
                    'Team': config.get('team_id') or profile_info.get('team_id'),
                },
                'ArchiveVersion': 2,
                'CreationDate': __import__('datetime').datetime.now(),
                'Name': config.get('app_name'),
                'SchemeName': 'Runner',
            }

            with open(os.path.join(archive_path, 'Info.plist'), 'wb') as f:
                plistlib.dump(archive_info, f)

            # Export to IPA using xcodebuild
            ipa_export_dir = os.path.join(build_dir, 'ipa_export')
            os.makedirs(ipa_export_dir, exist_ok=True)

            export_result = subprocess.run(
                [
                    'xcodebuild', '-exportArchive',
                    '-archivePath', archive_path,
                    '-exportPath', ipa_export_dir,
                    '-exportOptionsPlist', export_options_path,
                ],
                capture_output=True,
                text=True,
                timeout=300,
                env={**os.environ, 'KEYCHAIN_PATH': signer.keychain_name}
            )

            if export_result.returncode != 0:
                # If xcodebuild fails, fall back to manual IPA creation
                ipa_path = create_ipa_manually(app_path, build_dir, config, signing_identity)
                if ipa_path:
                    output_path = os.path.join(output_dir, f'{config["app_name"]}.ipa')
                    shutil.move(ipa_path, output_path)
                    return output_path
                raise Exception(f"IPA export failed: {export_result.stderr}")

            # Find the exported IPA
            for file in os.listdir(ipa_export_dir):
                if file.endswith('.ipa'):
                    output_path = os.path.join(output_dir, f'{config["app_name"]}.ipa')
                    shutil.move(os.path.join(ipa_export_dir, file), output_path)
                    return output_path

            raise Exception("IPA file not found after export")

        except Exception as e:
            raise Exception(f"iOS signed build failed: {str(e)}")


def build_macos_signed(project_dir, build_dir, config):
    """Build signed macOS app using Apple credentials"""
    output_dir = os.path.join(build_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    apple_cert_path = config.get('apple_certificate_path')
    apple_cert_password = config.get('apple_certificate_password')
    apple_profile_path = config.get('apple_provisioning_profile_path')

    with SecureAppleSigning(os.path.basename(build_dir)) as signer:
        try:
            # Create temporary keychain and import certificate
            signer.create_temporary_keychain()
            signer.import_certificate(apple_cert_path, apple_cert_password)

            # Install and validate provisioning profile (optional for macOS)
            profile_info = {}
            if apple_profile_path and os.path.exists(apple_profile_path):
                profile_info = signer.install_provisioning_profile(apple_profile_path)

            # Get signing identity
            signing_identity = signer.get_signing_identity()

            # Build the macOS app with Flutter
            build_env = {**os.environ, 'CODE_SIGN_IDENTITY': signing_identity}

            subprocess.run(
                ['flutter', 'build', 'macos', '--release'],
                cwd=project_dir,
                check=True,
                capture_output=True,
                timeout=600,
                env=build_env
            )

            # Find the .app bundle
            app_path = os.path.join(
                project_dir, 'build', 'macos', 'Build', 'Products', 'Release',
                f'{config.get("app_name", "Runner")}.app'
            )

            # Try default name if custom name not found
            if not os.path.exists(app_path):
                app_path = os.path.join(
                    project_dir, 'build', 'macos', 'Build', 'Products', 'Release', 'Runner.app'
                )

            if not os.path.exists(app_path):
                # Find any .app in the release directory
                release_dir = os.path.join(project_dir, 'build', 'macos', 'Build', 'Products', 'Release')
                for item in os.listdir(release_dir):
                    if item.endswith('.app'):
                        app_path = os.path.join(release_dir, item)
                        break

            if not os.path.exists(app_path):
                raise Exception("macOS build failed - .app not found")

            # Sign the app bundle with codesign
            subprocess.run(
                [
                    'codesign', '--force', '--deep', '--sign', signing_identity,
                    '--keychain', signer.keychain_name,
                    '--options', 'runtime',
                    app_path
                ],
                check=True,
                capture_output=True,
                timeout=120
            )

            # Verify the signature
            verify_result = subprocess.run(
                ['codesign', '--verify', '--deep', '--strict', app_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if verify_result.returncode != 0:
                raise Exception(f"Code signature verification failed: {verify_result.stderr}")

            # Create DMG or ZIP
            output_path = os.path.join(output_dir, f'{config["app_name"]}_macos_signed.zip')
            shutil.make_archive(
                output_path.replace('.zip', ''),
                'zip',
                os.path.dirname(app_path),
                os.path.basename(app_path)
            )

            return output_path

        except Exception as e:
            raise Exception(f"macOS signed build failed: {str(e)}")


def create_ipa_manually(app_path, build_dir, config, signing_identity):
    """Create IPA file manually when xcodebuild export fails"""
    try:
        ipa_dir = os.path.join(build_dir, 'ipa_manual')
        payload_dir = os.path.join(ipa_dir, 'Payload')
        os.makedirs(payload_dir, exist_ok=True)

        # Copy .app to Payload directory
        app_dest = os.path.join(payload_dir, os.path.basename(app_path))
        shutil.copytree(app_path, app_dest)

        # Create IPA (zip with .ipa extension)
        ipa_path = os.path.join(ipa_dir, f'{config["app_name"]}.ipa')

        # Use zip command for proper IPA structure
        subprocess.run(
            ['zip', '-r', '-q', ipa_path, 'Payload'],
            cwd=ipa_dir,
            check=True,
            capture_output=True,
            timeout=120
        )

        return ipa_path
    except Exception:
        return None


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
        # Check if Apple signing credentials are provided
        apple_cert_path = config.get('apple_certificate_path')
        apple_cert_password = config.get('apple_certificate_password')
        apple_profile_path = config.get('apple_provisioning_profile_path')

        if apple_cert_path and apple_cert_password and apple_profile_path and is_macos():
            # Build with code signing
            return build_ios_signed(project_dir, build_dir, config)
        else:
            # Build without code signing (for development/testing)
            subprocess.run(
                ['flutter', 'build', 'ios', '--release', '--no-codesign'],
                cwd=project_dir,
                check=True,
                capture_output=True,
                timeout=600
            )
            # Create xcarchive for unsigned build
            app_path = os.path.join(project_dir, 'build', 'ios', 'iphoneos', 'Runner.app')
            if os.path.exists(app_path):
                output_path = os.path.join(output_dir, f'{config["app_name"]}_ios_unsigned.zip')
                shutil.make_archive(output_path.replace('.zip', ''), 'zip', os.path.dirname(app_path), 'Runner.app')
                return output_path
            return None

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
        # Check if Apple signing credentials are provided
        apple_cert_path = config.get('apple_certificate_path')
        apple_cert_password = config.get('apple_certificate_password')

        if apple_cert_path and apple_cert_password and is_macos():
            # Build with code signing
            return build_macos_signed(project_dir, build_dir, config)
        else:
            # Build without code signing
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

# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    """Redirect to auth or dashboard based on session"""
    return redirect(url_for('auth_page'))

@app.route('/auth')
def auth_page():
    """Authentication page (login/signup)"""
    return render_template('auth.html', firebase_config=get_firebase_config())

@app.route('/dashboard')
def dashboard_page():
    """Dashboard page - requires authentication (checked client-side)"""
    return render_template('dashboard.html', firebase_config=get_firebase_config())

@app.route('/builder')
def builder_page():
    """Builder page - the main app builder interface"""
    return render_template('index.html', firebase_config=get_firebase_config())

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files (icons, etc.)"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/build', methods=['POST'])
def start_build():
    data = request.json

    # Validate required fields
    required_fields = ['app_name', 'app_description', 'app_version', 'build_number', 'package_name', 'web_url', 'platforms']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    if not data['platforms']:
        return jsonify({'error': 'At least one platform must be selected'}), 400

    # Generate build ID
    build_id = str(uuid.uuid4())

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
        # Keystore config (optional - Android)
        'keystore_path': data.get('keystore_path'),
        'keystore_password': data.get('keystore_password'),
        'key_alias': data.get('key_alias'),
        'key_password': data.get('key_password'),
        # Apple signing config (optional - iOS/macOS)
        'apple_certificate_path': data.get('apple_certificate_path'),
        'apple_certificate_password': data.get('apple_certificate_password'),
        'apple_provisioning_profile_path': data.get('apple_provisioning_profile_path'),
        'team_id': data.get('team_id'),
        # Icon config (optional)
        'icon_path': data.get('icon_path')
    }

    thread = threading.Thread(target=run_build, args=(build_id, config))
    thread.start()

    return jsonify({'build_id': build_id})

@app.route('/api/build/<build_id>/status')
def get_build_status(build_id):
    if build_id not in build_progress:
        return jsonify({'error': 'Build not found'}), 404

    return jsonify(build_progress[build_id])

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


# ==================== APPLE SIGNING API ENDPOINTS ====================

@app.route('/api/upload/apple-certificate', methods=['POST'])
def upload_apple_certificate():
    """Upload and validate Apple distribution certificate (.p12)"""
    if not is_macos():
        return jsonify({'error': 'Apple signing is only available on macOS'}), 400

    if 'certificate' not in request.files:
        return jsonify({'error': 'No certificate file provided'}), 400

    file = request.files['certificate']
    password = request.form.get('password', '')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.p12', '.pfx']:
        return jsonify({'error': 'Invalid file type. Use .p12 or .pfx file'}), 400

    # Save to secure temp location first for validation
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{uuid.uuid4()}{ext}")
    file.save(temp_path)

    try:
        # Validate the certificate
        validation = validate_apple_certificate(temp_path, password)

        if not validation['valid']:
            os.remove(temp_path)
            return jsonify({'error': validation['error']}), 400

        # Move to permanent location with unique name
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.rename(temp_path, filepath)

        return jsonify({
            'success': True,
            'filename': filename,
            'path': filepath,
            'info': validation.get('info', {})
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': f'Certificate validation failed: {str(e)}'}), 500


@app.route('/api/upload/provisioning-profile', methods=['POST'])
def upload_provisioning_profile():
    """Upload and validate Apple provisioning profile"""
    if not is_macos():
        return jsonify({'error': 'Apple signing is only available on macOS'}), 400

    if 'profile' not in request.files:
        return jsonify({'error': 'No provisioning profile provided'}), 400

    file = request.files['profile']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file extension
    if not file.filename.endswith('.mobileprovision'):
        return jsonify({'error': 'Invalid file type. Use .mobileprovision file'}), 400

    # Save to temp location for validation
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{uuid.uuid4()}.mobileprovision")
    file.save(temp_path)

    try:
        # Create temporary signing handler to validate profile
        with SecureAppleSigning('validation') as signer:
            profile_info = signer.validate_provisioning_profile(temp_path)

        # Move to permanent location
        filename = f"{uuid.uuid4()}.mobileprovision"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.rename(temp_path, filepath)

        # Sanitize profile info for JSON response
        response_info = {
            'uuid': profile_info.get('uuid'),
            'name': profile_info.get('name'),
            'team_id': profile_info.get('team_id'),
            'app_bundle_id': profile_info.get('app_bundle_id'),
            'platform': profile_info.get('platform'),
            'is_development': profile_info.get('is_development', False),
        }

        # Handle datetime serialization
        if profile_info.get('expiration_date'):
            response_info['expiration_date'] = profile_info['expiration_date'].isoformat()

        return jsonify({
            'success': True,
            'filename': filename,
            'path': filepath,
            'info': response_info
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 400


@app.route('/api/apple/check-platform', methods=['GET'])
def check_apple_platform():
    """Check if Apple signing is available (macOS only)"""
    return jsonify({
        'available': is_macos(),
        'platform': platform.system(),
        'message': 'Apple signing is available' if is_macos() else 'Apple signing requires macOS'
    })

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
            # Apple signing info (credentials only, files stored separately)
            'apple_certificate_password': data.get('apple_certificate_password', ''),
            'team_id': data.get('team_id', ''),
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

        # Copy Apple certificate if provided
        apple_cert_path = data.get('apple_certificate_path')
        if apple_cert_path and os.path.exists(apple_cert_path):
            ext = os.path.splitext(apple_cert_path)[1]
            shutil.copy(apple_cert_path, os.path.join(assets_dir, f'certificate{ext}'))

        # Copy Apple provisioning profile if provided
        apple_profile_path = data.get('apple_provisioning_profile_path')
        if apple_profile_path and os.path.exists(apple_profile_path):
            shutil.copy(apple_profile_path, os.path.join(assets_dir, 'profile.mobileprovision'))

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

        # Copy Apple certificate to uploads if exists
        for ext in ['.p12', '.pfx']:
            apple_cert_path = os.path.join(assets_dir, f'certificate{ext}')
            if os.path.exists(apple_cert_path):
                new_cert_name = f"{uuid.uuid4()}{ext}"
                new_cert_path = os.path.join(app.config['UPLOAD_FOLDER'], new_cert_name)
                shutil.copy(apple_cert_path, new_cert_path)
                response_data['apple_certificate_path'] = new_cert_path
                break

        # Copy Apple provisioning profile to uploads if exists
        apple_profile_path = os.path.join(assets_dir, 'profile.mobileprovision')
        if os.path.exists(apple_profile_path):
            new_profile_name = f"{uuid.uuid4()}.mobileprovision"
            new_profile_path = os.path.join(app.config['UPLOAD_FOLDER'], new_profile_name)
            shutil.copy(apple_profile_path, new_profile_path)
            response_data['apple_provisioning_profile_path'] = new_profile_path

            # Validate and extract profile info for UI
            try:
                with SecureAppleSigning('project_open') as signer:
                    profile_info = signer.validate_provisioning_profile(new_profile_path)
                    response_data['apple_profile_info'] = {
                        'uuid': profile_info.get('uuid'),
                        'name': profile_info.get('name'),
                        'team_id': profile_info.get('team_id'),
                        'app_bundle_id': profile_info.get('app_bundle_id'),
                    }
                    if profile_info.get('expiration_date'):
                        response_data['apple_profile_info']['expiration_date'] = profile_info['expiration_date'].isoformat()
            except Exception:
                pass  # Profile info extraction is optional

        return jsonify({'success': True, 'project': response_data})

    except Exception as e:
        return jsonify({'error': f'Failed to open project: {str(e)}'}), 500

    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

# ==================== FIRESTORE PROJECT API ====================

@app.route('/api/projects', methods=['GET'])
@firebase_auth_required
def get_projects():
    """Get all projects for the authenticated user"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']
        projects_ref = db.collection('projects')
        query = projects_ref.where('userId', '==', user_id).order_by('updatedAt', direction=firestore.Query.DESCENDING)
        docs = query.stream()

        projects = []
        for doc in docs:
            project = doc.to_dict()
            project['id'] = doc.id
            # Convert timestamps to ISO format
            if project.get('createdAt'):
                project['createdAt'] = project['createdAt'].isoformat() if hasattr(project['createdAt'], 'isoformat') else str(project['createdAt'])
            if project.get('updatedAt'):
                project['updatedAt'] = project['updatedAt'].isoformat() if hasattr(project['updatedAt'], 'isoformat') else str(project['updatedAt'])
            projects.append(project)

        return jsonify({'projects': projects})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch projects: {str(e)}'}), 500

@app.route('/api/projects', methods=['POST'])
@firebase_auth_required
def create_project():
    """Create a new project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']
        data = request.json

        if not data:
            return jsonify({'error': 'No project data provided'}), 400

        # Log received data for debugging
        print(f"Creating project for user {user_id}")
        print(f"Received data: {data}")

        project_data = {
            'userId': user_id,
            'name': data.get('name', 'Untitled Project'),
            'webUrl': data.get('webUrl', ''),
            'description': data.get('description', ''),
            'appVersion': data.get('appVersion', '1.0.0'),
            'buildNumber': data.get('buildNumber', 1),
            'packageName': data.get('packageName', ''),
            'iconUrl': data.get('iconUrl', ''),
            'settings': data.get('settings', {
                'allowZoom': True,
                'enableJavascript': True,
                'enableDomStorage': True,
                'enableGeolocation': True,
                'enablePullRefresh': True,
                'showNavigation': True,
                'enableFileAccess': True,
                'enableCache': True,
                'enableMediaAutoplay': False
            }),
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP
        }

        print(f"Saving project_data to Firestore: {project_data}")
        doc_ref = db.collection('projects').add(project_data)
        project_id = doc_ref[1].id
        print(f"Project saved with ID: {project_id}")

        return jsonify({'success': True, 'projectId': project_id})
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to create project: {str(e)}'}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
@firebase_auth_required
def get_project(project_id):
    """Get a specific project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']
        doc_ref = db.collection('projects').document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({'error': 'Project not found'}), 404

        project = doc.to_dict()

        # Verify ownership
        if project.get('userId') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        project['id'] = doc.id
        if project.get('createdAt'):
            project['createdAt'] = project['createdAt'].isoformat() if hasattr(project['createdAt'], 'isoformat') else str(project['createdAt'])
        if project.get('updatedAt'):
            project['updatedAt'] = project['updatedAt'].isoformat() if hasattr(project['updatedAt'], 'isoformat') else str(project['updatedAt'])

        return jsonify({'project': project})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch project: {str(e)}'}), 500

@app.route('/api/projects/<project_id>', methods=['PUT'])
@firebase_auth_required
def update_project(project_id):
    """Update a project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']
        data = request.json

        if not data:
            return jsonify({'error': 'No project data provided'}), 400

        print(f"Updating project {project_id} for user {user_id}")
        print(f"Received data: {data}")

        doc_ref = db.collection('projects').document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({'error': 'Project not found'}), 404

        project = doc.to_dict()
        if project.get('userId') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        # Update allowed fields
        update_data = {'updatedAt': firestore.SERVER_TIMESTAMP}
        allowed_fields = ['name', 'webUrl', 'description', 'appVersion', 'buildNumber',
                          'packageName', 'iconUrl', 'settings', 'keystoreData', 'appleData']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]

        print(f"Updating with data: {update_data}")
        doc_ref.update(update_data)
        print(f"Project {project_id} updated successfully")

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating project: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to update project: {str(e)}'}), 500

@app.route('/api/projects/<project_id>', methods=['DELETE'])
@firebase_auth_required
def delete_project(project_id):
    """Delete a project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']

        doc_ref = db.collection('projects').document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({'error': 'Project not found'}), 404

        project = doc.to_dict()
        if project.get('userId') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        doc_ref.delete()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Failed to delete project: {str(e)}'}), 500

@app.route('/api/projects/<project_id>/download', methods=['GET'])
@firebase_auth_required
def download_project_swab(project_id):
    """Download project as .swab file"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']

        doc_ref = db.collection('projects').document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({'error': 'Project not found'}), 404

        project = doc.to_dict()
        if project.get('userId') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        # Create .swab file from project data
        temp_dir = tempfile.mkdtemp()

        try:
            # Prepare project data for .swab file
            project_data = {
                'app_name': project.get('name', 'Untitled'),
                'app_description': project.get('description', ''),
                'app_version': project.get('appVersion', '1.0.0'),
                'build_number': project.get('buildNumber', 1),
                'package_name': project.get('packageName', ''),
                'web_url': project.get('webUrl', ''),
            }

            # Add settings
            settings = project.get('settings', {})
            project_data.update({
                'allow_zoom': settings.get('allowZoom', True),
                'enable_javascript': settings.get('enableJavascript', True),
                'enable_dom_storage': settings.get('enableDomStorage', True),
                'enable_geolocation': settings.get('enableGeolocation', True),
                'enable_pull_refresh': settings.get('enablePullRefresh', True),
                'show_navigation': settings.get('showNavigation', True),
                'enable_file_access': settings.get('enableFileAccess', True),
                'enable_cache': settings.get('enableCache', True),
                'enable_media_autoplay': settings.get('enableMediaAutoplay', False),
            })

            # Save project.json
            project_json_path = os.path.join(temp_dir, 'project.json')
            with open(project_json_path, 'w') as f:
                json.dump(project_data, f, indent=2)

            # Create assets directory
            assets_dir = os.path.join(temp_dir, 'assets')
            os.makedirs(assets_dir, exist_ok=True)

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
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', project.get('name', 'project'))
            filename = f"{safe_name}.swab"

            # Save encrypted file
            output_path = os.path.join(temp_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)

            return send_file(
                output_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/octet-stream'
            )
        finally:
            # Cleanup will happen after response is sent
            pass

    except Exception as e:
        return jsonify({'error': f'Failed to download project: {str(e)}'}), 500

@app.route('/api/projects/import', methods=['POST'])
@firebase_auth_required
def import_project_swab():
    """Import a .swab file as a new project"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    if 'project' not in request.files:
        return jsonify({'error': 'No project file provided'}), 400

    file = request.files['project']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.swab'):
        return jsonify({'error': 'Invalid file type. Please select a .swab file'}), 400

    temp_dir = tempfile.mkdtemp()

    try:
        user_id = request.user['uid']

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

        # Create new project in Firestore
        firestore_data = {
            'userId': user_id,
            'name': project_data.get('app_name', 'Imported Project'),
            'webUrl': project_data.get('web_url', ''),
            'description': project_data.get('app_description', ''),
            'appVersion': project_data.get('app_version', '1.0.0'),
            'buildNumber': project_data.get('build_number', 1),
            'packageName': project_data.get('package_name', ''),
            'iconUrl': '',
            'settings': {
                'allowZoom': project_data.get('allow_zoom', True),
                'enableJavascript': project_data.get('enable_javascript', True),
                'enableDomStorage': project_data.get('enable_dom_storage', True),
                'enableGeolocation': project_data.get('enable_geolocation', True),
                'enablePullRefresh': project_data.get('enable_pull_refresh', True),
                'showNavigation': project_data.get('show_navigation', True),
                'enableFileAccess': project_data.get('enable_file_access', True),
                'enableCache': project_data.get('enable_cache', True),
                'enableMediaAutoplay': project_data.get('enable_media_autoplay', False)
            },
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP
        }

        doc_ref = db.collection('projects').add(firestore_data)
        project_id = doc_ref[1].id

        return jsonify({'success': True, 'projectId': project_id})

    except Exception as e:
        return jsonify({'error': f'Failed to import project: {str(e)}'}), 500

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# ==================== BUILD HISTORY API ====================

@app.route('/api/builds', methods=['GET'])
@firebase_auth_required
def get_builds():
    """Get build history for the authenticated user"""
    if not db:
        return jsonify({'error': 'Database not available'}), 503

    try:
        user_id = request.user['uid']
        builds_ref = db.collection('builds')
        query = builds_ref.where('userId', '==', user_id).order_by('createdAt', direction=firestore.Query.DESCENDING).limit(50)
        docs = query.stream()

        builds = []
        for doc in docs:
            build = doc.to_dict()
            build['id'] = doc.id
            if build.get('createdAt'):
                build['createdAt'] = build['createdAt'].isoformat() if hasattr(build['createdAt'], 'isoformat') else str(build['createdAt'])
            builds.append(build)

        return jsonify({'builds': builds})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch builds: {str(e)}'}), 500

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='SWAB - Simple Web App Builder')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run the server on (default: 5000)')
    args = parser.parse_args()
    app.run(debug=True, port=args.port)
