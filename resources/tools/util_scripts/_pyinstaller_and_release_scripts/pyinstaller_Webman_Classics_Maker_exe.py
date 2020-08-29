# pyinstaller build command:
# pyinstaller.exe --onefile --noconsole --icon=./resources/image_resources/param_sfo.ico start_edit_param_sfo.py
# pyinstaller.exe --onefile --icon=./resources/image_resources/webman.ico ./resources/tools/util_scripts/build_all_scripts.py
# NOTE: '--noconsole' is optional and seems to give a false positive on my AV

import os, subprocess
from shutil import rmtree

import application_path
from global_paths import Image as ImagePaths
from global_paths import App as AppPaths

if not os.path.exists('build'):
    os.makedirs('build')

script_filename='webman_classics_maker.py'
script_folder_path=AppPaths.application_path

icon_path=ImagePaths.misc
icon_name='webman.ico'

executable_name='Webman_Classics_Maker'
dist_path=AppPaths.application_path
spec_path='build'

hidden_imports = '--hidden-import=' + 'ConfigParser' + ' ' + '--hidden-import=' + 'glob'

app = 'pyinstaller.exe'
args = hidden_imports + ' ' + '--distpath=' + dist_path + ' ' + '--specpath=' + spec_path + ' ' + '--name=' + executable_name + ' ' + '--onefile' + ' ' + '--icon=' + os.path.join(icon_path, icon_name) + ' ' + os.path.join(script_folder_path, script_filename)

p = subprocess.call(app + ' ' + args)


# clean up residuals from pyinstaller
if os.path.isdir('build'):
    rmtree('build')
if os.path.isdir('__pycache__'):
    rmtree('__pycache__')

for root, dirs, files in os.walk('.'):
    for file in files:
        if 'pyc' in str(file):
            os.remove(file)

print('\n----------------------------------------------------')
print('Succesfully built \"' + executable_name + '.exe\"')
print('----------------------------------------------------\n\n')