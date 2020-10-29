import copy, json, os, re, StringIO, sys, time, traceback
import PIL.Image as Image
from ftplib import FTP
from shutil import copyfile

# adding util_scripts depending on if it's an executable or if it's running from the wcm_gui
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts'))
else:
    sys.path.append('..')

from global_paths import App as AppPaths
from global_paths import GlobalVar
from global_paths import GlobalDef

sys.path.append(AppPaths.settings)

class FtpGameList():
    def __init__(self, selected_drive, selected_platform):
        # drive and platforms to fetch
        self.global_drive_paths = GlobalVar.drive_paths
        self.global_platform_paths = GlobalVar.platform_paths

        self.selected_drives = []
        self.platform_filter = []

        # fix drive path based on gamelist filter
        if any(x in selected_drive for x in ['ALL']): #, 'USB(*)']):
            self.selected_drives.extend(GlobalVar.drive_paths)
            if self.selected_drives.count(('/dev_usb(*)/', 'USB(*)')) > 0:
                self.selected_drives.remove(('/dev_usb(*)/', 'USB(*)'))
        elif any(x in selected_drive for x in ['USB(*)']):
            self.selected_drives.extend(GlobalVar.drive_paths)
            if self.selected_drives.count(('/dev_usb(*)/', 'USB(*)')) > 0:
                self.selected_drives.remove(('/dev_usb(*)/', 'USB(*)'))
            if self.selected_drives.count(('/dev_hdd0/', 'HDD0')) > 0:
                self.selected_drives.remove(('/dev_hdd0/', 'HDD0'))
        else:
            self.selected_drives.extend(filter(lambda x: str(selected_drive) == x[1], self.global_drive_paths))

        # fix platform path based on gamelist filter
        if 'ALL' in selected_platform:
            self.platform_filter.extend(self.global_platform_paths)
        else:
            self.platform_filter.extend(filter(lambda x: str(selected_platform) == x[1], self.global_platform_paths))

        # messages
        self.PAUSE_MESSAGE              = 'Press ENTER to continue...'
        self.CONNECTION_ERROR_MESSAGE   = "TIPS: Check your PS3 ip-address in webMan VSH menu (hold SELECT on the XMB)"
        self.TITLE_ID_EXCEPTION_MESSAGE = """Exception: 'get_image' failed during regex operation."""

        # constants
        self.GAME_LIST_DATA_FILE    = os.path.join(AppPaths.application_path, 'game_list_data.json')
        self.NEW_LIST_DATA_FILE     = os.path.join(AppPaths.util_resources, 'game_list_data.json.BAK')

        # ftp settings
        with open(os.path.join(AppPaths.settings, 'ftp_settings.cfg')) as f:
            ftp_settings_file = json.load(f)
            f.close()

        # some PSP-images is found around 20MB into the ISO
        self.ftp_psp_png_offset_kb  = ftp_settings_file['ftp_psp_png_offset_kb']
        self.chunk_size_kb          = ftp_settings_file['ftp_chunk_size_kb']
        self.chunk_size_kb          = ftp_settings_file['ftp_chunk_size_kb']
        self.ps3_lan_ip             = ftp_settings_file['ps3_lan_ip']
        self.ftp_timeout            = ftp_settings_file['ftp_timeout']
        self.ftp_pasv_mode          = ftp_settings_file['ftp_pasv_mode']
        self.ftp_user               = ftp_settings_file['ftp_user']
        self.ftp_password           = ftp_settings_file['ftp_password']
        self.ftp_folder_depth       = ftp_settings_file['ftp_folder_depth']
        self.ftp_retry_count        = ftp_settings_file['ftp_retry_count']

        # platform ISO paths
        self.ntfs_lines = []
        self.psp_lines  = []
        self.psx_lines  = []
        self.ps2_lines  = []
        self.ps3_lines  = []
        self.all_lines  = []

        # singular instances
        self.total_lines_count = 0
        self.game_count = 0

        self.ftp = None
        self.data_chunk = None

    def execute(self):
        try:
            print('Connection attempt to ' + self.ps3_lan_ip + ', timeout set to ' + str(self.ftp_timeout) + 's...\n')
            self.ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout)
            self.ftp.set_pasv = self.ftp_pasv_mode
            self.ftp.login(user=self.ftp_user, passwd=self.ftp_password)
            self.ftp.voidcmd('TYPE I')

            # get a listing of active drives
            active_drives_list = []
            self.ftp.retrlines('MLSD /', active_drives_list.append)

            # filter out all active drives that are also selected
            filtered_drives = []
            for sd in self.selected_drives:
                for a in active_drives_list:
                    ad = '/' + str(a).split(';')[6].strip() + '/'
                    if sd[0] == ad:
                        print('DEBUG adding drive: ' + ad + ' for scanning')
                        filtered_drives.append(sd)
            if len(filtered_drives) < 1:
                print('''DEBUG: The USB port you're trying to scan is not active''')

            for drive in filtered_drives:
                for platform in self.platform_filter:
                    if 'PSP' == platform[1]:
                        self.ftp_walk(self.ftp, drive[0] + platform[0], self.psp_lines)
                    elif 'PSX' in platform[1]:
                        self.ftp_walk(self.ftp, drive[0] + platform[0], self.psx_lines)
                    elif 'PS2' in platform[1]:
                        self.ftp_walk(self.ftp, drive[0] + platform[0], self.ps2_lines)
                    elif 'PS3' in platform[1]:
                        self.ftp_walk(self.ftp, drive[0] + platform[0], self.ps3_lines)
                    elif 'NTFS' in platform[1] and 'HDD0' in drive[1]:
                            self.ftp_walk(self.ftp, drive[0] + platform[0], self.ntfs_lines)
                    # elif 'GAMES' in platform[1] and 'HDD0' in drive[1]:
                    #     self.ftp_walk(self.ftp, drive[0] + platform[0], self.games_lines)


            # filter out any empty entries
            self.all_lines.append(self.psp_lines)
            self.all_lines.append(self.psx_lines)
            self.all_lines.append(self.ps2_lines)
            self.all_lines.append(self.ps3_lines)
            self.all_lines.append(self.ntfs_lines)

            for p in self.all_lines:
                self.total_lines_count += len(p)

            # after retrieving the list of file paths we fetch the actual data
            self.data_chunk = FTPDataHandler(self.ftp, self.total_lines_count)

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
            self.new_platform_list_data = self.list_builder(str(platform).split('_')[0].upper())

        # save updated gamelist to disk
        with open(self.GAME_LIST_DATA_FILE, 'w') as newFile:
            json_text = json.dumps(self.json_game_list_data, indent=4, separators=(",", ":"))
            newFile.write(json_text)


    def list_builder(self, original_platform):
        if 'PSP' in original_platform:
            platform_list = 'psp_games'
            filtered_platform = self.psp_lines
        elif 'PSX' in original_platform:
            platform_list = 'psx_games'
            filtered_platform = self.psx_lines
        elif 'PS2' in original_platform:
            platform_list = 'ps2_games'
            filtered_platform = self.ps2_lines
        elif 'PS3' in original_platform:
            platform_list = 'ps3_games'
            filtered_platform = self.ps3_lines
        elif 'NTFS' in original_platform:
            platform_list = 'ntfs_games'
            filtered_platform = self.ntfs_lines

        # instantiate variables
        title_id = None
        meta_data_link = None
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None

        for game_filename in filtered_platform:
            game_exist = False
            filepath = game_filename
            dir_path = os.path.dirname(filepath).__add__('/')
            filename = os.path.basename(filepath)
            platform_path = dir_path
            platform = original_platform

            # check if game exist
            for game in self.json_game_list_data[platform_list]:
                game_path = str(os.path.join(game['path'], game['filename']))
                if filepath == game_path:
                    self.game_count += 1
                    print('DEBUG PROGRESS: ' + "{:.0%}".format(float(self.game_count).__div__(float(self.total_lines_count))) + ' (' + str(self.game_count) + '/' + str(self.total_lines_count) + ')')
                    print('\nDEBUG skipping ' + filename + ', already fetched\n')
                    game_exist = True
                    pass


            # .NTFS[xxx] gets a donor platform for metadata scraping
            if platform == 'NTFS':
                match = re.search('(?<=\[).*?(?=\])', filename)
                if match is not None:
                    # These will not match: '.NTFS[BDISO]', '.NTFS[DVDISO]', '.NTFS[BDFILE]',
                    tmp_platform = filter(lambda x: match.group() in x[0], self.global_platform_paths)
                    if tmp_platform:
                        platform = tmp_platform[0][1]


            # if not, add it
            if not game_exist:
                title_id, icon0, pic0, pic1, pic2, at3, pam = self.get_game_data(dir_path, filename)
                title = filename.strip()

                # removes the file extension and use it as title
                for file_ext in GlobalVar.file_extensions:
                    if filename.upper().endswith(file_ext):
                        title = title[0:len(title)-len(file_ext)]
                        break

                # removes parenthesis & brackets including their content
                title = re.sub(r'\([^)]*\)', '', title)
                title = re.sub(r'\[[^)]*\]', '', title)

                # read platform db
                platform_db_file = platform + '_all_title_ids.json'
                with open(os.path.join(AppPaths.games_metadata, platform_db_file)) as f:
                    self.json_platform_metadata = json.load(f)


                # check for for match the platform game database
                if title_id is not None and title_id is not '':
                    for game in self.json_platform_metadata['games']:
                        # adapt the title_id format for the xml db
                        if platform == 'PS3':
                            title_id = title_id.replace('-', '')

                        if title_id == game['title_id']:
                            if platform == 'PSP' or platform == 'PSX' or platform == 'PS2':
                                title = game['title'].encode('utf-8').strip()

                                if game['meta_data_link'] is not None:
                                    meta_data_link = game['meta_data_link']

                            elif platform == 'PS3':
                                # use the first element for English
                                title = game['locale'][0]['title'].encode('utf-8').strip()

                            break

                # check for duplicates of the same title
                dup_list = []
                for _platform in self.json_game_list_data:
                    for game in self.json_game_list_data[_platform]:
                        dup_match = re.search('^' + title + '\s(\()\d{1,3}?(\))$', game['title'])
                        if title == game['title'] or dup_match:
                            dup_list.append(game['title'].encode('utf-8').strip())
                # if there they are the same, append suffix ' (1)'
                if len(dup_list) == 1 and dup_list[0] == title:
                        title = title + ' (1)'
                # if more than one we need to figure out what suffix to append
                elif len(dup_list) > 1:
                    new_title = ''
                    curr_dup_number = 1
                    for dup in dup_list:
                        # a dup_title must have a '(#)' pattern
                        dup_match = re.search('(?<=\()\d{1,3}?(?=\))', dup)
                        if dup_match is not None:
                            new_number = dup_match.group()
                            pre_string = str(dup).replace('(' + new_number + ')', '')
                            # title should match the pre_string w/o '(#)' pattern
                            if title == pre_string.strip() and new_number > curr_dup_number:
                                curr_dup_number += 1
                                suf_string = '(' + str(curr_dup_number) + ')'
                                new_title = pre_string + suf_string
                    title = new_title
                    # if there was no '(#)' pattern duplicates
                    if new_title == '':
                        for dup in dup_list:
                            if title == dup:
                                # make the first duplicate
                                title = title + ' (1)'
                                break

                title = title.replace('  ', ' ')
                title = title.strip().encode('utf-8')

                # add game to list of new games
                self.game_count += 1
                print('DEBUG PROGRESS: ' + "{:.0%}".format(float(self.game_count).__div__(float(self.total_lines_count))) + ' (' + str(self.game_count) + '/' + str(self.total_lines_count) + ')')

                if platform != original_platform:
                    platform = original_platform

                self.new_json_game_list_data[platform_list].append({
                    "title_id": title_id,
                    "title": title,
                    "platform": platform,
                    "filename": filename,
                    "path": platform_path,
                    "meta_data_link": meta_data_link})

                # also append it to the existing list for next iteration
                self.json_game_list_data[platform_list].append({
                    "title_id": title_id,
                    "title": title,
                    "platform": platform,
                    "filename": filename,
                    "path": platform_path,
                    "meta_data_link": meta_data_link})

                print('DEBUG \'' + filename + '\' got the title \'' + str(title) + '\'' + '\n')
                print("Added '" + str(title) + "' to the list:\n"
                      + 'Platform: ' + platform + '\n'
                      + 'Filename: ' + filename + '\n'
                      + 'Title id: ' + str(title_id) + '\n')



            # save data to game build folder here
            if title_id is not None and title_id is not '':
                game_folder_name = filename[:-4].replace(' ', '_') + '_(' + title_id.replace('-', '') + ')'
                game_build_dir = os.path.join(AppPaths.builds, game_folder_name)

                # making sure the work_dir and pkg directories exists
                if not os.path.exists(os.path.join(game_build_dir, 'work_dir', 'pkg')):
                    os.makedirs(os.path.join(game_build_dir, 'work_dir', 'pkg'))

                # save images to game work folders
                self.image_saver(platform, game_build_dir, [icon0, pic0, pic1, pic2, at3, pam])

            # reset game data for next iteration
            title = None
            title_id = None
            meta_data_link = None
            platform = original_platform

        return self.new_json_game_list_data

    def get_game_data(self, platform_path, game_filename):
        title_id = None
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None

        game_filepath = os.path.join(platform_path, game_filename)

        try:
            split_folder_path = game_filepath.split('/')
            platform_str = split_folder_path[2] + '/'
            platform_match = filter(lambda x: platform_str in x[0], self.global_platform_paths)
            platform = str(platform_match[0][1]).upper()

            original_platform = platform
            # this is where .NTFS[xxx] files need a donor platform
            if platform == 'NTFS':
                match = re.search('(?<=\[).*?(?=\])', game_filename)
                if match is not None:
                    # These will not match: '.NTFS[BDISO]', '.NTFS[DVDISO]', '.NTFS[BDFILE]',
                    donor_platform = filter(lambda x: match.group() in x[0], self.global_platform_paths)
                    if donor_platform:
                        platform = donor_platform[0][1]

        except Exception as e:
            print('ERROR could not parse platform')
            print(e.message)

        try:
            # if no offset
            title_id, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, self.chunk_size_kb, 0, self.game_count, self.ftp_retry_count)

            # make another fetch with rest offset for PSP images
            if platform == 'PSP':
                not_used, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, self.chunk_size_kb, self.ftp_psp_png_offset_kb, self.game_count, self.ftp_retry_count)

            # PS3 guitar hero games needs a larger chunk to find the PIC1
            elif platform == 'PS3' and 'guitar' in game_filename.lower():
                not_used, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, 6000, 0, self.game_count, self.ftp_retry_count)

        # retry connection
        except Exception as e:
            print('DEBUG Error: ' + e.message)
            print('Connection timed out, re-connecting in ' + str(self.ftp_timeout) + 's...\n')

            self.make_new_ftp()
            self.data_chunk = FTPDataHandler(self.ftp, self.total_lines_count)

            title_id, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, self.chunk_size_kb, 0, self.game_count, self.ftp_retry_count)

            # make another fetch with rest offset for PSP images
            if platform == 'PSP':
                title_id, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, self.chunk_size_kb, self.ftp_psp_png_offset_kb, self.game_count, self.ftp_retry_count)

            # PS3 guitar hero games needs a larger chunk to find the PIC1
            elif platform == 'PS3' and 'guitar' in game_filename.lower():
                not_used, icon0, pic0, pic1, pic2, at3, pam = self.data_chunk.ftp_buffer_data(game_filepath, platform, 6000, 0, self.game_count, self.ftp_retry_count)

        return title_id, icon0, pic0, pic1, pic2, at3, pam

    def ftp_walk(self, ftp, folder_path, files):
        print('DEBUG adding path for scanning:' + folder_path)
        depth = len(folder_path.split('/')) -2
        extensions = GlobalVar.file_extensions

        if '/dev_usb' in folder_path:
            # check what usb-drive are available so we can speed things up
            isPath = False
            folder_list = []
            split_folder_path = folder_path.split('/')

            folder_base_path = '/' + '/'.join(split_folder_path[1: len(split_folder_path)-2]) + '/'
            folder_name = split_folder_path[len(split_folder_path)-2]

            # retrieve folders in the basepath we're scanning and check if our dir is listed
            self.ftp.retrlines('MLSD ' + folder_base_path, folder_list.append)
            for d in folder_list:
                ds = str(d).split(';')[6].strip()
                if folder_name == ds:
                    isPath = True
                    break
            if not isPath:
                return files

        # only NTFS extensions valid in this folder
        elif 'tmp/wmtmp/' in folder_path:
            extensions = tuple([i for i in list(extensions) if 'NTFS' in i])

        # TODO: implement /Games PARAMS.SFO parser
        elif 'Games/' in folder_path:
            return files

        dirs = []
        stuff = []
        try:
            ftp.retrlines('MLSD ' + folder_path, stuff.append)
        except Exception as e:
            print('DEBUG retrlines error: ' + e.message)
            return files

        for item in stuff:
            split_item = item.split(';')
            # check if it's a dir or a file
            if split_item[0] == 'type=dir':
                dirs.append(split_item[len(split_item)-1].strip())

            elif split_item[0] == 'type=file':
                # a file must have at least size of 1 byte
                if 'size=' in split_item[1] and int(split_item[1].replace('size=', '')) > 0:
                    filename = split_item[len(split_item)-1].strip()

                    # make sure that .BIN.ENC files has capitalized extension
                    if filename.upper().endswith('.BIN.ENC'):
                        if filename.endswith('.BIN.ENC'):
                            files.append(os.path.join(folder_path + split_item[len(split_item) - 1].strip()))
                        else:
                            # we need to return here or it will be included in the next clause
                            return files
                    # check if filename ends with any of our white listed extensions
                    elif filename.upper().endswith(extensions):
                        files.append(os.path.join(folder_path + split_item[len(split_item) - 1].strip()))

        if len(dirs) > 0 and depth < self.ftp_folder_depth:
            for subdir in sorted(dirs):
                current_dir = os.path.join(folder_path, subdir + '/')
                self.ftp_walk(ftp, current_dir, files)
        return files


    def make_new_ftp(self):

        if None is not self.ftp:
            self.ftp.close()
            time.sleep(self.ftp_timeout)

        self.ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout)
        self.ftp.set_pasv=self.ftp_pasv_mode
        self.ftp.login(user='', passwd='')

    def image_saver(self, platform, game_build_dir, images):
        import shutil
        import PIL.Image as Image
        import io

        icon0 = images[0]
        pic0 = images[1]
        pic1 = images[2]
        pic2 = images[3]
        at3 = images[4]
        pam = images[5]

        game_work_dir = os.path.join(game_build_dir, 'work_dir')
        game_pkg_dir = os.path.join(game_work_dir, 'pkg')
        try:
            if os.path.isdir(game_pkg_dir):
                shutil.rmtree(game_pkg_dir)
                os.makedirs(game_pkg_dir)
        except Exception as e:
            print('ERROR: could not clean the folder: ' + game_work_dir + '\n' +
                  'Please close any file browser accessing the specific folder.')


        GlobalDef().copytree(os.path.join(AppPaths.util_resources, 'pkg_dir_bak'), os.path.join(game_work_dir, 'pkg'))

        # platforms such as PSP needs rescaling of images
        if icon0 is not None:
            icon0_image = Image.open(io.BytesIO(icon0)).convert("RGBA")

            if platform == 'PSP':
                t_icon0 = Image.open(os.path.join(AppPaths.application_path, 'resources', 'images', 'pkg', 'default', 'transparent_ICON0.PNG')).convert("RGBA")
                icon0_image = icon0_image.resize((int(icon0_image.width*2), int(icon0_image.height*2)), Image.ANTIALIAS)
                x_pos = (t_icon0.width - icon0_image.width)/2
                y_pos = (t_icon0.height - icon0_image.height)/2
                t_icon0.paste(icon0_image, (x_pos, y_pos), icon0_image)

                t_icon0.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PNG'))
            else:
                icon0_image.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PNG'))
                # icon0_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PNG'), "wb")
                # icon0_file.write(icon0)
                # icon0_file.close()

        else:
            default_pkg_img_dir = os.path.join(AppPaths.resources, 'images', 'pkg', 'default')
            icon0_platform_path = os.path.join(default_pkg_img_dir, platform, 'ICON0.PNG')
            if not os.path.isfile(icon0_platform_path):
                platform = ''
            # icon0_image = Image.open(os.path.join(default_pkg_img_dir, platform, 'ICON0.PNG')).convert("RGBA")
            # icon0_image.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PNG'))
            shutil.copyfile(os.path.join(default_pkg_img_dir, platform, 'ICON0.PNG'), os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PNG'))


        if pic0 is not None:
            pic0_image = Image.open(io.BytesIO(pic0)).convert("RGBA")
            if platform == 'PSP':
                t_pic0 = Image.open(os.path.join(AppPaths.application_path, 'resources', 'images', 'pkg', 'default', 'transparent_PIC0.PNG')).convert("RGBA")
                x_pos = (t_pic0.width - pic0_image.width)/2
                y_pos = (t_pic0.height - pic0_image.height)/2
                t_pic0.paste(pic0_image, (x_pos, y_pos), pic0_image)

                t_pic0.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC0.PNG'))
            else:
                # pic0_image.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC0.PNG'))
                pic0_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC0.PNG'), "wb")
                pic0_file.write(pic0)
                pic0_file.close()

        if pic1 is not None:
            pic1_image = Image.open(io.BytesIO(pic1)).convert("RGBA")
            if platform == 'PSP':
                t_pic1 = Image.open(os.path.join(AppPaths.application_path, 'resources', 'images', 'pkg', 'default', 'transparent_PIC1.PNG')).convert("RGBA")
                pic1_image = pic1_image.resize((int(pic1_image.width*3), int(pic1_image.height*3)), Image.ANTIALIAS)
                x_pos = (t_pic1.width - pic1_image.width)/2
                y_pos = (t_pic1.height - pic1_image.height)/2
                t_pic1.paste(pic1_image, (x_pos, y_pos), pic1_image)

                t_pic1.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC1.PNG'))
            else:
                # pic1_image.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC1.PNG'))
                pic1_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC1.PNG'), "wb")
                pic1_file.write(pic1)
                pic1_file.close()


        if pic2 is not None:
            pic2_image = Image.open(io.BytesIO(pic2)).convert("RGBA")
            if platform == 'PS3':
                # pic2_image.save(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC2.PNG'))
                pic2_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'PIC2.PNG'), "wb")
                pic2_file.write(pic2)
                pic2_file.close()

        if at3 is not None:
            if platform == 'PS3':
                # for .AT3 we need to save the binary data to a file
                at3_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'SND0.AT3'), "wb")
                at3_file.write(at3)
                at3_file.close()

        if pam is not None:
            if platform == 'PS3':
                # for .PAM we need to save the binary data to a file
                pam_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON1.PAM'), "wb")
                pam_file.write(pam)
                pam_file.close()

        # if at3 is not None or pam is not None:
        #     if platform == 'PS3':
        #         # add PS3LOGO.DAT
        #         shutil.copyfile(os.path.join(AppPaths.util_resources, 'PS3_LOG_DAT.BAK'), os.path.join(game_build_dir, 'work_dir', 'pkg', 'PS3LOGO.DAT'))


        # elif platform == 'PSP':
        #     # for .PMF we need to save the binary data to a file
        #     pmf_file = open(os.path.join(game_build_dir, 'work_dir', 'pkg', 'ICON0.PMF'), "wb")
        #     pmf_file.write(pam)
        #     pmf_file.close()


