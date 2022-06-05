import json
import os
import shutil
import subprocess
import sys

from resources.tools.util_scripts.global_paths import GlobalVar
from resources.tools.util_scripts.global_paths import AppPaths

class Webman_pkg:
    def execute(self):

        with open(os.path.join(AppPaths.game_work_dir, 'pkg.json')) as f:
            json_data = json.load(f)

        content_id = str(json_data['content_id'])
        title_id = str(json_data['title_id'])
        filepath = str(json_data['path'])
        filename = str(json_data['filename'])

        pkg_dir_path = os.path.join(AppPaths.game_work_dir, 'pkg') + '/'
        tmp_filename = filename
        # removes the file extension from tmp_filename
        for file_ext in GlobalVar.file_extensions:
            if tmp_filename.upper().endswith(file_ext):
                tmp_filename = tmp_filename[0:len(tmp_filename)-len(file_ext)]
                break
        pkg_name = tmp_filename.replace(' ', '_') + '_(' + title_id.replace('-', '') + ')' + '.pkg'
        build_dir_path = os.path.join(AppPaths.game_work_dir, '..')

        print('DEBUG pkg_name: ' + pkg_name)
        if os.path.isdir(build_dir_path):
            print('DEBUG pkg_dir_path: ' + pkg_dir_path + ' is a path')
        if os.path.isdir(build_dir_path):
            print('DEBUG build_dir_path: ' + build_dir_path + ' is a path')

        print('Create PKG')
        subprocess.call(['python3', 'resources/tools/ps3py/pkg.py', '-c', content_id, pkg_dir_path, pkg_name])

        if os.path.isdir(build_dir_path) and os.path.isfile(pkg_name):
            if os.path.isfile(os.path.join(build_dir_path, pkg_name)):
                os.remove(os.path.join(build_dir_path, pkg_name))
            shutil.move(pkg_name, build_dir_path)

            print('[5/5] Execution of \'webman_pkg.py\':              DONE')
            print('-----------------------------------------------------')
            print('Package created in: ' + build_dir_path + '/' + pkg_name + '\n')
            return pkg_name

        else:
            print('[5/5] Execution of \'webman_pkg.py\':              FAILED')
            print('-----------------------------------------------------')
            raise Exception('pkg_name: ' + pkg_name +
                        ',\nbuild_dir_path: ' + build_dir_path +
                        ',\njson_data[\'path\']: ' + filepath)
            usage()
            sys.exit(2)
