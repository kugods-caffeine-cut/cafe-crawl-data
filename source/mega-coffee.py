import urllib3
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import datetime
import re


cwd = os.getcwd()
print(cwd)
html = 'https://www.mega-mgccoffee.com/menu/?menu_category1=1&menu_category2=1'     
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨
driver.maximize_window()
driver.get(html)


for loop in range(1, 7):
    driver.implicitly_wait(3) 

    # prev_height = driver.execute_script('return document.body.scrollHeight')
    # #스크롤 내리기 -> 필요 없을 시, 없애도 무방함.
    # for i in range(10):
    #     driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    #     time.sleep(1)

    #     current_height = driver.execute_script('return document.body.scrollHeight')

    #     if prev_height == current_height:
    #         break
    #     time.sleep(3)
    
    
    data = dict()
    date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
    data["date"] = date
    data["count"] = 0
    data["item"] =[]
    
    # Parse html
    bsObject = bs(driver.page_source, "html.parser")    
    menu_list_li = bsObject.select('ul#menu_list>li')
    for item in menu_list_li:
        temp = item.select('a.inner_modal_open div.cont_gallery_list_label')[0].text
        name = item.select('a.inner_modal_open div.text1')[0].text.strip()
        img = item.select('img')[0].get('src')
        size = item.select('div.inner_modal>div.cont_text_box>div.cont_text>div.cont_text_inner')[2].text.strip().split('/ ')[-1]
        
        kcal_str = item.select('div.inner_modal>div.cont_text_box>div.cont_text>div.cont_text_inner')[3].text.strip().split(' ')[2]
        kcal = float(re.findall(r'\d+.\d', kcal_str)[0])
        caffeine_str = item.select('ul>li')[4].text.strip()
        caffeine = int(re.findall(r'\d+', caffeine_str)[0])
        data['item'].append({"drink_name" : name, "img":img, "temp":temp, "size":size, "kcal":kcal,  "caffeine":caffeine})
        data['count'] += 1

    #push item into ./data/data.json
    if loop == 1:
        with open((cwd+"/data/megacoffee.json"),"w",encoding='utf-8') as file:
            json.dump(data, file, indent='\t', ensure_ascii=False)
        driver.find_element(By.XPATH, '//*[@id="board_page"]/li[6]/a').click()
        print("page "+str(loop)+" done")
        continue
    else:
        with open((cwd+"/data/megacoffee.json"),"r",encoding='utf-8') as file:
            JsonFile = json.load(file)
            JsonFile["count"] += data["count"]
            JsonFile["item"] += data["item"]

        with open((cwd+"/data/megacoffee.json"),"w",encoding='utf-8') as file:
            json.dump(JsonFile, file, indent='\t', ensure_ascii=False)

    if loop<5:        
        driver.find_element(By.XPATH,'//*[@id="board_page"]/li[7]/a').click()
    else:
        driver.find_element(By.XPATH,'//*[@id="board_page"]/li[5]/a').click()

    print("page "+str(loop)+" done")


# //*[@id="board_page"]/li[5]/a
# //*[@id="board_page"]/li[7]
# //*[@id="board_page"]/li[3]/a #1p 기준 2p
# //*[@id="board_page"]/li[5]/a #2p기준 3p
# //*[@id="board_page"]/li[6]/a #3p 기준 4p
# //*[@id="board_page"]/li[7]/a #4p 기준 5p

