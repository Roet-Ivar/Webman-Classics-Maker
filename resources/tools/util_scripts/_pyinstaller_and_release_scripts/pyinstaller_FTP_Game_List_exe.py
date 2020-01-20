# pyinstaller build command:
# pyinstaller.exe --onefile --noconsole --icon=./resources/image_resources/param_sfo.ico start_edit_param_sfo.py
# pyinstaller.exe --onefile --icon=./resources/image_resources/webman.ico ./resources/tools/util_scripts/build_all_scripts.py
# NOTE: '--noconsole' is optional and seems to give a false positive on my AV

import os, subprocess, sys
from shutil import rmtree

sys.path.append('../../wcm_gui')
from global_paths import Image as ImagePaths
from global_paths import Build as BuildPaths

if not os.path.exists('build'):
    os.makedirs('build')

script_filename='ftp_game_list.py'
script_folder_path=BuildPaths.util_scripts

icon_path=ImagePaths.misc
icon_name='ftp_game_list.ico'

executable_name='FTP_Game_List'
dist_path=BuildPaths.application_path
spec_path='./build'

zip_dir_path=BuildPaths.application_path
zip_archive_name = 'webman_classics_maker.zip'

app = 'pyinstaller.exe'
args = '--distpath=' + dist_path + ' ' + '--specpath=' + spec_path + ' ' + '--name=' + executable_name + ' ' + '--onefile' + ' ' + '--icon=' + os.path.join(icon_path, icon_name) + ' ' + os.path.join(script_folder_path, script_filename)

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