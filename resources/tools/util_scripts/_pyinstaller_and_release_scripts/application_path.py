import sys, os
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'

    if 'resources' == os.path.basename(application_path):
        application_path = os.path.join(application_path, '..')

else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive"

        if 'wcm_gui' == os.path.basename(application_path):
            application_path = os.path.join(application_path, '..', '..', '..', '..')
        elif 'resources' == os.path.basename(application_path):
            application_path = os.path.join(application_path, '..')
        elif '_pyinstaller_and_release_scripts' == os.path.basename(application_path):
            application_path = os.path.join(application_path, '..', '..', '..', '..')

    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

    # adds util_scripts in order to have access to the global_paths
sys.path.append(os.path.join(application_path, 'resources', 'tools', 'util_scripts'))