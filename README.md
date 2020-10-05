
![Alt text](https://i.imgur.com/AHBXvnK.png "Optional title")
# ABOUT
Webman Classics Maker is tool for the PS3 that makes PKG shortcuts for ISO files straight to the home menu. It is using web commands  through webMAN-mod to mount and launch the ISOs automatically:
http://www.psx-place.com/threads/webman-mod-web-commands.1508/

This software is under GPLv2 license: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html, not to be confused with the GPLv3 license.

# BUILDS
Get the latest build from releases:
https://github.com/Roet-Ivar/Webman-Classics-Maker/releases/

# TOOLS/BINARIES USED

* SCETOOL 0.2.9 (scetool.exe):
https://github.com/naehrwert/scetool

* OpenSCETool (oscetool):
https://github.com/spacemanspiff/oscetool

* PSL1GHT PS3py (pkgcrypt)
https://github.com/HACKERCHANNEL/PSL1GHT/tree/master/tools/PS3Py

* PARAM_SFO_EDITOR (Aldos PS3 tool collection)
https://www.aldostools.org/


**Credits goes to all of you guys!**

------------------------------------------------------------------------
# HOW TO USE
1. Dump your disc-based games (multiman is great for this)
2. Make sure webMan-mod from aldostools is installed
3. Start Webman Classics Maker application
4. Fetch games-list over FTP
5. Build PKG forwarder for the game you like
6. Install PKG on PS3 and enjoy disc-images straight from XMB	
---------------------------------------------------------------------------------------------------	
# TROUBLESHOOTING
	
* If you hear three rapid beeps: Probably misspelled path to the ISO, double check it (case sensitive)!
* Games only mounts but doesn't automatically start: the timings on the webcommand are not enough for
your HDD read speeds, see the forum thread for mor info!  	
---------------------------------------------------------------------------------------------------

# Windows dev environment setup 

* install python2.7.xx x86_64 (https://www.python.org/downloads/release/python-2715/)
* pip install pillow (often bundled in the windows version)
* pip install pyinstaller

**Building the executable**

* Run the pyinstaller-scipts located in:
/Webman-Classics-Maker/resources/tools/util_scripts/_pyinstaller_and_release_scripts/
* Run your new **webman-classics-maker.exe** based on your new changes


# Linux dev environment setup

* sudo apt-get update
* sudo apt-get install python2.7
* sudo apt-get install python-tk
* sudo apt-get install python-pip
* pip install pillow
* pip install pyinstaller

**Building executables**

Right now you can't build any executables for linux

