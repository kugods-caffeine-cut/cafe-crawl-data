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
html = 'https://mo.twosome.co.kr'     
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.set_window_size(960,1080)

driver.implicitly_wait(5)#로딩시간에 따라 변경하거나, 없애도 됨
html_item = ['/mn/menuInfoDetail.do?menuCd=10191427', '/mn/menuInfoDetail.do?menuCd=10191382', '/mn/menuInfoDetail.do?menuCd=10191381', '/mn/menuInfoDetail.do?menuCd=10191380', '/mn/menuInfoDetail.do?menuCd=10100001', '/mn/menuInfoDetail.do?menuCd=10100002', '/mn/menuInfoDetail.do?menuCd=10100003', '/mn/menuInfoDetail.do?menuCd=10100004', '/mn/menuInfoDetail.do?menuCd=10100005', '/mn/menuInfoDetail.do?menuCd=10100007', '/mn/menuInfoDetail.do?menuCd=10100009', '/mn/menuInfoDetail.do?menuCd=10100008', '/mn/menuInfoDetail.do?menuCd=10100010', '/mn/menuInfoDetail.do?menuCd=10100017', '/mn/menuInfoDetail.do?menuCd=10100018', '/mn/menuInfoDetail.do?menuCd=10100019', '/mn/menuInfoDetail.do?menuCd=10100020', '/mn/menuInfoDetail.do?menuCd=10100021', '/mn/menuInfoDetail.do?menuCd=10100022', '/mn/menuInfoDetail.do?menuCd=10191275', '/mn/menuInfoDetail.do?menuCd=10201655', '/mn/menuInfoDetail.do?menuCd=10201654', '/mn/menuInfoDetail.do?menuCd=10201656', '/mn/menuInfoDetail.do?menuCd=10201638', '/mn/menuInfoDetail.do?menuCd=10201639', '/mn/menuInfoDetail.do?menuCd=10201604', '/mn/menuInfoDetail.do?menuCd=10200027', '/mn/menuInfoDetail.do?menuCd=10200028', '/mn/menuInfoDetail.do?menuCd=10200025', '/mn/menuInfoDetail.do?menuCd=10200026', '/mn/menuInfoDetail.do?menuCd=10201605', '/mn/menuInfoDetail.do?menuCd=10200029', '/mn/menuInfoDetail.do?menuCd=10200030', '/mn/menuInfoDetail.do?menuCd=10200035', '/mn/menuInfoDetail.do?menuCd=10200079', '/mn/menuInfoDetail.do?menuCd=10200033', '/mn/menuInfoDetail.do?menuCd=10200034', '/mn/menuInfoDetail.do?menuCd=10200031', '/mn/menuInfoDetail.do?menuCd=10200032', '/mn/menuInfoDetail.do?menuCd=10200024', '/mn/menuInfoDetail.do?menuCd=10301872', '/mn/menuInfoDetail.do?menuCd=10301763', '/mn/menuInfoDetail.do?menuCd=10301764', '/mn/menuInfoDetail.do?menuCd=10300051', '/mn/menuInfoDetail.do?menuCd=10300049', '/mn/menuInfoDetail.do?menuCd=10300050', '/mn/menuInfoDetail.do?menuCd=10301794', '/mn/menuInfoDetail.do?menuCd=10300041', '/mn/menuInfoDetail.do?menuCd=10301781', '/mn/menuInfoDetail.do?menuCd=10300044', '/mn/menuInfoDetail.do?menuCd=10300042', '/mn/menuInfoDetail.do?menuCd=10300043', '/mn/menuInfoDetail.do?menuCd=10300048', '/mn/menuInfoDetail.do?menuCd=10300039', '/mn/menuInfoDetail.do?menuCd=10300040', '/mn/menuInfoDetail.do?menuCd=10300045', '/mn/menuInfoDetail.do?menuCd=10300046', '/mn/menuInfoDetail.do?menuCd=10300047', '/mn/menuInfoDetail.do?menuCd=10301834', '/mn/menuInfoDetail.do?menuCd=10300036', '/mn/menuInfoDetail.do?menuCd=10300056', '/mn/menuInfoDetail.do?menuCd=10300057', '/mn/menuInfoDetail.do?menuCd=10300037', '/mn/menuInfoDetail.do?menuCd=10300038', '/mn/menuInfoDetail.do?menuCd=10300053', '/mn/menuInfoDetail.do?menuCd=10300054', '/mn/menuInfoDetail.do?menuCd=10300055']

for loop in range(0, len(html_item)):
    driver.get(html + html_item[loop])
    driver.implicitly_wait(5) 
        
    prev_height = driver.execute_script('return document.body.scrollHeight')
        #스크롤 내리기 -> 필요 없을 시, 없애도 무방함.
    for i in range(10):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)

                current_height = driver.execute_script('return document.body.scrollHeight')

                if prev_height == current_height:
                    break

    driver.find_element('xpath','/html/body/div[1]/div/div/div[2]/section[1]/div[1]/button').click()


    time.sleep(3)
    
    bsObject = bs(driver.page_source, "html.parser") 
    temp = bsObject.find_all('li', attrs = {'name':'ondoOptLi'})
  
    for temp_sel in range(1, len(temp)+1):
        driver.find_element('xpath','//*[@id="layer-info-popup"]/div[1]/ul/li['+str(temp_sel)+']').click()

        bsObject = bs(driver.page_source, "html.parser") 

        
        # Parse html
        bsObject = bs(driver.page_source, "html.parser")
        time.sleep(3)
        
        item = dict()
        title = bsObject.select('dl.menu-detail-info-title strong')[0].text
        kcal = bsObject.select("div.custom-layer-wrap.popupIn-wrap.mt-110 > article > div.menu-detail-dl-wrap > dl:nth-child(3) > dd")[0].text
        caffeine = 0
        try:
            caffeine = int(bsObject.select("div.custom-layer-wrap.popupIn-wrap.mt-110 > article > div.menu-detail-dl-wrap > dl:nth-child(8) > dd")[0].text)
        except:
            caffeine = 0
        img_tag = bsObject.select('div.swiper-wrapper img')[0]
        img = img_tag.get("src")
        size = ""
        try:
            size = bsObject.select('ul.no-line-bottom li a')[0].text
        except IndexError:
            size = "레귤러"
            item["error"] = ["size"]


        temp_str = ""
        if "핫" in temp[temp_sel-1].text  :
            temp_str = "HOT"
        elif "아이스" in temp[temp_sel-1].text:
            temp_str = "ICE"
        
        item = dict()
        item["drink_name"] = title
        item["img"]=img 
        item["temp"]=temp_str
        item["size"]=size
        item["kcal"] = int(kcal) 
        item["caffeine"] = int(caffeine)
        
        
        #push item into ./data/data.json
    
        with open((cwd+"/../drink-data/data_twosome.json"),"r",encoding='utf-8') as file:
            JsonFile = json.load(file)
            JsonFile["count"] += 1
            JsonFile["item"].append(item)
        with open((cwd+"/../drink-data/data_twosome.json"),"w",encoding='utf-8') as file:
            json.dump(JsonFile, file, indent='\t', ensure_ascii=False)

        print("page "+str(loop+1)+"/"+str(len(html_item)+1)+" \n\tver : "+str(temp_sel)+"/"+str(len(temp))+" done")


    
    
# //*[@id="board_page"]/li[3]/a #1p 기준 2p
# //*[@id="board_page"]/li[5]/a #2p기준 3p
# //*[@id="board_page"]/li[6]/a #3p 기준 4p
# //*[@id="board_page"]/li[7]/a #4p 기준 5p

