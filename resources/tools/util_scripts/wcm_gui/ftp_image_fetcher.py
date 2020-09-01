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

class FtpGameList():
    def __init__(self):
        # messages
        self.PAUSE_MESSAGE              = 'Press ENTER to continue...'
        self.CONNECTION_ERROR_MESSAGE   = "Check your PS3 ip-address in webMan VSH menu (hold SELECT on the XMB), then update your 'settings/ftp_settings.py' accordingly"
        self.MOCK_DATA_MESSAGE          = 'DEBUG: Using PS2 ISO mock data for test purposes!'
        self.TITLE_ID_EXCEPTION_MESSAGE = """Exception: 'get_image' failed during regex operation."""

        # constants
        self.MOCK_DATA_FILE         = os.path.join(AppPaths.util_resources, 'mock_ftp_game_list_response.txt')
        self.GAME_LIST_DATA_FILE    = os.path.join(AppPaths.application_path, 'game_list_data.json')
        self.NEW_LIST_DATA_FILE     = os.path.join(AppPaths.util_resources, 'game_list_data.json.BAK')

        self.PSP_ISO_PATH           = '/dev_hdd0/PSPISO/'
        self.PSX_ISO_PATH           = '/dev_hdd0/PSXISO/'
        self.PS2_ISO_PATH           = '/dev_hdd0/PS2ISO/'
        self.PS3_ISO_PATH           = '/dev_hdd0/PS3ISO/'

        # system specifict FTP data
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
        with open(os.path.join(AppPaths.settings, 'ftp_settings.cfg')) as f:
            ftp_settings_file = json.load(f)
            f.close()

        # self.chunk_size_kb          = ftp_settings_file['chunk_size_kb']
        self.ftp_chunk_size_kb      = 5000
        self.ftp_rest               = 0
        self.ps3_lan_ip             = ftp_settings_file['ps3_lan_ip']
        self.ftp_timeout            = ftp_settings_file['ftp_timeout']
        self.ftp_pasv_mode          = ftp_settings_file['ftp_pasv_mode']
        self.ftp_user               = ftp_settings_file['ftp_user']
        self.ftp_password           = ftp_settings_file['ftp_password']
        self.use_mock_data          = False

        # platforms to handle
        self.show_psp_list  = ftp_settings_file['show_psx_list']
        self.show_psx_list  = ftp_settings_file['show_psx_list']
        self.show_ps2_list  = ftp_settings_file['show_ps2_list']
        self.show_ps3_list  = ftp_settings_file['show_ps3_list']
        self.show_psn_list  = ftp_settings_file['show_psn_list']



        # singular instances
        self.ftp = None
        self.ftp_chunk_dl = None

    def execute(self):
        try:
            print('Connection attempt to: ' + self.ps3_lan_ip + ', timeout set to ' + str(self.ftp_timeout) + 's...\n')
            self.ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout)
            self.ftp.set_pasv = self.ftp_pasv_mode
            self.ftp.login(user=self.ftp_user, passwd=self.ftp_password)
            self.ftp.voidcmd('TYPE I')

            self.ftp.retrlines('NLST ' + self.PSP_ISO_PATH, self.psplines.append)
            self.ftp.retrlines('NLST ' + self.PSX_ISO_PATH, self.psxlines.append)
            self.ftp.retrlines('NLST ' + self.PS2_ISO_PATH, self.ps2lines.append)
            self.ftp.retrlines('NLST ' + self.PS3_ISO_PATH, self.ps3lines.append)

            self.all_lines.append(self.psplines)
            self.all_lines.append(self.psxlines)
            self.all_lines.append(self.ps2lines)
            self.all_lines.append(self.ps3lines)

            self.ftp_chunk_dl = FTPChunkDownloader(self.ftp)

        except Exception as e:
            error_message = str(e)
            print('Connection error: ' + error_message)
            print(self.CONNECTION_ERROR_MESSAGE)
            print('\n')

            return

        # open a copy of the current gamelist from disk
        with open(self.GAME_LIST_DATA_FILE) as f:
            self.json_game_list_data = json.load(f)

        # open a copy of an empty gamelist from disk
        with open(self.NEW_LIST_DATA_FILE) as f:
            self.new_json_game_list_data = json.load(f)

        # append the platform lists
        for platform in self.json_game_list_data:
            self.new_platform_list_data = self.list_builder(platform[0:3])

            self.json_game_list_data[platform].extend(self.new_platform_list_data[platform])

        # save the updated gamelist to disk
        with open(self.GAME_LIST_DATA_FILE, 'w') as newFile:
            json_text = json.dumps(self.json_game_list_data, indent=4, separators=(",", ":"))
            newFile.write(json_text)


    def list_builder(self, platform):
        if 'psp' == platform.lower():
            platform_list   = 'psp_games'
            platform_path   = self.PSP_ISO_PATH
            platform_filter = self.psp_filter
            platform_lines  = self.psplines
        elif 'psx' == platform.lower():
            platform_list   = 'psx_games'
            platform_path   = self.PSX_ISO_PATH
            platform_filter = self.psx_filter
            platform_lines  = self.psxlines
        elif 'ps2' == platform.lower():
            platform_list   = 'ps2_games'
            platform_path   = self.PS2_ISO_PATH
            platform_filter = self.ps2_filter
            platform_lines  = self.ps2lines
        elif 'ps3' == platform.lower():
            platform_list   = 'ps3_games'
            platform_path   = self.PS3_ISO_PATH
            platform_filter = self.ps3_filter
            platform_lines  = self.ps3lines

        # filer the lines using the platform filter
        filtered_lines = filter(platform_filter, platform_lines)
        null = None     # to comply with json syntax
        # game_exist = False

        title = null
        title_id = null
        meta_data_link = null

        for game_filename in filtered_lines:
            game_exist = False

            # check if game exist
            for list_game in self.json_game_list_data[platform_list]:
                if game_filename == list_game['filename']:
                    print('\nSkipped ' + game_filename + ', it already exists\n')
                    game_exist = True
                    pass

            # if not, add it
            if not game_exist:

                # get title_id from the ISO using ftp
                title_id = self.get_title_id_from_ps3(platform_path, game_filename)

                if title_id is not None and title_id != '':
                    platform_db_file = platform + '_all_title_ids.json'

                    with open(os.path.join(AppPaths.games_metadata, platform_db_file)) as f:
                        self.json_platform_data_list = json.load(f)

                    # check for for match the platform game database
                    games = self.json_platform_data_list['games']
                    for game in games:

                        # find a match in of title_id
                        if platform == 'ps3':
                            title_id = title_id.replace('-', '')

                        if title_id == str(game['title_id']):

                            if platform == 'psp' or platform == 'psx' or platform == 'ps2':
                                title = str(game['title'])

                                # if game['meta_data_link'] is not null:
                                #     meta_data_link = str(game['meta_data_link'])

                            elif platform == 'ps3':
                                title = str(game['name'])
                                print('ps3 title: ' + title)



                            # removes parenthesis including content of title
                            title = re.sub(r'\([^)]*\)', '', title)
                            title = re.sub(r'\[[^)]*\]', '', title)

                            # if str(title).isupper() and str(meta_data_link) == null:
                            #     # if no meta_data_link, capitalize titles with all upper-case
                            #     title = title.title()
                            break

                # if no title is found, use filename as title
                if title is None:
                    game_filepath = os.path.join(platform_path, game_filename)

                    if game_filepath.lower().endswith('iso'):
                        m_filename = re.search('ISO.*', game_filepath)
                        if m_filename is not None:
                            title = m_filename.group(0).replace('ISO/', '')

                    elif game_filepath.lower().endswith('bin'):
                        m_filename = re.search('BIN.*', game_filepath)
                        if m_filename is not None:
                            title = m_filename.group(0).replace('BIN/', '')

                # check for duplicates of the same title in the list
                for game in self.json_game_list_data[platform_list]:
                    # maybe check against title_id instead?
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

                # add game an image
                self.new_json_game_list_data[platform + '_games'].append({
                    "title_id": title_id,
                    "title": title,
                    "platform": platform.upper(),
                    "filename": game_filename,
                    "path": platform_path,
                    "meta_data_link": meta_data_link})

                # reset game data for next iterationF
                title 			= null
                title_id 		= null
                meta_data_link 	= null

        print('DEBUG: new games added:')
        print(str(self.new_json_game_list_data))

        return self.new_json_game_list_data

    def get_title_id_from_ps3(self, platform_path, game_filename):
        game_filepath = os.path.join(platform_path, game_filename)

        if self.ftp_chunk_dl is None:
            raise Exception('ERROR in ftp_chunk_dl: No instance of self.ftp_chunk_dl found.')

        try:
            title_id = self.ftp_chunk_dl.get_file_data_chunk(game_filepath, self.ftp_chunk_size_kb)

         # retry connection
        except Exception as e:
            print('Connection timed out when parsing: ' + game_filename + '\nAuto retry in ' + str(self.ftp_timeout) + 's...\n')

            if '' is not e.message:
                print('DEBUG - ftp_game_list execute: ' + e.message)

            self.make_new_ftp()
            self.ftp_chunk_dl = FTPChunkDownloader(self.ftp)
            # title_id = self.ftp_chunk_dl.get_title_id(game_filepath, self.chunk_size_kb)
            title_id = self.ftp_chunk_dl.get_file_data_chunk(game_filepath, self.ftp_rest, self.ftp_chunk_size_kb)

        return title_id


    def make_new_ftp(self):

        if None is not self.ftp:
            self.ftp.close()
            time.sleep(self.ftp_timeout)

        self.ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout)
        self.ftp.set_pasv=self.ftp_pasv_mode
        self.ftp.login(user='', passwd='')


