import time 
from bs4 import BeautifulSoup
from csv import writer

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def Livemint_articles_list(inputkey):
    options = Options()
    options.headless = False
    driver = webdriver.Chrome('./chromedriver', options=options)

    driver.get("https://www.livemint.com/")
    driver.find_element_by_xpath("//a[@onclick='topSearch()']").click()
    driver.find_element_by_id("searchParameter").clear()
    driver.find_element_by_id("searchParameter").send_keys(inputkey)
    driver.find_element_by_id("searchParameter").send_keys(Keys.ENTER)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1 
    screen_height = driver.execute_script("return window.screen.height;") # get the screen height of the web
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

    page_source = driver.page_source

    soup = BeautifulSoup(page_source)
    articles = []
    articleLists = soup.find_all('div', class_='listingNew clearfix')
    for article in articleLists:
        article_div = article.find('div', class_='listtostory clearfix').find('div', class_='headlineSec')
        headline = article_div.find('h2', class_='headline').find('a')
        headlinetxt = headline.get_text()
        headlineURL = headline['href']

        datespan = article_div.find('span', class_='fl date').find_all('span')[1]
        dateTime = datespan['data-updatedtime']
        List = [dateTime, headlinetxt, headlineURL]
        # To store data to CSV. 
        # with open(inputkey+'data.csv', 'a') as f_object:
        #     writer_object = writer(f_object)
        #     writer_object.writerow(List)
        #     f_object.close()
        articles.append(List)
    
    return articles