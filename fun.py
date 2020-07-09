from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

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

def login(url,username,password):
    chromedriver = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver,options=options)
    driver.get(url)  # 前往這個網址
    wait = WebDriverWait(driver, 10)
    second_page_flag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "KPnG0")))  # util login page appear
    e = driver.find_element(By.NAME, "username")
    e.send_keys(username)
    e = driver.find_element(By.NAME, "password")
    time.sleep(5)
    e.send_keys(password)
    time.sleep(5)
    e = driver.find_element(By.CLASS_NAME, "sqdOP.L3NKy.y3zKF")
    e.click()
    time.sleep(5) # util page appear
    e = driver.find_element(By.CLASS_NAME, "sqdOP.yWX7d.y3zKF")
    e.click()
    back = driver.page_source
    driver.close() # , cookies = cookie)
    return back


def clean_data(data):
    for i in range(len(data)):
        data[i] = data[i]['node']
        del data[i]['thumbnail_src']
        del data[i]['thumbnail_resources']
    return data