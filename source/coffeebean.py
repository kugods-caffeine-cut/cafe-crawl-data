import urllib3
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import datetime

cwd = os.getcwd()
print("current path: ", cwd)
htmls = []    
for i in range(1,4): # https://www.coffeebeankorea.com/menu/list.asp?category=13
    htmls.append('https://www.coffeebeankorea.com/menu/list.asp?page='+ str(i) +'&category=13&category2=1')
htmls.append('https://www.coffeebeankorea.com/menu/list.asp?category=12')
htmls.append('https://www.coffeebeankorea.com/menu/list.asp?category=14')

# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()


data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]

with open((cwd+"/data/data_coffeebean.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)

for html in htmls:

    driver.get(html)
    bsObject = bs(driver.page_source, "html.parser")    

    menu_list_li = bsObject.select('#contents > div > div > ul > li')

    for item in menu_list_li:
        img = 'https://www.coffeebeankorea.com/data/menu'+item.select('img')[0].get('src')
        name = item.select('span')[1].text
        temp = ''
        size='스몰'

        try :
            kcal=int(item.select('div > dl')[0].select('dt')[0].text)
            caffeine=int(item.select('div > dl')[4].select('dt')[0].text)
        except:
            kcal=''
            caffeine =''   
             
        data['item'].append({"drink_name" : name, "temp":temp, "img":img, "size":size, "kcal":kcal,  "caffeine":caffeine})
        data['count'] += 1

    
          
        
    with open((cwd+"/data/data_coffeebean.json"),"r",encoding='utf-8') as file:
        JsonFile = json.load(file)
        JsonFile["count"] += data["count"]
        JsonFile["item"] += data["item"]

        data["item"] = []
        data["count"] = 0
        
    with open((cwd+"/data/data_coffeebean.json"),"w",encoding='utf-8') as file:
        json.dump(JsonFile, file, indent='\t', ensure_ascii=False)


    print(html + "  done")


    
    
