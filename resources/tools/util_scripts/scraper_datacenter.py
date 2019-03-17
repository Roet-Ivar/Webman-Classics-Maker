import json
from bs4 import BeautifulSoup
import requests

# Platform: 'psp'/'psx'/'ps2'
platform = 'psp'

# Region: 0 - 2 -> us/eu/jp
region = 2

game_list_file_name = []
page_link_list = []

if 'psp' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['psp_games']

    game_list_file_name.append('./games_metadata/psp_us_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psp/ulist.html')

    game_list_file_name.append('./games_metadata/psp_eu_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psp/plist.html')

    game_list_file_name.append('./games_metadata/psp_jp_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psp/jlist.html')


if 'psx' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['psx_games']

    game_list_file_name.append('./games_metadata/psx_us_games_list.json')
    page_link_list.append('https://psxdatacenter.com/ulist.html')

    game_list_file_name.append('./games_metadata/psx_eu_games_list.json')
    page_link_list.append('https://psxdatacenter.com/plist.html')

    game_list_file_name.append('./games_metadata/psx_eu_games_list.json')
    page_link_list.append('https://psxdatacenter.com/jlist.html')

if 'ps2' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['ps2_games']

    game_list_file_name.append('./games_metadata/ps2_us_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psx2/ulist2.html')

    game_list_file_name.append('./games_metadata/ps2_eu_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psx2/plist2.html')

    game_list_file_name.append('./games_metadata/ps2_jp_games_list.json')
    page_link_list.append('https://psxdatacenter.com/psx2/jlist2.html')


file_name = game_list_file_name[region]
page_link = page_link_list[region]

page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")

col1s = page_content.findAll('td', {"class":"col1"})
col5s = page_content.findAll('td', {"class":"col5"})
col1s.extend(col5s)

col2s = page_content.findAll('td', {"class":"col2"})
col6s = page_content.findAll('td', {"class":"col6"})
col2s.extend(col6s)

col3s = page_content.findAll('td', {"class":"col3"})
col7s = page_content.findAll('td', {"class":"col7"})
col3s.extend(col7s)


link = []
title_id = []
title = []
null = None

i = 0
for col in col1s:
    link = ''
    try:
        link = col.a.get('href')
    except:
        link = null

    title_id = col2s[i].get_text(separator=u' ')
    title = col3s[i].get_text(separator=u' ')
    title = title.replace(u"\u00A0", "") # removes the initial non-breaking space

    game_list.append({
        "meta_data_link": link,
        "title_id": title_id,
        "title": title})
    i += 1

with open(file_name, "w") as newFile:
    json_text = json.dumps(json_game_list_data, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    newFile.write(json_text)

print('')
