import json
import os
import sys
import re
import StringIO
import time
from ftplib import FTP


class GameMetadataFetcher():
	def __init__(self, game_json_data):
		game_data = game_json_data

		if game_data['meta_data_link'] is not null:
			print('Game')

	# get gamedata from 'psx data center' local file
	def get_title_from_pdc(self):
			print()
	# get metadata from pcsx2 wiki
	def get_title_from_pcsx2(self):
			print()
	# get metadata from launchbox local file
	def get_title_from_pcsx2(self):
			print()

	# def get_game_title(self):
	# 	def collect

class FTPChunkDownloader():
	def __init__(self, ftp):
		self.ftp = ftp

	def get_title_id(self, ftp_filename, rest, cnt):
		self.sio = StringIO.StringIO()
		self.cnt = cnt
		self.ftp.voidcmd('TYPE I')
		conn = self.ftp.transfercmd('RETR ' + ftp_filename, rest)
		game_id = null

		while 1:
			data = conn.recv(1460)
			if not data:
				break
			if self.get_chunk_callback(data):
				try:
					conn.close()
					self.ftp.voidresp()

				# intended exception is thrown when chunk has been loaded in memory
				except Exception, e:
					game_id = self.get_chunk(self.sio.getvalue())
					self.sio.close()
					conn.close()
					break
		return game_id

	def get_chunk_callback(self, received):
		tmp_arr = ''
		for char in received:

			if ord(char) < 32 or ord(char) > 126:
				tmp_arr = tmp_arr + ' '
			else:
				if char == ';':
					char = '\n'
				tmp_arr = tmp_arr + str(char)
		if self.cnt <= 0:
			return True

		else:
			self.sio.write(tmp_arr)

		self.cnt -= len(received)

	def get_chunk(self, buffer_data):
		game_id = null
		try:
			for m in re.finditer("""\w{4}\_\d{3}\.\w{2}""", buffer_data):
				game_id = str(m.group(0)).strip()
				game_id = game_id.replace('_', '-')
				game_id = game_id.replace('.', '')

		except Exception, e1:
			print('get_title_id exception: ' + e1)
			game_id = null
		finally:
			return game_id

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

platform 			= None




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
	platform = 'psp'
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
	platform = 'psx'
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
	platform = 'ps2'
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
	meta_data_link = null
	chunk_size = 750

	for ps2_game in filtered_ps2lines:
		game_exist = False
		for list_game in json_game_list_data['ps2_games']:
			if ps2_game == list_game['filename']:
				print('\nExisting game: ' + ps2_game + '\n')
				game_exist = True
				pass
		if not game_exist:
			filename = '/dev_hdd0/PS2ISO/%s' % ps2_game
			try:
				dl = FTPChunkDownloader(ftp)
			except Exception, e:
				print('FTPChunkDownloader exception: ' + str(e))
			try:
				title_id = dl.get_title_id(filename, 0, chunk_size * 1024)
				print('Added new game: ' + ps2_game + '\nGame_id: ' + title_id)

			# retry connection
			except Exception, e2:
				print('get_title_id exception: ' + str(e2))

				# print(e)
				print('Connection timed out when adding: ' + ps2_game + '\nAuto retry attempt in 10s ...')
				ftp.close()
				time.sleep(10)

				ftp = FTP(ps3_lan_ip, timeout=30)
				ftp.login(user='', passwd='')

				dl = FTPChunkDownloader(ftp)
				title_id = dl.get_title_id(filename, 0, chunk_size * 1024)

				print('Added new game: ' + ps2_game + '\nGame_id: ' + title_id)

			with open('./games_metadata/region_list.json') as f:
				region_json_data = json.load(f)


			id_region_list = region_json_data[platform.upper()]
			for id_reg in id_region_list:
				if title_id[0:4] in id_reg['id']:
					tmp_reg = id_reg['region']
					print('Platform/region: ' + platform.upper() + '/' + tmp_reg)

					with open('./games_metadata/' + platform + '_' + tmp_reg + '_games_list.json') as f:
						games_list_json_data = json.load(f)

					games = games_list_json_data['games']
					for game in games:
						title = null
						meta_data_link = null

						tmp_title_id = str(game['title_id'])
						if title_id == tmp_title_id:
							title = str(game['title'])
							if game['meta_data_link'] is not null:
								meta_data_link = str(game['meta_data_link'])
							# remove parenthesis and content
							title = re.sub(r'\([^)]*\)', '', title)

							if title.isupper() and meta_data_link == null:
								# if no meta link, fix uppercase titles
								title = title.title()
							print('Title: ' + title + '\n')
							break




			json_game_list_data['ps2_games'].append({
				"title_id": title_id,
				"title": title,
				"game_type": platform,
				"filename": ps2_game,
				"installed": null,
				"meta_data_link": meta_data_link})


	if len(filtered_ps2lines) > 0:
		for isoname in filtered_ps2lines:
			ps2_list = ps2_list + (ps2iso_path + isoname) + '\n'
		ps2_list = ps2_list + ('\n')
	else:
		ps2_list = ps2_list + ('No PS2 ISOs found.\n')
	ftp_game_list = ftp_game_list + ps2_list + '\n'
	
if(show_ps3_list):
	platform = 'ps3'
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