from __future__ import print_function
import json
import os
import urllib
from global_paths import App as AppPaths

class Edit_launch_txt:
	def execute(self):
		try:
			with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			from global_paths import FtpSettings

			# init variables
			web_command_string = ''
			path = str(json_data['path'])
			full_path = path + str(json_data['filename'])

			cfg_webcommand = FtpSettings.webcommand

			if '/PSPISO/' in path:
				web_command_string = '/mount_ps3' + path + ';/wait.ps3?8;/browser.ps3$focus_segment_index xmb_app3 0;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$focus_index 0 4;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$exec_push;/wait.ps3?1;/browser.ps3$exec_push'
			elif '/GAMES/' in path or '/GAMEZ/' in path:
				split_path = path.split('/')
				folder_path = '/'.join(split_path[0:len(split_path) -1])
				pre_delay = 'xmb'
				post_delay = 4
				pre_cmd = '/wait.ps3?' + str(pre_delay) + ';/mount_ps3'
				post_cmd = ';/wait.ps3?' + str(post_delay) + ';/play.ps3'
				web_command_string = pre_cmd + str(full_path) + post_cmd

			# check if the user has added a custom webcommand in the config file
			else:
				if len(cfg_webcommand) > len('[filepath_var]'):
					if '[filepath_var]' in cfg_webcommand:
						web_command_string = cfg_webcommand.replace('[filepath_var]', str(full_path))
						web_command_string = web_command_string.replace('//', '/')
					else:
						print("""Error: make sure the string [filepath_var] (including brackets) is present in webcommand of settings.cfg""")
						print("""Will revert back to the default webcommand""")

				# webman-mod v.47.30 and newer
				if web_command_string == '':
					pre_delay = 'xmb'
					post_delay = 4
					pre_cmd = '/wait.ps3?' + str(pre_delay) + ';/mount_ps3'
					post_cmd = ';/wait.ps3?' + str(post_delay) + ';/play.ps3'
					web_command_string = pre_cmd + str(full_path + post_cmd)

			web_url_string = 'GET ' + urllib.quote(web_command_string) + ' HTTP/1.0'

			if not os.path.exists(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR')):
				os.makedirs(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR'))

			launch_txt = open(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR', 'launch.txt'), 'wb')
			launch_txt_byteArray = bytearray(web_command_string, 'utf8') + os.linesep
			launch_txt.write(launch_txt_byteArray)

			url_txt = open(os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR', 'url.txt'), 'wb')
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
