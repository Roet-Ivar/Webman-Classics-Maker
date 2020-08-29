# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, re
import xml.etree.ElementTree as Etree

platform = 'PSP'
# with open(platform + '_not_migrated.json') as f:
with open('psp_all_games_list.json') as f: # 6896
    json_data = json.load(f)
json_data_tmp = json_data

parser = Etree.XMLParser(encoding="utf-8")
xml_tree = Etree.parse(platform + '_LaunchBox.xml', parser=parser)
xml_root = xml_tree.getroot()

def str_pre_process(name_str):
    pattern = re.compile("""[a-z\d\s]""")
    words_list = re.findall(pattern, name_str.lower())

    return "".join(words_list)

def get_signicant_numeral(str_title):
    pattern = re.compile("""\d+""")
    numeral_list = re.findall(pattern, str_title)

    # compare the only number
    if len(numeral_list) < 1:
        return None


    elif len(numeral_list[0]) == 1:
        return numeral_list[0]

    # compare the first number that is not 0
    elif len(numeral_list[0]) > 1:
        for n in numeral_list:
            if int(n) > 0:
                return n
    else:
        return None



non_migrated_games = {"games":[]}
if True:
    print('DEBUG progress:')
    json_max_cnt = 6896
    xml_max_count = 1682

    match_cnt = 0
    non_match_cnt = 0
    potential_match_cnt = 0

    xml_cnt = 0
    for x in xml_root.iter('Game'):
        xml_cnt +=1
        xml_title = x.find('Name').text

        json_cnt = 0
        for game in json_data['games']:
            json_cnt +=1
            match = False

            if(platform == 'PS3'):
                for l in game['locale']:
                    if 'EN' == l['lang']:
                        json_title = l['title']
            else:
                json_title = game['title']
            json_title_id = game['title_id']

        json_cnt = 0
        for game in json_data['games']:
            json_cnt +=1
            match = False

            # rule 1: title must have more than one word (this need to handled later)
            if ' ' in json_title.strip() and ' ' in xml_title.strip():

                # rule 2: if there are numerals they must be included in both titles
                sig_num = get_signicant_numeral(json_title)
                # if there is a number
                if sig_num is not None:
                    # and its not in the xml_title

                    # if not sig_num in xml_title:
                    if not sig_num in json_title:
                        # skip to the next
                        continue

                j_title = str_pre_process(json_title)
                x_title = str_pre_process(xml_title)

            else:
                continue

            if json_cnt <= 9999999:
                ratio = fuzz.WRatio(x_title, j_title)
                if ratio > 89:
                    match = True
                    match_cnt +=1

                    print('+ Ratio ' + str(ratio) + '% -> ' + ' [' + game['title_id'] + ']' + ' [' + json_title + ']' + ' vs [' + xml_title + ']')
                    print('+ Match: ' + str(match_cnt) + ' of ' + str(json_max_cnt) + '\n')


                elif ratio > 86:
                    potential_match_cnt +=1

                    match = False
                    print('    - Ratio ' + str(ratio) + '% -> ' + ' [' + game['title_id'] + ']' + ' [' + json_title + ']' + ' vs [' + xml_title + ']')
                    print('    - Match: ' + str(match_cnt) + ' of ' + str(json_max_cnt) + '\n')


                else:
                    non_match_cnt +=1
