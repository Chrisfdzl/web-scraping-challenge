#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[5]:


# Dependencies and Setup
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re

from splinter import browser
from selenium import webdriver

def scrape():

# In[6]:


# Set Executable Path & Initialize Chrome Browser
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# In[7]:


#scrape the NASA Mars News SIte, collect news title, paragraph text, assign
#to variables for later reference
url = "https://mars.nasa.gov/news/" 
response = req.get(url)

soup = bs(response.text, 'html5lib')

title = soup.find("div", class_="content_title").text
paragraph_text = soup.find("div", class_="rollover_description_inner").text


# In[8]:


#print(soup.prettify())
print(f"Title: {title}")
print(f"Paragraph: {paragraph_text}")


# ## JPL Mars Space Images - Featured Image
# 

# In[9]:


#Visit the URL for JPL's Space images
#splinter to navigate the site and find the image url for the current featured
#image and assign it to featured_image_url (use .jpg)
executable_path = {'executable_path' : 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[13]:


html = browser.html
soup = bs(html, "html.parser")


# In[15]:


browser.click_link_by_partial_text('FULL IMAGE')
#time.sleep(5)


# In[16]:


browser.click_link_by_partial_text('more info')


# In[17]:


new_html = browser.html
new_soup = bs(new_html, 'html.parser')
temp_img_url = new_soup.find('img', class_='main_image')
back_half_img_url = temp_img_url.get('src')

recent_mars_image_url = "https://www.jpl.nasa.gov" + back_half_img_url

print(recent_mars_image_url)


# ## Mars Weather

# #####  Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

# In[18]:


twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
twitter_soup = bs(twitter_response.text, 'html.parser')


# In[19]:


tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")


# In[20]:


print(tweet_containers[0].text)
p = tweet_containers[0].text
type(p)


# In[21]:


for tweets in tweet_containers:
    if tweets.text:
        print(tweets.text)
        break


# In[22]:


for i in range(10):
    tweets = tweet_containers[i].text
    if "Sol " in tweets:
        print(tweets)
        break


# ## Mars Facts

# ##### Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

# In[23]:


#convert pandas table to html table string. 
request_mars_space_facts = req.get("https://space-facts.com/mars/")


# In[24]:


mars_space_table_read = pd.read_html(request_mars_space_facts.text)


# In[25]:


mars_space_table_read
df = mars_space_table_read[0]
df


# In[26]:


df.set_index(0, inplace=True)


# In[27]:


mars_data_df = df
mars_data_df


# In[28]:


mars_data_html = mars_data_df.to_html()
mars_data_html


# In[29]:


mars_data_html.replace('\n', '')


# In[30]:


mars_data_df.to_html('mars_table.html')


# # Mars Hemispheres

# ##### Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.

# In[37]:


executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[38]:


hemisphere_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()


# In[39]:


hemisphere_image_urls


# In[ ]:


  # Assigning scraped data to a page
    
    marspage = {}
    marspage["title"] = title
    marspage["news_p"] = paragraph_text
    marspage["featured_image_url"] = featured_image_url
    marspage["tweet_containers"] = mars_weather
    marspage["mars_data_html"] = marsfacts_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
