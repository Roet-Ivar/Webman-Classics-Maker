import json, os
import subprocess
from shutil import copyfile
from global_paths import App as AppPaths

class Resign_eboot:
	def execute(self):
		try:
			# common paths
			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			content_id = json_data['content_id']

			current_dir = AppPaths.util_scripts
			scetool_dir = AppPaths.scetool
			# TODO: No more CHDIR!
			os.chdir(scetool_dir)
			args = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=' + content_id + ' --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'
			subprocess.call('scetool.exe ' + args)
			# TODO: No more CHDIR!
			os.chdir(current_dir)
			copyfile(os.path.join(scetool_dir, 'EBOOT.BIN'), os.path.join(AppPaths.USRDIR, 'EBOOT.BIN'))
			# TODO: No more CHDIR!
			os.chdir(AppPaths.wcm_gui)
			print('\nExecution of \'resign_eboot.py\':            DONE')
			print('-----------------------------------------------')
			return True
		except Exception as e:
			print('\nExecution of \'resign_eboot.py\':            FAILED')
			print(e.message)
			print('-----------------------------------------------')
			return False
