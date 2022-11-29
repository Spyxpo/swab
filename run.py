'''
Author: Mantresh Khurana | Spyxpo
Project Name: Spyxpo Web To App Builder
Project Description: This is a tool which is used to convert a website into an app for iOS, Android, Windows, macOS and Linux.
'''

import json
import tarfile
import time
from tkinter import *
import tkinter as tk
from tkinter import messagebox
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
machine_architecture = platform.machine()

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
line = packages_version_info.readlines()

flutter_version = line[0]
nodejs_version = line[1]
jdk_version = line[2]
jre_version = line[3]
git_version = line[4]
android_sdk_version = line[5]

packages_version_info.close()

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

def custom_bar(current, total, width=80):
    return wget.bar_adaptive(round(current/1024/1024, 2), round(total/1024/1024, 2), width) + ' MB'

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
            print(f"{bcolors.OKGREEN}Downloading Flutter for Windows...")
            wget.download(url, 'flutter.zip', bar=custom_bar)
            print("\nExtracting Flutter.....")
            with zipfile.ZipFile('flutter.zip', "r") as zip_ref:
                zip_ref.extractall("C:\\")
            location = "C:\\flutter\\bin"
            userpath.append(location)
            os.remove('flutter.zip')
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
                print("Downloading Flutter for macOS...")
                wget.download(url, 'flutter.zip', bar=custom_bar)
                print("\nExtracting Flutter.....")
                with zipfile.ZipFile('flutter.zip', "r") as zip_ref:
                    zip_ref.extractall("/Users/")
                location = "/Users/flutter/bin"
                userpath.append(location)
                os.remove('flutter.zip')
                print("Flutter installed successfully.")      
            elif platform == 'Linux':
                url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_{flutter_version}-stable.tar.xz"
                print("Downloading Flutter for Linux...")
                wget.download(url, 'flutter.tar.xz', bar=custom_bar)
                print("\nExtracting Flutter.....")
                os.system('tar xf flutter.tar.xz')
                location = "flutter/bin"
                userpath.append(location)
                os.remove('flutter.tar.xz')
                print("Flutter installed successfully.")
            else:
                pass

def check_nodejs():
    if running_on == 'Windows':
        nodejs = subprocess.call(['where', 'node'])
        if nodejs == 0:
            print(f'{bcolors.OKGREEN}NodeJS is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}NodeJS is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"nodejs\" then set PATH and try again.\n')
            url = f"https://nodejs.org/dist/v{nodejs_version}/node-v{nodejs_version}-x64.msi"
            print(f"{bcolors.OKGREEN}Downloading NodeJS for Windows...")
            wget.download(url, 'nodejs.msi', bar=custom_bar)
            print("\nInstalling NodeJS.....")
            os.system('nodejs.msi')
            os.remove('nodejs.msi')
            print("NodeJS installed successfully.")
            
    else:
        nodejs = subprocess.call(['which', 'node'])
        if nodejs == 0:
            print(f'{bcolors.OKGREEN}NodeJS is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}NodeJS is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"nodejs\" then set PATH and try again.\n')
            if running_on == 'Darwin':
                if machine_architecture == 'arm64':
                    url = f"https://nodejs.org/dist/v{nodejs_version}/node-v{nodejs_version}-darwin-arm64.tar.gz"
                    print(f"Downloading NodeJS for macOS...")
                    wget.download(url, 'nodejs.tar.gz', bar=custom_bar)
                    print("\nInstalling NodeJS.....")
                    
                    with tarfile.open('nodejs.tar.gz', 'r:gz') as tar:
                        tar.extractall()

                    os.rename(f"node-v{nodejs_version}-darwin-arm64", "nodejs")

                    location = os.getcwd() + "/nodejs/bin/"
                    userpath.append(location)
                    os.remove('nodejs.tar.gz')
                    print("NodeJS installed successfully.")

                else:
                    url = f"https://nodejs.org/dist/v{nodejs_version}/node-v{nodejs_version}-darwin-x64.tar.gz"
                    print(f"Downloading NodeJS for macOS...")
                    wget.download(url, 'nodejs.tar.gz', bar=custom_bar)
                    print("\nInstalling NodeJS.....")
                    
                    with tarfile.open('nodejs.tar.gz', 'r:gz') as tar:
                        tar.extractall()

                    os.rename(f"node-v{nodejs_version}-darwin-x64", "nodejs")

                    location = os.getcwd() + "/nodejs/bin/"
                    userpath.append(location)
                    os.remove('nodejs.tar.gz')
                    print("NodeJS installed successfully.")
                    
            elif running_on == 'Linux':
                url = f"https://nodejs.org/dist/v{nodejs_version}/node-v{nodejs_version}-linux-x64.tar.xz"
                print(f"{bcolors.OKGREEN}Downloading NodeJS for Linux...")
                wget.download(url, 'nodejs.tar.xz', bar=custom_bar)
                print("\nExtracting NodeJS.....")
                os.system('tar xf nodejs.tar.xz')
                location = os.getcwd() + "/nodejs/bin"
                userpath.append(location)
                os.remove('nodejs.tar.xz')
            else:
                pass    

