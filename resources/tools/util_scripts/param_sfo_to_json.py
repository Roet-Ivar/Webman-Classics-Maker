from __future__ import print_function
import os, json

from resources.tools.util_scripts import AppPaths

class Param_to_json:
	def execute(self):
		# common paths
		with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
			json_data = json.load(f)


		# load it
		with open(os.path.join(AppPaths.util_resources, 'PARAM.SFO_MOD.BAK'), 'rb') as f:
			file = f.read()
			f.close()
			
			try:
				print('\n-----------------------------------------------')
				params = file[912:1400]
				params_arr = [x for x in params.split(b'\x00') if x != '']
				# print(params_arr)

				json_data['title']=params_arr[0]
				json_data['title_id']=params_arr[1]
				json_data['content_id']='UP0001-'+ params_arr[1] + '_00-0000000000000000'
				json_data['path']=params_arr[3]

				newFile = open(os.path.join(AppPaths.game_work_dir, 'pkg.json'), 'wb')
				json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
				
				newFile.write(json_text)

				print('Execution of \'param_sfo_json.py\':          Done')
				print('-----------------------------------------------')
			except ValueError:
				print("File write error: 'PKGLAUNCH' not found or 'title_id' not a string")