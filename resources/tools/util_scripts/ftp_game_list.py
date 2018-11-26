import json
import os
import sys
from ftplib import FTP


current_path= os.getcwd()
# print('current_path: ' + current_path)
if '\util_scripts' not in os.getcwd():
	os.chdir('./resources/tools/util_scripts/')

if not os.path.exists('./build'):
	os.makedirs('./build')

mock = False
mock_data_file = '../util_resources/mock_ftp_game_list_response.txt'
user_settings_file = '../util_user_settings/user_settings.txt'

psxiso_path  = '/dev_hdd0/PSISO/'
ps2iso_path = '/dev_hdd0/PS2ISO/'
ps3iso_path = '/dev_hdd0/PS3ISO/'
psn_games_path = '/dev_hdd0/games/'

psxlines = []
ps2lines = []
ps3lines = []
psnlines = []


if os.path.isfile(mock_data_file) or os.path.isfile(user_settings_file):
	with open(user_settings_file) as f:
		json_data = json.load(f)
		
		ps3_lan_ip = json_data['ps3_lan_ip']
		show_psx_list = json_data['show_psx_list']
		show_ps2_list = json_data['show_ps2_list']
		show_ps3_list = json_data['show_ps3_list']
		show_psn_list = json_data['show_psn_list']
else:
	print('Error: either ' + mock_data_file + ' or ' + user_settings_file + ' not found.')
	os.system("pause")
	sys.exit()
	


print('Connecting to PS3 at: ' + ps3_lan_ip)

try:
	ftp = FTP(ps3_lan_ip, timeout=5)
	ftp.login(user='', passwd = '')

	ftp.retrlines('NLST ' + psxiso_path, psxlines.append)
	ftp.retrlines('NLST ' + ps2iso_path, ps2lines.append)
	ftp.retrlines('NLST ' + ps3iso_path, ps3lines.append)
	ftp.retrlines('NLST ' + psn_games_path, psnlines.append)
	
except:
	print('\nERROR: The connecton timed out. \nCheck your PS3 FTP-IP in webMAN (hold SELECT for 2-3s), then update the /util_user_setting/user_setting.txt.\n')
	print('Using PS2 ISO mock data.')
	os.system("pause")
	# mock = True	#Remove this line later


if mock is True:
	with open(mock_data_file, 'rb') as f:
		file = f.read()
		f.close()

		ps2lines = file.split(', ')


def iso_filter(list_of_files):
	if('.iso' in list_of_files):
		return True
	else:
		return False

		
if(show_psx_list):
	filtered_psxlines = filter(iso_filter, psxlines)
	print(' ______     ___ _    _  ')
	print('  _____|   |     \__/   ')
	print(' |      ___|    _/  \_  ')
	print('______________________  ')
	 
	if len(filtered_psxlines) > 0:
		for isoname in filtered_psxlines:
			print(psxiso_path + isoname)
		print('\n')
	else:
		print('No PSX ISOs found.\n')


if(show_ps2_list):
	filtered_ps2lines = filter(iso_filter, ps2lines)
	print(' ______     ___ _____   ')
	print('  _____|   |    _____|  ')
	print(' |      ___|   |_____   ')
	print('_______________________ ')

	if len(filtered_ps2lines) > 0:
		for isoname in filtered_ps2lines:
			print(ps2iso_path + isoname)
		print('\n')
	else:
		print('No PS2 ISOs found.\n')
	
	
if(show_ps3_list):
	filtered_ps3lines = filter(iso_filter, ps3lines)
	print(' ______     ___ _____   ')
	print('  _____|   |    _____]  ')
	print(' |      ___|    _____]  ')
	print('______________________  ')

	if len(filtered_ps3lines) > 0:
		for isoname in filtered_ps3lines:
			print(ps3iso_path + isoname)
		print('\n')
	else:
		print('No PS3 ISOs found.\n')


if(show_psn_list):
	print(' ______     ___ __   _  ')
	print('  _____|   |    | \  |  ')
	print(' |      ___|    |  \_|  ')
	print('______________________  ')

	if len(psnlines) > 0:
		for games in psnlines:
			print(psn_games_path + isoname)
		print('\n')
	else:
		print('No PSN games found.\n')
		
os.system("pause")