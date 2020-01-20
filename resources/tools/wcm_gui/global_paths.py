import sys, os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"

        print('DEBUG Running mode:', running_mode)
        print('DEBUG Appliction path  :', application_path)

        if 'Non-interactive' in running_mode:
            application_path = os.path.join(application_path, '..', '..', '..')
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

class App:
    application_path= application_path
    # in application folder
    builds          = os.path.join(application_path, 'builds')
    release         = os.path.join(application_path, 'release')
    resources       = os.path.join(application_path, 'resources')
    settings        = os.path.join(application_path, 'settings')

    # in resources
    fonts           = os.path.join(resources, 'fonts')
    pkg             = os.path.join(resources, 'pkg')

    # in pkg
    USRDIR          = os.path.join(pkg, 'USRDIR')
    tools           = os.path.join(resources, 'tools')

    # in tools
    scetool         = os.path.join(tools, 'scetool')
    util_resources  = os.path.join(tools, 'util_resources')
    util_scripts    = os.path.join(tools, 'util_scripts')
    wcm_gui         = os.path.join(tools, 'wcm_gui')

    # in wcm_gui
    wcm_work_dir    = os.path.join(wcm_gui, 'work_dir')

    # in util_scripts
    games_metadata  = os.path.join(util_scripts, 'games_metadata')
    pkgcrypt        = os.path.join(util_scripts, 'pkgcrypt')

class Image:
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

    Param_SFO_Editor = os.path.join(application_path, 'Param_SFO_Editor')


