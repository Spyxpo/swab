'''
Author: Mantresh Khurana | Spyxpo
Project Name: Spyxpo Web To App Builder
Project Description: This is a tool which is used to convert a website into an app for iOS, Android, Windows, macOS and Linux.
'''

from tkinter import *
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import shutil
import os
import platform
import webbrowser
from PIL import Image
import icnsutil
import wget
import userpath
import zipfile
import subprocess

running_on = platform.system()

if running_on == 'Darwin':
    print("Running on macOS")
elif running_on == 'Linux':
    print("Running on Linux")
elif running_on == 'Windows':
    print("Running on Windows")
else:
    print("Platform can't be detected.")            

def clear():
    if running_on == 'Darwin':
        os.system('clear')
    elif running_on == 'Linux':
        os.system('clear')
    elif running_on == 'Windows':
        os.system('cls')
    else:
        pass

clear()

# packages version details
packages_version_info = open('.packages', 'r')
flutter_version = packages_version_info.readlines()[0]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_requirements(name, success_text, error_text):
    if running_on == 'Windows':
        program = subprocess.call(['where', name])
        if program == 0:
            print(f'{bcolors.OKGREEN}{success_text}\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}{error_text}\n')
            print(f'{bcolors.FAIL}Please install \"{name}\" then try again.\n')
            exit()
    else:        
        program = subprocess.call(['which', name])
        if program == 0:
            print(f'{bcolors.OKGREEN}{success_text}\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}{error_text}\n')
            print(f'{bcolors.FAIL}Please install \"{name}\" then set PATH and try again.\n')
            input(f'{bcolors.ENDC}Press ENTER to exit.')
            exit()
        
def check_flutter():
    if running_on == 'Windows':
        flutter = subprocess.call(['where', 'flutter'])
        if flutter == 0:
            print(f'{bcolors.OKGREEN}Flutter is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Flutter is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"flutter\" then set PATH and try again.\n')
            
            url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_{flutter_version}-stable.zip"
            print(f"{bcolors.OKGREEN}Downloading FLutter for Windows...")
            wget.download(url, 'flutter.zip')
            print("Extracting Flutter.....")
            with zipfile.ZipFile('flutter.zip', "r") as zip_ref:
                zip_ref.extractall("C:\\")
            location = "C:\\flutter\\bin"
            userpath.append(location)
            os.remove('flutter.zip')
            #os.system('setx /M path "%path%;C:\\flutter\\bin"')
            print("Flutter installed successfully.")
        
    else:
        program = subprocess.call(['which', 'flutter'])
        if program == 0:
            print(f'{bcolors.OKGREEN}Flutter is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Flutter is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"flutter\" then set PATH and try again.\n')
          
            if platform == 'Darwin':
                url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_{flutter_version}-stable.zip"
                print("Downloading FLutter for macOS...")
                wget.download(url, 'flutter.zip')
                print("Extracting Flutter.....")
                with zipfile.ZipFile('flutter.zip', "r") as zip_ref:
                    zip_ref.extractall("/Users/")
                location = "/Users/flutter/bin"
                userpath.append(location)
                os.remove('flutter.zip')
                print("Flutter installed successfully.")      
            elif platform == 'Linux':
                url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_{flutter_version}-stable.tar.xz"
                print("Downloading FLutter for Linux...")
                wget.download(url, 'flutter.tar.xz')
                print("Extracting Flutter.....")
                os.system('tar xf flutter.tar.xz')
                location = os.getcwd() + "/flutter/bin"
                userpath.append(location)
                os.remove('flutter.tar.xz')
                print("Flutter installed successfully.")
            else:
                pass
  
if running_on == 'Windows':
    pass
elif running_on == 'Darwin':
    check_requirements('python3', 'Python is already installed.', 'Python is not in the PATH or is installed on this device.')
elif running_on == 'Linux':
    check_requirements('python3', 'Python is already installed.', 'Python is not in the PATH or is installed on this device.')
else:
    pass

