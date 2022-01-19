#!/usr/bin/env python
# coding: utf-8

# In[213]:


import requests
from bs4 import BeautifulSoup
import re
import csv

domain = 'https://www.npo.org.tw/'
latest_page = 'https://www.npo.org.tw/npolist.aspx?nowPage=1&tid=146&Orgnpo_SubType=%E8%80%81%E4%BA%BA%E7%A6%8F%E5%88%A9'

output_file_name = 'collection.csv'

	
#讀取清單目錄 html
result = requests.get(latest_page)
bs = BeautifulSoup(result.text,'html.parser')

#爬取清單目錄中最後一頁頁數
last_page = bs.find('a',{'title':'最後一頁'})

	
last_page_url = last_page.get('href')
#print(last_page_url)

last_page = re.findall('Page=\d+', last_page_url).pop()
#print(last_page)

last_page_number = re.findall('\d+', last_page).pop()
#print(last_page_number)
urls = []
info_urls = []

base_url = 'https://www.npo.org.tw/npolist.aspx?nowPage=$&tid=146&Orgnpo_SubType=%E8%80%81%E4%BA%BA%E7%A6%8F%E5%88%A9'

	
#將所有清單目錄頁面網址餵給陣列變數urls
for page in range(1, int(last_page_number)+1):
    #print(page) 
    url = base_url.replace('$',str(page))
    #print(url)
    urls.append(url)
    #print(urls)

#爬取各清單目錄中所有機構代碼
for url in urls:
    result = requests.get(url)
    bs = BeautifulSoup(result.text,'html.parser')
    page_blocks = bs.findAll('td',{'data-th':'機構代碼'})
    for page_block in page_blocks:
        #print(page_block.text)
        
        #將所有機構頁面網址餵給陣列變數info_urls
        info_base_url = 'https://www.npo.org.tw/orgnpointroduction.aspx?tid=200&orgid=$'
        info_url = info_base_url.replace('$',str(page_block.text))
        #print(info_url)
        info_urls.append(info_url)
        #print(info_urls)

#建立csv檔案作為資料存取端        
with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Attribute', 'Service', 'Contacts', 'Phone', 'Email', 'Website', 'Address'])

    #爬取各機構頁面中機構名稱、性質、服務項目、聯絡人、電話、Email、網址、地址等資訊
    for serial_no in info_urls:
        result = requests.get(serial_no)
        bs = BeautifulSoup(result.text,'html.parser')
        info_blocks = bs.findAll('div',{'class':'profile off'})
        #print(info_blocks)
        for info_block in info_blocks:

            name = bs.find('h3')
            #print(name.text)

            attribute = name.find_next_sibling('h3')
            #print(attribute.text)

            service = attribute.find_next_sibling('h3')
            #print(service.text)

            contacts = service.find_next_sibling('h3')
            #print(contacts.text)

            phone = contacts.find_next_sibling('h3')
            #print(phone.text)

            email = phone.find_next_sibling('h3')
            #print(email.text)

            web = email.find_next_sibling('h3')
            try:
                web_name = web.find('a')
                web_url = web_name.get('href')
                #print(web_url)

                address = web.find_next_sibling('h3')
                #print(address.text)
                
                #將爬取到的資料寫入csv檔案
                writer.writerow([name.text, attribute.text, service.text, contacts.text, phone.text, email.text, web_url, address.text])

            except:
                web_url = 'none'
                #print(web_url)
                address = email.find_next_sibling('h3')
                #print(address.text)
                writer.writerow([name.text, attribute.text, service.text, contacts.text, phone.text, email.text, web_url, address.text])
                continue
        
        
        

