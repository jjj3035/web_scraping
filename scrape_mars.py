
# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape():
    mars_data = {}
    # # NASA Mars News

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
  
    # Extract title text
    news_items = soup.find_all(class_='slide')
    news_title = news_items[0].find(class_='content_title').text

    # Print paragraph texts
    news_p = news_items[0].find(class_='rollover_description_inner').text
        
    mars_data["latest_mars_news"] = {"news_title":news_title, "news_p":news_p}


    # # JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    
    soup = bs(html, 'html.parser')
    articles = soup.find_all('article', class_='carousel_item')

    for article in articles:
        footer = article.find('footer')
        featured_image_url = 'https://www.jpl.nasa.gov' + footer.a['data-fancybox-href']
    mars_data["featured_image_url"] = featured_image_url


    # # Mars Weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')
    results = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather = []
    for result in results:
        if "Sol" in result.text:
            weather.append(result.text)
    mars_weather = weather[0]
    mars_data["mars_weather"] = mars_weather

    # # Mars Facts

    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables
    df = tables[0]
    df.columns = ["Description", "Value"]
    df.set_index("Description", inplace=True)

    html_table = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    html_table.replace('\n', '')
    df.to_html('table.html')
    
    mars_data["mars_facts"] = html_table

    # # Mars Hemisperes
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all(class_='item')
    hemisphere_image_urls = []
    for result in results:
        title = result.find('h3').text
        browser.visit('https://astrogeology.usgs.gov/' + result.find('a')['href'])
        html = browser.html
        soup = bs(html, 'html.parser')
        response = soup.find_all(class_='downloads')[0]
        img_url = (response.a)['href']
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    return mars_data

if __name__ == "__main__":
    scrape()
