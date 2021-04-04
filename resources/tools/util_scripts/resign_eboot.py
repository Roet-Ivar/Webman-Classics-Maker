import json, os
from shutil import copyfile
from global_paths import App as AppPaths

class Resign_eboot:
	def execute(self):
		try:
			# common paths
			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			# clean any up old EBOOT
			if os.path.isfile(os.path.join(AppPaths.scetool, 'EBOOT.BIN')):
				os.remove(os.path.join(AppPaths.scetool, 'EBOOT.BIN'))
			if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR', 'EBOOT.BIN')):
				os.remove(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR', 'EBOOT.BIN'))

			content_id = json_data['content_id']
			print('DEBUG content_id: ' + content_id)


			scetool_exe_path = os.path.join(AppPaths.scetool, 'scetool.exe')
			args = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=' + content_id + ' --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'

			current_dir = os.getcwd()
			os.chdir(AppPaths.scetool)
			os.system('"' + scetool_exe_path + ' ' + args + '"')
			os.chdir(current_dir)
			copyfile(os.path.join(AppPaths.scetool, 'EBOOT.BIN'), os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR', 'EBOOT.BIN'))

			print('\n[4/5] Execution of \'resign_eboot.py\':            DONE')
			print('-----------------------------------------------------')
			return True
		except Exception as e:
			print('\n[4/5] Execution of \'resign_eboot.py\':            FAILED')
			print(e.message)
			print('-----------------------------------------------------')
			return False
