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
# opts.add_argument("--headless")

#open driver
driver = webdriver.Chrome(options=opts)

driver.delete_all_cookies()

## for writing the first row of the csv using DictWriter
full = ['STT','Cụm Thi','Họ Tên','SBD','Ngày sinh','Giới tính','Toán (D1)', 'Ngữ văn (D2)', 'Vật lí (D3)', 'Hóa học (D4)', 'Sinh học (D5)', 'KHTN (D6)', 'Lịch sử (D7)','Địa lí (D8)', 'GDCD (D9)', 'KHXH (D10)', 'Ngoại ngữ (D11)','D12']


if os.path.isfile(f'index.txt') and os.path.isfile(f'score2021.csv') and os.path.isfile(f'index2.txt'):
    index = int(open('index.txt').read())
    index2 = int(open('index2.txt').read())
    csv_file = open(f'score2021.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
else:
    index = 1
    index2 = 1000001
    csv_file = open(f'score2021.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(full)
newindex=index
driver.get('https://thanhnien.vn/giao-duc/tuyen-sinh/2020/tra-cuu-diem-thi-thpt-quoc-gia.html')
list= []
check_dup_list=[]
try:
    for x in range(index,64):
        count = 0
        if newindex != index:
            index2 = 1000001
        for y in range (index2,1999999):
            if count == 5:
                raise Exception
            if x<10:
                i = str(0) + str(x)+ str(y)[1:]
            else:
                i = str(x) + str(y)[1:]
            print(i)
            index=x
            index2=y
            sbd_dict = {}

            driver.implicitly_wait(6)
            input = driver.find_element_by_xpath('//input[@id="txtkeyword"]')
            input.clear()
            input.send_keys(i)
            input.send_keys(Keys.RETURN)
            time.sleep(1)

            cnt = 0
            while list == check_dup_list:
                if cnt >= 5:
                    count += 1
                    writer.writerow(['', '', '', i])
                    break
                try:
                    table = driver.find_element_by_xpath("//tbody[@id='resultcontainer']")
                    for r, row in enumerate(table.find_elements_by_xpath(".//tr")):
                        list = [[td.text for td in row.find_elements_by_xpath(".//td")]]
                        time.sleep(.5)
                    cnt+=1
                except:
                    continue

            if list != check_dup_list:
                writer.writerow(list[0])
                count = 0

            check_dup_list = list


            # time.sleep(5)



except Exception as e:
    ## write the index so the script knows where where it left off
    print(e)
    print(list)
    open('index.txt', 'w').write('%d' % (index))
    open('index2.txt', 'w').write('%d' % (index2))

    csv_file.close()
    driver.quit()
    quit()
