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
html = 'https://tomntoms.com/menu/menu.html'     
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()
driver.get(html)



driver.implicitly_wait(3) 

prev_height = driver.execute_script('return document.body.scrollHeight')
#스크롤 내리기 -> 필요 없을 시, 없애도 무방함.
for i in range(10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)

            current_height = driver.execute_script('return document.body.scrollHeight')

            if prev_height == current_height:
                break
time.sleep(3)



data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]

#11번 더보기 누르기
for i in range(11):
    driver.find_element(By.XPATH,'//*[@id="plusmode_tb_product_paging_area"]/button').send_keys(Keys.ENTER)

# Parse html
bsObject = bs(driver.page_source, "html.parser") 

menu_list_li = bsObject.select('div#plusmode_tb_product_listbody > div')


for item in menu_list_li:

    name = item.select('div.title-bx h3.tit')[0].text.strip()
    item_data=re.findall('<span>(.+?)</span>',str(menu_list_li[12].select('tbody')[0]))


    size = '정보 없음'
    j=0
    for i in item_data:
        j+=1
        if i=='1회 제공량':
            size=item_data[j].strip().split('ml')[0]

    kcal = 0
    j=0
    for i in item_data:
        j+=1
        if i=='열량':
            kcal=item_data[j]    

    caffeine=0
    j=0
    for i in item_data:
        j+=1
        if i=='카페인':
            caffeine=item_data[j].split('mg')[0]


    temp=""
    img=""

    data['item'].append({"drink_name" : name, "temp" : temp, "img":img, "size":(size.strip()), "kcal":kcal.strip(),  "caffeine":caffeine})
    data['count'] += 1
    

with open((cwd+"/data/data_tomntoms.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)

print('done')