from write_json_to_param_sfo import Write_param_sfo
from content_id_elf_replace import Elf_replace
from resign_eboot import Resign_eboot
from edit_launch_txt import Edit_launch_txt
from webman_pkg import Webman_pkg

from global_paths import App as AppPaths

class Webman_PKG:
	def build(self):
		try:
			write_json_to_param_sfo = Write_param_sfo()
			write_json_to_param_sfo.execute()

			content_id_elf_replace = Elf_replace()
			content_id_elf_replace.execute()

			edit_launch_txt = Edit_launch_txt()
			edit_launch_txt.execute()

			resign_eboot = Resign_eboot()
			resign_eboot.execute()

			webman_pkg = Webman_pkg()
			pkg_name = webman_pkg.execute()
		except Exception as e:
			print('Could not build and/or pkg_name!\nError: ' + e.message)

		# clean up .pyc-files
		import os
		util_scripts = AppPaths.util_scripts
		util_scripts_items = os.listdir(util_scripts)
		for item in util_scripts_items:
			if item.endswith(".pyc"):
				os.remove(os.path.join(util_scripts, item))

		wcm_gui = AppPaths.wcm_gui
		wcm_gui_items = os.listdir(wcm_gui)
		for item in wcm_gui_items:
			if item.endswith(".pyc"):
				os.remove(os.path.join(wcm_gui, item))

		return pkg_name