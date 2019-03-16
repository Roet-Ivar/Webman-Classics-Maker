import json
from bs4 import BeautifulSoup
import requests

us_file_name = 'us_ps2_game_db.json'
us_page_link = 'https://psxdatacenter.com/psx2/ulist2.html'

jp_file_name = 'jp_ps2_game_db.json'
jp_page_link = 'https://psxdatacenter.com/psx2/jlist2.html'

eu_page_link = 'https://psxdatacenter.com/psx2/plist2.html'
eu_file_name = 'eu_ps2_game_db.json'

file_name = eu_file_name
page_link = eu_page_link

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

with open(file_name) as f:
    json_game_list_data = json.load(f)


link = []
title_id = []
title = []

i = 0
for col in col1s:
    link = ''
    try:
        link = col.a.get('href')
    except:
        link =''

    title_id = col2s[i].get_text(separator=u' ')



    title = col3s[i].get_text(separator=u' ')
    # title = title.decode('latin1')
    # title = title.prettify('latin-1')
    # title = title.replace(u"\u00A0", "")


    json_game_list_data['ps2_games'].append({
        "meta_data_link": link,
        "title_id": title_id,
        "title": title})

    i += 1

with open(file_name, "w") as newFile:
    json_text = json.dumps(json_game_list_data, indent=4, separators=(",", ":"))
    newFile.write(json_text)

print('')