class FTPChunkDownloader():
    def __init__(self, ftp):
        self.ftp_instance = ftp
        self.ftp_instance.voidcmd('TYPE I')
        self.null = None
        self.file_data_chunk = None

    def get_file_data_chunk(self, ftp_filename, rest, chunk_size_kb):
        def fill_buffer(self, received):
            # tmp_arr = ''
            # for char in received:
            #     char = char
            #     buffer data clean-up
            #     if ord(char) < 32 or ord(char) > 126:
            #         tmp_arr = tmp_arr + ' '
            #     else:
            #         if char == ';':
            #             char = '\n'
            #
            #         tmp_arr = tmp_arr + str(char)

            if self.cnt <= 0:
                return True

            else:
                self.sio.write(received)
            self.cnt -= len(received)




        self.sio = StringIO.StringIO()
        self.cnt = chunk_size_kb * 1024
        # self.cnt = cnt * 1000
        self.ftp_instance.voidcmd('TYPE I')

        conn = self.ftp_instance.transfercmd('RETR ' + ftp_filename, chunk_size_kb, rest)


        game_id = None

        while 1:
            # the buffer size seems a bit random, can't remember why
            data = conn.recv(1460)
            if not data:
                break
            if fill_buffer(self, data):
                try:
                    conn.close()
                    self.ftp_instance.voidresp()

                # intended exception: this is thrown when the final data chunk been stored in buffer
                except Exception as e:
                    iso_index = ftp_filename.index('ISO/', 0, len(ftp_filename))
                    platform = ftp_filename[iso_index-3: iso_index].lower()
                    game_name = ftp_filename[iso_index+4: len(ftp_filename)-4]

                    self.file_data_chunk = self.sio.getvalue()
                    self.sio.close()

                    # do stuff here
                    game_id = get_png_from_buffer(self, platform, game_name, self.file_data_chunk)


                    # conn.close()
                    if '451' not in e.message:
                        print('DEBUG - fill_buffer error: ' + e.message)
                    break
        if game_id == None:
            game_id = ''
        return game_id

