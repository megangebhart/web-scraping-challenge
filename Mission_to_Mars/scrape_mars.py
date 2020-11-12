from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re

def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    slides = soup.find_all('li', class_='slide')
    content_title = slides[0].find('div', class_='content_title')
    news_title = content_title.text.strip()

    article_teaser_body = slides[0].find('div', class_='article_teaser_body')
    news_p = article_teaser_body.text.strip()

    # JPL Mars Space Images
    base_url = 'https://www.jpl.nasa.gov'
    url = base_url + '/spaceimages/?search=&category=Mars'

    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    image_url=soup.find(class_ = "button fancybox")["data-fancybox-href"]
    featured_image_url = base_url + image_url
    
    # Mars facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)

    mars_df = facts_table[0]
    mars_df.columns = ['Fact', 'Value']
    mars_df['Fact'] = mars_df['Fact'].str.replace(':', '')
    
    mars_facts_html = mars_df.to_html()
        
    # Mars Hemispheres

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html_hemispheres = browser.html
    soup = bs(html_hemispheres , 'html.parser')

    hemisphere_image_urls=[]
    products = soup.find ('div', class_='result-list')
    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup = bs(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Assigning scraped data to a page
    
    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["mars_facts_html"] = mars_facts_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
print(scrape())