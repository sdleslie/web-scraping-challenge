# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd

def news1(browser):
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide",wait_time = 1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_element = soup.select_one("ul.item_list li.slide")
    news_title = news_element.find("div",class_ = "content_title").get_text()
    news_paragraph = news_element.find("div",class_ = "article_teaser_body").get_text()
    return news_title, news_paragraph

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info',wait_time = 1)
    # moreinfo = browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_source = soup.select_one('figure.lede a img').get('src')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_source
    return featured_image_url

def facts1(browser):
    tables = pd.read_html('https://space-facts.com/mars/')[0]
    tables.columns=['Parameter', 'Mars']
    tables.set_index('Parameter',inplace = True)
    facts = tables.to_html()
    return facts

def hemi(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemi_links = browser.find_by_css('div.item a.product-item h3')
    len(hemi_links)
    hemispheres = []
    for i in range(len(hemi_links)):
        hemi_dict = {}
        browser.find_by_css('div.item a.product-item h3')[i].click()
        image_url = browser.links.find_by_text("Sample").first['href']
        title = browser.find_by_css("h2.title").text
        hemi_dict["image_url"] = image_url
        hemi_dict["title"] = title
        hemispheres.append(hemi_dict)
        browser.back()
    return hemispheres

from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)
browser.driver.set_window_size(720, 480)

def scrape():
    news = news1(browser)
    feature = featured_image(browser)
    facts = facts1(browser)
    hemis = hemi(browser)
    # Close the browser after scraping
    browser.quit()
    marsdict = {"news":news,"featured_image":feature,"facts":facts,"hemisphere_images":hemis}
    return marsdict
