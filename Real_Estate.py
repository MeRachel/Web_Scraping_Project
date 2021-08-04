from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver=webdriver.Chrome('E:/SPYDER/chromedriver.exe')

driver.get('https://www.99acres.com/NRI-Real-Estate.htm')

rent=driver.find_element_by_xpath('//*[@id="ResRentTab"]').click()
location=driver.find_element_by_xpath('//*[@id="keyword"]')
location.send_keys('Bengaluru')
location.send_keys(Keys.ENTER)
time.sleep(3)
c=1
df=pd.DataFrame({'Property_Name':[''], 'About':[''], 'Rent':[''], 'Area':[''], 'Bedrooms':[''], 
                 'Bathroom':[''], 'Posted_By':['']})
soup=BeautifulSoup(driver.page_source, 'lxml')
while True:
    soup=BeautifulSoup(driver.page_source, 'lxml')
    
    postings=soup.find_all('div',{'class':'srpTuple__cardWrap'})
    for post in postings:
        
        try:
            prop_name=post.find('td',{'class':'list_header_bold srpTuple__spacer10'}).text.strip()
        except:
            prop_name='NA'
        try:
            post_by=post.find('div',class_='caption_strong_small').text.strip()
        except:
            post_by='NA'
        try:
            abt=post.find('a',class_='body_med srpTuple__propertyName').text.strip()
        except:
            abt='NA'
        try:
            rent=post.find('td',{'id':'srp_tuple_price'}).text.strip()
        except:
            rent='NA'
        try:
            area=post.find('td',{'id':'srp_tuple_primary_area'}).text.strip()
        except:
            area='NA'
        try:
            bed_no=post.find('td',{'id':'srp_tuple_bedroom'}).text.strip()
        except:
            bed_no='NA'
            
        try:
            bath_no=post.find('div',{'id':'srp_tuple_bathroom'}).text.strip()
        except:
            bath_no='NA'
            
        df=df.append({'Property_Name':prop_name, 'About':abt, 'Rent':rent, 'Area':area, 'Bedrooms':bed_no, 
                 'Bathroom':bath_no, 'Posted_By':post_by},ignore_index=True)
    
    
    try:
        soup=BeautifulSoup(driver.page_source, 'lxml')    
        ast=soup.find('div',class_='Pagination__srpPagination')
        if c==1:
            next_page=ast.find('a',class_='list_header_bold')
            next_link=next_page.get('href')
            
        else:
            next_page1=ast.find_all('a',class_='list_header_bold')[1]
            next_link=next_page1.get('href')
            
        url=next_link
        c+=1
        driver.get(url)
        time.sleep(3)
        
    except:
        break
df.to_csv('E:\SPYDER\Project_Datasets\Real_Estate.csv',sep=';') 
            
        
        