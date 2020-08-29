
import application_path
import global_paths

import os, sys, json
from shutil import copyfile
import urllib
import ConfigParser
import glob


import param_sfo_to_json
import build_all_scripts

param_to_json = param_sfo_to_json.Param_to_json()
param_to_json.execute()

webmanpkg = build_all_scripts.Webman_PKG()
pkg_name = webmanpkg.build()