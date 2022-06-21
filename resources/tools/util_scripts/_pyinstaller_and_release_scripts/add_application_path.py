import os
import sys

if getattr(sys, 'frozen', False):
    add_application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'

    if 'resources' == os.path.basename(add_application_path):
        add_application_path = os.path.join(add_application_path, '..')

else:
    try:
        app_full_path = os.path.realpath(__file__)
        add_application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive"

        if 'wcm_gui' == os.path.basename(add_application_path):
            add_application_path = os.path.join(add_application_path, '..', '..', '..', '..')
        elif 'resources' == os.path.basename(add_application_path):
            add_application_path = os.path.join(add_application_path, '..')
        elif '_pyinstaller_and_release_scripts' == os.path.basename(add_application_path):
            add_application_path = os.path.join(add_application_path, '..', '..', '..', '..')

    except NameError:
        add_application_path = os.getcwd()
        running_mode = 'Interactive'

# adds path to util_scripts in order to have access to the global_paths
sys.path.append(os.path.join(add_application_path, 'resources', 'tools', 'util_scripts'))
