import sys, os
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

class App:
    application_path = application_path
    # in application folder
    builds          = os.path.join(application_path, 'builds')
    release         = os.path.join(application_path, 'release')
    resources       = os.path.join(application_path, 'resources')
    settings        = os.path.join(application_path, 'settings')

    # in resources
    fonts           = os.path.join(resources, 'fonts')
    images          = os.path.join(resources, 'images')
    pkg             = os.path.join(resources, 'pkg')
    tools           = os.path.join(resources, 'tools')

    # in pkg
    USRDIR          = os.path.join(pkg, 'USRDIR')

    # in tools
    scetool         = os.path.join(tools, 'scetool')
    util_resources  = os.path.join(tools, 'util_resources')
    util_scripts    = os.path.join(tools, 'util_scripts')

    # in util_scripts
    games_metadata  = os.path.join(util_scripts, 'games_metadata')
    pkgcrypt        = os.path.join(util_scripts, 'pkgcrypt')
    wcm_gui         = os.path.join(util_scripts, 'wcm_gui')

    # in wcm_gui
    wcm_work_dir    = os.path.join(wcm_gui, 'work_dir')

    # variable game work dir
    game_work_dir   = ''

class Image:
    launchbox_base_image_url = 'https://gamesdb.launchbox-app.com/games/images/'
    images          = os.path.join(App.resources, 'images')
    # in images
    misc            = os.path.join(images, 'misc')
    pkg             = os.path.join(images, 'pkg')
    xmb             = os.path.join(images, 'xmb')

class Build:
    application_path = application_path
    zip_dir          = application_path
    release          = os.path.join(application_path, 'release')
    util_scripts     = App.util_scripts
    pyinstaller      = os.path.join(util_scripts, '_pyinstaller_and_release_scripts')

    Param_SFO_Editor = os.path.join(App.tools, 'Param_SFO_Editor')

class GlobalVar:
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

    file_extension_by_platform = [('PSP', ('.ISO','.NTFS[PSPISO]')),
                                  ('PSX', ('.ISO', '.BIN', '.MDF', '.NTFS[PSXISO]')),
                                  ('PS2', ('.ISO', '.BIN.ENC', '.NTFS[PS2ISO]')),
                                  ('PS3', ('.ISO','.NTFS[PS3ISO]')),
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


if not os.path.exists(os.path.join(App.wcm_work_dir, 'pkg')):
    os.makedirs(os.path.join(App.wcm_work_dir, 'pkg'))