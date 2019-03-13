import json
import os
import sys
from ftplib import FTP


class ChunkDownloader():
	def __init__(self, ftp):
		self.ftp = ftp

	def getpart_callback(self, received):
		# print "received a packet"
		if self.cnt <= 0:
			return True
		else:
			# print 'received packet, [0] = %x' % ord(received[0])
			if 'SCES' in received: #.decode('latin-1'):
				print('got SCES: ' + received)
			self.sio.write(received)
			self.outf.write(received)
			self.cnt -= len(received)

	def getpart(self, ftp_filename, rest, cnt, out_filename):
		import StringIO
		self.sio = StringIO.StringIO()
		self.outf = open('_chunk_' + out_filename, 'wb')
		self.cnt = cnt
		self.ftp.voidcmd('TYPE I')
		conn = self.ftp.transfercmd('RETR ' + ftp_filename, rest)
		while 1:
			data = conn.recv(1024)
			if not data:
				break
			if self.getpart_callback(data):
				try:
					# ftp.set_debuglevel(2)
					conn.close()
					self.ftp.voidresp()
				except Exception, e:
					# ftp.set_debuglevel(0)
					# print(e)
					break

		self.outf.close()



current_path= os.getcwd()
# print('current_path: ' + current_path)
if 'util_scripts' not in os.getcwd():
	os.chdir('./resources/tools/util_scripts/')

#Constants
pause_message		= 'Press ENTER to continue...'
mock_data_file		= '../util_resources/mock_ftp_game_list_response.txt'
user_settings_file	= '../../../settings/ftp_settings.txt'
game_data 			= './game_list_data.json'

pspiso_path 		= '/dev_hdd0/PSPISO/'
psxiso_path 		= '/dev_hdd0/PSISO/'
ps2iso_path 		= '/dev_hdd0/PS2ISO/'
ps3iso_path 		= '/dev_hdd0/PS3ISO/'
hdgame_path 		= '/dev_hdd0/game/'

psplines			= []	
psxlines			= []
ps2lines			= []
ps3lines			= []
psnlines			= []




try:
	with open(user_settings_file) as f:
		json_data = json.load(f)
		
		use_mock_data	= json_data['use_mock_data']
		# use_mock_data	= True
		ps3_lan_ip 	= json_data['ps3_lan_ip']
		ftp_timeout 	= json_data['ftp_timeout']
		
		show_psp_list 	= json_data['show_psx_list']
		show_psx_list 	= json_data['show_psx_list']
		show_ps2_list 	= json_data['show_ps2_list']
		show_ps3_list 	= json_data['show_ps3_list']
		show_psn_list 	= json_data['show_psn_list']
		
except Exception, e:
	print('Error: ' + str(e))
	raw_input(pause_message)
	sys.exit()
	
	
try:
	print('Connecting to PS3 at: ' + ps3_lan_ip + ' ...')
	ftp = FTP(ps3_lan_ip, timeout=ftp_timeout)
	ftp.login(user='', passwd = '')

	ftp.retrlines('NLST ' + pspiso_path, psplines.append)
	ftp.retrlines('NLST ' + psxiso_path, psxlines.append)
	ftp.retrlines('NLST ' + ps2iso_path, ps2lines.append)
	ftp.retrlines('NLST ' + ps3iso_path, ps3lines.append)
	ftp.retrlines('NLST ' + hdgame_path, psnlines.append)
	
except Exception, e:
	error_message = str(e)
	if 'Errno 10061' in error_message:
		print('Error: ' + error_message)
		
	else:
		print('Error: ' + error_message)
		print('Check your PS3 ip in webMAN (hold START + SELECT on the XMB), then update /setting/ftp_settings.txt.\n')

	if use_mock_data is True:
		print('\nUsing PS2 ISO mock data for test purposes.')
		raw_input(pause_message)

		with open(mock_data_file, 'rb') as f:
			file = f.read()
			f.close()

			ps2lines = file.split(', ')
	else:
		raw_input(pause_message)
		sys.exit()


def iso_filter(list_of_files):
	list_of_files = list_of_files.lower()
	if '.iso' in list_of_files or '.bin' in list_of_files:
		return True
	else:
		return False


ftp_game_list 	= ''
if(show_psx_list):
	psp_list = ''
	psp_list =  psp_list + (' ______     ___ _____  \n')
	psp_list =  psp_list + ('  _____|   |    _____| \n')
	psp_list =  psp_list + (' |      ___|   |       \n')
	psp_list =  psp_list + ('_______________________\n')
	
	filtered_psplines = filter(iso_filter, psplines)
	if len(filtered_psplines) > 0:
		for isoname in filtered_psplines:
			psp_list = psp_list + (pspiso_path + isoname) + '\n'
		psp_list = psp_list + ('\n')
	else:
		psp_list = psp_list + ('No PSP ISOs found.\n')
	ftp_game_list = ftp_game_list + psp_list + '\n'

