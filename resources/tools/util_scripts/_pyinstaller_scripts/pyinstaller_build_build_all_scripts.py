# pyinstaller build command:
# pyinstaller.exe --onefile --noconsole --icon=./resources/image_resources/param_sfo.ico start_edit_param_sfo.py
# pyinstaller.exe --onefile --icon=./resources/image_resources/webman.ico ./resources/tools/util_scripts/build_all_scripts.py
# NOTE: '--noconsole' is optional and seems to give a false positive on my AV

import os
import subprocess
from shutil import rmtree

os.mkdir('./build')

script_filename='build_all_scripts.py'
script_folder_path='../'

icon_path='../../../images/'
icon_name='webman.ico'

executable_name='Build_Webman_PKG'
dist_path='../../../../'
spec_path='./build'

app = 'pyinstaller.exe'
args = '--distpath=' + dist_path + ' ' + '--specpath=' + spec_path + ' ' + '--name=' + executable_name + ' ' + '--onefile' + ' ' + '--icon=' + icon_path + icon_name + ' ' + script_folder_path + script_filename

p = subprocess.call(app + ' ' + args)

rmtree('./build')

print('Succesfully built \"' + executable_name + '.exe\"')