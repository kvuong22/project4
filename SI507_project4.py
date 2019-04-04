import requests, json
from bs4 import BeautifulSoup
from caching import Cache
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


START_URL = "https://www.nps.gov/index.htm"
FILENAME = "np_cache.json" #file name for all data to be cached in (1 file for caching for 1 program)

# So I can use 1 (one) instance of the Cache tool -- just one for my whole program, even though I'll get data from multiple places
PROGRAM_CACHE = Cache(FILENAME)

def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data) #put identifier in first and then what I want in there. # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
    return data

main_page = access_page_data(START_URL)

# explore... find that there's a <ul> with class 'topics' and I want the links at each list item...

# I've cached this so I can do work on it a bunch
main_soup = BeautifulSoup(main_page, features="html.parser")
list_of_topics = main_soup.find('ul',{'class':'dropdown-menu SearchBar-keywordSearch'})


state_links = list_of_topics.find_all('a')

state_pages = [] # gotta get all the data in BeautifulSoup objects to work with...
for s in state_links:
    # print(s)
    page_data = access_page_data('http://www.nps.gov' + s['href'])
    soup_of_page = BeautifulSoup(page_data, features="html.parser")
    # print(soup_of_page)
    state_pages.append(soup_of_page)


# print(state_pages[0].prettify()) testing

all_list = []
for state in state_pages:
    each_site = state.find_all('li', {'class':'clearfix'})
    for site in each_site:
        each_site_list = []
        if site.find('h3') == None:
            continue

        if site.find('h3'):
            site_name = site.find('h3')
            # print(site_name.text)
            each_site_list.append(site_name.text)
        if len(site.find('h2')) == 0:
            each_site_list.append('Not Available')
        else:
            site_type = site.find('h2')
            # print(site_type.text)
            each_site_list.append(site_type.text)
        if site.find('p'):
            site_desc = site.find('p')
            # print(site_desc.text)
            each_site_list.append(site_desc.text.replace('\n',' '))
        if len(site.find('h4')) == 0:
                each_site_list.append('Not Available')
        else:
            location = site.find('h4')
            # print(location.text)
            each_site_list.append(location.text)
        # print(each_site_list)
        all_list.append(each_site_list)
