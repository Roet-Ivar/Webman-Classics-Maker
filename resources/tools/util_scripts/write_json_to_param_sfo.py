from __future__ import print_function
import os
import json
from resources.tools.util_scripts import AppPaths

class Write_param_sfo():
	def execute(self):
		# common paths
		try:
			print("DEBUG game_work_dir path: " + AppPaths.game_work_dir)
			print("DEBUG wcm_gui path: " + AppPaths.wcm_gui)

			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			title = json_data['title'].encode('utf-8')
			title_id = json_data['title_id'].encode('utf-8')

			dummy_title_array = b'\x00'*128
			title = title + dummy_title_array[len(title):]

			dummy_title='PKG/ROM Launcher'

			# load backup and edit it
			with open(os.path.join(AppPaths.util_resources, 'PARAM.SFO.BAK'), 'rb') as f:
				file = f.read()
				f.close()

				# add title
				start_index_title = file.find(dummy_title.encode('utf-8'))
				print('DEBUG: ' + file[888:1025].decode('utf-8'))
				file=file[0:start_index_title] + title + file[start_index_title+len(title):]

				# add title_id
				max_pos_title_id = 1025
				file=file[0:max_pos_title_id-len(title_id)] + title_id + file[max_pos_title_id:]
				print('DEBUG: ' +file[start_index_title:1025].decode('utf-8'))

				# write to generated files
				# newFile = open(os.path.join(AppPaths.pkg, 'PARAM.SFO'), 'wb')
				newFile = open(os.path.join(AppPaths.game_work_dir, 'pkg', 'PARAM.SFO'), 'wb')
				newFileByteArray = bytearray(file)
				newFile.write(newFileByteArray)

				print('\n\n[1/5] Execution of \'write_json_to_param_sfo.py\': DONE')
				print('-----------------------------------------------------')
				return True
		except Exception as e:
			print('\n\n[1/5] Execution of \'write_json_to_param_sfo.py\': FAILED')
			print(getattr(e, 'message', repr(e)))
			print('-----------------------------------------------------')
			return False