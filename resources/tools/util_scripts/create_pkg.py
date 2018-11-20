# :: ------------------------------------------------------------------
# :: Simple script to build a proper PKG using Python (by CaptainCPS-X)
# :: ------------------------------------------------------------------


import json
import os
import shutil

class Create_pkg:
	def execute(self):
		with open('../util_generated_files/params.json') as f:
			json_data = json.load(f)

		content_id = str(json_data['content_id'])

		title_id = str(json_data['title_id'])
		# print(title_id)

		filepath = str(json_data['iso_filepath'])
		filepath_arr = [x for x in filepath.split('/')]
		# print(filepath)
		# print(filepath_arr)

		pkg_build_script='./pkg_build_scripts/pkg.py'
		pkg_flag='--contentid'
		pkg_dir='../../pkg/'
		# pkg_name = content_id + '.pkg'
		pkg_name = title_id + '_' + filepath_arr[3][:-4] + '.pkg'
		pkg_name = pkg_name.replace(' ', '_')
		build_dir='../../../builds/'

		# print('pkg_build_script: ' + pkg_build_script)
		# print('pkg_flag: ' + pkg_flag)
		# print('pkg_dir: ' + pkg_dir)
		# print('pkg_name: ' + pkg_name)

		execute_string = 'python' + ' '  + pkg_build_script + ' ' + pkg_flag + ' ' + content_id + ' ' + pkg_dir + ' ' + pkg_name
		# print(execute_string)
		os.system(execute_string)

		shutil.move(pkg_name, build_dir + pkg_name)

		print('Execution of \'create_pkg.py\': Done')
		print('------------------------------------------------\n' + 'Package created: ' + '/Builds/' + pkg_name)
