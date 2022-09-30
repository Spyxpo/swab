# this works on Windows for now, macOS & Linux support coming soon

import os
import shutil
import platform

running_on = platform.system()
path = os.getcwd()

print('Build Started.')

os.system(f'pyinstaller --noconfirm --onedir --console --icon "{path}/images/logo.ico" --add-data "{path}/build;build/" --add-data "{path}/images;images/" --add-data "{path}/template;template/" --add-data "{path}/VERSION;." --add-data "{path}/LICENSE;."  "{path}/run.py"')

shutil.rmtree(f'{path}/build/run')

if running_on == 'Darwin':
    os.system('clear')
elif running_on == 'Linux':
    os.system('clear')
elif running_on == 'Windows':
    os.system('cls')
else:
    pass

print('Executable is located in \"/dist/run/\" folder.')
print('Build complete.')
