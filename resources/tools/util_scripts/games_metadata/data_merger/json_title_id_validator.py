# download launchbox metadata here: http://gamesdb.launchbox-app.com/Metadata.zip
from fuzzywuzzy import fuzz
import json, re, os
import xml.etree.ElementTree as Etree




platform = 'PSP'
with open(platform + '_all_title_ids.json') as f: # 6896
    json_data = json.load(f)
json_data_tmp = json_data


# Get number of games in json
json_max_cnt = 0
for game in json_data['games']:
    json_max_cnt +=1


def check_title_id_duplicates(json_data):
    dup_title_id_list = {"games": []}
    duplicates_titles_tot = 0
    one_duplicates_tot = 0
    two_duplicates_tot = 0
    three_duplicates_tot = 0
    four_duplicates_tot = 0


    tot_exact_match_cnt = 0
    for game in json_data['games']:
        exact_match_cnt = 0

        id = game['title_id']
        title = game['title']

        has_duplicates = False
        tmp_duplicate_cnt = 0

        tmp_duplicate_id = ''
        tmp_duplicate_title = ''
        for g in json_data['games']:
            if g['title_id'] == id and g['title'] == title:


                exact_match_cnt +=1
                tot_exact_match_cnt +=1

                game['count'] = str(exact_match_cnt)
                dup_title_id_list['games'].append(game)

                if exact_match_cnt > 1:
                    print('Exact match -> title_id: ' + tmp_duplicate_id + ', title: ' + tmp_duplicate_title + ', occurred: ' + str(exact_match_cnt) + ' times.')

            if g['title_id'] == id:
                tmp_duplicate_cnt +=1
                tmp_duplicate_id = id
                tmp_duplicate_title = g['title']

                # if tmp_duplicate_cnt > 1:
                #     print('Duplicate of title_id: ' + tmp_duplicate_id + ', title: ' + tmp_duplicate_title + ', occurred: ' + str(tmp_duplicate_cnt) + ' times.')

        if tmp_duplicate_cnt > 1:
            duplicates_titles_tot +=1
            # print('Duplicate of title_id: ' + tmp_duplicate_id + ', title: ' + tmp_duplicate_title + ', occurred: ' + str(tmp_duplicate_cnt) + ' times.')



            # game['count'] = str(tmp_duplicate_cnt)
            # dup_title_id_list['games'].append(game)

    # for g in json_data['games']:
    #     for ga in dup_title_id_list['games']:
    #         if g['title_id'] == ga['title_id']:
                # print('Title id: ' + g['title_id'] + ', title: ' + g['title'] + ', count: ' + g['count'])

    print('Exact match count: ' + str(tot_exact_match_cnt-json_max_cnt))



check_title_id_duplicates(json_data)

# # Get number of games in json
# json_max_cnt = 0
# for game in json_data['games']:
#     json_max_cnt +=1
#
# if True:
#     match_cnt = 0
#     non_match_cnt = 0
#
#     json_cnt = 0
#     for game in json_data['games']:
#         is_migrated = False
#         json_cnt +=1
#
#         if(platform == 'PS3'):
#             for l in game['locale']:
#                 if 'EN' == l['lang']:
#                     json_title = l['title']
#         else:
#             json_title = game['title']
#         json_title_id = game['title_id']
#
#
#         check_title_id_duplicates(json_data)

        # validate_title_id(json_title_id)
        # validate_title(json_title)





        # # only show progress when percentage increased
        # progress_percent = int(100*json_cnt/json_max_cnt)
        # if progress_percent != int(100*(json_cnt-1)/json_max_cnt):
        #
        #     if progress_percent == 100:
        #         print('-----------------------------------------------------------------------')
        #         print('DONE')
        #         print('-----------------------------------------------------------------------')
        #         print('[Match count: ' + str(int(100*match_cnt/json_max_cnt)) + '% (' + str(match_cnt) + '/' + str(json_max_cnt) + ')]')
        #
        #     else:
        #         print('[Progress: ' + str(int(100*json_cnt/json_max_cnt)) + '% (' + str(json_cnt) + '/' + str(json_max_cnt) + ')]')


    # with open(platform + '_migrated.json', "w") as newFile:
    #     json_text = json.dumps(migrated_games, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    #     newFile.write(json_text)

