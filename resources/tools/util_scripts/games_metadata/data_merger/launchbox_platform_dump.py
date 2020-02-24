# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip

import xml.etree.ElementTree as Etree

# with open(os.path.join('ps2_all_games_list.json')) as f:
#     json_data = json.load(f)
# json_data_tmp = json_data

parser = Etree.XMLParser(encoding="utf-8")
xml_tree = Etree.parse('C:/Users/nicla/Downloads/launchboxMetadata/Metadata.xml')
xml_root = xml_tree.getroot()

xml_psp = Etree.parse('PSP.xml')
xml_psp_root = xml_psp.getroot()
xml_psx = Etree.parse('PSX.xml')
xml_psx_root = xml_psx.getroot()
xml_ps2 = Etree.parse('PS2.xml')
xml_ps2_root = xml_ps2.getroot()
xml_ps3 = Etree.parse('PS3.xml')
xml_ps3_root = xml_ps3.getroot()


xml_cnt = 0
for x in xml_root.findall('Game'):
    platform_name = x.find('Platform').text

    if platform_name == 'Sony PSP':
        xml_psp_root.append(x)
        print('added a ' + platform_name + ' game: ')
        print(x.find('Name').text)

    elif platform_name == 'Sony Playstation':
        xml_psx_root.append(x)
        print('added a ' + platform_name + ' game: ')
        print(x.find('Name').text)

    elif platform_name == 'Sony Playstation 2':
        xml_ps2_root.append(x)
        print('added a ' + platform_name + ' game: ')
        print(x.find('Name').text)

    elif platform_name == 'Sony Playstation 3':
        xml_ps3_root.append(x)
        print('added a ' + platform_name + ' game: ')
        print(x.find('Name').text)

xml_psp.write(open('psp.xml', 'w'), encoding='utf-8')
xml_psx.write(open('psx.xml', 'w'), encoding='utf-8')
xml_ps2.write(open('ps2.xml', 'w'), encoding='utf-8')
xml_ps3.write(open('ps3.xml', 'w'), encoding='utf-8')