
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import re
import requests
import pandas as pd
from splinter import Browser


# In[2]:


def prepareSoup(url):
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    return soup


# In[3]:


def openBrowser(url):
    #get_ipython().system('which chromedriver')
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    return browser
    


# In[4]:
def scrape():
    data={}

    soup = prepareSoup('https://mars.nasa.gov/news/')
    news_p = soup.findAll('div', class_='rollover_description_inner')[0].text.strip()
    data['news_para'] = news_p
    news_title = soup.findAll('div', class_='content_title')[0].find('a').text.strip()
    data['news_title'] = news_title



    # In[5]:


    #JPL Mars Space Images
    browser = openBrowser('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    ele = browser.find_by_id('full_image')
    ele.click()
    soup = bs(browser.html,'html.parser')
    details = soup.findAll('a',class_='button fancybox')[0].attrs
    featured_image_url = 'https://www.jpl.nasa.gov' + details['data-fancybox-href']
    data['featured_image_url'] = featured_image_url

    # In[6]:


    soup = prepareSoup('https://twitter.com/marswxreport?lang=en')
    divs = soup.findAll('div',class_='js-tweet-text-container')
    for div in divs:
        txt = div.find('p').text
        if(txt.startswith('Sol')):
            weather = txt
            break

    print(weather)
    data['weather'] = weather




    # In[7]:


    soup = prepareSoup('https://space-facts.com/mars/')
    values = soup.findAll('table')[0].findAll('td', class_='column-1')
    details = {}
    for x in range(len(values)-1):
        k = values[x].find('strong').text.replace(':','')
        v = soup.findAll('table')[0].findAll('td', class_='column-2')[x].text
        details[k] = v


    df = pd.DataFrame([details])
    data['mars_fact'] = details
    df


    # In[8]:


    table_df = df.to_html(index=False)


    # In[9]:


    #browser = openBrowser('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    #items = browser.find_by_xpath('//div[@class=\'item\']')
    #items[0].click()


    # In[10]:


    # Splinter click not working, using beasutiful soup approach
    soup = prepareSoup('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    divs = soup.find_all('div',class_='item')
    base_url = 'https://astrogeology.usgs.gov'
    img_list = []
    for div in divs:
        img_details = {}
        img_url = div.find('a')['href']
        int_soup = prepareSoup(base_url + img_url)
        img_details['title'] = int_soup.find('h2',class_='title').text
        img_details['img_url'] = int_soup.find_all('a',{'target':'_blank'})[0]['href']
        img_list.append(img_details)

    data['mars_hemisphere'] = img_list
    
    print(data)
    return data

