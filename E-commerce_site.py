# IMPORT THE RELEVANT LIBRARIES
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# START THE DRIVER
driver=webdriver.Chrome('E:/SPYDER/chromedriver.exe')

# GO THE WEBPAGE
driver.get('https://www.amazon.in/')
time.sleep(2)

# CREATE A VARIABLE CONTAINING THE NAME OF THE ITEM YOU WANT TO SEARCH
item='Laptops'

# ENTER THE ITEM NAME IN THE SEARCH BOX
input_box=driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
input_box.send_keys(item)
input_box.send_keys(Keys.ENTER)
time.sleep(3)

df=pd.DataFrame({'Brand':[''], 'Series':[''], 'Form_Factor':[''], 'Item_Weight':[''], 'Screen_Size':[''],
               'Processor_Brand':[''], 'Processor_Type':[''], 'Ram_size':[''],  
               'Battery_Life':[''], 'Operating_System':[''], 'Original_Price':[''], 'Discount_Price':[''], 'Ratings':['']})

soup=BeautifulSoup(driver.page_source, 'lxml')
while True:
    
    soup=BeautifulSoup(driver.page_source, 'lxml')
    postings=soup.find_all('div',{'data-component-type':'s-search-result'})[0:22]
    for post in postings:
        link=post.find('a',class_='a-link-normal a-text-normal').get('href')
       
        full_link='https://www.amazon.in/'+link
        driver.get(full_link)
        
        soup=BeautifulSoup(driver.page_source, 'lxml')
        
        table=soup.find('table',{'id':'productDetails_techSpec_section_1'})
        
        sec=table.find_all('tr')
        for rows in sec:
            ar=rows.find('th',class_='a-color-secondary a-size-base prodDetSectionEntry')
            if (ar.text.strip()=='Brand'):
                brand=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()

            if (ar.text.strip()=='Series' or ar.text.strip()=='Model Name' ):
                series=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
                
            if (ar.text.strip()=='Standing screen display size'):
                screen_size=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            
            if (ar.text.strip()=='Processor Brand'):
                processor_brand=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
                
            if (ar.text.strip()=='Processor Type'):
                processor_type=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
                
            if (ar.text.strip()=='RAM Size'):
                r_size=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            
             
            if (ar.text.strip()=='Average Battery Life (in hours)' or ar.text.strip()=='Battery Average Life' ):
                battery_life=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            
            if (ar.text.strip()=='Operating System'):
                os=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            try:
                if(ar.text.strip()=='Item Weight'):
                    item_wt=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            except:
                item_wt='NA'
                
            try:
                rating=soup.find('span',{'data-hook':'rating-out-of-text'}).text.strip()
            except:
                rating='NA'
            try:
                if (ar.text.strip()=='Form Factor'):
                    form_factor=rows.find('td',class_='a-size-base prodDetAttrValue').text.strip()
            except:
                form_factor='NA'
                
        price_table=soup.find('table',class_='a-lineitem')
        try:
            ori_price=price_table.find('span', class_='priceBlockStrikePriceString a-text-strike').text
        except:
            ori_price='NA'
        try:
            sell_price=price_table.find('span',{'id':'priceblock_ourprice'}).text.strip()
        except:
            sell_price='NA'
             
        df=df.append({'Brand':brand, 'Series':series, 'Form_Factor':form_factor, 'Item_Weight':item_wt, 'Screen_Size':screen_size, 
                      'Processor_Brand':processor_brand, 'Processor_Type':processor_type, 'Ram_size':r_size, 
                      'Battery_Life':battery_life, 'Operating_System':os, 'Original_Price':ori_price, 'Discount_Price':sell_price, 'Ratings':rating},ignore_index=True )
        
        driver.back()
       
    try:
        s=BeautifulSoup(driver.page_source, 'lxml')    
        ast=s.find('ul',class_='a-pagination')
        np=ast.find('li',class_='a-last')
        next_page=np.find('a').get('href')
        url='https://www.amazon.in/'+next_page
        driver.get(url)
        
    except:
        break
  

df.to_csv('E:\SPYDER\Project_Datasets\E-commerce_site.csv',sep=';')