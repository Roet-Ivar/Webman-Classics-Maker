import json
from bs4 import BeautifulSoup
import requests
# Here, we're just importing both Beautiful Soup and the Requests library
page_link = 'https://psxdatacenter.com/psx2/ulist2.html'
# this is the url that we've already determined is safe and legal to scrape from.
page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library
page_content = BeautifulSoup(page_response.content, "html.parser")

table = page_content.find('table', {"id":"table302"})
rows = table('tr')
col1s = rows.find('td')

# col1 = rows('td')
#
print('')