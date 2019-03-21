import os
import json

class Elf_replace:
	def execute(self):
		
		with open('../util_generated_files/webman_classics_pkg.json') as f:
			json_data = json.load(f)

			
		title_id = json_data['title_id']

		# load it
		with open("../util_resources/EBOOT.ELF.BAK", 'rb') as f:
			file = f.read()
			
			try:
				file=file.replace('PKGLAUNCH',str(title_id))

				newFile = open("../scetool/EBOOT.ELF", "wb")
				newFileByteArray = bytearray(file)
				newFile.write(newFileByteArray)

				print('Execution of \'content_id_elf_replace.py\': Done')
				print('-----------------------------------------------')
			except ValueError:
				print('File write error/PKGLAUNCH not found/titel_id not a string')