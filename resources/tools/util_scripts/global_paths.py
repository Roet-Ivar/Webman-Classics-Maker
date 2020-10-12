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
    file_extensions = ('.BIN', '.BIN.ENC', '.MDF', '.NTFS', '.IMG', '.ISO', '.ISO.0')

if not os.path.exists(os.path.join(App.wcm_work_dir, 'pkg')):
    os.makedirs(os.path.join(App.wcm_work_dir, 'pkg'))