from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

import time
import random
import re
import os
import csv
import math

# create user agent at random
ua = UserAgent()
userAgent = ua.random

#add options
opts = Options()
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
opts.add_argument("--disable-notifications")
opts.add_argument(f'user-agent={userAgent}')
opts.add_argument("--headless")

#open driver
driver = webdriver.Chrome(options=opts)

driver.delete_all_cookies()

## for writing the first row of the csv using DictWriter
full = ['SBD','Name','CMND','Toán', 'Ngữ văn', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD', 'KHTN', 'KHXH', 'Tiếng Anh', 'Tiếng Pháp', 'Tiếng Trung', 'Tiếng Nhật', 'Tiếng Đức','Tiếng Nga', 'Tiếng Hàn']



column_dict = dict(zip(full,full))
if os.path.isfile(f'index.txt') and os.path.isfile(f'score2021.csv'):
    index = int(open('index.txt').read())
    csv_file = open(f'score2021.csv', 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=full)
else:
    index = 2000001
    csv_file = open(f'score2021.csv', 'w', encoding='utf-8', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=full)
    writer.writerow(column_dict)

try:
    for i in range(index,2089275):
        print(i)
        index=i
        sbd_dict = {}

        driver.implicitly_wait(10)
        driver.get('http://diemthi.hcm.edu.vn/Home')
        input = driver.find_element_by_xpath('//input[@id="SoBaoDanh"]')
        input.send_keys(str(0)+str(i))
        submit_btn = driver.find_element_by_xpath('//input[@value="Xem điểm"]')
        submit_btn.click()

        list=[]
        try:
            table = driver.find_element_by_xpath("//table")
            for r, row in enumerate(table.find_elements_by_xpath(".//tr")):
                if r<1 :
                    continue
                list.append([td.text for td in row.find_elements_by_xpath(".//td")])
        except:
            pass

        try:
            sbd_dict["SBD"] = str(0)+str(i)
            sbd_dict["Name"] = list[0][0]
            sbd_dict["CMND"] = list[0][1]
        except:
            pass


        try:
            split_sq = list[0][2].split(':', 1)
            for x in range(1, 15):
                s = split_sq[1].strip().split(' ',1)
                sbd_dict[split_sq[0].strip()] = s[0]
                split_sq = s[1].split(':',1)
        except:
            pass

        writer.writerow(sbd_dict)
        # time.sleep(5)



except Exception as e:
    ## write the index so the script knows where where it left off
    print(e)
    print(sbd_dict)
    open('index.txt', 'w').write('%d' % (index))
    csv_file.close()
    driver.quit()
    quit()