def check_java():
    if running_on == 'Windows':
        java = subprocess.call(['where', 'java'])
        if java == 0:
            print(f'{bcolors.OKGREEN}Java is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Java is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"java\" then set PATH and try again.\n')
            url = f"https://download.oracle.com/java/{jdk_version}/latest/jdk-{jdk_version}_windows-x64_bin.exe"
            print(f"{bcolors.OKGREEN}Downloading Java for Windows...")
            wget.download(url, 'java.exe', bar=custom_bar)
            print("\nInstalling Java.....")
            os.system('java.exe')
            location = f"C:\\Program Files\\Java\\jdk-{jdk_version}\\bin"
            userpath.append(location)
            os.remove('java.exe')
            print("Java installed successfully.")
            
    else:
        java = subprocess.call(['which', 'java'])
        if java == 0:
            print(f'{bcolors.OKGREEN}Java is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Java is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"java\" then set PATH and try again.\n')
            if running_on == 'Darwin':
                if machine_architecture == 'arm64':
                    url = f"https://download.oracle.com/java/{jdk_version}/latest/jdk-{jdk_version}_macos-aarch64_bin.tar.gz"
                    print(f"Downloading Java for macOS...")
                    wget.download(url, 'java.tar.gz', bar=custom_bar)
                    print("\nInstalling Java.....")
                    
                    with tarfile.open('java.tar.gz', 'r:gz') as tar:
                        tar.extractall()
                        
                    os.rename(f'jdk-{jdk_version}.0.1.jdk', 'java')    

                    location = os.getcwd() + '/java/Contents/Home/bin'  
                    userpath.append(location)
                    os.remove('java.tar.gz')
                    print("Java installed successfully.")

                else:
                    url = f"https://download.oracle.com/java/{jdk_version}/latest/jdk-{jdk_version}_macos-x64_bin.tar.gz"   
                    print(f"Downloading Java for macOS...")
                    wget.download(url, 'java.tar.gz', bar=custom_bar)
                    print("\nInstalling Java.....")
                    
                    with tarfile.open('java.tar.gz', 'r:gz') as tar:
                        tar.extractall()

                    os.rename(f'jdk-{jdk_version}.0.1.jdk', 'java')    

                    location = os.getcwd() + '/java/Contents/Home/bin'  
                    userpath.append(location)
                    os.remove('java.tar.gz')
                    print("Java installed successfully.")

            elif running_on == 'Linux':
                url = f"https://download.oracle.com/otn/java/{jdk_version}/latest/jdk-{jdk_version}_linux-x64_bin.tar.gz"
                print(f"{bcolors.OKGREEN}Downloading Java for Linux...")
                wget.download(url, 'java.tar.gz', bar=custom_bar)
                print("\nExtracting Java.....")
                os.system('tar xf java.tar.gz')
                location = os.getcwd() + f"/jdk-{jdk_version}/bin"
                userpath.append(location)
                os.remove('java.tar.gz')
                print("Java installed successfully.")
            else:
                pass    

