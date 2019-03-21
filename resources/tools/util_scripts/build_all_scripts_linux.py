import os

from write_json_to_param_sfo import Write_param_sfo
from content_id_elf_replace import Elf_replace
from resign_eboot_linux import Resign_eboot
from edit_launch_txt import Edit_launch_txt
from webman_pkg import Webman_pkg

current_path= os.getcwd()
# print('current_path: ' + current_path)
if 'util_scripts' not in os.getcwd():
	os.chdir('./resources/tools/util_scripts/')

write_json_to_param_sfo = Write_param_sfo()
write_json_to_param_sfo.execute()

content_id_elf_replace = Elf_replace()
content_id_elf_replace.execute()

edit_launch_txt = Edit_launch_txt()
edit_launch_txt.execute()

resign_eboot = Resign_eboot()
resign_eboot.execute()

webman_pkg = Webman_pkg()
webman_pkg.execute()

raw_input('press ENTER to continue...')