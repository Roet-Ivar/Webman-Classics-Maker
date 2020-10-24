from write_json_to_param_sfo import Write_param_sfo
from content_id_elf_replace import Elf_replace
from edit_launch_txt import Edit_launch_txt
from resign_eboot import Resign_eboot
from webman_pkg import Webman_pkg

from global_paths import App as AppPaths

class Webman_PKG:
	def build(self):
		pkg_name = None
		write_json_to_param_sfo = Write_param_sfo()
		content_id_elf_replace = Elf_replace()
		edit_launch_txt = Edit_launch_txt()
		resign_eboot = Resign_eboot()
		webman_pkg = Webman_pkg()

		build_is_ok = True
		while True:
			if not write_json_to_param_sfo.execute():
				build_is_ok = False
				break
			if not content_id_elf_replace.execute():
				build_is_ok = False
				break
			if not edit_launch_txt.execute():
				build_is_ok = False
				break
			if not resign_eboot.execute():
				build_is_ok = False
				break
			break

		try:
			if build_is_ok:
				pkg_name = webman_pkg.execute()
		except Exception as e:
			print('Could not build pkg and/or return pkg_name!')
			if e.message:
				print('ERROR: ' + e.message)

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