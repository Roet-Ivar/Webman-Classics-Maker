import json
import os
import urllib
from global_paths import App as AppPaths

class Edit_launch_txt:
	def execute(self):
		if os.path.exists(AppPaths.game_work_dir):
			work_dir = AppPaths.game_work_dir
			USRDIR = os.path.join(AppPaths.game_work_dir, 'pkg', 'USRDIR')
		else:
			work_dir = AppPaths.wcm_work_dir
			USRDIR = AppPaths.USRDIR

		try:
			with open(os.path.join(work_dir, 'pkg.json')) as f:
				json_data = json.load(f)

			# webman-mod v.47.14 and older
			if False:
				web_command = '/play.ps3'
				web_command_string = web_command + str(json_data['iso_filepath'])

			# webman-mod v.47.15 and newer
			if True:
				pre_delay = 6
				post_delay = 2
				pre_cmd = '/wait.ps3?' + str(pre_delay) + ';/mount_ps3'
				post_cmd = ';/wait.ps3?' + str(post_delay) + ';/play.ps3'
				web_command_string = pre_cmd + str(json_data['iso_filepath'] + post_cmd)

			web_url_string = 'GET ' + urllib.quote(web_command_string) + ' HTTP/1.0'

			launch_txt = open(os.path.join(USRDIR, 'launch.txt'), 'wb')
			launch_txt_byteArray = bytearray(web_command_string) + os.linesep
			launch_txt.write(launch_txt_byteArray)

			url_txt = open(os.path.join(USRDIR, 'url.txt'), 'wb')
			url_txt_byteArray = bytearray(web_url_string) + os.linesep
			url_txt.write(url_txt_byteArray)

			print('Execution of \'edit_launch_txt.py\':         Done')
			print('-----------------------------------------------')
		except Exception as e:
			print('Error: ' + str(e))