def get_png_from_buffer(self, platform, game_name, buffer_data):
    self.data = buffer_data
    game_id = None
    try:
        # let's try PS3 ISO files first'
        if platform == 'ps3':
            self.has_icon0 = False
            self.has_pic0 = False
            self.has_pic1 = False


            # these byte sequences are standard start and end of PNGs
            def png_finder(data):
                index_png_start = data.find(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
                index_png_end = data.find(b'\x00\x00\x00\x00\x49\x45\x4E\x44', index_png_start)

                image_exist = False
                if index_png_start != -1:
                    if index_png_end != -1:
                        import PIL.Image as Image
                        import io

                        png_byte_array = data[index_png_start:index_png_end+8]
                        image = Image.open(io.BytesIO(png_byte_array))

                        img_name = None
                        img_exist = False

                        if image.size == (320, 176):
                            img_name = 'ICON0.PNG'
                            if self.has_icon0:
                                img_exist = True
                            self.has_icon0 = True

                        # when multiple pic0 the first seem to be English
                        elif image.size == (1000, 560):
                            img_name = 'PIC0.PNG'
                            if self.has_pic0:
                                img_exist = True
                            self.has_pic0 = True


                        elif image.size == (1920, 1080):
                            img_name = 'PIC1.PNG'
                            if self.has_pic1:
                                img_exist = True
                            self.has_pic1 = True

                        # exclude that data for next iteration
                        self.data = data[index_png_end:len(data)-1]

                        # save image
                        if img_name is not None:

                            if not img_exist:
                                image.show()
                                print('DEBUG Found ' + img_name + ' for ' + "\'" + game_name + "\'")
                                newFile = open(os.path.join(AppPaths.application_path, img_name), 'wb')
                                newFile.write(png_byte_array)
                            return True
                    return False
            while png_finder(self.data):
                print()

    except Exception:
        print('get_image_from_buffer_exception: ' + self.TITLE_ID_EXCEPTION_MESSAGE)
    finally:
        return game_id

# TODO: different sources for meta data
class GameMetadataFetcher():
    def __init__(self, game_json_data):

        game_data = game_json_data

