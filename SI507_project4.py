import requests, json
from bs4 import BeautifulSoup
from caching import Cache
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


START_URL = "https://www.nps.gov/index.htm"
FILENAME = "np_cache.json"

PROGRAM_CACHE = Cache(FILENAME)

def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data)
    return data

main_page = access_page_data(START_URL)


main_soup = BeautifulSoup(main_page, features="html.parser")
list_of_topics = main_soup.find('ul',{'class':'dropdown-menu SearchBar-keywordSearch'})


state_links = list_of_topics.find_all('a')

state_pages = []
for s in state_links:
    # print(s) for testing
    page_data = access_page_data('http://www.nps.gov' + s['href'])
    soup_of_page = BeautifulSoup(page_data, features="html.parser")
    # print(soup_of_page) for testing
    state_pages.append(soup_of_page)


# print(state_pages[0].prettify()) for testing

all_list = []
for state in state_pages:
    each_site = state.find_all('li', {'class':'clearfix'})
    for site in each_site:
        each_site_list = []
        if site.find('h3') == None:
            continue

        if site.find('h3'):
            site_name = site.find('h3')
            # print(site_name.text) for testing
            each_site_list.append(site_name.text)
        if len(site.find('h2')) == 0:
            each_site_list.append('Not Available')
        else:
            site_type = site.find('h2')
            # print(site_type.text) for testing
            each_site_list.append(site_type.text)
        if site.find('p'):
            site_desc = site.find('p')
            # print(site_desc.text) for testing
            each_site_list.append(site_desc.text.replace('\n',' '))
        if len(site.find('h4')) == 0:
                each_site_list.append('Not Available')
        else:
            location = site.find('h4')
            # print(location.text) for testing
            each_site_list.append(location.text)
        # print(each_site_list) for testing
        all_list.append(each_site_list)
