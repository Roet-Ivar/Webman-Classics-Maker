import json
import os
import urllib

class Edit_launch_txt:
	def execute(self):
		try:
			with open('../wcm_gui/work_dir/pkg.json ') as f:
				json_data = json.load(f)

			web_command = '/play.ps3'
			web_command_string = web_command + str(json_data['iso_filepath'])
			web_url_string = 'GET ' + urllib.quote(web_command_string) + ' HTTP/1.0'
			
			launch_txt = open("../../pkg/USRDIR/launch.txt", "wb")
			launch_txt_byteArray = bytearray(web_command_string) + os.linesep
			launch_txt.write(launch_txt_byteArray)

			url_txt = open("../../pkg/USRDIR/url.txt", "wb")
			url_txt_byteArray = bytearray(web_url_string) + os.linesep
			url_txt.write(url_txt_byteArray)

			print('Execution of \'edit_launch_txt.py\':         Done')
			print('-----------------------------------------------')
		except Exception as e:
			print('Error: ' + str(e))