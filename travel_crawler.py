import requests
from bs4 import BeautifulSoup

import pyppdf.patch_pyppeteer
import lxml
import re
import json
import codecs
import urllib
import requests_html
import time
import random
import numpy as np


session = requests_html.HTMLSession()
def crawler(url,param = None):  # ,cookie):
    r = session.get(url, params = param)
    r.encoding = 'utf-8'
    r.html.render(timeout = 800000)  # , cookies = cookie)
    return r


"""

##
url='https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
r = crawler(url)
soup = BeautifulSoup(r.text, "lxml")
data_str = soup.get_text()[1:]
decoded_data = codecs.decode(r.text.encode(), 'utf-8-sig')
data = json.loads(decoded_data)
data1 = data['XML_Head']['Infos']['Info']

## sights to data_frame
import pandas as pd
df1 = pd.DataFrame(data1)
#print(df1)

## for loop 尚未寫

#取得id
urlid1 = 'https://www.instagram.com/web/search/topsearch/?context=blended&query='
urlid2 = urllib.parse.quote(df1['Name'][0]) #for
urlid = urlid1+urlid2
url = urlid1+urlid2

r = crawler(url)
soup = BeautifulSoup(r.text, "lxml")
id_dict = json.loads(str(soup.find_all('p'))[4:len(str(soup.find_all('p')))-5])
id_need = id_dict['places'][0]['place']['location']['pk']

#location
url1 ='https://www.instagram.com/explore/locations/'
url2 = id_need + '/-/' 
url = url1+url2
r = crawler(url)
# output observe
intro = r.html.find(".-vDIg", first=True)
print(intro.text)
print('------------------------------------')
print(r.html.find("v9tJq AAaSh VfzDr~_3dEHb", first=True))
print(r.html.find("li", first=True).text)
print(r.html.find("ul", first=True).text)
# hashtag
url1 ='https://www.instagram.com/explore/tags/'
url2 = df1['Name'][1]+'/' #for
crawler(url)
# output observe
print(soup.prettify())
"""

# by 縣市
city = ['台中']

    #['屏東', '台東', '苗栗', '花蓮', '台中', '宜蘭', '彰化', '澎湖', '南投', '金門','雲林', '連江']
city2 = ['基隆', '嘉義', '台北', '新北', '台南', '桃園', '高雄', '新竹', '屏東', '台東', '苗栗', '花蓮', '台中', '宜蘭', '彰化', '澎湖', '南投', '金門',
        '雲林', '連江']
complete = []

for i in range(len(city)):
    # hashtag
    url1 = 'https://www.instagram.com/explore/tags/'
    url2 = city[i] + '景點' + '/'  # for
    urls = url1 + url2
    url3 = '?__a=1'
    url = urls + url3
    r = crawler(url)
    end_cursor_data = json.loads(r.text[11:len(r.text) - 1])
    total_count = end_cursor_data['hashtag']['edge_hashtag_to_media']['count']
    page_info = end_cursor_data['hashtag']['edge_hashtag_to_media']['page_info']
    edges = end_cursor_data['hashtag']['edge_hashtag_to_media']['edges']
    edges_o = edges
    variables = {
        'tag_name': city[i] + '景點',
        'first': 30,
        'after': page_info['end_cursor']}
    query_para = {'query_hash': '7dabc71d3e758b1ec19ffb85639e427b',
                  'variables': json.dumps(variables)
                  }
    try :
        while len(edges) < total_count :
            r_new = crawler('https://www.instagram.com/graphql/query', query_para)#, proxies = proxies)  # ,cookies=cookie)
            page_data_new = json.loads(r_new.text)
            edges_new = page_data_new['data']['hashtag']['edge_hashtag_to_media']['edges']
            end_cursor2 = page_data_new['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            edges = edges + edges_new
            print(city[i]+': {:f}'.format(len(edges)/total_count,3))
            variables['after'] = end_cursor2
            query_para['variables'] = json.dumps(variables)
            time.sleep(2)
        a = np.array(edges)
        np.save('ig' + city[i] + '.npy', a)
        complete.append(len(edges) / total_count)
    except :
        a = np.array(edges)
        np.save('ig'+city[i]+'.npy', a)
        complete.append(len(edges)/total_count)



"""
check = edges
for i in range(len(check)):
  check[i]=str(edges[i])
myset = set(check)
print("myset: "+str(len(list(myset))))
print("edges: "+str(len(edges)))

for i in range(len(edges_new)):
  for j in range(len(edges_new2)):
    if edges_new[i] == edges_new2[j] :
      print("edges_new: "+str(i)+"\nedges_new2:"+str(j))

"""
# print(len(page_data['data']['hashtag']['edge_hashtag_to_media']['edges'])) #first*3

"""
'https://www.instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables=%7B%22tag_name%22%3A%22%E6%96%B0%E7%AB%B9%E6%99%AF%E9%BB%9E%22%2C%22first%22%3A6%2C%22after%22%3A%22QVFBdTZKREd6eTM4ZTZiSXNSeTBpbGEtcWpWUnRpMUR5MmN1S2xHWUlUdVdrRV85LTZad3g4dXVWc3N0b1RfclIxV2hrbnlzUGU1dkpxelJoRTVhWF9hYg%3D%3D%22%7D'

#fb -> ming han
url1 = 'https://m.facebook.com/'
user_agent_g = user_agent.generate_user_agent()
r = requests.get(url1, headers={'user-agent': user_agent_g },auth=('', ''))
 r.encoding = 'utf-8'
 print(r.text)
 soup = BeautifulSoup(r.text, "lxml")


print(soup.prettify())
txt = open('ig_hashtag.txt','w')
txt.write(soup.prettify())
txt.close()

data = json.loads(soup.get_text())
data_list = 
for i in data_str:


data_json = soup.prettify()
print('------------------------------------')

url = 'https://www.instagram.com/static/bundles/es6/TagPageContainer.js/1cd2f84e371f.js'
r = crawler(url)
soup = BeautifulSoup(r.text, "lxml")

txt = open('query_id.txt','w')
txt.write(soup.prettify())
txt.close()

string = soup.prettify()
start = string.find('t.tagMedia.byTagName.get(n)).pagination,queryId:')

import requests_html
session = requests_html.HTMLSession()
r = session.get(url)
r.encoding = 'utf-8'
, headers={ 'user-agent': user_agent })
r.html.render(timeout=50)
 output observe
data_json =
print(intro.text)
print('------------------------------------')
print(r.html.find("v9tJq AAaSh VfzDr~_3dEHb", first=True))
print(r.html.find("li", first=True).text)
print(r.html.find("ul", first=True).text)

# api

import json
import os

with open('datagovtw_dataset_20200512.json') as f:
  data = json.load(f)
len(list(data))
"""
