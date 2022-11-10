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
htmls=[]
htmls.append('https://composecoffee.com/board_koTk88/category/185'     
)
htmls.append('https://composecoffee.com/board_koTk88/category/186')  # 더치커피


# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()

data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]

for html in htmls:
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






    # Parse html
    bsObject = bs(driver.page_source, "html.parser") 

    menu_list_li = bsObject.select('div#masonry-container > div')

    for item in menu_list_li:

        name=item.select('h4')[0].text.strip()
        try : 
            temp = re.findall('[a-zA-Z]+',name)[0]
        except:
            temp=''
        name=re.sub('[a-zA-Z]+','',item.select('h4')[0].text.strip()).strip()   
        img='https://composecoffee.com/'+item.select('div#rthumbnail img')[0].get('src')
        size='One size'
    

        try:
            kcal=int(re.findall(r'\d+',item.select('ul li')[3].text.strip())[0])
        except:
            kcal=''

        
        try :
            caffeine= int(re.findall(r'\d+',item.select('ul li')[0].text.strip())[1])
        except:
            try :
                caffeine= int(re.findall(r'\d+',item.select('ul li')[1].text.strip())[1])
            except:
                try:
                    caffeine= int(re.findall(r'\d+',item.select('ul li')[2].text.strip())[1])
                except:
                    caffeine= int(re.findall(r'\d+',item.select('ul li')[3].text.strip())[1])

        data['item'].append({"drink_name" : name, "temp" : temp, "img":img, "size":size, "kcal":kcal,  "caffeine":caffeine})
        data['count'] += 1
        

with open((cwd+"/data/data_compose-coffee.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)

print('done')