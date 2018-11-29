# ABOUT
A tool for PS3 that makes PKG shortcuts for ISO files using webMAN-mod through web commands.

Read more about webman web commands here:
http://www.psx-place.com/threads/webman-mod-web-commands.1508/

**BUILDS**
Get the latest build from releases:
https://github.com/Roet-Ivar/Webman-Classics-Maker/releases/

**TOOLS/BINARIES USED**

* SCETOOL 0.2.9 (scetool.exe):
https://github.com/naehrwert/scetool

* OpenSCETool (oscetool):
https://github.com/spacemanspiff/oscetool

* PSL1GHT PS3py (pkgcrypt)
https://github.com/HACKERCHANNEL/PSL1GHT/tree/master/tools/PS3Py

* PARAM_SFO_EDITOR (Aldos PS3 tool collection)
https://www.aldostools.org/

------------------------------------------------------------------------
# HOW TO USE

**(optional) FTP DUMP -> 'games_list.txt'**
	
	1. Check IP settings in webMan (holding [SELECT])
	2. Edit your /settings/ftp_settings.txt with your IP
	3. To get your "game_list.txt run "FTP_Game_List.exe", or "ftp_game_list.py" for linux
n
**EDIT PARAM.SFO**

	1. Run "Edit_param_sfo.exe" (Windows only right now, you can hex edit the "params.sfo" in linux)
	2. Fill in "Title ID"
	3. Fill in the field "TITLE"
	4. Drop down and fill in the field "FILE_PATH"

	NOTE: The filepath must be exact and it is case-sensitive!
	Bad path: /dev_HDD0/ps3ISO/Marvel Vs Capcom 3.iso
	Good path: /dev_hdd0/PS3ISO/Marvel Vs Capcom 3.iso

	5. Click "Save" to save your PARAM.SFO


**BUILD PKG -> game.pkg'**

	1. Run "Build_Webman_PKG.exe", or "build_all_scripts_linux.py" for linux
	2. Get your built package in the "builds"-folder
	3. Install the PKG on your PS3
	
---------------------------------------------------------------------------------------------------	
# TROUBLESHOOTING
	
* If you hear three rapid beeps you probably misspelled your path to the ISO, double check it!

* Sometimes at first boot the game hangs on blackscreen, reboot and start it again. This is mostly due to modifications of the same game w/o reboots.
	
---------------------------------------------------------------------------------------------------
# HOW TO BUILD THE TOOLS: Windows

1. Install python 2.7.x x86 + pyinstaller lib

2. Windows: Run the pyinstaller-scipts located in:
/Webman-Classics-Maker/resources/tools/util_scripts/_pyinstaller_and_release_scripts/

You now have a brand new **Build_Webman_PKG.exe** / **Edit_Param_SFO.exe** / **FTP_Game_List.exe** based on the changes you made in the scripts

# HOW TO BUILD THE TOOLS: Linux
1. There are nothing to build, only edit the .py scripts of your liking and run them
