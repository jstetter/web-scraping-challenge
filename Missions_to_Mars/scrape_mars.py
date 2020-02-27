#!/usr/bin/env python
# coding: utf-8

# Import Dependencies

# In[104]:


from bs4 import BeautifulSoup as bs
import requests
import pandas
from splinter import Browser
import time

def scrape():
# In[105]:
    scraped_data = {}

    executable_path = 'chromedriver.exe'
    browser = Browser('chrome', executable_path, headless=False)


    # ## NASA Mars News

    # Open Browser and visit NASA news page

    # In[106]:


    url = 'https://mars.nasa.gov/news/'


    # In[107]:


    browser.visit(url)
    time.sleep(2)


    # Save HTML into a variable to be parsed with Beautiful Soup

    # In[108]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # Pull latest article title and decription

    # In[109]:


    title = soup.find('div', class_='content_title').text
    description = soup.find('div', class_= 'article_teaser_body').text

    scraped_data['Title']=title
    scraped_data['Description']=description
    # ## JPL Mars Space Images - Featured Image

    # In[110]:


    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(2)


    # In[111]:


    button = browser.find_by_id('full_image')
    button.click()
    time.sleep(2)


    # In[112]:


    image = browser.html
    soup = bs(image, "html.parser")


    # In[113]:


    base = 'jpl.nasa.gov'
    image_url = soup.find("img", class_="fancybox-image")["src"]
    image_url = base + image_url

    scraped_data['Recent Image'] = image_url
    # ## Mars Weather

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    tweets = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    mars_weather = tweets[41].text

    scraped_data['Weather'] = mars_weather
    # ## Mars Facts

    # In[119]:


    facts_url = 'https://space-facts.com/mars/'


    # In[120]:


    tables = pandas.read_html(facts_url)


    # In[121]:


    facts = tables[0]


    # In[122]:


    facts = facts.rename(columns={0:'Metric', 1:'Value'})
    facts = facts.set_index('Metric')


    # In[123]:


    mass = facts.loc['Mass:']['Value']
    diameter = facts.loc['Equatorial Diameter:']['Value']

    scraped_data['Mass'] = mass
    scraped_data['Diameter'] = diameter
    # ## Mars Hemispheres

    # In[124]:


    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)


    # In[125]:


    time.sleep(2)


    # In[126]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[127]:


    hemispheres = soup.find_all('h3')


    # In[128]:


    img_urls = soup.find_all('a', class_='itemLink product-item')


    # In[129]:


    hrefs = [img.get('href') for img in img_urls]


    # In[130]:


    base = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = [
        {'title': hemispheres[0].text, 'img_url': base + hrefs[0]},
        {'title':hemispheres[1].text, 'img_url': base + hrefs[2]},
        {'title':hemispheres[2].text,'img_url': base + hrefs[4]},
        {'title':hemispheres[3].text,'img_url': base + hrefs[6]},
    ]


    # In[131]:


    hemisphere_image_urls


    # Kind of an odd way to do this but I realized I didn't get the right image urls and didn't want to throw away the work

    # In[132]:


    browser.visit(hemisphere_image_urls[0]['img_url'])
    time.sleep(2)
    html=browser.html

    soup=bs(html, 'html.parser')

    urls = soup.find_all('a', target='_blank')
    hemisphere_image_urls[0]['img_url']=urls[0].get('href')


    # In[133]:


    browser.visit(hemisphere_image_urls[1]['img_url'])
    time.sleep(2)
    html=browser.html

    soup=bs(html, 'html.parser')

    urls = soup.find_all('a', target='_blank')
    hemisphere_image_urls[1]['img_url']=urls[0].get('href')


    # In[134]:


    browser.visit(hemisphere_image_urls[2]['img_url'])
    time.sleep(2)
    html=browser.html

    soup=bs(html, 'html.parser')

    urls = soup.find_all('a', target='_blank')
    hemisphere_image_urls[2]['img_url']=urls[0].get('href')


    # In[135]:


    browser.visit(hemisphere_image_urls[3]['img_url'])
    time.sleep(2)
    html=browser.html

    soup=bs(html, 'html.parser')

    urls = soup.find_all('a', target='_blank')
    hemisphere_image_urls[3]['img_url']=urls[0].get('href')


    # In[136]:


    scraped_data['Hemispheres'] = hemisphere_image_urls
    return scraped_data

# In[ ]:




