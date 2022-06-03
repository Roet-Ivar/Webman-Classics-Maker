import os
import json
from global_paths import AppPaths

class Elf_replace:
	def execute(self):
		with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
			json_data = json.load(f)

		# load it
		with open(os.path.join(AppPaths.util_resources, 'EBOOT.ELF.BAK'), 'rb') as f:
			eboot_elf_file = f.read()
			
			try:
				eboot_elf_file = eboot_elf_file.replace('PKGLAUNCH'.encode('utf-8'), json_data['title_id'].encode('utf-8'))
				newFile = open(os.path.join(AppPaths.scetool, 'EBOOT.ELF'), 'wb')
				newFileByteArray = bytearray(eboot_elf_file)
				newFile.write(newFileByteArray)

				print('[2/5] Execution of \'content_id_elf_replace.py\':  DONE')
				print('-----------------------------------------------------')
				return True
			except Exception as e:
				print('[2/5] Execution of \'content_id_elf_replace.py\':  FAILED')
				print(getattr(e, 'message', repr(e)))
				print('-----------------------------------------------------')
				return False