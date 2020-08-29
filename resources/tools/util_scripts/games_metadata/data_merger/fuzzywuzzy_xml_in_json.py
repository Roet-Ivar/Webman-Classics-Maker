# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, re, os
import xml.etree.ElementTree as Etree




platform = 'PSP'
regular_list = False
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


# Get number of games in xml
xml_max_cnt = 0
for x in xml_root.iter('Game'):
    xml_max_cnt +=1

# Get number of games in json
json_max_cnt = 0
for game in json_data['games']:
    json_max_cnt +=1

migrated_games = {"games":[]}
non_migrated_games = {"games":[]}
if True:
    print('DEBUG progress:')

    match_cnt = 0
    non_match_cnt = 0

    json_cnt = 0
    for game in json_data['games']:
        is_migrated = False
        json_cnt +=1
        if len(migrated_games) > 0:
            for g in migrated_games['games']:
                if game['title_id'] == g['title_id']:
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
            is_migrated = False
            xml_cnt +=1
            xml_title = x.find('Name').text

            # rule 1: title must have more than one word (this need to handled later)
            if ' ' in json_title.strip() and ' ' in xml_title.strip():

                # rule 2: if there are numerals they must be included in both titles

                sig_num = get_signicant_numeral(json_title)
                # if there is a number
                if sig_num is not None:
                    # and its not in the xml_title

                    if not sig_num in xml_title:
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
                        match_cnt += 1
                        is_migrated = True
                        continue

            if not is_migrated:
                for g in migrated_games['games']:
                    if g['title_id'] == game['title_id']:
                        is_migrated = True
                if not is_migrated:
                    game['database_id'] = x.find('DatabaseID').text
                    migrated_games['games'].append(game)
                    print('Migrated -> ' + game['title_id'] + ': ' + game['title'])
                    is_migrated = True

                    continue

        # only show progress when percentage increased
        progress_percent = int(100*json_cnt/json_max_cnt)
        if progress_percent != int(100*(json_cnt-1)/json_max_cnt):

            if progress_percent == 100:
                print('-----------------------------------------------------------------------')
                print('DONE')
                print('-----------------------------------------------------------------------')
                print('[Match count: ' + str(int(100*match_cnt/json_max_cnt)) + '% (' + str(match_cnt) + '/' + str(json_max_cnt) + ')]')

            else:
                print('[Progress: ' + str(int(100*json_cnt/json_max_cnt)) + '% (' + str(json_cnt) + '/' + str(json_max_cnt) + ')]')




    #
    # for x in json_data['games']:
    #     exist = False
    #     for y in migrated_games['games']:
    #         if y['title_id'] == x['title_id']:
    #             exist = True
    #         else:
    #             exist = False
    #
        # if not exist:
            # migrated_games['games'].append(x)


    with open(platform + '_migrated.json', "w") as newFile:
        json_text = json.dumps(migrated_games, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
        newFile.write(json_text)

