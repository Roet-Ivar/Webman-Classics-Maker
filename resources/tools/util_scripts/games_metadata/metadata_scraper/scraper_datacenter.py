import json, os, re, requests
from bs4 import BeautifulSoup
from resources.tools.util_scripts import AppPaths

game_list_file_name = []
page_link_list = []

# Platform: 'psp'/'psx'/'ps2'
platform = 'ps2'

# Region: 0 - 2 -> us/eu/jp
region = 2


if 'psp' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['games']

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psp_us_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/psp/ulist.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psp_eu_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/psp/plist.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psp_jp_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/psp/jlist.html')


if 'psx' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['games']

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psx_us_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/ulist.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psx_eu_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/plist.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'psx_jp_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/jlist.html')

if 'ps2' == platform:
    x = """{"games":[]}"""
    json_game_list_data = json.loads(x)
    game_list = json_game_list_data['games']

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'ps2_us_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/psx2/ulist2.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'ps2_eu_games_list.json'))
    page_link_list.append('https://psxdatacenter.com/psx2/plist2.html')

    game_list_file_name.append(os.path.join(AppPaths.games_metadata, 'ps2_jp_games_list.json'))
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


def get_title_from_meta_link(meta_link):
    base_url = 'https://psxdatacenter.com/'
    platform_url = ''
    if 'psp' in platform:
        platform_url = 'psp/'
        ot_word = 'OFFICIAL TITLE'
    elif 'psx' in platform:
        platform_url = ''
        ot_word = 'Official Title'
    elif 'ps2' in platform:
        platform_url = 'psx2/'
        ot_word = 'OFFICIAL TITLE'

    full_link = base_url + platform_url + meta_link
    meta_link_response = requests.get(full_link, timeout=5)
    meta_link_content = BeautifulSoup(meta_link_response.content, "html.parser")

    ot_text = meta_link_content.find(text="""\r\n\t\t\t\t""" + ot_word)
    if ot_text is null or ot_text is '':
        ot_text = meta_link_content.find(text=re.compile(r'(\s)*' + ot_word))
        print()
    try:
        ot_parent = ot_text.parent
        title_parent = ot_parent.findNext('td')
        title_text = title_parent.contents[0].strip()

    except Exception as e:
        print('parent error?: ' + str(e))
        title_text = null
        return title_text
    print(title_text)
    return title_text

i = 0
for col in col1s:
    title = null
    link = null
    title_id = col2s[i].get_text(separator=u' ')

    try:
        link = col.a.get('href')
    except:
        link = null

    # if there is a metadata link, get title
    if link is not null:
        title = get_title_from_meta_link(link)


    # if no title from link, get regular title
    if title is null:
        title = col3s[i].get_text(separator=u' ')
        title = title.replace(u"\u00A0", "") # removes the initial non-breaking space
        title = title.title()



    game_list.append({
        "meta_data_link": link,
        "title_id": title_id,
        "title": title})
    i += 1

with open(file_name, "w") as newFile:
    json_text = json.dumps(json_game_list_data, indent=4, separators=(",", ":"), ensure_ascii=False).encode('utf8')
    newFile.write(json_text)

print('')
