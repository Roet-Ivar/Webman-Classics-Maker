from __future__ import print_function
import json, os
import subprocess
from shutil import copyfile
from global_paths import AppPaths

class Resign_eboot:
	def execute(self):
		with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
			json_data = json.load(f)
			
		content_id = json_data['content_id']

		scetool_dir = AppPaths.scetool
		print('DEBUG scetool_dir: ' + scetool_dir)
		args = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=' + content_id + ' --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'
		subprocess.call(os.path.join(scetool_dir, 'oscetool ') + args, shell=True)
		copyfile(os.path.join(scetool_dir, 'EBOOT.BIN'), os.path.join(AppPaths.USRDIR, 'EBOOT.BIN'))

		print('\nExecution of \'resign_eboot_linux.py\':   Done')
		print('-----------------------------------------------')
