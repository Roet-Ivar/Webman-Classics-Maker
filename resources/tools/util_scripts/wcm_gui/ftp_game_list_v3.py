import json, os, re, StringIO, sys, time
from ftplib import FTP
from shutil import copyfile

# adding util_scripts depending on if it's an executable or if it's running from the wcm_gui
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts'))
else:
    sys.path.append('..')

from global_paths import App as AppPaths
sys.path.append(AppPaths.settings)
import ftp_settings

class FtpGameList():
    def __init__(self):
        # messages
        self.PAUSE_MESSAGE              = 'Press ENTER to continue...'
        self.CONNECTION_ERROR_MESSAGE   = "Find your PS3 ip in webMAN VSH menu (hold START + SELECT on the XMB), then update your 'ftp_settings.txt' accordingly"
        self.MOCK_DATA_MESSAGE          = 'DEBUG: Using PS2 ISO mock data for test purposes!'
        self.TITLE_ID_EXCEPTION_MESSAGE = 'Exception: get_title_id failed during regex operation.'

        # constants
        self.MOCK_DATA_FILE         = os.path.join(AppPaths.util_resources, 'mock_ftp_game_list_response.txt')
        self.USER_SETTINGS_FILE     = os.path.join(AppPaths.settings, 'ftp_settings.txt')
        self.GAME_LIST_DATA_FILE    = os.path.join(AppPaths.util_scripts, 'game_list_data.json')

        self.PSP_ISO_PATH           = '/dev_hdd0/PSPISO/'
        self.PSX_ISO_PATH           = '/dev_hdd0/PSXISO/'
        self.PS2_ISO_PATH           = '/dev_hdd0/PS2ISO/'
        self.PS3_ISO_PATH           = '/dev_hdd0/PS3ISO/'
        self.HDD_GAME_PATH          = '/dev_hdd0/game/'

        # variables
        self.psplines   = []
        self.psxlines   = []
        self.ps2lines   = []
        self.ps3lines   = []
        self.psnlines   = []
        self.all_lines  = []

        self.ftp_game_list  = ''
        self.psp_list       = ''
        self.psx_list       = ''
        self.ps2_list       = ''
        self.ps3_list       = ''
        self.psn_list       = ''

        # filters
        self.psp_filter = lambda x: x.endswith('.bin') or x.endswith('.iso')
        self.psx_filter = lambda x: x.endswith('.bin') or x.endswith('.iso')
        self.ps2_filter = lambda x: x.endswith('.bin') or x.endswith('.iso')
        self.ps3_filter = lambda x: x.endswith('.bin') or x.endswith('.iso')

        # ftp settings
        self.chunk_size_kb          = ftp_settings.chunk_size_kb
        self.ps3_lan_ip             = ftp_settings.ps3_lan_ip
        self.ftp_timeout            = ftp_settings.ftp_timeout
        self.ftp_passive_mode       = ftp_settings.ftp_passive_mode
        self.ftp_user               = ftp_settings.ftp_user
        self.ftp_password           = ftp_settings.ftp_password
        self.use_mock_data          = False

        # platforms to handle
        self.show_psp_list 		    = ftp_settings.show_psx_list
        self.show_psx_list 		    = ftp_settings.show_psx_list
        self.show_ps2_list 		    = ftp_settings.show_ps2_list
        self.show_ps3_list 		    = ftp_settings.show_ps3_list
        self.show_psn_list 		    = ftp_settings.show_psn_list

        # singular instances
        self.ftp = None

    def execute(self):
        try:
            print('Connecting to PS3 at: ' + self.ps3_lan_ip + ', using a timeout of ' + str(self.ftp_timeout) + 's...\n')
            self.ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout)
            self.ftp.set_pasv=self.ftp_passive_mode
            self.ftp.login(user=self.ftp_user, passwd=self.ftp_password)

            self.ftp.retrlines('NLST ' + self.PSP_ISO_PATH, self.psplines.append)
            self.ftp.retrlines('NLST ' + self.PSX_ISO_PATH, self.psxlines.append)
            self.ftp.retrlines('NLST ' + self.PS2_ISO_PATH, self.ps2lines.append)
            self.ftp.retrlines('NLST ' + self.PS3_ISO_PATH, self.ps3lines.append)
            self.ftp.retrlines('NLST ' + self.HDD_GAME_PATH,self.psnlines.append)

            self.all_lines.append(self.psplines)
            self.all_lines.append(self.psxlines)
            self.all_lines.append(self.ps2lines)
            self.all_lines.append(self.ps3lines)

            ftp_chunk_dl = FTPChunkDownloader(self.ftp)

        except Exception as e:
            error_message = str(e)
            if 'Errno 10061' in error_message:
                print('Error: ' + error_message)

            else:
                print('Error: ' + error_message)
                print(self.CONNECTION_ERROR_MESSAGE)
                print('\n')

            if self.use_mock_data is True:
                print('\n')
                print(self.MOCK_DATA_MESSAGE)
                raw_input(self.PAUSE_MESSAGE)

                with open(self.MOCK_DATA_FILE, 'rb') as f:
                    file = f.read()
                    f.close()

                    self.ps2lines = file.split(', ')
            else:
                print(self.PAUSE_MESSAGE)


        if(self.show_psx_list):
            platform = 'psp'
            filtered_psplines = filter(lambda x: x.endswith('.bin') or x.endswith('.iso'), self.psplines)
            if len(filtered_psplines) > 0:
                for iso_name in filtered_psplines:
                    self.psp_list.join(self.PSP_ISO_PATH + iso_name + '\n')
                self.psp_list.join('\n')
            else:
                self.psp_list.join('No PSP ISOs found.\n')
            self.ftp_game_list.join(self.psp_list + '\n')

        if(self.show_psx_list):
            platform = 'psx'
            filtered_psxlines = filter(lambda x: x.endswith('.bin') or x.endswith('.iso'), self.psxlines)
            if len(filtered_psxlines) > 0:
                for isoname in filtered_psxlines:
                    self.psx_list.join(self.PSX_ISO_PATH + isoname + '\n')
                self.psx_list.join('\n')
            else:
                self.psx_list.join('No PSX ISOs found.\n')
            self.ftp_game_list.join(self.psx_list + '\n')


        if(self.show_ps2_list):
            platform = 'ps2'

            if 'ps2' == platform:
                platform_list   = 'ps2_games'
                platform_path   = self.PS2_ISO_PATH
                platform_filter = self.ps2_filter
                platform_lines  = self.ps2lines

            with open(self.GAME_LIST_DATA_FILE) as f:
                json_game_list_data = json.load(f)

            filtered_ps2lines = filter(platform_filter, platform_lines)
            null = None
            # game_exist = False

            title = null
            title_id = null
            meta_data_link = null

            for game_filename in filtered_ps2lines:
                game_exist = False

                # check if game exist
                for list_game in json_game_list_data[platform_list]:
                    if game_filename == list_game['filename']:
                        print('\nExisting game: ' + game_filename + '\n')
                        game_exist = True
                        pass

                # if not, add it
                if not game_exist:
                    game_filepath = platform_path + game_filename
                    try:
                        title_id = ftp_chunk_dl.get_title_id(game_filepath, 0, self.chunk_size_kb)

                    # retry connection
                    except Exception as e:
                        print('Connection timed out when adding: ' + game_filename + '\nAuto retry in ' + str(self.ftp_timeout) + ' s...\n')

                        if '' is not e.message:
                            print('DEBUG in ftp_game_list execute: ' + e.message)

                        self.ftp.close()
                        time.sleep(self.ftp_timeout)

                        self.ftp = FTP(self.ps3_lan_ip, timeout=10)
                        self.ftp.set_pasv=self.ftp_passive_mode
                        self.ftp.login(user='', passwd='')

                        ftp_chunk_dl = FTPChunkDownloader(self.ftp)
                        title_id = ftp_chunk_dl.get_title_id(game_filepath, 0, self.chunk_size_kb)

                    with open(os.path.join(AppPaths.games_metadata, 'region_list.json')) as f:
                        region_json_data = json.load(f)

                    # gets all region list data based on platform
                    region_ids = region_json_data[platform.upper()]
                    for region_id in region_ids:

                        # find the correct region from title_id e.g: 'SLUS' -> U-NTSC PS2 games
                        if len(str(title_id)) == 10 and title_id[0:4] in region_id['id']:
                            # print('DEBUG Platform/region: ' + platform.upper() + '/' + id_reg['region'].upper())

                            # with a known region we can now load the correct game database (json file)
                            with open(os.path.join(AppPaths.games_metadata, 'ps2_pcsx2_list.json')) as f:
                                games_list_json_data = json.load(f)

                            # iterate through the games in the game database
                            games = games_list_json_data['games']
                            for game in games:
                                # find a match in of title_id
                                if title_id == str(game['title_id']):
                                    title = str(game['title'])

                                    if game['meta_data_link'] is not null:
                                        meta_data_link = str(game['meta_data_link'])

                                    # removes parenthesis including content of title
                                    title = re.sub(r'\([^)]*\)', '', title)
                                    title = re.sub(r'\[[^)]*\]', '', title)

                                    if str(title).isupper() and str(meta_data_link) == null:
                                        # if no meta_data_link, capitalize titles with all upper-case
                                        title = title.title()
                                    break

                    # if no title_id, use filename as title
                    if title_id is None:
                        m_filename = re.search('ISO.*', game_filepath)
                        title = m_filename.group(0).replace('ISO/', '')

                    # check for duplicates of the same title in the list
                    for game in json_game_list_data[platform_list]:
                        if str(title) == str(game['title']):

                            # check if there are earlier duplicates title + (1), (2) etc
                            dup_title = re.search('\(\d{1,3}\)$', str(title))
                            if dup_title is not None:
                                pre = str(title)[:len(str(title))-3]
                                suf = str(title)[len(str(title))-3:]
                                new_suf = re.sub('\d(?!\d)', lambda x: str(int(x.group(0)) + 1), suf)
                                title = pre + new_suf

                            # no earlier duplicates, makes the first one (1)
                            else:
                                title = str(title) + ' (1)'


                    print("Added '" + str(title) + "' to the list:\n"
                          + 'Platform: ' + platform.upper() + '\n'
                          + 'Filename: ' + game_filename + '\n'
                          + 'Title id: ' + str(title_id) + '\n')

                    # add game to ps2 games
                    json_game_list_data['ps2_games'].append({
                        "title_id": title_id,
                        "title": title,
                        "platform": platform.upper(),
                        "filename": game_filename,
                        "installed": null,
                        "meta_data_link": meta_data_link})

                    # reset game data for next iteration
                    title 			= null
                    title_id 		= null
                    meta_data_link 	= null

            # build the text list for manual use, just as the other platforms
            if len(filtered_ps2lines) > 0:
                for isoname in filtered_ps2lines:
                    self.ps2_list.join(self.PS2_ISO_PATH + isoname + '\n')
                self.ps2_list.join('\n')
            else:
                self.ps2_list.join('No PS2 ISOs found.' + '\n')
            self.ftp_game_list.join(self.ps2_list + '\n')

        if(self.show_ps3_list):
            platform = 'ps3'

            filtered_ps3lines = filter(lambda x: x.endswith('.bin') or x.endswith('.iso'), self.ps3lines)
            if len(filtered_ps3lines) > 0:
                for isoname in filtered_ps3lines:
                    self.ps3_list.join(self.PS3_ISO_PATH + isoname + '\n')
                self.ps3_list.join('\n')
            else:
                self.ps3_list.join('No PS3 ISOs found.\n')

            self.ftp_game_list.join(self.ps3_list + '\n')


        if(self.show_psn_list):
            platform = 'psn'
            if len(self.psnlines) > 0:
                for game_name in self.psnlines:
                    if not game_name in ['.', '..']:
                        self.psn_list.join(self.HDD_GAME_PATH + game_name + '\n')
                self.psn_list.join('\n')
            else:
                self.psn_list.join('No PSN games found.\n')
            self.ftp_game_list.join(self.psn_list + '\n')


        # write game list to files
        with open(os.path.join(AppPaths.application_path, 'game_list.txt'), 'wb') as f:
            f.write(self.ftp_game_list)

        with open(self.GAME_LIST_DATA_FILE, 'w') as newFile:
            json_text = json.dumps(json_game_list_data, indent=4, separators=(",", ":"))
            newFile.write(json_text)



