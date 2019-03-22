from write_json_to_param_sfo import Write_param_sfo
from content_id_elf_replace import Elf_replace
from resign_eboot import Resign_eboot
from edit_launch_txt import Edit_launch_txt
from webman_pkg import Webman_pkg

class WebmanClassicsBuilder:
	def make_webman_pkg(self):
		write_json_to_param_sfo = Write_param_sfo()
		write_json_to_param_sfo.execute()

		content_id_elf_replace = Elf_replace()
		content_id_elf_replace.execute()

		edit_launch_txt = Edit_launch_txt()
		edit_launch_txt.execute()

		resign_eboot = Resign_eboot()
		resign_eboot.execute()

		webman_pkg = Webman_pkg()

		try:
			pkg_name = webman_pkg.execute()
			return pkg_name
		except:
			print('Error: could not return pkg_name.')


		# os.system("pause")