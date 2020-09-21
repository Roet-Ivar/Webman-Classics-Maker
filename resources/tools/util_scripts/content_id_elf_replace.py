import os
import json
from global_paths import App as AppPaths

class Elf_replace:
	def execute(self):
		if os.path.exists(AppPaths.game_work_dir):
			work_dir = AppPaths.game_work_dir
		else:
			work_dir = AppPaths.wcm_work_dir

		with open(os.path.join(work_dir, 'pkg.json')) as f:
			json_data = json.load(f)

		# load it
		with open(os.path.join(AppPaths.util_resources, 'EBOOT.ELF.BAK'), 'rb') as f:
			file = f.read()
			
			try:
				file = file.replace('PKGLAUNCH', str(json_data['title_id']))

				newFile = open(os.path.join(AppPaths.scetool, 'EBOOT.ELF'), 'wb')
				newFileByteArray = bytearray(file)
				newFile.write(newFileByteArray)

				print('Execution of \'content_id_elf_replace.py\':  Done')
				print('-----------------------------------------------')
			except ValueError:
				print('File write error/PKGLAUNCH not found/titel_id not a string')