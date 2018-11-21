import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
	build_webman_pkg_exe_exist = False
	edit_param_sfo_exist = False
	webman_exe = 'Build_Webman_PKG.exe'
	param_exe = 'Edit_Param_SFO.exe'
		
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(".zip") is not True:
				ziph.write(os.path.join(root, file))
			if file ==  webman_exe:
				build_webman_pkg_exe_exist = True
			if file ==  param_exe:
				edit_param_sfo_exist = True
	if((build_webman_pkg_exe_exist and edit_param_sfo_exist) == False):
		print('Warning: Cannot find the binaries: ' + webman_exe + ' and/or ' + param_exe)
		print('Tip: Rebuild binaries using the pyinstaller scripts.')
		exit()
		
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