def check_jre():
    if running_on == 'Windows':
        jre = subprocess.call(['where', 'keytool'])
        if jre == 0:
            print(f'{bcolors.OKGREEN}JRE is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}JRE is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"jre\" then set PATH and try again.\n')
            url = f'https://www.techspot.com/downloads/downloadnow/5198/?evp=8ac5f15c387fb61b7484086c2f15e494&file=5647'
            print(f"{bcolors.OKGREEN}Downloading JRE for Windows...")
            wget.download(url, 'jre.exe', bar=custom_bar)
            print("\nInstalling JRE.....")
            os.system('jre.exe')
            location = f"C:\\Program Files\\Java\\jre{jre_version}\\bin"
            userpath.append(location)
            os.remove('jre.exe')
            print("JRE installed successfully.")
    else:
        jre = subprocess.call(['which', 'keytool'])
        if jre == 0:
            print(f'{bcolors.OKGREEN}JRE is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}JRE is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"jre\" then set PATH and try again.\n')
            if running_on == 'Darwin':
                url = f"https://www.techspot.com/downloads/downloadnow/5198/?evp=91a508f7a3f5244c06e5b0706bbc39d7&file=5649"
                print(f"Downloading JRE for macOS...")
                wget.download(url, 'jre.dmg', bar=custom_bar)
                print("\nInstalling JRE.....")
                location = os.getcwd() + f'/jre{jre_version}/Contents/Home/bin'  
                userpath.append(location)
                os.remove('jre.dmg')
                print("JRE installed successfully.")

            elif running_on == 'Linux':
                url = f"https://javadl.oracle.com/webapps/download/AutoDL?BundleId=247127_10e8cce67c7843478f41411b7003171c"
                print(f"{bcolors.OKGREEN}Downloading JRE for Linux...")
                wget.download(url, 'jre.tar.gz', bar=custom_bar)
                print("\nExtracting JRE.....")
                os.system('tar xf jre.tar.gz')
                location = os.getcwd() + f"/jre{jre_version}/bin"
                userpath.append(location)
                os.remove('jre.tar.gz')
                print("JRE installed successfully.")
            else:
                pass

def check_git():
    if running_on == 'Windows':
        git = subprocess.call(['where', 'git'])
        if git == 0:
            print(f'{bcolors.OKGREEN}Git is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Git is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"Git\" then set PATH and try again.\n')
            url = f"https://github.com/git-for-windows/git/releases/download/v{git_version}.windows.1/Git-{git_version}-64-bit.exe"
            print(f"{bcolors.OKGREEN}Downloading Git for Windows...")
            wget.download(url, 'git.exe', bar=custom_bar)
            print("\nInstalling Git.....")
            os.system('git.exe')
            os.remove('git.exe')
            print("Git installed successfully.")
            
    else:
        git = subprocess.call(['which', 'git'])
        if git == 0:
            print(f'{bcolors.OKGREEN}Git is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Git is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"Git\" then set PATH and try again.\n')
            if running_on == 'Darwin':
                if machine_architecture == 'arm64':
                    brew = subprocess.call(['which', 'brew'])
                    if brew == 0:
                        print("Installing Git...")
                        subprocess.call(['brew', 'install', 'git'])
                        print("Git installed successfully.")
                    else:
                        subprocess.call(['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'])     
                        subprocess.call(['brew', 'install', 'git'])
                        print("Git installed successfully.")

                else:
                    brew = subprocess.call(['which', 'brew'])
                    if brew == 0:
                        print("Installing Git...")
                        subprocess.call(['brew', 'install', 'git'])
                        print("Git installed successfully.")
                    else:
                        subprocess.call(['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'])     
                        subprocess.call(['brew', 'install', 'git'])
                        print("Git installed successfully.")

            elif running_on == 'Linux':
                url = f"https://www.kernel.org/pub/software/scm/git/git-{git_version}.tar.gz"
                print(f"{bcolors.OKGREEN}Downloading Git for Linux...")
                wget.download(url, 'git.tar.gz', bar=custom_bar)
                print("\nExtracting Git.....")
                os.system('tar xf git.tar.gz')
                location = os.getcwd() + f"/git/bin"
                userpath.append(location)
                os.remove('git.tar.gz')
                print("Git installed successfully.")
            else:
                pass    