if running_on == 'Windows':
    try:
        check_requirements('python', 'Python is already installed.', 'Python is not in the PATH or is installed on this device.')
    except:
        check_requirements('python3', 'Python is already installed.', 'Python is not in the PATH or is installed on this device.')
    else:
        pass
else:
    pass

check_flutter()
check_requirements('node', 'NodeJS is already installed.', 'NodeJS is not in the PATH or is installed on this device.')
check_requirements('java', 'JRE is already installed.', 'JRE is not in the PATH or is installed on this device.')
check_requirements('javac', 'JDK is already installed.', 'JDK is not in the PATH or is installed on this device.')
check_requirements('git', 'Git is already installed.', 'Git is not in the PATH or is installed on this device.')
check_requirements('android', 'Android Studio is already installed.', 'Android Studio is not in the PATH or is installed on this device.')

if os.path.exists("assets"):
    pass
else:
    os.mkdir("assets")

if os.path.exists("assets/favicon.png"):
    os.remove("assets/favicon.png")
else:
    pass

if os.path.exists("assets/favicon.ico"):
    os.remove("assets/favicon.ico")
else:
    pass

if os.path.exists("assets/favicon.icns"):
    os.remove("assets/favicon.icns")
else:
    pass

if os.path.exists("assets/key.properties"):
    os.remove("assets/key.properties")
else:
    pass

def remove_assets():
    if os.path.exists("assets"):
        shutil.rmtree("assets")
        print(f"{bcolors.ENDC}Assets folder cleaned.")
    else:
        pass   

def remove_projects():
    if os.path.exists("projects"):
        shutil.rmtree("projects")
        print(f"{bcolors.ENDC}Projects folder cleaned.")
    else:
        pass

def remove_pycache():
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print(f"{bcolors.ENDC}Pycache folder cleaned.")
    else:
        pass   

def remove_dist():
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("Dist folder cleaned.")
    else:
        pass   

def remove_run_spec():
    if os.path.exists("run.spec"):
        os.remove("run.spec")   
    else:
        pass    

def clean_dir():
    remove_assets()
    remove_projects()
    remove_pycache()
    remove_dist()
    remove_run_spec()
    
def clean_build():
    try:

        if os.path.exists("build"):
            shutil.rmtree("build/")
            print("Build folder cleaned.")
        else:
            pass

    except Exception as e:
        print(e)
        pass

def openBuildfolder():
    if running_on == 'Darwin':
        os.system('open build')
    elif running_on == 'Linux':
        os.system('open build')
    elif running_on == 'Windows':
        os.system('start build')
    else:
        pass

def uploadIconAction(event=None):
    app_name_info = app_name.get()

    if app_name_info == "":
        showinfo("No app name", "No app name, please enter an app name.")
        return False
    else:
        pass

    app_name_info = app_name.get()
    icon = filedialog.askopenfilename(filetypes=[("png files", "*.png")])
    print(f'{bcolors.ENDC}Icon image: {icon}')
    
    if icon == '':
        pass
    else:
        size = 512, 512
        image = Image.open(icon)
        image_resized = image.resize(size)
        image_resized.save("assets/favicon.png", "PNG")

        ico = Image.open('assets/favicon.png')
        ico.save('assets/favicon.ico')

        icns = icnsutil.IcnsFile()
        icns.add_media(file='assets/favicon.png')
        icns.write('assets/favicon.icns')

def uploadKeystoreAction():
    app_name_info = app_name.get()

    if app_name_info == "":
        showinfo("No app name", "No app name, please enter an app name.")
        return False
    else:
        pass

    app_name_info = app_name.get()
    store_pass_info = store_pass.get()
    key_pass_info = key_pass.get()
    alias_info = alias.get()
    keystore_path = filedialog.askopenfilename(filetypes=[("keystore files", "*.jks")])
    print('Keystore file:', keystore_path)

    key_file = open('assets/key.properties', 'w')
    key_file.write(f'storeFile={keystore_path}\n')
    key_file.close()

