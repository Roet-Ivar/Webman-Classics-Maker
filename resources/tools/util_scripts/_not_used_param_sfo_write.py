import os
import json
import re

with open('../util_generated_files/params.json') as f:
    json = json.load(f)

title = json['title']
title_id = json['title_id']
content_id = json['content_id']

tmp_title_array = b'\x00'*128
title = str(title) + tmp_title_array[len(title):]

tmp_title='PKG/ROM Launcher'
tmp_title_id='PKGLAUNCH'


# load it
with open("../util_resources/PARAM.SFO.BAK", 'rb') as f:
	file = f.read()
	f.close()
	
	try:
	
		# print(file.find(tmp_title))
	
		# print(file[888:1025])
		
		file=file[0:888]+str(title)+file[888+len(str(title)):]
		file=file[0:1025-len(str(title_id))]+str(title_id)+file[1025:]
		
		# print(file[888:1025])
		
		# write it
		newFile = open("../util_generated_files/PARAM.SFO", "wb")
		newFileByteArray = bytearray(file)
		newFile.write(newFileByteArray)
	
	except ValueError:
		print('File write error/PKGLAUNCH not found/titel_id not a string')