import sys
import os
import json
from shutil import copyfile

if getattr(sys, 'frozen', False):
    application_path = os.path.join(os.path.dirname(sys.executable))
    running_mode = 'Frozen/executable'

    if 'resources' == os.path.basename(application_path):
        application_path = os.path.join(application_path, '..')

    if 'wcm_gui' == os.path.basename(application_path):
        application_path = os.path.join(application_path, '..', '..', '..', '..')
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"

        if 'Non-interactive' in running_mode:
            application_path = os.path.join(application_path, '..', '..', '..')

    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'


class AppPaths:
    game_work_dir = ''
    game_pkg_dir = os.path.join(game_work_dir, 'pkg')
    application_path = application_path
    # in application folder
    builds = os.path.join(application_path, 'builds')
    release = os.path.join(application_path, 'release')
    resources = os.path.join(application_path, 'resources')
    settings = os.path.join(application_path, 'settings')
    tmp_work_dir = os.path.join(application_path, 'work_dir')
    tmp_pkg_dir = os.path.join(tmp_work_dir, 'pkg')

    # in resources
    fonts = os.path.join(resources, 'fonts')
    images = os.path.join(resources, 'images')
    tools = os.path.join(resources, 'tools')

    # in tmp_pkg_dir
    USRDIR = os.path.join(tmp_pkg_dir, 'USRDIR')

    # in tools
    scetool = os.path.join(tools, 'scetool')
    util_resources = os.path.join(tools, 'util_resources')
    util_scripts = os.path.join(tools, 'util_scripts')
    ps3py = os.path.join(tools, 'ps3py')

    # in util_scripts
    games_metadata = os.path.join(util_scripts, 'games_metadata')
    pkgcrypt = os.path.join(util_scripts, 'pkgcrypt')
    wcm_gui = os.path.join(util_scripts, 'wcm_gui')
    build_scripts = os.path.join(util_scripts, '_pyinstaller_and_release_scripts')

    # variable game work dir
    def get_game_build_dir(self, title_id, filename):
        title_id = str(title_id or '')
        filename = str(filename or '')

        if title_id != '' and title_id != '':
            tmp_filename = filename
            # removes the file extension from tmp_filename
            for file_ext in GlobalVar.file_extensions:
                if filename.upper().endswith(file_ext):
                    tmp_filename = filename[0:len(filename) - len(file_ext)]
                    break
            game_folder_name = tmp_filename.replace(' ', '_') + '_(' + title_id.replace('-', '') + ')'
            game_build_dir = os.path.join(AppPaths.builds, game_folder_name)
            return game_build_dir
        else:
            return None


class ImagePaths:
    images = os.path.join(AppPaths.resources, 'images')
    # in images
    misc = os.path.join(images, 'misc')
    pkg = os.path.join(images, 'pkg')
    xmb = os.path.join(images, 'xmb')


class MetadataPaths:
    launchbox_base_image_url = 'https://gamesdb.launchbox-app.com/games/images/'


class BuildPaths:
    application_path = application_path
    zip_dir = application_path
    release = os.path.join(application_path, 'release')
    util_scripts = AppPaths.util_scripts
    pyinstaller = os.path.join(util_scripts, '_pyinstaller_and_release_scripts')

    Param_SFO_Editor = os.path.join(AppPaths.tools, 'Param_SFO_Editor')


