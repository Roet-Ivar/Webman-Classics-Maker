# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, os, re
import xml.etree.ElementTree as Etree

platform = 'PSP'
with open(platform + '_all_title_ids.json') as f:
    json_data = json.load(f)
json_data_tmp = json_data

parser = Etree.XMLParser(encoding="utf-8")
xml_tree = Etree.parse(platform + '_LaunchBox.xml', parser=parser)
xml_root = xml_tree.getroot()

# title_id_element = Etree.parse('title_id_snippet.xml')
# xml_title_title_id_root    = title_id_element.getroot()

# id_element = Etree.Element('ID')
# xml_title_title_id_root.extend(id_element)
#
# xml_root.insert(1, xml_title_title_id_root)




s_chars = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
json_cnt = 0
json_max_cnt = 11452
xml_max_cnt = 2960
match_cnt = 0

non_migrated_games = {"games":[]}
if True:
    print('DEBUG progress:')

    for game in json_data['games']:
        match = False
        json_cnt +=1
        print('# ' + str(json_cnt) + ' of ' + str(json_max_cnt))

        if(platform == 'PS3'):
            for l in game['locale']:
                if 'EN' == l['lang']:
                    json_title = l['title']
        else:
            json_title = game['title']
        json_title_id = game['title_id']

        j_clean_title = json_title.lower()
        j_clean_title = j_clean_title.replace('the', ' ')
        j_clean_title = j_clean_title.replace('and', ' ')
        new_j_clean_title = ''.join(e for e in j_clean_title if e not in s_chars)

        xml_cnt = 0
        for x in xml_root.iter('Game'):
            xml_cnt +=1

            xml_title = x.find('Name').text
            x_clean_title = xml_title.lower()
            x_clean_title = x_clean_title.replace('the', ' ')
            x_clean_title = x_clean_title.replace('and', ' ')
            new_x_clean_title = ''.join(e for e in x_clean_title if e not in s_chars)

            # check if we got a match
            if new_j_clean_title == new_x_clean_title:
                match = True
                match_cnt +=1
                print('json_Title_id: ' + json_title_id + '\njson_Title: ' + json_title)

                title_id_element = Etree.Element('TitleID')
                title_id_element.set('id', game['title_id'])
                title_id_element.tail = "\n    "

                x.append(title_id_element)
                Etree.dump(x)

        # if game didn't match, add it to non-match list
        if not match:
            g_exist = False
            for g in non_migrated_games['games']:
                if g['title_id'] == game['title_id']:
                    g_exist = True

            if not g_exist:
                non_migrated_games['games'].append(game)

    with open(platform + '_not_migrated.json', "w") as newFile:
        json_text = json.dumps(non_migrated_games, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
        newFile.write(json_text)

    xml_tree.write(open(platform + '_migrated.xml', 'w'), encoding='utf-8')