def saveData():

    app_name_info = app_name.get()
    app_description_info = app_description.get()
    app_package_info = app_package_name.get().lower()
    app_version_info = app_version.get()
    app_build_info = app_build_number.get()
    app_web_url = web_url.get().lower()
    key_alias_info = alias.get()
    key_pass_info = key_pass.get()
    store_pass_info = store_pass.get()

    if os.path.exists("projects"):
        pass
    else:
        os.mkdir("projects")

    if os.path.exists(f"build/{app_name_info}_{app_version_info}.apk"):
        os.remove(f"build/{app_name_info}_{app_version_info}.apk")
    else:
        pass

    if os.path.exists(f"build/{app_name_info}_{app_version_info}.aab"):
        os.remove(f"build/{app_name_info}_{app_version_info}.aab")
    else:
        pass

    if app_name_info == "":
        showinfo("No app name", "No app name, please enter an app name.")
        return False
    else:
        pass

    if app_build_info.isnumeric():
        pass
    else:
        showinfo("Build Number", "Build Number must be a number.")
        return False

    if os.path.exists("assets/favicon.png"):
        pass
    else:
        showinfo("No icon selected", "No icon selected, please select an icon for your app.")
        return False
    
    if os.path.exists("assets/key.properties"):
        pass
    else:
        showinfo("No keystore selected", "No keystore selected, please select a keystore for your app.")
        return False    

    if app_description_info == "":
        showinfo("No description", "No description, please enter a description.")
        return False
    elif app_package_info == "":
        showinfo("No package name",
                 "No package name, please enter a package name.")
        return False
    elif app_version_info == "":
        showinfo("No version", "No version, please enter a version.")
        return False
    elif app_build_info == "":
        showinfo("No build number",
                 "No build number, please enter a build number.")
        return False
    elif app_web_url == "":
        showinfo("No web url", "No web url, please enter a web url.")
        return False
    elif os.path.exists(f"projects/{app_name_info}/mobile"):
        showinfo("App already exists",
                 "App already exists, please try another name for your app.")
        return False 
    elif key_alias_info == "":
        showinfo("Keystore Alias",
                 "Keystore alias is required.")
        return False
    elif key_pass_info == "":
        showinfo("Keystore Key Password",
                 "Keystore key password is required.")
        return False
    elif store_pass_info == "":
        showinfo("Keystore Password",
                 "Keystore password is required.")
        return False       
    else:
        shutil.copytree("template/mobile", f"projects/{app_name_info}/mobile")
        shutil.copytree("template/desktop", f"projects/{app_name_info}/desktop")
    
    key_file = open('assets/key.properties', 'a+')
    key_file.write(f'storePassword={store_pass_info}\nkeyPassword={key_pass_info}\nkeyAlias={key_alias_info}\n')
    key_file.close()

    shutil.copy('assets/favicon.png',
                    f'projects/{app_name_info}/mobile/assets/images/favicon.png')    

    shutil.copy('assets/favicon.ico',
                    f'projects/{app_name_info}/desktop/assets/icons/win/favicon.ico')    

    shutil.copy('assets/favicon.icns',
                    f'projects/{app_name_info}/desktop/assets/icons/mac/favicon.icns')    

    shutil.copy('assets/favicon.png',
                    f'projects/{app_name_info}/desktop/assets/icons/png/favicon.png')    

    shutil.copy('assets/key.properties',
                    f'projects/{app_name_info}/mobile/android/key.properties')                        
                
    # add app name in main.dart
    with open(f'projects/{app_name_info}/mobile/lib/main.dart')as main_file:
        name = main_file.read().replace("APP_NAME", str(app_name_info), 1)

    with open(f'projects/{app_name_info}/mobile/lib/main.dart', "w") as new_main_file:
        new_main_file.write(name)

    # add ios package name in main.dart
    with open(f'projects/{app_name_info}/mobile/lib/main.dart')as main_file_ios_package_name:
        ios_package_name = main_file_ios_package_name.read().replace("IOS_APP_ID", str(app_package_info), 1)

    with open(f'projects/{app_name_info}/mobile/lib/main.dart', "w") as new_main_file_ios_package_name:
        new_main_file_ios_package_name.write(ios_package_name)

    # add android package name in main.dart
    with open(f'projects/{app_name_info}/mobile/lib/main.dart')as main_file_android_package_name:
        android_package_name = main_file_android_package_name.read().replace("ANDROID_PACKAGE_NAME", str(app_package_info), 1)

    with open(f'projects/{app_name_info}/mobile/lib/main.dart', "w") as new_main_file_android_package_name:
        new_main_file_android_package_name.write(android_package_name)

    # add deep link in Android projects
    with open(f'projects/{app_name_info}/mobile/android/app/src/main/AndroidManifest.xml')as deep_link_url_name:
        deep_link_url = deep_link_url_name.read().replace("website.com", str(app_web_url), 1)

    with open(f'projects/{app_name_info}/mobile/android/app/src/main/AndroidManifest.xml', "w") as new_deep_link_url_name:
        new_deep_link_url_name.write(deep_link_url)

    # add app website url in main.dart
    with open(f'projects/{app_name_info}/mobile/lib/main.dart')as home_file:
        website_name = home_file.read().replace("WEBSITE", str(app_web_url), 1)

    with open(f'projects/{app_name_info}/mobile/lib/main.dart', "w") as new_home_file:
        new_home_file.write(website_name)

    # add android app package name in main.dart
    with open(f'projects/{app_name_info}/mobile/lib/main.dart')as android_package_name_file:
        android_package_name = android_package_name_file.read().replace("ANDROID_PACKAGE_NAME", str(app_web_url), 1)

    with open(f'projects/{app_name_info}/mobile/lib/main.dart', "w") as new_android_package_name_file:
        new_android_package_name_file.write(android_package_name)    

    # add project name in pubspec.yaml
    with open(f'projects/{app_name_info}/mobile/pubspec.yaml')as pubspec_file:
        new_app_name_info = app_name_info.replace(" ", "")
        new_name = pubspec_file.read().replace("APP_NAME", str(new_app_name_info), 1)

    with open(f'projects/{app_name_info}/mobile/pubspec.yaml', "w") as new_pubspec_file:
        new_pubspec_file.write(new_name)

    # add app description in pubspec.yaml
    with open(f'projects/{app_name_info}/mobile/pubspec.yaml')as pubspec_file_description:
        description = pubspec_file_description.read().replace(
            "DESCRIPTION", str(app_description_info), 1)

    with open(f'projects/{app_name_info}/mobile/pubspec.yaml', "w") as new_pubspec_file_description:
        new_pubspec_file_description.write(description)

    # add app name in pubspec.yaml
    with open(f'projects/{app_name_info}/mobile/pubspec.yaml') as pubspec_file_name:
        new_app_name = pubspec_file_name.read().replace(
            "APP_NAME", f"{app_name_info}", 1)

    with open(f'projects/{app_name_info}/mobile/pubspec.yaml', "w") as new_pubspec_file_name:
        new_pubspec_file_name.write(new_app_name)

    pubspec_file = open(f"projects/{app_name_info}/mobile/pubspec.yaml", "r")
    list_of_lines = pubspec_file.readlines()
    list_of_lines[5] = f"version: {app_version_info}+{app_build_info}" + "\n"

    pubspec_file = open(f"projects/{app_name_info}/mobile/pubspec.yaml", "w")
    pubspec_file.writelines(list_of_lines)
    pubspec_file.close()

    readme_file = open(f"projects/{app_name_info}/mobile/README.md", "w")
    readme_file.write(
        f"{app_name_info}\n{app_package_info}\n{app_version_info}\n{app_build_info}")
    readme_file.close()

    # for desktop app

     # add app name in package.json
    with open(f'projects/{app_name_info}/desktop/package.json')as desktop_name_file:
        desktop_name = desktop_name_file.read().replace("app_name", str(app_name_info).lower(), 1)

    with open(f'projects/{app_name_info}/desktop/package.json', "w") as new_desktop_name_file:
        new_desktop_name_file.write(desktop_name)

     # add website url in index.html
    with open(f'projects/{app_name_info}/desktop/index.html')as desktop_url_file:
        desktop_url = desktop_url_file.read().replace("WEBSITE", str(app_web_url), 1)

    with open(f'projects/{app_name_info}/desktop/index.html', "w") as new_desktop_url_file:
        new_desktop_url_file.write(desktop_url)
        
    # add app name in package.json
    with open(f'projects/{app_name_info}/desktop/package.json')as desktop_name_file_2:
        desktop_name_2 = desktop_name_file_2.read().replace("APP_NAME", str(app_name_info), 1)

    with open(f'projects/{app_name_info}/desktop/package.json', "w") as new_desktop_name_file_2:
        new_desktop_name_file_2.write(desktop_name_2)    

    # add app version in package.json
    with open(f'projects/{app_name_info}/desktop/package.json')as desktop_version_file:
        desktop_version = desktop_version_file.read().replace("VERSION", str(app_version_info), 1)

    with open(f'projects/{app_name_info}/desktop/package.json', "w") as new_desktop_version_file:
        new_desktop_version_file.write(desktop_version)    

    # add app description in package.json
    with open(f'projects/{app_name_info}/desktop/package.json')as desktop_description_file:
        desktop_description = desktop_description_file.read().replace("DESCRIPTION", str(app_description_info), 1)

    with open(f'projects/{app_name_info}/desktop/package.json', "w") as new_desktop_description_file:
        new_desktop_description_file.write(desktop_description)    

     # add app name in view.js
    with open(f'projects/{app_name_info}/desktop/src/view.js')as desktop_view_file:
        desktop_view = desktop_view_file.read().replace("WEBSITE", str(app_web_url), 1)

    with open(f'projects/{app_name_info}/desktop/src/view.js', "w") as new_desktop_view_file:
        new_desktop_view_file.write(desktop_view)

    os.chdir(f"projects/{app_name_info}/mobile/")

    os.system("flutter clean")  # clean the project

    os.system("flutter pub get")  # install plugin
    os.system("flutter pub run flutter_app_name")  # change app name
        
    os.system("flutter pub get")  # install plugins
    os.system(
        f"flutter pub run change_app_package_name:main {app_package_info}")  # change app package name

    os.system("flutter pub get")  # install plugin
    os.system("flutter pub run flutter_launcher_icons:main")  # change app icon
    
    os.system("flutter pub get")  # install plugin
    os.system("flutter pub run splash_screen_view:create")  # change splash screen

    os.system("flutter build apk --release")
    os.system("flutter build appbundle --release")

    os.chdir(os.path.dirname(os.getcwd()))

    os.chdir("desktop/")

    os.system("npm install")

    if (running_on == "Darwin"):
        os.system("npm run package-mac -y")
    else:
        pass

    if (running_on == "Windows"):
        os.system("npm run package-win -y")
    else:
        pass

    if (running_on == "Linux"):
        os.system("npm run package-linux -y")
    else:
        pass

    os.chdir(os.path.dirname(os.getcwd()))
    os.chdir(os.path.dirname(os.getcwd()))
    os.chdir(os.path.dirname(os.getcwd()))
    
    if os.path.exists("build"):
        pass
    else:
        os.mkdir("build")

    if os.path.exists(f"build/{app_name_info}"):
        print('Build already exists.')
        pass
    else:
        os.mkdir(f"build/{app_name_info}")

    original_build_location_apk = (r'projects/' + app_name_info +
                               r'/mobile/build/app/outputs/apk/release/app-release.apk') 
    target_build_location_apk = (r'build/' + app_name_info +
                             r'/' + app_name_info + r'_' + app_version_info + r'_android' + r'.apk')  

    original_build_location_aab = (r'projects/' + app_name_info +
                               r'/mobile/build/app/outputs/bundle/release/app-release.aab') 
    target_build_location_aab = (r'build/' + app_name_info +
                             r'/' + app_name_info + r'_' + app_version_info + r'_android' + r'.aab')                  

    mac_desktop_original_build_location = (r'projects/' + app_name_info +
                               r'/desktop/release-builds/' + app_name_info + r'-darwin-x64/' + app_name_info + r'.app')  
    mac_desktop_target_build_location = (r'build/' + app_name_info +
                             r'/' + app_name_info + r'_' + app_version_info + r'_macos' +  r'.app') 

    win_desktop_original_build_location = (r'projects/' + app_name_info +
                               r'/desktop/release-builds/' + app_name_info + r'-win32-x64/')  
    win_desktop_target_build_location = (r'build/' + app_name_info +
                             r'/' + app_name_info + r'_' + app_version_info + r'_windows_x64') 

    linux_desktop_original_build_location = (r'projects/' + app_name_info +
                               r'/desktop/release-builds/' + app_name_info + r'-linux-x64/')  
    linux_desktop_target_build_location = (r'build/' + app_name_info +
                             r'/' + app_name_info + r'_' + app_version_info + r'_linux_x64') 

    # copy original app to new location
    shutil.copyfile(original_build_location_apk, target_build_location_apk)
    shutil.copyfile(original_build_location_aab, target_build_location_aab)

    if (running_on == "Darwin"):
        shutil.copytree(mac_desktop_original_build_location, mac_desktop_target_build_location)
    else:
        pass
    
    if (running_on == "Windows"):
        shutil.copytree(win_desktop_original_build_location, win_desktop_target_build_location)
    else:
        pass

    if (running_on == "Linux"):
        shutil.copytree(linux_desktop_original_build_location, linux_desktop_target_build_location)
    else:
        pass
    # remove existing project files, updating existing projects coming soon
    shutil.rmtree(f"projects/{app_name_info}/")

    if os.path.exists("assets/favicon.png"):
        os.remove("assets/favicon.png")
    else:
        pass

    if os.path.exists("assets/favicon.ico"):
        os.remove("assets/favicon.ico")
    else:
        pass

    if os.path.exists("assets/favicon.icns"):
        os.remove("assets/favicon.icns")
    else:
        pass

    if os.path.exists("assets/key.properties"):
        os.remove("assets/key.properties")
    else:
        pass

    clear()

    print(
        f"Your apk is located in \"/build/{app_name_info}/{app_name_info}_{app_version_info}.apk\"\n")
    print(
        f"Your appBundle is located in \"/build/{app_name_info}/{app_name_info}_{app_version_info}.aab\"\n")

    if (running_on == "Darwin"):
        print(f"Your mac app is located in \"/build/{app_name_info}/{app_name_info}_{app_version_info}.app\"\n")
    else:
        pass

    if (running_on == "Windows"):
        print(f"Your windows app is located in \"/build/{app_name_info}/{app_name_info}_{app_version_info}_windows_x64\"\n")
    else:
        pass
    
    if (running_on == "Linux"):
        print(f"Your linux app is located in \"/build/{app_name_info}/{app_name_info}_{app_version_info}_linux_x64\"\n")
    else:
        pass

    openBuildfolder()

