# Import the relevant libraries
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# Start the driver 
driver=webdriver.Chrome('E:/SPYDER/chromedriver.exe')

# Go the Webpage
driver.get('https://in.indeed.com/?r=us')

job='Data Analyst'
region='India'
# Input the Job title
what=driver.find_element_by_xpath('//*[@id="text-input-what"]')
what.send_keys(job)

# Input the Location
where=driver.find_element_by_xpath('//*[@id="text-input-where"]')
where.send_keys(region)

# Click the button to get the results
button=driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button').click()
time.sleep(3) # wait for the whole page to load for 5 secs

# Initialise the dataframe
df=pd.DataFrame({'Link':[''], 'Title':[''], 'Comapny':[''], 'Location':[''], 'Salary':[''], 'Rating':[''], 'Posting_Date':['']})

# Extracting the required data for analyis
# First creating a loop which will go through all the pages and extract the postings
while True:
    # This will extract the HTML of the entire page displayed in Python
    soup=BeautifulSoup(driver.page_source,'lxml') 
    
    # Get the HTML of the all the individual postings
    postings=soup.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
    for post in postings:
        try:
            link=post.find('a',class_='jobtitle turnstileLink').get('href')
            full_link='https://in.indeed.com/'+link
            company=post.find('span',{'class':'company'}).text.strip()
            title=post.find('h2',{'class':'title'}).text.strip()
            date=post.find('span',class_='date date-a11y').text.strip()
        except:
            pass
        try:
            location=post.find('span',class_='location accessible-contrast-color-location').text.strip()
        except:
            location='N/A'
        try:
            rating=post.find('span',class_='ratingsContent').text.strip()
        except:
            rating='N/A'
        try:
            salary=post.find('span',class_='salaryText').text.strip()
        except:
            salary='N/A'
        df=df.append({'Link':full_link, 'Title':title, 'Comapny':company, 'Location':location, 'Salary':salary, 'Rating':rating, 'Posting_Date':date},ignore_index=True)  
    # To get to the next page, if any 
    try:
        next_page=soup.find('a', attrs = {'aria-label': 'Next'}).get('href')
        next_page_full='https://in.indeed.com/'+next_page
        url=next_page_full
        driver.get(url)
    except:
        break
#Save the dataframe to a .csv file
df.to_csv('E:\SPYDER\Project_Datasets\Indeed_Project_1.csv')