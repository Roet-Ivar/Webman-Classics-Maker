import json
import re
import copy

# Platform: 'PSP'/'PSX'/'PS2'
platform = 'PS2'
# Region: 0 - 2 -> us/eu/jp
region = 0

game_list_file_name = []
if 'PSP' in platform:
    game_list_file_name.append('./games_metadata/psp_us_games_list.json')
    game_list_file_name.append('./games_metadata/psp_eu_games_list.json')
    game_list_file_name.append('./games_metadata/psp_jp_games_list.json')
if 'PSX' in platform:
    game_list_file_name.append('./games_metadata/psx_us_games_list.json')
    game_list_file_name.append('./games_metadata/psx_eu_games_list.json')
    game_list_file_name.append('./games_metadata/psx_jp_games_list.json')
if 'PS2' in platform:
    game_list_file_name.append('./games_metadata/ps2_us_games_list.json')
    game_list_file_name.append('./games_metadata/ps2_eu_games_list.json')
    game_list_file_name.append('./games_metadata/ps2_jp_games_list.json')
# load the needed json data
# region_list_data = json.loads("""{"us_region":[],"eu_region":[],"jp_region":[]}""")
region_list_file_name = './games_metadata/region_list.json'
with open(region_list_file_name) as f:
    region_list_data = json.load(f)

with open(game_list_file_name[region]) as f:
    active_game_list_data = json.load(f)

# active_region
if """us_""" in str(game_list_file_name[region]):
    active_platform = region_list_data[platform]
    region = 'US'
elif """eu_""" in game_list_file_name[region]:
    active_platform = region_list_data[platform]
    region = 'EU'
elif """jp_""" in game_list_file_name[region]:
    active_platform = region_list_data[platform]
    region = 'JP'

# make stuff
try:
    for m in re.finditer("""(\w{4}\-\d{5})""", str(active_game_list_data)):
        id = str(m.group(0))
        id = id[0:4]
        key = 'id'
        reg_exist = False

        # if list is empty, add first region
        if len(active_platform) < 1:
            print('test')
            active_platform.append({
                "id": id, "region": region})

        for reg_id in active_platform:
            list_reg_id = str(reg_id[key])
            if id == list_reg_id:
                reg_exist = True
                break
            else:
                continue
        if not reg_exist:
            active_platform.append({
                "id": id, "region": region})
        reg_exist = False

except Exception as e1:
    print('e1: ' + str(e1))
    game_id = ''
# us_game_list_data
print('')


# save region file
with open(region_list_file_name, "w") as regions_file:
    json_text = json.dumps(region_list_data, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    regions_file.write(json_text)

