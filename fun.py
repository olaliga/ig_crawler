from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

def crawler(url,param = None):  # ,cookie):
    chromedriver = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver,options=options)
    driver.get(url)  # 前往這個網址
    back = driver.page_source
    driver.close() # , cookies = cookie)
    return back


def clean_data(data):
    for i in range(len(data)):
        data[i] = data[i]['node']
        del data[i]['thumbnail_src']
        del data[i]['thumbnail_resources']
    return data