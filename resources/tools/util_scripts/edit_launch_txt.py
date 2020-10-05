import json
import os
import urllib
from global_paths import App as AppPaths

class Edit_launch_txt:
	def execute(self):
		try:
			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			with open(os.path.join(AppPaths.settings, 'ftp_settings.cfg'), 'r') as settings_file:
				json_settings_data = json.load(settings_file)
				settings_file.close()

			# init variables
			web_command_string = ''
			iso_filepath = str(json_data['iso_filepath'])
			cfg_webcommand = json_settings_data['webcommand']

			if '/pspiso/' in iso_filepath.lower():
				web_command_string = '/mount_ps3' + iso_filepath + ';/wait.ps3?8;/browser.ps3$focus_segment_index xmb_app3 0;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$focus_index 0 4;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$exec_push'

			# check if the user has added a custom webcommand in the config file
			else:
				if len(cfg_webcommand) > len('[filepath_var]'):
					if '[filepath_var]' in cfg_webcommand:
						web_command_string = cfg_webcommand.replace('[filepath_var]', str(json_data['iso_filepath']))
						web_command_string = web_command_string.replace('//', '/')
					else:
						print("""Error: make sure the string [filepath_var] (including brackets) is present in webcommand of settings.cfg""")
						print("""Will revert back to the default webcommand""")

				# webman-mod v.47.30 and older
				if web_command_string == '':
					pre_delay = 6
					post_delay = 4
					pre_cmd = '/wait.ps3?' + str(pre_delay) + ';/mount_ps3'
					post_cmd = ';/wait.ps3?' + str(post_delay) + ';/play.ps3'
					web_command_string = pre_cmd + str(json_data['iso_filepath'] + post_cmd)

				# # webman-mod v.47.31 and newer
				# if web_command_string == '':
				# 	pre_cmd = '/wait.ps3?xmb;/play.ps3'
				# 	web_command_string = pre_cmd + str(json_data['iso_filepath'])

			web_url_string = 'GET ' + urllib.quote(web_command_string) + ' HTTP/1.0'

			if not os.path.exists(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR')):
				os.makedirs(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR'))

			launch_txt = open(os.path.join(AppPaths.pkg, 'USRDIR', 'launch.txt'), 'wb')
			launch_txt_byteArray = bytearray(web_command_string, 'utf8') + os.linesep
			launch_txt.write(launch_txt_byteArray)

			url_txt = open(os.path.join(AppPaths.pkg, 'USRDIR', 'url.txt'), 'wb')
			url_txt_byteArray = bytearray(web_url_string) + os.linesep
			url_txt.write(url_txt_byteArray)

			print('[3/5] Execution of \'edit_launch_txt.py\':         DONE')
			print('-----------------------------------------------------')
			return True

		except Exception as e:
			print('[3/5] Execution of \'edit_launch_txt.py\':         FAILED')
			print('Error: ' + e.message)
			print('-----------------------------------------------------')
			return False
