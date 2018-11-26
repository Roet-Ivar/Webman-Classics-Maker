import os
import subprocess

current_path= os.getcwd()
print(current_path)
if '\util_scripts' not in os.getcwd():
	os.chdir('./resources/tools/util_scripts/_pyinstaller_and_release_scripts')

app = './../../Param_SFO_Editor/PARAM.SFO.Editor.exe'
args = './../../../pkg/PARAM.SFO'

p = subprocess.call(app + ' ' + args)

