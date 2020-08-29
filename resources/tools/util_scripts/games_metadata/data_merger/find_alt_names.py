# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, re
import xml.etree.ElementTree as Etree

platform = 'PSP'
# with open(platform + '_not_migrated.json') as f:

parser = Etree.XMLParser(encoding="utf-8")

platform_tree = Etree.parse(platform + '_LaunchBox_Alt.xml', parser=parser)
platform_root = platform_tree.getroot()

alt_name_tree = Etree.parse('game_alternate_name.xml')
alt_name_root = alt_name_tree.getroot()
alt_name_root.tail = "\n    "


# PlatformAlternateName -> Name == 'Sony '.join(platform)
# GameImage -> DatabaseID == DatabaseID of platform_xml
# GameAlternateName -> DatabaseID == DatabaseID of platform_xml

# this loop finds alt names
if True:
    for x in platform_root.iter('Game'):
        platform_database_id = x.find('DatabaseID').text

        for y in alt_name_root.iter('GameAlternateName'):
            alt_name_database_id = y.find('DatabaseID').text

            if platform_database_id == alt_name_database_id:
                print('\n')
                print('ALT_NAME -> id: ' + platform_database_id + ', name: '  + x.find('Name').text)
                # alt_xml_element = Etree.tostring(y, encoding='utf8', method='xml').replace("""<?xml version='1.0' encoding='utf8'?>""", "").strip()
                # print(alt_xml_element)

                platform_root.append(y)
    # platform_tree.write(open('alt_' + platform + '_LaunchBox.xml', 'w'), encoding='utf-8')

# this loop finds image names
if False:
    for x in platform_root.iter('Game'):
        platform_database_id = x.find('DatabaseID').text

        for z in alt_name_root.iter('GameImage'):
            image_database_id = z.find('DatabaseID').text

            if platform_database_id == image_database_id:

                print('\n')
                print('IMAGE -> id: ' + platform_database_id + ', name: '  + z.find('FileName').text)
                platform_root.append(z)
platform_tree.write(open('alt_' + platform + '_LaunchBox.xml', 'w'), encoding='utf-8')