if(show_psx_list):
	psx_list = ''
	psx_list =  psx_list + (' ______     ___ _    _  \n')
	psx_list =  psx_list + ('  _____|   |     \__/   \n')
	psx_list =  psx_list + (' |      ___|    _/  \_  \n')
	psx_list =  psx_list + ('_______________________ \n')
	
	filtered_psxlines = filter(iso_filter, psxlines)
	if len(filtered_psxlines) > 0:
		for isoname in filtered_psxlines:
			psx_list = psx_list + (psxiso_path + isoname) + '\n'
		psx_list = psx_list + ('\n')
	else:
		psx_list = psx_list + ('No PSX ISOs found.\n')
	ftp_game_list = ftp_game_list + psx_list + '\n'


if(show_ps2_list):
	ps2_list = ''
	ps2_list = ps2_list + (' ______     ___ _____  \n')
	ps2_list = ps2_list + ('  _____|   |    _____| \n')
	ps2_list = ps2_list + (' |      ___|   |_____  \n')
	ps2_list = ps2_list + ('_______________________\n')

	with open('game_list_data.json') as f:
		json_game_list_data = json.load(f)

	filtered_ps2lines = filter(iso_filter, ps2lines)
	null = None
	game_exist = False

	for ps2_game in filtered_ps2lines:
		game_exist = False
		for list_game in json_game_list_data['ps2_games']:
			if ps2_game == list_game['filename']:
				print('Game exist: ' + ps2_game)
				game_exist = True
				pass
		if not game_exist:
			# print('New game found, adding: ' + ps2_game)
			filename = '/dev_hdd0/PS2ISO/%s' % ps2_game

			try:
				dl = ChunkDownloader(ftp)
				dl.getpart(filename, 0, 750*1024, ps2_game)

				print('Added new game: ' + ps2_game)
			except Exception, e:
				print('Connection timed out when adding: ' + ps2_game + '\nAuto retry attempt in 20s ...')
				import time
				time.sleep(20)
				ftp.close()
				ftp = FTP(ps3_lan_ip, timeout=ftp_timeout)
				ftp.login(user='', passwd='')
				dl = ChunkDownloader(ftp)
				dl.getpart(filename, 0, 750 * 1024, ps2_game)

				print('Added new game: ' + ps2_game)

			json_game_list_data['ps2_games'].append({
				"title_id": null,
				"title": null,
				"game_type": null,
				"filename": ps2_game,
				"last_change": null,
				"installed": null})


	if len(filtered_ps2lines) > 0:
		for isoname in filtered_ps2lines:
			ps2_list = ps2_list + (ps2iso_path + isoname) + '\n'
		ps2_list = ps2_list + ('\n')
	else:
		ps2_list = ps2_list + ('No PS2 ISOs found.\n')
	ftp_game_list = ftp_game_list + ps2_list + '\n'
	
if(show_ps3_list):
	ps3_list = ''
	ps3_list = ps3_list + (' ______     ___ _____  \n')
	ps3_list = ps3_list + ('  _____|   |    _____] \n')
	ps3_list = ps3_list + (' |      ___|    _____] \n')
	ps3_list = ps3_list + ('_______________________\n')
	
	filtered_ps3lines = filter(iso_filter, ps3lines)
	if len(filtered_ps3lines) > 0:
		for isoname in filtered_ps3lines:
			ps3_list = ps3_list + (ps3iso_path + isoname) + '\n'
		ps3_list = ps3_list + ('\n')
	else:
		ps3_list = ps3_list + ('No PS3 ISOs found.\n')
	ftp_game_list = ftp_game_list + ps3_list + '\n'


if(show_psn_list):
	psn_list = ''
	psn_list = psn_list + (' ______     ___ __   _ \n')
	psn_list = psn_list + ('  _____|   |    | \  | \n')
	psn_list = psn_list + (' |      ___|    |  \_| \n')
	psn_list = psn_list + ('_______________________\n')
	
	if len(psnlines) > 0:
		for game_name in psnlines:
			if not game_name in ['.', '..']:
				psn_list = psn_list + (hdgame_path + game_name) + '\n'
		psn_list = psn_list + '\n'
	else:
		psn_list = psn_list + ('No PSN games found.\n')
	ftp_game_list = ftp_game_list + psn_list + '\n'

with open("../../../game_list.txt", "wb") as f:
	f.write(ftp_game_list)

with open('../util_resources/params.json.BAK') as f:
	json_data = json.load(f)

with open("game_list_data.json", "w") as newFile:
	json_text = json.dumps(json_game_list_data, indent=4, separators=(",", ":"))
	newFile.write(json_text)


# print(ftp_game_list)
# raw_input(pause_message)