import sys
import os
import zipfile
import pyinstaller_Build_Webman_PKG_exe
import pyinstaller_Edit_Param_SFO_exe
import pyinstaller_FTP_Game_List_exe

def zipdir(path, ziph):
    # ziph is zipfile handle
	build_webman_pkg_exe_exist = False
	edit_param_sfo_exist = False
	ftp_game_list_exist = False
	
	webman_exe = 'Build_Webman_PKG.exe'
	param_exe = 'Edit_Param_SFO.exe'
	ftp_list_exe = 'FTP_Game_List.exe'
		
	for root, dirs, files in os.walk(path):
		if '.git' in dirs:
			dirs.remove('.git')
		if 'release' in dirs:
			dirs.remove('release')
		if 'builds' in dirs:
			dirs.remove('builds')
		if 'game_list.txt' in files:
			files.remove('game_list.txt')
		
		for file in files:
			if file.endswith('.zip') is not True and file.endswith('.pyc') is not True:
				ziph.write(os.path.join(root, file))
			if file ==  webman_exe:
				build_webman_pkg_exe_exist = True
			if file ==  param_exe:
				edit_param_sfo_exist = True
			if file ==  ftp_list_exe:
				ftp_game_list_exist = True	
				
	if((build_webman_pkg_exe_exist and edit_param_sfo_exist and ftp_game_list_exist) == False):
		print('Warning: Cannot find all binaries: ' + webman_exe + ', ' + ftp_list_exe + ' and/or ' + param_exe)
		print('Rebuild binaries using the pyinstaller scripts.')
		sys.exit()
		
if __name__ == '__main__':
	zip_dir_path = './../../../../'
	zip_archive_name = 'webman_classics_maker.zip'
	release_dir = zip_dir_path + '/release/'
	
	if not os.path.exists(zip_dir_path + 'release'):
		os.makedirs(zip_dir_path + 'release')

	zipf = zipfile.ZipFile(release_dir + zip_archive_name, 'w', zipfile.ZIP_DEFLATED)
	zipdir(zip_dir_path, zipf)
	zipf.close()
	
	print('The release archive has sucessfully been package and distributed to:\n' + '/release/' + zip_archive_name)
	os.system("pause")