class FTPDataHandler:
    def __init__(self, ftp, total_lines):
        self.global_platform_paths = GlobalVar.platform_paths
        self.ftp_instance = ftp
        self.ftp_instance.voidcmd('TYPE I')
        self.null = None
        self.total_lines = total_lines

    def ftp_buffer_data(self, filepath, platform, chunk_size, rest, game_count, ftp_retry_count):
        icon0 = None
        pic0 = None
        pic1 = None
        pic2 = None
        at3 = None
        pam = None

        filename = os.path.basename(filepath)
        game_title = filename[0:len(filename) - 4]

        file_size_bytes = self.ftp_instance.size(filepath)
        if file_size_bytes > 0 and file_size_bytes < (chunk_size * 1024):
            chunk_size = (file_size_bytes / 1024) * 0.95
        elif platform == ('PSX', 'PS2'):
            chunk_size = 750

        if rest * 1024 > file_size_bytes:
            rest = 0

        def fill_buffer(self, received):
            if self.chunk_size <= 0:
                return True
            else:
                self.sio.write(received)
            self.chunk_size -= len(received)


        game_title_id = ''
        self.sio = StringIO.StringIO()
        self.chunk_size = chunk_size * 1024

        offset = max(rest*1024, 0)
        conn = self.ftp_instance.transfercmd('RETR ' + filepath, rest=offset)
        retry_cnt = 0
        while 1:
            # the buffer size seems a bit random, can't remember why(?)
            try:
                data = conn.recv(1460)
            except Exception as e1:
                error_msg = ''
                if e1.message is not '':
                    error_msg = e1.message
                else:
                    error_msg = repr(e1)
                    # print('DEBUG ERROR traceback: ' + str(traceback.print_exc()))
                    # offset = max(rest*1024, 0)

                print('ERROR when fetching \'' + filename + '\', reason: ' + error_msg)
                print('DEBUG Retrying fetching of \'' + filename + '\'')
                retry_cnt += 1
                print('DEBUG retry_cnt: ' + str(retry_cnt))
                # retry fetching
                if retry_cnt < ftp_retry_count:
                    try:
                        conn = self.ftp_instance.transfercmd('RETR ' + filepath, rest=offset)
                    except:
                        print('ERROR could not refetch ' + filename + ', skipping metadata')
                        data = None
                else:
                    print('ERROR could not refetch ' + filename + ', skipping metadata')
                    break

            # if None: refetch has failed => skip game by breaking the loop
            if data is None:
                game_count += 1
                print('DEBUG PROGRESS: ' + "{:.0%}".format(float(game_count).__div__(float(self.total_lines))) + ' (' + str(game_count) + '/' + str(self.total_lines) + ')')
                break
            else:
                if fill_buffer(self, data):
                    try:
                        conn.close()
                        self.ftp_instance.voidresp()

                    # intended exception: this is thrown when the full data chunk been stored in buffer
                    except Exception as e:
                        # reset values for next round
                        icon0 = None
                        pic0 = None
                        pic1 = None
                        pic2 = None
                        pam = None
                        at3 = None

                        self.data_chunk = self.sio.getvalue()
                        self.sio.close()

                        # try find title_id from beginning of file for all platforms
                        if rest == 0:
                            game_title_id = get_title_id_from_buffer(self, platform, self.data_chunk)

                        # PS3 and PSP are the only platforms that has game art embedded
                        if platform == 'PSP' or platform == 'PS3':
                            icon0, pic0, pic1, pic2 = get_png_from_buffer(self, platform, filename, self.data_chunk)

                            if platform == 'PS3':
                                at3 = get_AT3_from_buffer(self, platform, filename, self.data_chunk)
                                pam = get_PAM_from_buffer(self, platform, filename, self.data_chunk)

                                try:
                                    at3_size_KB = int(len(at3)*0.978/1000)
                                except:
                                    at3_size_KB = 0
                                try:
                                    pam_size_KB = int(len(at3)*0.978/1000)
                                except:
                                    pam_size_KB = 0

                                if at3_size_KB + pam_size_KB > 24000:
                                    print("ERROR: the sum of the sizes of SND0.AT3 + ICON1.PAM can't be larger than 2.4MB")

                        # Error 451 is normal when closing the conection
                        if '451' not in e.message:
                            print('DEBUG - connection ' + e.message + ' during data fetching of ' + filename)
                        break

        return game_title_id, icon0, pic0, pic1, pic2, at3, pam