class FtpSettings:
    # ftp settings
    import json
    import shutil

    ftp_settings_path = os.path.join(AppPaths.settings, 'ftp_settings.cfg')
    if not os.path.isdir(AppPaths.settings):
        os.mkdir(AppPaths.settings)
        if os.path.isfile(os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK')):
            shutil.copyfile(os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK'), ftp_settings_path)
        else:
            print('Error: ' + os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK') + ' could not be find.')
    with open(ftp_settings_path) as f:
        ftp_settings_file = json.load(f)
        f.close()

    # some PSP-images is found around 20MB into the ISO
    ps3_lan_ip = ftp_settings_file['ps3_lan_ip']
    ftp_timeout = ftp_settings_file['ftp_timeout']
    ftp_pasv_mode = ftp_settings_file['ftp_pasv_mode']
    ftp_user = ftp_settings_file['ftp_user']
    ftp_password = ftp_settings_file['ftp_password']
    ftp_chunk_size_kb = ftp_settings_file['ftp_chunk_size_kb']
    ftp_folder_depth = ftp_settings_file['ftp_folder_depth']
    ftp_psp_png_offset_kb = ftp_settings_file['ftp_psp_png_offset_kb']
    use_w_title_id = ftp_settings_file['use_w_title_id']
    legacy_webcommand = ftp_settings_file['legacy_webcommand']
    ftp_retry_count = ftp_settings_file['ftp_retry_count']
    webcommand = ftp_settings_file['webcommand']

    def get_ftp(self):
        from ftplib import FTP
        print('Connection attempt to ' + self.ps3_lan_ip + ', timeout set to ' + str(self.ftp_timeout) + 's...\n')
        ftp = FTP(self.ps3_lan_ip, timeout=self.ftp_timeout, encoding='ISO-8859-1')
        ftp.set_pasv = self.ftp_pasv_mode
        ftp.login(user='', passwd='')
        ftp.voidcmd('TYPE I')
        return ftp


class GameListData:
    def __init__(self):
        self.game_list_data_json = None
        self.game_list_data_bak_json = None

        # open a copy of the current gamelist from disk
        try:
            with open(os.path.join(AppPaths.application_path, 'game_list_data.json'), encoding="utf8") as f1:
                self.game_list_data_json = json.load(f1)
            with open(os.path.join(AppPaths.util_resources, 'game_list_data.json.BAK'), encoding="utf8") as f2:
                self.game_list_data_bak_json = json.load(f2)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))

    def get_game_list_data_json(self):
        return self.game_list_data_json

    def get_game_list_data_json_bak(self):
        return self.game_list_data_bak_json

    def get_game_list_from_disk(self):
        import json
        import shutil
        # makes sure there is a json_game_list file
        GAME_LIST_DATA_PATH = os.path.join(AppPaths.application_path, 'game_list_data.json')
        GAME_LIST_DATA_BAK_PATH = os.path.join(AppPaths.util_resources, 'game_list_data.json.BAK')

        if not os.path.isfile(GAME_LIST_DATA_PATH):
            shutil.copyfile(GAME_LIST_DATA_BAK_PATH, GAME_LIST_DATA_PATH)

        try:
            with open(GAME_LIST_DATA_PATH) as f:
                self.game_list_data_json = json.load(f)
        except Exception as e:
            print(
                """Error in 'game_list_data.json' contains incorrect json-syntax. Either remove it or find the error using json lint""")
            print("Details: " + getattr(e, 'message', repr(e)))
        return self.game_list_data_json


class GlobalVar:
    coding = 'ISO-8859-1'
    file_extensions = ('.BIN',
                       '.BIN.ENC',
                       '.MDF',
                       '.NTFS[PSXISO]',
                       '.NTFS[PSPISO]',
                       '.NTFS[PS2ISO]',
                       '.NTFS[PS3ISO]',
                       '.IMG',
                       '.ISO',
                       '.ISO.0'
                       )
    # ,
    # '.NTFS[BDISO]',
    # '.NTFS[DVDISO]',
    # '.NTFS[BDFILE]',)

    platform_by_file_extension = [('.BIN', ('PSX')),
                                  ('.BIN.ENC', ('PS2')),
                                  ('.MDF', ('PSX')),
                                  ('.NTFS[PSXISO]', ('NTFS', 'PSX')),
                                  ('.NTFS[PSPISO]', ('NTFS', 'PSP')),
                                  ('.NTFS[PS2ISO]', ('NTFS', 'PS2')),
                                  ('.NTFS[PS3ISO]', ('NTFS', 'PS3')),
                                  ('.NTFS[BDISO]', ('NTFS', 'MOVIE')),
                                  ('.NTFS[DVDISO]', ('NTFS', 'MOVIE')),
                                  ('.NTFS[BDFILE]', ('NTFS', 'MOVIE')),
                                  ('.IMG', ('')),
                                  ('.ISO', ('PSP', 'PSX', 'PS2', 'PS3')),
                                  ('.ISO.0', (''))]

    file_extension_by_platform = [('PSP', ('.ISO', '.NTFS[PSPISO]')),
                                  ('PSX', ('.ISO', '.BIN', '.MDF', '.NTFS[PSXISO]')),
                                  ('PS2', ('.ISO', '.BIN.ENC', '.NTFS[PS2ISO]')),
                                  ('PS3', ('.ISO', '.NTFS[PS3ISO]')),
                                  ('NTFS', ('.NTFS[PSXISO]',
                                            '.NTFS[PSPISO]',
                                            '.NTFS[PS2ISO]',
                                            '.NTFS[PS3ISO]',
                                            '.NTFS[BDISO]',
                                            '.NTFS[DVDISO]',
                                            '.NTFS[BDFILE]'))]

    drive_paths = [('/dev_hdd0/', 'HDD0'),
                   ('/dev_usb000/', 'USB000'),
                   ('/dev_usb001/', 'USB001'),
                   ('/dev_usb002/', 'USB002'),
                   ('/dev_usb003/', 'USB003'),
                   ('/dev_usb(*)/', 'USB(*)')]

    platform_paths = [('PSPISO/', 'PSPISO'),
                      ('PSXISO/', 'PSXISO'),
                      ('PS2ISO/', 'PS2ISO'),
                      ('PS3ISO/', 'PS3ISO'),
                      ('tmp/wmtmp/', 'NTFS'),
                      ('GAMES/', 'GAMES')]


class GlobalDef:
    def copytree(self, src, dst, symlinks=False, ignore=None):
        import shutil
        if not os.path.exists(dst):
            os.makedirs(dst)
            shutil.copystat(src, dst)
        lst = os.listdir(src)
        if ignore:
            excl = ignore(src, lst)
            lst = [x for x in lst if x not in excl]
        for item in lst:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if symlinks and os.path.islink(s):
                if os.path.lexists(d):
                    os.remove(d)
                os.symlink(os.readlink(s), d)
                try:
                    st = os.lstat(s)
                    mode = stat.S_IMODE(st.st_mode)
                    os.lchmod(d, mode)
                except:
                    pass  # lchmod not available
            elif os.path.isdir(s):
                self.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)


if not os.path.exists(AppPaths.tmp_pkg_dir):
    os.makedirs(AppPaths.tmp_pkg_dir)
