import os
import json
import subprocess
from shutil import copyfile

# python -c "from resign_eboot_linux import Resign_eboot; resign = Resign_eboot(); resign.execute()"
class Resign_eboot:
	def execute(self):

		with open('../util_generated_files/params.json') as f:
			json_data = json.load(f)
			
		content_id = json_data['content_id']

		current_path= os.getcwd()
		# print('current_path: ' + current_path)
		if 'util_scripts' in os.getcwd():
			os.chdir(os.path.pardir)
		os.chdir('scetool')

		args = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=' + content_id + ' --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'
		p2 = subprocess.call('./scetool.exe' + ' ' + args)

		copyfile('./EBOOT.BIN', './../../pkg/USRDIR/EBOOT.BIN')
		
		if 'scetool' in os.getcwd():
			os.chdir(os.path.pardir)
		os.chdir('util_scripts')

		print('\nExecution of \'resign_eboot.py\':           Done')		
		print('-----------------------------------------------')