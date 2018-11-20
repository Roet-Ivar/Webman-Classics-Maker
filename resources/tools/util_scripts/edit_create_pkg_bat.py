import json
import os

class Edit_create_pkg_bat:
	def execute(self):
		with open('../util_generated_files/params.json') as f:
			json_data_bat = json.load(f)


		title_id = json_data_bat['title_id']
		content_id = json_data_bat['content_id']

		with open("../util_resources/CREATE_PKG.bat.BAK", 'rb') as f:
			file = f.read()
			f.close()
			
			try:
				file=file.replace('UP0001-PKGLAUNCH_00-0000000000000000',str(content_id))
				

				newFile = open("../../../CREATE_WEBMAN_CLASSICS.bat", "wb")
				newFileByteArray = bytearray(str(file))
				newFile.write(newFileByteArray)

				print('Execution of \'edit_create_pkg_bat.py\': Done')
			except ValueError:
				print('File write error/PKGLAUNCH not found/titel_id not a string')