def check_cmdline_tools():
    if running_on == 'Windows':
        cmdline_tools = subprocess.call(['where', 'sdkmanager'])
        if cmdline_tools == 0:
            print(f'{bcolors.OKGREEN}Android SDK is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Android SDK is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"Android SDK\" then set PATH and try again.\n')
            url = f"https://dl.google.com/android/repository/commandlinetools-win-{android_sdk_version}_latest.zip"
            print(f"{bcolors.OKGREEN}Downloading Android SDK for Windows...")
            wget.download(url, 'android-sdk.zip', bar=custom_bar)
            print("\nExtracting Android SDK.....")
            with zipfile.ZipFile('android-sdk.zip', 'r') as zip_ref:
                zip_ref.extractall()
            location = os.getcwd() + f"/cmdline-tools/bin"
            userpath.append(location)
            os.remove('android-sdk.zip')
            print("Android SDK installed successfully.")
            input("Press Enter to exit and restart the program...")
            exit()
    else:
        cmdline_tools = subprocess.call(['which', 'sdkmanager'])
        if cmdline_tools == 0:
            print(f'{bcolors.OKGREEN}Android SDK is already installed.\n')
            clear()
            pass
        else:
            print(f'{bcolors.WARNING}Android SDK is not in the PATH or is installed on this device.\n')
            print(f'{bcolors.FAIL}Please install \"Android SDK\" then set PATH and try again.\n')
            if running_on == 'Darwin':
                url = f"https://dl.google.com/android/repository/commandlinetools-mac-{android_sdk_version}_latest.zip"
                print(f"Downloading Android SDK for macOS...")
                wget.download(url, 'android-sdk.zip', bar=custom_bar)
                print("\nExtracting Android SDK.....")

                with zipfile.ZipFile('android-sdk.zip', 'r') as zip_ref:
                    zip_ref.extractall()

                location = os.getcwd() + f"/cmdline-tools/bin"

                os.system(f"chmod +x {location}/sdkmanager")
                os.system(f"chmod +x {location}/avdmanager")
                os.system(f"chmod +x {location}/apkanalyser")
                os.system(f"chmod +x {location}/lint")
                os.system(f"chmod +x {location}/profgen")
                os.system(f"chmod +x {location}/retrace")
                os.system(f"chmod +x {location}/screenshot2")

                userpath.append(location)
                os.remove('android-sdk.zip')
                print("Android SDK installed successfully.")
                input("Press Enter to exit and restart the program...")
                exit()
            elif running_on == 'Linux':
                os.system('sudo apt install snapd')
                os.system('sudo snap install android-studio --classic')
                print("Android SDK installed successfully.")
                input("Press Enter to exit and restart the program...")
                exit()
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
check_nodejs()
check_java()
check_jre()
check_git()
check_cmdline_tools()

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
    os.mkdir("assets/")
    
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

def open_build_folder():
    if running_on == 'Darwin':
        if (os.path.exists("build")):
            os.system("open build")
        else:
            os.mkdir("build")
            os.system("open build")
    elif running_on == 'Linux':
        if (os.path.exists("build")):
            os.system("open build")
        else:
            os.mkdir("build")
            os.system("open build")
    elif running_on == 'Windows':
        if (os.path.exists("build")):
            os.system("start build")
        else:
            os.mkdir("build")
            os.system("start build")
    else:
        pass

