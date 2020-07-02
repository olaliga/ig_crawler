import requests
from bs4 import BeautifulSoup
import json
import requests_html
import re
import os
import time
import numpy as np

session = requests_html.HTMLSession()
os.chdir('location_data2') # saving file

def crawler(url,param = None):  # ,cookie):
    r = session.get(url, params = param)
    r.encoding = 'utf-8'
    r.html.render(timeout = 800000)  # , cookies = cookie)
    return r


Base_url = 'https://www.instagram.com/explore/locations/'
# location

# 找出所有city
url = Base_url + 'TW/taiwan/'
next_page = 0
i = 0
city_list = []
while i == 0 or next_page != None:
    i += 1
    r = crawler(url + '?page=' + str(i))
    soup = BeautifulSoup(r.text, "lxml")
    scripts = soup.find_all('script')
    for t in scripts:
        try:
            need = json.loads(str(t)[re.search('window._sharedData = ', str(t)).span()[1]:len(str(t)) - 10])
            print('city_crawler page: ' + str(i))
        except:
            pass
    city_list = city_list + need['entry_data']['LocationsDirectoryPage'][0]['city_list']
    next_page = need['entry_data']['LocationsDirectoryPage'][0]['next_page']

# 找出所有sights
id_need = city_list[0]['id']
url_1 = Base_url + id_need + '/'
next_page = 0
i = 0
location_list = []
while i == 0 or next_page != None:
    i += 1
    r1 = crawler(url_1 + '?page=' + str(i))
    soup1 = BeautifulSoup(r1.text, "lxml")
    scripts1 = soup1.find_all('script')
    for t in scripts1:
        try:
            need1 = json.loads(str(t)[re.search('window._sharedData = ', str(t)).span()[1]:len(str(t)) - 10])
            print('page: ' + str(i))
        except:
            pass
    location_list = location_list + need1['entry_data']['LocationsDirectoryPage'][0]['location_list']
    next_page = need1['entry_data']['LocationsDirectoryPage'][0]['next_page']

# sights crawler
lat = []
lng = []
complete = []

for i in range(len(location_list)):
    url2 = Base_url + location_list[i]['id']+'/'
    r2 = crawler(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    scripts2 = soup2.find_all('script')
    for t in scripts2:
        try:
            need = json.loads(str(t)[re.search('window._sharedData = ', str(t)).span()[1]:len(str(t)) - 10])
        except:
            pass

    # need['entry_data']['LocationsPage'][0]['graphql']['location'] 有許多好用的東西
    lat.append(need['entry_data']['LocationsPage'][0]['graphql']['location']['lat']) #緯度
    lng.append(need['entry_data']['LocationsPage'][0]['graphql']['location']['lng']) #經度
    total_count = need['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['count']
    page_info = need['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['page_info']
    edges = need['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
    location_name = need['entry_data']['LocationsPage'][0]['graphql']['location']['name']
    variables = {
        'id': location_list[i]['id'],
        'first': 30,
        'after': page_info['end_cursor']}
    query_para = {'query_hash': '36bd0f2bf5911908de389b8ceaa3be6d',
                  'variables': json.dumps(variables)
                  }

    while page_info['has_next_page'] == True:
        try:
            r_new = requests.get('https://www.instagram.com/graphql/query', query_para)  # , proxies = proxies)  # ,cookies=cookie)
            page_data_new = json.loads(r_new.text)
            edges_new = page_data_new['data']['location']['edge_location_to_media']['edges']
            page_info = page_data_new['data']['location']['edge_location_to_media']['page_info']
            end_cursor2 = page_data_new['data']['location']['edge_location_to_media']['page_info']['end_cursor']
            edges = edges + edges_new
            print(location_name + ': {:f}'.format(len(edges) / total_count, 3))
            variables['after'] = end_cursor2
            query_para['variables'] = json.dumps(variables)
        except:
            time.sleep(2)
    a = np.array(edges)
    np.save('ig' + location_name + '.npy', a)
    complete.append(len(edges) / total_count)
