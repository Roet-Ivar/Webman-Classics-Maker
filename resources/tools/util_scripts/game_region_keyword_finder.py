import json
import re
import copy

# Platform: 'psp'/'psx'/'ps2'
platform = 'psx'

# Region: 0 - 2 -> us/eu/jp
region = 2

game_list_file_name = []
if 'psp' in platform:
    game_list_file_name.append('./games_metadata/psp_us_games_list.json')
    game_list_file_name.append('./games_metadata/psp_eu_games_list.json')
    game_list_file_name.append('./games_metadata/psp_jp_games_list.json')
if 'psx' in platform:
    game_list_file_name.append('./games_metadata/psx_us_games_list.json')
    game_list_file_name.append('./games_metadata/psx_eu_games_list.json')
    game_list_file_name.append('./games_metadata/psx_jp_games_list.json')
if 'ps2' in platform:
    game_list_file_name.append('./games_metadata/ps2_us_games_list.json')
    game_list_file_name.append('./games_metadata/ps2_eu_games_list.json')
    game_list_file_name.append('./games_metadata/ps2_jp_games_list.json')
# load the needed json data
# region_list_data = json.loads("""{"us_region":[],"eu_region":[],"jp_region":[]}""")
region_list_file_name = 'region_list.json'
with open(region_list_file_name) as f:
    region_list_data = json.load(f)

with open(game_list_file_name[region]) as f:
    active_game_list_data = json.load(f)

# active_region
if """us_""" in str(game_list_file_name[region]):
    active_region = region_list_data[platform]['us_region']
elif """eu_""" in game_list_file_name[region]:
    active_region = region_list_data[platform]['eu_region']
elif """jp_""" in game_list_file_name[region]:
    active_region = region_list_data[platform]['jp_region']

# make stuff
try:
    for m in re.finditer("""(\w{4}\-\d{5})""", str(active_game_list_data)):
        game_region = str(m.group(0))
        game_region = game_region[0:4]
        key = 'region'
        reg_flag = False

        # if list is empty, add first region
        if len(active_region) < 1:
            print('test')
            active_region.append({
                "region": game_region})

        for reg in active_region:
            list_region = str(reg[key])
            if game_region == list_region:
                reg_flag = True
                break
            else:
                continue
        if not reg_flag:
            active_region.append({
                "region": game_region})
        reg_flag = False

except Exception, e1:
    print('e1: ' + str(e1))
    game_id = ''
# us_game_list_data
print('')


# save region file

with open(region_list_file_name, "w") as regions_file:
    json_text = json.dumps(region_list_data, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    regions_file.write(json_text)