# version details
version_info = open('VERSION', 'r')
version = version_info.read()

# tkinter ui
root = tk.Tk()
icon = PhotoImage(file = 'images/logo.png')
root.iconphoto(False, icon)
root.title('Spyxpo Web To App Builder | ' + version)
root.geometry('480x670')
root.resizable(0, 0)

menubar = Menu(root)
root.config(menu=menubar)
file_menu = Menu(menubar,tearoff=False)
commands_menu = Menu(menubar, tearoff=False)
help_menu = Menu(menubar, tearoff=False)

# file menu item
menubar.add_cascade(
    label="File",
    menu=file_menu,
    underline=0
)

file_menu.add_command(
    label='Open Build Folder',
    command=lambda: openBuildfolder(),
)

file_menu.add_separator()

file_menu.add_command(
    label='Exit',
    command=root.destroy,
)

# run menu item
menubar.add_cascade(
    label="Commands",
    menu=commands_menu
)
commands_menu.add_command(
    label='Build',
    command=lambda: saveData(),
)
commands_menu.add_command(
    label='Clean',
    command=lambda: clean_dir(),
)
commands_menu.add_command(
    label='Clean Build',
    command=lambda: clean_build(),
)

# help menu item
menubar.add_cascade(
    label="About",
    menu=help_menu
)
help_menu.add_command(
    label='Visit Website',
    command=lambda: webbrowser.open('https://www.spyxpo.com'),
)
help_menu.add_separator()
help_menu.add_command(
    label='Changelog',
    command=lambda: webbrowser.open('https://github.com/Spyxpo/swab/blob/stable/CHANGELOG.md'),
)
help_menu.add_command(
    label='Source Code',
    command=lambda: webbrowser.open('https://github.com/Spyxpo/swab/'),
)
help_menu.add_command(
    label='View License',
    command=lambda: webbrowser.open('https://github.com/Spyxpo/swab/blob/stable/LICENSE'),
)

