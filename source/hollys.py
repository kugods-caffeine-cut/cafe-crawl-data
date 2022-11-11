import urllib3
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import datetime
from selenium.webdriver.common.keys import Keys

import re

cwd = os.getcwd()
print(cwd)
html = 'https://www.hollys.co.kr/menu/espresso.do'     
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()
driver.get(html)

driver.implicitly_wait(3) 

data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]

# 더보기 한 번 누르기
driver.find_element(By.XPATH,'//*[@id="contents"]/div[2]/div[38]/a').send_keys(Keys.ENTER)
    
bsObject = bs(driver.page_source, "html.parser")    
menu_list_li = bsObject.select('ul#menuSmallList > li')

table=bsObject.select('tbody > tr')
for i in range (len(menu_list_li)):  # i : 0~17
    item = menu_list_li[i]
    # driver.find_element(By.XPATH,'//*[@id="menuSmallList"]/li['+str(i+1)+']/a').send_keys(Keys.ENTER)
    # bsObject = bs(driver.page_source, "html.parser") 
    name = bsObject.select('table > caption')[i].text
    temp = table[i].select('th')[0].text
    kcal = int(re.findall('\d+',table[i].select('td')[0].text)[0])
    caffeine = int(re.findall('\d+',table[i].select('td')[5].text)[0])   
    img = bsObject.select('li > a > img')[i+22].get('src')
    size='Regular'
    
    data['item'].append({"drink_name" : name, "temp" : temp, "img":img, "size":size, "kcal":kcal,  "caffeine":caffeine})
    data['count'] += 1
    

with open((cwd+"/data/data_hollys.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)

print('done')