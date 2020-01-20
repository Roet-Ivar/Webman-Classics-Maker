import os, subprocess
from global_paths import App as AppPaths
from global_paths import Build as BuildPaths

app = os.path.join(BuildPaths.Param_SFO_Editor, 'PARAM.SFO.Editor.exe')
args = os.path.join(AppPaths.pkg, 'PARAM.SFO')

p = subprocess.call(app + ' ' + args)