def get_title_id_from_buffer(self, platform, buffer_data):
    title_id = ''
    try:
        # psx and ps2
        if platform == 'PSX' or platform == 'PS2':
            for m in re.finditer("""\w{4}\_\d{3}\.\d{2}""", buffer_data):
                if m is not None:
                    title_id = str(m.group(0)).strip()
                    title_id = title_id.replace('_', '-')
                    title_id = title_id.replace('.', '')

        elif platform == 'PS3':
            for m in re.finditer("""\w{4}-\d{5} """, buffer_data):
                if m is not None:
                    title_id = str(m.group(0)).strip()

        elif platform == 'PSP':
            for m in re.finditer("""\w{4}-\d{5}\|""", buffer_data):
                title_id = str(m.group(0)).strip()
                title_id = title_id[0:len(title_id)-1]

    except Exception as e:
        print('ERROR -> get_title_id_from_buffer: ' + e.message)
    finally:
        return title_id

def get_png_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data

    try:
        self.has_icon0 = False
        self.has_pic0 = False
        self.has_pic1 = False
        self.has_pic2 = False
        self.image_duplicate = False

        self.icon0_image = None
        self.pic0_image = None
        self.pic1_image = None
        self.pic2_image = None
        self.image_name = None

        # these byte sequences are standard start and end of PNGs
        def png_finder(data, image_name):
            index_png_start = data.find(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
            png_end_seq = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
            index_png_end = data.find(png_end_seq, index_png_start)

            self.image_duplicate = False
            self.image_name = image_name
            if index_png_start != -1:
                if index_png_end != -1:
                    import PIL.Image as Image
                    import io

                    png_byte_array = data[index_png_start:index_png_end + len(png_end_seq)]
                    tmp_image = Image.open(io.BytesIO(png_byte_array)).convert("RGBA")
                    self.img_name = None

                    if self.platform == 'PSP':
                        # icon image PSP
                        if tmp_image.size == (144, 80):
                            self.img_name = 'ICON0.PNG'
                            if not self.has_icon0:
                                self.icon0_image = png_byte_array
                                self.has_icon0 = True

                        # this is background image PSP
                        elif tmp_image.size == (480, 272):
                            self.img_name = 'PIC1.PNG'
                            if not self.has_pic1:
                                self.pic1_image = png_byte_array
                                self.has_pic1 = True


                    elif self.platform == 'PS3':
                        # icon image PS3
                        if tmp_image.size == (320, 176):
                            self.img_name = 'ICON0.PNG'
                            if not self.has_icon0:
                                self.icon0_image = png_byte_array
                                self.has_icon0 = True


                        # when multiple pic0 we pic the first for English
                        elif tmp_image.size == (1000, 560):
                            self.img_name = 'PIC0.PNG'
                            if not self.has_pic0:
                                self.pic0_image = png_byte_array
                                self.has_pic0 = True


                        # this is background image PS3
                        elif tmp_image.size == (1920, 1080):
                            self.img_name = 'PIC1.PNG'
                            if not self.has_pic1:
                                self.pic1_image = png_byte_array
                                self.has_pic1 = True

                        # PIC2 is variant of the PIC0 for 4:3 screens
                        elif tmp_image.size == (310, 250):
                            self.img_name = 'PIC2.PNG'
                            if not self.has_pic2:
                                self.pic2_image = png_byte_array
                                self.has_pic2 = True

                    if self.img_name is not None:
                        # crop data for next iteration
                        self.data = data[index_png_end:len(data)-1]
                        return True

                return False

        while png_finder(self.data, self.image_name):
            print('DEBUG Found ' + self.img_name + ' for \'' + game_name + '\'')

        return self.icon0_image, self.pic0_image, self.pic1_image, self.pic2_image

    except Exception as e:
        print('ERROR: get_png_from_buffer - ' + e.message)
        return self.icon0_image, self.pic0_image, self.pic1_image, self.pic2_image


# TODO The sum of the sizes of SND0.AT3 + ICON1.PAM can't be larger than 2.4MB
def get_PAM_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data

    try:
        self.has_pam = False
        self.pam_image = None
        self.image_name = None
        self.pam_size = 0

        # these byte sequences are standard start and end of PNGs
        def PAM_finder(data, image_name, pam_size):

            index_pam_start = data.find(b'\x50\x41\x4D\x46\x30\x30\x34\x31')
            pam_stop_seq = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'

            self.image_name = image_name
            if index_pam_start > -1:
                # TODO: make more solid somehow?
                index_png_start = data.find(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', index_pam_start)

                # find the last occurrence of the stop sequence and use as eof
                index_pam_end = index_pam_start + data[index_pam_start:index_png_start].rfind(pam_stop_seq) + len(pam_stop_seq)
                if index_pam_end > -1:
                    tmp_image = data[index_pam_start:index_pam_end]
                    self.pam_size = len(tmp_image)

                    # PAM image PS3
                    if tmp_image is not None:
                        self.img_name = 'ICON1.PAM'
                        if not self.has_pam:
                            self.pam_image = tmp_image
                            self.has_pam = True

                    if self.img_name is not None:
                        # crop data for next iteration
                        self.data = data[index_pam_end:len(data)-1]
                        return True

                return False

        while PAM_finder(self.data, self.image_name, self.pam_size):
            # if int(self.pam_size) > 0:
            #     print('DEBUG ICON1.PAM size: ' + str(int(self.pam_size*0.978/1000)) + 'KB')
            if int(self.pam_size*0.978/1000) > 24000:
                print('''ERROR The size of ICON1.PAM can't be larger than 2.4MB.''')

            print('DEBUG Found ' + self.img_name + ' for \'' + game_name + '\'')

        return self.pam_image

    except Exception as e:
        print('ERROR: get_PAM_from_buffer - ' + e.message)
        return self.pam_image


# TODO The sum of the sizes of SND0.AT3 + ICON1.PAM can't be larger than 2.4MB
def get_AT3_from_buffer(self, platform, game_name, buffer_data):
    self.platform = platform
    self.data = buffer_data

    try:
        self.has_at3 = False
        self.at3_image = None
        self.image_name = None
        self.at3_size = 0
        # these byte sequences are standard start and end of PNGs
        def AT3_finder(data, image_name, file_size):
            index_at3_start = data.find(b'\x57\x41\x56\x45\x66\x6D\x74\x20') - 8
            at3_stop_seq = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

            self.image_name = image_name
            if index_at3_start > -1:
                # find the last occurrence of the stop sequence and use as eof
                index_at3_end = index_at3_start + data[index_at3_start:].find(at3_stop_seq)

                if index_at3_end > -1:
                    tmp_image = data[index_at3_start:index_at3_end]
                    self.at3_size = len(tmp_image)


                    # AT3 image PS3
                    if tmp_image is not None:
                        self.img_name = 'SND0.AT3'
                        if not self.has_at3:
                            self.at3_image = tmp_image
                            self.has_at3 = True

                    if self.img_name is not None:
                        # crop data for next iteration
                        self.data = data[index_at3_end:len(data)-1]
                        return True

                return False

        while AT3_finder(self.data, self.image_name, self.at3_size):
            # if int(self.at3_size) > 0:
            #      print('DEBUG SND0.AT3 size: ' + str(int(self.at3_size*0.978/1000)) + 'KB')
            if int(self.at3_size*0.978/1000) > 24000:
                print('''ERROR The size of SND0.AT3 can't be larger than 2.4MB.''')

            print('DEBUG Found ' + self.img_name + ' for \'' + game_name + '\'')
            break

        return self.at3_image

    except Exception as e:
        print('ERROR: get_AT3_from_buffer - ' + e.message)
        return self.at3_image

