import os
import json
import subprocess
from shutil import copyfile

class Resign_eboot:
	def execute(self):
		with open('../util_generated_files/params.json') as f:
			json_data = json.load(f)
			
		content_id = json_data['content_id']

		os.chdir(os.path.pardir)
		os.chdir("resigner_tool")

		args1 = 'EBOOT.ELF 24 13 BC C5 F6 00 33 00 00 00 36 24 13 BC C5 F6 00 33 00 00 00 34 /340'
		p1 = subprocess.call('./FixELF.exe' + ' ' + args1)

		args2 = '-v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=%CID% --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN'
		p2 = subprocess.call('./scetool.exe' + ' ' + args2)

		copyfile('./EBOOT.BIN', './../../pkg/USRDIR/EBOOT.BIN')
		
		os.chdir(os.path.pardir)
		os.chdir('util_scripts')
		
		print('Execution of \'resign_eboot.py\': Done')