import os

from param_sfo_to_json import Param_to_json
from content_id_elf_replace import Elf_replace
from resign_eboot import Resign_eboot
from edit_launch_txt import Edit_launch_txt
from webman_pkg import Webman_pkg

current_path= os.getcwd()
# print('current_path: ' + current_path)
if 'util_scripts' not in os.getcwd():
	os.chdir('./resources/tools/util_scripts/')
	
# print('__file__:' + __file__)
# print('real path:' + os.path.dirname(os.path.realpath(__file__)))

param_sfo_to_json = Param_to_json()
param_sfo_to_json.execute()

content_id_elf_replace = Elf_replace()
content_id_elf_replace.execute()

edit_launch_txt = Edit_launch_txt()
edit_launch_txt.execute()

resign_eboot = Resign_eboot()
resign_eboot.execute()

webman_pkg = Webman_pkg()
webman_pkg.execute()

# os.system("pause")