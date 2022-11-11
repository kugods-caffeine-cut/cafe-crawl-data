import urllib3
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import datetime
import re



data = dict()
date = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S.%f초")
data["date"] = date
data["count"] = 0
data["item"] =[]
item_list = ['9200000004312', '9200000004279', '9200000002487', '9200000000479', '9200000002081', '9200000000487', '9200000003509', '9200000003661', '9200000002672', '9200000000038', '9200000001636', '9200000003285', '9200000001635', '106509', '2', '128401', '128198', '9200000004313', '30', '25', '110563', '94', '110582', '126197', '110601', '38', '9200000004119', '9200000001086', '9200000001939', '9200000002095', '128692', '9200000004120', '9200000001941', '128695', '9200000004292', '110569', '9200000004291', '41', '110566', '110572', '46', '128192', '9200000002406', '110612', '9200000004308', '9200000002950', '9200000003505', '9200000003506', '9200000002953', '20', '9200000004310', '9200000004311', '9200000004309', '110611', '9200000001631', '110614', '9200000002760', '168004', '168007', '168016', '168010', '168013', '168054', '9200000002088', '9200000002090', '9200000002502', '168066', '9200000002403', '167004', '9200000003276', '169001', '9200000004295', '9200000003763', '9200000003766', '107025', '9200000004121', '107051', '107031', '9200000004270', '9200000004276', '9200000004267', '9200000004273', '4004000000056', '9200000004306', '4004000000059', '4004000000039', '9200000000229', '9200000002959', '4004000000019', '400400000094', '4004000000079', '4004000000069', '4004000000036', '9200000000226', '9200000002956', '4004000000016', '9200000000187', '400400000091', '4004000000076', '4004000000066', '9200000004307', '9200000000190', '9200000004294', '9200000004293', '9200000002963', '9200000004305', '9200000004303', '9200000002966', '9200000004304', '9200000002499', '135612', '9200000003234', '9200000002496', '135608', '9200000003233', '72', '110621', '9200000003658', '9200000002594', '9200000003659', '17', '9200000001302', '18', '9200000001301', '9300000004407', '9300000004348', '9300000004346', '9300000004347', '5210008070', '5210008061', '9300000003773', '9300000003774', '9300000003771', '9300000003772', '5210008072', '5210008074', '9300000003776', '5210008055', '9300000002565', '9300000003775', '5210008063', '9300000004239', '9300000004238']


cwd = os.getcwd()
print(cwd)
html = 'https://www.starbucks.co.kr/menu/drink_list.do'
detail_html="https://www.starbucks.co.kr/menu/drink_view.do?product_cd="
# driver = webdriver.Chrome(os.path.join(cwd, "/chromedriver"))
driver = webdriver.Chrome(cwd + "/chromedriver")
driver.implicitly_wait(2) #로딩시간에 따라 변경하거나, 없애도 됨


for loop in range(132,len(item_list)): 


    #Open every item in detail page
    driver.get(detail_html+item_list[loop])
    driver.implicitly_wait(5) #로딩시간에 따라 변경하거나, 없애도 됨

    bsObject = bs(driver.page_source, "html.parser")  

    #Title
    title =bsObject.select('h4')[0].text
    name= ""
    try:
        pattern = '([ㄱ-ㅣ가-힣][a-zA-Z0-9_.+-]+)' 
        index = re.search(pattern=pattern, string=title).start()
        name = title[:(index+1)]
    except:
        name = title
    
    caffeine =bsObject.select('li.caffeine dd')[0].text
    kcal = ""
    try:
        kcal = bsObject.select('li.kcal dd')[0].text
    except ValueError:
        bsObject = bs(driver.page_source, "html.parser")  
        kcal = bsObject.select('li.kcal dd')[0].text
        
        
    #size 
    size = ""
    size_err_flg = False
    try:
        size = bsObject.select('div#product_info01')[0].text.split()[0]
        size_in_kor = re.findall(r'[ㄱ-ㅣ가-힣]+', size)
        if len(size_in_kor) > 0:
            size = size_in_kor[0]
    except IndexError:    
        print('Idx ERR...')
        size = "톨"
        size_err_flg = True

    #img
    img = ""
    try:
        img_tag = bsObject.select('div.product_thum_wrap img')[0]
        img = img_tag.get("src")
    except:
        img = ""
    item = dict()
    item["drink_name"] = name
    item["img"]=img 
    item["temp"]=""
    item["size"]=size
    item["kcal"] = int(kcal) 
    item["caffeine"] = int(caffeine)
    if(size_err_flg):
        item["error"] = ["SIZE ERROR"]
    # data['item'].append()
    # data['count'] += 1
    print("drink_name : " + name+ "\nimg :"+img +  "\ntemp : """+""+ "\nsize :"+size +"\nkcal : "+kcal +  "\ncaffeine : "+ caffeine)
    
    #push item into ./data/data.json
    with open((cwd+"/../drink-data/data_starbucks.json"),"r",encoding='utf-8') as file:
        JsonFile = json.load(file)
        JsonFile["count"] += 1
        JsonFile["item"].append(item)
    with open((cwd+"/../drink-data/data_starbucks.json"),"w",encoding='utf-8') as file:
        json.dump(JsonFile, file, indent='\t', ensure_ascii=False)
    print("Item  "+str(loop+1)+"/"+str(len(item_list))+" done")








    
    
# //*[@id="board_page"]/li[3]/a #1p 기준 2p
# //*[@id="board_page"]/li[5]/a #2p기준 3p
# //*[@id="board_page"]/li[6]/a #3p 기준 4p
# //*[@id="board_page"]/li[7]/a #4p 기준 5p

