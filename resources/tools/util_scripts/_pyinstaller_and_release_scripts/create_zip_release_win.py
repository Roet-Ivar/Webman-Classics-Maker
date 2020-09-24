import sys, os, zipfile
import application_path
from global_paths import Build as BuildPaths

# import pyinstaller_Build_Webman_PKG_exe
# import pyinstaller_Edit_Param_SFO_exe
# import pyinstaller_FTP_Game_List_exe
import pyinstaller_Webman_Classics_Maker_exe

def zipdir(path, ziph):
	# ziph is zipfile handle
	webman_classics_maker_exist = False
	webman_classic_exe = 'Webman_Classics_Maker.exe'

	# TODO: No more CHDIR plz!
	# files folders to exclude
	os.chdir(path)
	for root, dirs, files in os.walk('./'):

		# folders to exclude
		if '.git' in dirs:
			dirs.remove('.git')
		if '.idea' in dirs:
			dirs.remove('.idea')
		if 'release' in dirs:
			dirs.remove('release')
		if 'animations' in dirs:
			dirs.remove('animations')
		if 'pdn' in dirs:
			dirs.remove('pdn')
		if 'builds' in dirs:
			dirs.remove('builds')
		if 'icons' in dirs:
			dirs.remove('icons')
		if 'tv_frames' in dirs:
			dirs.remove('tv_frames')
		if 'work_dir' in dirs:
			dirs.remove('work_dir')
		if 'xmb_capture' in dirs:
			dirs.remove('xmb_capture')
		if 'burnout_3_example' in dirs:
			dirs.remove('burnout_3_example')
		if 'misc_scripts' in dirs:
			dirs.remove('misc_scripts')
		if 'data_merger' in dirs:
			dirs.remove('data_merger')
		if 'metadata_scraper' in dirs:
			dirs.remove('metadata_scraper')

		# Remove old webMan tools for a slimmer release
		if 'Param_SFO_Editor' in dirs:
			dirs.remove('Param_SFO_Editor')

		# files to exclude
		if '.gitignore' in files:
			files.remove('.gitignore')
		if 'game_list.txt' in files:
			files.remove('game_list.txt')
		if 'Webman-Classics-Maker.iml' in files:
			files.remove('Webman-Classics-Maker.iml')
		if 'Webman-Classics-Maker.iml' in files:
			files.remove('Webman-Classics-Maker.iml')
		if 'game_list_data.json' in files:
			files.remove('game_list_data.json')
		if 'ftp_settings.cfg' in files:
			files.remove('ftp_settings.cfg')


		# exclude old webMan tools for a slimmer release
		if 'Build_Webman_PKG.exe' in files:
			files.remove('Build_Webman_PKG.exe')
		if 'Edit_Param_SFO.exe' in files:
			files.remove('Edit_Param_SFO.exe')
		if 'FTP_Game_List.exe' in files:
			files.remove('FTP_Game_List.exe')

		for file in files:
			# add all files that aren't zip or pyc
			if file.endswith('.zip') is not True and file.endswith('.pyc') is not True:
				ziph.write(os.path.join(root, file))
			if file == webman_classic_exe:
				webman_classics_maker_exist = True

	if((webman_classics_maker_exist) == False):
		print("Warning: Couldn't find Webman_Classics_Maker.exe")
		print('Try rebuilding binaries using the included pyinstaller scripts.')
		sys.exit()

if __name__ == '__main__':

	# windows release
	zip_archive_name = 'webman_classics_maker_v2.0_win.zip'
	zip_dir_path = BuildPaths.zip_dir
	release_dir = BuildPaths.release

	if not os.path.exists(os.path.join(zip_dir_path, 'release')):
		os.makedirs(os.path.join(zip_dir_path, 'release'))

	zipf = zipfile.ZipFile(os.path.join(release_dir, zip_archive_name), 'w', zipfile.ZIP_DEFLATED)
	zipdir(zip_dir_path, zipf)
	zipf.close()

	print('The release archive has sucessfully been package and distributed to:\n' + '/release/' + zip_archive_name)
	try:
		# pause
		input = raw_input
	except NameError: pass
	input('\npress ENTER to continue...')
