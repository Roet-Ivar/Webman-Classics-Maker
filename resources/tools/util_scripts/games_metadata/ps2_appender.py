import json, os
from global_paths import AppPaths

with open(os.path.join(AppPaths.games_metadata, 'GamesIndex_2.json')) as f:
    pcsx2_all_list_data = json.load(f)
    f.close()

# region = 'PAL'
# region = 'NTSC-U'
region = 'NTSC-J'

if 'NTSC-U' in region:
    with open(os.path.join(AppPaths.games_metadata, 'ps2_us_games_list.json')) as f:
        psxcenter_list_data = json.load(f)
if 'PAL' in region:
    with open(os.path.join(AppPaths.games_metadata, 'ps2_eu_games_list.json')) as f:
        psxcenter_list_data = json.load(f)
if 'NTSC-J' in region:
    with open(os.path.join(AppPaths.games_metadata, 'ps2_jp_games_list.json')) as f:
        psxcenter_list_data = json.load(f)

# json_body = json.loads("""{"games":[]}""")
pcsx2_games = pcsx2_all_list_data['games']
pdc_games = psxcenter_list_data['games']

pcsx2_str = str(pcsx2_games)
# for pcsx2_game in pcsx2_games:
for game in pdc_games:
    pdc_title_id = str(game['title_id'])
    if pdc_title_id not in pcsx2_str:
        print(pdc_title_id + ' not in the list')
        pcsx2_games.append(
        {
            "title_id": game['title_id'],
            "meta_data_link": game['meta_data_link'],
            "region": region,
            "title": game['title']
        })
        # break
# json_body.append(str(pcsx2_games))

pcsx2_all_list_data['games'] = pcsx2_games
with open(os.path.join(AppPaths.games_metadata, 'GamesIndex_2.json'), "w") as newFile:
    json_text = json.dumps(pcsx2_all_list_data, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    newFile.write(json_text)