from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import requests


def scrapes():
    executable_path = {'executable_path': '/Users/hunterblock/Downloads/chromedriver'}

    browser = Browser('chrome', **executable_path)

    news_title, news_paragraph = marsnews(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured(browser),
        "hemispheres": hemispheres(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }    

    browser.quit()
    return data

def marsnews(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html

    news_soup = BeautifulSoup(html, 'html.parser')

    slide_elem = news_soup.select_one('ul.item_list li.slide')

    title = slide_elem.find("div", class_= 'content_title').get_text()
    content = slide_elem.find("div", class_= 'article_teaser_body').get_text()

    return title, content

def featured(browser):
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2) 

    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    html = browser.html
    img = BeautifulSoup(html, "html.parser")
    img_url = img.select_one('figure.lede a img').get('src')

    img_url_fin = f"https://www.jpl.nasa.gov{img_url}"

    return img_url_fin

def hemispheres(browser):
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)

    image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
    
        fullres = browser.links.find_by_text("Sample")
        hemisphere["image_url"] = fullres["href"]

        hemisphere["title"] = browser.find_by_css("h2.title").text

        image_urls.append(hemisphere)

        browser.back()


    return image_urls

def mars_facts():
    df = pd.read_html('https://space-facts.com/mars/')[0]

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)   

    #df.to_html()
    df = df.to_html()
    
    return df

if __name__ == "__main__":
    print(scrapes())
