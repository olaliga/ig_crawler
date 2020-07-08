import json
import time
import numpy as np
import os
import requests
import multiprocessing as mp
import fun

os.chdir('hashtag_data')
# by 縣市
city = ['基隆', '嘉義', '台北', '新北', '台南', '桃園', '高雄', '新竹', '屏東', '台東', '苗栗', '花蓮',
        '台中', '宜蘭', '彰化', '澎湖', '南投', '金門', '雲林', '連江']
complete = []

# hashtag
# for i in range(len(city)):

def need_to_crawler(i):
    url1 = 'https://www.instagram.com/explore/tags/'
    url2 = city[i] + '景點' + '/'  # for
    urls = url1 + url2
    url3 = '?__a=1'
    url = urls + url3
    r = requests.get(url)
    end_cursor_data = json.loads(r.text[11:len(r.text) - 1])
    total_count = end_cursor_data['hashtag']['edge_hashtag_to_media']['count']
    page_info = end_cursor_data['hashtag']['edge_hashtag_to_media']['page_info']
    edges = end_cursor_data['hashtag']['edge_hashtag_to_media']['edges']
    edges = fun.clean_data(edges)
    variables = {
        'tag_name': city[i] + '景點',
        'first': 30,
        'after': page_info['end_cursor']}
    query_para = {'query_hash': '7dabc71d3e758b1ec19ffb85639e427b',
                  'variables': json.dumps(variables)
                  }

    while len(edges) < total_count:
    # while len(edges) < 100:
        try:
            r_new = requests.get('https://www.instagram.com/graphql/query', query_para)
            page_data_new = json.loads(r_new.text)
            edges_new = page_data_new['data']['hashtag']['edge_hashtag_to_media']['edges']
            end_cursor2 = page_data_new['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            edges_new = fun.clean_data(edges_new)
            edges = edges + edges_new
            print(city[i] + ': {:f} - 子程序: {} - 任務{}'.format(len(edges) / total_count, os.getpid(), i))
            variables['after'] = end_cursor2
            query_para['variables'] = json.dumps(variables)
        except:
            time.sleep(2)
        a = np.array(edges)
        np.save('ig' + city[i] + '.npy', a)
        complete.append(len(edges) / total_count)


print("CPU核心數:{}".format(mp.cpu_count()))
print('當前母程序: {}'.format(os.getpid()))
start = time.time()
p = mp.Pool(mp.cpu_count())
p.map(need_to_crawler, range(len(city)))
print('等待所有子程序完成。')
p.close()
p.join()
end = time.time()
print("總共用時{}秒".format((end - start)))
