import urllib3
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os
import time
import datetime
import re

cwd = os.getcwd()
print(cwd)
html = 'https://www.ediya.com/contents/drink.html#c'     
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()
driver.get(html)
driver.implicitly_wait(3) 
prev_height = driver.execute_script('return document.body.scrollHeight')

data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]

#22번 더보기 누르기
for i in range(22):
    driver.find_element(By.LINK_TEXT,'더보기+').click();

bsObject = bs(driver.page_source, "html.parser") 

menu_list_li = bsObject.select('ul#menu_ul > li')

for item in menu_list_li:
    name = item.select('h2')[0].text

    name_list=name.split(' ')
    if name_list[0]=='(EX)':
        size='엑스트라'
    elif '이디야' in name_list:
        size='병음료'
    else :
        size = '레귤러'

    temp=""
    if 'HOT' in name_list:
        temp='HOT'
    elif 'ICED' in name_list:
        temp='ICE'

    name=re.sub('[^ ㄱ-ㅣ가-힣+]','',name).strip()
    kcal=re.sub(r'[^0-9]', '',str(item.select('dl > dd')[0]))

    img = ''
    caffeine=re.sub(r'[^0-9]', '',str(item.select('dl > dd')[4]))

    data['item'].append({"drink_name" : name, "temp" : temp, "img":img, "size":size, "kcal":kcal,  "caffeine":caffeine})
    data['count'] += 1
    

with open((cwd+"/data/data_ediya.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)

print('done')