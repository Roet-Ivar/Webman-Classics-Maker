import os
import json
import re

class Write_param_sfo():
	def execute(self):
		with open('../util_generated_files/webman_classics_pkg.json') as f:
			json_data = json.load(f)

		title = json_data['title']
		title_id = json_data['title_id']

		tmp_title_array = b'\x00'*128
		title = str(title) + tmp_title_array[len(title):]

		tmp_title='PKG/ROM Launcher'
		tmp_title_id='PKGLAUNCH'


		# load backup
		with open("../util_resources/PARAM.SFO.BAK", 'rb') as f:
			file = f.read()
			f.close()
			
			try:
			
				print(file.find(tmp_title))
				print(file[888:1025])
				
				file=file[0:888]+str(title)+file[888+len(title):]
				file=file[0:1025-len(str(title_id))]+str(title_id)+file[1025:]
				
				print(file[888:1025])
				
				# write to generated files
				newFile = open("../../pkg/PARAM.SFO", "wb")
				newFileByteArray = bytearray(file)
				newFile.write(newFileByteArray)
			
			except ValueError:
				print('File write error / \'PKGLAUNCH\' not found / \'title_id\' not a string')