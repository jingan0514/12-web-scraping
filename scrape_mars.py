import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    # NASA Mars News
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_news_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title_res = soup.find('div', class_='content_title')
    news_title = title_res.find('a').text
    p_res = soup.find('div', class_='article_teaser_body')
    news_p = p_res.text

    listings['news_title'] = news_title
    listings['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    featured_space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_space_image_url)
    time.sleep(1)

    xpath = '//div[@class="img"]'
    browser.find_by_xpath(xpath).click()
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    listings['featured_image_url'] = featured_image_url

    # Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('div', class_='js-tweet-text-container').\
                        find('p').find(text=True).strip().\
                        replace('\n', ', ')

    listings['mars_weather'] = mars_weather

    # Mars Facts
    mars_fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_fact_url)

    df = tables[1]
    df.columns = ['parameter', 'value']
    df.set_index('parameter', inplace = True)

    mars_fact_table = df.to_html()

    listings['mars_fact_table'] = mars_fact_table

    # Mars Hemispheres
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    titles = [soup.find_all('h3')[x].text.replace('Enhanced', '').strip() for x in range(len(soup.find_all('h3')))]
    hemisphere_image_urls = []
    img_urls = []
    for x in range(len(titles)):
        browser.visit(mars_hemispheres_url)
        browser.click_link_by_partial_text(titles[x])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_urls.append(soup.find('li').find('a')['href'])

    hemisphere_image_urls = [{'title': titles[x], "img_url": img_urls[x]} for x in range(len(titles))]

    listings['hemisphere_image_urls'] = hemisphere_image_urls
    
    return listings