def upload_icon_action(event=None):
    app_name_info = app_name.get()

    if app_name_info == "":
        showinfo("No app name", "No app name, please enter an app name.")
        return False
    elif icon_path_label.cget("text") == "No file selected": 
        icon = filedialog.askopenfilename(filetypes=[("png files", "*.png")])
        icon_path_label['text'] = icon
        print(f'{bcolors.ENDC}Icon image: {icon}')

        if icon == '':
            showinfo("No icon", "No icon, please select an icon.")
            icon_path_label['text'] = 'No file selected'
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
    else:
        icon = filedialog.askopenfilename(filetypes=[("png files", "*.png")])
        icon_path_label['text'] = icon
        print(f'{bcolors.ENDC}Icon image: {icon}')

        if icon == '':
            showinfo("No icon", "No icon, please select an icon.")
            icon_path_label['text'] = 'No file selected'
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

def upload_keystore_action():
    app_name_info = app_name.get()

    if app_name_info == "":
        showinfo("No app name", "No app name, please enter an app name.")
        return False
    elif keystore_path_label.cget("text") == "No file selected": 
        keystore_path = filedialog.askopenfilename(filetypes=[("keystore files", "*.jks"), ("keystore files", "*.keystore")])
        keystore_path_label['text'] = keystore_path

        if keystore_path == '':
            showinfo("No keystore", "No keystore, please select a keystore.")
            keystore_path_label['text'] = 'No file selected'
            pass
        else:
            print('Keystore file:', keystore_path)
            keystore_path_label['text'] = keystore_path
            key_file = open('assets/key.properties', 'w')
            key_file.write(f'storeFile={keystore_path}\n')
            key_file.close()
    else:
        keystore_path = filedialog.askopenfilename(filetypes=[("keystore files", "*.jks"), ("keystore files", "*.keystore")])
        keystore_path_label['text'] = keystore_path

        if keystore_path == '':
            showinfo("No keystore", "No keystore, please select a keystore.")
            keystore_path_label['text'] = 'No file selected'
            pass
        else:
            print('Keystore file:', keystore_path)
            keystore_path_label['text'] = keystore_path
            key_file = open('assets/key.properties', 'w')
            key_file.write(f'storeFile={keystore_path}\n')
            key_file.close()

def save_data():

    start_time = time.time()

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

    if os.path.exists(f"build/{app_name_info}/"):
        shutil.rmtree(f"build/{app_name_info}/")
    else:
        pass

    if os.path.exists(f"projects/{app_name_info}/"):
        shutil.rmtree(f"projects/{app_name_info}/")
    else:
        pass

    if os.path.exists(f"projects/"):
        shutil.rmtree(f"projects/")
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

    app_name.set('')
    app_description.set('')
    app_package_name.set('')
    app_version.set('')
    app_build_number.set('')
    web_url.set('')
    icon_path_label.config(text='No file selected')
    keystore_path_label.config(text = 'No file selected')
    alias.set('')
    key_pass.set('')
    store_pass.set('')

    print('Build completed in ' + str(time.time() - start_time) + ' seconds.')

    open_build_folder()

# version details
version_info = open('VERSION', 'r')
version = version_info.read()

# tkinter ui
root = tk.Tk()
app_icon = PhotoImage(file = 'images/logo.png')
root.iconphoto(False, app_icon)
root.title('SWAB | ' + version)
root.geometry('480x690')
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

def new_project():
    if app_name == '' and app_description == '' and app_package_name == '' and app_version == '' and app_build_number == '' and web_url == '' and icon_path_label.cget('text') == 'No file selected' and keystore_path_label.cget('text') == 'No file selected' and alias == '' and key_pass == '' and store_pass == '':
        app_name.set('')
        app_description.set('')
        app_package_name.set('')
        app_version.set('')
        app_build_number.set('')
        web_url.set('')
        icon_path_label.config(text='No file selected')
        keystore_path_label.config(text = 'No file selected')
        alias.set('')
        key_pass.set('')
        store_pass.set('')
    else:
        save_project_answer = messagebox.askyesno("Save Project", "Do you want to save the current project?")
        if save_project_answer == True:
            save_as_project()
        else:
            app_name.set('')
            app_description.set('')
            app_package_name.set('')
            app_version.set('')
            app_build_number.set('')
            web_url.set('')
            icon_path_label.config(text='No file selected')
            keystore_path_label.config(text = 'No file selected')
            alias.set('')
            key_pass.set('')
            store_pass.set('')