class FTPChunkDownloader():
    def __init__(self, ftp):
        self.ftp_instance = ftp
        self.null = None

    def get_title_id(self, ftp_filename, rest, cnt):
        def fill_buffer(self, received):
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


        def get_id_from_buffer(self, buffer_data):
            game_id = self.null
            try:
                for m in re.finditer("""\w{4}\_\d{3}\.\d{2}""", buffer_data):
                    game_id = str(m.group(0)).strip()
                    game_id = game_id.replace('_', '-')
                    game_id = game_id.replace('.', '')

            except Exception:
                print(self.TITLE_ID_EXCEPTION_MESSAGE)
            finally:
                return game_id


        self.sio = StringIO.StringIO()
        self.cnt = cnt * 1024
        self.ftp_instance.voidcmd('TYPE I')

        conn = self.ftp_instance.transfercmd('RETR ' + ftp_filename, rest)
        game_id = self.null

        while 1:
            data = conn.recv(1460)
            if not data:
                break
            if fill_buffer(self, data):
                try:
                    conn.close()
                    self.ftp_instance.voidresp()

                # intended exception: this is thrown when the data chunk been stored in buffer
                except Exception as e:
                    game_id = get_id_from_buffer(self, self.sio.getvalue())
                    self.sio.close()
                    conn.close()
                    if '451 ERR' not in e.message:
                        print('DEBUG in fill_buffer: ' + e.message)
                    break
        return game_id

# TODO: different sources for meta data
class GameMetadataFetcher():
    def __init__(self, game_json_data):

        game_data = game_json_data

    # get gamedata from 'psx data center' local file
    def get_title_from_pdc(self):
        print()
    # get metadata from pcsx2 wiki
    def get_title_from_pcsx2(self):
        print()
    # get metadata from launchbox local file
    def get_title_from_pcsx2(self):
        print()