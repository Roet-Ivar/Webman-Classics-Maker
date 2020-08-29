import os, subprocess
from shutil import copyfile

import application_path
from global_paths import App as AppPaths
from global_paths import Build as BuildPaths

copyfile(os.path.join(AppPaths.util_resources, 'PARAM.SFO_MOD.BAK'), os.path.join(AppPaths.pkg, 'PARAM.SFO'))

app = os.path.join(BuildPaths.Param_SFO_Editor, 'PARAM.SFO.Editor.exe')
args = os.path.join(AppPaths.pkg, 'PARAM.SFO')

p = subprocess.call(app + ' ' + args)