file_menu.add_command(
    label='New',
    command=lambda: new_project(),
)

def open_project():
    if app_name == '' and app_description == '' and app_package_name == '' and app_version == '' and app_build_number == '' and web_url == '' and icon_path_label.cget('text') == 'No file selected' and keystore_path_label.cget('text') == 'No file selected' and alias == '' and key_pass == '' and store_pass == '':
        pass
    else:
        save_project_answer = messagebox.askyesno("Save Project", "Do you want to save the current project?")
        if save_project_answer == True:
            save_as_project()
        else:
            file = filedialog.askopenfilename(filetypes=[("SWAB Project Files", "*.swab")])
            if file == '':
                pass
            else:
                with open(file, 'r') as f:
                    data = json.load(f)
                    app_name.set(data['app_name'])
                    app_description.set(data['app_description'])
                    app_package_name.set(data['app_package_name'])
                    app_version.set(data['app_version'])
                    app_build_number.set(data['app_build_number'])
                    web_url.set(data['web_url'])
                    icon_path_label.config(text=data['icon_path'])
                    keystore_path_label.config(text=data['keystore_path'])
                    alias.set(data['alias'])
                    key_pass.set(data['key_pass'])
                    store_pass.set(data['store_pass'])   

                size = 512, 512
                image = Image.open(icon_path_label.cget('text'))
                image_resized = image.resize(size)
                image_resized.save("assets/favicon.png", "PNG")

                ico = Image.open('assets/favicon.png')
                ico.save('assets/favicon.ico')

                icns = icnsutil.IcnsFile()
                icns.add_media(file='assets/favicon.png')
                icns.write('assets/favicon.icns')       

                key_file = open('assets/key.properties', 'w')
                key_file.write('storeFile=' + keystore_path_label.cget('text') + '\n')
                key_file.close()            

file_menu.add_command(
    label='Open Project',
    command=lambda: open_project(),
)

file_menu.add_separator()

def save_as_project():
    if app_name.get() == '':
        messagebox.showerror("Error", "Please enter app name.")
        return False
    elif app_description.get() == '':
        messagebox.showerror("Error", "Please enter app description.")
        return False
    elif app_package_name.get() == '':
        messagebox.showerror("Error", "Please enter app package name.")
        return False
    elif app_version.get() == '':
        messagebox.showerror("Error", "Please enter app version.")
        return False
    elif app_build_number.get() == '':
        messagebox.showerror("Error", "Please enter app build number.")
        return False
    elif web_url.get() == '':
        messagebox.showerror("Error", "Please enter web url.")
        return False
    elif icon_path_label.cget('text') == 'No file selected':
        messagebox.showerror("Error", "Please select icon.")
        return False
    elif keystore_path_label.cget('text') == 'No file selected':
        messagebox.showerror("Error", "Please select keystore.")
        return False
    elif alias.get() == '':
        messagebox.showerror("Error", "Please enter alias.")
        return False
    elif key_pass.get() == '':
        messagebox.showerror("Error", "Please enter key password.")
        return False
    elif store_pass.get() == '':
        messagebox.showerror("Error", "Please enter store password.")
        return False
    else:
        project = {
            'app_name': app_name.get(),
            'app_description': app_description.get(),
            'app_package_name': app_package_name.get(),
            'app_version': app_version.get(),
            'app_build_number': app_build_number.get(),
            'web_url': web_url.get(),
            'icon_path': icon_path_label.cget('text'),
            'keystore_path': keystore_path_label.cget('text'),
            'alias': alias.get(),
            'key_pass': key_pass.get(),
            'store_pass': store_pass.get()
        }

        file = filedialog.asksaveasfile(mode='w', defaultextension=".swab")
        if file is None:
            json.dump(project, app_name_info + '.swab', indent=4)
            file.close()
        else:
            json.dump(project, file, indent=4)
            file.close()

file_menu.add_command(
    label='Save As...',
    command=lambda: save_as_project(),
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
    command=lambda: save_data(),
)

