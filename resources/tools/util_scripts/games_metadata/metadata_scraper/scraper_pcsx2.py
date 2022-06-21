import json
import os
from global_paths import AppPaths

# Serial = PBPX-95205
# Name   = Playstation 2 - Demo Disc 2000
# Region = PAL-Unk

# {
#     "title_id":"SLUS-21488",
#     "meta_data_link":null,
#     "title":".Hack - G.U. Vol.2 - Reminisce"
# }
null = None
j_body = json.loads("""{"games":[]}""")
game_list = j_body['games']
games_string = ''
print(os.path.dirname(os.path.join(AppPaths.games_metadata, 'GamesIndex.txt')))
try:
    with open(os.path.join(AppPaths.games_metadata, 'GameIndex.txt'), 'r') as f:
        # print(f.read())
        title_id    = ''
        title       = ''
        region      = ''
        for x in f:

            if 'Serial = ' in x:
                title_id = x.replace('Serial = ', '')
                title_id = title_id.replace('\n', '')
                # print(title_id)
            elif 'Name   = ' in x:
                title = x.replace('Name   = ', '')
                title = title.replace('\n', '')
                # print(title)
            elif 'Region = ' in x:
                region = x.replace('Region = ', '')
                region = region.replace('\n', '')
                # print(region)
                if title_id is not '' and title is not '' and region is not '':
                    game_list.append({
                        "title_id": title_id,
                        "title": title,
                        "region": region,
                        "meta_data_link": null})
                    title_id    = ''
                    title       = ''
                    region      = ''
                    # games_string = games_string + title_id + '\n' + title + '\n' + region + '\n'

                    next(f)

        f.close()
        with open(os.path.join(AppPaths.games_metadata, 'GamesIndex.json'), "w") as newFile:
            json_text = json.dumps(j_body, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
            newFile.write(json_text)
        # with open(os.path.join(AppPaths.games_metadata, 'GamesIndex_str.txt', "w") as newFile:
        #     json_text = json.dumps(game_list, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
except Exception as e:
    print(e)
