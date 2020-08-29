# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, re, os
import xml.etree.ElementTree as Etree



# count 6896
platform = 'PSP'
migrated_games = None

with open(platform + '_all_title_ids.json') as f: # 6896
    # with open(os.path.join('_results', platform + '_not_migrated')) as f: # 6896
    json_data = json.load(f)
json_data_tmp = json_data

parser = Etree.XMLParser(encoding="utf-8")
xml_tree = Etree.parse(platform + '_LaunchBox_Alt.xml', parser=parser)
xml_root = xml_tree.getroot()

def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


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



xml_max_cnt = 0
for x in xml_root.iter('Game'):
    xml_max_cnt +=1
json_max_cnt = 0
for game in json_data['games']:
    json_max_cnt +=1

migrated_games = {"games":[]}
non_migrated_games = {"games":[]}
if True:
    print('DEBUG progress:')
    # json_max_cnt = 6896
    # xml_max_cnt = 1682

    match_cnt = 0
    non_match_cnt = 0

    json_cnt = 0
    for game in json_data['games']:
        is_migrated = False
        json_cnt +=1
        # xml_cnt = 0
        # for x in xml_root.iter('Game'):
        #     xml_cnt +=1
        #     xml_title = x.find('Name').text
        if len(migrated_games) > 0:
            for g in migrated_games['games']:
                if game['title_id'] == g['title_id']:
                    # if get_attribute(m_game, 'database_id', None) is not None:
                    #     print('Game already got a DatabaseID: ' + str(game['database_id']))
                    continue

        if(platform == 'PS3'):
            for l in game['locale']:
                if 'EN' == l['lang']:
                    json_title = l['title']
        else:
            json_title = game['title']
        json_title_id = game['title_id']

        # json_cnt = 0
        # for game in json_data['games']:
        #     json_cnt +=1
        xml_cnt = 0
        for x in xml_root.iter('Game'):
            xml_cnt +=1
            xml_title = x.find('Name').text

            # rule 1: title must have more than one word (this need to handled later)
            if ' ' in json_title.strip() and ' ' in xml_title.strip():

                # rule 2: if there are numerals they must be included in both titles

                # sig_num = get_signicant_numeral(json_title)
                sig_num = get_signicant_numeral(xml_title)
                # if there is a number
                if sig_num is not None:
                    # and its not in the xml_title

                    if not sig_num in xml_title:
                        # if not sig_num in json_title:

                        # no match, skip to the next
                        continue

                j_title = str_pre_process(json_title)
                x_title = str_pre_process(xml_title)
            else:
                continue

            ratio = fuzz.WRatio(x_title, j_title)
            if ratio > 99:
                for g in migrated_games['games']:
                    if g['title_id'] == game['title_id']:
                        is_migrated = True

                # if get_attribute(game, 'database_id', None) is None:
                #    match_cnt +=1

                # if get_attribute(game, 'DatabaseID', None) is None:
                if not is_migrated:
                    match_cnt +=1
                    game['database_id'] = x.find('DatabaseID').text
                    migrated_games['games'].append(game)
                    print('Added -> match: ' + game['title_id'] + '; name: '+ game['title'])
                    print('match_cnt: ' + str('6896/' + match_cnt))


        # if not is_migrated:
        #     skip = False
        #     for g in migrated_games['games']:
        #         if g['title_id'] == game['title_id']:
        #             skip = True
        #     if not skip:
        #         print('Added -> No match: ' + game['title_id'] + '; ' + game['title'])
        #         migrated_games['games'].append(game)


    for y in migrated_games['games']:
        exist= False
        for x in json_data['games']:
            if y['title_id'] == x['title_id']:
                exist = True
        if exist:
            non_migrated_games['games'].append(x)

    non_migrated_games['games'].extend(migrated_games['games'])


    # save
    # with open(platform + '_migrated.json', "w") as newFile:
    #     json_text = json.dumps(migrated_games, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    #     newFile.write(json_text)
    #