commands_menu.add_separator()

commands_menu.add_command(
    label='Clean',
    command=lambda: clean_dir(),
)
commands_menu.add_command(
    label='Clean Build',
    command=lambda: clean_build(),
)

commands_menu.add_separator()

def create_keystore():
    create_keystore_window = Toplevel(root)
    create_keystore_window.title('Create a Keystore')
    create_keystore_window.geometry('400x440')
    create_keystore_window.resizable(False, False)

    alias_name_label = Label(create_keystore_window, text="Alias Name")
    alias_name_label.pack()
    alias_name = StringVar()
    Entry(create_keystore_window, textvariable=alias_name, width=35).pack()

    keystore_password_label = Label(create_keystore_window, text="Keystore Password")
    keystore_password_label.pack()
    keystore_password = StringVar()
    Entry(create_keystore_window, textvariable=keystore_password, width=35).pack()

    your_name_label = Label(create_keystore_window, text="Your Name")
    your_name_label.pack()
    your_name = StringVar()
    Entry(create_keystore_window, textvariable=your_name, width=35).pack()

    your_organization_unit_label = Label(create_keystore_window, text="Your Organization Unit")
    your_organization_unit_label.pack()
    your_organization_unit = StringVar()
    Entry(create_keystore_window, textvariable=your_organization_unit, width=35).pack()

    your_organization_label = Label(create_keystore_window, text="Your Organization")
    your_organization_label.pack()
    your_organization = StringVar()
    Entry(create_keystore_window, textvariable=your_organization, width=35).pack()

    your_city_or_locality_label = Label(create_keystore_window, text="Your City or Locality")
    your_city_or_locality_label.pack()
    your_city_or_locality = StringVar()
    Entry(create_keystore_window, textvariable=your_city_or_locality, width=35).pack()

    your_state_or_province_label = Label(create_keystore_window, text="Your State or Province")
    your_state_or_province_label.pack()
    your_state_or_province = StringVar()
    Entry(create_keystore_window, textvariable=your_state_or_province, width=35).pack()

    your_two_letter_country_code_label = Label(create_keystore_window, text="Your Two-Letter Country Code")
    your_two_letter_country_code_label.pack()
    your_two_letter_country_code = StringVar()
    Entry(create_keystore_window, textvariable=your_two_letter_country_code, width=35).pack()

    def save_keystore():
        file = filedialog.asksaveasfile(mode='w', defaultextension=".keystore")
        if file is None:
            return
        else:
            keystore_file =  'keytool -genkey -noprompt \
            -alias ' + alias_name.get() + ' \
            -keypass ' + keystore_password.get() + ' \
            -keyalg ' + 'RSA' + ' \
            -sigalg ' + 'SHA1withRSA' + '\
            -validity ' + '10000' + ' \
            -keysize ' + '2048' + ' \
            -keystore ' + file.name + ' \
            -storepass '+ keystore_password.get() +' \
            -storetype  ' + 'JKS' 
            
            os.system(keystore_file)
            print('Keystore created successfully.')
            create_keystore_window.destroy()
            messagebox.showinfo("Success", "Keystore created successfully.")

    create_keystore_button = Button(create_keystore_window, text='Create', command=lambda: save_keystore())
    create_keystore_button.pack()

commands_menu.add_command(
    label='Create a Keystore',
    command=lambda: create_keystore(),
)

commands_menu.add_separator()

commands_menu.add_command(
    label='Open Build Folder',
    command=lambda: open_build_folder(),
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
Button(tk.Button(root, text=f'Choose an Icon', command=upload_icon_action).pack())

icon_path_label = Label(root, text="No file selected", fg='grey')
icon_path_label.pack()

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

keystore_label = Label(root, text="Keystore File")
keystore_label.pack()
Button(tk.Button(root, text='Choose a Keystore', command=upload_keystore_action).pack())

keystore_path_label = Label(root, text="No file selected", fg='grey')
keystore_path_label.pack()

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

build_button = Button(root, text='Build', command=lambda: save_data())
build_button.pack()

root.mainloop()