app_name_label = Label(root, text="App Name")
app_name_label.pack()
app_name = StringVar()
app_name_info = app_name.get()
Entry(root, textvariable=app_name, width=35).pack()

description_label = Label(root, text="Description (Keep it short)")
description_label.pack()
app_description = StringVar()
Entry(root, textvariable=app_description, width=35).pack()

package_name_label = Label(
    root, text="Package Name (e.g. com.companyname.appname)")
package_name_label.pack()
app_package_name = StringVar()
Entry(root, textvariable=app_package_name, width=35).pack()

version_label = Label(root, text="Version (e.g. 1.0.0)")
version_label.pack()
app_version = StringVar()
Entry(root, textvariable=app_version, width=35).pack()

build_number_label = Label(root, text="Build Number (e.g. 1)")
build_number_label.pack()
app_build_number = StringVar()
Entry(root, textvariable=app_build_number, width=35).pack()

web_url_label = Label(root, text="Website URL (www.website.com)")
web_url_label.pack()
web_url = StringVar()
Entry(root, textvariable=web_url, width=35).pack()

icon_label = Label(root, text="Icon (Choose .png image only (recommended 512x512))")
icon_label.pack()
Button(tk.Button(root, text='Choose an Icon', command=uploadIconAction).pack())

if running_on == 'Darwin':
    device_label = Label(root, text="Running on macOS", fg='green')
    device_label.pack()
    
elif running_on == 'Windows':
    device_label = Label(root, text="Running on Windows", fg='green')
    device_label.pack()

elif running_on == 'Linux':
    device_label = Label(root, text="Running on Linux", fg='green')
    device_label.pack()
    
else:
    pass

keystore_label = Label(root, text="Keystore (Choose .jks file only)")
keystore_label.pack()
Button(tk.Button(root, text='Choose a Keystore', command=uploadKeystoreAction).pack())

keystore_label = Label(root, text="-Keystore file information-")
keystore_label.pack()

alias_label = Label(root, text="Key Alias")
alias_label.pack()
alias = StringVar()
Entry(root, textvariable=alias, width=35).pack()

store_pass_label = Label(root, text="Store Password")
store_pass_label.pack()
store_pass = StringVar()
Entry(root, textvariable=store_pass, width=35, show="\u2022").pack()

key_pass_label = Label(root, text="Key Password")
key_pass_label.pack()
key_pass = StringVar()
Entry(root, textvariable=key_pass, width=35, show="\u2022").pack()

blank_label = Label(root, text="\nVerify the details before building")
blank_label.pack()

build_button = Button(root, text='Build', command=lambda: saveData())
build_button.pack()

root.mainloop()