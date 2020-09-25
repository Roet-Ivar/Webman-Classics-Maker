import json
import os
import urllib
from global_paths import App as AppPaths

class Edit_launch_txt:
	def execute(self):
		try:
			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)


			with open(self.ftp_settings_path, 'r') as settings_file:
				json_settings_data = json.load(settings_file)
				cfg_webcommand = json_settings_data['webcommand']
				settings_file.close()

			# check if the user has added a custom webcommand in the config file
			web_command_string = ''
			if len(cfg_webcommand) > len('[filepath_var]'):
				if '[filepath_var]' in cfg_webcommand:
					web_command_string = cfg_webcommand.replace('[filepath_var]', str(json_data['iso_filepath']))
				else:
					print("""Error: make sure the string [filepath_var] (including brackets) is present in webcommand of settings.cfg""")
					print("""Will revert back to the default webcommand""")


			# # webman-mod v.47.14 and older
			# web_command = '/play.ps3'
			# web_command_string = web_command + str(json_data['iso_filepath'])

			# webman-mod v.47.15 and newer
			if web_command_string == '':
				pre_delay = 6
				post_delay = 3
				pre_cmd = '/wait.ps3?' + str(pre_delay) + ';/mount_ps3'
				post_cmd = ';/wait.ps3?' + str(post_delay) + ';/play.ps3'
				web_command_string = pre_cmd + str(json_data['iso_filepath'] + post_cmd)

			web_url_string = 'GET ' + urllib.quote(web_command_string) + ' HTTP/1.0'

			if not os.path.exists(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR')):
				os.makedirs(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR'))

			launch_txt = open(os.path.join(AppPaths.pkg, 'USRDIR', 'launch.txt'), 'wb')
			launch_txt_byteArray = bytearray(web_command_string) + os.linesep
			launch_txt.write(launch_txt_byteArray)

			url_txt = open(os.path.join(AppPaths.pkg, 'USRDIR', 'url.txt'), 'wb')
			url_txt_byteArray = bytearray(web_url_string) + os.linesep
			url_txt.write(url_txt_byteArray)

			print('Execution of \'edit_launch_txt.py\':         Done')
			print('-----------------------------------------------')

		except Exception as e:
			print('Error: ' + e.message)