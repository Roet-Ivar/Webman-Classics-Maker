import json, os
import subprocess
from shutil import copyfile

class Resign_eboot:
	def execute(self):
		with open('../util_generated_files/pkg.json') as f:
			json_data = json.load(f)
			
		content_id = json_data['content_id']

		current_dir = os.path.dirname(__file__)
		scetool_dir = '../scetool/'
		os.chdir(scetool_dir)
		args = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=' + content_id + ' --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'
		subprocess.call('oscetool' + args, shell=True)
		os.chdir(current_dir)
		copyfile(scetool_dir + '/EBOOT.BIN', './../../pkg/USRDIR/EBOOT.BIN')

		print('\nExecution of \'resign_eboot_linux.py\':   Done')
		print('-----------------------------------------------')
